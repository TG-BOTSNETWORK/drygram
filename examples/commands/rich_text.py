# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext, RichText

client = DryClient("rt_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("rich", description="Send a formatted message with bold, italic, and spoilers")
async def rich_handler(ctx: CommandContext):
    # Construct a chainable formatted text payload
    rt = RichText()
    rt.text("Standard text, ").bold("bold text, ").italic("italic text, ").spoiler("spoiler text.")
    
    # We can send this output compile as Markdown or HTML
    await ctx.respond(rt.to_html(), parse_mode="HTML")

async def main():
    print("DryGram RichText builder example configured.")

if __name__ == "__main__":
    asyncio.run(main())
