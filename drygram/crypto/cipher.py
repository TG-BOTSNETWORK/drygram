# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import os
import hashlib
import struct
from typing import Tuple
from drygram.crypto.backend import encrypt_ige, decrypt_ige

class Cipher:
    @staticmethod
    def encrypt_ige(data: bytes, key: bytes, iv: bytes) -> bytes:
        return encrypt_ige(data, key, iv)

    @staticmethod
    def decrypt_ige(data: bytes, key: bytes, iv: bytes) -> bytes:
        return decrypt_ige(data, key, iv)

    @staticmethod
    def sha256(data: bytes) -> bytes:
        return hashlib.sha256(data).digest()

    @staticmethod
    def compute_keys(auth_key: bytes, msg_key: bytes, is_client: bool) -> Tuple[bytes, bytes]:
        x = 0 if is_client else 8
        sha256_a = hashlib.sha256(msg_key + auth_key[x:x+36]).digest()
        sha256_b = hashlib.sha256(auth_key[x+40:x+76] + msg_key).digest()
        aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
        aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]
        return aes_key, aes_iv

class TLSerializer:
    @staticmethod
    def serialize_int(val: int) -> bytes:
        return struct.pack("<i", val)

    @staticmethod
    def serialize_long(val: int) -> bytes:
        return struct.pack("<q", val)

    @staticmethod
    def serialize_double(val: float) -> bytes:
        return struct.pack("<d", val)

    @staticmethod
    def serialize_bytes(val: bytes) -> bytes:
        length = len(val)
        if length < 254:
            res = bytes([length]) + val
        else:
            res = b'\xfe' + struct.pack("<I", length)[:3] + val
        padding = (4 - len(res) % 4) % 4
        return res + b'\x00' * padding

    @staticmethod
    def serialize_string(val: str) -> bytes:
        return TLSerializer.serialize_bytes(val.encode("utf-8"))

class TLDeserializer:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def deserialize_int(self) -> int:
        val = struct.unpack_from("<i", self.data, self.offset)[0]
        self.offset += 4
        return val

    def deserialize_long(self) -> int:
        val = struct.unpack_from("<q", self.data, self.offset)[0]
        self.offset += 8
        return val

    def deserialize_double(self) -> float:
        val = struct.unpack_from("<d", self.data, self.offset)[0]
        self.offset += 8
        return val

    def deserialize_bytes(self) -> bytes:
        first = self.data[self.offset]
        if first < 254:
            length = first
            self.offset += 1
        else:
            length = struct.unpack_from("<I", self.data[self.offset:self.offset+4] + b'\x00')[0] >> 8
            self.offset += 4
        val = self.data[self.offset:self.offset+length]
        self.offset += length
        padding = (4 - (length + (1 if first < 254 else 4)) % 4) % 4
        self.offset += padding
        return val

    def deserialize_string(self) -> str:
        return self.deserialize_bytes().decode("utf-8")
