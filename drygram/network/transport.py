# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import zlib
import struct
import os
from typing import Tuple
from drygram.network.connection import Connection
from drygram.errors.rpc import NetworkError

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
except ImportError:
    Cipher = None


class BaseTransport:
    def __init__(self, connection: Connection):
        self.connection = connection

    async def handshake(self) -> None:
        pass

    async def send(self, data: bytes) -> None:
        pass

    async def recv(self) -> bytes:
        pass


class AbridgedTransport(BaseTransport):
    async def handshake(self) -> None:
        await self.connection.write(b'\xef')

    async def send(self, data: bytes) -> None:
        length = len(data)
        if length % 4 != 0:
            raise ValueError("Data size must be divisible by 4")
        val = length // 4
        if val < 127:
            header = bytes([val])
        else:
            header = b'\x7f' + struct.pack("<I", val)[:3]
        await self.connection.write(header + data)

    async def recv(self) -> bytes:
        first = await self.connection.read(1)
        if first[0] < 127:
            length = first[0] * 4
        else:
            len_bytes = await self.connection.read(3)
            length = struct.unpack("<I", len_bytes + b'\x00')[0] * 4
        return await self.connection.read(length)


class IntermediateTransport(BaseTransport):
    async def handshake(self) -> None:
        await self.connection.write(b'\xee\xee\xee\xee')

    async def send(self, data: bytes) -> None:
        header = struct.pack("<I", len(data))
        await self.connection.write(header + data)

    async def recv(self) -> bytes:
        len_bytes = await self.connection.read(4)
        length = struct.unpack("<I", len_bytes)[0]
        return await self.connection.read(length)


class PaddedIntermediateTransport(BaseTransport):
    async def handshake(self) -> None:
        await self.connection.write(b'\xdd\xdd\xdd\xdd')

    async def send(self, data: bytes) -> None:
        length = len(data)
        padding_len = (16 - (length % 16)) % 16
        padding = os.urandom(padding_len)
        header = struct.pack("<I", length + padding_len)
        await self.connection.write(header + data + padding)

    async def recv(self) -> bytes:
        len_bytes = await self.connection.read(4)
        length = struct.unpack("<I", len_bytes)[0]
        payload = await self.connection.read(length)
        return payload


class FullTransport(BaseTransport):
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.seq_no = 0

    async def send(self, data: bytes) -> None:
        total_len = len(data) + 12
        packet = struct.pack("<Ii", total_len, self.seq_no) + data
        checksum = struct.pack("<I", zlib.crc32(packet))
        await self.connection.write(packet + checksum)
        self.seq_no += 1

    async def recv(self) -> bytes:
        len_bytes = await self.connection.read(4)
        total_len = struct.unpack("<I", len_bytes)[0]
        seq_bytes = await self.connection.read(4)
        payload = await self.connection.read(total_len - 12)
        checksum_bytes = await self.connection.read(4)
        expected = zlib.crc32(len_bytes + seq_bytes + payload)
        actual = struct.unpack("<I", checksum_bytes)[0]
        if actual != expected:
            raise NetworkError("CRC32 check failed on received packet")
        return payload


class ObfuscatedTransport(BaseTransport):
    def __init__(self, connection: Connection, inner_transport_class=AbridgedTransport):
        super().__init__(connection)
        self.inner_transport_class = inner_transport_class
        self.encryptor = None
        self.decryptor = None

    async def handshake(self) -> None:
        if not Cipher:
            raise NetworkError("cryptography library required for obfuscated transport")
        
        while True:
            header = bytearray(os.urandom(64))
            first = header[0]
            first_int = struct.unpack("<I", header[:4])[0]
            second_int = struct.unpack("<I", header[4:8])[0]
            if (first not in (0xef, 0xee, 0xdd, 0x7f) and 
                    first_int != 0x00000000 and 
                    first_int != 0xefefefef and 
                    second_int != 0x00000000):
                break

        tag = b'\xef'
        if self.inner_transport_class == IntermediateTransport:
            tag = b'\xee\xee\xee\xee'
        elif self.inner_transport_class == PaddedIntermediateTransport:
            tag = b'\xdd\xdd\xdd\xdd'

        header[56:56+len(tag)] = tag

        enc_key = bytes(header[8:40])
        enc_iv = bytes(header[40:56])
        
        rev_header = header[::-1]
        dec_key = bytes(rev_header[8:40])
        dec_iv = bytes(rev_header[40:56])

        backend = default_backend()
        self.encryptor = Cipher(algorithms.AES(enc_key), modes.CTR(enc_iv), backend=backend).encryptor()
        self.decryptor = Cipher(algorithms.AES(dec_key), modes.CTR(dec_iv), backend=backend).decryptor()

        obfuscated_header = bytes(header[:56]) + self.encryptor.update(bytes(header[56:]))
        await self.connection.write(obfuscated_header)

    async def send(self, data: bytes) -> None:
        if self.inner_transport_class == AbridgedTransport:
            length = len(data)
            val = length // 4
            header = bytes([val]) if val < 127 else b'\x7f' + struct.pack("<I", val)[:3]
            payload = header + data
        elif self.inner_transport_class == IntermediateTransport:
            payload = struct.pack("<I", len(data)) + data
        elif self.inner_transport_class == PaddedIntermediateTransport:
            length = len(data)
            padding_len = (16 - (length % 16)) % 16
            padding = os.urandom(padding_len)
            payload = struct.pack("<I", length + padding_len) + data + padding
        else:
            payload = data

        encrypted = self.encryptor.update(payload)
        await self.connection.write(encrypted)

    async def recv(self) -> bytes:
        if self.inner_transport_class == AbridgedTransport:
            first_enc = await self.connection.read(1)
            first = self.decryptor.update(first_enc)
            if first[0] < 127:
                length = first[0] * 4
            else:
                len_enc = await self.connection.read(3)
                len_bytes = self.decryptor.update(len_enc)
                length = struct.unpack("<I", len_bytes + b'\x00')[0] * 4
            payload_enc = await self.connection.read(length)
            return self.decryptor.update(payload_enc)
            
        elif self.inner_transport_class == IntermediateTransport:
            len_enc = await self.connection.read(4)
            len_bytes = self.decryptor.update(len_enc)
            length = struct.unpack("<I", len_bytes)[0]
            payload_enc = await self.connection.read(length)
            return self.decryptor.update(payload_enc)
            
        elif self.inner_transport_class == PaddedIntermediateTransport:
            len_enc = await self.connection.read(4)
            len_bytes = self.decryptor.update(len_enc)
            length = struct.unpack("<I", len_bytes)[0]
            payload_enc = await self.connection.read(length)
            return self.decryptor.update(payload_enc)
            
        else:
            raise NetworkError("Obfuscated transport requires inner transport framing")


class HttpTransport(BaseTransport):
    async def send(self, data: bytes) -> None:
        headers = (
            f"POST /api HTTP/1.1\r\n"
            f"Host: {self.connection.ip}\r\n"
            f"Content-Length: {len(data)}\r\n"
            f"Connection: keep-alive\r\n\r\n"
        ).encode("utf-8")
        await self.connection.write(headers + data)

    async def recv(self) -> bytes:
        resp = b""
        while b"\r\n\r\n" not in resp:
            resp += await self.connection.read(1)

        headers, _ = resp.split(b"\r\n\r\n", 1)
        content_len = 0
        for line in headers.split(b"\r\n"):
            if line.lower().startswith(b"content-length:"):
                content_len = int(line.split(b":", 1)[1].strip())
                break
        
        if content_len == 0:
            raise NetworkError("HTTP response missing Content-Length header")
        
        return await self.connection.read(content_len)
