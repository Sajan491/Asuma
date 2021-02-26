import discord
import logging
import requests
import json
logging.basicConfig(level=logging.INFO)
from itertools import cycle
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import os

from discord.ext import commands, tasks
client = commands.Bot(command_prefix = '!')

statuses = cycle(["with your wife", "with your life", "chess"])
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

@client.command()
async def help(ctx):
    embed = discord.Embed(title = "Help", colour = discord.Colour.orange())
    embed.add_field(name = "!ping", value = "Returns latency", inline = False)
    embed.add_field(name = "!say [message]", value = "Says what you ask it to say", inline = False)
    embed.add_field(name = "!inspire", value = "Prints an inspiring quote", inline = False)
    embed.add_field(name = "!clear [number]", value = "Clears latest messages", inline = False)
    embed.add_field(name = "!warn @[username] (reason)", value = "Gives warning to users", inline = False)
    embed.add_field(name = "!wanted @[username] (reason)", value = "Displays a wanted poster", inline = False)
    embed.add_field(name = "!rip @[username]", value = "Displays a RIP picture", inline = False)
    embed.add_field(name = "!whois @[username]", value = "Gives info about a user", inline = False)
    embed.add_field(name = "!warn @[username] (reason)", value = "Gives warning to users", inline = False)
    embed.add_field(name = "!meme [optional:subreddit]", value = "Displays a meme", inline = False)
    embed.add_field(name = "!tictactoe @[username] @[username]", value = "Gives warning to users", inline = False)
    embed.add_field(name = "!place [int]", value = "Places a cros or a circle in the tictactoe game", inline = False)
    await ctx.send(embed=embed)

@client.command(aliases =['motivate'])
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)

@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount+1)

@client.command()
async def warn(ctx, *, msg):
    await clear(ctx,0)
    user = msg.split(" ")[0]
    reason = msg.split(" ",1)[1]
    await ctx.send(f"{user} You've been WARNED {reason}.")

@client.command()
async def say(ctx, *, msg):
    await clear(ctx,0)
    await ctx.send(msg)

@client.command()
async def wanted(ctx, user: discord.Member = None, *, msg):
    await clear(ctx,0)
    if user==None:
        await ctx.send("No user included")
    wanted = Image.open("backg.jpg")
    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    ppic = Image.open(data)
    ppic = ppic.resize((165,165))
    wanted.paste(ppic,(110,195))
    write = ImageDraw.Draw(wanted)
    write.text((70,380), msg, (0,0,0))
    wanted.save("profile.jpg")
    await ctx.send(file = discord.File("profile.jpg"))

@client.command()
async def rip(ctx, user: discord.Member = None):
    await clear(ctx,0)
    if user==None:
        await ctx.send("No user included")
    wanted = Image.open("rip.png")
    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    ppic = Image.open(data)
    ppic = ppic.resize((200,200))
    wanted.paste(ppic,(304,346))
    wanted.save("profile.jpg")
    await ctx.send(file = discord.File("profile.jpg"))

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
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded Successfully")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded Successfully")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Reloaded Successfully")


for filename in os.listdir("./cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run("ODE0MTQzNTY2MjE3NDc4MTY1.YDZkSA.Bl62V9h_bS9PVZ8hljwPrd1UXsc")


