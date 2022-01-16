import discord
import requests
import json
from itertools import cycle
from PIL import Image, ImageDraw
from io import BytesIO
from utils.languages import LANGUAGES
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

import os
from google_trans_new import google_translator
translator = google_translator()
from keep_alive import keep_alive

from discord.ext import commands, tasks
from discord import Intents
from cogs.roleshandler import RolesHandler

intents = Intents.default()
intents.members = True 
client = commands.Bot(command_prefix = '#', intents=intents)

statuses = cycle(["Kaun Banega Crorepati", "with life", "chess"])
client.remove_command("help")
#events
@client.event
async def on_ready():
    change_status.start()
    print("Bot is online")

#tasks
@tasks.loop(seconds = 60)
async def change_status():
    await client.change_presence(status=discord.Status.online, activity = discord.Game(next(statuses)))

#commands
@client.command(help="Returns latency")
async def ping(ctx):
    await ctx.send(f'**PONG!** {round(client.latency * 1000)}ms')

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return quote

@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title = "Help", colour = discord.Colour.orange())
    embed.add_field(name = "#ping", value = "Returns latency", inline = False)
    
    embed.add_field(name = "#inspire", value = "Returns an inspiring quote", inline = False)
    embed.add_field(name = "#clear [number]", value = "Clears latest messages (for moderators only)", inline = False)
    embed.add_field(name = "#warn @[username] (reason)", value = "Gives warning to users", inline = False)
    embed.add_field(name = "#wanted @[username] (reason)", value = "Displays a wanted poster", inline = False)
    embed.add_field(name = "#rip @[username]", value = "Displays a RIP picture", inline = False)
    embed.add_field(name = "#whois @[username]", value = "Gives info about a user", inline = False)
    embed.add_field(name = "#meme [optional:subreddit]", value = "Displays a meme", inline = False)
    embed.add_field(name = "#tictactoe @[username] @[username]", value = "Starts a tictactoe game", inline = False)
    embed.add_field(name = "#place [int]", value = "Places a cross or a circle in the tictactoe game", inline = False)
    embed.add_field(name = "#translate [from] [to] [text]", value = "Translates text from one language to another", inline = False)
    embed.add_field(name = "#help translate", value = "Shows help for translation", inline = False)
    embed.add_field(name = "#random <search_text> <amount>", value = "Returns random number of queried image", inline = False)
    embed.add_field(name = "#guesser", value = "Starts the guesser game", inline = False)
    embed.add_field(name = "#guess <word>", value = "For guessing word in the game", inline = False)
    embed.add_field(name = "#scoreboard", value = "Shows scoreboard for the guesser game", inline = False)
    await ctx.send(embed=embed)


@client.command()
async def translate(ctx, fromlang, tolang, *, message):
    translated = translator.translate(message,lang_src=fromlang,lang_tgt=tolang, pronounce=True)
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.add_field(name = "Input text", value = message, inline = False)
    embed.add_field(name = "Translated text", value = translated[0] + " ( "+ translated[2]+ " )", inline = False)
    await ctx.send(embed=embed)

@help.command()
async def translate(ctx):
    await ctx.send("Languages Supported for Translation")
    await ctx.send(LANGUAGES)

@client.command(aliases =['motivate'])
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)

@commands.has_role('Moderators')
@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount+1)

@commands.has_role('Moderators')
@client.command()
async def warn(ctx,userr, *, msg=" "):
    await clear(ctx,0)
    user = userr
    reason = msg
    await ctx.send(f"{user} You've been WARNED {reason}.")

@client.command()
async def summon(ctx,userr):
    await clear(ctx,0)
    user = userr
    await ctx.send(f"{user}, You've been SUMMONED.")

@commands.has_role('Moderators')
@client.command()
async def say(ctx, *, msg):
    await clear(ctx,0)
    await ctx.send(msg)

@client.command()
async def wanted(ctx, user: discord.Member = None, *, msg):
    await clear(ctx,0)
    if user==None:
        await ctx.send("No user included")
    wanted = Image.open("assets/wantedBackG.jpg")
    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    ppic = Image.open(data)
    ppic = ppic.resize((165,165))
    wanted.paste(ppic,(110,195))
    write = ImageDraw.Draw(wanted)
    write.text((70,380), msg, (0,0,0))
    wanted.save("temp.jpg")
    await ctx.send(file = discord.File("temp.jpg"))

@client.command()
async def rip(ctx, user: discord.Member = None):
    await clear(ctx,0)
    if user==None:
        await ctx.send("No user included")
    wanted = Image.open("assets/ripBackG.png")
    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    ppic = Image.open(data)
    ppic = ppic.resize((200,200))
    wanted.paste(ppic,(304,346))
    wanted.save("temp.jpg")
    await ctx.send(file = discord.File("temp.jpg"))

@client.command()
async def whois(ctx, member:discord.Member):
    embed = discord.Embed(title = member.name, description = member.mention, color = discord.Colour.green())
    embed.add_field(name = "ID", value=member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    await ctx.send(embed = embed)

#error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not Found!")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please also include the amount of messages to delete!")

#cogs
@commands.has_role('Moderators')
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded Successfully")

@commands.has_role('Moderators')
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded Successfully")

@commands.has_role('Moderators')
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Successfully")


# for filename in os.listdir("./cogs"):
#     if filename.endswith('.py'):
#         client.load_extension(f'cogs.{filename[:-3]}')

client.add_cog(RolesHandler(client))

# keep_alive()
client.run(os.getenv('TOKEN'))


