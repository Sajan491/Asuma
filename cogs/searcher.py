import discord
from discord.ext import commands
import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class Searcher(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def random(self, ctx, word, num:int = 1):
        all_images = []
        req = Request(f"https://results.dogpile.com/serp?qc=images&q={word}", headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = BeautifulSoup(webpage, 'html.parser')
        images = soup.find_all('img')
        for item in images:
            all_images.append(item['src'])
        if num<4:
          for i in range(num):
            image_url = random.choice(all_images)
            embed = discord.Embed(colour = discord.Colour.orange())
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
            i=i+1
        else:
          await ctx.send("U nub. Max = 3")


def setup(client):
    client.add_cog(Searcher(client))



