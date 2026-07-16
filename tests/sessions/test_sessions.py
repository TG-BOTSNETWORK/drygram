# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import pytest
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from drygram import MemorySession, SQLiteSession, PostgresSession, RedisSession, MongoSession

@pytest.mark.asyncio
async def test_memory_session():
    sess = MemorySession("mem1")
    await sess.load()
    sess.auth_key = b"abc"
    await sess.save()
    assert sess.auth_key == b"abc"
    await sess.delete()
    assert sess.auth_key is None

@pytest.mark.asyncio
async def test_sqlite_session():
    db_file = "test_sess.session"
    if os.path.exists(db_file):
        os.remove(db_file)
    sess = SQLiteSession("sql1", db_path=db_file)
    await sess.load()
    sess.auth_key = b"123"
    sess.user_id = 999
    await sess.save()
    
    sess2 = SQLiteSession("sql1", db_path=db_file)
    await sess2.load()
    assert sess2.auth_key == b"123"
    assert sess2.user_id == 999
    
    await sess2.delete()
    assert sess2.auth_key is None
    
    if os.path.exists(db_file):
        os.remove(db_file)

@pytest.mark.asyncio
async def test_postgres_session():
    mock_conn = AsyncMock()
    mock_conn.fetchrow.return_value = {
        "dc_id": 2,
        "server_address": "127.0.0.1",
        "server_port": 88,
        "auth_key": b"key_pg",
        "user_id": 555,
        "is_bot": True
    }
    
    with patch("asyncpg.connect", return_value=mock_conn):
        sess = PostgresSession("pg_sess", dsn="postgresql://localhost")
        await sess.load()
        assert sess.dc_id == 2
        assert sess.auth_key == b"key_pg"
        assert sess.is_bot is True
        
        await sess.save()
        await sess.delete()
        assert sess.auth_key is None

@pytest.mark.asyncio
async def test_redis_session():
    mock_client = AsyncMock()
    mock_client.hgetall.return_value = {
        b"dc_id": b"3",
        b"server_address": b"127.0.0.2",
        b"server_port": b"99",
        b"auth_key": b"key_red",
        b"user_id": b"777",
        b"is_bot": b"0"
    }
    
    with patch("redis.asyncio.from_url", return_value=mock_client):
        sess = RedisSession("red_sess", redis_url="redis://localhost")
        await sess.load()
        assert sess.dc_id == 3
        assert sess.user_id == 777
        assert sess.is_bot is False
        
        await sess.save()
        await sess.delete()
        assert sess.auth_key is None

@pytest.mark.asyncio
async def test_mongo_session():
    mock_client = MagicMock()
    mock_db = MagicMock()
    mock_collection = AsyncMock()
    
    mock_client.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection
    
    mock_collection.find_one.return_value = {
        "dc_id": 4,
        "server_address": "127.0.0.3",
        "server_port": 100,
        "auth_key": b"key_mongo",
        "user_id": 888,
        "is_bot": True
    }
    
    with patch("motor.motor_asyncio.AsyncIOMotorClient", return_value=mock_client):
        sess = MongoSession("mongo_sess", connection_string="mongodb://localhost")
        await sess.load()
        assert sess.dc_id == 4
        assert sess.user_id == 888
        assert sess.is_bot is True
        
        await sess.save()
        await sess.delete()
        assert sess.auth_key is None
