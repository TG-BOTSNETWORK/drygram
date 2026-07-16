# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("admin_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("kick", admin_only=True, description="Kicks a user from the chat (Admin only)")
async def kick_handler(ctx: CommandContext, user_id: int):
    # Perform kick logic using DryGram core API
    await ctx.respond(f"User {user_id} has been kicked from the chat.")

async def main():
    print("DryGram admin command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
