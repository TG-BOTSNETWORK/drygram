# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
import socket
import struct
from typing import Optional
from drygram.errors.rpc import NetworkError
from drygram.network.connection import Connection

class ProxyConnection(Connection):
    def __init__(
        self,
        ip: str,
        port: int,
        proxy_type: str,
        proxy_ip: str,
        proxy_port: int,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_ipv6: bool = False,
        timeout: float = 10.0
    ):
        super().__init__(proxy_ip, proxy_port, use_ipv6, timeout)
        self.target_ip = ip
        self.target_port = port
        self.proxy_type = proxy_type.lower()
        self.username = username
        self.password = password

    async def connect(self) -> None:
        await super().connect()
        if self.proxy_type == "socks5":
            await self._negotiate_socks5()
        elif self.proxy_type == "http":
            await self._negotiate_http()
        else:
            raise NetworkError(f"Unsupported proxy type: {self.proxy_type}")

    async def _negotiate_socks5(self) -> None:
        if self.username and self.password:
            await self.write(b'\x05\x02\x00\x02')
        else:
            await self.write(b'\x05\x01\x00')
        method_resp = await self.read(2)
        if method_resp[0] != 5:
            raise NetworkError("Invalid SOCKS5 version in greeting response")
        method = method_resp[1]
        if method == 2:
            if not self.username or not self.password:
                raise NetworkError("Proxy requires authentication but none provided")
            u_len = len(self.username)
            p_len = len(self.password)
            auth_req = b'\x01' + bytes([u_len]) + self.username.encode() + bytes([p_len]) + self.password.encode()
            await self.write(auth_req)
            auth_resp = await self.read(2)
            if auth_resp[0] != 1 or auth_resp[1] != 0:
                raise NetworkError("SOCKS5 authentication failed")
        elif method != 0:
            raise NetworkError("No acceptable SOCKS5 authentication method")
        
        try:
            ip_bytes = socket.inet_aton(self.target_ip)
            atype = b'\x01'
        except OSError:
            try:
                ip_bytes = socket.inet_pton(socket.AF_INET6, self.target_ip)
                atype = b'\x04'
            except OSError:
                host_bytes = self.target_ip.encode()
                ip_bytes = bytes([len(host_bytes)]) + host_bytes
                atype = b'\x03'

        port_bytes = struct.pack(">H", self.target_port)
        req = b'\x05\x01\x00' + atype + ip_bytes + port_bytes
        await self.write(req)
        
        resp = await self.read(4)
        if resp[0] != 5:
            raise NetworkError("Invalid SOCKS5 version in connect response")
        if resp[1] != 0:
            raise NetworkError(f"SOCKS5 connection failed with code {resp[1]}")
        
        res_atype = resp[3]
        if res_atype == 1:
            await self.read(4)
        elif res_atype == 3:
            domain_len = await self.read(1)
            await self.read(domain_len[0])
        elif res_atype == 4:
            await self.read(16)
        await self.read(2)

    async def _negotiate_http(self) -> None:
        host_port = f"{self.target_ip}:{self.target_port}"
        req = f"CONNECT {host_port} HTTP/1.1\r\nHost: {host_port}\r\n"
        if self.username and self.password:
            import base64
            auth_str = f"{self.username}:{self.password}"
            b64_auth = base64.b64encode(auth_str.encode()).decode()
            req += f"Proxy-Authorization: Basic {b64_auth}\r\n"
        req += "\r\n"
        await self.write(req.encode())
        
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = await self.read(1)
            resp += chunk
            if len(resp) > 4096:
                raise NetworkError("HTTP proxy response headers too long")
        
        status_line = resp.split(b"\r\n")[0].decode()
        if "200" not in status_line:
            raise NetworkError(f"HTTP proxy connection failed: {status_line}")
