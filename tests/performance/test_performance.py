# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import time
import pytest
import os
from drygram.raw import Ping, TLDeserializer
from drygram.crypto.cipher import Cipher
from drygram.sessions.sqlite import SQLiteSession


def test_tl_serialization_performance():
    ping = Ping(ping_id=99999)
    
    start = time.perf_counter()
    for _ in range(1000):
        data = ping.serialize()
        _ = TLDeserializer(data).deserialize()
    end = time.perf_counter()
    
    duration = end - start
    # Ensure 1000 serializations/deserializations take less than 0.5s
    assert duration < 0.5


def test_aes_encryption_performance():
    key = os.urandom(32)
    # IV for AES-IGE must be 32 bytes
    iv = os.urandom(32)
    # Data length must be a multiple of 16 for AES-IGE
    data = b"benchmark_data_payload_aes_performance" * 8
    
    start = time.perf_counter()
    for _ in range(1000):
        enc = Cipher.encrypt_ige(data, key, iv)
        _ = Cipher.decrypt_ige(enc, key, iv)
    end = time.perf_counter()
    
    duration = end - start
    assert duration < 0.5


@pytest.mark.asyncio
async def test_sqlite_throughput_performance():
    session = SQLiteSession("perf_test_db")
    await session.load()
    
    start = time.perf_counter()
    for i in range(100):
        session.user_id = i
        await session.save()
    end = time.perf_counter()
    
    duration = end - start
    await session.delete()
    # 100 database writes should complete within a reasonable timeframe
    assert duration < 3.0
