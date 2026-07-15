# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com
import asyncio
from drygram import DryClient, Gates, Message

app = DryClient("stories_session", api_id=12345, api_hash="abcdef")

@app.observe(Gates.text("post_story"))
async def post_story_example(msg: Message):
    story_id = await app.publish_story(caption="Story from DryGram!")
    await app.react_to_story(story_id, "🔥")
    await app.echo(msg, f"Published story ID: {story_id}")

async def main():
    await app.start()
    await asyncio.sleep(2)
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
