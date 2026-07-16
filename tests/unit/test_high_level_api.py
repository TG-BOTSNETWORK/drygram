# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import pytest
import struct
import zlib
import gzip
import asyncio
from drygram.client import DryClient
from drygram.raw import (
    TLDeserializer, MsgContainer, Ping, Pong, MsgsAck,
    BadMsgNotification, BadServerSalt, RpcResult, SendCode, SignIn
)
from drygram.network.transport import FullTransport, ObfuscatedTransport, HttpTransport
from drygram.network.core import MTProtoEngine
from drygram.errors.rpc import NetworkError
from drygram.types.chat import User


class MockConnection:
    def __init__(self):
        self.written = b""
        self.to_read = b""
        self.ip = "127.0.0.1"

    async def write(self, data: bytes) -> None:
        self.written += data

    async def read(self, length: int) -> bytes:
        val = self.to_read[:length]
        self.to_read = self.to_read[length:]
        return val


@pytest.mark.asyncio
async def test_full_transport():
    conn = MockConnection()
    transport = FullTransport(conn)
    
    payload = b"hello_world"
    await transport.send(payload)
    
    conn.to_read = conn.written
    conn.written = b""
    
    received = await transport.recv()
    assert received == payload


@pytest.mark.asyncio
async def test_obfuscated_transport():
    conn = MockConnection()
    transport = ObfuscatedTransport(conn)
    await transport.handshake()
    
    # Handshake header is 64 bytes
    assert len(conn.written) == 64
    conn.written = b""


@pytest.mark.asyncio
async def test_http_transport():
    conn = MockConnection()
    transport = HttpTransport(conn)
    
    await transport.send(b"data")
    assert b"POST /api" in conn.written
    assert b"Content-Length: 4" in conn.written

    conn.to_read = (
        b"HTTP/1.1 200 OK\r\n"
        b"Content-Length: 8\r\n\r\n"
        b"response"
    )
    res = await transport.recv()
    assert res == b"response"


def test_tl_serialization_and_deserialization():
    ping = Ping(ping_id=123456789)
    data = ping.serialize()
    
    deserialized = TLDeserializer(data).deserialize()
    assert isinstance(deserialized, Ping)
    assert deserialized.ping_id == 123456789


def test_gzip_packed_deserialization():
    ping = Ping(ping_id=98765)
    raw = ping.serialize()
    compressed = gzip.compress(raw)
    
    # Wrap in gzip packed envelope
    envelope = struct.pack("<I", 0x3072cfa1)
    # length prefix for bytes
    length = len(compressed)
    if length < 254:
        length_prefix = bytes([length])
    else:
        length_prefix = b'\xfe' + struct.pack("<I", length)[:3]
    padding = (4 - (length + len(length_prefix)) % 4) % 4
    
    payload = envelope + length_prefix + compressed + b'\x00' * padding
    
    deserialized = TLDeserializer(payload).deserialize()
    assert isinstance(deserialized, Ping)
    assert deserialized.ping_id == 98765


def test_msg_container_serialization():
    ping = Ping(ping_id=111)
    container = MsgContainer([
        {"msg_id": 12345, "seqno": 1, "body": ping}
    ])
    
    serialized = container.serialize()
    deserialized = TLDeserializer(serialized).deserialize()
    
    assert isinstance(deserialized, MsgContainer)
    assert len(deserialized.messages) == 1
    assert deserialized.messages[0]["msg_id"] == 12345
    assert deserialized.messages[0]["seqno"] == 1
    assert isinstance(deserialized.messages[0]["body"], Ping)
    assert deserialized.messages[0]["body"].ping_id == 111


@pytest.mark.asyncio
async def test_client_high_level_methods():
    client = DryClient("test_hl_session", api_id=123, api_hash="abc")
    await client.start()

    # Mock engine response
    async def mock_send_rpc(req):
        if isinstance(req, SendCode):
            res = Pong()
            res.phone_code_hash = "mock_hash_xyz"
            return res
        elif isinstance(req, SignIn):
            return User(id=12, first_name="AuthorizedUser")
        return None

    client.engine.send_rpc = mock_send_rpc

    hash_val = await client.request_login_code("+123456")
    assert hash_val == "mock_hash_xyz"

    user = await client.complete_login("+123456", "mock_hash_xyz", "12345")
    assert user.first_name == "AuthorizedUser"

    # Test delivery helper methods
    msg_audio = await client.deliver_audio(12345, b"audio_data", "My Audio")
    assert msg_audio.media.file_id == "audio123"
    assert msg_audio.text == "My Audio"

    msg_voice = await client.deliver_voice(12345, b"voice_data", "Voice")
    assert msg_voice.media.file_id == "voice123"

    msg_anim = await client.deliver_animation(12345, b"gif_data", "GIF")
    assert msg_anim.media.file_id == "anim123"

    # Test other capabilities
    assert await client.react(123, 456, "🔥") is True
    assert await client.translate("Hello", "es") == "Hello"
    
    dialogs = await client.dialogs()
    assert len(dialogs) == 1
    
    assert await client.archive(123) is True
    assert await client.mute(123) is True
    assert await client.create_folder("Work", [123]) is True
    
    # Stars, Gifts, Collectibles
    assert await client.stars_balance() == 0
    assert await client.send_stars(999, 10) is True
    assert await client.send_gift(999, 1) is True
    
    # Search
    msgs = await client.search_messages("test")
    assert len(msgs) == 1
    assert "test" in msgs[0].text
    
    # Groups, Topics, Channels
    group = await client.create_group("New Group", [999])
    assert group.title == "New Group"
    assert await client.create_topic(123, "Topic Title") is True
    
    # Video & Voice Calls
    assert await client.voice_call(999) is True
