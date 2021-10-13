from discord.ext import commands
import discord, aiohttp
import base64
import json
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import time
import random

wargaming = {
    "wows": {
        "servers": {
            "ru": "https://api.worldofwarships.ru/wows/",
            "eu": "https://api.worldofwarships.eu/wows/",
            "na": "https://api.worldofwarships.com/wows/",
            "asia": "https://api.worldofwarships.asia/wows/"
        },
        "nations": {
            "commonwealth": "🇦🇺 ",
            "italy": "🇮🇹 ",
            "usa": "🇺🇸 ",
            "pan_asia": "🇨🇳 ",
            "france": "🇫🇷 ",
            "ussr": "☭ ",
            "germany": "🇩🇪 ",
            "uk": "🇬🇧 ",
            "japan": "🇯🇵 ",
            "poland": "🇵🇱 ",
            "pan_america": ""
        }
    }
}

osu_icons = ["osu", "taiko", "ctb", "mania"]
__gradients = [
    ["fad0c4", "ff9a9e"],
    ["333333", "dd1818"],
    ["11998e", "38ef7d"],
    ["108dc7", "ef8e38"],
    ["FC5C7D", "6A82FB"],
    ["FC466B", "3F5EFB"],
    ["c94b4b", "4b134f"],
    ["23074d", "cc5333"],
    ["fffbd5", "b20a2c"],
    ["00b09b", "96c93d"],
    ["D3CCE3", "E9E4F0"],
    ["800080", "ffc0cb"],
    ["00F260", "0575E6"],
    ["fc4a1a", "f7b733"],
    ["74ebd5", "ACB6E5"],
    ["22c1c3", "fdbb2d"],
    ["ff9966", "ff5e62"],
    ["7F00FF", "E100FF"],
    ["d9a7c7", "fffcdc"],
    ["EF3B36", "FFFFFF"],
    ["56CCF2", "2F80ED"],
    ["F2994A", "F2C94C"],
    ["30E8BF", "FF8235"],
    ["4568DC", "B06AB3"],
    ["43C6AC", "F8FFAE"]
]


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def mcskin(self, ctx, username:str):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as r:
                    res = await r.json()
            user_id = res['id']
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{user_id}") as r:
                    res = await r.json()
            data = base64.b64decode(res['properties'][0]['value'])
            data = json.loads(data)
            skin = data['textures']['SKIN']['url']
            embed = discord.Embed(color=0xDEADBF, title=f"User: {res['name']}")
            embed.set_image(url=skin)
            await ctx.send(embed=embed)
        except:
            await ctx.send("**Failed to get user**")


def setup(bot):
    bot.add_cog(Games(bot))