from discord.ext.commands.cooldowns import BucketType
from datetime import date
from inspect import trace
from logging import exception
from operator import mul
from os import name
from typing import AsyncContextManager
import discord
from discord import errors
from discord import client
from discord import channel
from discord import embeds
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.core import check, command
from discord.member import Member
from discord.player import PCMAudio
from discord.utils import time_snowflake
from pymongo import MongoClient, settings
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
from pymongo.message import _do_batched_op_msg
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
import pymongo
import ssl
global ServerSettings
ServerSettings = {
    "Profanity Filter":{"desc":"Censors Profanity.", "enabled":True},
    "lol on message":{"desc":"sends a lol message when someone laughs", "enabled":True},
    "announce":{"desc":"settings for `^announce`", "enabled":True},
    "suggest":{"desc":"settings for `^suggest`", "enabled":True},
}
global ServerConfig
ServerConfig = [
    {"name":"prefix", "value":"^"},
    {"name":"badwords", "value":["fuck", "bitch", "shit", "cunt"]},
    {"name":"announcement channels", "value":[]},
    {"name":"suggestion channels", "value":[]},
    {"name":"automod", "value":["links", "images","spam"]}
]
    



global DatabaseKeys
DatabaseKeys = [
    {"name":"needsUpdate", "value":True},
    {"name":"gf", "value":0},
    {"name":"lp", "value":0},
    {"name":"breakups", "value":0},
    {"name":"kisses", "value":0},
    {"name":"boinks", "value":0},
    {"name":"money", "value":0},
    {"name":"job", "value":None},
    {"name":"duelwins", "value":0},
    {"name":"duelloses", "value":0},
    {"name":"duelretreats", "value":0},
    {"name":"inv", "value":[]},
    {"name":"watchlist", "value":[]},
    {"name":"achievements", "value":[]},
    {"name":"proposes", "value":0},
    {"name":"dates", "value":0},
    {"name":"relationships", "value":0, "conditional":"gf", "ModifiedVal":1},
    {"name":"gambles", "value":0},
    {"name":"gamblewins","value":0},
    {"name":"upgradepoints","value":0},
    {"name":"gameskill","value":{}},
    {"name":"bank", "value":0},
    {"name":"net","value":0},
    {"name":"abilityxp", "value":{}},
    {"name":"mmorpg",
    "value":{
        "level":1,
        "class":None,
        "stats":{
            "strength":1, 
            "intelligence":100, 
            "defense":1, 
            "health":100,
            }, 
        "abilities":{"Punch":1},
        
        "loadout":{
            "head":None, 
            "torso":None, 
            "pants":None, 
            "arms":None, 
            "hands":None, 
            "primary":None,
            "secondary":None,
        }
    }
    }
]
global Serverdbcheck
async def Serverdbcheck(guild):
    global ServerConfig
    for x in ServerConfig:
        try:
            value = DiscordGuild.find_one({"id":guild.id},{x["name"]})[x["name"]]
        except:
            Dbmsg=True
            DiscordGuild.update_one({"id":guild.id}, {"$set":{x["name"]:x["value"]}}, True)

global ServerCheck
async def ServerCheck(guild):
    global ServerSettings
    try:
        settings = DiscordGuild.find_one({"id":guild.id}, {"settings"})["settings"]
        for x in ServerSettings.keys():
            try:
                z = settings[x]
            except:
                Dbmsg=True
                settings[x] = ServerSettings[x]
                DiscordGuild.update_one({"id":guild.id}, {"$set":{"settings":ServerSettings}}, True)
    except:
        Dbmsg=True
        print(traceback.format_exc())
        stats = levelling.find_one({"id" : guild.id})
        if stats == None:
            DiscordGuild.insert_one({"id":guild.id, "settings":ServerSettings})
        else:
            DiscordGuild.update_one({"id":guild.id}, {"$set":{"settings":ServerSettings}})

global abilityLevelCheck
async def abilityLevelCheck(user:discord.Member):
    mmorpg = mulah.find_one({"id":user.id},{"mmorpg"})["mmorpg"]
    abilityxp = mulah.find_one({"id":user.id},{"abilityxp"})["abilityxp"]
    for x in abilityxp.keys():
        if Globals.getLevelfromxp(abilityxp[x])!=mmorpg["abilities"][x]:
            mmorpg["abilities"][x] = Globals.getLevelfromxp(abilityxp[x])
    mulah.update_one({"id":user.id}, {"$set":{"mmorpg":mmorpg}})


global abilityxpcheck
async def abilityxpcheck(user:discord.Member):
    ability = mulah.find_one({"id":user.id},{"mmorpg"})["mmorpg"]["abilities"]
    abilityxp = mulah.find_one({"id":user.id},{"abilityxp"})["abilityxp"]
    for x in ability.keys():
        if x not in abilityxp.keys():
            abilityxp[x]=0
    mulah.update_one({"id":user.id}, {"$set":{"abilityxp":abilityxp}})



global dbcheck
async def dbcheck(user:discord.Member):
    global DatabaseKeys
    global Dbmsg
    try:
        needsUpdate = mulah.find_one({"id":user.id},{"needsUpdate"})["needsUpdate"]
    except:
        mulah.update_one({"id":user.id}, {"$set":{"needsUpdate":True}}, True)
        needsUpdate = mulah.find_one({"id":user.id},{"needsUpdate"})["needsUpdate"]
        print("updated %s' needUpdate to True"%(user.display_name))
    if needsUpdate:
        mulah.update_one({"id":user.id}, {"$set":{"needsUpdate":False}})
        print("updated %s' needUpdate to False"%(user.display_name))
        for x in DatabaseKeys:
            try:
                value = mulah.find_one({"id":user.id},{x["name"]})[x["name"]]
            except:
                Dbmsg=True
                mulah.update_one({"id":user.id}, {"$set":{x["name"]:x["value"]}})
                print("updated %s' %s"%(user.display_name, x["name"]))
                try:
                    value = mulah.find_one({"id":user.id},{x["name"]})[x["name"]]
                except:
                    Dbmsg=True
                    mulah.update_one({"id":user.id}, {"$set":{x["name"]:x["value"]}}, True)
                    print("updated %s' %s"%(user.display_name, x["name"]))        




cluster = Globals.getMongo()
mulah = cluster["discord"]["mulah"]
levelling = cluster["discord"]["levelling"]
DiscordGuild = cluster["discord"]["guilds"]

class DatabaseHandler(commands.Cog):
    def __init__(self, client):
        self.client = client



    global getNumMembers
    def getNumMembers():
        membersz=0
        for x in self.client.guilds:
            membersz+=len(x.members)+1
        return membersz        


    @commands.has_permissions(administrator=True)
    @commands.command()
    async def resetguild(self, ctx):
        guild = ctx.guild
        for x in ServerConfig:
            DiscordGuild.update_one({"id":guild.id}, {"$set":{x["name"]:x["value"]}}, True)
        DiscordGuild.update_one({"id":guild.id}, {"$set":{"settings":ServerSettings}})
        await ctx.channel.send("Guild settings have been reset to default")



    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.client.user:
            return
        if ctx.author.bot: return


        await abilityxpcheck(ctx.author)
        await abilityLevelCheck(ctx.author)
        money = mulah.find_one({"id":ctx.author.id}, {"money"})["money"]
        bank = mulah.find_one({"id":ctx.author.id}, {"bank"})["bank"]
        mulah.update_one({"id":ctx.author.id}, {"$set":{"money":math.ceil(money)}})
        mulah.update_one({"id":ctx.author.id}, {"$set":{"net":money+bank}})

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        await ServerCheck(guild)
        await Serverdbcheck(guild)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name = "^help %s users"%(getNumMembers())))
        for x in guild.members:
            if not x.bot:
                await dbcheck(x)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            await dbcheck(member)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            for member in guild.members:
                if not member.bot:
                    await dbcheck(member)
        print("The bot is ready, and the database has been updated")

    @commands.command()
    async def updateWholeDb(self, ctx):
        for guild in self.client.guilds:
            for member in guild.members:
                mulah.update_one({"id":member.id}, {"$set":{"needsUpdate":True}})
                await dbcheck(member)
        await ctx.channel.send("The bot is ready, and the database has been updated")  

    @commands.Cog.listener()
    async def on_command_completion(self,ctx):
        try:
            gfval = mulah.find_one({"id":ctx.author.id}, {"gf"})["gf"]
            lpval = mulah.find_one({"id":ctx.author.id}, {"lp"})["lp"]
            breakups = mulah.find_one({"id":ctx.author.id}, {"breakups"})["breakups"]
            kisses = mulah.find_one({"id":ctx.author.id}, {"kisses"})["kisses"]
            boinks = mulah.find_one({"id":ctx.author.id}, {"boinks"})["boinks"]
            dates = mulah.find_one({"id":ctx.author.id}, {"dates"})["dates"]
            relationships = mulah.find_one({"id":ctx.author.id}, {"relationships"})["relationships"]
            proposes = mulah.find_one({"id":ctx.author.id}, {"proposes"})["proposes"]
            money = mulah.find_one({"id":ctx.author.id}, {"money"})["money"]
            inv = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
            watchlist = mulah.find_one({"id":ctx.author.id}, {"watchlist"})["watchlist"]
            gameskill = mulah.find_one({"id":ctx.author.id}, {"gameskill"})["gameskill"]
            gambles = mulah.find_one({"id":ctx.author.id}, {"gambles"})["gambles"]
            gamblewins = mulah.find_one({"id":ctx.author.id}, {"gamblewins"})["gamblewins"]
            job = mulah.find_one({"id":ctx.author.id}, {"job"})["job"]
        except:
            pass
        
        UserAchievements = mulah.find_one({"id":ctx.author.id}, {"achievements"})["achievements"]
        
        try:
            if boinks>=1:
                await Globals.AchievementEmbed(ctx, "Virginity Loss!")
            
            if breakups>=10:
                await Globals.AchievementEmbed(ctx, "Jerk")

            if kisses>=1:
                await Globals.AchievementEmbed(ctx, "First Kiss!")

            if proposes>=1:
                await Globals.AchievementEmbed(ctx, "Engaged!")
            
            if money>=15:
                await Globals.AchievementEmbed(ctx, "Getting By")

            if money>=1000000:
                await Globals.AchievementEmbed(ctx, "Millionaire!")
            
            if money>=1000000000:
                await Globals.AchievementEmbed(ctx, "Billionaire!")
            
            if gameskill["Minecraft"]>=100:
                await Globals.AchievementEmbed(ctx, "FloorGang")
            
            if gameskill["League of Legends"]>100:
                await Globals.AchievementEmbed(ctx, "virgin")
            
            if dates>=1:
                await Globals.AchievementEmbed(ctx, "First Date!")
            
            if any(x for x in inv if "parts" in x.keys()):
                await Globals.AchievementEmbed(ctx, "First PC!")
            
            for x in inv:
                if "parts" in x.keys(): 
                    if len(x["games"])>=5:
                        await Globals.AchievementEmbed(ctx, "True Gamer")

                    if x["parts"]["power"]>=12000:
                        await Globals.AchievementEmbed(ctx, "Linus Tech Tips")
            if gambles>=1:
                await Globals.AchievementEmbed(ctx, "Gambler!")

            if gamblewins>=1:
                await Globals.AchievementEmbed(ctx, "Winner!")
            if job:
                await Globals.AchievementEmbed(ctx, "Employed!")
        except:
            pass



    @commands.command()
    async def ResetGuildSettings(self, ctx):
        if ctx.author.guild_permissions.administrator:
            DiscordGuild.update_one({"id":ctx.guild.id}, {"$set":{"settings":ServerSettings}})
            print("updated %s' guild"%(ctx.author))
            await ctx.channel.send("Done.   ")



    @commands.command()
    async def editDB(self,ctx, key, val:int, p1:discord.Member=None):
        if ctx.author.id==643764774362021899:
            if p1 ==None:
                p1=ctx.author
            mulah.update_one({"id":p1.id}, {"$set":{key:val}})
            await ctx.channel.send("ok creator senpai! i did it.")



    @commands.command()
    async def resetDB(self, ctx, key, p1:discord.Member=None):
        global DatabaseKeys
        if ctx.author.id==643764774362021899:
            if p1 ==None:
                p1=ctx.author
            x = next(a for a in DatabaseKeys if a["name"].lower()==key.lower())
            mulah.update_one({"id":p1.id}, {"$set":{x["name"]:x["value"]}})
            await ctx.channel.send("ok creator senpai! i did it.")


            


    @commands.command()
    async def database(self, ctx,p1:discord.Member=None):
        if p1==None:
            p1=ctx.author
        if ctx.author.id==643764774362021899:
            await dbcheck(p1)
            await ctx.channel.send("I have completed the database check for %s"%(p1.display_name))

    @commands.command()
    async def CheckDatabase(self, ctx, key:str, p1:discord.Member=None):
        if p1==None:
            p1=ctx.author
        if ctx.author.id==643764774362021899:
            Data = mulah.find_one({"id":p1.id}, {key})
            await ctx.channel.send("```%s```"%(Data))



    @commands.command()
    async def removeachievement(self, ctx, achievement, p1:discord.Member=None):
        if str(ctx.author) == "SentientPlatypus#1332":
            if p1 ==None:
                p1=ctx.author
            achievementval = mulah.find_one({"id":p1.id}, {"achievements"})["achievements"]
            achievementval.remove(achievement)
            mulah.update_one({"id":p1.id},{"$set":{"achievements":achievementval}})
            await ctx.channel.send("I have removed %s from %s, creator senpai!"%(achievement, p1.display_name))


    @commands.command()
    async def debug(self, ctx, dictionary:str, member:discord.Member):
        z = mulah.find_one({"id":member.id}, {dictionary})
        await ctx.channel.send("%s"%(z))
        x = z[dictionary]
        await ctx.channel.send("%s"%(x))



















def setup(client):
    client.add_cog(DatabaseHandler(client))