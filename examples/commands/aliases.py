# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("alias_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("status", aliases=["st", "info"], description="Show connection and status details")
async def status_handler(ctx: CommandContext):
    await ctx.respond("DryGram status is online.")

async def main():
    print("DryGram command aliases example configured.")

if __name__ == "__main__":
    asyncio.run(main())
