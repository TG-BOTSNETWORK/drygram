# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("cooldowns_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("spam", cooldown_rate=1, cooldown_per=5.0, description="Rate-limited command (1 call per 5s)")
async def spam_handler(ctx: CommandContext):
    await ctx.respond("This command executed successfully and is now on a 5-second cooldown.")

async def main():
    print("DryGram cooldowns command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
