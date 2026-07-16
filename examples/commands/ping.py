# DryGram Developed By Santhu
# mail: telegramsanthu@gmail.com

import asyncio
import time
from drygram import DryClient
from drygram.commands import CommandRouter, command, CommandContext

client = DryClient("ping_sess", api_id=123, api_hash="abc")
router = CommandRouter(client)

@command("ping", description="Ping check response latency")
async def ping_handler(ctx: CommandContext):
    start_time = time.time()
    msg = await ctx.respond("Pinging...")
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    await ctx.client.edit(msg, f"Pong! Latency: {latency:.2f}ms")

async def main():
    print("DryGram ping command example configured.")

if __name__ == "__main__":
    asyncio.run(main())
