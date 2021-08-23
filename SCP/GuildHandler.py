from asyncio.events import set_child_watcher
from datetime import date
from inspect import trace
from logging import exception
from operator import mul
from os import name, path, spawnl
from typing import AsyncContextManager
import discord
from discord import errors
from discord import client
from discord import channel
from discord import embeds
from discord import player
from discord import file
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.core import command
from discord.ext.commands.help import _HelpCommandImpl
from discord.member import Member
from discord.player import PCMAudio
from discord.utils import time_snowflake
from pymongo import MongoClient
import names
from pymongo.collection import _FIND_AND_MODIFY_DOC_FIELDS
import re
import random
import math
import asyncio
import linecache
import sys
import traceback
import string
import itertools
from imdb import IMDb
from pymongo.database import Database
from pymongo.read_preferences import Secondary
from youtube_search import YoutubeSearch
import json
import youtube_dl
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import text2emotion as te
from removebg import RemoveBg
import os
from PIL import Image
from io import BytesIO
import requests
import Globals
from discord import Color

cluster = MongoClient('mongodb+srv://SCPT:Geneavianina@scptsunderedatabase.fp8en.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
DiscordGuild = cluster["discord"]["guilds"]

class GuildHandler(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def settings(self, ctx, command=None, value=None):
        settings = DiscordGuild.find_one({"id":ctx.guild.id}, {"settings"})["settings"]
        if not command:
            embed = discord.Embed(title = 'Server Settings', description = 'This servers settings.\n use `^settings "<command>" <enable|disable>`\n `^configuration` is to alter server settings.')
            for x in settings.keys():
                check=""
                if settings[x]["enabled"]==True:
                    check = "✅ `enabled`"
                else:
                    check="❌ `disabled`"
                embed.add_field(name = x, value = "%s\n%s"%(settings[x]["desc"], check), inline=False)
            await ctx.channel.send(embed=embed)
        
        else:
            if ctx.author.guild_permissions.administrator:
                namekey = []
                for l in settings.keys():
                    namekey.append(l.lower())
                    
                if command!=None and value==None:
                    if command.lower() in namekey:
                        setting = next(x for x in settings.keys() if x.lower()==command.lower())
                        embed = discord.Embed(title = setting, description = settings[setting]["desc"] + "\n use `^settings <command> <value>`")
                        check=""
                        if settings[setting]["enabled"]==True:
                            check = "✅ `enabled`"
                        else:
                            check="❌ `disabled`"
                        embed.add_field(name = "Setting:", value = "%s\n%s"%(settings[setting]["desc"], check), inline=False)
                        await ctx.channel.send(embed=embed)
                else:
                    if command.lower() in namekey:
                        setting = next(x for x in settings.keys() if x.lower()==command.lower())
                        embed = discord.Embed(title = "You Updated "+setting, description = settings[setting]["desc"] + "\n use `^settings <command> <value>`")
                        if value.lower() == "enable".lower():
                            settings[setting]["enabled"]=True
                            DiscordGuild.update_one({"id":ctx.guild.id}, {"$set":{"settings":settings}})
                        if value.lower()=="disable".lower():
                            settings[setting]["enabled"]=False
                            DiscordGuild.update_one({"id":ctx.guild.id}, {"$set":{"settings":settings}})
                        check=""
                        if settings[setting]["enabled"]==True:
                            check = "✅ `enabled`"
                        elif settings[setting]["enabled"]==False:
                            check="❌ `disabled`"
                        else:
                            check="✅"
                        embed.add_field(name = "Setting:", value = "%s\n%s"%(settings[setting]["desc"], check), inline=False)
                        await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("You do not have those perms")

        

    @commands.group(invoke_without_command=True)
    async def configuration(self, ctx):
        embed= discord.Embed(title = "Edit values for server settings!")
        embed.add_field(name = "commands", value = "`^configuration badword`, `^configuration announcement`, `^configuration suggestion`")
        await ctx.channel.send(embed=embed)
    
    @configuration.command()
    async def badword(self, ctx):
        leave = False
        if ctx.author.guild_permissions.administrator:
            while leave==False:
                print("this worked")
                embed = discord.Embed(title = "Bad Words!", value = "These words will be censored if `Profanity Filter` is enabled.", color = ctx.author.color)
                words = DiscordGuild.find_one({"id":ctx.guild.id}, {"badwords"})
                print(words)
                try:
                    embed.add_field(name = "badwords:", value = "Observe:\n"+"\n".join(words["badwords"]))
                except:
                    embed.add_field(name = "badwords:", value = "Default")
                msg = await ctx.channel.send(embed=embed)   
                if not ctx.author.guild_permissions.administrator:
                    break
                words = DiscordGuild.find_one({"id":ctx.guild.id}, {"badwords"})
                print(words)
                try:
                    await msg.clear_reactions()
                except:
                    pass
                choice = await Globals.AddChoices(self, ctx, ["➕", "➖", "🚪"], msg)
                if choice=="➕":
                    await ctx.channel.send(embed=discord.Embed(title = "Type a word to add to the badword list"))
                    def check(m):
                        return m.author ==ctx.author and m.channel ==ctx.channel
                    wordtoadd = await self.client.wait_for('message', check=check, timeout=30)
                    try:
                        words["badwords"].append(wordtoadd.content.lower())
                    except asyncio.TimeoutError:
                        pass
                if choice=="➖":
                    await ctx.channel.send(embed=discord.Embed(title = "Type a word to remove from the badword list"))
                    def check(m):
                        return m.author ==ctx.author and m.channel ==ctx.channel
                    wordtoadd = await self.client.wait_for('message', check=check, timeout=30)
                    try:
                        words["badwords"].remove(wordtoadd.content.lower())
                    except asyncio.TimeoutError:
                        pass          
                if choice=="🚪":
                    break
                DiscordGuild.update_one({"id":ctx.guild.id}, {"$set":{"badwords":words["badwords"]}})
        else:
            await ctx.channel.send("You dont have the permissions.")                
                    

    @configuration.command()
    async def announcement(self, ctx):
        leave = False
        if ctx.author.guild_permissions.administrator:
            while leave==False:
                embed = discord.Embed(title = "Announcement Channels!", value = "Channels to send announcements to!.\n react with ➕ and type the channel id!", color = ctx.author.color)
                words = DiscordGuild.find_one({"id":ctx.guild.id}, {"announcement channels"})
                try:
                    embed.add_field(name = "Channels:", value = "Observe:\n"+"\n".join([str(i) for i in words["announcement channels"]]))
                except:
                    embed.add_field(name = "Channels:", value = "Default")
                msg = await ctx.channel.send(embed=embed)   
                if not ctx.author.guild_permissions.administrator:
                    break
                words = DiscordGuild.find_one({"id":ctx.guild.id}, {"announcement channels"})
                print(words)
                try:
                    await msg.clear_reactions()
                except:
                    pass
                choice = await Globals.AddChoices(self, ctx, ["➕", "➖", "🚪"], msg)
                if choice=="➕":
                    await ctx.channel.send(embed=discord.Embed(title = "Type a channel id to add"))
                    def check(m):
                        return m.author ==ctx.author and m.channel ==ctx.channel
                    wordtoadd = await self.client.wait_for('message', check=check, timeout=30)
                    wordtoadd  = int(wordtoadd.content)
                    if ctx.guild.get_channel(wordtoadd):
                        try:
                            words["announcement channels"].append(wordtoadd)
                        except asyncio.TimeoutError:
                            pass
                if choice=="➖":
                    await ctx.channel.send(embed=discord.Embed(title = "Type a channel id to remove from the list"))
                    def check(m):
                        return m.author ==ctx.author and m.channel ==ctx.channel
                    wordtoadd = await self.client.wait_for('message', check=check, timeout=30)
                    wordtoadd  = int(wordtoadd.content)
                    if ctx.guild.get_channel(wordtoadd):
                        try:
                            words["announcement channels"].remove(wordtoadd)
                        except asyncio.TimeoutError:
                            pass          
                if choice=="🚪":
                    break
                DiscordGuild.update_one({"id":ctx.guild.id}, {"$set":{"announcement channels":words["announcement channels"]}})
        else:
            await ctx.channel.send("You dont have the permissions.")


    @configuration.command()
    async def suggestion(self, ctx):
        leave = False
        if ctx.author.guild_permissions.administrator:
            while leave==False:
                embed = discord.Embed(title = "Suggestion Channels!", value = "Channels to send suggestions to!.\nreact with ➕ and type the channel id!", color = ctx.author.color)
                words = DiscordGuild.find_one({"id":ctx.guild.id}, {"suggestion channels"})
                try:
                    embed.add_field(name = "Channels:", value = "Observe:\n"+"\n".join([str(i) for i in words["suggestion channels"]]))
                except:
                    embed.add_field(name = "Channels:", value = "Default")
                msg = await ctx.channel.send(embed=embed)   
                if not ctx.author.guild_permissions.administrator:
                    break
                words = DiscordGuild.find_one({"id":ctx.guild.id}, {"suggestion channels"})
                print(words)
                try:
                    await msg.clear_reactions()
                except:
                    pass
                choice = await Globals.AddChoices(self, ctx, ["➕", "➖", "🚪"], msg)
                if choice=="➕":
                    await ctx.channel.send(embed=discord.Embed(title = "Type a channel id to add"))
                    def check(m):
                        return m.author ==ctx.author and m.channel ==ctx.channel
                    wordtoadd = await self.client.wait_for('message', check=check, timeout=30)
                    wordtoadd  = int(wordtoadd.content)
                    if ctx.guild.get_channel(wordtoadd):
                        try:
                            words["suggestion channels"].append(wordtoadd)
                        except asyncio.TimeoutError:
                            pass
                if choice=="➖":
                    await ctx.channel.send(embed=discord.Embed(title = "Type a channel id to remove from the list"))
                    def check(m):
                        return m.author ==ctx.author and m.channel ==ctx.channel
                    wordtoadd = await self.client.wait_for('message', check=check, timeout=30)
                    wordtoadd  = int(wordtoadd.content)
                    if ctx.guild.get_channel(wordtoadd):
                        try:
                            words["suggestion channels"].remove(wordtoadd)
                        except asyncio.TimeoutError:
                            pass          
                if choice=="🚪":
                    break
                DiscordGuild.update_one({"id":ctx.guild.id}, {"$set":{"suggestion channels":words["suggestion channels"]}})
        else:
            await ctx.channel.send("You dont have the permissions.")





def setup(client):
    client.add_cog(GuildHandler(client))