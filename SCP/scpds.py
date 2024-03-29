from discord import message
from discord.ext.commands.converter import RoleConverter
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
from discord.ext.commands.core import command
from discord.member import Member
from discord.player import PCMAudio
from discord.utils import time_snowflake
from pymongo import DESCENDING, MongoClient
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
from io import BytesIO, IncrementalNewlineDecoder
import requests
import Globals
import pymongo
import ssl

cluster = Globals.getMongo()
mulah = cluster["discord"]["mulah"]
class noGirlfriend(commands.CommandError):
    def __init__(self, user, *args, **kwargs):
        self.user = user

class tooLong(commands.CommandError):
    def __init__(self, user, *args, **kwargs):
        self.user = user


def hasGirlfriend():
    def predicate(ctx):
        gf = mulah.find_one({"id":ctx.author.id}, {"gf"})["gf"]
        if gf==0 or gf==None:
            raise noGirlfriend(ctx.author)
        else:
            return True
    return commands.check(predicate)

class noWatchlist(commands.CommandError):
    def __init__(self, user, *args, **kwargs):
        self.user = user

def hasWatchlist():
    def predicate(ctx):
        gf = mulah.find_one({"id":ctx.author.id}, {"watchlist"})["watchlist"]
        if not gf:
            raise noWatchlist(ctx.author)
        else:
            return True
    return commands.check(predicate)

class insufficientLovePoints(commands.CommandError):
    def __init__(self, user, lp, *args, **kwargs):
        self.user=user
        self.requiredlb = lp
def hasLovePoints(lp:int):
    def predicate(ctx):
        points = mulah.find_one({"id":ctx.author.id}, {"lp"})["lp"]
        if points >= lp:
            return True
        else:
            raise insufficientLovePoints(ctx.author, lp)
    return commands.check(predicate)

class DatingSim(commands.Cog):
    def __init__(self, client):
        self.client = client



    @commands.Cog.listener()
    async def on_ready(self):
        global emotionlist
        emotionlist = Globals.getEmotionList()


        global backgrounds
        backgrounds = Globals.getBackgroundList()



        global restaurants
        restaurants = Globals.getRestaurants()


        global datetalkmap
        datetalkmap = Globals.getDateTalkMap()


        global talkmap
        talkmap = Globals.getTalkMap()

        global boinkresponse
        boinkresponse = Globals.getBoinkResponse()


        global pcitems
        pcitems = Globals.getPcItems
        global gameitems
        gameitems = Globals.getGameItems()
        global gamewords
        gamewords = Globals.getGameWords()
        global shopitems
        shopitems = Globals.getShopItems()

        global gftypes
        gftypes = Globals.getGfTypes()
        
        global typeconplaint  
        typeconplaint = Globals.getTypeComplaint()
        global typegenrepraise
        typegenrepraise = Globals.getTypeGenrePraise()
        global gfgamingresponse
        gfgamingresponse = Globals.getGfGamingResponse()
        global typepraise
        typepraise = Globals.getTypePraise()






    @commands.group(invoke_without_command=True)
    async def gf(self,ctx):
        await ctx.send("use a command.")




    @gf.command()
    @hasGirlfriend()
    async def image(self, ctx):
        leave = False
        while leave == False:
            gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})
            gfdict = gfvar["gf"]
            global emotionlist
            alphlist = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟', '🚪']
            count = 0
            reactionlist = []
            emptydict = {}
            for x in emotionlist:
                emptydict[alphlist[count]]=x
                reactionlist.append(alphlist[count])
                count+=1
            reactionlist.append('🚪')
            embed = discord.Embed(title = "Girlfriend Images!", description = "Personalize your girlfriend experience with images based upon emotion! transparent images are preferred, as they will look nicer.", color = ctx.author.color)
            count = 0
            for x in emotionlist:
                valuestr = ""
                checkorno = ""
                try:
                    valuestr+=gfdict[x]
                    checkorno+="✅"
                except:

                    valuestr+="You havnt uploaded an image yet!"
                    checkorno+="❌"
                embed.add_field(name = "%s: %s---> %s"%(alphlist[count], x, checkorno), value = valuestr, inline = False)
                count+=1
            embed.set_footer(text = "Use the reactions to change or examine your images!")
            try:
                await msg.delete()
                msg = await ctx.channel.send(embed=embed)
            except:
                msg = await ctx.channel.send(embed=embed)
            for x in reactionlist:
                await msg.add_reaction(x)
            
            def check(reaction,user):
                return user ==ctx.author and str(reaction.emoji) in alphlist and reaction.message == msg
            
            confirm = await self.client.wait_for('reaction_add', check=check)
            if confirm:
                reactionstr = str(confirm[0])
                if reactionstr == '🚪':
                    await ctx.channel.send("you have left the manu")
                    leave = True
                    break
                else:
                    embed = discord.Embed(title = "Update %s' %s!"%(gfdict["name"], emptydict[reactionstr]), color = ctx.author.color)
                    try:
                        embed.set_image(url = gfdict[emptydict[reactionstr]])
                    except:
                        embed.add_field(name = "No image",value = "go get one!", inline = False)
                    updatereaction = ['📁', '⬅️', '🚪']
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    for x in updatereaction:
                        await msg.add_reaction(x)
                    def check2(reaction, user):
                        return user ==ctx.author and str(reaction.emoji) in updatereaction and reaction.message == msg
                    
                    confirm2 = await self.client.wait_for('reaction_add', check=check2)
                    if confirm2:
                        reactionstrr = str(confirm2[0])
                        if reactionstrr == '🚪':
                            await ctx.channel.send("you have left the menu")
                            leave = True
                            break
                        if reactionstrr == '📁':
                            embed = discord.Embed(title = "input a url to update image", description = "url must be http or https", color = ctx.author.color)
                            await msg.clear_reactions()
                            await msg.edit(embed = embed)

                            def check3(m):
                                return m.author==ctx.author and m.channel==ctx.channel
                            confirm3 = await self.client.wait_for('message', check=check3)
                            turl = confirm3.content
                            emotion = emptydict[reactionstr]
                            if emotion is None:
                                emotion = "image"
                            if emotion.lower() in emotionlist:
                                if turl.startswith('http'):
                                    try:
                                        gfdict[emotion] = turl
                                        mulah.update_one({"id":ctx.author.id}, {"$set":{"gf":gfdict}})
                                        embed = discord.Embed(title = "You have updated %s's %s"%(gfdict["name"], emotion), color = ctx.author.color)
                                        embed.set_image(url = turl)
                                        m = await ctx.channel.send(embed = embed)
                                        await confirm3.delete()
                                        await asyncio.sleep(1)
                                        await m.delete()
                                    except:
                                        await ctx.channel.send("Get a girlfriend first")
                                else:
                                    await ctx.channel.send("make sure its http or https")
                            else:
                                await ctx.channel.send("you need a valid emotion! There is %s"%(",".join(emotionlist)))
                        if reactionstrr =='⬅️':
                            pass
                        await msg.clear_reactions()





































































    @gf.command()
    @hasGirlfriend()
    @hasWatchlist()
    @commands.cooldown(1, 360, BucketType.user)
    @Globals.hasItem(itemToCheckFor="netflixsub")
    async def netflix(self,ctx):
        global typegenrepraise
        global typeconplaint
        global typepraise
        global gftypes
        if mulah.find_one({"id":ctx.author.id}, {"gf"})["gf"]!=0:
            invar = mulah.find_one({"id":ctx.author.id},{"inv"})   
            inval = invar["inv"]     
            ticketcheck = next((item for item in inval if item["name"] == "netflixsub" and "parts" not in item.keys()), None)   
            if ticketcheck is not None:
                moviesDB = IMDb()
                gfvar = mulah.find_one({"id":ctx.author.id},{"gf"})
                gfval = gfvar["gf"]
                lpvar = mulah.find_one({"id":ctx.author.id},{"lp"})
                lpval = lpvar["lp"]
                showvar = mulah.find_one({"id":ctx.author.id},{"watchlist"})
                showval = showvar["watchlist"]            
                alphabet = string.ascii_lowercase
                alphlist = list(alphabet)
                emptydict = {}
                count = 0
                finalstring = ""
                movielist = []
                for x in showval:
                    movielist.append(str(x))
                    emptydict[alphlist[count]] = str(x)
                    finalstring+= alphlist[count] + "| " + "%s\n"%(x)
                    count+=1


                embed = discord.Embed(title = "Choose a Movie/Show!", description = finalstring, color = ctx.author.color)
                await ctx.channel.send(embed=embed)

                def check(m):
                    return m.author==ctx.author and m.channel==ctx.channel
                
                try:
                    msg = await self.client.wait_for('message', check=check,timeout = 30)
                    if emptydict[msg.content.lower()] in movielist:
                        moviesearch = moviesDB.search_movie(emptydict[msg.content.lower()])
                        id = moviesearch[0].movieID

                        moviefind = moviesDB.get_movie(id)
                        genre = moviefind["genres"]
                        genre = [x.lower() for x in genre]

                        gfsat = 23
                        dialogue = ""
                        try:
                            if moviefind["rating"] <6:
                                dialogue+=next(item for item in gftypes if item["typename"] == gfval["type"])["netflixresponse"][0]
                            if 6<=moviefind["rating"]<8:
                                dialogue+=next(item for item in gftypes if item["typename"] == gfval["type"])["netflixresponse"][1]
                            if 8<=moviefind["rating"]:
                                dialogue+=next(item for item in gftypes if item["typename"] == gfval["type"])["netflixresponse"][2]
                        except:
                            dialogue+=next(item for item in gftypes if item["typename"] == gfval["type"])["netflixresponse"][2]
                        if gfval["dislikes"] in genre:
                            dialogue+="typeconplaint"
                            gfsat*=85/100
                        if gfval["favorite genre"] in genre:
                            try:
                                dialogue += next(item for item in typegenrepraise if item["typename"] == gfval["type"])[gfval["favorite genre"]]
                            except:
                                pass
                            gfsat*=115/100
                        if gfval["likes"] == "relaxing":
                            dialogue += next(item for item in typepraise if item["typename"] == gfval["type"])["relaxing"]
                            gfsat+=115/100

                        gfResponse = Globals.getGFresponse("*watches %s with you*"%(emptydict[msg.content.lower()]), ctx.author)
                        embed = discord.Embed(title = "You watched %s with %s"%(emptydict[msg.content.lower()],gfval["name"]), color = ctx.author.color)
                        embed.add_field(name = "%s:"%(gfval["name"]), value = gfResponse)
                        try:
                            embed.set_image(url=Globals.getGFimage(ctx.author,Globals.classifyGFEmotion(gfResponse)))
                        except:
                            pass
                        lpval+=math.floor(gfsat)
                        embed.set_footer(text="You gained %s Love points."%(math.floor(gfsat)))
                        await ctx.channel.send(embed=embed)
                        mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})
                        data = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]    
                        data["netflix"]+=1
                        mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":data}})

                    else:
                        pass
                except asyncio.TimeoutError:
                    await ctx.channel.send("You took too long! I guess we arent doing this.")
                    

            else:
                gfvar = mulah.find_one({"id":ctx.author.id},{"gf"})
                gfval = gfvar["gf"]     
                embed = discord.Embed(title = "%s"%(gfval["name"]), description = "you need a netflix subscription, %s"%(ctx.author.display_name), color = ctx.author.color)
                try:
                    embed.set_image(url = gfval["dissapointed"])
                except:
                    try:
                        embed.set_image(url = gfval["image"])
                    except:
                        pass
                await ctx.channel.send(embed=embed)
                
        else:
            await ctx.channel.send("You dont have a gf lmao")
            












    @gf.command()
    @hasGirlfriend()
    @commands.cooldown(1, 600, BucketType.user)
    @hasLovePoints(120)
    async def holdhand(self,ctx):
        global typegenrepraise
        global typeconplaint
        global typepraise
        global gftypes
        try: 
            gfvar = mulah.find_one({"id":ctx.author.id},{"gf"})   
            gfval = gfvar["gf"]
            lpvar = mulah.find_one({"id":ctx.author.id},{"lp"})
            lpval = lpvar["lp"] 
            embed = discord.Embed(title = "You held %s's hand!"%(gfval["name"]), color = ctx.author.color)
            try:
                dialogue = Globals.getGFresponse("*holds your hand*", ctx.author)
            except:
                dialogue = next(item for item in gftypes if item["typename"] == gfval["type"])["hugresponse"]
            embed.add_field(name = "%s:"%(gfval["name"]), value = dialogue)
            try:
                embed.set_image(url=Globals.getGFimage(ctx.author, Globals.classifyGFEmotion(dialogue)))
            except:
                pass
            embed.set_footer(text = "You have gained 25 Love points!")
            await ctx.channel.send(embed=embed)
            lpval+=15
            mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})
        except:
            await ctx.channel.send("You need a girlfriend lmao")







    @gf.command()
    @hasGirlfriend()
    @commands.cooldown(1, 600, BucketType.user)
    @hasLovePoints(150)
    async def hug(self,ctx):
        global typegenrepraise
        global typeconplaint
        global typepraise
        global gftypes
        try: 
            gfvar = mulah.find_one({"id":ctx.author.id},{"gf"})   
            gfval = gfvar["gf"]
            lpvar = mulah.find_one({"id":ctx.author.id},{"lp"})
            lpval = lpvar["lp"] 
            embed = discord.Embed(title = "You hugged %s!"%(gfval["name"]), color = ctx.author.color)
            try:
                dialogue = Globals.getGFresponse("*hugs you*", ctx.author)
            except:
                dialogue = next(item for item in gftypes if item["typename"] == gfval["type"])["hugresponse"]
            embed.add_field(name = "%s:"%(gfval["name"]), value = dialogue)
            try:
                embed.set_image(url=Globals.getGFimage(ctx.author, Globals.classifyGFEmotion(dialogue)))
            except:
                pass
            embed.set_footer(text = "You have gained 25 Love points!")
            await ctx.channel.send(embed=embed)
            lpval+=25
            mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})
            data = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]    
            data["hugs"]+=1
            mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":data}})
        except:
            await ctx.channel.send("You need a girlfriend lmao")

    @gf.command()
    @hasGirlfriend()
    @hasLovePoints(200)
    @commands.cooldown(1, 600, BucketType.user)
    async def kiss(self,ctx):
        global typegenrepraise
        global typeconplaint
        global typepraise
        global gftypes
        try: 
            gfvar = mulah.find_one({"id":ctx.author.id},{"gf"})   
            gfval = gfvar["gf"]
            lpvar = mulah.find_one({"id":ctx.author.id},{"lp"})
            lpval = lpvar["lp"] 
            if lpval>=200:
                embed = discord.Embed(title = "You kissed %s!"%(gfval["name"]), color = ctx.author.color)
                try:
                    dialogue = Globals.getGFresponse("*kisses you*", ctx.author)
                except:
                    print(traceback.format_exc())
                    dialogue = next(item for item in gftypes if item["typename"] == gfval["type"])["kissresponse"]
                embed.add_field(name = "%s:"%(gfval["name"]), value = dialogue)
                try:
                    embed.set_image(url=Globals.getGFimage(ctx.author,Globals.classifyGFEmotion(dialogue)))
                except:
                    pass
                if gfval["tier"] == 1:
                    
                    gfval["tier"] = 2
                    embed.add_field(name = "%s levelled up!"%(gfval["name"]),value = "She is now a tier %s girlfriend!"%(gfval["tier"]))
                    mulah.update_one({"id":ctx.author.id},{"$set":{"gf":gfval}})
                else:
                    pass
                kisses = mulah.find_one({"id":ctx.author.id},{"kisses"})["kisses"]
                kisses+=1
                mulah.update_one({"id":ctx.author.id},{"$set":{"kisses":kisses}})

                embed.set_footer(text = "You have gained 40 Love points!")
                await ctx.channel.send(embed=embed)
                lpval+=40
                mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})
                data = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]    
                data["kisses"]+=1
                mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":data}})
            else:
                await ctx.channel.send("You dont have enogh love points")
        except:
            await ctx.channel.send("You need a girlfriend lmao")


















    @gf.command()
    @commands.cooldown(1,3600, BucketType.user)
    @commands.is_nsfw()
    @hasGirlfriend()
    @hasLovePoints(800)
    async def boink(self, ctx):
        gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})["gf"]
        gfname = gfvar["name"]
        gfdata = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]
        model = Globals.getModel(ctx.author.id)
        backgroundInfo = Globals.chat.getprompt(ctx.author)
        backgroundInfo += f"Right now, {gfname} wants to be intimate with {ctx.author.display_name}. {gfname} wants to start a family with him. {gfname} wants to be intimate with {ctx.author.display_name}. They are about to do it now."
        newChat = Globals.chat(backgroundInfo, ctx.author.display_name, gfvar["name"], model)
        openstatement = newChat.ask("Hi there!")

        embed = discord.Embed(title = "%s:"%(gfvar["name"]), description= openstatement, color = discord.Color.red())
        embed.set_footer(icon_url=ctx.author.avatar_url, text="type what you want to do. you can literally do anything. just dont do something irrelevant\n type \"end interaction\" to end")
        try:
            embed.set_image(url=Globals.getGFimage(ctx.author, Globals.classifyGFEmotion(openstatement, False)))
        except:
            pass
        toEdit = await ctx.channel.send(embed=embed)

        def check(m):
            return m.author==ctx.author and m.channel == ctx.channel
        
        climax = False
        irrelevance = 0
        ended = False
        lpcounted = 0
        while not climax:
            embed = discord.Embed(title = "%s:"%(gfvar["name"]),color = discord.Color.red())
            embed.set_footer(icon_url=ctx.author.avatar_url, text="type what you want to do. you can literally do anything. just dont do something irrelevantn type \"end interaction\" to end")

            message = await self.client.wait_for('message', check=check, timeout=100)
            if len(message.content) >200:
                raise tooLong(ctx.author)
            if message.content.lower() == "end interaction":
                ended = True
                break
            response = newChat.ask(message.content)
            embed.description = response
            try:
                embed.set_image(url=Globals.getGFimage(ctx.author, Globals.classifyGFEmotion(response, False)))
            except: 
                pass
            

            actionAnalysis = Globals.classifyGFBoinking(message.content).lower()
            if actionAnalysis == "irrelevant":
                Globals.addIrrelevantWarning(embed)
                irrelevance += 1
            await toEdit.delete()
            await message.delete()
            toEdit = await ctx.channel.send(embed=embed)
            if irrelevance >=3:
                break
            if actionAnalysis == "kiss":
                gfdata["kisses"]+=1
                mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":gfdata}})
                mulah.update_one({"id":ctx.author.id}, {"$inc":{"kisses":1}})
                mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":40}})
                lpcounted += 40
            if actionAnalysis == "hug":
                gfdata["hugs"]+=1
                mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":gfdata}})  
                mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":25}})
                lpcounted += 25
            if actionAnalysis == "breast groping":
                await Globals.AchievementEmbed(ctx, "bobs")         
            if actionAnalysis == "climax":
                climax = True
        if irrelevance >=5:
            embed = discord.Embed(title = "irrelevant.", description= "You went off topic.", color = discord.Color.red())
            embed.set_footer(text="You have been penalized $100 and 50 love points")
            mulah.update_one({"id":ctx.author.id}, {"$inc":{"money":-100}})
            mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":-50}})
            return await ctx.channel.send(embed=embed)

        if ended:
            embed = discord.Embed(title = "Interaction ended", color = discord.Color.red())
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f"You have gained {lpcounted} love points!\n complete the boinking to upgrade your girlfriends tier!")
            return await ctx.channel.send(embed=embed)
        lpcounted += 100
        mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":100}})
        embed = discord.Embed(title = "Boinking complete", color=discord.Color.green())
        if gfvar["tier"]<3:
            gfvar["tier"] = 3
            embed.add_field(name = "%s levelled up!"%(gfvar["name"]), value = "she is now tier %s"%(gfvar["tier"]))
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"You have gained {lpcounted} love points!")
        await ctx.channel.send(embed=embed)
        mulah.update_one({"id":ctx.author.id}, {"$inc":{"boinks":1}})
        gfdata["boinks"]+=1
        mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":gfdata}})  
        mulah.update_one({"id":ctx.author.id}, {"$set":{"gf":gfvar}}) 
        



            











    @gf.command()
    @commands.cooldown(1, 3600, BucketType.user)
    @commands.is_nsfw()
    @hasGirlfriend()
    async def boinkk(self,ctx):
        global boinkmap
        global boinkresponse        
        gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})
        gfval = gfvar["gf"]
        lpvar = mulah.find_one({"id":ctx.author.id}, {"lp"})
        lpval = lpvar["lp"]
        if lpval>=800:
            responsedict = next(item for item in boinkresponse if item["typename"] == gfval["type"])
            action = "start"
            climaxx = False
            pinned = False
            actionlist = []
            while climaxx == False:
                global achievementpercent
                UserAchievements = mulah.find_one({"id":ctx.author.id},{"achievements"})["achievements"]
                boinks = mulah.find_one({"id":ctx.author.id},{"boinks"})["boinks"]
                kisses = mulah.find_one({"id":ctx.author.id},{"kisses"})["kisses"]
                if action == "climax":
                    response = responsedict[action]
                    if re.search("\{0\}", response):
                        response = response.format(ctx.author.display_name)
                    embed = discord.Embed(title = "%s:"%(gfval["name"]), description = "%s"%(response), color = ctx.author.color)
                    try:
                        embed.set_image(url = gfval["bed"])
                    except:
                        try:
                            embed.set_image(url = gfval["image"])
                        except:
                            await ctx.channel.send("you should really add an image for your gf")
                    embed.set_footer(text = "You have gained 100 Love points!")
                    boinks+=1
                    mulah.update_one({"id":ctx.author.id},{"$set":{"boinks":boinks}})
                    if gfval["tier"]<3:
                        gfval["tier"] =3
                        embed.add_field(name = "%s levelled up!"%(gfval["name"]), value = "she is now tier %s"%(gfval["tier"]))
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gf":gfval}})
                    lpval+=100
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":lpval}})
                    data = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]    
                    data["boinks"]+=1
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":data}})
                    await editthis.edit(embed=embed)
                    climaxx == True
                    break

                if action == "kiss":
                    kisses+=1
                    mulah.update_one({"id":ctx.author.id},{"$set":{"kisses":kisses}})
                    data = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]    
                    data["kisses"]+=1
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":data}})
                if action == "pin down":
                    pinned = True
                if action in actionlist:
                    response = responsedict[action][1]
                else:
                    response = responsedict[action][0]
                if re.search("\{0\}", response):
                    response = response.format(ctx.author.display_name)

                embed = discord.Embed(title = "%s:"%(gfval["name"]), description = "%s"%(response), color = ctx.author.color)
                alphabet = string.ascii_lowercase
                alphlist = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
                emptydict = {}
                count = 0
                finalstring = ""
                actions = []
                reactions = []
                boinkmapdict = next(item for item in boinkmap if item["action"] == action)
                for x in boinkmapdict["map"]:
                    if x == "pin down":
                        if pinned:
                            pass
                        else:
                            actions.append(x)
                            emptydict[alphlist[count]] = x
                            finalstring+= alphlist[count] + "| " + "%s\n"%(x)
                            reactions.append(alphlist[count])
                            count+=1
                    else:
                        actions.append(x)
                        emptydict[alphlist[count]] = x
                        finalstring+= alphlist[count] + "| " + "%s\n"%(x)
                        reactions.append(alphlist[count])
                        count+=1
                embed.add_field(name = "what will you do?", value = finalstring)
                try:
                    embed.set_image(url = gfval[boinkmapdict["img"]])
                except:
                    try:
                        embed.set_image(url = gfval["image"])
                    except:
                        pass   
                actionlist.append(action)
                listofcomp = [Button(style = ButtonStyle.red, label = x) for x in actions]
                if action == "start":
                    editthis = await ctx.channel.send(embed=embed) 
                if action!="start":
                    await editthis.edit(embed=embed)
                    await editthis.clear_reactions()
                for x in range(len(reactions)):
                    await editthis.add_reaction(alphlist[x])


                def check4(reaction,user):
                    return user==ctx.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'] and reaction.message == editthis                         

                confirmation = await self.client.wait_for('reaction_add',check=check4)

                if confirmation:
                    action = emptydict[str(confirmation[0])]
        else:
            await ctx.channel.send("You dont have enough love points for that. Lmao get cock blocked")

    @gf.command()
    @hasGirlfriend()
    @Globals.hasItem(itemToCheckFor="ring")
    @commands.cooldown(1, 600, BucketType.user)
    async def propose(self,ctx):
        global gftypes
        gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})
        gfval = gfvar["gf"]
        lpvar = mulah.find_one({"id":ctx.author.id}, {"lp"})
        lpval = lpvar["lp"]    
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        if lpval>=1600:
            if next((x for x in inval if x["name"] == "ring" and "parts" not in x.keys()), None) is not None:
                if gfval["tier"] !=4:
                    try:
                        response = Globals.getGFresponse("Will you marry me? *proposes* \n%s: YES!"%(gfval["name"]), ctx.author)
                    except:
                        response = next(x for x in gftypes if x["typename"] == gfval["type"])["proposeresponse"].format(ctx.author.display_name)
                    embed = discord.Embed(title = "You proposed to %s!"%(gfval["name"]), color = ctx.author.color)
                    embed.add_field(name = "%s"%(gfval["name"]), value=response)
                    try:
                        embed.set_image(url = Globals.getGFimage(ctx.author, Globals.classifyGFEmotion(response)))
                    except:
                        pass
                    UserAchievements = mulah.find_one({"id":ctx.author.id},{"achievements"})["achievements"]
                    proposes = mulah.find_one({"id":ctx.author.id},{"proposes"})["proposes"]
                    proposes+=1
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"proposes":proposes}})

                    embed.add_field(name = "%s levelled up!"%(gfval["name"]), value = "Congratulaions! %s is now tier 4, She is now your fiance!"%(gfval["name"]))
                    embed.set_footer(text = "you have gained 1000 love points! congratulations!")
                    await ctx.channel.send(embed=embed)
                    lpval+=1000
                    gfval["tier"] =4
                    mulah.update_one({"id":ctx.author.id},{"$set":{"gf":gfval}})
                    mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})
                    Globals.RemoveFromInventory(ctx.author, "ring", 1)
                else:
                    await ctx.channel.send("%s is already your fiance."%(gfval["name"]))
            else:
                await ctx.channel.send("You need a ring to propose. this is basic shit, man. come on.")

        else:
            await ctx.channel.send('You dont have enough Love points for that! come on bro, its gonna be weird if you move too quickly!')


























    @gf.command()
    @hasGirlfriend()
    async def date(self,ctx):
        global restaurants
        global backgrounds
        global datetalkmap
        alphlist = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
        gfval = mulah.find_one({"id":ctx.author.id}, {"gf"})["gf"]
        lpval = mulah.find_one({"id":ctx.author.id}, {"lp"})["lp"]
        walletval = mulah.find_one({"id":ctx.author.id}, {"money"})["money"]
        dates = mulah.find_one({"id":ctx.author.id}, {"dates"})["dates"]
        choice = random.choice(["invite"])
        typemap = next(x for x in datetalkmap if x["typename"] == gfval["type"])


        if choice == "invite":
            count = 0
            emptydict = {}
            reactions = []
            finalstring = ""
            for x in restaurants:
                emptydict[alphlist[count]]=x["name"]
                reactions.append(alphlist[count])
                finalstring+="%s| %s\n"%(alphlist[count], x["name"])
                count+=1
                
            try:
                invitation = Globals.getGFresponse("Im taking you out to eat!", ctx.author)
            except:
                random.choice(typemap["invite"]).format(author = ctx.author.display_name)
            embed = discord.Embed(title = "%s:"%(gfval["name"]), description = invitation, color = ctx.author.color)
            embed.add_field(name = "Where do you take her?", value = finalstring)

            try:
                embed.set_image(url = Globals.getGFimage(ctx.author, Globals.classifyGFEmotion(invitation)))
            except:
                pass
            editthis = await ctx.channel.send(embed=embed)
            for x in reactions:
                await editthis.add_reaction(x)

            def check(reaction, user):
                return user==ctx.author and str(reaction.emoji) in reactions and reaction.message==editthis
            confirm = await self.client.wait_for('reaction_add', check=check)
            if confirm:
                rawreaction = str(confirm[0])
                choice2=1
                if choice2==1:
                    restaurant = next(x for x in restaurants if x["name"] == emptydict[rawreaction])
                    menu = []
                    for x in restaurant["menu"]:
                        menu.append(x)
                    order = random.choice(typemap["whattoeat"])
                    gforder = random.choice(menu)
                    try:
                        order = order.format(order = gforder)
                    except:
                        try:
                            order = order.format(order=gforder,author = ctx.author.display_name)
                        except:
                            pass

                    count = 0
                    emptydict = {}
                    reactions = []
                    finalstring = ""
                    for x in restaurant["menu"]:
                        emptydict[alphlist[count]]=x
                        reactions.append(alphlist[count])
                        finalstring+="%s| %s-$%s\n"%(alphlist[count], x, restaurant["menu"][x])
                        count+=1
                    embed = discord.Embed(title = "%s:"%(gfval["name"]), description = order, color = ctx.author.color)
                    embed.set_footer(text = "Use the 🚪 to order!")
                    embed.add_field(name = "Menu!", value = finalstring)
                    try:
                        backgroundict = next(a for a in backgrounds if a["name"] == restaurant["background"])
                        asset = requests.get(gfval[restaurant["img"]])
                        data = BytesIO(asset.content)
                        foreground = Image.open(data)
                        background = Image.open(restaurant["background"])
                        foreground = foreground.resize(backgroundict["size"])
                        try:
                            background.paste(foreground, backgroundict["paste"], foreground)
                        except:
                            background.paste(foreground, backgroundict["paste"])

                        background.save("finalgf.png")
                        file = discord.File("finalgf.png")
                        embed.set_image(url = "attachment://finalgf.png") 
                    except:
                        try:
                            embed.set_image(url = gfval["image"])
                        except: 
                            pass                        
                    await editthis.clear_reactions()
                    await editthis.delete()
                    try:
                        editthis = await ctx.channel.send(embed=embed,file = file)
                    except:
                        editthis = await ctx.channel.send(embed=embed)
                    reactions.append("🚪")
                    for x in reactions:
                        await editthis.add_reaction(x)
                    userreact = []
                    leave = False
                    while leave ==False:
                        def check2(reaction,user):
                            return user==ctx.author and str(reaction.emoji) in reactions and reaction.message==editthis
                        confirm2 = await self.client.wait_for('reaction_add', check=check2)
                        if confirm2:  
                            if str(confirm2[0])=="🚪":
                                leave=True
                                break
                            else:
                                userreact.append(str(confirm2[0]))
                                pass


                            
                    embed = discord.Embed(title = "%s:"%(gfval["name"]), description = "Itadakimasu!", color = ctx.author.color)
                    try:
                        backgroundict = next(a for a in backgrounds if a["name"] == restaurant["background"])
                        asset = requests.get(gfval[restaurant["img"]])
                        data = BytesIO(asset.content)
                        foreground = Image.open(data)
                        background = Image.open(restaurant["background"])
                        foreground = foreground.resize(backgroundict["size"])
                        try:
                            background.paste(foreground, backgroundict["paste"], foreground)
                        except:
                            background.paste(foreground, backgroundict["paste"])

                        background.save("finalgf.png")
                        file = discord.File("finalgf.png")
                        embed.set_image(url = "attachment://finalgf.png") 
                    except:
                        try:
                            embed.set_image(url = gfval["image"])
                        except:
                            pass                      
                    embed.set_footer(text = "Are you done eating? use 🚪 to leave!")  
                    await editthis.clear_reactions()
                    await editthis.delete()
                    try:
                        editthis = await ctx.channel.send(embed=embed,file = file)    
                    except:
                        editthis = await ctx.channel.send(embed=embed)
                    await editthis.add_reaction("🚪")    
                    def check3(reaction,user):
                        return user==ctx.author and str(reaction.emoji)== "🚪" and reaction.message ==editthis
                    confirm3 = await self.client.wait_for('reaction_add', check=check3)
                    if confirm3:
                        bill = 0
                        valuestring = ""
                        for x in userreact:
                            bill+= restaurant["menu"][emptydict[x]] 
                            valuestring+= "\n%s"%(emptydict[x])
                        bill+= restaurant["menu"][gforder]
                        embed = discord.Embed(title = "Waiter:", description = "Your bill is $%s!"%(bill), color = ctx.author.color)
                        embed.add_field(name = "You ordered:", value = valuestring)
                        embed.add_field(name = "%s ordered:"%(gfval["name"]), value = gforder)
                        finalfile = discord.File(restaurant["waiter"])
                        filename= restaurant["waiter"]
                        stringfile = f"attachment://{filename}"
                        embed.set_image(url=stringfile)
                        if walletval>=bill:
                            walletval-=bill
                            mulah.update_one({"id":ctx.author.id}, {"$set":{"money":walletval}})
                            embed.set_footer(text = "your balance is now $%s\n You have gained 25 love points!"%(walletval))

                            dates+=1
                            mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":25}})
                            mulah.update_one({"id":ctx.author.id}, {"$set":{"dates":dates}})
                            await editthis.clear_reactions()
                            await editthis.delete()
                            editthis = await ctx.channel.send(embed=embed, file=finalfile)
                            Globals.AchievementEmbed("First Date!")
                        else:
                            embed.description="Im sorry, You dont have enough money"
                            await ctx.channel.send(embed=embed, file=finalfile)
                            embed = discord.Embed(title = "%s"%(gfval["name"]), description = "Seriously, %s?"%(ctx.author.display_name), color = discord.Color.red())
                            try:
                                embed.set_image(url=gfval["dissapointed"])   
                            except:
                                pass
                            embed.set_footer(text="you have lost 10 love points")
                            mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":-10}})
                      
                            await ctx.channel.send(embed=embed)    
                        data = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]    
                        data["dates"]+=1
                        mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":data}})

                    


        if choice == "react":
            embed = discord.Embed(title = "%s:"%(gfval["name"]), description = random.choice(typemap["react"]), color = ctx.author.color)
            try:
                embed.set_image(url = gfval["image"])
            except:
                pass
            editthis = await ctx.channel.send(embed=embed)






















    @gf.command()
    @hasGirlfriend()
    @Globals.hasItem(itemToCheckFor="movieticket")
    async def movies(self,ctx):
        global typegenrepraise
        global typeconplaint
        global typepraise
        global gftypes
        invar = mulah.find_one({"id":ctx.author.id},{"inv"})   
        inval = invar["inv"]     
        ticketcheck = next((item for item in inval if item["name"] == "movieticket" and "parts" not in item.keys()), None)
        if ticketcheck is not None:
            moviesDB = IMDb()
            gfvar = mulah.find_one({"id":ctx.author.id},{"gf"})
            gfval = gfvar["gf"]
            lpvar = mulah.find_one({"id":ctx.author.id},{"lp"})
            lpval = lpvar["lp"]
            top = moviesDB.get_top250_movies()
            randomten = random.sample(top,10)
            alphabet = string.ascii_lowercase
            alphlist = list(alphabet)
            emptydict = {}
            count = 0
            finalstring = ""
            movielist = []
            for x in randomten:
                movielist.append(str(x))
                emptydict[alphlist[count]] = str(x)
                finalstring+= alphlist[count] + "| " + "%s\n"%(x)
                count+=1


            embed = discord.Embed(title = "Choose a Movie!", description = finalstring, color = ctx.author.color)
            await ctx.channel.send(embed=embed)

            def check(m):
                return m.author==ctx.author and m.channel==ctx.channel
            
            try:
                msg = await self.client.wait_for('message', check=check,timeout = 30)
                if emptydict[msg.content] in movielist:
                    moviesearch = moviesDB.search_movie(emptydict[msg.content])
                    id = moviesearch[0].movieID

                    moviefind = moviesDB.get_movie(id)
                    genre = moviefind["genres"]
                    genre = [x.lower() for x in genre]
                    gfsat = 23
                    dialogue = ""
                    dialogue+=next(item for item in gftypes if item["typename"] == gfval["type"])["movieresponse"]
                    if gfval["dislikes"] in genre:
                        dialogue+="typeconplaint"
                        gfsat*=85/100
                    if gfval["favorite genre"] in genre:
                        try:
                            dialogue += next(item for item in typegenrepraise if item["typename"] == gfval["type"])[gfval["favorite genre"]]
                        except:
                            pass
                        gfsat*=115/100
                    if gfval["likes"] == "movies":
                        dialogue += next(item for item in typepraise if item["typename"] == gfval["type"])["movies"]
                        gfsat+=115/100


                    dialogue = Globals.getGFresponse("*watches %s with you"%(emptydict[msg.content]), ctx.author)
                    embed = discord.Embed(title = "You watched %s with %s"%(emptydict[msg.content],gfval["name"]), color = ctx.author.color)
                    embed.add_field(name = "%s:"%(gfval["name"]), value = dialogue)
                    try:
                        embed.set_image(url=Globals.getGFimage(ctx.author,Globals.classifyGFEmotion(gfResponse)))
                    except:
                        pass
                    lpval+=math.floor(gfsat)
                    embed.set_footer(text="You gained %s Love points."%(math.floor(gfsat)))
                    await ctx.channel.send(embed=embed)
                    ticketcheck["amount"]-=1
                    if ticketcheck["amount"]==0:
                        inval.remove(ticketcheck)

                    mulah.update_one({"id":ctx.author.id},{"$set":{"inv":inval}})
                    mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})
                    data = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]    
                    data["movies"]+=1
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":data}})

                else:
                    pass
            except asyncio.TimeoutError:
                await ctx.channel.send("You took too long! I guess we arent doing this.")

        else:
            gfvar = mulah.find_one({"id":ctx.author.id},{"gf"})
            gfval = gfvar["gf"]     
            embed = discord.Embed(title = "%s"%(gfval["name"]), description = "you need a movieticket   , %s"%(ctx.author.display_name), color = ctx.author.color)
            try:
                embed.set_image(url = gfval["dissapointed"])
            except:
                try:
                    embed.set_image(url = gfval["image"])
                except:
                    pass
            await ctx.channel.send(embed=embed)


    @commands.command()
    @commands.is_owner()
    async def removegf(self,ctx,p1:discord.Member):
        if str(ctx.author) == "SentientPlatypus#1332":
            mulah.update_one({"id":p1.id},{"$set":{"gf":0}})
            mulah.update_one({"id":p1.id},{"$set":{"lp":0}})
            await ctx.channel.send("Ok creator senpai! I removed %s gf!"%(p1.display_name))



















    @gf.command()
    @Globals.hasItem("phone")
    @hasGirlfriend()
    async def text(self,ctx):
        gf = mulah.find_one({"id":ctx.author.id}, {"gf"})["gf"]
        embed = discord.Embed(title="Text %s"%(gf["name"]), description="Your next message in this channel will be sent to %s"%(gf["name"]), color=discord.Color.blue())
        await ctx.channel.send(embed=embed)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        textContent = await self.client.wait_for('message', check=check, timeout= 120)
        textContent = textContent.content

        lpIncrease = 0
        imageToSend="image"
        classification = Globals.classifyGFText(textContent)
        classification = classification.lower()
        if classification=="good":
            lpIncrease+=15
            imageToSend = "image"
        if classification=="decent":
            lpIncrease+=10
            imageToSend = "image"
        if classification=="bad":
            lpIncrease+=3
            imageToSend = random.choice(["angry","sad", "dissapointed"])
        
        embed = discord.Embed(title = "You texted %s"%(gf["name"]), color = discord.Color.blue())
        embed.add_field(name=f"{ctx.author.display_name}:", value=f"{textContent}", inline=False)
        
        gfResponse = Globals.getGFresponse(textContent, ctx.author)
        try:
            embed.set_image(url=Globals.getGFimage(ctx.author,Globals.classifyGFEmotion(gfResponse)))
        except:
            pass
        embed.add_field(name="%s:"%(gf["name"]), value=gfResponse, inline=False)

        mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":lpIncrease}})

        embed.set_footer(text=f"You have gained {lpIncrease} love points!")

        await ctx.channel.send(embed=embed)




        







    @gf.command()
    @hasGirlfriend()
    @Globals.hasItem("pc")
    async def gaming(self, ctx):
        global gameitems
        global gamewords
        global gfgamingresponse
        global typegenrepraise
        global typeconplaint
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})
        gfval = gfvar["gf"]
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
        if finalstring !="":
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
                                        pass
                                        
                                    else:
                                        skillint =4

                                    gameskill = mulah.find_one({"id":ctx.author.id}, {"gameskill"})
                                    try:
                                        skilldict = gameskill["gameskill"]
                                        try:
                                            skilldict[newdict[msg.content]] +=skillint
                                        except:
                                            skilldict[newdict[msg.content]] = 0
                                            skilldict[newdict[msg.content]]+=skillint
                                    except:
                                        skilldict = {}
                                        skilldict[newdict[msg.content]] =0
                                        skilldict[newdict[msg.content]] +=skillint
                                    responsedict = next(item for item in gfgamingresponse if item["typename"] == gfval["type"])
                                    
                                    gflikesgaming = next(item for item in typepraise if item["typename"] == gfval["type"])
                                    gfgenrebad = next(item for item in typeconplaint if item["typename"] == gfval["type"])
                                    gfgenregood = next(item for item in typegenrepraise if item["typename"] == gfval["type"])
                                    gamedict = next(item for item in gameitems if item["name"] == newdict[msg.content])
                                    gfsat = gamedict["lpincrease"]*(skilldict[newdict[msg.content]]/100)
                                    try:
                                        quality = "*plays %s with you but does "%(gamedict["name"])
                                        if skilldict[newdict[msg.content]]<35:
                                            quality+="poorly"
                                        elif 35<=skilldict[newdict[msg.content]]<45:
                                            quality+="decent"
                                        elif 45<=skilldict[newdict[msg.content]]:
                                            quality+="really good"
                                        finalstring = Globals.getGFresponse(quality, ctx.author)
                                            
                                    except:
                                        finalstring = ""
                                        if skilldict[newdict[msg.content]]<35:
                                            finalstring+="%s"%(responsedict["poor"])
                                        elif 35<=skilldict[newdict[msg.content]]<45:
                                            finalstring+="%s"%(responsedict["medium"])
                                        elif 45<=skilldict[newdict[msg.content]]:
                                            finalstring+="%s"%(responsedict["good"])

                                        dislikes = False
                                        if gfval["likes"] == "gaming":
                                            finalstring+="%s"%(gflikesgaming["gaming"])
                                            gfsat= gfsat*(115/100)
                                        if gfval["dislikes"] in gamedict["genre"]:
                                            dislikes = True
                                            finalstring+="%s"%(gfgenrebad[gfval["dislikes"]])
                                            gfsat= gfsat*(85/100)
                                        elif gfval["favorite genre"] in gamedict["genre"]:
                                            finalstring+="%s"%(gfgenregood[gfval["favorite genre"]])
                                            gfsat= gfsat*(115/100)


                                        
                                    embed = discord.Embed(title = "You played %s with %s!"%(newdict[msg.content], gfval["name"]), color = ctx.author.color)

                                    embed.add_field(name = "%s:"%(gfval["name"]), value = finalstring)
                                    try:
                                        embed.set_image(url=Globals.getGFimage(ctx.author,Globals.classifyGFEmotion(finalstring)))
                                    except:
                                        pass
                                    embed.set_footer(text = "You have gained %g love points"%(gfsat))
                                    try:
                                        if dislikes == True:
                                            embed.set_image(url = gfval["dissapointed"])
                                        else:
                                            embed.set_image(url = gfval["image"])
                                    except:
                                        try:
                                            embed.set_image(url = gfval["image"])
                                        except:
                                            pass
                                    lp = mulah.find_one({"id":ctx.author.id}, {"lp"})
                                    lpval = lp["lp"]
                                    lpval+=gfsat
                                    mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":lpval}})

                                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gameskill":skilldict}})
                                    data = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]    
                                    data["games"]+=1
                                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":data}})
                                    await ctx.channel.send(embed=embed)
                                else:
                                    await ctx.channel.send("Your PC does not meet the requirements. You should look at system requirements before installing a game!")
                                    
                            else:
                                await ctx.channel.send("You were supposed to type a letter.")


                                


                                ##code
                        except asyncio.TimeoutError:
                            await ctx.channel.send("You took too long! i guess we arent doing this.")
                    else:
                        try:
                            finalstring = Globals.getGFresponse(quality, ctx.author)
                        except:
                            finalstring = "you dont have any games on this pc, %s"%(ctx.author.display_name)
                        embed = discord.Embed(title = "%s"%(gfval["name"]), description = finalstring, color = ctx.author.color)
                        try:
                            embed.set_image(url = gfval["dissapointed"])
                        except:
                            try:
                                embed.set_image(url = gfval["image"])
                            except:
                                pass
                        await ctx.channel.send(embed=embed)
                else:
                    await ctx.channel.send("Use the lowercase letter associated with the game name.")
        
            except asyncio.TimeoutError:
                await ctx.channel.send("You took to long! i guess we arent doing this.")
        else:
            embed = discord.Embed(title = "%s"%(gfval["name"]), description = "you need a pc, %s"%(ctx.author.display_name), color = ctx.author.color)
            try:
                embed.set_image(url = gfval["dissapointed"])
            except:
                try:
                    embed.set_image(url = gfval["image"])
                except:
                    pass
            await ctx.channel.send(embed=embed)


















    @gf.command()
    @hasGirlfriend()
    @commands.is_nsfw()
    async def talk(self, ctx):
        gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})["gf"]
        gfname = gfvar["name"]
        gfdata = mulah.find_one({"id":ctx.author.id}, {"gfdata"})["gfdata"]
        model = Globals.getModel(ctx.author.id)
        backgroundInfo = Globals.chat.getprompt(ctx.author)
        backgroundInfo += f"Right now, {gfname} is about to have a conversation with {ctx.author.display_name}"
        newChat = Globals.chat(backgroundInfo, ctx.author.display_name, gfvar["name"], model)
        openstatement = newChat.ask("Hi there!")

        embed = discord.Embed(title = "%s:"%(gfvar["name"]), description= openstatement, color = discord.Color.red())
        embed.set_footer(icon_url=ctx.author.avatar_url, text="type what you want to do. you can literally do anything. just dont do something irrelevant\n type \"end interaction\" to end")
        try:
            embed.set_image(url=Globals.getGFimage(ctx.author, Globals.classifyGFEmotion(openstatement, False)))
        except:
            pass
        toEdit = await ctx.channel.send(embed=embed)

        def check(m):
            return m.author==ctx.author and m.channel == ctx.channel
        
        done = False
        nsfwCounter = 0
        ended = False
        lpcounted = 0
        while not done:
            embed = discord.Embed(title = "%s:"%(gfvar["name"]),color = discord.Color.red())
            embed.set_footer(icon_url=ctx.author.avatar_url, text="type what you want to do. you can literally do anything. just dont do something irrelevantn type \"end interaction\" to end")

            message = await self.client.wait_for('message', check=check, timeout=100)
            if len(message.content) >200:
                raise tooLong(ctx.author)
            if message.content.lower() == "end interaction":
                ended = True
                break
            response = newChat.ask(message.content)
            embed.description = response
            try:
                embed.set_image(url=Globals.getGFimage(ctx.author, Globals.classifyGFEmotion(response)))
            except: 
                pass
            

            actionAnalysis = Globals.classifyGFTalking(message.content).lower()
            print(actionAnalysis)
            if actionAnalysis == "nsfw":
                nsfwCounter += 1
                embed.add_field(name="NSFW warning.", value="This sounds like NSFW content. Keep it up and I will terminate this command.")

            await toEdit.delete()
            await message.delete()
            toEdit = await ctx.channel.send(embed=embed)
            if nsfwCounter >=3:
                break
            if actionAnalysis == "kiss":
                gfdata["kisses"]+=1
                mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":gfdata}})
                mulah.update_one({"id":ctx.author.id}, {"$inc":{"kisses":1}})
                mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":40}})
                lpcounted += 40
            if actionAnalysis == "hug":
                gfdata["hugs"]+=1
                mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":gfdata}})  
                mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":25}})
                lpcounted += 25        
            if actionAnalysis == "over":
                done = True
        if nsfwCounter >=3:
            embed = discord.Embed(title = "NSFW penalty.", description= "You were not supposed to do that.", color = discord.Color.red())
            embed.set_footer(text="You have been penalized $100 and 50 love points")
            mulah.update_one({"id":ctx.author.id}, {"$inc":{"money":-100}})
            mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":-50}})
            return await ctx.channel.send(embed=embed)

        if ended:
            embed = discord.Embed(title = "Interaction ended", color = discord.Color.red())
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f"You have gained {lpcounted} love points!\n complete the talking to get more lp")
            return await ctx.channel.send(embed=embed)
        lpcounted += 50    
        mulah.update_one({"id":ctx.author.id}, {"$inc":{"lp":50}})
        embed = discord.Embed(title = "Talking complete", color=discord.Color.green())
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"You have gained {lpcounted} love points!")
        await ctx.channel.send(embed=embed)

























    @commands.group(invoke_without_command=True)
    async def gfinteract(self, ctx, pg:int=None):
        gfinteractlist = [
            {"name": "📱text", "lpincrease": 15, "lprequired": 0, "itemrequired": "phone","category":"texting", "desc": "Text your girlfriend! you need a phone for this."},
            {"name": "🎥movies", "lpincrease": 23, "lprequired":0, "itemrequired": "movieticket","category":"gaming","desc": "watch a movie with your girlfriend!"},
            {"name": "📺netflix", "lpincrease": 10, "lprequired":0, "itemrequired": "netflixsub, watchlist","category":"relax", "desc": "watch netflix with your girlfriend"},
            {"name": "🍴date", "lpincrease": 20, "lprequired":0, "itemrequired": None,"category":"relax", "desc": "go on a date with your girlfriend!"},
            {"name": "🎮gaming", "lpincrease": 25, "lprequired": 0, "itemrequired": "PC","category":"gaming", "desc":"Play Minecraft With your girlfriend! You need a laptop for this."},
            {"name": "💋kiss", "lpincrease":40, "lprequired" : 200, "itemrequired": None,"category":None, "desc": "Kiss your girlfriend!"},
            {"name": "🧑‍🤝‍🧑holdhand", "lpincrease":15, "lprequired": 130, "itemrequired": None,"category":None,"desc": "early game move"},
            {"name": "🤗hug", "lpincrease":25, "lprequired": 150, "itemrequired": None,"category":None,"desc": "Hug your girlfriend! A great way to bond."},
            {"name": "❤️boink", "lpincrease": 100, "lprequired": 800, "itemrequired": None,"category":None, "desc":"boink your girlfriend! Late game move."},
            {"name": "💍propose", "lpincrease": 1000, "lprequired": 1600, "itemrequired": "ring","category":None, "desc": "Finally. You have the love of your life. Go live happily ever after."}]
        if pg is None:
            embed = discord.Embed(title = "Interact with Your Girlfriend!", description = "Use `^gf <command>`", color = ctx.author.color)
            for x in range(len(gfinteractlist)):
                value = gfinteractlist[x]
                embed.add_field(name = "%s➡️ +lp:%s"%(value["name"], value["lpincrease"]), value = "*love point requirement: %s \n Item requirement: %s \n Description:%s "%(value["lprequired"],value["itemrequired"],value["desc"], ), inline = False)
            embed.set_footer(text ="page 1")
            await ctx.channel.send(embed=embed)



















    @commands.command()
    @hasGirlfriend()
    async def breakup(self,ctx, name=None):
        gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})
        if name is None:
            if gfvar is not  None or gfvar["gf"] != 0:
                string = "are you sure you want to breakup with %s? You will lose all love points. type `^breakup yes` if you do."%(gfvar["gf"]["name"])
                await ctx.channel.send(string)
            else:
                await ctx.channel.send("You dont even have a girlfriend.")
        elif name == "yes".casefold(): 
            gfname = mulah.find_one({"id":ctx.author.id}, {"gf"})
            gfname = gfname["gf"]
            mulah.update_one({"id":ctx.author.id},{"$set":{"lp":0}})
            mulah.update_one({"id":ctx.author.id}, {"$set":{"gf": 0}})
            embed = discord.Embed(title = "You have broken up with %s"%(gfname["name"]))
            UserAchievements = mulah.find_one({"id":ctx.author.id},{"achievements"})["achievements"]
            breakups = mulah.find_one({"id":ctx.author.id},{"breakups"})["breakups"]
            breakups+=1
            mulah.update_one({"id":ctx.author.id}, {"$set":{"breakups":breakups}})

            await ctx.channel.send(embed = embed)            




















    @commands.command()
    @hasGirlfriend()
    async def gfstats(self, ctx, p1:discord.Member=None):
        global emotionlist
        if p1 is None:
            p1 = ctx.author
        try:
            gfvar = mulah.find_one({"id":p1.id}, {"gf"})
            gfdict = gfvar["gf"]

            try:
                lpvar = mulah.find_one({"id": p1.id}, {"lp"})
                lpval = math.floor(lpvar["lp"])

                embed = discord.Embed(title = "%s's stats!"%(gfdict["name"]), color = p1.color)
                for x in gfdict.keys():
                    if x not in emotionlist:
                        embed.add_field(name = "%s"%(x), value = gfdict[x])



                embed.add_field(name = "❤️Love Points", value = "%s"%(lpval))
                try:
                    if gfdict["image"].startswith("http"):
                        embed.set_image(url = gfdict["image"])
                except:
                    pass
                await ctx.channel.send(embed=embed)
                        
            except:
                await ctx.channel.send("Get a Gf.")
                
        except:
            await ctx.channel.send("you/they dont have a girlfriend")
























    @commands.command()
    async def getgf(self, ctx):
        global gftypes, typeconplaint
        try:
            gfvar = mulah.find_one({"id": ctx.author.id}, {"gf"})
            gfvarlist = gfvar["gf"]
            if gfvarlist == 0:
                embed = discord.Embed(title = "Type your Girlfriend's name!", color = ctx.author.color)
                await ctx.channel.send(embed = embed)
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    gfname = await self.client.wait_for('message', check = check, timeout = 30.0)
                    newdictionary = {"name": "%s"%(gfname.content)}
                    types = [x["typename"] for x in gftypes]
                    GfType = await Globals.ChoiceEmbed(self, ctx, types, "What is %s's type?"%(newdictionary["name"]))
                    GfType = GfType[0]
                    newdictionary["type"] = GfType
                    favoritesub = ["language", "Math", "Computer Science", "biology", "chemistry", "Physics", "art", "gender studies", "business", "political sciences"]

                    glikes = ["horror", "adventure", "creativity", "strategy", "thriller", "comedy", "animation", "action", "romance", "drama"]
                    
                    likes = ["food", "texting", "gaming", "social media", "relaxing", "movies"]
                    EmbedChoices = await Globals.ChoiceEmbed(self, ctx, likes, "What does %s like?"%(newdictionary["name"]))
                    randlikes = EmbedChoices[0]
                    randsub = await Globals.ChoiceEmbed(self, ctx, favoritesub, "What is %s's Favorite Subject?"%(newdictionary["name"]))
                    randsub = randsub[0]
                    genre = await Globals.ChoiceEmbed(self, ctx, glikes, "What is %s's Favorite Genre?"%(newdictionary["name"]))
                    genre = genre[0]
                    randdislikes = await Globals.ChoiceEmbed(self, ctx, glikes, "What is %s's Least favorite genre?"%(newdictionary["name"]))
                    randdislikes = randdislikes[0]

                    if randdislikes == genre:
                        while randdislikes==genre:
                            randdislikes = random.choice(glikes)
                    
                    newdictionary["likes"] = randlikes
                    newdictionary["favorite subject"] = randsub
                    newdictionary["dislikes"] = randdislikes
                    newdictionary["favorite genre"] = genre
                    newdictionary["tier"] = 1
                    
                    embed = discord.Embed(title = "You are now dating %s!"%(newdictionary["name"]), description = "Here is her profile! you can access this at anytime using `^gfstats`", color = ctx.author.color)
                    for x in newdictionary.keys():
                        embed.add_field(name = "%s:"%(x), value = newdictionary[x])
                    await ctx.channel.send(embed = embed)  
                    relationships = mulah.find_one({"id":ctx.author.id}, {"relationships"})["relationships"]
                    relationships+=1
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"relationships":relationships}})
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gf":newdictionary}})
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":100}})
                    datadict ={
                            "kisses":0,
                            "boinks":0,
                            "dates":0,
                            "hugs":0,
                            "games":0,
                            "text":0,
                            "netflix":0,
                            "movies":0,
                            "start":date.today().strftime("%B %d, %Y")
                        }
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gfdata":datadict}})
            
                except asyncio.TimeoutError:
                    await ctx.channel.send("You took to long to respond! I guess we arent doing this.")
            else:
                await ctx.channel.send("You already have a girlfriend! Infidelity is disgusting. Shame on you.")
        except:
            mulah.update_one({"id": ctx.author.id}, {"$set":{"gf":0}})
            await ctx.channel.send("I have set up your dating profile! Try `^getgf` again!")
            return 
        number = random.randint(1,500)
        try:
            gfval = mulah.find_one({"id":ctx.author.id}, {"gf"})["gf"]
            lpval = mulah.find_one({"id":ctx.author.id}, {"lp"})["lp"]
            if number == 1:
                global talkmap
                alphlist = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
                end = False
                actionlist = ["gaming", "movies", "netflix", "comfortgf1", "attentionwant", "sadgf", "happygf"]
                action = random.choice(actionlist)
                end = False    
                talklistdict = next(x for x in talkmap if x[0]["typename"] == gfval["type"])
                while end == False:
                    if action == "accept invitation":
                        cmd = self.client.get_command("gf "+"boink")
                        await cmd(ctx)
                        break
                    if action == "kiss":
                        kisses = mulah.find_one({"id":ctx.author.id},{"kisses"})["kisses"]
                        kisses+=1
                        mulah.update_one({"id":ctx.author.id},{"$set":{"kisses":kisses}})
                    if action in ["comfortgf", "yeah sure what?"]:
                        action = random.choice(["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"])
                    talkdict = next(x for x in talklistdict if x["action"] == str(action))
                    penultres = random.choice(talkdict["response"])
                    if re.search("\{0\}", penultres):
                        finalstring = penultres.format(ctx.author.display_name)
                    else:
                        finalstring = penultres

                    embed = discord.Embed(title = "%s:"%(gfval["name"]), description = finalstring, color = ctx.author.color)
                    mapto = talkdict["map"]
                    count = 0
                    emptydict = {}
                    valuestrint = ""
                    reactions = []
                    for x in mapto:
                        valuestrint+="%s| %s\n"%(alphlist[count], x)
                        emptydict[alphlist[count]] = x
                        reactions.append(alphlist[count])
                        count+=1
                    embed.add_field(name = "what will you do?", value = valuestrint)
                    try:
                        try:
                            try:
                                backgroundict = next(a for a in backgrounds if a["name"] == talkdict["background"])
                                rmbg.remove_background_from_img_url(img_url=gfval[talkdict["img"]], new_file_name="GFTALK.png")
                                foreground = Image.open("GFTALK.png")
                                background = Image.open(backgroundict["name"])
                                foreground = foreground.resize(backgroundict["size"])
                                background.paste(foreground, backgroundict["paste"], foreground)
                                background.save("finalgf.png")
                                file = discord.File("finalgf.png")
                                embed.set_image(url = "attachment://finalgf.png")
                            except:
                                backgroundict = next(a for a in backgrounds if a["name"] == talkdict["background"])
                                asset = requests.get(gfval[talkdict["img"]])
                                data = BytesIO(asset.content)
                                foreground = Image.open(data)
                                background = Image.open(talkdict["background"])
                                foreground = foreground.resize(backgroundict["size"])
                                try:
                                    background.paste(foreground, backgroundict["paste"], foreground)
                                except:
                                    background.paste(foreground, backgroundict["paste"])

                                background.save("finalgf.png")
                                file = discord.File("finalgf.png")
                                embed.set_image(url = "attachment://finalgf.png")                        
                        except:
                            embed.set_image(url = gfval[talkdict["img"]])
                    except:
                        try:
                            embed.set_image(url = gfval["image"])
                        except:
                            pass

                    try:
                        await editthis.delete()
                        editthis = await ctx.channel.send(embed=embed, file = file)
                    except:
                        try:
                            editthis = await ctx.channel.send(embed=embed, file = file)
                        except:
                            editthis = await ctx.channel.send(embed=embed)
                    for x in reactions:
                        await editthis.add_reaction(x)
                    if action == "leave":
                        end = True
                        break

                    def check(reaction,user):
                        return user==ctx.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'] and reaction.message == editthis  
                    try:
                        confirm = await self.client.wait_for('reaction_add', check=check, timeout = 20)
                        if confirm:
                            action = emptydict[str(confirm[0])]
                            if action in ["gaming", "movies", "netflix", "kiss", "hug"]:
                                cmd = self.client.get_command("gf "+action)
                                await cmd(ctx)
                                break
                    except asyncio.TimeoutError:
                        gftimeout = [
                            {"typename":"Tsundere", "img":"angry", "response": "Fine if you wanna be like that!", "lpdecrease":30},
                            {"typename":"Sweet", "img":"sad", "response": "are you just going to leave me hanging like that? I.. its alright though", "lpdecrease":10},
                            {"typename":"Dandere", "img":"sad", "response": ".. alright", "lpdecrease":10},
                            {"typename":"Kuudere", "img":"sad", "response": ".. alright", "lpdecrease":20},
                            {"typename":"Yandere", "img":"dissapointed", "response": "What could you possibly be doing thats more important than me?", "lpdecrease":60},
                            {"typename":"Sadodere", "img":"angry", "response": "Hmph. Thats fine if you dont want to.", "lpdecrease":50},
                            {"typename":"Kamidere", "img":"dissapointed", "response": "I understand that you are busy, but is it really too much?", "lpdecrease":30},

                            
                        ]
                        timeoutdict = next(x for x in gftimeout if x["typename"] == gfval["type"])
                        embed = discord.Embed(title = "%s:"%(gfval["name"]), description = timeoutdict["response"], color = ctx.author.color)
                        try:
                            embed.set_image(url = gfval[timeoutdict["img"]])
                        except:
                            try:    
                                embed.set_image(url = gfval["image"])
                            except:
                                pass
                        embed.set_footer(text = "You heartless scum! you lost %s Love Points!"%(timeoutdict["lpdecrease"]))
                        await editthis.delete()
                        editthis = await ctx.channel.send(embed=embed)
                        lpval-=timeoutdict["lpdecrease"]
                        mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":lpval}})
                        break
            

        except:
            pass

def setup(client):
    client.add_cog(DatingSim(client))