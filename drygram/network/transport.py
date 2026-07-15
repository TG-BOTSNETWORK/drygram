# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import os
import struct
from drygram.network.connection import Connection

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
