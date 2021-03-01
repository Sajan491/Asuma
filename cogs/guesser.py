import discord
from discord.ext import commands
import random
import aiohttp
from randthings import diction


class Guesser(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.final_word = ""
        self.guessed = False

    @commands.command()
    async def guesser(self, ctx):
        if self.final_word == "":
            self.guessed = False
            self.final_word = ""
            async with ctx.channel.typing():
                data = diction
                the_word = random.choice(data["RandL"]["items"])
                self.final_word = the_word
                print(the_word)
                embed = discord.Embed(title="Guess the word using #guess <name>")
                embed.set_image(url=f"https://www.randomlists.com/img/things/{the_word}.jpg")
                await ctx.send(embed=embed)
        else:
            await ctx.send("Please complete the previous game first")

    @commands.command()
    async def guess(self, ctx, *, guessed_word):
        if self.final_word != "":
            if self.guessed == False:
                if guessed_word == self.final_word:
                    self.guessed = True
                    self.final_word = ""
                    await ctx.send(f"{ctx.author} has guessed the word and won a point!")
                else:
                    await ctx.send("Wrong! Try Again")
            else:
                await ctx.send("Word already guessed!")
        else:
            await ctx.send("Please start a new game using #guesser first.")

def setup(client):
    client.add_cog(Guesser(client))

