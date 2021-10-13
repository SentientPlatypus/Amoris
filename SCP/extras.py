
  
from discord.ext import commands
import discord
import aiohttp
from bs4 import BeautifulSoup
import base64
import random
from PIL import Image
from io import BytesIO
import datetime
from urllib.parse import quote_plus
from math import sqrt
from prsaw import RandomStuff
class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot




    @commands.command()
    async def cookie(self, ctx, user: discord.Member):
        """Give somebody a cookie :3"""
        await ctx.send(" **{} gave {} a cookie** -"
                         " :cookie:".format(ctx.message.author.name, user.mention))

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def choose(self, ctx, *items):
        """Choose between multiple options"""
        if not items:
            return await ctx.send_help(ctx.command)
        await ctx.send("I chose: **{}**!".format(random.choice(items)))

    def get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    

    @commands.command(aliases=["user"])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def userinfo(self, ctx, user: discord.Member = None):
        """Get a users info."""

        if not user:
            user = ctx.message.author
        try:
            playinggame = user.activity.title
        except:
            playinggame = None

        server = ctx.message.guild
        embed = discord.Embed(color=0xDEADBF)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Discriminator", value=user.discriminator)
        embed.add_field(name="Bot", value=str(user.bot))
        embed.add_field(name="Created", value=user.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Joined", value=user.joined_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Animated Avatar", value=str(user.is_avatar_animated()))
        embed.add_field(name="Playing", value=playinggame)
        embed.add_field(name="Status", value=user.status)
        embed.add_field(name="Color", value=str(user.color))

        try:
            roles = [x.name for x in user.roles if x.name != "@everyone"]

            if roles:
                roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                           if x.name != "@everyone"].index)
                roles = ", ".join(roles)
            else:
                roles = "None"
            embed.add_field(name="Roles", value=roles)
        except:
            pass

        await ctx.send(embed=embed)

    @commands.command(aliases=["server"])
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def serverinfo(self, ctx):
        """Display Server Info"""
        server = ctx.guild
        verif = server.verification_level

        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])

        embed = discord.Embed(color=0xDEADBF)
        embed.add_field(name="Name", value=f"**{server.name}**\n({server.id})")
        embed.add_field(name="Owner", value=server.owner)
        embed.add_field(name="Online (Cached)", value=f"**{online}/{server.member_count}**")
        embed.add_field(name="Created at", value=server.created_at.strftime("%d %b %Y %H:%M"))
        embed.add_field(name="Channels", value=f"Text Channels: **{len(server.text_channels)}**\n"
        f"Voice Channels: **{len(server.voice_channels)}**\n"
        f"Categories: **{len(server.categories)}**\n"
        f"AFK Channel: **{server.afk_channel}**")
        embed.add_field(name="Roles", value=str(len(server.roles)))
        embed.add_field(name="Emojis", value=f"{len(server.emojis)}/100")
        embed.add_field(name="Region", value=str(server.region).title())
        embed.add_field(name="Security", value=f"Verification Level: **{verif}**\n"
        f"Content Filter: **{server.explicit_content_filter}**")

        try:
            embed.set_thumbnail(url=server.icon_url)
        except:
            pass

        await ctx.send(embed=embed)

    @commands.command(aliases=["channel"])
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        """Get Channel Info"""

        if channel is None:
            channel = ctx.message.channel

        embed = discord.Embed(color=0xDEADBF, description=channel.mention)
        embed.add_field(name="Name", value=channel.name)
        embed.add_field(name="Server", value=channel.guild)
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Category ID", value=channel.category_id)
        embed.add_field(name="Position", value=channel.position)
        embed.add_field(name="NSFW", value=str(channel.is_nsfw()))
        embed.add_field(name="Members (cached)", value=str(len(channel.members)))
        embed.add_field(name="Category", value=channel.category)
        embed.add_field(name="Created", value=channel.created_at.strftime("%d %b %Y %H:%M"))

        await ctx.send(embed=embed)



    @commands.command()
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def coffee(self, ctx):
        """Coffee owo"""
        await ctx.channel.trigger_typing()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekobot.xyz/api/image?type=coffee") as res:
                imgdata = await res.json()
            em = discord.Embed()
            msg = await ctx.send("*drinks coffee*", embed=em.set_image(url=imgdata["message"]))
            em = discord.Embed(color=discord.Color.purple())
            await msg.edit(embed=em.set_image(url=imgdata["message"]))

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def animepic(self, ctx):
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://nekobot.xyz/api/v2/image/animepic") as r:
                res = await r.json()
        image = res["message"]
        em = discord.Embed(color=discord.Color.blurple())
        await ctx.send(embed=em.set_image(url=image))



    @commands.command(aliases=["perms"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def permissions(self, ctx, user: discord.Member = None, channel: str = None):
        """Get Permissions,
        Example Usage:
            n!permissions/n!perms @ひびき#0001 testing
        or
            n!permissions/n!perms ひびき#0001 #testing"""

        if user is None:
            user = ctx.message.author

        if channel is None:
            channel = ctx.message.channel
        else:
            channel = discord.utils.get(ctx.message.guild.channels, name=channel)

        msg = "Perms for {} in {}: \n".format(user.name.replace("@", "@\u200B"), channel.name.replace("@", "@\u200B"))

        try:
            perms = user.permissions_in(channel)
            msg += ", ".join([x[0].replace("_", " ").title() for x in perms if x[1]])
            await ctx.send(msg)
        except:
            await ctx.send("Problem getting that channel...")

    @commands.command(aliases=["8"], name="8ball")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def _8ball(self, ctx, *, question: str):
        """Ask 8Ball a question"""
        answers = [":green_circle: It is certain", ":green_circle: As I see it, yes",
                   ":green_circle: It is decidedly so", ":green_circle: Most likely",
                   ":green_circle: Without a doubt", ":green_circle: Outlook good",
                   ":green_circle: Yes definitely", ":green_circle: Yes",
                   ":green_circle: You may rely on it", ":green_circle: Signs point to yes",
                   ":yellow_circle: Reply hazy try again", ":yellow_circle: Ask again later",
                   ":yellow_circle: Better not tell you now",
                   ":yellow_circle: Cannot predict now",
                   ":yellow_circle: Concentrate and ask again",
                   ":red_circle: Don't count on it",
                   ":red_circle: My reply is no", ":red_circle: My sources say no",
                   ":red_circle: Outlook not so good", ":red_circle: Very doubtful"]
        await ctx.send(embed=discord.Embed(title=random.choice(answers), color=0xDEADBF))

    




    @commands.command(name="av", hidden=True)
    @commands.is_owner()
    async def conf_av(self, ctx, *, avatar_url: str):
        """Change bots avatar"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get(avatar_url) as r:
                res = await r.read()
        await self.bot.user.edit(avatar=res)
        try:
            emoji = self.bot.get_emoji(408672929379909632)
            await ctx.message.add_reaction(emoji)
        except:
            pass

    @commands.command(name="username", hidden=True)
    @commands.is_owner()
    async def conf_name(self, ctx, *, name: str):
        """Change bots username"""
        await self.bot.user.edit(username=name)
        try:
            emoji = self.bot.get_emoji(408672929379909632)
            await ctx.message.add_reaction(emoji)
        except:
            pass



def setup(bot):
    bot.add_cog(General(bot))
