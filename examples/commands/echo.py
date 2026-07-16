# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("echo_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("echo", description="Echo back the exact text message passed as arguments")
async def echo_handler(ctx: CommandContext, text: str):
    await ctx.respond(f"You said: {text}")

async def main():
    print("DryGram echo command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
