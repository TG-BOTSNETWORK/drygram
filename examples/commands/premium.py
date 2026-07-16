# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("premium_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("premium_feature", premium_only=True, description="Access premium member features (Premium only)")
async def premium_handler(ctx: CommandContext):
    await ctx.respond("Welcome, Premium user! You have successfully accessed a premium command.")

async def main():
    print("DryGram premium command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
