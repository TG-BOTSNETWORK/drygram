# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext, CodeBuilder

client = DryClient("code_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("code_sample", description="Send a syntax-highlighted python code block")
async def code_handler(ctx: CommandContext):
    cb = CodeBuilder(language="python")
    cb.add_line("def greet():")
    cb.add_line("    print('Hello World')")
    
    await ctx.respond(cb.to_markdown(), parse_mode="Markdown")

async def main():
    print("DryGram CodeBuilder example configured.")

if __name__ == "__main__":
    asyncio.run(main())
