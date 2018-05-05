import asyncio
from discord.ext.commands import Bot

BOT_PREFIX = ("!k ")
TOKEN = "NDQxMzExODkxNDc4ODA2NTM4.DcubcA.OAdV3PLqV7Yd4HGAOmJ_8nHV0HA"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)
        
client.loop.create_task(list_servers())
client.run(TOKEN)
