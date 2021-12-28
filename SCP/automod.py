import discord
from discord.ext import commands
import datetime
import datetime
import json
from re import search
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import cog
from discord.ext.commands.errors import BadArgument
import Globals

cluster = Globals.getMongo()
DiscordGuild = cluster["discord"]["guilds"]
class illegalAction(commands.CommandError):
    def __init__(self, user, action, *args, **kwargs):
        self.user = user
        self.action=action



class AutoMod(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.description = "Commands to setup Auto-Mod"
        self.theme_color = discord.Color.purple()
        self.url_regex = (
            r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.]"
            r"[a-z]{2,4}/)("
            r"?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<"
            r">]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^"
            r"\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        )

    @commands.command(name="automod", help="Allows you to enable/disable automod features")
    @commands.has_permissions(administrator=True)
    @commands.has_guild_permissions(administrator=True)
    async def automod(self, ctx):

        available_features = ["links", "images", "spam"]
        reactionlist = ["🔗", "🖼️", "📣", "🚪"]
        dictionary = {"🔗":"links", "🖼️":"images", "📣": "spam", "🚪":"leave"}
        activated_features = DiscordGuild.find_one({"id":ctx.guild.id}, {"automod"})["automod"]
        def check(key):
            if key.lower() in activated_features:
                return "✅ enabled"
            else:
                return "❌ disabled"
        def save():
            DiscordGuild.update_one({"id":ctx.guild.id}, {"$set":{"automod":activated_features}})
        mod_embed = discord.Embed(
            title="Auto-Mod",
            description=(
                "Allow me to mod on my own. "
                "Reply with a particular feature."
            ),
            color=self.theme_color,
        )
        mod_embed.add_field(
            name="`links`%s"%(check("links")),
            value="Bans links from being sent to this server",
            inline=False,
        )
        mod_embed.add_field(
            name="`images`%s"%(check("images")),
            value="Bans attachments from being sent to this server",
            inline=False,
        )
        mod_embed.add_field(
            name="`spam`%s"%(check("spam")),
            value="Temporarily mutes users who are spamming mentions in this server",
            inline=False,
        )
        mod_embed.set_footer(
            text=(
                "React with with 🚪 if you want to stop "
                "adding auto-mod features and save your changes"
            )
        )




        msg = await ctx.send(embed=mod_embed)
        for x in reactionlist:
            await msg.add_reaction(x)
        def bettercheck(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactionlist and reaction.message == msg
        while True:
            mod_embed = discord.Embed(
                title="Auto-Mod",
                description=(
                    "Allow me to mod on my own. "
                    "Reply with a particular feature."
                ),
                color=self.theme_color,
            )
            mod_embed.add_field(
                name="`links`%s"%(check("links")),
                value="Bans links from being sent to this server",
                inline=False,
            )
            mod_embed.add_field(
                name="`images`%s"%(check("images")),
                value="Bans attachments from being sent to this server",
                inline=False,
            )
            mod_embed.add_field(
                name="`spam`%s"%(check("spam")),
                value="Temporarily mutes users who are spamming mentions in this server",
                inline=False,
            )
            mod_embed.set_footer(
                text=(
                    "Reply with stop if you want to stop "
                    "adding auto-mod features and save your changes"
                )
            )
            await msg.edit(embed=mod_embed)

            try:
                confirm = await self.client.wait_for("reaction_add", check=bettercheck, timeout=30.0)
            except asyncio.TimeoutError:
                # Just an example error message I copied from Diablo
                embed = discord.Embed(
                        description="you took too long lmao",
                        color=0xFF0000
                    )
                embed.set_author(name='It appears you have timed out.', icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            rawreaction = str(confirm[0])
            if dictionary[rawreaction] == "leave":
                await ctx.send("The changes have been saved!")
                save()
                return
            if dictionary[rawreaction] in activated_features:
                activated_features.remove(dictionary[rawreaction].lower())
                save()
            else:
                activated_features.append(dictionary[rawreaction].lower())
                save()
            await msg.remove_reaction(rawreaction, ctx.author)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.client.user:
            return
        activated_features = DiscordGuild.find_one({"id":message.guild.id}, {"automod"})["automod"]
        embed = discord.Embed()
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_author(icon_url=self.client.user.avatar_url, name="Command Error")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.color=discord.Color.red()
        embed.title = "Illegal Action"
        embed.set_footer(text="you can change this setting with %sautomod or by using our new [Server Dashboard](%s)"%(Globals.getPrefix(message.guild.id), Globals.getDashboardURL()))
        def spam_check(msg):
            return (
                (msg.author == message.author)
                and len(msg.mentions)
                and (
                    (datetime.datetime.utcnow() - msg.created_at).seconds < 20
                )
            )

        # if channel id's data contains "links":
        if "links" in activated_features:
            if search(self.url_regex, message.content):
                await message.delete()
                embed.description = "```You cant send links in this channel.```"
                await message.channel.send(embed=embed)
        # if channel id's data contains "images"
        if "images" in activated_features:
            if any([hasattr(a, "width") for a in message.attachments]):
                await message.delete()
                embed.description = "```You cant send images in this channel.```"
                await message.channel.send(embed=embed)

        # if channel id's data contains "spam":
        if "spam" in activated_features:
            if (
                len(
                    list(
                        filter(
                            lambda m: spam_check(m), self.client.cached_messages
                        )
                    )
                )
                >= 5
            ):
                embed.description = "```please stop spamming.```"
                await message.channel.send(embed=embed)
def setup(client):
    client.add_cog(AutoMod(client))