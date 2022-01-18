from discord.ext import commands
import discord
from PIL import Image, ImageFont, ImageDraw, ImageChops
from io import BytesIO
from dotenv import load_dotenv
load_dotenv() 
import os

welcome_channel_id = os.getenv('WELCOME_CHANNEL_ID')
roles_channel_id = os.getenv('ROLES_CHANNEL_ID')
rules_channel_id = os.getenv('RULES_CHANNEL_ID')

def circle(avatar, size=(400, 400)):
    avatar = avatar.resize(size, Image.ANTIALIAS).convert("RGBA")
    mask = Image.new('L', avatar.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0) + avatar.size, fill=255)
    mask = ImageChops.darker(mask, avatar.split()[-1])
    avatar.putalpha(mask)
    return avatar

class Welcomer(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(welcome_channel_id)
        if channel is not None:
            embed = discord.Embed(
                title=f"Welcome to Darkside  :partying_face:",
                colour=1234567, description=f"Review <#{roles_channel_id}> to gain access to the rest of the server.\n"
            ).add_field(
                name=f"Members Count:",
                value=f"{member.guild.member_count}",
            ).add_field(
                name=f"Rules:",
                value=f"<#{rules_channel_id}>"
            )

            # fetches backround
            background = Image.open("assets/background.jpg").convert("RGBA")

            # fetch user image
            userAvatar = member.avatar_url_as(size=256)
            userPic = Image.open(BytesIO(await userAvatar.read())).convert("RGBA")
            
            #crop circular user profile image and add border
            avatar = circle(userPic, (400,400))            

            # paste userPic in background
            background.paste(avatar, (130, 150), avatar)

            #for long user names 
            name = f"{member.name[:20]}.." if len(member.name) > 20 else member.name

            # write text
            write = ImageDraw.Draw(background)
            msg = f"Warm Welcome\n"
            fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 110)
            write.multiline_text((650, 220), msg, font=fnt, fill=(
                0, 0, 0), stroke_width=3, stroke_fill="black")
            write.text((650, 340), name, font=fnt, fill=(
                0, 0, 0), stroke_width=3, stroke_fill="purple")
            background.convert("RGB").save("assets/welcomeImage.jpg")
            file = discord.File("assets/welcomeImage.jpg", filename="welcomeImg.jpg")

            #embeds 
            embed.set_image(url="attachment://welcomeImg.jpg")
            embed.set_author(
                name="Asuma", icon_url="https://i.imgur.com/DhULA4z.jpg")
            await channel.send(embed=embed, file=file)

def setup(client):
    client.add_cog(Welcomer(client))