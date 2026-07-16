# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from drygram.crypto.cipher import Cipher, TLSerializer, TLDeserializer
from drygram.network.connection import Connection
from drygram.network.proxy import ProxyConnection
from drygram.network.pool import ConnectionPool
from drygram.network.transport import AbridgedTransport, IntermediateTransport, PaddedIntermediateTransport

def test_aes_ige_crypt():
    key = b"0123456789abcdef0123456789abcdef"
    iv = b"0123456789abcdef0123456789abcdef"
    data = b"hello world 1234"
    enc = Cipher.encrypt_ige(data, key, iv)
    dec = Cipher.decrypt_ige(enc, key, iv)
    assert dec == data

def test_tl_serialization():
    val = "Hello MTProto"
    ser = TLSerializer.serialize_string(val)
    deser = TLDeserializer(ser)
    assert deser.deserialize_string() == val

@pytest.mark.asyncio
async def test_connection():
    mock_reader = AsyncMock()
    mock_reader.readexactly.return_value = b"testdata"
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = Connection("127.0.0.1", 80)
        await conn.connect()
        await conn.write(b"hello")
        data = await conn.read(8)
        assert data == b"testdata"
        await conn.close()

@pytest.mark.asyncio
async def test_socks5_proxy_connection():
    mock_reader = AsyncMock()
    mock_reader.readexactly.side_effect = [
        b"\x05\x00",
        b"\x05\x00\x00\x01",
        b"\x7f\x00\x00\x01",
        b"\x00\x50"
    ]
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "socks5", "127.0.0.1", 1080)
        await conn.connect()
        await conn.close()

@pytest.mark.asyncio
async def test_http_proxy_connection():
    mock_reader = AsyncMock()
    mock_reader.readexactly.side_effect = [
        b"HTTP/1.1 200 Connection Established\r\n\r\n"
    ]
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        conn = ProxyConnection("127.0.0.1", 80, "http", "127.0.0.1", 8080)
        await conn.connect()
        await conn.close()

@pytest.mark.asyncio
async def test_connection_pool():
    mock_reader = AsyncMock()
    mock_writer = MagicMock()
    mock_writer.drain = AsyncMock()
    
    with patch("asyncio.open_connection", return_value=(mock_reader, mock_writer)):
        pool = ConnectionPool("127.0.0.1", 80, pool_size=2)
        conn = await pool.acquire()
        assert conn is not None
        await pool.release(conn)
        await pool.close_all()

@pytest.mark.asyncio
async def test_transports():
    mock_conn1 = AsyncMock()
    mock_conn1.read.side_effect = [b"\x02", b"abcd"]
    mock_conn1.readexactly.side_effect = [b"\x01", b"abcd"]
    abridged = AbridgedTransport(mock_conn1)
    await abridged.handshake()
    await abridged.send(b"test")
    data = await abridged.recv()
    assert data == b"abcd"
    
    mock_conn2 = AsyncMock()
    mock_conn2.read.side_effect = [b"\x04\x00\x00\x00", b"test"]
    intermediate = IntermediateTransport(mock_conn2)
    await intermediate.handshake()
    await intermediate.send(b"test")
    data = await intermediate.recv()
    assert data == b"test"
    
    mock_conn3 = AsyncMock()
    mock_conn3.read.side_effect = [b"\x10\x00\x00\x00", b"test" + b"\x00"*12]
    padded = PaddedIntermediateTransport(mock_conn3)
    await padded.handshake()
    await padded.send(b"test")
    data = await padded.recv()
    assert data == b"test" + b"\x00"*12

def test_cipher_errors_and_extra_types():
    with pytest.raises(ValueError):
        Cipher.encrypt_ige(b"123", b"k"*32, b"i"*32)
    with pytest.raises(ValueError):
        Cipher.decrypt_ige(b"123", b"k"*32, b"i"*32)
        
    k, iv = Cipher.compute_keys(b"k"*256, b"m"*16, is_client=True)
    assert len(k) == 32
    assert len(iv) == 32
    
    long_val = 1234567890123
    long_ser = TLSerializer.serialize_long(long_val)
    assert TLDeserializer(long_ser).deserialize_long() == long_val
    
    double_val = 3.14159
    double_ser = TLSerializer.serialize_double(double_val)
    assert abs(TLDeserializer(double_ser).deserialize_double() - double_val) < 0.0001
    
    large_bytes = b"x" * 300
    large_ser = TLSerializer.serialize_bytes(large_bytes)
    assert TLDeserializer(large_ser).deserialize_bytes() == large_bytes

