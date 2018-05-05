import random
import asyncio
import re
from discord.ext.commands import Bot

BOT_PREFIX = ("!k ")
TOKEN = "NDQxMzExODkxNDc4ODA2NTM4.DcubcA.OAdV3PLqV7Yd4HGAOmJ_8nHV0HA"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='xingar',
                description="Xinga um filho da puta.",
                aliases=['fdp'],
                pass_context=True)
async def xingar(ctx, user):
    possible_responses = [
        'Desgraçado',
        'Filho da puta',
        'Cabeça de desgraça',
        'Lixo',
        'Vagabundo',
    ]

    member = ctx.message.server.get_member_named(user)

    if member:
        await client.say(member.mention + " é um "+ random.choice(possible_responses))
    elif re.match("<@[0-9]*>", user):
        await client.say(user + " é um "+ random.choice(possible_responses))
    else:
        await client.say("Entrada inválida, tente novamente")

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)
        
client.loop.create_task(list_servers())
client.run(TOKEN)
