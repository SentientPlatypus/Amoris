
from typing import Optional

from discord import Embed, member
from discord.ext import commands
from discord.ext.commands import Cog, command
import discord
from discord.ext.menus import ListPageSource, Menu, MenuPages
from discord.utils import get
import Globals
import asyncio
import pymongo
from pymongo import MongoClient
cluster = Globals.getMongo()
DiscordGuild = cluster["discord"]["guilds"]

#python pagekite.py 5000 scp16tsundere.pagekite.me

class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=5)
    
    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(title="Help",
                      description="SCP help!",
                      color=self.ctx.author.color)
        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
        
        return embed
    
    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((entry.brief or "No description", Globals.syntax(entry)))

        return await self.write_page(menu, fields)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    async def cmd_help(self, ctx, command):
        embed = Embed(title=f"Help with `{command}`",
                        description=Globals.syntax(command),
                        color=ctx.author.color)
        embed.add_field(name="Command description", value=command.help)
        await ctx.send(embed=embed)

    @command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):

        if cmd is None:
            leave=False
            pgnum=1
            while leave==False:
                embed = discord.Embed(title = "Help", description = "Use `%shelp <command>` for extended information on a command.\n If the command is in a group, please use `%s <group>` to get more info"%(DiscordGuild.find_one({"id":ctx.author.guild.id}, {"prefix"})["prefix"],DiscordGuild.find_one({"id":ctx.author.guild.id}, {"prefix"})["prefix"]),color = discord.Color.from_rgb(255, 192, 203))
                if pgnum==1:
                    embed.add_field(name="Bot", value="> `info`,`help`, `credit`",inline=False)
                    embed.add_field(name = "MODERATION🚨", value = Globals.getModCommands(),inline=False)
                    embed.add_field(name = "ECONOMY💰", value = Globals.getEconomyCommands(),inline=False)
                    embed.add_field(name = "DATINGSIM❤️", value = Globals.getGfCommands(),inline=False)
                    embed.add_field(name = "DUELS ⚔️", value = Globals.getDuelsCommands(),inline=False)
                if pgnum==2:
                    embed.add_field(name = "LEVELS📈", value = Globals.getLevelCommands(),inline=False)
                    embed.add_field(name = "FUN😃", value = Globals.getFunCommands(),inline=False)
                    embed.add_field(name = "IMAGES📷", value = Globals.getImageCommands(),inline=False)
                if pgnum == 3:
                    embed.add_field(name = "GAMES🎮", value = Globals.getGamesCommands(),inline=False)
                    embed.add_field(name = "SOLVE🖩", value = Globals.getSolveCommands(),inline=False)
                    embed.add_field(name = "MATH📚📐📏", value = Globals.getMathCommands(),inline=False)
                    embed.add_field(name = "WEB🌎", value = Globals.getWebCommands(),inline=False)
                if pgnum == 4:
                    embed.add_field(name = "UTILITY🔧", value = Globals.getUtilityCommands(),inline=False)
                    embed.add_field(name = "SETTINGS ⚙️", value = Globals.getSettingsCommands(),inline=False)
                    embed.add_field(name = "VOICE CHAT 🎵 ", value = Globals.getVcCommands(),inline=False)	



                embed.set_footer(text="I have a completed webapp/user interface to make server management easier, but I am currently looking for online hosting for it.")
                try:
                    await msg.edit(embed=embed)
                    await msg.remove_reaction(emoji=rawreaction, member=ctx.author)
                except:
                    msg= await ctx.send(embed = embed)
                    await msg.add_reaction("⬅️") 
                    await msg.add_reaction("➡️")
                try:
                    def check(reaction, user):
                        return user==ctx.author and str(reaction.emoji) in ["➡️","⬅️"] and reaction.message == msg
                    confirm = await self.bot.wait_for('reaction_add',check=check, timeout = 60)
                    try:
                        if confirm:
                            rawreaction = str(confirm[0])
                            if rawreaction=="➡️":
                                pgnum+=1
                                if pgnum>4:
                                    pgnum=1
                            elif rawreaction=="⬅️":
                                pgnum-=1
                                if pgnum<1:
                                    pgnum=1
                    except:
                        pass
                except asyncio.TimeoutError:
                    break

        
        else:
            if (command := get(self.bot.commands, name=cmd)):
                await self.cmd_help(ctx, command)
            else:
                await ctx.send("That command does not exist.")


def setup(bot):
    bot.add_cog(Help(bot))