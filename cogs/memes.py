import discord
from discord.ext import commands
import random
import praw

class Memes(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.reddit = praw.Reddit(client_id="HBcR9G6Qq_YsUA",
                    client_secret="YMgUARR946zNzuOjITrKQbYPoiToUw",
                    username="Sajan491",
                    password="appleball123",
                    user_agent="Asuma")

    @commands.command()
    async def meme(self, ctx, subred = "memes"):
        subreddit = self.reddit.subreddit(subred)
        all_subs = []
        top = subreddit.top(limit = 100)
        for t in top:
            all_subs.append(t)
        random_sub = random.choice(all_subs)
        name = random_sub.title
        url = random_sub.url
        embed = discord.Embed(title = name)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Memes(client))

