import random
import asyncio
import discord
import re
from discord.ext.commands import Bot
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests

BOT_PREFIX = ("k!")
TOKEN = "NDQxMzExODkxNDc4ODA2NTM4.DcubcA.OAdV3PLqV7Yd4HGAOmJ_8nHV0HA"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='img',
                description='Send the img of a member from discord server',
                aliases=['member', 'Member', 'info', 'Img', 'img member', 'Img member'],
                pass_context=True)
async def img_member(ctx, *, user):
    embed = discord.Embed(colour=discord.Colour.purple())
    
    replaceables = "<@!>"
    for char in user:
        if char in replaceables:
            user = user.replace(char, '') 
    
    member = ctx.message.server.get_member(user)
    
    try:
        member_avatar_url = member.avatar_url
        
        embed.set_image(url=member_avatar_url)
            
        await client.say(embed=embed)
    except:
        await client.say(embed=discord.Embed(title="Invalid input", colour=discord.Colour.purple()))
        
@client.command(name='xingar',
                description="Xinga um filho da puta.",
                aliases=['fdp'],
                pass_context=True)
async def xingar(ctx, *, user):
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

@client.command(name='maple',
                description="Find a maple character in the rankings",
                aliases=['name', 'maplestory', 'Maple', 'MapleStory', 'Maplestory'],
                pass_context=True)
async def maple(ctx, name):
    result = requests.get("http://maplestory.nexon.net/rankings/overall-ranking/legendary?pageIndex=1&character_name="+ name +"&search=true#ranking")

    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    samples = soup.find_all('tr')
    
    embed = discord.Embed(colour=discord.Colour.purple())
    
    found = False
    for a in samples[1:]:
        tds = a.find_all('td')
        
        character_name = tds[2].string.strip()

        if character_name.lower() == name.strip().lower():
            character_rank = tds[0].string.strip()
            character_avatar = tds[1].img['src'].strip()
            character_world = tds[3].a['title'].strip()
            character_job = tds[4].img['title'].strip()
            character_level = tds[5].br.previous_sibling.strip()
            character_legion_level = get_legion_level(character_name, character_world)
            
            embed.add_field(name="Name", value=character_name, inline=False)
            embed.add_field(name="Level", value=character_level, inline=False)
            embed.add_field(name="Job", value=character_job, inline=False)
            embed.add_field(name="World", value=character_world, inline=False)
            embed.add_field(name="Rank", value=character_rank, inline=False)
            embed.add_field(name="Legion Level", value=character_legion_level, inline=False)
            embed.set_thumbnail(url=character_avatar)
            
            found = True
            
    if found:
        await client.say(embed=embed)
    else:
        await client.say(embed=discord.Embed(title="Character not found!", colour=discord.Colour.purple()))

def get_legion_level(character_name, character_world):
    result = requests.get("http://maplestory.nexon.net/rankings/legion/"+ character_world +"?pageIndex=1&character_name="+ character_name +"&search=true#ranking")
    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    samples = soup.find_all('tr')
    
    for a in samples[1:]:
        tds = a.find_all('td')
        
        character_name_td = tds[2].string.strip()
        if character_name_td == character_name:
            return tds[3].string.strip()
    
    return "Legion level unavailable"

@client.command(name='christina',
                aliases=['Christina'],
                pass_context=True)
async def christina(ctx):
    await client.say("Remove the 'Tina' :rage:")

@client.command(name='anime',
                aliases=['Anime'],
                pass_context=True)
async def anime(ctx, *, anime_to_find):
    anime_url = find_anime_page(anime_to_find)
    
    if anime_url:
        result = requests.get(url=anime_url)
        c = result.content
        
        soup = BeautifulSoup(c, "html.parser", from_encoding="utf8")
        
        name = soup.find('span', {'itemprop': 'name'}).string.strip()
        img = soup.find('img', {'alt': name, 'class': 'ac', 'itemprop': 'image'})['src'].strip()
        score = soup.find('div', {'class': 'fl-l score'}).string.strip()
        score_voters = soup.find('div', {'class': 'fl-l score'})['data-user'].strip().replace(" users", "")
        rank = soup.find('span', {'class': 'numbers ranked'}).strong.string.strip().replace("#", "")
        popularity = soup.find('span', {'class': 'numbers popularity'}).strong.string.strip().replace("#", "")
        members = soup.find('span', {'class': 'numbers members'}).strong.string.strip()
        
        embed = discord.Embed(colour=discord.Colour.purple())
            
        embed.add_field(name="Name", value=name)
        embed.add_field(name="Score", value=score)
        embed.add_field(name="Voters", value=score_voters)
        embed.add_field(name="Rank", value=rank)
        embed.add_field(name="Popularity", value=popularity)
        embed.add_field(name="Members", value=members)
        embed.set_image(url=img)
        
        await client.say(embed=embed)
    else:
        await client.say(embed=discord.Embed(title="No anime found", colour=discord.Colour.purple()))
    
def find_anime_page(anime_to_find):
    try:
        result = requests.get("https://myanimelist.net/anime.php?q="+ str(anime_to_find), headers={'Connection': 'close'})
        c = result.content
        
        only_div_class = SoupStrainer("div", {'class': 'js-categories-seasonal js-block-list list'})
        soup = BeautifulSoup(c, "html.parser", from_encoding="utf8", parse_only=only_div_class)
        
        samples = soup.find_all('tr')
        s = samples[1].find('a', {'class': 'hoverinfo_trigger fw-b fl-l'})
        srch_anime_url = s['href']
        
        return srch_anime_url
    except:
        return None
    
async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)
        
client.loop.create_task(list_servers())
client.run(TOKEN)
