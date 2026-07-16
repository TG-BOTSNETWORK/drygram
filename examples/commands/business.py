# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("business_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("autoresponder", business_only=True, description="Manage business autoresponder settings")
async def business_handler(ctx: CommandContext, status: bool):
    state = "enabled" if status else "disabled"
    await ctx.respond(f"Business autoresponder has been {state}.")

async def main():
    print("DryGram business command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
