from asyncio.events import set_child_watcher
from datetime import date, datetime, timedelta
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
levelling = cluster["discord"]["levelling"]
DiscordGuild = cluster["discord"]["guilds"]
mulah = cluster["discord"]["mulah"]
class levelsys(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ready')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.client.user:
            return
        if DiscordGuild.find_one({"id":ctx.guild.id}, {"settings"})["settings"]["Profanity Filter"]["enabled"]==True:
            global badwords
            list = DiscordGuild.find_one({"id":ctx.guild.id}, {"badwords"})["badwords"]
            if not list:
                badwords = ["fuck", "bitch", "shit", "cunt", "entot", "anjing", "asw", "ngentod", "goblok", "gblk", "wtf", "ngentot"]
            else:
                badwords = list
            global badwordresponse
            badwordresponse = ["Language. My  creator senpai does not support that vulgar language.", "Shut up. Dont taint this server with those words.", "Do not swear. use of those words is unacceptable."]
            if any(word in ctx.content.casefold() for word in badwords):
                await ctx.delete()
                randbadwords = random.choice(badwordresponse)
                count = 0
                for badwordint in range(0,len(badwords)):
                    count+= len(re.findall(badwords[badwordint], ctx.content.casefold()))
                    ctx.content = ctx.content.casefold().replace(badwords[badwordint],"*censor*")

                embed = discord.Embed(title = "Hey. I noticed that you tried to swear.", description = "%s"%(randbadwords), color = discord.Color.red())
                embed.add_field(name = "%s intended to say,"%(re.sub("\#\d{4}$", "", str(ctx.author))), value = "%s"%(ctx.content))
                await ctx.channel.send(embed = embed)
                try:
                    swearvar = levelling.find_one({"id":ctx.author.id}, {"swears"})
                    swearval = swearvar["swears"]
                    swearval+=count
                    levelling.update_one({"id":ctx.author.id},{"$set":{"swears":swearval}})
                except:
                    levelling.update_one({"id":ctx.author.id},{"$set":{"swears":1}})
            else:
                pass

        shutupresponse = ["how about you shut up.", "No, u", "can you shut up? your opinion is worth as much as an old cucumber"]

        shutuplist = ["shutup", "shut up", "stfu", "fuck you", "fuck u", "stupid bot"]
        #FUNNY
        if DiscordGuild.find_one({"id":ctx.guild.id}, {"settings"})["settings"]["lol on message"]["enabled"]==True:

            funny = ["lol", "lmao", "haha", "Lol", "Lmao"]
            if any(word in ctx.content.casefold() for word in funny):
                if ctx.author.id==643764774362021899:
                    trexyfunny = ["hahaha", "lmao", "lol"]
                    randtrexyfunny = random.choice(trexyfunny)
                    await ctx.channel.send(randtrexyfunny)
                else:
                    funnyresponse = ["lol", "lmao", "haha"]
                    randfunny = random.choice(funnyresponse)
                    await ctx.channel.send(randfunny)

        #SAD
        if DiscordGuild.find_one({"id":ctx.guild.id}, {"settings"})["settings"]["sad on message"]["enabled"]==True:
            sad = ["sad", "depressed", "depression", "unhappy"]
            if any(word in ctx.content for word in sad):
                if ctx.author.id==643764774362021899:
                    trexysad = [" creator senpai! dont be sad, Is there anything I can do to cheer you up?", " creator senpai, please feel better.", "NO, You are not allowed to feel that way,  creator senpai."]
                    randtrexysad = random.choice(trexysad)
                    await ctx.channel.send(randtrexysad)
                else:
                    sadresponse = ["cheer up. Its not like I care or anything.", "You need to be happier, My  creator senpai wants people to be happy"]
                    randsad = random.choice(sadresponse)
                    await ctx.channel.send(randsad)
                def check(m):
                    return m.author==ctx.author and m.channel == ctx.channel
                try:
                    shutupctx = await client.wait_for('ctx', check = check, timeout=5)
                except asyncio.TimeoutError:
                    pass
                if any(word in ctx.content.casefold() for word in shutuplist):
                    await ctx.channel.send(random.choice(shutupresponse))
                    
                else:
                    pass


            #WHY
        if DiscordGuild.find_one({"id":ctx.guild.id}, {"settings"})["settings"]["on message"]["enabled"]==True:
            if ctx.content.startswith("why"):
                if ctx.author.id==643764774362021899:
                    trexywhy = ["I will find out asap.", "I will google it for you,  creator senpai", "Someone, answer  creator senpai's question!"]
                    randtrexywhy = random.choice(trexywhy)
                    await ctx.channel.send(randtrexywhy)
                else:
                    whyy = ["Im not sure, Try asking my  creator senpai.", "How would I know? I dont even like talking to you guys, but my  creator senpai wants me to.", "Look it up, baka."]
                    randwhyy = random.choice(whyy)
                    await ctx.channel.send(randwhyy)
                def check(m):
                    return m.author==ctx.author and m.channel == ctx.channel
                try:
                    shutupctx = await self.client.wait_for('ctx', check = check, timeout=5)
                except asyncio.TimeoutError:
                    pass
                if any(word in ctx.content.casefold() for word in shutuplist):
                    await ctx.channel.send(random.choice(shutupresponse))
                    
                else:
                    pass
                    
            #UWU
            if ctx.content.casefold().startswith("uwu"):
                await ctx.channel.send("Shut up.")

            #appreciation

            praiseresponse = ["thank you. its not like I care though.", "My creator senpai made me that way. Thank him.", "...ty"]
            praiseresponsesentient = ["Its all thanks to you for working on me!", "Thank you creator senpai for the time you invest in me.", "I will never let you down!"]
            appreciationtext = "(ily|ty|good\sjob|well\sdone)(sm|\s(so\s)+(much))*\!*\s(bot|scp|tsundere)"
            contecttext = re.findall(appreciationtext, ctx.content.casefold())
            if len(contecttext)>0:
                if str(ctx.author) == "SentientPlatypus#1332":
                    await ctx.channel.send(random.choice(praiseresponsesentient))
                else:
                    await ctx.channel.send(random.choice(praiseresponse))
            else:
                pass	

            #shut up bot
            shutup = "^(shut\s(the\s[a-zA-Z]+\s)*up|be\squiet|fuck\s(this|you|your)|stfu)\s([a-zA-Z\*]+)*(bot|robot|scp|tsundere|trex(y|ycrocs)*|sen(tient)*(platypus)*|platypus)"
            shutupresponse = ["how about you shut up.", "No, u", "can you shut up? your opinion is worth as much as an old cucumber"]
            shutupre = re.findall(shutup,ctx.content.casefold())
            trexyscold = ["Im sorry  creator senpai. I wont do it again.", "sumimasen.", "Its your fault for making me that way! Baka!"]
            if len(shutupre)>0:
                if ctx.author.id==643764774362021899:
                    await ctx.channel.send(random.choice(trexyscold))
                else:
                    await ctx.channel.send(random.choice(shutupresponse))
            else:
                pass








        stats = levelling.find_one({"id" : ctx.author.id})
        if not ctx.author.bot:
            if stats is None:
                newuser = {"id" : ctx.author.id, "xp" :100}
                levelling.insert_one(newuser)
            else:
                xp = stats["xp"] + 5
                levelling.update_one({"id":ctx.author.id}, {"$set":{"xp":xp}})
                lvl = 0
                while True:
                    if xp < ((50*(lvl**2))+(50*(lvl))):
                        break
                    lvl+=1
                xp-=((50*((lvl-1)**2))+(50*(lvl-1)))
                if xp ==0:
                    embed = discord.Embed(title = "You have leveled up to level %s"%(lvl), description = "You have gained 3 `UpgradePoints` and `$%g`!"%(int(200*((1/2)*lvl))), color = discord.Color.green())
                    embed.set_thumbnail(url = ctx.author.avatar_url)
                    await ctx.channel.send(embed=embed)
                    money = mulah.find_one({"id":ctx.author.id}, {"money"})["money"]
                    money+=int(200*((1/2)*lvl))
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"money":money}})
                    point = [{"name":"UpgradePoint", "value":2000, "desc":"`^upgrade` one of your stats!"},]
                    Globals.AddToInventory(ctx.author, "UpgradePoint", point, 3)
                    


    @commands.command()
    async def swear(self,ctx, p1:discord.Member=None):
        if p1 is None:
            try:
                swearvar = levelling.find_one({"id":ctx.author.id},{"swears"})
                swearval = swearvar["swears"]
                id = ctx.guild
                for x in ctx.guild.members:
                    print(x)
                embed = discord.Embed(title = "You have sworn %s times."%(swearval), color = ctx.author.color)
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            except:
                await ctx.channel.send("You need to swear, motherfucker.")
        else:
            try:
                swearvar = levelling.find_one({"id":p1.id},{"swears"})
                swearval = swearvar["swears"]
                id = p1.guild
                for x in p1.guild.members:
                    print(x)
                embed = discord.Embed(title = "%s has sworn %s times."%(p1.display_name, swearval), color = ctx.author.color)
                embed.set_author(name = p1.display_name, icon_url=p1.avatar_url)
                await ctx.channel.send(embed=embed)
            except:
                await ctx.channel.send("they need to swear first, motherfucker.")            


    @commands.command()
    async def announce(self, ctx, title, message):
        if ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title = title, description = message, color = ctx.author.color)
            embed.set_author(name = "Announcement from %s"%(ctx.author.display_name), icon_url=ctx.author.avatar_url)
            embed.set_footer(text = datetime.now().strftime("%Y-%m-%d, %H:%M"))
            embed.set_thumbnail(url = ctx.author.avatar_url)
            channels = DiscordGuild.find_one({"id":ctx.guild.id}, {"announcement channels"})["announcement channels"]
            try:
                for x in channels:
                    x = self.client.get_channel(x)
                    await x.send(embed=embed)
            except:
                await ctx.channel.send("You need to add announcement channels with `^configuration announcement`")
        else:
            await ctx.channel.send("You dont have the permissions.")

    @commands.command()
    async def suggest(self, ctx, title, message):
        if ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title = title, description = message, color = ctx.author.color)
            embed.set_author(name = "Suggestion from %s"%(ctx.author.display_name), icon_url=ctx.author.avatar_url)
            embed.set_footer(text = datetime.now().strftime("%Y-%m-%d, %H:%M"))
            embed.set_thumbnail(url = ctx.author.avatar_url)
            channels = DiscordGuild.find_one({"id":ctx.guild.id}, {"suggestion channels"})["suggestion channels"]
            try:
                for x in channels:
                    x = self.client.get_channel(x)
                    await x.send(embed=embed)
            except:
                await ctx.channel.send("You need to add suggestion channels with `^configuration suggestion`")
        else:
            await ctx.channel.send("You dont have the permissions.")
    @commands.command()
    async def rank(self, ctx, p1:discord.Member=None):
        if not p1:
            p1=ctx.author
        stats = levelling.find_one({"id": p1.id})
        if stats is None:
            embed = discord.Embed(title = "You havnt sent any ctxs yet.")
            await ctx.channel.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50*(lvl**2))+(50*(lvl))):
                    break
                lvl+=1
            xp-=((50*((lvl-1)**2))+(50*(lvl-1)))
            boxes = int((xp/(200*((1/2)*lvl)))*20)     
            rankings = levelling.find().sort("xp",-1)
            for x in rankings:
                rank+=1
                if stats["id"] == x["id"]:
                    break
            embed = discord.Embed(title = "Level %g"%(Globals.GetLevel(p1.id)))
            embed.add_field(name = "Name", value = p1.mention, inline = True)
            embed.add_field(name = "xp", value =f"{xp}/{int(200*((1/2)*lvl))}", inline = True)   
            embed.add_field(name = "progress bar", value = boxes*":blue_square:" + (20-boxes) *":white_large_square:", inline = False)  
            embed.set_thumbnail(url = p1.avatar_url)    
            await ctx.channel.send(embed = embed)

    

    @commands.command()
    async def swearlb(self, ctx):
        ids = [x.id for x in ctx.guild.members]
        rankings = levelling.find().sort("swears",-1)
        count=0
        for x in levelling.find():
            print(x["xp"])
            count+=1
        print(count)
        i=1
        embed = discord.Embed(title = "Swear Leaderboard", color = ctx.author.color)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(int(x["id"])).display_name

                tempswears = x["swears"]
                embed.add_field(name = f"{i}: {temp}", value = f"Swears: {tempswears}", inline = False) 
                i+=1
                if i==11:
                    break
            except:
                pass
        await ctx.channel.send(embed=embed)


    @commands.group(invoke_without_command=True)
    async def summon(self,ctx):
        if str(ctx.author) == "SentientPlatypus#1332":
            await ctx.channel.send("summon someone, creator senpai.")
        else:
            await ctx.channel.send("begone!")
    @summon.group()
    async def jesus(self, ctx):
        if str(ctx.author) == "SentientPlatypus#1332":
            rankings = levelling.find().sort("swears",-1)
            for x in rankings:
                levelling.update_one({"id":x["id"]}, {"$set":{"swears":0}})
            await ctx.channel.send(embed=discord.Embed(title = "Creator senpai has summoned Jesus.", description = "Sin no more!", color = ctx.author.color))
        else:
            await ctx.channel.send("begone!")        

def setup(client):
    client.add_cog(levelsys(client))




