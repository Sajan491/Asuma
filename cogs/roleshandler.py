from discord.ext import commands

import discord, json, os

ROLES_CHANNEL = 923893701225349120
ROLES = [
    {"name": "Programmer", "aname": "Programming and Technology", "emoji":"<:programming:923903358245408810>", "emojiname":"programming"},
    {"name": "Weeb", "aname": "Anime", "emoji":"<:shine:852074265419186186>", "emojiname":"shine"},
    {"name": "Gamer", "aname": "Games and Sports", "emoji":"🎮", "emojiname":"video_game"},
    {"name": "Geet-sunne", "aname": "Music", "emoji":"🎵", "emojiname":"musical_note"},
    {"name": "Movie-herne", "aname": "Movie", "emoji":"🎥", "emojiname":"movie_camera"},
    {"name": "Nerd", "aname": "Study", "emoji":"📗", "emojiname":"green_book"},
    {"name": "NSFW", "aname": "NSFW", "emoji":"🔞", "emojiname":"underage"},
]

json_path =  os.path.join(os.getcwd(), "cogs", "message.json")
with open(json_path, mode="r") as jfile:
    res = json.load(jfile)
    MESSAGE_IDS = res["message_ids"]

class RolesHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = None
    
    async def react_role(self, action, payload):
        if payload.user_id == self.bot.user.id:
            return

        for message in MESSAGE_IDS:
            if payload.message_id == message:
                guild_id = payload.guild_id
                guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

                for r in ROLES:
                    names = r.get("emoji"), r.get("emojiname"), r.get("name")
                    if payload.emoji.name in names:
                        role_name = r["name"]
                        break
                else:
                    role_name = None
                
                role = discord.utils.get(guild.roles, name=role_name)
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if not role:
                    print(f"{role_name} Role not found for {payload.emoji}")
                    message = await self.channel.fetch_message(message)
                    await message.remove_reaction(payload.emoji, member)
                    return
                
                if member is not None:
                    await getattr(member, action)(role)
                else:
                    print("Member not found")

    
    @commands.command(name="sutc")
    async def set_up_text_channel(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            self.channel = self.bot.get_channel(ROLES_CHANNEL) 
        else:
            self.channel = channel
        await ctx.send(f"Set up roles channel: {self.channel.mention} :white_check_mark:")

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.react_role("add_roles", payload)

    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.react_role("remove_roles", payload)
        
    
    @commands.has_role("Moderators")
    @commands.command(name="surr")
    async def set_up_reaction_roles(self, ctx):
        if not self.channel:
            await self.set_up_text_channel(ctx)
        
        global MESSAGE_IDS

        ## Status roles
        s_msg = "**Get roles by reacting to the message and gain access to different portions of the server**\n\n"
        for role in ROLES:
            s_msg += f"{role['aname']} - {role['emoji']}\n"
        message = await self.channel.send(s_msg)
        MESSAGE_IDS.append(message.id)

        for role in ROLES:
            await message.add_reaction(role["emoji"])
        
        with open(json_path, "w") as jfile:
            res["message_ids"] = MESSAGE_IDS
            json.dump(res, jfile, indent = 4)
        
def setup(bot):
    bot.add_cog(RolesHandler(bot))
