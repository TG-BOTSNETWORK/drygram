# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient

async def main():
    client = DryClient("stories_session", api_id=12345, api_hash="abcdef")
    await client.start()
    story_id = await client.publish_story("Daily update!")
    print(f"Story published with ID: {story_id}")
    await client.stop()

if __name__ == "__main__":
    asyncio.run(main())
