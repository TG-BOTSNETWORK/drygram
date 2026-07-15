# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, PostgresSession, RedisSession, MongoSession

async def main():
    pg_session = PostgresSession("session1", dsn="postgresql://user:pass@localhost/db")
    redis_session = RedisSession("session2", redis_url="redis://localhost:6379/0")
    mongo_session = MongoSession("session3", connection_string="mongodb://localhost:27017")
    
    c1 = DryClient(pg_session, api_id=123, api_hash="abc")
    c2 = DryClient(redis_session, api_id=123, api_hash="abc")
    c3 = DryClient(mongo_session, api_id=123, api_hash="abc")
    
    print("Multi-engine session pool loaded successfully")

if __name__ == "__main__":
    asyncio.run(main())
