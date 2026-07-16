# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("groups_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("pin_message", group_only=True, description="Pin a message in the group chat")
async def pin_message_handler(ctx: CommandContext):
    await ctx.respond("Message has been pinned in this group.")

async def main():
    print("DryGram group command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
