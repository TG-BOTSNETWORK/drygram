# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("args_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("greet", description="Greet a user with custom styling")
async def greet_handler(ctx: CommandContext, name: str, age: int = 18):
    await ctx.respond(f"Hello {name}! You are registered as {age} years old.")

async def main():
    print("DryGram command arguments example configured.")

if __name__ == "__main__":
    asyncio.run(main())
