# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
from drygram import DryClient
from drygram.commands import CommandRouter, CommandGroup, CommandContext

client = DryClient("sub_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

# Define command group
config_group = CommandGroup("config", description="Manage global configurations")

@config_group.command("set", description="Set a configuration value")
async def config_set(ctx: CommandContext, key: str, value: str):
    await ctx.respond(f"Config '{key}' set to '{value}'.")

@config_group.command("get", description="Get a configuration value")
async def config_get(ctx: CommandContext, key: str):
    await ctx.respond(f"Config '{key}' is active.")

# Register group in registry
router.registry.register_group(config_group)

async def main():
    print("DryGram subcommands group example configured.")

if __name__ == "__main__":
    asyncio.run(main())
