# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("perms_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("restricted_admin", owner_only=True, description="Restrict command execution strictly to owner")
async def restricted_handler(ctx: CommandContext):
    await ctx.respond("Access granted to the bot owner.")

async def main():
    print("DryGram permissions command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
