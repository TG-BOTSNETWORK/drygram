# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("topics_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("topic_info", topic_only=True, description="Retrieve details about the current forum topic thread")
async def topic_handler(ctx: CommandContext):
    topic_id = getattr(ctx.message, "topic_id", None)
    await ctx.respond(f"Executing topic command in thread ID: {topic_id}")

async def main():
    print("DryGram topic command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
