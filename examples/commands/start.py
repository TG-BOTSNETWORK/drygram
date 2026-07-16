# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("start_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("start", description="Start the bot and get a welcome message")
async def start_handler(ctx: CommandContext):
    await ctx.respond("Welcome to the DryGram Command Framework! Use /help to see all commands.")

async def main():
    # Setup mock loops for example demonstration
    print("DryGram start command example configured.")
    # In a real app:
    # await client.start()
    # await client.idle()

if __name__ == "__main__":
    asyncio.run(main())
