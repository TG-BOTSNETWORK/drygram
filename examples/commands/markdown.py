# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext, MarkdownBuilder

client = DryClient("md_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("markdown", description="Send a MarkdownV2 formatted message")
async def markdown_handler(ctx: CommandContext):
    # Construct a MarkdownV2 message safely with auto-escaping
    mb = MarkdownBuilder()
    mb.text("Here is some ").bold("bold").text(" and ").italic("italic").text(" styling in MarkdownV2.")
    
    await ctx.respond(mb.build(), parse_mode="Markdown")

async def main():
    print("DryGram MarkdownBuilder example configured.")

if __name__ == "__main__":
    asyncio.run(main())
