# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext, HTMLBuilder

client = DryClient("html_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("html", description="Send an HTML formatted message")
async def html_handler(ctx: CommandContext):
    hb = HTMLBuilder()
    hb.text("This is an ").underline("underlined").text(" and ").strikethrough("strikethrough").text(" message.")
    
    await ctx.respond(hb.build(), parse_mode="HTML")

async def main():
    print("DryGram HTMLBuilder example configured.")

if __name__ == "__main__":
    asyncio.run(main())
