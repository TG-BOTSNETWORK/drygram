# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("help_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("help", description="Show this global help message or help for a specific command")
async def help_handler(ctx: CommandContext):
    # CommandRouter natively intercepts and handles `/help` and `/help <command>`
    # But this callback can override or handle custom help actions
    await ctx.respond("Use /help <command_name> for specific command usage.")

async def main():
    print("DryGram auto help example configured.")

if __name__ == "__main__":
    asyncio.run(main())
