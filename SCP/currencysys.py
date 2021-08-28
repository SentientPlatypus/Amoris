
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
from discord.ext.commands.cooldowns import BucketType
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




gfnamelist = []
class currencysys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global emotionlist
        emotionlist = ["embarrassed", "horny","surprised","climax", "image", "bed", "angry", "fear", "sad", "dissapointed"]

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


        global worklists
        worklists = [
            {"name":"McDonalds worker", "salary":15, "req":1, "words":["bigmac", "burger", "broken"], "sentences":["sorry, the icecream machine is broken", "what can I get for you?", "welcome to mcdonalds"]},
            {"name":"Gamer", "salary":150, "req": 5, "words":["dorito", "mechanical", "virgin"], "sentences":["i hate lag", "hes one tap", "what a sweat"]},
            {"name":"Business Man", "salary":160, "req":20, "words":["business", "passive", "pigeon"], "sentences":["sorry thats not passive income", "it is ten times cheaper to keep a customer than to get a new one"]},
            {"name":"Jeff bezos", "salary":1000000000, "req":100, "words":["bigmac", "burger", "broken"]},
        ]

        global shopitems
        shopitems = [
            {"name":"phone", "value":800, "desc":"Text your Girlfriend!"},
            {"name": "netflixsub", "value": 29, "desc": "Netflix and chill with your gf"},
            {"name": "lotteryticket", "value": 2, "desc": "A chance to win 1 million dollars"},
            {"name": "movieticket", "value" : 16, "desc":"watch a movie with your gf"},
            {"name": "ring", "value" : 10000, "desc":"propose to your gf"},
        ]


        global pcitems
        pcitems = [
            {"name":"4gbRam", "type":"ram", "value": 20,"desc":"Use this for your PC!","power":0,"space":0, "rspace": 4000, "synthesis":0, "consumption":10},
            {"name":"8gbRam", "type":"ram", "value": 50, "desc":"Reasonable upgrade!","power":0,"space":0, "rspace": 8000, "synthesis":0, "consumption":10},
            {"name":"16gbRam", "type":"ram", "value": 100, "desc":"Do you really need this?","power":0,"space":0, "rspace": 16000, "synthesis":0, "consumption":10},
            {"name":"32gbRam", "type":"ram", "value": 200, "desc":"Thats overkill man, but you do you ig.","space":0,"power":0, "rspace": 32000, "synthesis":0, "consumption":10},
            {"name":"i5","type":"cpu", "value": 160, "desc":"A perfect cpu- if you are on a budget","space":0,"rspace":0, "power":1500 , "synthesis":0, "consumption":250},
            {"name":"i7","type":"cpu", "value": 250, "desc":"Great for upper middle range machines!","space":0, "power":2000,"rspace":0, "synthesis":0, "consumption":250 },
            {"name":"i9","type":"cpu", "value": 370, "desc":"A great gaming cpu overall.","space":0, "power":2500,"rspace":0, "synthesis":0, "consumption":250 },
            {"name":"threadripper","type":"cpu", "value": 3000, "desc":"An excellent cpu that will never know pain.","space":0, "power":4000,"rspace":0, "synthesis":0, "consumption":280 },
            {"name":"xeon","type":"cpu", "value": 10000, "desc":"For NASA computers", "power":10000,"space":0,"rspace":0, "synthesis":0, "consumption":350},
            {"name":"512SSD","type":"storage", "value": 70, "desc":"Great storage for a decent machine!","rspace":0,"power":0, "synthesis":0, "space": 512000, "consumption":10},
            {"name":"1TBSSD","type":"storage", "value": 100, "desc":"This should be enough for most people","rspace":0,"power":0, "synthesis":0, "space": 1000000, "consumption":10 },
            {"name":"4TBSSD","type":"storage", "value": 500, "desc":"enough storage for your homework folder","rspace":0,"power":0, "synthesis":0, "space": 4000000, "consumption":10 },
            {"name":"1660ti","type":"gpu", "value": 280, "desc":"entry level gpu","space":0, "power":1500,"rspace":0, "synthesis":0,"consumption":120  },
            {"name":"1080ti","type":"gpu", "value": 1074, "desc":"Good for mid range machines","space":0, "power":2000,"rspace":0, "synthesis":0, "consumption":250 },
            {"name":"2080ti","type":"gpu", "value": 1376, "desc":"imagine using a 20 series","space":0, "power":2500,"rspace":0, "synthesis":0, "consumption":275 },
            {"name":"3080ti","type":"gpu", "value": 3000, "desc":"Scalper price!", "space":0, "power":6000,"rspace":0, "synthesis":0, "consumption":350 },
            {"name":"650watt","type":"psu", "value": 5000, "desc":"scalper price!","space":0,"power":0, "synthesis":650,"rspace":0, "consumption":0  },
            {"name":"750watt","type":"psu", "value": 5000, "desc":"scalper price!","space":0,"power":0, "synthesis":750,"rspace":0, "consumption":0  },
            {"name":"850watt","type":"psu", "value": 5000, "desc":"scalper price!","space":0,"power":0, "synthesis":850,"rspace":0, "consumption":0  },
            {"name":"900watt","type":"psu", "value": 5000, "desc":"scalper price!","space":0,"power":0, "synthesis":900,"rspace":0, "consumption":0  },
            {"name":"motherboard","type":"board", "value": 100, "desc":"build a pc.","space":0,"power":0, "synthesis":0,"rspace":0, "consumption":0  }


        ]  
        global gameitems
        gameitems = [
            {"name":"Minecraft", "genre":["adventure", "creativity"],"space":1500, "value":26, "desc": "anything can run Minecraft!", "lpincrease":30, "recommendedspecs":{"totalram":8000, "power":1500}},
            {"name":"Fortnite", "genre":["fps"],"space":49000, "value":0, "desc": "How much lp were you expecting for fortnite?", "lpincrease":5, "recommendedspecs":{"totalram":8000, "power":2500}},
            {"name":"Valorant", "genre":["fps"],"space":14400, "value":0, "desc": "spend 80% of the game spectating.", "lpincrease":25, "recommendedspecs":{"totalram":8000, "power":3000}},
            {"name":"Terraria", "genre":["adventure", "creativity"],"space":100, "value":5, "desc": "A great friend of Mc", "lpincrease":20, "recommendedspecs":{"totalram":8000, "power":1500}},
            {"name":"Microsoft Flight simulator", "genre":["creativity"],"space":150000, "value":60, "desc": "You probably cant run this.", "lpincrease":40, "recommendedspecs":{"totalram":16000, "power":5000}},
            {"name":"Crysis 3", "genre":["adventure"],"space":17000, "value":5, "desc": "Your pc simply cant run this.", "lpincrease":50, "recommendedspecs":{"totalram":32000, "power":7800}},
            {"name":"League of Legends", "genre":["strategy"],"space":22000, "value":0, "desc": "Dont do it.", "lpincrease":-50, "recommendedspecs":{"totalram":8000, "power":2800}}
        ]
        global gamewords
        gamewords = [
            {"name": "Minecraft", "words":["block", "redstone", "blockhit", "endcrystal"]},
            {"name": "Fortnite", "words":["build", "ninja", "virgin", "clap"]},
            {"name": "Valorant", "words":["hipfire", "slow", "spectator", "Operator"]},
            {"name": "Terraria", "words":["Terraria", "cheap", "fun", "pewdiepie"]},
            {"name": "Microsoft Flight Simulator", "words":["plane", "aviation", "pilot", "graphics"]},
            {"name": "Crysis 3", "words":["Block", "redstone", "blockhit", "endcrystal"]},
            {"name": "League of Legends", "words":["virgin", "discordmod", "glasses", "asian"]},
        ]



    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def work(self, ctx):
        workk = mulah.find_one({"id" : ctx.author.id}, {"money"})
        job = mulah.find_one({"id":ctx.author.id}, {"job"})["job"]
        if job:
            hourlywage = next(x for x in worklists if x["name"]==job)["salary"]
        else:
            hourlywage=15

        if job:
            try:
                YourJob = next(x for x in worklists if x["name"]==job)
                workoption = random.choice(["unscramble", "guess"])
                right = False
                wrong = False
                if workoption == "guess":
                    def check(m):
                        return m.author==ctx.author and m.channel==ctx.channel

                    ListOfWords = random.choice(YourJob["sentences"]).split()
                    ListIndex = random.randint(0, len(ListOfWords))
                    word = ListOfWords[ListIndex]
                    answer = word
                    ListOfWords[ListIndex] = "-"*len(ListOfWords[ListIndex])
                    display = " ".join(ListOfWords)
                    embed = discord.Embed(title = "fill in the blank!", description = display, color = discord.Color.green())
                    embed.set_footer(text = "working as %s"%(job))
                    await ctx.channel.send(embed=embed)

                    msg = await self.client.wait_for('message', check=check, timeout=20)
                    if msg.content.lower()==word.lower():
                        right = True
                    else:
                        wrong = True
  

                if workoption == "unscramble":    
                    def check(m):
                        return m.author==ctx.author and m.channel==ctx.channel

                    randomword = random.choice(YourJob["words"])
                    answer = randomword
                    while "".join(list(randomword))==answer:
                        random.shuffle(list(randomword))
                    finalrandword = "".join(list(randomword))     
                    checks = []
                    for x in range(3):
                        embed = discord.Embed(title = "fill in the blank!", description = "You have %s chances! Unscramble the word `%s`"%(3-x, finalrandword), color = discord.Color.green())
                        embed.set_footer(text = "working as %s"%(job))

                        await ctx.channel.send(embed=embed)
                        nmsg = await self.client.wait_for('message', check = check, timeout = 30)
                        if nmsg.content == randomword.casefold():
                            skillint = 10-x*2
                            checks.append(nmsg.content)
                            break
                    if checks:
                        right = True
                    else:
                        wrong = True
                if right:
                    newmoney = workk["money"] + hourlywage
                    embed=discord.Embed(title = "Great work, %s!"%(ctx.author.display_name), description = "You did great. Here's $%g!"%(hourlywage), color = discord.Color.green())
                    embed.set_footer(text = "working as %s\nCurrent Balance:$%g"%(job, newmoney))
                    await ctx.channel.send(embed=embed)
                elif wrong:
                    hourlywage*=0.8
                    newmoney = workk["money"] + hourlywage
                    embed=discord.Embed(title = "Terrible job, %s!"%(ctx.author.display_name), description = "You need to do better. The answer was `%s`! Here's $%g!"%(answer,hourlywage), color = discord.Color.red())
                    embed.set_footer(text = "working as %s\nCurrent Balance:$%g"%(job, newmoney))
                    await ctx.channel.send(embed=embed)
            except TimeoutError:
                hourlywage*=0.6
                newmoney = workk["money"] + hourlywage
                embed=discord.Embed(title = "Terrible job, %s!"%(ctx.author.display_name), description = "You didnt even answer! The answer was `%s`! Here's $%g!"%(answer, hourlywage), color = discord.Color.red())
                embed.set_footer(text = "working as %s\nCurrent Balance:$%g"%(job, newmoney))
                await ctx.channel.send(embed=embed)  
        else:
            newmoney = workk["money"] + hourlywage
            mulah.update_one({"id":ctx.author.id},{"$set":{"money":newmoney}})
            embed = discord.Embed(title = "You have made %s dollars."%(hourlywage), description = "You now have $%g"%(newmoney),color = ctx.author.color)
            await ctx.channel.send(embed = embed)

        mulah.update_one({"id":ctx.author.id},{"$set":{"money":newmoney}})


    @commands.command()
    async def worklist(self, ctx):
        workk = mulah.find_one({"id" : ctx.author.id}, {"money"})["money"]
        job = mulah.find_one({"id":ctx.author.id}, {"job"})["job"]
        lvl = Globals.GetLevel(ctx)

        embed = discord.Embed(title = "Employment options!", description = 'join the workforce! use `^apply "<job>"` to apply!', color = discord.Color.blue())

        for x in worklists:
            if lvl>= x["req"]:
                check = "✅ "
            else:
                check = "❌ "
            embed.add_field(name = check + x["name"], value = "Salary:`%s`"%(x["salary"]), inline=False)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def apply(self, ctx, jobt):
        workk = mulah.find_one({"id" : ctx.author.id}, {"money"})["money"]
        job = mulah.find_one({"id":ctx.author.id}, {"job"})["job"]
        lvl = Globals.GetLevel(ctx)

        x = next(y for y in worklists if y["name"].lower()==jobt.lower())
        if lvl>=x["req"]:
            mulah.update_one({"id":ctx.author.id}, {"$set":{"job":x["name"]}})
            embed = discord.Embed(title = "You Got the Job!", description = "You are now working as %s!"%(x["name"]), color = discord.Color.green())
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title = "You were rejected!", description = "You dont have enough xp to work as a %s!"%(x["name"]), color = discord.Color.red())
            await ctx.channel.send(embed=embed)










        







    @commands.command()
    async def achievement(self,ctx, p1:discord.Member=None):
        if p1 ==None:
            p1=ctx.author
        global achievements
        embed = discord.Embed(title = "Achievements!", description = "use reactions to navigate achievements!", color = ctx.author.color)
        embed.set_image(url ="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/socialmedia/apple/271/trophy_1f3c6.png")
        reactions = ["💰","❤️","🎮", "🚪"]
        profilembed = await ctx.channel.send(embed=embed)
        for x in reactions:
            await profilembed.add_reaction(x)
        leave = False
        while leave ==False:
            global achievementcheck

            def check(reaction,user):
                return user == ctx.author and str(reaction.emoji) in reactions and reaction.message==profilembed
            confirm = await self.client.wait_for('reaction_add', check=check)
            if confirm:
                rawreaction = str(confirm[0])
                if rawreaction == "💰":
                    embed = discord.Embed(title = "%s's Financial Achievements"%(p1.display_name), value = "if only you could move out of your parents basement", color = p1.color)
                    for x in achievements:
                        if x["category"]=="finance":
                            embed.add_field(name = "%s| %s"%(x["name"],Globals.achievementcheck(p1,x["name"])), value = x["desc"], inline = False)

                if rawreaction == "❤️":
                    try:
                        gfval = mulah.find_one({"id":p1.id}, {"gf"})["gf"]
                        embed = discord.Embed(title = "%s's Relationship Achievements"%(p1.display_name), description = "If only %s was real."%(gfval["name"]), color = p1.color)
                    except:
                        embed = discord.Embed(title = "%s's Relationship Achievements"%(p1.display_name), description = "If only You had a gf", color = p1.color)
  
                    for x in achievements:
                        if x["category"]=="relationships":
                            embed.add_field(name = "%s| %s"%(x["name"],Globals.achievementcheck(p1,x["name"])), value = x["desc"], inline = False)                    
                if rawreaction == "🎮":
                    embed = discord.Embed(title = "%s's Gaming Achievements"%(p1.display_name), value = "Are you a true gamer?", color = p1.color)
                    for x in achievements:
                        if x["category"]=="gaming":
                            embed.add_field(name = "%s| %s"%(x["name"],Globals.achievementcheck(p1,x["name"])), value = x["desc"], inline = False)
                
                if rawreaction=="🚪":
                    embed = discord.Embed(title = "you have left!")
                    await profilembed.edit(embed=embed)
                    break

                await profilembed.edit(embed=embed)
                await profilembed.remove_reaction(emoji = rawreaction,member =ctx.author)   

    @commands.command()
    async def balance(self, ctx, namee:discord.Member=None):
        if namee is None:
            embed = discord.Embed(title = "%s current balance"%(ctx.author.display_name), color = ctx.author.color)
            walletval = mulah.find_one({"id":ctx.author.id},{"money"})
            if walletval is not None:
                try:
                    walletval = walletval["money"]
                    embed.add_field(name = "Wallet", value = "%s"%(walletval))
                except:
                    pass
            lovepoints = mulah.find_one({"id" : ctx.author.id}, {"lp"})
            if lovepoints is not None:
                try:
                    lovepoints = lovepoints["lp"]
                    embed.add_field(name = "Love points", value = "%s"%(lovepoints))
                except:
                    pass
            await ctx.send(embed = embed)       
        else:
            embed = discord.Embed(title = "%s current balance"%(namee.display_name), color = ctx.author.color)
            walletval = mulah.find_one({"id":namee.id},{"money"})
            if walletval is not None:
                try:
                    walletval = walletval["money"]
                    embed.add_field(name = "Wallet", value = "%s"%(walletval))
                except:
                    pass
            lovepoints = mulah.find_one({"id" : namee.id}, {"lp"})    
            if lovepoints is not None:
                try:
                    lovepoints = lovepoints["lp"]
                    embed.add_field(name = "Love points", value = "%s"%(lovepoints))
                except:
                    pass
            await ctx.send(embed = embed)           
    






            





      
        









    @commands.group(invoke_without_command = True)
    async def shop(self,ctx):
        embed = discord.Embed(title = "Main shop.", description = "use `^buy <item>` to buy something.`navigate with reactions`", color = ctx.author.color)
        global shopitems
        global pcitems
        global gameitems
        
        for x in range(len(shopitems)):
            nameee = shopitems[x]
            embed.add_field(name = "%s"%(nameee["name"]), value = "%s| %s"%(nameee["value"], nameee["desc"]), inline=False)
        shopmessage = await ctx.send(embed = embed)
        reactionlist = ["🎮", "🖥️", "🛒", "🚪"]
        for x in reactionlist:
            await shopmessage.add_reaction(x)
        def check(reaction,user):
            return user == ctx.author and str(reaction.emoji) in reactionlist and reaction.message == shopmessage
        exitshop = False
        totreactions = []
        while exitshop == False:
            confirm = await self.client.wait_for('reaction_add', check=check)
            if confirm:
                thereaction = str(confirm[0])

                if thereaction == "🎮":
                    embed = discord.Embed(title = "Game Shop!", description = "Buy games to play with your girlfriend!", color = ctx.author.color)
                    for x in gameitems:
                        finalstring = ""
                        for z in x.keys():
                            if not z == "name":
                                if not z=="value":
                                    extrastring = "%s: %s\n"%(z,x[z])
                                    finalstring+=extrastring
                        embed.add_field(name = "%s -$%s"%(x["name"], x["value"]), value = finalstring)
                    await shopmessage.edit(embed=embed)
                if thereaction == "🛒":
                    embed = discord.Embed(title = "Main shop", description = "use `^buy <item>` to buy something.`navigate with reactions`",color = ctx.author.color)
                    for x in range(len(shopitems)):
                        nameee = shopitems[x]
                        embed.add_field(name = "%s"%(nameee["name"]), value = "%s| %s"%(nameee["value"], nameee["desc"]), inline=False)
                    await shopmessage.edit(embed = embed)      
                if thereaction == "🖥️":
                    embed = discord.Embed(title = "PC SHOP!", description = "upgrade your PC. no one wants to see you play an AAA game on a chromebook", color=ctx.author.color)
                    for x in pcitems:
                        finalstring = ""
                        for z in x.keys():
                            if x[z]!=0:
                                extrastring = "%s: %s\n"%(z,x[z])
                                finalstring+=extrastring
                        embed.add_field(name = "%s - $%s"%(x["name"], x["value"]), value = finalstring)
                    await shopmessage.edit(embed = embed)    
                if thereaction == "🚪":
                    await shopmessage.edit(embed=discord.Embed(title = "You left the shop!"))   
                    break
                await shopmessage.clear_reactions()
                for x in reactionlist:
                    await shopmessage.add_reaction(x)















    @commands.group(invoke_without_command=True)
    async def pc(self, ctx):
        embed = discord.Embed(title = "Build a pc.", description = "herer are some commands. use `^pc` before each one", color = ctx.author.color)
        embed.add_field(name = "commands", value = "`add`, `remove`, `build`")
        await ctx.channel.send(embed = embed)

    @pc.command()
    async def build(self, ctx):
        try:
            global pcitems
            requirements = ["cpu", "psu", "ram", "board", "storage"]
            invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
            invdict = invar["inv"]
            parts =[]
            cpu =[]
            psu =[]
            ram =[]
            motherboard = []
            storage = []
            gpu = []
            for x in invdict:
                for z in pcitems:
                    if x["name"] == z["name"]:
                        parts.append({x["name"], z["type"]})
                        if z["type"] == "cpu":
                            cpu.append(x)
                        if z["type"] == "psu":
                            psu.append(x)
                        if z["type"] == "ram":
                            ram.append(x)
                        if z["type"] == "board":
                            motherboard.append(x)
                        if z["type"] == "storage":
                            storage.append(x)
                        if z["type"] == "gpu":
                            gpu.append(x)
                        try:
                            requirements.remove(z["type"])
                        except:
                            pass
                        break


            if not requirements:
                pcdict = {}
                partdict = {}
                await ctx.channel.send("Lets build your PC! What do you want to name your PC?")
                def check(m):
                    return m.author==ctx.author and m.channel == ctx.channel
                try:
                    msg = await self.client.wait_for('message', check = check, timeout = 20)
                    pcdict["name"] = msg.content
                    await ctx.channel.send("write a description for your PC!")
                    def check(m):
                        return m.author==ctx.author and m.channel == ctx.channel
                    try:
                        msg = await self.client.wait_for('message', check = check, timeout = 40)
                        pcdict["desc"] = msg.content
                        for x in range(6):
                            if x == 0:
                                var = cpu
                                stri = "cpu"
                            elif x ==1:
                                var = psu
                                stri ="psu"
                            elif x ==2:
                                var = ram
                                stri = "ram"
                            elif x ==3:
                                var = motherboard
                                stri = "board"
                            elif x ==4:
                                var = storage
                                stri = "storage"
                            elif x == 5:
                                if gpu:
                                    var = gpu
                                    stri = "gpu"
                                else:
                                    pass
                            reactiondict = {}
                            alphlist = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
                            var2 = []
                            count = 0
                            finalstring = ""
                            reactlist = []
                            for l in var:
                                var2.append(l["name"])
                                reactiondict[alphlist[count]] = l["name"]
                                finalstring+= "%s| %s\n"%(alphlist[count], l["name"])
                                reactlist.append(alphlist[count])
                                count+=1
                                


                            print(var)
                            embed = discord.Embed(title = "Choose your %s!"%(stri), description =finalstring, color = ctx.author.color)
                            if x == 0:
                                reactthis = await ctx.channel.send(embed =embed)
                            else:
                                await reactthis.edit(embed=embed)
                            for m in reactlist:
                                await reactthis.add_reaction(m)

                            def check2(reaction, user):
                                return user==ctx.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'] and reaction.message == reactthis                                
                            confirm = await self.client.wait_for('reaction_add', check = check2, timeout = 20)
                            if confirm:
                                print("this worked")
                                thisreaction = str(confirm[0])
                                partdict[stri] = reactiondict[thisreaction]
                                z = next(a for a in invdict if a["name"] == reactiondict[thisreaction])
                                z['amount']-=1
                                if z['amount']==0:
                                    invdict.remove(z)
                            await reactthis.clear_reactions()
                        totalpower = 0
                        for z in pcitems:
                            for x in partdict.keys():
                                if z["name"] == partdict[x]:
                                    totalpower+=z["consumption"]
                        psucreates = None
                        for x in pcitems:
                            if partdict["psu"] == x["name"]:
                                psucreates = x["synthesis"]


                        if psucreates>= totalpower:
                            partdict["totalram"] = 0
                            partdict["power"] = 0
                            partdict["space"] = 0
                            if not gpu:
                                for z in pcitems:
                                        if partdict["ram"] == z["name"]:
                                            partdict["totalram"]+=z["rspace"]
                                        elif partdict["cpu"] == z["name"]:
                                            partdict["power"] +=z["power"]
                                        elif partdict["storage"] == z["name"]:
                                            partdict["space"] += z["space"]    
                            else:                            
                                for z in pcitems:
                                        if partdict["ram"] == z["name"]:
                                            partdict["totalram"]+=z["rspace"]
                                        elif partdict["cpu"] == z["name"] or partdict["gpu"] == z["name"]:
                                            partdict["power"] +=z["power"]
                                        elif partdict["storage"] == z["name"]:
                                            partdict["space"] += z["space"]

                            partdict["ram2"] = None
                            partdict["ram3"] = None
                            partdict["ram4"] = None
                            pcdict["games"] = []
                                        
                            pcdict["parts"] = partdict
                            pcdict["amount"] = 1
                            newinv = invdict
                            newinv.append(pcdict)
                            mulah.update_one({"id":ctx.author.id}, {"$set":{"inv":newinv}})

                            embed = discord.Embed(title = "here is your pc!", color = ctx.author.color)
                            ramval = 0
                            for x in pcdict["parts"].keys():
                                    embed.add_field(name = "%s:"%(x), value = "%s"%(pcdict["parts"][x]))  
                            await ctx.channel.send(embed=embed)
                        else:
                            await ctx.channel.send("Your psu needs to be able to power all that, baka.")
                                
     
                    except:
                        print(traceback.format_exc())
                        await ctx.channel.send("you took too long")               
                except:
                    await ctx.channel.send("You took too long.")


                        
                        
                    
                    
            else:
                await ctx.channel.send("You dont have all the parts! you need %s"%(requirements))
        except:
            print(traceback.format_exc())
            await ctx.channel.send("You need to buy the parts")

    
    @commands.command()
    async def addram(self,ctx):
        global pcitems
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        findlist = []
        ramlist = []
        count = 0
        pcdict =  None
        for x in inval:
            if "parts" in x.keys():
                findlist.append(x)

        for x in inval:
            for z in pcitems:
                if x["name"] == z["name"]:
                    if z["type"] == "ram":
                        ramlist.append(x["name"])
        pcnamestring = ""
        pcname = []
        alphabet = string.ascii_lowercase
        alphlist = list(alphabet)
        countalph = 0
        for x in findlist:
            pcname.append(x["name"])
            pcnamestring+= "\n%s:%s"%(alphlist[countalph],x["name"])
            countalph+=1
        emptydict = {}
        for x in range(len(pcname)):
            emptydict[alphlist[x]] = pcname[x]
        print(emptydict)
            


        embed = discord.Embed(title = "Which PC would you like to upgrade?", description = pcnamestring, color = ctx.author.color)
        await ctx.channel.send(embed=embed)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        try:
            msg = await self.client.wait_for('message', check = check, timeout = 30)
            checklist =[]

            if emptydict[msg.content]in pcname:
                checklist.append(x)
                for x in inval:
                    if "parts" in x.keys():
                        findlist.append(x)
                        if x["name"] == emptydict[msg.content]:
                            pcdict = x
                            for z in x["parts"]:
                                if x["parts"][z] == None and len(re.findall("ram",z))>0:
                                    print(x["parts"][z])
                                    count+=1


                lettertoint = {"a":1, "b":2, "c":3, "d":4}
                embed = discord.Embed(title = "You have %g slots left."%(count), description = "How many slots would you like to fill?\n a|1\nb|2\nc|3", color = ctx.author.color)
                await ctx.channel.send(embed=embed)
                try:
                    msg = await self.client.wait_for('message', check = check, timeout=30)
                    if lettertoint[msg.content]<=count:


                        count1 = 0
                        for x in inval:
                            for z in pcitems:
                                if x["name"] == z["name"]:
                                    if z["type"] == "ram":
                                        count1+=1
                        if count1 >= lettertoint[msg.content]:
                            for x in range(lettertoint[msg.content]):
                                embed = discord.Embed(title = "Choose which ram you would like to use.", description = "%s"%("\n".join(ramlist)),color = ctx.author.color)
                                await ctx.channel.send(embed=embed)
                                try:
                                    msg = await self.client.wait_for('message', check=check,timeout=30)
                                    for x in ramlist:
                                        if msg.content == x.casefold():  #check if its in inv                                                
                                            inval.remove(pcdict)      #removes from temporary inventory dictionary so it can be updated.
                                            if pcdict["parts"]["ram"] is None:
                                                pcdict["parts"].update({"ram" : x})
                                            elif pcdict["parts"]["ram2"] is None:
                                                pcdict["parts"].update({"ram2" : x})
                                            elif pcdict["parts"]["ram3"] is None:
                                                pcdict["parts"].update({"ram3" : x})
                                            elif pcdict["parts"]["ram4"] is None:
                                                pcdict["parts"].update({"ram4" : x})
                                            
                                            for y in pcitems:
                                                if x == y["name"]:
                                                    pcdict["parts"]["totalram"]+=y["rspace"]
                                                    pcdict["parts"].update({"totalram":pcdict["parts"]["totalram"]})
                                                    inval.append(pcdict)
                                                    mulah.update_one({"id":ctx.author.id}, {"$set":{"inv":inval}})
                                            for item in inval:
                                                if item["name"] ==x:
                                                    item["amount"]-=1
                                                    if item["amount"]==0:
                                                        inval.remove(item)
                                            mulah.update_one({"id":ctx.author.id}, {"$set":{"inv":inval}})
                                except asyncio.TimeoutError:
                                    print(traceback.format_exc())
                                    await ctx.channel.send("you took too long.")
                        else:
                            await ctx.channel.send("You dont have that many ram sticks")
                    else:
                        await ctx.channel.send("You dont have that many vacant ram slots")
                except asyncio.TimeoutError:
                    await ctx.channel.send("You took too long.")       
            else:
                await ctx.channel.send("It has to be the letter")         
        except asyncio.TimeoutError:
            await ctx.channel.send("You took to long! Please dont waste my time.")

    @pc.command()
    async def stats(self,ctx):
        alphabet = string.ascii_lowercase
        alphlist = list(alphabet)
        emptydict = {}
        global pcitems

        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        pcdict = 0
        count =0
        pcnames = []
        stringpc = ""
        for x in inval:
            if "parts" in x.keys():
                pcdict = x
                pcnames.append(x["name"])
                emptydict[alphabet[count]] = x["name"]
                stringpc+= "%s:%s\n"%(alphlist[count], x["name"])
                count+=1
        embed = discord.Embed(title = "Which PC would you like to see the stats for?", description = stringpc, color = ctx.author.color)
        await ctx.channel.send(embed=embed)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            msg = await self.client.wait_for('message', check = check, timeout = 30)
            if emptydict[msg.content] in pcnames:
                for x in inval:
                    if "parts" in x.keys() and x["name"] == emptydict[msg.content]:
                        print(x)
                        embed =discord.Embed(title = "%s"%(x["name"]), description = x["desc"], color = ctx.author.color)
                        for z in x["parts"]:
                            embed.add_field(name = "%s"%(z), value = "%s"%(pcdict["parts"][z]))
                        for z in x.keys():
                            if z=="games":
                                embed.add_field(name = "%s"%(z), value = "%s"%x[z])
                        await ctx.channel.send(embed = embed)                  

        except asyncio.TimeoutError:
            print(traceback.format_exc())
            await ctx.channel.send("You took too long")
 



    @commands.command()
    async def use(self, ctx, item, number=None):

        global shopitems
        if number == None:
            number = 1
        else:
            number = int(number)
        inval = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
        itemdict = next((x for x in inval if x["name"].lower()==item.lower()), None)
        money = mulah.find_one({"id":ctx.author.id}, {"money"})["money"]
        if itemdict is not None:
            if item.lower() == "lotteryticket":
                gambleval = Globals.gamble(10000, number)
                if gambleval>=1:
                    money+=1000000*gambleval
                    embed = discord.Embed(title = "CONGRATULATIONS %s!!!"%(ctx.author.display_name), description = "You won the lottery!!!!", color = ctx.author.color)
                    embed.add_field(name = "You won $%s"%(1000000*gambleval), value = "you now own $%s"%(money))
                else:
                    embed = discord.Embed(title = "Sorry! %s!!!"%(ctx.author.display_name), description = "You didnt win the lottery!", color = ctx.author.color)
                    embed.add_field(name = "What were you expecting?", value = "dont let this ruin you.")
                    
                gambles = mulah.find_one({"id":ctx.author.id}, {"gambles"})["gambles"]
                gambles+=1
                mulah.update_one({"id":ctx.author.id}, {"$set":{"gambles":gambles}})
                await ctx.channel.send(embed=embed)
            

            Globals.RemoveFromInventory(ctx.author, item, number)
        else:
            await ctx.channel.send("That item is not in your inventory!")

    @pc.command()
    async def install(self, ctx):
        global pcitems
        global gameitems
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        pcnames = []
        emptydict = {}
        pcdict = 0
        ownedgames = []
        alphabet = string.ascii_lowercase
        alphlist = list(alphabet)
        finalstring = ""
        count = 0
        for x in inval:
            if "parts" in x.keys():
                pcnames.append(x["name"])
                finalstring+= "%s:%s\n"%(alphlist[count], x["name"])
                emptydict[alphlist[count]] = x["name"]
                count+=1
        embed = discord.Embed(title = "Which pc would you like to install on?", description = finalstring, color = ctx.author.color)
        await ctx.channel.send(embed=embed)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        try:
            msg = await self.client.wait_for('message', check = check, timeout=30)
            if emptydict[msg.content] in pcnames:
                for x in inval:
                    if "parts" in x.keys() and x["name"] == emptydict[msg.content]:
                        pcdict = x

                finalstring = ""
                finaldict = {}
                finalcount = 0
                gameslist = []
                for x in inval:
                    for z in gameitems:
                        if x["name"] == z["name"]:
                            finalstring+="%s:%s, space:%s\n"%(alphlist[finalcount], x["name"], z["space"])  
                            finaldict[alphlist[finalcount]] = x["name"]
                            gameslist.append(x["name"])
                            finalcount+=1
                embed = discord.Embed(title = "Which game would you like to install?", description = finalstring, color = ctx.author.color)
                await ctx.channel.send(embed=embed)
                try:
                    msg = await self.client.wait_for('message', check = check, timeout = 30)
                    if finaldict[msg.content] in gameslist:
                        inval.remove(pcdict)
                        pcdict["games"].append(finaldict[msg.content])
                        for x in gameitems:
                            if x["name"] == finaldict[msg.content]:
                                pcdict["parts"]["space"]-=x["space"]
                                break
                        for x in inval:
                            if x["name"] == finaldict[msg.content]:
                                x["amount"]-=1
                                if x["amount"] == 0:
                                    inval.remove(x)
                        inval.append(pcdict)
                        mulah.update_one({"id":ctx.author.id}, {"$set":{"inv":inval}})


                        









                except asyncio.TimeoutError:
                    await ctx.channel.send("You took to long! do the command again!")
                            


        except asyncio.TimeoutError:
            await ctx.channel.send("You took too long!")
        
        
        
        
        
        
        







    @pc.command()
    async def dismantle(self, ctx):
        global pcitems
        global gameitems
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        pcnames = []
        emptydict = {}
        pcdict = 0
        ownedgames = []
        alphabet = string.ascii_lowercase
        alphlist = list(alphabet)
        finalstring = ""
        count = 0
        for x in inval:
            if "parts" in x.keys():
                pcnames.append(x["name"])
                finalstring+= "%s:%s\n"%(alphlist[count], x["name"])
                emptydict[alphlist[count]] = x["name"]
                count+=1
        embed = discord.Embed(title = "Which PC would you like to dismantle?", description = finalstring, color = ctx.author.color)
        await ctx.channel.send(embed=embed)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        try:
            msg = await self.client.wait_for('message', check = check, timeout = 30)
            if emptydict[msg.content] in pcnames:
                pcdict = next(item for item in inval if "parts" in item.keys() and item["name"] == emptydict[msg.content])
                print(pcdict)
                for x in pcdict["parts"].keys():
                    invaldict = next((item for item in inval if item["name"] == pcdict["parts"][x]), None)
                    pcitemdict = next((item for item in pcitems if item["name"] == pcdict["parts"][x]), None)
                    print(pcitemdict)           
                    print(x)  
                    print(pcdict["parts"][x])    
                    if invaldict is not None:
                        invaldict["amount"]+=1
                    else:   
                        try:
                            inval.append({"name":pcdict["parts"][x], "amount": 1, "desc":pcitemdict["desc"]})
                        except:
                            pass
                for x in pcdict["games"]:
                    invaldict = next((item for item in inval if item["name"] == pcdict["games"][x]), None)
                    gamedict = next((item for item in gameitems if item["name"] == pcdict["games"][x]), None)
                    if invaldict is not None:
                        invaldict["amount"]+=1
                    else:
                        inval.append({"name":pcdict["games"][x], "amount": 1, "desc":gamedict["desc"]})   

                inval.remove(pcdict)
                mulah.update_one({"id":ctx.author.id},{"$set":{"inv":inval}})
                embed = discord.Embed(title = "I have dismantled %s."%(emptydict[msg.content]), description = "All parts have been returned to your inventory.",color = ctx.author.color)
                await ctx.channel.send(embed=embed)

                
        except asyncio.TimeoutError:
            await ctx.channel.send("You took to long! i guess we arent doing this.")



    @pc.command()
    async def play(self, ctx):
        global gameitems
        global gamewords
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        pcnames = []
        emptydict = {}
        pcdict = 0
        ownedgames = []
        alphabet = string.ascii_lowercase
        alphlist = list(alphabet)
        finalstring = ""
        count = 0
        for x in inval:
            if "parts" in x.keys():
                pcnames.append(x["name"])
                finalstring+= "%s:%s\n"%(alphlist[count], x["name"])
                emptydict[alphlist[count]] = x["name"]
                count+=1
        print(emptydict)
        print(pcnames)
        embed = discord.Embed(title = "Which PC would you like to use?", description = finalstring, color = ctx.author.color)
        await ctx.channel.send(embed=embed)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        try:
            msg = await self.client.wait_for('message', check = check, timeout = 30)
            if emptydict[msg.content] in pcnames:
                gamelist = []
                newdict = {}
                count = 0
                finalstring = ""
                for x in inval:
                    if "parts" in x.keys() and x["name"] == emptydict[msg.content]:
                        pcdict = x
                        for z in gamewords:
                            for y in x["games"]:
                                if y == z["name"]:
                                    gamelist.append(y)
                                    finalstring+="%s:%s\n"%(alphlist[count], y)
                                    newdict[alphlist[count]] = y
                                    count+=1
                if gamelist:
                    embed = discord.Embed(title = "which game would you like to play?", description = finalstring, color = ctx.author.color)
                    await ctx.channel.send(embed=embed)
                    try:
                        msg = await self.client.wait_for('message', check = check, timeout = 30)
                        if newdict[msg.content] in gamelist:
                            specscheck = []
                            for x in gameitems:
                                if x["name"] == newdict[msg.content]:
                                    if x["recommendedspecs"]["totalram"]>pcdict["parts"]["totalram"] or x["recommendedspecs"]["power"]>pcdict["parts"]["power"]:
                                        specscheck.append("nope")
                            if not specscheck:
                                print(newdict[msg.content])
                                for x in gamewords:
                                    if x["name"] == newdict[msg.content]:
                                        randomword = random.choice(x["words"])
                                        randomwordlist = list(randomword)
                                        random.shuffle(randomwordlist)
                                        finalrandword = "".join(randomwordlist)
                                        break
                                checks = []
                                for x in range(3):
                                    await ctx.channel.send("You have %s chances! Unscramble the word `%s`"%(3-x, finalrandword))
                                    try:
                                        nmsg = await self.client.wait_for('message', check = check, timeout = 30)
                                        if nmsg.content == randomword.casefold():
                                            skillint = 10-x*2
                                            checks.append(nmsg.content)
                                            break
                                    except asyncio.TimeoutError:
                                        await ctx.channel.send("You took too long! Try the whole command over again.")
                                if checks:
                                    embed = discord.Embed(title = "You Played %s"%(newdict[msg.content]), description = "You gained %g skill points for %s!"%(skillint, newdict[msg.content]), color = ctx.author.color)
                                    
                                    await ctx.channel.send(embed=embed)
                                else:
                                    skillint = 4
                                    await ctx.channel.send("the word was %s!!"%(randomword))
                                    embed = discord.Embed(title = "You Played %s"%(newdict[msg.content]), description = "You gained only %g skill points for %s! You should be glad I didnt give you 0."%(skillint, newdict[msg.content]), color = ctx.author.color)
                                    await ctx.channel.send(embed=embed)
                                gameskill = mulah.find_one({"id":ctx.author.id}, {"gameskill"})
                                try:
                                    skilldict = gameskill["gameskill"]
                                    try:
                                        skilldict[newdict[msg.content]] +=skillint
                                    except:
                                        print(traceback.format_exc())
                                        skilldict[newdict[msg.content]] = 0
                                        skilldict[newdict[msg.content]]+=skillint
                                except:
                                    print(traceback.format_exc())
                                    skilldict = {}
                                    skilldict[newdict[msg.content]] =0
                                    skilldict[newdict[msg.content]] +=skillint

                                mulah.update_one({"id":ctx.author.id}, {"$set":{"gameskill":skilldict}})
                            else:
                                await ctx.channel.send("Your PC does not meet the requirements. You should look at system requirements before installing a game!")
                                
                        else:
                            await ctx.channel.send("You were supposed to type a letter, Baka.")


                            


                            ##code
                    except asyncio.TimeoutError:
                        await ctx.channel.send("You took too long! i guess we arent doing this.")
                else:
                    await ctx.channel.send("You dont have any games on this PC.")
            else:
                await ctx.channel.send("Use the lowercase letter associated with the game name.")

        


        except asyncio.TimeoutError:
            await ctx.channel.send("You took to long! i guess we arent doing this.")


    @commands.command()
    async def give(self, ctx, itemtogive, number:int, p1:discord.Member):
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        p1invar = mulah.find_one({"id":p1.id}, {"inv"})
        p1inval = p1invar["inv"]
        itemcheck = []
        for x in inval:
            if x["name"].casefold() ==itemtogive: 
                for z in p1inval:
                    if ("name", x["name"]) in z.items():
                        if x["amount"]>=number:
                            z["amount"]+=number
                            itemcheck.append("yes")
                            
                            x["amount"]-=number
                            if x["amount"] == 0:
                                inval.remove(x)
                        else:
                            await ctx.channel.send("You do not have that many items in your inventory!")
                            return
                        

        if not itemcheck:
            for x in inval:
                if x["name"].casefold()==itemtogive.lower():
                    if x["amount"]>=number:
                        x["amount"]-=number
                        if x["amount"] == 0:
                            inval.remove(x)
                        pdict = x
                        pdict["amount"] = number
                        p1inval.append(pdict)
                    else:
                        await ctx.channel.send("You do not have that many items in your inventory!")
                        return
                

        mulah.update_one({"id":p1.id}, {"$set":{"inv":p1inval}})
        mulah.update_one({"id":ctx.author.id}, {"$set":{"inv":inval}})
        embed = discord.Embed(title = "You have given %s %s %s"%(p1.display_name,number, itemtogive), color = ctx.author.color)
        await ctx.channel.send(embed=embed)


        
        

            



    @commands.command()
    async def gamestats(self,ctx):
        try:
            gamvar = mulah.find_one({"id":ctx.author.id}, {"gameskill"})
            gameval = gamvar["gameskill"]
            embed = discord.Embed(title = "Your game stats", color = ctx.author.color)
            for x in gameval.keys():
                embed.add_field(name = "%s"%(x), value = "Skill:%s"%(gameval[x]))
            await ctx.channel.send(embed = embed)

        except:
            print(traceback.format_exc())
            await ctx.channel.send("You dont have any stats!")

























        




    @commands.command()
    async def buy(self,ctx, item:str, number:int=None):
        global shopitems
        global pcitems     
        global gameitems
        if number is None:
            number = 1   
        allitems = pcitems+shopitems+gameitems
        xvalue = []
        AllItems = pcitems+shopitems+gameitems
        for x in AllItems:
            if item.lower() == x["name"].casefold():
                xvalue.append(x)
                itemvalue = x["value"]
                itemdesc = x["desc"]
                walletvar = mulah.find_one({"id":ctx.author.id}, {"money"})
                walletval = walletvar["money"]
                print(walletval, walletvar)
                if itemvalue<=walletval*number:
                    Globals.AddToInventory(ctx.author, item=item, ReferenceList=AllItems, AmountToAdd=number)    
                    embed=discord.Embed(title = "Purchase successfull!", description = "You have purchased %s %s!"%(number, item), color = ctx.author.color)
                    await ctx.channel.send(embed=embed)
                else:
                    await ctx.channel.send("you dont have enough money for that.")
                    break
            else:
                pass
        if len(xvalue) ==0:
            await ctx.channel.send("That item isnt in the shop.")
            xvalue.clear()
        else:
            pass
            xvalue.clear()
    

    @commands.command()
    async def inv(self,ctx, p1:discord.Member=None):
        embed = discord.Embed(title = "inventory", color = ctx.author.color)
        invariable = mulah.find_one({"id": ctx.author.id}, {"inv"})
        invariable = invariable["inv"]
        if p1 is None:
            embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
            print(invariable)
            for entry in invariable:
                embed.add_field(name = "%s  (%s)"%(entry["name"], entry["amount"]), value = "%s"%(entry["desc"]), inline = False)
        elif p1 is not None:
            embed.set_author(name = p1.display_name, icon_url=p1.avatar_url)
            invar = mulah.find_one({"id":p1.id}, {"inv"})
            inval = invar["inv"]
            for entry in inval:
                embed.add_field(name = "%s  (%s)"%(entry["name"], entry["amount"]), value = "%s"%(entry["desc"]), inline = False)
        await ctx.channel.send(embed = embed)

            
    @commands.command()
    async def clearinv(self,ctx,p1:discord.Member=None):
        if str(ctx.author) == "SentientPlatypus#1332":
            if p1 is None:
                invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
                inval = invar["inv"]
                inval.clear()
                mulah.update_one({"id":ctx.author.id}, {"$set":{"inv":inval}})
                await ctx.channel.send("I have cleared your inventory, creator senpai!")
            else:
                invar = mulah.find_one({"id":p1.id}, {"inv"})
                inval = invar["inv"]
                inval.clear()
                mulah.update_one({"id":p1.id}, {"$set":{"inv":inval}})
                await ctx.channel.send("I have cleared %s's inventory, creator senpai!"%(p1.display_name))    
        else:
            await ctx.channel.send("Only creator senpai can do that!")            



    
    @commands.command()
    async def getmoney(self,ctx,num:int, name:discord.Member=None):
        if str(ctx.author) == "SentientPlatypus#1332":
            if name is None:
                walletvar = mulah.find_one({"id":ctx.author.id}, {"money"})
                walletval = walletvar["money"] + num
                mulah.update_one({"id":ctx.author.id}, {"$set":{"money":walletval}})
                string = "Ok creator senpai!!! I added $%s to your wallet!"%(num)
                await ctx.channel.send(string)
            else:
                walletvar = mulah.find_one({"id":name.id}, {"money"})
                walletval = walletvar["money"] + num
                mulah.update_one({"id":name.id}, {"$set":{"money":walletval}})
                string = "Ok creator senpai!!! I added $%s to %s's wallet!"%(num, name.display_name)
                await ctx.channel.send(string)                
        else:
            await ctx.channel.send("You dont have the rights to this command.")
    
    @commands.command()
    async def getlp(self,ctx,num:int, name:discord.Member=None):
        if str(ctx.author) == "SentientPlatypus#1332":
            if name is None:
                lpvar = mulah.find_one({"id":ctx.author.id}, {"lp"})
                lpval = lpvar["lp"] + num
                mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":lpval}})
                string = "Ok creator senpai!!! I added %s love points to your relationship!"%(num)
                await ctx.channel.send(string)
            else:
                lpvar = mulah.find_one({"id":name.id}, {"lp"})
                lpval = lpvar["lp"] + num
                mulah.update_one({"id":name.id}, {"$set":{"lp":lpval}})
                string = "Ok creator senpai!!! I added %s love points to %s's relationship!"%(num, name.display_name)
                await ctx.channel.send(string)                
        else:
            await ctx.channel.send("You dont have the rights to this command.")
    
    @commands.command()
    async def profile(self,ctx,p1:discord.Member=None):
        if p1 == None:
            p1 = ctx.author
        print(mulah.find_one({"id":p1.id}))
        breakupval = mulah.find_one({"id":p1.id}, {"breakups"})["breakups"]
        kissval = mulah.find_one({"id":p1.id}, {"kisses"})["kisses"]
        boinkval = mulah.find_one({"id":p1.id}, {"boinks"})["boinks"]
        proposeval = mulah.find_one({"id":p1.id}, {"proposes"})["proposes"]
        relationships = mulah.find_one({"id":p1.id}, {"relationships"})["relationships"]
        dates = mulah.find_one({"id":p1.id}, {"dates"})["dates"]
        gambles = mulah.find_one({"id":p1.id}, {"gambles"})["gambles"]
        gamblewins = mulah.find_one({"id":p1.id}, {"gamblewins"})["gamblewins"]
        mmorpg = mulah.find_one({"id":p1.id}, {"mmorpg"})["mmorpg"]
        job = mulah.find_one({"id":p1.id}, {"job"})["job"]
        embed = discord.Embed(title = "%s' Profile!"%(p1.display_name), description = "Use the reactions to navigate the profile!", color = ctx.author.color)
        embed.set_image(url = p1.avatar_url)
        reactions = ["💰","❤️","🎮", "🏆","💼", "⚔️","🚪"]
        profilembed = await ctx.channel.send(embed=embed)
        for x in reactions:
            await profilembed.add_reaction(x)
        leave = False
        while leave ==False:
            def check(reaction,user):
                return user==ctx.author and str(reaction.emoji) in reactions and reaction.message==profilembed
            confirm = await self.client.wait_for('reaction_add', check=check)
            if confirm:
                rawreaction = str(confirm[0])
                if rawreaction =="⚔️":
                    embed = discord.Embed(title = "MMORPG stats!", color = ctx.author.color)
                    for x in mmorpg.keys():
                        if x == "loadout":
                            finalstring=""
                            for x in mmorpg["loadout"].keys():
                                finalstring+="%s: %s\n"%(x, mmorpg["loadout"][x])
                            embed.add_field(name = "Loadout:", value = finalstring, inline=False)
                        else:
                            embed.add_field(name = "%s"%(x), value = "%s"%(mmorpg[x]), inline = False)

                if rawreaction == "💰":
                    try:
                        walletval = mulah.find_one({"id":p1.id}, {"money"})["money"]
                        embed = discord.Embed(title = "%s's Financial stability!"%(p1.display_name), color = ctx.author.color)
                        embed.set_image(url = p1.avatar_url)
                        embed.add_field(name="Job:", value = job)
                        embed.add_field(name ="Current balance:", value = "$%s"%(walletval))
                        embed.add_field(name = "Total gambles:", value = gambles)
                        embed.add_field(name = "Total successful gambles:", value = gamblewins)
                        try:
                            embed.add_field(name = "gambling winrate:", value = "%%%g"%((gamblewins/gambles)*100))
                        except:
                            pass
                    except:
                        print(traceback.format_exc())
                        embed = discord.Embed(title = "This man hasnt worked a single day in his life.", color = ctx.author.color)
                if rawreaction == "❤️":
                    try:
                        gfvar = mulah.find_one({"id":p1.id}, {"gf"})
                        gfval = gfvar["gf"]

                        try:
                            lpvar = mulah.find_one({"id": p1.id}, {"lp"})
                            lpval = math.floor(lpvar["lp"])

                            embed = discord.Embed(title = "%s's stats!"%(gfval["name"]), description = "if only she was real.", color = p1.color)
                            for x in gfval.keys():
                                if x not in emotionlist:
                                    embed.add_field(name = "%s"%(x), value = gfval[x])


                            embed.add_field(name = "❤️Love Points", value = "%s"%(lpval))
                            try:
                                print(gfval["image"])
                                if gfval["image"].startswith("http"):
                                    print("yes, it starts with http")
                                    embed.set_image(url = gfval["image"])
                            except:
                                print(traceback.format_exc())
                                    
                        except:
                            print(traceback.format_exc())
                            embed = discord.Embed(title = "get a gf", color = ctx.author.color)
                            
                    except:
                        embed = discord.Embed(title = "Single af. rip.", color = ctx.author.color) 
                    embed.add_field(name = "%s's total boinks "%(p1.display_name), value = boinkval, inline=False)
                    embed.add_field(name = "%s's total kisses "%(p1.display_name),value = kissval, inline=False)
                    embed.add_field(name = "%s's total breakups "%(p1.display_name), value = breakupval, inline=False)          
                    embed.add_field(name = "%s's total proposes "%(p1.display_name), value = proposeval, inline=False)  
                    embed.add_field(name = "%s's total dates "%(p1.display_name), value = dates, inline=False)            
                    embed.add_field(name = "%s's total relationships"%(p1.display_name), value = relationships, inline=False)                   
                if rawreaction == "🎮":
                    try:
                        gamvar = mulah.find_one({"id":p1.id}, {"gameskill"})
                        gameval = gamvar["gameskill"]
                        embed = discord.Embed(title = "Your game stats", color = ctx.author.color)
                        for x in gameval.keys():
                            embed.add_field(name = "%s"%(x), value = "Skill:%s"%(gameval[x]))


                    except:
                        print(traceback.format_exc())
                        embed = discord.Embed(title = "You dont have any stats!", color = ctx.author.color)    
                if rawreaction == "🏆": 
                    global achievements
                    try:
                        achievementval = mulah.find_one({"id":p1.id}, {"achievements"})["achievements"]
                        embed = discord.Embed(title = "%s's achievements!"%(p1.display_name), description = "use ^achievements for a more detailed view!", color = ctx.author.color)
                        for y in achievementval:
                            achievementdict = next(x for x in achievements if x["name"] ==y)
                            embed.add_field(name = y+" "+Globals.achievementcheck(p1,y), value = achievementdict["desc"], inline = False)


                    except:
                        mulah.update_one({"id":p1.id}, {"$set":{"achievements":[]}})     
                        embed = discord.Embed(title = "He has no achievements. Rip", color = ctx.author.color)
                if rawreaction=="🚪":
                    embed = discord.Embed(title = "You have left the profile!", color =ctx.author.color)
                    await profilembed.edit(embed=embed)
                    leave = True
                
                if rawreaction=="💼":
                    embed = discord.Embed(title = "%s's inventory"%(p1.display_name), color = ctx.author.color)
                    invariable = mulah.find_one({"id": ctx.author.id}, {"inv"})
                    invariable = invariable["inv"]
                    embed.set_author(name = p1.display_name, icon_url=p1.avatar_url)
                    invar = mulah.find_one({"id":p1.id}, {"inv"})
                    inval = invar["inv"]
                    for entry in inval:
                        embed.add_field(name = "%s  (%s)"%(entry["name"], entry["amount"]), value = "%s"%(entry["desc"]), inline = False)

                await profilembed.edit(embed=embed)
                await profilembed.remove_reaction(emoji = rawreaction,member =ctx.author)                    


    




    @commands.group(invoke_without_command=True)
    async def watchlist(self, ctx):
        leavewatchlist = False
        while leavewatchlist == False:
            try:
                await message.clear_reactions()
            except:
                pass
            try:
                moviesDB = IMDb()
                embed = discord.Embed(title = "Welcome to the watchlist!", description = "You can add a movie to your watchlist, or just look at its details!", color = ctx.author.color)
                try:
                    watchvar = mulah.find_one({"id":ctx.author.id},{"watchlist"})
                    watchval = watchvar["watchlist"]           
                    print(watchval)     
                    embed.add_field(name = "current watchlist:", value = "entries by title:\n"+"\n".join(watchval))
                except:
                    print(traceback.format_exc())
                    pass
                
                message = await ctx.channel.send(embed=embed)
                await message.add_reaction("❓")
                await message.add_reaction("➕")
                await message.add_reaction("➖")
                await message.add_reaction("🚪")
                def check4(reaction,user):
                    return user==ctx.author and str(reaction.emoji) in ["➕","❓","➖", "🚪"] and reaction.message == message                

                
                def check(m):
                    return m.author ==ctx.author and m.channel ==ctx.channel
                confirmation2 = await self.client.wait_for('reaction_add',check=check4)
                if confirmation2: 
                    try:
                        await message.clear_reactions()
                    except:
                        pass
                    print(confirmation2)
                    print("this")
                    print(str(confirmation2[0]))
                    print("before")
                    if str(confirmation2[0]) == "➕":
                        await message.edit(embed=discord.Embed(title = "Search for a movie/show to add!", color = ctx.author.color))
                        try:
                            msg = await self.client.wait_for('message', check = check, timeout = 120)
                            movies  = moviesDB.search_movie(msg.content)
                            movieID = movies[0].getID()
                            movie = moviesDB.get_movie(movieID)

                            
                            yt = YoutubeSearch(str(movie)+" trailer", max_results=1).to_json()
                            yt_id = str(json.loads(yt)['videos'][0]['id'])
                            yt_url = 'https://www.youtube.com/watch?v='+yt_id
                            newyt = YoutubeSearch(str(movie)+" trailer", max_results=1).to_json()
                            newytid = str(json.loads(newyt)['videos'][0]['id'])
                            thumnail_url = "https://img.youtube.com/vi/%s/maxresdefault.jpg"%(newytid)
                            try:
                                embed = discord.Embed(title = "%s, (%s)"%(movie, movie["year"]),url = yt_url,description = " Genre:%s"%(movie["genres"]), color = ctx.author.color)
                            except:
                                embed = discord.Embed(title = "%s"%(movie),url = yt_url,description = " Genre:%s"%(movie["genres"]), color = ctx.author.color)
                            try:
                                embed.add_field(name = "Synopsis:", value = "%s"%(str(moviesDB.get_movie_synopsis(movieID)["data"]["plot"][0])))
                            except:
                                pass
                            embed.set_image(url = thumnail_url)
                            embed.add_field(name = "Trailer", value = yt_url, inline=False)

                            listofdirectories = ["rating"]
                            for x in listofdirectories:
                                try:
                                    embed.add_field(name = x, value = "%s"%(movie[x]))
                                except:
                                    pass

                            try:
                                embed.add_field(name= "Episodes:", value = "%s"%(moviesDB.get_movie_episodes(movieID)["data"]["number of episodes"]))
                            except:
                                pass
                            try:
                                watchvar = mulah.find_one({"id":ctx.author.id},{"watchlist"})
                                watchval = watchvar["watchlist"]
                                if str(movie) not in watchval:
                                    embed.set_footer(text = "React with ✅ to add to your watchlist")

                                    await message.edit(embed=embed)
                                    await message.add_reaction("✅")
                                    def check2(reaction, user):
                                        return user == ctx.author and str(reaction.emoji) in ["✅"] and reaction.message == message
                                    confirmation = await self.client.wait_for("reaction_add", check=check2) 
                                    if confirmation:
                                        await message.edit(embed= discord.Embed(title = "You have added %s to your watchlist!"%(movie), color = ctx.author.color))
                                        try:
                                            watchvar = mulah.find_one({"id":ctx.author.id},{"watchlist"})
                                            watchval = watchvar["watchlist"]
                                            watchval.append(str(movie))
                                            mulah.update_one({"id":ctx.author.id},{"$set":{"watchlist":watchval}})
                                        except:
                                            mulah.update_one({"id":ctx.author.id},{"$set":{"watchlist":[str(movie)]}})
                                else:
                                    embed.set_footer(text="This movie is already in your watchlist!")
                                    await message.edit(embed=embed)
                            except:
                                embed.set_footer(text = "React with ✅ to add to your watchlist")

                                await message.edit(embed=embed)
                                await message.add_reaction("✅")
                                def check2(reaction, user):
                                    return user == ctx.author and str(reaction.emoji) in ["✅"] and reaction.message == message
                                confirmation = await self.client.wait_for("reaction_add", check=check2) 
                                if confirmation:
                                    await message.edit(embed= discord.Embed(title = "You have added %s to your watchlist!"%(movie), color = ctx.author.color))
                                    try:
                                        watchvar = mulah.find_one({"id":ctx.author.id},{"watchlist"})
                                        watchval = watchvar["watchlist"]
                                        watchval.append(str(movie))
                                        mulah.update_one({"id":ctx.author.id},{"$set":{"watchlist":watchval}})
                                    except:
                                        mulah.update_one({"id":ctx.author.id},{"$set":{"watchlist":[str(movie)]}})                        


                        except:
                            print(traceback.format_exc())
                            await message.edit("I couldnt find anything. Im sorry.")
                    if str(confirmation2[0])=="❓":
                        await message.edit(embed=discord.Embed(title = "type the movie you want to find information on!", color = ctx.author.color))
                        try:
                            msg = await self.client.wait_for('message', check = check, timeout = 120)
                            movies  = moviesDB.search_movie(msg.content)
                            movieID = movies[0].getID()
                            movie = moviesDB.get_movie(movieID)

                            
                            yt = YoutubeSearch(str(movie)+" trailer", max_results=1).to_json()
                            yt_id = str(json.loads(yt)['videos'][0]['id'])
                            yt_url = 'https://www.youtube.com/watch?v='+yt_id
                            newyt = YoutubeSearch(str(movie)+" opening", max_results=1).to_json()
                            newytid = str(json.loads(newyt)['videos'][0]['id'])
                            thumnail_url = "https://img.youtube.com/vi/%s/maxresdefault.jpg"%(newytid)
                            try:
                                embed = discord.Embed(title = "%s, (%s)"%(movie, movie["year"]),url = yt_url,description = " Genre:%s"%(movie["genres"]), color = ctx.author.color)
                            except:
                                embed = discord.Embed(title = "%s"%(movie),url = yt_url,description = " Genre:%s"%(movie["genres"]), color = ctx.author.color)
                            try:
                                embed.add_field(name = "Synopsis:", value = "%s"%(str(moviesDB.get_movie_synopsis(movieID)["data"]["plot"][0])))
                            except:
                                pass
                            embed.set_image(url = thumnail_url)
                            embed.add_field(name = "Trailer", value = yt_url, inline=False)

                            listofdirectories = ["rating"]
                            for x in listofdirectories:
                                try:
                                    embed.add_field(name = x, value = "%s"%(movie[x]))
                                except:
                                    pass

                            try:
                                embed.add_field(name= "Episodes:", value = "%s"%(moviesDB.get_movie_episodes(movieID)["data"]["number of episodes"]))
                            except:
                                pass
                            await message.edit(embed=embed)
                        except:
                            await message.edit("Are you sure that was in your watchlist? I couldnt find any info on it.")    
                    if str(confirmation2[0]) == "🚪":
                        await message.edit(embed = discord.Embed(title = "You left", color = ctx.author.color))
                        leavewatchlist == True
                        break

                    
                    
                    
                    if str(confirmation2[0]) == "➖":
                        await message.edit(embed=discord.Embed(title = "type the movie you want to remove!", color = ctx.author.color))
                        try:
                            msg = await self.client.wait_for('message', check = check, timeout = 120)
                            movies  = moviesDB.search_movie(msg.content)
                            movieID = movies[0].getID()
                            movie = moviesDB.get_movie(movieID)
                            print(movie)
                            watchval = mulah.find_one({"id":ctx.author.id}, {"watchlist"})
                            watchval = watchval["watchlist"]
                            print(watchval)
                            if str(movie) in watchval:
                                watchval.remove(str(movie))
                                mulah.update_one({"id":ctx.author.id},{"$set":{"watchlist":watchval}})
                                await message.edit(embed=discord.Embed(title = "I have removed %s from your watchlist!"%(movie)))
                            else:
                                await message.edit("Thats not in your watchlist! Try being more specific!")
                        except asyncio.TimeoutError:
                            await message.edit("You took too long!")                        

            except asyncio.TimeoutError:
                await message.edit("You took too long! i guess we arent doing this!")
            except:
                await message.edit("U need a watchlist bro")


    @commands.command()
    async def clearwatchlist(self, ctx, p1:discord.Member=None):
        if str(ctx.author) == "SentientPlatypus#1332":
            if p1 is None:
                watchvar = mulah.find_one({"id":ctx.author.id},{"watchlist"})
                watchval = watchvar["watchlist"]
                watchval.clear()
                mulah.update_one({"id":ctx.author.id},{"$set":{"watchlist":watchval}})                
            else:
                watchvar = mulah.find_one({"id":p1.id},{"watchlist"})
                watchval = watchvar["watchlist"]
                watchval.clear()
                mulah.update_one({"id":p1.id},{"$set":{"watchlist":watchval}})

def setup(client):
    client.add_cog(currencysys(client))