# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("flags_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("delete_cache", description="Cleans database cache (supports --all and --force flags)")
async def delete_handler(ctx: CommandContext):
    force = ctx.flags.get("force", False)
    all_cache = ctx.flags.get("all", False)
    
    status = []
    if all_cache: status.append("all data")
    if force: status.append("forced clean")
    
    await ctx.respond(f"Clean action processed: {', '.join(status) if status else 'default'}")

async def main():
    print("DryGram command flags example configured.")

if __name__ == "__main__":
    asyncio.run(main())
