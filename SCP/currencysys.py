
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
from discord import user
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
import pymongo
import ssl

cluster = Globals.getMongo()
mulah = cluster["discord"]["mulah"]
levelling = cluster["discord"]["levelling"]




gfnamelist = []
class currencysys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        global emotionlist
        emotionlist = Globals.getEmotionList()
        global achievements
        achievements = Globals.getAchievementList()
    

        global worklists
        worklists = Globals.getWorkLists()

        global shopitems
        shopitems = Globals.getShopItems()


        global BattleShop
        BattleShop = Globals.getBattleItems()


        global ToolValues
        ToolValues = Globals.getToolValues()
        global farmitems
        farmitems =Globals.getFarmItems()
        global pcitems
        pcitems = Globals.getPcItems()
        global gameitems
        gameitems = Globals.getGameItems()
        global gamewords
        gamewords = Globals.getGameWords()



    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
    async def work(self, ctx):
        workk = mulah.find_one({"id" : ctx.author.id}, {"money"})
        job = mulah.find_one({"id":ctx.author.id}, {"job"})["job"]
        if job:
            hourlywage = next(x for x in worklists if x["name"]==job)["salary"]
        else:
            hourlywage=15
        print("check1")
        if job:
            print("check2")
            try:
                YourJob = next(x for x in worklists if x["name"]==job)
                workoption = random.choice(["unscramble", "guess"])
                right = False
                wrong = False
                print("check3")
                print(workoption)
                if workoption == "guess":
                    def check(m):
                        return m.author==ctx.author and m.channel==ctx.channel

                    ListOfWords = random.choice(YourJob["sentences"]).split()
                    print(ListOfWords)
                    ListIndex = random.randint(0, len(ListOfWords)-1)
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
                    print(randomword)
                    answer = randomword
                    ll = list(randomword)
                    random.shuffle(ll)

                    while "".join(ll)==answer:
                        random.shuffle(ll)
                        print("".join(ll))
                    finalrandword = "".join(ll)     
                    print(finalrandword)
                    print("sdjfklsdjklf")
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
            except:
                print(traceback.format_exc())
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
        lvl = Globals.GetLevel(ctx.author.id)

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
        lvl = Globals.GetLevel(ctx.author.id)

        x = next(y for y in worklists if y["name"].lower()==jobt.lower())
        if lvl>=x["req"]:
            mulah.update_one({"id":ctx.author.id}, {"$set":{"job":x["name"]}})
            embed = discord.Embed(title = "You Got the Job!", description = "You are now working as %s!"%(x["name"]), color = discord.Color.green())
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title = "You were rejected!", description = "You dont have enough xp to work as a %s!"%(x["name"]), color = discord.Color.red())
            await ctx.channel.send(embed=embed)


    @commands.cooldown(1, 30, BucketType.user)
    @commands.command()
    async def fish(self, ctx):
        inval = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
        if Globals.InvCheck(ctx.author, "fishpole"):
            luck = random.randint(0,100)
            if 10> luck >= 0:
                embed = discord.Embed(title = "Fishing session", description = "You caught back nothing!", color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            else:
                if 50> luck >=10:
                    item = "common fish"
                if 85> luck >= 50:
                    item = "uncommon fish"
                if 95> luck >= 85:
                    item = "rare fish"
                if 101>luck >=95:
                    item = "legendary fish"
                HowMany = random.randint(1,3)
                Globals.AddToInventory(ctx.author, item, farmitems, HowMany)
                embed = discord.Embed(titile = "Fishing session!", description = "You Caught %g `%s`!"%(HowMany, item), color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text = 'You can sell this item using `%ssell "%s"`!'%(Globals.getPrefix(ctx.guild.id) ,item))
                await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("you need a fishpole to fish.")



    @commands.cooldown(1, 30, BucketType.user)
    @commands.command()
    async def hunt(self, ctx):
        inval = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
        if Globals.InvCheck(ctx.author, "rifle"):
            luck = random.randint(0,100)
            if 10> luck >= 0:
                embed = discord.Embed(title = "hunting session", description = "You brought back nothing!", color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            else:
                if 50> luck >=10:
                    item = "mouse"
                if 85> luck >= 50:
                    item = "rabbit"
                if 95> luck >= 85:
                    item = "deer"
                if 101>luck >=95:
                    item = "bigfoot"
                Globals.AddToInventory(ctx.author, item, farmitems)
                embed = discord.Embed(titile = "Hunting session!", description = "You brought back a `%s`!"%(item), color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text = 'You can sell this item using `%ssell "%s"`!'%(Globals.getPrefix(ctx.guild.id),item))
                await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("you need a rifle to hunt.")



    @commands.cooldown(1, 3600, BucketType.user)
    @commands.command()
    async def mine(self, ctx):
        inval = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
        if Globals.InvCheck(ctx.author, "pickaxe") or Globals.InvCheck(ctx.author, "iron pickaxe") or Globals.InvCheck(ctx.author, "gold pickaxe") or Globals.InvCheck(ctx.author, "diamond pickaxe"):
            luck = random.randint(0,100)
            for z in ["pickaxe", "iron pickaxe", "gold pickaxe", "diamond pickaxe"]:
                try:
                    tool = next(x for x in ToolValues if x["name"].lower()==z.lower())
                except:
                    pass
            for x in range(tool["fortune"]):
                luck*=(115/100)
            print(luck)
            if 10> luck >= 0:
                embed = discord.Embed(title = "Mining session", description = "You found nothing!", color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            else:
                if 50> luck >=10:
                    item = "coal"
                if 85> luck >= 50:
                    item = "iron"
                if 90> luck >= 85:
                    item = "gold"
                if 97>luck >=90:
                    item = "diamond"
                if luck >=97:
                    item = "ruby"

                


                HowMany = random.randint(1,3)
                Globals.AddToInventory(ctx.author, item, farmitems, HowMany)
                embed = discord.Embed(titile = "Hunting session!", description = "You found %g `%s`!"%(HowMany,item), color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text = 'You can sell this item using `%ssell "%s"`!'%(Globals.getPrefix(ctx.guild.id),item))
                await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("you need a pickaxe to mine.")



    @commands.cooldown(1, 60, BucketType.user)
    @commands.command()
    async def farm(self, ctx):
        inval = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
        if Globals.InvCheck(ctx.author, "hoe") or Globals.InvCheck(ctx.author, "iron hoe") or Globals.InvCheck(ctx.author, "gold hoe") or Globals.InvCheck(ctx.author, "diamond hoe"):
            luck = random.randint(0,100)
            for z in ["hoe", "iron hoe", "gold hoe", "diamond hoe"]:
                try:
                    tool = next(x for x in ToolValues if x["name"].lower()==z.lower())
                except:
                    pass
            for x in range(tool["fortune"]):
                luck*=(115/100)
            luck = random.randint(0,100)
            if 10> luck >= 0:
                embed = discord.Embed(title = "Farming session", description = "You got nothing!", color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            else:
                if 50> luck >=10:
                    item = "wheat"
                if 85> luck >= 50:
                    item = "beetroot"
                if 90> luck >= 85:
                    item = "melon"
                if luck >=90:
                    item = "pumpkin"
                HowMany = random.randint(1,3)
                Globals.AddToInventory(ctx.author, item, farmitems, HowMany)
                embed = discord.Embed(titile = "Farming session!", description = "You brought back %g `%s`!"%(HowMany,item), color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text = 'You can sell this item using `%ssell "%s"`!'%(Globals.getPrefix(ctx.guild.id),item))
                await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("you need a hoe to farm.")

    @commands.cooldown(1, 3600, BucketType.user)
    @commands.command()
    async def chop(self, ctx):
        inval = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
        if Globals.InvCheck(ctx.author, "axe") or Globals.InvCheck(ctx.author, "iron axe") or Globals.InvCheck(ctx.author, "gold axe") or Globals.InvCheck(ctx.author, "diamond axe"):
            luck = random.randint(0,100)
            for z in ["axe", "iron axe", "gold axe", "diamond axe"]:
                try:
                    tool = next(x for x in ToolValues if x["name"].lower()==z.lower())
                except:
                    pass
            for x in range(tool["fortune"]):
                luck*=(115/100)
            luck = random.randint(0,100)
            if 10> luck >= 0:
                embed = discord.Embed(title = "Chopping session", description = "You found no trees!", color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            else:
                if 50> luck >=10:
                    HowMany = 10
                if 85> luck >= 50:
                    HowMany = 20
                if 90> luck >= 85:
                    HowMany = 50
                if luck >=90:
                    HowMany = 100
                item = "wood"
                Globals.AddToInventory(ctx.author, item, farmitems, HowMany)
                embed = discord.Embed(titile = "Farming session!", description = "You brought back %g `%s`!"%(HowMany,item), color = discord.Color.blue())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text = 'You can sell this item using `%ssell "%s"`!'%(Globals.getPrefix(ctx.guild.id),item))
                await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("you need an axe to farm.")


    @commands.command()
    async def sell(self, ctx, ItemToSell, number=None):
        inval = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
        money = mulah.find_one({"id":ctx.author.id}, {"money"})["money"]
        if Globals.InvCheck(ctx.author, ItemToSell):
            item= next(x for x in inval if x["name"].lower()==ItemToSell.lower() and "parts" not in x.keys())

            if not number:
                number="1"
            if number:
                if not number.isdigit():
                    if number.lower()=="all":
                        number = item["amount"]
            number=int(number)
            number = abs(number)

            AllItems = pcitems+shopitems+gameitems+farmitems+ToolValues+BattleShop
            ItemRef = next(x for x in AllItems if x["name"].lower()==item["name"].lower())
            print(ItemRef)
            SoldFor = ItemRef["value"]*number
            money+=SoldFor
            Globals.RemoveFromInventory(ctx.author, item["name"], number)
            mulah.update_one({"id":ctx.author.id}, {"$set":{"money":money}})
            embed = discord.Embed(title = "Successfull sale", description = "%s sold %s `%s` for `$%s`!"%(ctx.author.mention, number, item["name"], SoldFor), color = discord.Color.green())
            embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text = "You now have `$%s`"%(money))
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("You dont have this item in your inventory.")

    @commands.command()
    async def craft(self, ctx, ItemToCraft=None):
        if not ItemToCraft:
            embed=discord.Embed(title = "Craftable items!", description = "if you have the resources, you can craft items! better items give better drops!", color = discord.Color.blue())
            for x in ToolValues:
                try:
                    check = "✅"
                    recipe = x["craft"]
                    for z in recipe:
                        if not Globals.InvCheck(ctx.author, z, False, recipe[z]):
                            check="❌"
                    string = ""
                    for y in recipe.keys():
                        string+="`%s %s`,"%(y, x["craft"][y])
                    embed.add_field(name = x["name"]+" "+check, value = "Crafting recipe: %s"%(string))
                except:
                    pass
            await ctx.channel.send(embed=embed)
        else:
            tool = next(x for x in ToolValues if x["name"].lower()==ItemToCraft.lower())
            recipe = tool["craft"]
            check = True
            for x in recipe.keys():
                if not Globals.InvCheck(ctx.author, x, False, recipe[x]):
                    check=False
            if check:
                for x in recipe.keys():
                    Globals.RemoveFromInventory(ctx.author, x, recipe[x])
                Globals.AddToInventory(ctx.author, tool["name"], ToolValues)
                embed =discord.Embed(title = "Successfull Craft!", description = "You have crafted a %s!"%(tool["name"]), color = discord.Color.green())
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("You dont have enough resources to craft this.")


    @commands.command()
    @commands.is_owner()
    async def UpgradePoint(self, ctx):
        XpRank = levelling.find()
        MulahRank = mulah.find()
        for x in XpRank:
            print(x)
            DbId = x["id"]
            CurrentLevel = Globals.GetLevel(DbId)
            temp = ctx.guild.get_member(int(DbId))
            try:
                Globals.AddToInventory(temp, "UpgradePoint", BattleShop, CurrentLevel)
            except:
                pass

        
    @commands.command()
    async def send(self, ctx, p1:discord.Member, amount:int):
        money = mulah.find_one({"id":ctx.author.id}, {"money"})["money"]
        money1 = mulah.find_one({"id":p1.id}, {"money"})["money"]
        if money>=amount:
            if amount>0:
                money-=amount
                money1+=amount
                
                mulah.update_one({"id":ctx.author.id},{"$set":{"money":money}})
                mulah.update_one({"id":p1.id},{"$set":{"money":money1}})

                embed = discord.Embed(title = "Successfull transaction!", description  = "%s has sent `$%s` to %s!"%(ctx.author.mention, amount, p1.mention), color = discord.Color.green())
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(title = "Failed transaction!", description  = "%s is trying to send a negative amount of money. use `rob` instead lol"%(ctx.author.mention), color = discord.Color.red())
                await ctx.channel.send(embed=embed)
  
        else:
            embed = discord.Embed(title = "Failed transaction!", description  = "%s doesnt have enough money"%(ctx.author.mention), color = discord.Color.red())
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
            namee=ctx.author
        embed = discord.Embed(title = "%s's current balance"%(namee.display_name), color = ctx.author.color)
        walletval = mulah.find_one({"id":namee.id},{"money"})
        bankval = mulah.find_one({"id":namee.id},{"bank"})
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

        embed.add_field(name="bank", value = bankval["bank"])
        embed.set_author(icon_url=namee.avatar_url, name = namee.display_name)
        await ctx.send(embed = embed)           
    






            





      
        









    @commands.group(invoke_without_command = True)
    async def shop(self,ctx):
        embed = discord.Embed(title = "SHOP INSTRUCTIONS", description = 'use `^buy "<item>"` to buy something.`navigate with reactions`', color = ctx.author.color)
        global shopitems
        global pcitems
        global gameitems
        
        shopmessage = await ctx.send(embed = embed)
        reactionlist = ["🎮", "🖥️", "🛒","🪓","🌳","❤️","⚔️", "🚪"]
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
                    embed = discord.Embed(title = "Game Shop!", description = "Buy games to play on your pc!", color = ctx.author.color)
                    for x in gameitems:
                        finalstring = ""
                        for z in x.keys():
                            if not z == "name":
                                if not z=="value":
                                    extrastring = "%s: %s\n"%(z,x[z])
                                    finalstring+=extrastring
                        embed.add_field(name = "%s -$%s"%(x["name"], x["value"]), value = finalstring)
                    await shopmessage.edit(embed=embed)
                if thereaction == "❤️":
                    embed = discord.Embed(title = "Girlfriend shop", description = "Improve your relationship!",color = ctx.author.color)
                    for x in range(len(shopitems)):
                        nameee = shopitems[x]
                        embed.add_field(name = "%s"%(nameee["name"]), value = "`$%s`| %s"%(nameee["value"], nameee["desc"]), inline=False)
                    await shopmessage.edit(embed = embed)    
                if thereaction == "🛒":
                    embed = discord.Embed(title = "SHOP INSTRUCTIONS", description = 'use `^buy "<item>"` to buy something.`navigate with reactions`',color = ctx.author.color)
                    await shopmessage.edit(embed = embed)   
                if thereaction == "⚔️":
                    embed = discord.Embed(title = "MMORPG shop", description = "Battle gear!",color = ctx.author.color)
                    for x in range(len(BattleShop)):
                        nameee = BattleShop[x]
                        embed.add_field(name = "%s"%(nameee["name"]), value = "`$%s`| %s"%(nameee["value"], nameee["desc"]), inline=False)
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

                if thereaction=="🪓":
                    embed = discord.Embed(title = "Tools!", description = "use `^craft` to make new tools!",color = ctx.author.color)
                    for x in range(len(ToolValues)):
                        nameee = ToolValues[x]
                        embed.add_field(name = "%s"%(nameee["name"]), value = "`$%s`| %s"%(nameee["value"], nameee["desc"]), inline=True)
                    await shopmessage.edit(embed = embed)      

                if thereaction=="🌳":
                    embed = discord.Embed(title = "Farming rates", description = 'use `%ssell "<material>"` to sell something!',color = ctx.author.color)
                    for x in range(len(farmitems)):
                        nameee = farmitems[x]
                        embed.add_field(name = "%s"%(nameee["name"]), value = "`$%s`| %s"%(nameee["value"], nameee["desc"]), inline=True)
                    await shopmessage.edit(embed = embed)   
                
                if thereaction == "🚪":
                    await shopmessage.edit(embed=discord.Embed(title = "You left the shop!"))   
                    break
                await shopmessage.remove_reaction(emoji=thereaction, member=ctx.author)















    @commands.group(invoke_without_command=True)
    async def pc(self, ctx):
        embed = discord.Embed(title = "Build a pc.", description = "herer are some commands. use `^pc` before each one", color = ctx.author.color)
        embed.add_field(name = "commands", value = "`add`, `remove`, `build`")
        await ctx.channel.send(embed = embed)

    @pc.command()
    @Globals.hasItem("pc")
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
                            embed=discord.Embed(title="Added Ram to PC", description="nice, i doubt you will need it tho lol", color=discord.Color.green())
                            await ctx.send(embed=embed)
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
    @Globals.hasItem("pc")
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
    @Globals.hasItem("pc")
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
                ThePcYouareInstallingOn=emptydict[msg.content]
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
                        embed = discord.Embed(title="Added %s to %s"%(finaldict[msg.content], ThePcYouareInstallingOn), description="congrats on your new game! play it with `pc play`", color = discord.Color.green())
                        embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
                        await ctx.channel.send(embed=embed)
                    else:
                        await ctx.send("please type the lowercase letter associated with the game. try the command again please.")
                except asyncio.TimeoutError:
                    await ctx.channel.send("You took to long! do the command again!")
                            


        except asyncio.TimeoutError:
            await ctx.channel.send("You took too long!")
        
        
        
        
        
        
        







    @pc.command()
    @Globals.hasItem("pc")
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
    @Globals.hasItem("pc")
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
        number = abs(number)
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
    async def dep(self, ctx, amount=None):
        money = mulah.find_one({"id":ctx.author.id}, {"money"})["money"]
        try:
            if amount.lower()=="all":
                amount = money
            else:
                amount=int(amount)
        except:
            pass
        if amount<=money:
            if amount>0:
                money-=amount
                mulah.update_one({"id":ctx.author.id}, {"$inc":{"bank":amount}})
                mulah.update_one({"id":ctx.author.id}, {"$set":{"money":money}})
                embed = discord.Embed(title = "Successfull deposit", description = "You have deposited `$%g` into your bank!"%(amount), color=discord.Color.green())
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(title = "Failed deposit", description = "You are trying to deposit a negative amount of money. that is called withdrawing lmao", color=discord.Color.red())
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
                await ctx.channel.send(embed=embed)
              
        else:
            embed = discord.Embed(title = "Failed deposit", description = "You dont have that much money lmao", color=discord.Color.red())
            embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
            await ctx.channel.send(embed=embed)
          

    @commands.command()
    async def withdraw(self, ctx, amount=None):
        bank = mulah.find_one({"id":ctx.author.id}, {"bank"})["bank"]
        try:
            if amount.lower()=="all":
                amount = bank
            else:
                amount=int(amount)
        except:
            pass

        if amount<=bank:
            if amount>0:
                bank-=amount
                mulah.update_one({"id":ctx.author.id}, {"$inc":{"money":amount}})
                mulah.update_one({"id":ctx.author.id}, {"$set":{"bank":bank}})
                embed = discord.Embed(title = "Successfull withdrawal", description = "You have withdrawn `$%g` from your bank!"%(amount), color=discord.Color.green())
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
                await ctx.channel.send(embed=embed)
            else:
                embed = discord.Embed(title = "Failed withdrawal", description = "You are trying to withdraw a negative amount of money. that is called a deposit lmao", color=discord.Color.red())
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
                await ctx.channel.send(embed=embed)
              
        else:
            embed = discord.Embed(title = "Failed withdrawal", description = "You dont have that much money lmao", color=discord.Color.red())
            embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
            await ctx.channel.send(embed=embed)




    @commands.command()
    async def buy(self,ctx, item:str, number:int=None):
        global shopitems
        global pcitems     
        global gameitems
        if number is None:
            number = 1   
        allitems = pcitems+shopitems+gameitems
        xvalue = []
        AllItems = pcitems+shopitems+gameitems+farmitems+ToolValues+BattleShop
        for x in AllItems:
            if item.lower() == x["name"].casefold():
                xvalue.append(x)
                itemvalue = x["value"]
                itemdesc = x["desc"]
                walletvar = mulah.find_one({"id":ctx.author.id}, {"money"})
                walletval = walletvar["money"]
                inval = mulah.find_one({"id":ctx.author.id}, {"inv"})["inv"]
                if itemvalue*number<=walletval:
                    walletval-=number*itemvalue
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"money":walletval}})
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
            p1 = ctx.author

        embed.set_author(name = p1.display_name, icon_url=p1.avatar_url)
        invar = mulah.find_one({"id":p1.id}, {"inv"})
        inval = invar["inv"]
        for entry in inval:
            embed.add_field(name = "%s  (%s)"%(entry["name"], entry["amount"]), value = "%s"%(entry["desc"]), inline = False)
        await ctx.channel.send(embed = embed)

            
    @commands.command()
    @commands.is_owner()
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
    @commands.cooldown(1, 1000, BucketType.user)
    async def beg(self,ctx):
        dictionaryofresponses = Globals.getBegList()
        randominteger=random.randint(1,10)
        embed=discord.Embed(title=dictionaryofresponses[randominteger]["name"], description = dictionaryofresponses[randominteger]["value"], color=discord.Color.green())
        embed.set_footer(text="You have recieved $%g"%(dictionaryofresponses[randominteger]["amount"]))
        mulah.update_one({"id":ctx.author.id}, {"$inc":{"money":dictionaryofresponses[randominteger]["amount"]}})
        await ctx.channel.send(embed=embed) 
    @commands.command()
    @commands.is_owner()
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
    @commands.is_owner()
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
        YouWins =mulah.find_one({"id":ctx.author.id}, {"duelwins"})["duelwins"] 
        Youloss =mulah.find_one({"id":ctx.author.id}, {"duelloses"})["duelloses"] 

        embed = discord.Embed(title = "%s' Profile!"%(p1.display_name), description = "Use the reactions to navigate the profile!", color = discord.Color.blue())
        embed.set_image(url = p1.avatar_url)
        reactions = ["💰","❤️","🎮", "🏆","💼", "⚔️","⭐","🚪"]
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
                    embed = discord.Embed(title = "MMORPG stats!", color = discord.Color.blurple())
                    for x in mmorpg.keys():
                        if x == "loadout":
                            finalstring=""
                            for x in mmorpg["loadout"].keys():
                                finalstring+="%s: %s\n"%(x, mmorpg["loadout"][x])
                            embed.add_field(name = "Loadout:", value = finalstring, inline=False)
                            embed.add_field(name = "duel wins:", value = YouWins, inline=False)
                            embed.add_field(name = "duel loss:", value = Youloss, inline=False)

                        else:
                            embed.add_field(name = "%s"%(x), value = "%s"%(mmorpg[x]), inline = False)
                    embed.add_field(name = "XP", value = mulah.find_one({"id":ctx.author.id}, {"abilityxp"})["abilityxp"])

                if rawreaction == "💰":
                    try:
                        walletval = mulah.find_one({"id":p1.id}, {"money"})["money"]
                        embed = discord.Embed(title = "%s's Financial stability!"%(p1.display_name), color = discord.Color.blue())
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
                        embed = discord.Embed(title = "This man hasnt worked a single day in his life.", color = discord.Color.blue())
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
                            embed = discord.Embed(title = "get a gf", color = discord.Color.blue())
                            
                    except:
                        embed = discord.Embed(title = "Single af. rip.", color = discord.Color.blue()) 
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
                        embed = discord.Embed(title = "Your game stats", color = discord.Color.blue())
                        for x in gameval.keys():
                            embed.add_field(name = "%s"%(x), value = "Skill:%s"%(gameval[x]))


                    except:
                        print(traceback.format_exc())
                        embed = discord.Embed(title = "You dont have any stats!", color = discord.Color.blue())    
                if rawreaction == "🏆": 
                    global achievements
                    try:
                        achievementval = mulah.find_one({"id":p1.id}, {"achievements"})["achievements"]
                        embed = discord.Embed(title = "%s's achievements!"%(p1.display_name), description = "use ^achievements for a more detailed view!", color = discord.Color.blue())
                        for y in achievementval:
                            achievementdict = next(x for x in achievements if x["name"] ==y)
                            embed.add_field(name = y+" "+Globals.achievementcheck(p1,y), value = achievementdict["desc"], inline = False)


                    except:
                        mulah.update_one({"id":p1.id}, {"$set":{"achievements":[]}})     
                        embed = discord.Embed(title = "He has no achievements. Rip", color = discord.Color.blue())
                if rawreaction=="🚪":
                    embed = discord.Embed(title = "You have left the profile!", color =ctx.author.color)
                    await profilembed.edit(embed=embed)
                    leave = True
                
                if rawreaction=="💼":
                    embed = discord.Embed(title = "%s's inventory"%(p1.display_name), color = discord.Color.blue())
                    invariable = mulah.find_one({"id": p1.id}, {"inv"})
                    invariable = invariable["inv"]
                    embed.set_author(name = p1.display_name, icon_url=p1.avatar_url)
                    invar = mulah.find_one({"id":p1.id}, {"inv"})
                    inval = invar["inv"]
                    for entry in inval:
                        embed.add_field(name = "%s  (%s)"%(entry["name"], entry["amount"]), value = "%s"%(entry["desc"]), inline = False)

                if rawreaction=="⭐":
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

                await profilembed.edit(embed=embed)
                await profilembed.remove_reaction(emoji = rawreaction,member =ctx.author)                    


    

    @commands.command()
    async def richlb(self, ctx):
        ids = [x.id for x in ctx.guild.members]
        rankings = mulah.find().sort("net",-1)
        count=0
        i=1
        embed = discord.Embed(title = "%s's richest users"%(ctx.guild.name), color = ctx.author.color)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(int(x["id"])).display_name

                tempswears = x["net"]
                embed.add_field(name = f"{i}: {temp}", value = f"net worth: `${tempswears}`", inline = False) 
                i+=1
                if i==11:
                    break
            except:
                pass
        await ctx.channel.send(embed=embed)


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
                    if str(confirmation2[0]) == "➕":
                        await message.edit(embed=discord.Embed(title = "Search for a movie/show to add!", color = ctx.author.color))
                        try:
                            msg = await self.client.wait_for('message', check = check, timeout = 120)
                            dictt = await Globals.Imdb(ctx, msg.content)
                            embed = dictt[0]
                            movie = dictt[1]
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
                await ctx.channel.send("cleared watchlist")            
            else:
                if not ctx.author.guild_permissions.administrator:
                    raise commands.MissingPermissions("administrator")
                    return 
                watchvar = mulah.find_one({"id":p1.id},{"watchlist"})
                watchval = watchvar["watchlist"]
                watchval.clear()
                mulah.update_one({"id":p1.id},{"$set":{"watchlist":watchval}})
                await ctx.channel.send("cleared watchlist")            

def setup(client):
    client.add_cog(currencysys(client))