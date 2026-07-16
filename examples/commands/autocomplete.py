# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext, Autocompleter

client = DryClient("autocomplete_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

# Define static suggestions
completer = Autocompleter(choices=["apple", "banana", "cherry", "date"])

@command("fruit", description="Autocomplete command returning suggestions")
async def fruit_handler(ctx: CommandContext, name: str):
    suggestions = completer.get_suggestions(name)
    await ctx.respond(f"Matches for '{name}': {', '.join(suggestions)}")

async def main():
    print("DryGram autocomplete command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
