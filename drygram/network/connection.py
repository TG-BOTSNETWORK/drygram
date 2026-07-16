# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
import socket
from typing import Optional, Tuple
from drygram.errors.rpc import NetworkError

class Connection:
    def __init__(self, ip: str, port: int, use_ipv6: bool = False, timeout: float = 10.0):
        self.ip = ip
        self.port = port
        self.use_ipv6 = use_ipv6
        self.timeout = timeout
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

    async def connect(self) -> None:
        family = socket.AF_INET6 if self.use_ipv6 else socket.AF_INET
        try:
            connect_coro = asyncio.open_connection(
                host=self.ip,
                port=self.port,
                family=family
            )
            self.reader, self.writer = await asyncio.wait_for(connect_coro, timeout=self.timeout)
        except Exception as e:
            raise NetworkError(f"Failed to connect to {self.ip}:{self.port} - {str(e)}")

    async def write(self, data: bytes) -> None:
        if not self.writer:
            raise NetworkError("Connection is not established")
        try:
            self.writer.write(data)
            await self.writer.drain()
        except Exception as e:
            raise NetworkError(f"Failed to write data - {str(e)}")

    async def read(self, length: int) -> bytes:
        if not self.reader:
            raise NetworkError("Connection is not established")
        try:
            data = await self.reader.readexactly(length)
            return data
        except Exception as e:
            raise NetworkError(f"Failed to read data - {str(e)}")

    async def close(self) -> None:
        if self.writer:
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception:
                pass
            finally:
                self.writer = None
                self.reader = None
