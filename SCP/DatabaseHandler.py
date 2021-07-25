
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
from discord.ext.commands.core import command
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
cluster = MongoClient('mongodb+srv://SCPT:Geneavianina@scptsunderedatabase.fp8en.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mulah = cluster["discord"]["mulah"]
levelling = cluster["discord"]["levelling"]

class DatabaseHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        global achievements
        achievements = [
            {"name":"First Kiss!", "desc":"Kiss someone for the first time!", "category":"relationships"},
            {"name":"Virginity Loss!", "desc":"Boink someone for the first time!", "category":"relationships"},
            {"name":"Engaged!", "desc":"Propose to someone for the first time!", "category":"relationships"},
            {"name":"Jerk", "desc":"Turns out you were the problem", "category":"relationships"},
            {"name":"Divorcee!", "desc":"Get a life bro.", "category":"relationships"},
            {"name":"First Date!", "desc":"First date with GF!", "category":"relationships"},
            

            {"name":"Getting By", "desc":"finally making some money! good job!", "category":"finance"},
            {"name":"Millionaire!", "desc":"its what it sounds like", "category":"finance"},
            
            {"name":"Billionaire!", "desc":"Treat your workers with respect.", "category":"finance"},
            {"name":"Employed!", "desc":"You got a job.", "category":"finance"},
            {"name":"Gambler!", "desc":"You gambled for the first time! ", "category":"finance"},
            {"name":"Winner!", "desc":"You won a gamble! ", "category":"finance"},


            {"name":"Death!", "desc":"Get a life bro.", "category":"finance"},
            {"name":"virgin", "desc":"Secret!", "category":"gaming"},
            {"name":"FloorGang", "desc":"Secret!", "category":"gaming"},
            {"name":"First PC!", "desc":"Create your first PC!", "category":"gaming"},
            {"name":"Linus Tech Tips", "desc":"Create a beefy Computer with at least 12000 power!", "category":"gaming"},
            {"name":"True Gamer", "desc":"Install 5 games on a single PC!", "category":"gaming"},
            
        ]







    @commands.Cog.listener()
    async def on_message(self, ctx):
        global dbcheck
        async def dbcheck(user):
            DatabaseKeys = [
                {"name":"gf", "value":0},
                {"name":"lp", "value":0},
                {"name":"breakups", "value":0},
                {"name":"kisses", "value":0},
                {"name":"boinks", "value":0},
                {"name":"money", "value":0},
                {"name":"inv", "value":[]},
                {"name":"watchlist", "value":[]},
                {"name":"achievements", "value":[]},
                {"name":"proposes", "value":0},
                {"name":"dates", "value":0},
                {"name":"relationships", "value":0, "conditional":"gf", "ModifiedVal":1},
                {"name":"gambles", "value":0},
                {"name":"gamblewins","value":0},
                {"name":"gameskill","value":{}},
                {"name":"mmorpg",
                "value":{
                    "level":1,
                    "class":None,
                    "stats":{
                        "strength":1, 
                        "intelligence":1, 
                        "defense":1, 
                        "health":100,
                        "sense":1}, 
                    "abilities":{
                    }, 
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
            for x in DatabaseKeys:
                try:
                    value = mulah.find_one({"id":ctx.author.id},{x["name"]})[x["name"]]
                except:
                    if x["name"]=="gf":
                        print("the gf bug is this")
                        mulah.update_one({"id":ctx.author.id}, {"$set":{x["name"]:x["value"]}})
                    mulah.update_one({"id":ctx.author.id}, {"$set":{x["name"]:x["value"]}})
                    print("updated %s' %s"%(ctx.author.display_name, x["name"]))
        if ctx.author == self.client.user:
            if ctx.author.bot: return
            return


        await dbcheck(ctx.author)


    @commands.Cog.listener()
    async def on_command_completion(self,ctx):
        global achievements
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
        except:
            pass
        
        UserAchievements = mulah.find_one({"id":ctx.author.id}, {"achievements"})["achievements"]

        async def AchievementEmbed(EarnedAchievement):
            UserAchievements = mulah.find_one({"id":ctx.author.id}, {"achievements"})["achievements"]
            if EarnedAchievement not in UserAchievements:
                global achievements
                AchievementDict = next(x for x in achievements if x["name"]==EarnedAchievement)
                embed = discord.Embed(title = "Congratulations! you earned the achievement %s"%(AchievementDict["name"]), description = AchievementDict["desc"], color = ctx.author.color)
                embed.set_image(url = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/socialmedia/apple/271/trophy_1f3c6.png')
                UserAchievements.append(EarnedAchievement)
                mulah.update_one({"id":ctx.author.id}, {"$set":{"achievements":UserAchievements}})
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)            

        if boinks>=1:
            await AchievementEmbed("Virginity Loss!")
        
        if breakups>=10:
            await AchievementEmbed("Jerk")

        if kisses>=1:
            await AchievementEmbed("First Kiss!")

        if proposes>=1:
            await AchievementEmbed("Engaged!")
        
        if money>=15:
            await AchievementEmbed("Getting By")

        if money>=1000000:
            await AchievementEmbed("Millionaire!")
        
        if money>=1000000000:
            await AchievementEmbed("Billionaire!")
        
        if gameskill["Minecraft"]>=100:
            await AchievementEmbed("FloorGang")
        
        if gameskill["League of Legends"]>100:
            await AchievementEmbed("virgin")
        
        if dates>=1:
            await AchievementEmbed("First Date!")
        
        if any(x for x in inv if "parts" in x.keys()):
            await AchievementEmbed("First PC!")
        
        for x in inv:
            if "parts" in x.keys(): 
                if len(x["games"])>=5:
                    await AchievementEmbed("True Gamer")

                if x["parts"]["power"]>=12000:
                    await AchievementEmbed("Linus Tech Tips")
        if gambles>=1:
            await AchievementEmbed("Gambler!")

        if gamblewins>=1:
            await AchievementEmbed("Winner!")








    @commands.command()
    async def editDB(self,ctx, key, val:int, p1:discord.Member=None):
        if str(ctx.author)=="SentientPlatypus#1332":
            if p1 ==None:
                p1=ctx.author
            mulah.update_one({"id":p1.id}, {"$set":{key:val}})
            await ctx.channel.send("ok creator senpai! i did it.")



    @commands.command()
    async def resetDB(self, ctx, key, p1:discord.Member=None):
        global DatabaseKeys
        if str(ctx.author)=="SentientPlatypus#1332":
            if p1 ==None:
                p1=ctx.author
            x = next(a for a in DatabaseKeys if a["name"].lower()==key.lower())
            mulah.update_one({"id":p1.id}, {"$set":{x["name"]:x["value"]}})
            await ctx.channel.send("ok creator senpai! i did it.")



    @commands.command()
    async def database(self, ctx,p1:discord.Member=None):
        if p1 ==None:
            p1=ctx.author
        if str(ctx.author)=="SentientPlatypus#1332":
            global dbcheck
            dbcheck(p1)
            await ctx.channel.send("I have completed the database check for %s, creator senpai!!!"%(p1.display_name))




    @commands.command()
    async def removeachievement(self, ctx, achievement, p1:discord.Member=None):
        if str(ctx.author) == "SentientPlatypus#1332":
            if p1 ==None:
                p1=ctx.author
            achievementval = mulah.find_one({"id":p1.id}, {"achievements"})["achievements"]
            achievementval.remove(achievement)
            mulah.update_one({"id":p1.id},{"$set":{"achievements":achievementval}})
            await ctx.channel.send("I have removed %s from %s, creator senpai!"%(achievement, p1.display_name))






















def setup(client):
    client.add_cog(DatabaseHandler(client))