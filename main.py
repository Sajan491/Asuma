import discord
import logging
import requests
import json
logging.basicConfig(level=logging.INFO)
from itertools import cycle
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

from discord.ext import commands, tasks
client = commands.Bot(command_prefix = '!')

statuses = cycle(["with your wife", "with your life", "chess"])

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

@client.command(aliases =['motivate'], help="Shows an inspiring quote")
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)

@client.command(help="Clears latest messages")
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount+1)

@client.command(help="Gives warning to users")
async def warn(ctx, *, msg):
    await clear(ctx,0)
    user = msg.split(" ")[0]
    reason = msg.split(" ",1)[1]
    await ctx.send(f"{user} You've been WARNED {reason}.")

@client.command(help="Says whatever you want it to say")
async def say(ctx, *, msg):
    await clear(ctx,0)
    await ctx.send(msg)

@client.command(help="Displays a wanted poster")
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

@client.command(help="Displays a RIP picture")
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

#error handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not Found!")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please also include the amount of messages to delete!")

# @warn.error
# async def warn_error(ctx, error):
#     await ctx.send("Please also include the warning!")


client.run("ODE0MTQzNTY2MjE3NDc4MTY1.YDZkSA.Bl62V9h_bS9PVZ8hljwPrd1UXsc")


