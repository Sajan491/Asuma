import discord
from discord.ext import commands
import datetime 

EMOJIS  = [
    "1️⃣",
    "2️⃣",
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣",
    "🔟"
]

class MoviesRater(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.has_role('Moderators')
    @commands.command()
    async def movie(self, ctx, *, title):
        embed = discord.Embed(
                title=f"{title}",
                colour=1234567,
                timestamp=datetime.datetime.utcnow()
            )
        message = await ctx.send(embed=embed)
        for emoji in EMOJIS:
            await message.add_reaction(emoji)

def setup(client):
    client.add_cog(MoviesRater(client))