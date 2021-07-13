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
cluster = MongoClient('mongodb+srv://SCPT:Geneavianina@scptsunderedatabase.fp8en.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mulah = cluster["discord"]["mulah"]




gfnamelist = []
class currencysys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_completion(self,ctx):
        global achievements
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

        

        

        





    @commands.Cog.listener()
    async def on_message(self, ctx):
        def dbcheck(user):
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
                {"name":"relationships", "value":0, "conditional":"gf", "ModifiedVal":1}
            ]
            for x in DatabaseKeys:
                try:
                    value = mulah.find_one({"id":ctx.author.id},{x["name"]})[x["name"]]
                except:
                    if "conditional" in x.keys():
                        try:
                            value = mulah.find_one({"id":ctx.author.id},{x["conditional"]})[x["conditional"]]
                            if value != next(z for z in DatabaseKeys if z["name"]==x["conditional"])["value"]:
                                print("updated %s's %s"%(ctx.author.display_name, x["name"]))
                                mulah.update_one({"id":ctx.author.id}, {"$set":{x["name"]:x["ModifiedVal"]}})
                        except:
                            print("updated %s's %s"%(ctx.author.display_name, x["name"]))
                            mulah.update_one({"id":ctx.author.id}, {"$set":{x["name"]:x["value"]}})                           
                    else:
                        print("updated %s's %s"%(ctx.author.display_name, x["name"]))
                        mulah.update_one({"id":ctx.author.id}, {"$set":{x["name"]:x["value"]}})
            
            
        if ctx.author == self.client.user:
            return
        dbcheck(ctx.author)


        

        if ctx.content.startswith("^"):
            print("it starts")
            return 
        number = random.randint(1,20)
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
                    print(action)
                    if action in ["comfortgf", "yeah sure what?"]:
                        action = random.choice(["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"])
                    print(action)
                    print(str(action))
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
                                print(backgrounds)
                                print(backgroundict)
                                print(backgroundict["name"])
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
                            print("nonono")
                            print(traceback.format_exc())
                            embed.set_image(url = gfval[talkdict["img"]])
                    except:
                        try:
                            embed.set_image(url = gfval["image"])
                        except:
                            print(traceback.format_exc())
                            print("cant get image smh")

                    try:
                        await editthis.delete()
                        editthis = await ctx.channel.send(embed=embed, file = file)
                    except:
                        editthis = await ctx.channel.send(embed=embed, file = file)
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
                            print("this worked. the action is %s"%(action))
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
            print("this didnt work")


    
    @commands.Cog.listener()
    async def on_ready(self):
        global achievementcheck
        def achievementcheck(user,achievement:str):
            global achievements
            try:
                value = mulah.find_one({"id":user.id}, {"achievements"})["achievements"]
                if achievement in value:
                    return "✅"
                else:
                    return "❌"
            except:
                return "❌"
        global achievementpercent
        def achievementpercent(achievement:str):
            count = 0
            achCount=0
            for x in mulah.find():
                count+=1
                try:
                    if achievement in x["achievements"]:
                        achCount+=1
                except:
                    pass
            return (achCount/count)*100
        global rmbg
        rmbg = RemoveBg("aAtMveyyqHxf3DVczpwrxPLN", "error.log")

        global emotionlist
        emotionlist = ["embarrassed", "horny","surprised","climax", "image", "bed", "angry", "fear", "sad", "dissapointed"]


        global backgrounds
        backgrounds = [
            {"name":"house.jpg", "paste":(378,167), "size":(377,467)},
            {"name":"nightsky.jpg", "paste":(60,82), "size":(195,279)},
            {"name":"macd.jpg", "paste":(72,6), "size":(204,310)},
        ]

        global worklists
        worklists = [
            {"name":"McDonalds worker", "salary":15, "req":None},
            {"name":"Gamer", "salary":150, "req": "must have over 1000 total gameskill"},
            {"name":"Business Man", "salary":160, "req":"must be at least level 15"},
            {"name":"Jeff bezos", "salary":1000000000, "req":"must be Creator Senpai"},
        ]


        global restaurants
        restaurants = [
            {"name":"mcdonalds", "menu":{"bigmac":6, "QuarterPounder":3, "Bacon Clubhouse Burger":4, "fillet-o-fish":3, "happy meal":4}, "background":"macd.jpg", "img":"image", "waiter":"http://pilerats.com/assets/Uploads/_resampled/SetWidth940-mcdonalds-japan-anime-ad.jpg"}
        ]

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

            {"name":"Death!", "desc":"Get a life bro.", "category":"finance"},
            {"name":"virgin", "desc":"Secret!", "category":"gaming"},
            {"name":"FloorGang", "desc":"Secret!", "category":"gaming"},
            {"name":"First PC!", "desc":"Create your first PC!", "category":"gaming"},
            {"name":"Linus Tech Tips", "desc":"Create a beefy Computer with at least 12000 power!", "category":"gaming"},
            {"name":"True Gamer", "desc":"Install 5 games on a single PC!", "category":"gaming"},
            
        ]

        global datetalkmap
        datetalkmap = [
            {"typename":"Tsundere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Dandere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Kuudere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Sadodere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Kamidere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Sweet", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, darling?"]},
            {"typename":"Yandere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
        ]


        global talkmap
        talkmap = [
            [
            {"typename":"Sweet", "action":"none","img":"image", "response":"see you, {0}! I love you!", "background":"house.jpg"},
            {"map":["sad", "scared", "happy", "angry", "horny"], "action":"Im not feeling that way","img":"image", "response":["Im sorry, how are you feeling right now?"], "background":"house.jpg"},
            {"map":["accept invitation"], "action":"horny","img":"embarrassed", "response":["ohh, thats what you were feeling. Thats ok, I can help you out with that ;)"], "background":"house.jpg"},
            {"map":["leave","invite her to go do something"], "action":"end","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["No, Im fine", "Im not feeling that way"], "action":"sad","img":"image", "response":["It seems like you are sad. is that right? Thats too bad! is there anything I can do?"], "background":"house.jpg"},
            {"map":["lie on lap","dont lie on lap"], "action":"No, Im fine","img":"image", "response":["I cant give much, but I will support you will all Ive got! come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["leave","lie on lap"], "action":"dont lie on lap","img":"image", "response":["come on, just for a little while? come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["end"], "action":"lie on lap","img":"image","response": ["Hey. I know you can do it. I love you so much. That will never change. \n*You are my sunshine, My only sunshine\n You make me happy when skies are gray!\n You'll never know, dear, how much I love you!\n please dont take my sunshine away!*\n Did you like my voice? I hope so! *smooch*"], "background":"house.jpg"},
            {"map":["hug","kiss","Im really thankful for you!", "Im not feeling that way"], "action":"happy","img":"image", "response":["Thats amazing! im so happy for you!"], "background":"house.jpg"},
            {"map":["hug", "kiss", "end"], "action":"Im really thankful for you!","img":"image", "response":["aww, I love you so much! of course Id support you!"], "background":"house.jpg"},
            {"map":["end","kiss","invite her to go do something"], "action":"hug","img":"image", "response":["hmmm? You want a hug? of course!! *sqeezes*"], "background":"house.jpg"},
            {"map":["end","invite her to go do something"], "action":"kiss","img":"image", "response":["*mwah* I'll see you around! I love you!"], "background":"house.jpg"},
            {"map":["kiss"], "action":"Im really thankful for you!","img":"image", "response":["hey. I care about you!! Its only normal.."], "background":"house.jpg"},
            {"map":["walk away","lie on lap", "Im not feeling that way"], "action":"angry","img":"image", "response":["Hey. Im not sure if you are in the mood, you seem mad, or annoyed, but wanna rest on my lap?"], "background":"house.jpg"},
            {"map":["go with her", "dont follow"], "action":"walk away","img":"image", "response":["Hey I know just the thing! Follow me!"], "background":"house.jpg"},
            {"map":["end"], "action":"dont follow","img":"image", "response":["all right. I understand, Ill give you some time. If you wanna talk to me about anything, Im always available to you!"], "background":"house.jpg"},
            {"map":["leave","look at stars"], "action":"go with her","img":"image", "response":["this is the night sky! It looks nice, right? You can relax here. I find it nice gazing at the stars"], "background":"nightsky.jpg"},
            {"map":["end"], "action":"leave","img":"image", "response":["Im always ready to talk if you need me. I love you! bye!"], "background":"house.jpg"},
            {"map":["end"], "action":"look at stars","img":"image", "response":["Its nice right? Ill leave you be for now."], "background":"nightsky.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scared","img":"image", "response":["It sounds like you are scared. I know you are strong. You are also smart! if you cant handle it on your own, find someone to help you! You shouldnt always try to do things on your own!"], "background":"house.jpg"},
        
            {"map":["comfortgf"], "action":"sadgf","img":"sad", "response":["{0}, im feeling really sad! I dont like this! do something!"], "background":"house.jpg"},
            {"map":["gaming", "movies", "netflix", "horny"], "action":"invite her to go do something","img":"angry", "response":["What do you want to do together? Im... im open to anything!"], "background":"house.jpg"},            
            {"map":["accept invitation"], "action":"comfortgf1","img":"embarrassed", "response":["{0}! I.. I wanna f***. Im feeling horny af rn."], "background":"house.jpg"},
            {"map":["gaming"], "action":"comfortgf2","img":"image", "response":["I.. I wanna game."], "background":"house.jpg"},
            {"map":["netflix"], "action":"comfortgf3","img":"image", "response":["I.. I wanna watch netflix. "], "background":"house.jpg"},
            {"map":["movies"], "action":"comfortgf4","img":"image", "response":["I.. I wanna watch a movie."], "background":"house.jpg"},
            {"map":["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"], "action":"comfortgf","img":"angry", "response":["Hmm, I think I know what will cheer me up!"], "background":"house.jpg"},
            {"map":["great", "Im not feeling that way"], "action":"happygf","img":"image", "response":["Hey! How are you doing?"], "background":"house.jpg"},
            {"map":["yeah sure what?"], "action":"great","img":"embarrassed", "response":["I wanna go do something with you..."], "background":"house.jpg"},
            {"map":["gaming"], "action":"gaming","img":"image", "response":["{0}! Lets play a game! I havnt played with you in forever!!"], "background":"house.jpg"},
            {"map":["movies"], "action":"movies","img":"image", "response":["{0}! Lets watch a movie!"], "background":"house.jpg"},
            {"map":["netflix"], "action":"netflix","img":"image", "response":["{0}! Lets watch netflix"], "background":"house.jpg"},
            {"map":["kiss","hug"], "action":"attentionwant","img":"embarrassed", "response":["I want attention!"], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scaredgf","img":"angry", "response":["Im not sure how im gonna pay the rent."], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"angrygf","img":"angry", "response":["Im not having a good day. I just wanna go to sleep."], "background":"house.jpg"},
        ],


            [
            {"typename":"Tsundere", "action":"none","img":"image", "response":"see you, {0}! I love you!", "background":"house.jpg"},
            {"map":["sad", "scared", "happy", "angry", "horny"], "action":"Im not feeling that way","img":"image", "response":["Im sorry, how are you feeling right now?"], "background":"house.jpg"},
            {"map":["accept invitation"], "action":"horny","img":"embarrassed", "response":["ohh, thats what you were feeling. Thats ok, I can help you out with that ;)"], "background":"house.jpg"},
            {"map":["leave","invite her to go do something"], "action":"end","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["No, Im fine", "Im not feeling that way"], "action":"sad","img":"image", "response":["It seems like you are sad. is that right? Thats too bad! is there anything I can do?"], "background":"house.jpg"},
            {"map":["lie on lap","dont lie on lap"], "action":"No, Im fine","img":"image", "response":["I cant give much, but I will support you will all Ive got! come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["leave","lie on lap"], "action":"dont lie on lap","img":"image", "response":["come on, just for a little while? come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["end"], "action":"lie on lap","img":"image","response": ["Hey. I know you can do it. I love you so much. That will never change. \n*You are my sunshine, My only sunshine\n You make me happy when skies are gray!\n You'll never know, dear, how much I love you!\n please dont take my sunshine away!*\n Did you like my voice? I hope so! *smooch*"], "background":"house.jpg"},
            {"map":["hug","kiss","Im really thankful for you!", "Im not feeling that way"], "action":"happy","img":"image", "response":["Thats amazing! im so happy for you!"], "background":"house.jpg"},
            {"map":["hug", "kiss", "end"], "action":"Im really thankful for you!","img":"image", "response":["aww, I love you so much! of course Id support you!"], "background":"house.jpg"},
            {"map":["end","kiss","invite her to go do something"], "action":"hug","img":"image", "response":["hmmm? You want a hug? of course!! *sqeezes*"], "background":"house.jpg"},
            {"map":["end","invite her to go do something"], "action":"kiss","img":"image", "response":["*mwah* I'll see you around! I love you!"], "background":"house.jpg"},
            {"map":["kiss"], "action":"Im really thankful for you!","img":"image", "response":["hey. I care about you!! Its only normal.."], "background":"house.jpg"},
            {"map":["walk away","lie on lap", "Im not feeling that way"], "action":"angry","img":"image", "response":["Hey. Im not sure if you are in the mood, you seem mad, or annoyed, but wanna rest on my lap?"], "background":"house.jpg"},
            {"map":["go with her", "dont follow"], "action":"walk away","img":"image", "response":["Hey I know just the thing! Follow me!"], "background":"house.jpg"},
            {"map":["end"], "action":"dont follow","img":"image", "response":["all right. I understand, Ill give you some time. If you wanna talk to me about anything, Im always available to you!"], "background":"house.jpg"},
            {"map":["leave","look at stars"], "action":"go with her","img":"image", "response":["this is the night sky! It looks nice, right? You can relax here. I find it nice gazing at the stars"], "background":"nightsky.jpg"},
            {"map":["end"], "action":"leave","img":"image", "response":["Im always ready to talk if you need me. I love you! bye!"], "background":"house.jpg"},
            {"map":["end"], "action":"look at stars","img":"image", "response":["Its nice right? Ill leave you be for now."], "background":"nightsky.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scared","img":"image", "response":["It sounds like you are scared. I know you are strong. You are also smart! if you cant handle it on your own, find someone to help you! You shouldnt always try to do things on your own!"], "background":"house.jpg"},
        
            {"map":["comfortgf"], "action":"sadgf","img":"sad", "response":["{0}, im feeling really sad! I dont like this! do something!"], "background":"house.jpg"},
            {"map":["gaming", "movies", "netflix", "horny"], "action":"invite her to go do something","img":"angry", "response":["What do you want to do together? Im... im open to anything!"], "background":"house.jpg"},            
            {"map":["accept invitation"], "action":"comfortgf1","img":"embarrassed", "response":["{0}! I.. I wanna f***. Im feeling horny af rn."], "background":"house.jpg"},
            {"map":["gaming"], "action":"comfortgf2","img":"image", "response":["I.. I wanna game."], "background":"house.jpg"},
            {"map":["netflix"], "action":"comfortgf3","img":"image", "response":["I.. I wanna watch netflix. "], "background":"house.jpg"},
            {"map":["movies"], "action":"comfortgf4","img":"image", "response":["I.. I wanna watch a movie."], "background":"house.jpg"},
            {"map":["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"], "action":"comfortgf","img":"angry", "response":["Hmm, I think I know what will cheer me up!"], "background":"house.jpg"},
            {"map":["great", "Im not feeling that way"], "action":"happygf","img":"image", "response":["Hey! How are you doing?"], "background":"house.jpg"},
            {"map":["yeah sure what?"], "action":"great","img":"embarrassed", "response":["I wanna go do something with you..."], "background":"house.jpg"},
            {"map":["gaming"], "action":"gaming","img":"image", "response":["{0}! Lets play a game! I havnt played with you in forever!!"], "background":"house.jpg"},
            {"map":["movies"], "action":"movies","img":"image", "response":["{0}! Lets watch a movie!"], "background":"house.jpg"},
            {"map":["netflix"], "action":"netflix","img":"image", "response":["{0}! Lets watch netflix"], "background":"house.jpg"},
            {"map":["kiss","hug"], "action":"attentionwant","img":"embarrassed", "response":["I want attention!"], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scaredgf","img":"angry", "response":["Im not sure how im gonna pay the rent."], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"angrygf","img":"angry", "response":["Im not having a good day. I just wanna go to sleep."], "background":"house.jpg"},
        ],

            [
            {"typename":"Yandere", "action":"none","img":"image", "response":"see you, {0}! I love you!", "background":"house.jpg"},
            {"map":["sad", "scared", "happy", "angry", "horny"], "action":"Im not feeling that way","img":"image", "response":["Im sorry, how are you feeling right now?"], "background":"house.jpg"},
            {"map":["accept invitation"], "action":"horny","img":"embarrassed", "response":["ohh, thats what you were feeling. Thats ok, I can help you out with that ;)"], "background":"house.jpg"},
            {"map":["leave","invite her to go do something"], "action":"end","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["No, Im fine", "Im not feeling that way"], "action":"sad","img":"image", "response":["It seems like you are sad. is that right? Thats too bad! is there anything I can do?"], "background":"house.jpg"},
            {"map":["lie on lap","dont lie on lap"], "action":"No, Im fine","img":"image", "response":["I cant give much, but I will support you will all Ive got! come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["leave","lie on lap"], "action":"dont lie on lap","img":"image", "response":["come on, just for a little while? come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["end"], "action":"lie on lap","img":"image","response": ["Hey. I know you can do it. I love you so much. That will never change. \n*You are my sunshine, My only sunshine\n You make me happy when skies are gray!\n You'll never know, dear, how much I love you!\n please dont take my sunshine away!*\n Did you like my voice? I hope so! *smooch*"], "background":"house.jpg"},
            {"map":["hug","kiss","Im really thankful for you!", "Im not feeling that way"], "action":"happy","img":"image", "response":["Thats amazing! im so happy for you!"], "background":"house.jpg"},
            {"map":["hug", "kiss", "end"], "action":"Im really thankful for you!","img":"image", "response":["aww, I love you so much! of course Id support you!"], "background":"house.jpg"},
            {"map":["end","kiss","invite her to go do something"], "action":"hug","img":"image", "response":["hmmm? You want a hug? of course!! *sqeezes*"], "background":"house.jpg"},
            {"map":["end","invite her to go do something"], "action":"kiss","img":"image", "response":["*mwah* I'll see you around! I love you!"], "background":"house.jpg"},
            {"map":["kiss"], "action":"Im really thankful for you!","img":"image", "response":["hey. I care about you!! Its only normal.."], "background":"house.jpg"},
            {"map":["walk away","lie on lap", "Im not feeling that way"], "action":"angry","img":"image", "response":["Hey. Im not sure if you are in the mood, you seem mad, or annoyed, but wanna rest on my lap?"], "background":"house.jpg"},
            {"map":["go with her", "dont follow"], "action":"walk away","img":"image", "response":["Hey I know just the thing! Follow me!"], "background":"house.jpg"},
            {"map":["end"], "action":"dont follow","img":"image", "response":["all right. I understand, Ill give you some time. If you wanna talk to me about anything, Im always available to you!"], "background":"house.jpg"},
            {"map":["leave","look at stars"], "action":"go with her","img":"image", "response":["this is the night sky! It looks nice, right? You can relax here. I find it nice gazing at the stars"], "background":"nightsky.jpg"},
            {"map":["end"], "action":"leave","img":"image", "response":["Im always ready to talk if you need me. I love you! bye!"], "background":"house.jpg"},
            {"map":["end"], "action":"look at stars","img":"image", "response":["Its nice right? Ill leave you be for now."], "background":"nightsky.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scared","img":"image", "response":["It sounds like you are scared. I know you are strong. You are also smart! if you cant handle it on your own, find someone to help you! You shouldnt always try to do things on your own!"], "background":"house.jpg"},
        
            {"map":["comfortgf"], "action":"sadgf","img":"sad", "response":["{0}, im feeling really sad! I dont like this! do something!"], "background":"house.jpg"},
            {"map":["gaming", "movies", "netflix", "horny"], "action":"invite her to go do something","img":"angry", "response":["What do you want to do together? Im... im open to anything!"], "background":"house.jpg"},            
            {"map":["accept invitation"], "action":"comfortgf1","img":"embarrassed", "response":["{0}! I.. I wanna f***. Im feeling horny af rn."], "background":"house.jpg"},
            {"map":["gaming"], "action":"comfortgf2","img":"image", "response":["I.. I wanna game."], "background":"house.jpg"},
            {"map":["netflix"], "action":"comfortgf3","img":"image", "response":["I.. I wanna watch netflix. "], "background":"house.jpg"},
            {"map":["movies"], "action":"comfortgf4","img":"image", "response":["I.. I wanna watch a movie."], "background":"house.jpg"},
            {"map":["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"], "action":"comfortgf","img":"angry", "response":["Hmm, I think I know what will cheer me up!"], "background":"house.jpg"},
            {"map":["great", "Im not feeling that way"], "action":"happygf","img":"image", "response":["Hey! How are you doing?"], "background":"house.jpg"},
            {"map":["yeah sure what?"], "action":"great","img":"embarrassed", "response":["I wanna go do something with you..."], "background":"house.jpg"},
            {"map":["gaming"], "action":"gaming","img":"image", "response":["{0}! Lets play a game! I havnt played with you in forever!!"], "background":"house.jpg"},
            {"map":["movies"], "action":"movies","img":"image", "response":["{0}! Lets watch a movie!"], "background":"house.jpg"},
            {"map":["netflix"], "action":"netflix","img":"image", "response":["{0}! Lets watch netflix"], "background":"house.jpg"},
            {"map":["kiss","hug"], "action":"attentionwant","img":"embarrassed", "response":["I want attention!"], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scaredgf","img":"angry", "response":["Im not sure how im gonna pay the rent."], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"angrygf","img":"angry", "response":["Im not having a good day. I just wanna go to sleep."], "background":"house.jpg"},
        ],

            [
            {"typename":"Dandere", "action":"none","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["sad", "scared", "happy", "angry", "horny"], "action":"Im not feeling that way","img":"image", "response":["Im sorry, how are you feeling right now?"], "background":"house.jpg"},
            {"map":["accept invitation"], "action":"horny","img":"embarrassed", "response":["ohh, thats what you were feeling. Thats ok, I can help you out with that ;)"], "background":"house.jpg"},
            {"map":["leave","invite her to go do something"], "action":"end","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["No, Im fine", "Im not feeling that way"], "action":"sad","img":"image", "response":["It seems like you are sad. is that right? Thats too bad! is there anything I can do?"], "background":"house.jpg"},
            {"map":["lie on lap","dont lie on lap"], "action":"No, Im fine","img":"image", "response":["I cant give much, but I will support you will all Ive got! come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["leave","lie on lap"], "action":"dont lie on lap","img":"image", "response":["come on, just for a little while? come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["end"], "action":"lie on lap","img":"image","response": ["Hey. I know you can do it. I love you so much. That will never change. \n*You are my sunshine, My only sunshine\n You make me happy when skies are gray!\n You'll never know, dear, how much I love you!\n please dont take my sunshine away!*\n Did you like my voice? I hope so! *smooch*"], "background":"house.jpg"},
            {"map":["hug","kiss","Im really thankful for you!", "Im not feeling that way"], "action":"happy","img":"image", "response":["Thats amazing! im so happy for you!"], "background":"house.jpg"},
            {"map":["hug", "kiss", "end"], "action":"Im really thankful for you!","img":"image", "response":["aww, I love you so much! of course Id support you!"], "background":"house.jpg"},
            {"map":["end","kiss","invite her to go do something"], "action":"hug","img":"image", "response":["hmmm? You want a hug? of course!! *sqeezes*"], "background":"house.jpg"},
            {"map":["end","invite her to go do something"], "action":"kiss","img":"image", "response":["*mwah* I'll see you around! I love you!"], "background":"house.jpg"},
            {"map":["kiss"], "action":"Im really thankful for you!","img":"image", "response":["hey. I care about you!! Its only normal.."], "background":"house.jpg"},
            {"map":["walk away","lie on lap", "Im not feeling that way"], "action":"angry","img":"image", "response":["Hey. Im not sure if you are in the mood, you seem mad, or annoyed, but wanna rest on my lap?"], "background":"house.jpg"},
            {"map":["go with her", "dont follow"], "action":"walk away","img":"image", "response":["Hey I know just the thing! Follow me!"], "background":"house.jpg"},
            {"map":["end"], "action":"dont follow","img":"image", "response":["all right. I understand, Ill give you some time. If you wanna talk to me about anything, Im always available to you!"], "background":"house.jpg"},
            {"map":["leave","look at stars"], "action":"go with her","img":"image", "response":["this is the night sky! It looks nice, right? You can relax here. I find it nice gazing at the stars"], "background":"nightsky.jpg"},
            {"map":["end"], "action":"leave","img":"image", "response":["Im always ready to talk if you need me. I love you! bye!"], "background":"house.jpg"},
            {"map":["end"], "action":"look at stars","img":"image", "response":["Its nice right? Ill leave you be for now."], "background":"nightsky.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scared","img":"image", "response":["It sounds like you are scared. I know you are strong. You are also smart! if you cant handle it on your own, find someone to help you! You shouldnt always try to do things on your own!"], "background":"house.jpg"},
        
            {"map":["comfortgf"], "action":"sadgf","img":"sad", "response":["{0}, im feeling really sad! I dont like this! do something!"], "background":"house.jpg"},
            {"map":["gaming", "movies", "netflix", "horny"], "action":"invite her to go do something","img":"angry", "response":["What do you want to do together? Im... im open to anything!"], "background":"house.jpg"},            
            {"map":["accept invitation"], "action":"comfortgf1","img":"embarrassed", "response":["{0}! I.. I wanna f***. Im feeling horny af rn."], "background":"house.jpg"},
            {"map":["gaming"], "action":"comfortgf2","img":"image", "response":["I.. I wanna game."], "background":"house.jpg"},
            {"map":["netflix"], "action":"comfortgf3","img":"image", "response":["I.. I wanna watch netflix. "], "background":"house.jpg"},
            {"map":["movies"], "action":"comfortgf4","img":"image", "response":["I.. I wanna watch a movie."], "background":"house.jpg"},
            {"map":["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"], "action":"comfortgf","img":"angry", "response":["Hmm, I think I know what will cheer me up!"], "background":"house.jpg"},
            {"map":["great", "Im not feeling that way"], "action":"happygf","img":"image", "response":["Hey! How are you doing?"], "background":"house.jpg"},
            {"map":["yeah sure what?"], "action":"great","img":"embarrassed", "response":["I wanna go do something with you..."], "background":"house.jpg"},
            {"map":["gaming"], "action":"gaming","img":"image", "response":["{0}! Lets play a game! I havnt played with you in forever!!"], "background":"house.jpg"},
            {"map":["movies"], "action":"movies","img":"image", "response":["{0}! Lets watch a movie!"], "background":"house.jpg"},
            {"map":["netflix"], "action":"netflix","img":"image", "response":["{0}! Lets watch netflix"], "background":"house.jpg"},
            {"map":["kiss","hug"], "action":"attentionwant","img":"embarrassed", "response":["I want attention!"], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scaredgf","img":"angry", "response":["Im not sure how im gonna pay the rent."], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"angrygf","img":"angry", "response":["Im not having a good day. I just wanna go to sleep."], "background":"house.jpg"},
        ],

            [
            {"typename":"Sadodere", "action":"none","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["sad", "scared", "happy", "angry", "horny"], "action":"Im not feeling that way","img":"image", "response":["Im sorry, how are you feeling right now?"], "background":"house.jpg"},
            {"map":["accept invitation"], "action":"horny","img":"embarrassed", "response":["ohh, thats what you were feeling. Thats ok, I can help you out with that ;)"], "background":"house.jpg"},
            {"map":["leave","invite her to go do something"], "action":"end","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["No, Im fine", "Im not feeling that way"], "action":"sad","img":"image", "response":["It seems like you are sad. is that right? Thats too bad! is there anything I can do?"], "background":"house.jpg"},
            {"map":["lie on lap","dont lie on lap"], "action":"No, Im fine","img":"image", "response":["I cant give much, but I will support you will all Ive got! come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["leave","lie on lap"], "action":"dont lie on lap","img":"image", "response":["come on, just for a little while? come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["end"], "action":"lie on lap","img":"image","response": ["Hey. I know you can do it. I love you so much. That will never change. \n*You are my sunshine, My only sunshine\n You make me happy when skies are gray!\n You'll never know, dear, how much I love you!\n please dont take my sunshine away!*\n Did you like my voice? I hope so! *smooch*"], "background":"house.jpg"},
            {"map":["hug","kiss","Im really thankful for you!", "Im not feeling that way"], "action":"happy","img":"image", "response":["Thats amazing! im so happy for you!"], "background":"house.jpg"},
            {"map":["hug", "kiss", "end"], "action":"Im really thankful for you!","img":"image", "response":["aww, I love you so much! of course Id support you!"], "background":"house.jpg"},
            {"map":["end","kiss","invite her to go do something"], "action":"hug","img":"image", "response":["hmmm? You want a hug? of course!! *sqeezes*"], "background":"house.jpg"},
            {"map":["end","invite her to go do something"], "action":"kiss","img":"image", "response":["*mwah* I'll see you around! I love you!"], "background":"house.jpg"},
            {"map":["kiss"], "action":"Im really thankful for you!","img":"image", "response":["hey. I care about you!! Its only normal.."], "background":"house.jpg"},
            {"map":["walk away","lie on lap", "Im not feeling that way"], "action":"angry","img":"image", "response":["Hey. Im not sure if you are in the mood, you seem mad, or annoyed, but wanna rest on my lap?"], "background":"house.jpg"},
            {"map":["go with her", "dont follow"], "action":"walk away","img":"image", "response":["Hey I know just the thing! Follow me!"], "background":"house.jpg"},
            {"map":["end"], "action":"dont follow","img":"image", "response":["all right. I understand, Ill give you some time. If you wanna talk to me about anything, Im always available to you!"], "background":"house.jpg"},
            {"map":["leave","look at stars"], "action":"go with her","img":"image", "response":["this is the night sky! It looks nice, right? You can relax here. I find it nice gazing at the stars"], "background":"nightsky.jpg"},
            {"map":["end"], "action":"leave","img":"image", "response":["Im always ready to talk if you need me. I love you! bye!"], "background":"house.jpg"},
            {"map":["end"], "action":"look at stars","img":"image", "response":["Its nice right? Ill leave you be for now."], "background":"nightsky.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scared","img":"image", "response":["It sounds like you are scared. I know you are strong. You are also smart! if you cant handle it on your own, find someone to help you! You shouldnt always try to do things on your own!"], "background":"house.jpg"},
        
            {"map":["comfortgf"], "action":"sadgf","img":"sad", "response":["{0}, im feeling really sad! I dont like this! do something!"], "background":"house.jpg"},
            {"map":["gaming", "movies", "netflix", "horny"], "action":"invite her to go do something","img":"angry", "response":["What do you want to do together? Im... im open to anything!"], "background":"house.jpg"},            
            {"map":["accept invitation"], "action":"comfortgf1","img":"embarrassed", "response":["{0}! I.. I wanna f***. Im feeling horny af rn."], "background":"house.jpg"},
            {"map":["gaming"], "action":"comfortgf2","img":"image", "response":["I.. I wanna game."], "background":"house.jpg"},
            {"map":["netflix"], "action":"comfortgf3","img":"image", "response":["I.. I wanna watch netflix. "], "background":"house.jpg"},
            {"map":["movies"], "action":"comfortgf4","img":"image", "response":["I.. I wanna watch a movie."], "background":"house.jpg"},
            {"map":["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"], "action":"comfortgf","img":"angry", "response":["Hmm, I think I know what will cheer me up!"], "background":"house.jpg"},
            {"map":["great", "Im not feeling that way"], "action":"happygf","img":"image", "response":["Hey! How are you doing?"], "background":"house.jpg"},
            {"map":["yeah sure what?"], "action":"great","img":"embarrassed", "response":["I wanna go do something with you..."], "background":"house.jpg"},
            {"map":["gaming"], "action":"gaming","img":"image", "response":["{0}! Lets play a game! I havnt played with you in forever!!"], "background":"house.jpg"},
            {"map":["movies"], "action":"movies","img":"image", "response":["{0}! Lets watch a movie!"], "background":"house.jpg"},
            {"map":["netflix"], "action":"netflix","img":"image", "response":["{0}! Lets watch netflix"], "background":"house.jpg"},
            {"map":["kiss","hug"], "action":"attentionwant","img":"embarrassed", "response":["I want attention!"], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scaredgf","img":"angry", "response":["Im not sure how im gonna pay the rent."], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"angrygf","img":"angry", "response":["Im not having a good day. I just wanna go to sleep."], "background":"house.jpg"},
        ],

            [
            {"typename":"Kuudere", "action":"none","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["sad", "scared", "happy", "angry", "horny"], "action":"Im not feeling that way","img":"image", "response":["Im sorry, how are you feeling right now?"], "background":"house.jpg"},
            {"map":["accept invitation"], "action":"horny","img":"embarrassed", "response":["ohh, thats what you were feeling. Thats ok, I can help you out with that ;)"], "background":"house.jpg"},
            {"map":["leave","invite her to go do something"], "action":"end","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["No, Im fine", "Im not feeling that way"], "action":"sad","img":"image", "response":["It seems like you are sad. is that right? Thats too bad! is there anything I can do?"], "background":"house.jpg"},
            {"map":["lie on lap","dont lie on lap"], "action":"No, Im fine","img":"image", "response":["I cant give much, but I will support you will all Ive got! come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["leave","lie on lap"], "action":"dont lie on lap","img":"image", "response":["come on, just for a little while? come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["end"], "action":"lie on lap","img":"image","response": ["Hey. I know you can do it. I love you so much. That will never change. \n*You are my sunshine, My only sunshine\n You make me happy when skies are gray!\n You'll never know, dear, how much I love you!\n please dont take my sunshine away!*\n Did you like my voice? I hope so! *smooch*"], "background":"house.jpg"},
            {"map":["hug","kiss","Im really thankful for you!", "Im not feeling that way"], "action":"happy","img":"image", "response":["Thats amazing! im so happy for you!"], "background":"house.jpg"},
            {"map":["hug", "kiss", "end"], "action":"Im really thankful for you!","img":"image", "response":["aww, I love you so much! of course Id support you!"], "background":"house.jpg"},
            {"map":["end","kiss","invite her to go do something"], "action":"hug","img":"image", "response":["hmmm? You want a hug? of course!! *sqeezes*"], "background":"house.jpg"},
            {"map":["end","invite her to go do something"], "action":"kiss","img":"image", "response":["*mwah* I'll see you around! I love you!"], "background":"house.jpg"},
            {"map":["kiss"], "action":"Im really thankful for you!","img":"image", "response":["hey. I care about you!! Its only normal.."], "background":"house.jpg"},
            {"map":["walk away","lie on lap", "Im not feeling that way"], "action":"angry","img":"image", "response":["Hey. Im not sure if you are in the mood, you seem mad, or annoyed, but wanna rest on my lap?"], "background":"house.jpg"},
            {"map":["go with her", "dont follow"], "action":"walk away","img":"image", "response":["Hey I know just the thing! Follow me!"], "background":"house.jpg"},
            {"map":["end"], "action":"dont follow","img":"image", "response":["all right. I understand, Ill give you some time. If you wanna talk to me about anything, Im always available to you!"], "background":"house.jpg"},
            {"map":["leave","look at stars"], "action":"go with her","img":"image", "response":["this is the night sky! It looks nice, right? You can relax here. I find it nice gazing at the stars"], "background":"nightsky.jpg"},
            {"map":["end"], "action":"leave","img":"image", "response":["Im always ready to talk if you need me. I love you! bye!"], "background":"house.jpg"},
            {"map":["end"], "action":"look at stars","img":"image", "response":["Its nice right? Ill leave you be for now."], "background":"nightsky.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scared","img":"image", "response":["It sounds like you are scared. I know you are strong. You are also smart! if you cant handle it on your own, find someone to help you! You shouldnt always try to do things on your own!"], "background":"house.jpg"},
        
            {"map":["comfortgf"], "action":"sadgf","img":"sad", "response":["{0}, im feeling really sad! I dont like this! do something!"], "background":"house.jpg"},
            {"map":["gaming", "movies", "netflix", "horny"], "action":"invite her to go do something","img":"angry", "response":["What do you want to do together? Im... im open to anything!"], "background":"house.jpg"},            
            {"map":["accept invitation"], "action":"comfortgf1","img":"embarrassed", "response":["{0}! I.. I wanna f***. Im feeling horny af rn."], "background":"house.jpg"},
            {"map":["gaming"], "action":"comfortgf2","img":"image", "response":["I.. I wanna game."], "background":"house.jpg"},
            {"map":["netflix"], "action":"comfortgf3","img":"image", "response":["I.. I wanna watch netflix. "], "background":"house.jpg"},
            {"map":["movies"], "action":"comfortgf4","img":"image", "response":["I.. I wanna watch a movie."], "background":"house.jpg"},
            {"map":["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"], "action":"comfortgf","img":"angry", "response":["Hmm, I think I know what will cheer me up!"], "background":"house.jpg"},
            {"map":["great", "Im not feeling that way"], "action":"happygf","img":"image", "response":["Hey! How are you doing?"], "background":"house.jpg"},
            {"map":["yeah sure what?"], "action":"great","img":"embarrassed", "response":["I wanna go do something with you..."], "background":"house.jpg"},
            {"map":["gaming"], "action":"gaming","img":"image", "response":["{0}! Lets play a game! I havnt played with you in forever!!"], "background":"house.jpg"},
            {"map":["movies"], "action":"movies","img":"image", "response":["{0}! Lets watch a movie!"], "background":"house.jpg"},
            {"map":["netflix"], "action":"netflix","img":"image", "response":["{0}! Lets watch netflix"], "background":"house.jpg"},
            {"map":["kiss","hug"], "action":"attentionwant","img":"embarrassed", "response":["I want attention!"], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scaredgf","img":"angry", "response":["Im not sure how im gonna pay the rent."], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"angrygf","img":"angry", "response":["Im not having a good day. I just wanna go to sleep."], "background":"house.jpg"},
        ],
            [
            {"typename":"Kamidere", "action":"none","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["sad", "scared", "happy", "angry", "horny"], "action":"Im not feeling that way","img":"image", "response":["Im sorry, how are you feeling right now?"], "background":"house.jpg"},
            {"map":["accept invitation"], "action":"horny","img":"embarrassed", "response":["ohh, thats what you were feeling. Thats ok, I can help you out with that ;)"], "background":"house.jpg"},
            {"map":["leave","invite her to go do something"], "action":"end","img":"image", "response":["see you, {0}! I love you!"], "background":"house.jpg"},
            {"map":["No, Im fine", "Im not feeling that way"], "action":"sad","img":"image", "response":["It seems like you are sad. is that right? Thats too bad! is there anything I can do?"], "background":"house.jpg"},
            {"map":["lie on lap","dont lie on lap"], "action":"No, Im fine","img":"image", "response":["I cant give much, but I will support you will all Ive got! come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["leave","lie on lap"], "action":"dont lie on lap","img":"image", "response":["come on, just for a little while? come here! *motions to rest on lap*"], "background":"house.jpg"},
            {"map":["end"], "action":"lie on lap","img":"image","response": ["Hey. I know you can do it. I love you so much. That will never change. \n*You are my sunshine, My only sunshine\n You make me happy when skies are gray!\n You'll never know, dear, how much I love you!\n please dont take my sunshine away!*\n Did you like my voice? I hope so! *smooch*"], "background":"house.jpg"},
            {"map":["hug","kiss","Im really thankful for you!", "Im not feeling that way"], "action":"happy","img":"image", "response":["Thats amazing! im so happy for you!"], "background":"house.jpg"},
            {"map":["hug", "kiss", "end"], "action":"Im really thankful for you!","img":"image", "response":["aww, I love you so much! of course Id support you!"], "background":"house.jpg"},
            {"map":["end","kiss","invite her to go do something"], "action":"hug","img":"image", "response":["hmmm? You want a hug? of course!! *sqeezes*"], "background":"house.jpg"},
            {"map":["end","invite her to go do something"], "action":"kiss","img":"image", "response":["*mwah* I'll see you around! I love you!"], "background":"house.jpg"},
            {"map":["kiss"], "action":"Im really thankful for you!","img":"image", "response":["hey. I care about you!! Its only normal.."], "background":"house.jpg"},
            {"map":["walk away","lie on lap", "Im not feeling that way"], "action":"angry","img":"image", "response":["Hey. Im not sure if you are in the mood, you seem mad, or annoyed, but wanna rest on my lap?"], "background":"house.jpg"},
            {"map":["go with her", "dont follow"], "action":"walk away","img":"image", "response":["Hey I know just the thing! Follow me!"], "background":"house.jpg"},
            {"map":["end"], "action":"dont follow","img":"image", "response":["all right. I understand, Ill give you some time. If you wanna talk to me about anything, Im always available to you!"], "background":"house.jpg"},
            {"map":["leave","look at stars"], "action":"go with her","img":"image", "response":["this is the night sky! It looks nice, right? You can relax here. I find it nice gazing at the stars"], "background":"nightsky.jpg"},
            {"map":["end"], "action":"leave","img":"image", "response":["Im always ready to talk if you need me. I love you! bye!"], "background":"house.jpg"},
            {"map":["end"], "action":"look at stars","img":"image", "response":["Its nice right? Ill leave you be for now."], "background":"nightsky.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scared","img":"image", "response":["It sounds like you are scared. I know you are strong. You are also smart! if you cant handle it on your own, find someone to help you! You shouldnt always try to do things on your own!"], "background":"house.jpg"},
        
            {"map":["comfortgf"], "action":"sadgf","img":"sad", "response":["{0}, im feeling really sad! I dont like this! do something!"], "background":"house.jpg"},
            {"map":["gaming", "movies", "netflix", "horny"], "action":"invite her to go do something","img":"angry", "response":["What do you want to do together? Im... im open to anything!"]},            
            {"map":["accept invitation"], "action":"comfortgf1","img":"embarrassed", "response":["{0}! I.. I wanna f***. Im feeling horny af rn."], "background":"house.jpg"},
            {"map":["gaming"], "action":"comfortgf2","img":"image", "response":["I.. I wanna game."], "background":"house.jpg"},
            {"map":["netflix"], "action":"comfortgf3","img":"image", "response":["I.. I wanna watch netflix. "], "background":"house.jpg"},
            {"map":["movies"], "action":"comfortgf4","img":"image", "response":["I.. I wanna watch a movie."], "background":"house.jpg"},
            {"map":["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"], "action":"comfortgf","img":"angry", "response":["Hmm, I think I know what will cheer me up!"], "background":"house.jpg"},
            {"map":["great", "Im not feeling that way"], "action":"happygf","img":"image", "response":["Hey! How are you doing?"], "background":"house.jpg"},
            {"map":["yeah sure what?"], "action":"great","img":"embarrassed", "response":["I wanna go do something with you..."], "background":"house.jpg"},
            {"map":["gaming"], "action":"gaming","img":"image", "response":["{0}! Lets play a game! I havnt played with you in forever!!"], "background":"house.jpg"},
            {"map":["movies"], "action":"movies","img":"image", "response":["{0}! Lets watch a movie!"], "background":"house.jpg"},
            {"map":["netflix"], "action":"netflix","img":"image", "response":["{0}! Lets watch netflix"], "background":"house.jpg"},
            {"map":["kiss","hug"], "action":"attentionwant","img":"embarrassed", "response":["I want attention!"], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"scaredgf","img":"angry", "response":["Im not sure how im gonna pay the rent."], "background":"house.jpg"},
            {"map":["end", "Im not feeling that way"], "action":"angrygf","img":"angry", "response":["Im not having a good day. I just wanna go to sleep."], "background":"house.jpg"},
        ],
        ]

        global boinkmap
        boinkmap = [
            {"map":["pin down","kiss",], "action":"start","img":"image"},
            {"map":["pin down","fondle oppai",], "action":"kiss", "img":"embarrased"},
            {"map":["fondle oppai", "kiss", "insert pp", "bite", "finger vegana"], "action":"pin down", "img":"embarrassed"},
            {"map":["pin down","fondle oppai", "suck oppai", "bite", "finger vegana"], "action":"fondle oppai", "img":"horny"},
            {"map":["pin down","fondle oppai", "kiss", "bite", "finger vegana"], "action":"suck oppai", "img":"horny"},
            {"map":["pin down","fondle oppai", "lick vegana", "kiss", "bite", "finger vegana"], "action":"finger vegana", "img":"horny"},
            {"map":["pin down", "insert pp", "kiss", "bite", "finger vegana"], "action":"lick vegana", "img":"horny"},
            {"map":["pin down","fondle oppai", "kiss", "bite", "finger vegana"], "action":"bite", "img":"horny"},
            {"map":["climax"], "action":"insert pp", "img":"climax"},
            {"map":None, "action":"climax", "img":"bed"},


        ]
        global boinkresponse
        boinkresponse = [
            {"typename":"Tsundere",
             "start":["Hello!", "again?"], 
             "kiss":["..thanks! You are really good!", "aww, I love you too!"], 
             "pin down":["eh? What are you doing?", "again pin dowN"], 
             "fondle oppai":["*oh* t. That feels really good!", "again? I dont mind though..."], 
             "suck oppai":["*ahh* How do you like my boobs?", "You really like my boobs, dont you.."], 
             "finger vegana":["stop.. im really sensitive there!", "I think I might reach my limit! Its amazing!"],
             "lick vegana":["How does it taste?", "Youre a greedy boy, {0}, You keep coming back for more, huh?"], 
             "bite":["awww", "What do you think of my skin?"], 
             "insert pp":["oh! Its so big!, It feels like heaven!", "againinsert"], 
             "climax": "*That felt amazing. I love you so so much. I...\n I want 3 kids."},

            {"typename":"Yandere", 
            "start":["What do you plan to do to me today? ;)", "again?"], 
            "kiss":["huh, feeling horny are you?", "I never get tired of kissing you <3"], 
            "pin down":["Oh, its new seeing you with the initiative.. I like it!", "again pin dowN"], 
            "fondle oppai":["These tits are yours. Do you think they are bouncy?", "You really like my tits huh?"], 
            "suck oppai":["Please feel free to suck on my milkers anytime,", "Came back for more huh?"], 
            "finger vegana":["That feels sooo good", "This feels great.."],
            "lick vegana":["Im sensitive there, but go on. How does this fresh pussy taste, {0}?", "My pussy tasted so good, you came back for more, huh?"], 
            "bite":["aww, I love you too!", "bite me moree"], 
            "insert pp":["oh my! You feel even better than I imagined!! I cant tell you how long ive been waiting for this!", "againinsert"], 
            "climax": "That felt great Lets do this more, and more and more!!!!!"},            
            
            {"typename":"Dandere", 
            "start":["..oh hi!", "again?"], 
            "kiss":[".. *blushes* thank you..", "I love you too.."], 
            "pin down":[".. what are you doing?", "again pin dowN"], 
            "fondle oppai":["oh my.. that feels so good.", "*mph* im sensitive."], 
            "suck oppai":["that feels so good! I really like this!", "keep going!"], 
            "finger vegana":["..im sensitive there! I.. might not last long", "*im really sensitive there, {0}-kun"],
            "lick vegana":["{0}-kun is licking my..!", "it feels great!"], 
            "bite":["i want to bite you too!", "let me bite you! *bites back*"], 
            "insert pp":["i..its so big!", "againinsert"], 
            "climax": "{0}-kun, that felt amazing!"},  

            {"typename":"Kuudere", 
            "start":["Hello.", "again?"], 
            "kiss":["continue,", "I like your lips."], 
            "pin down":["Pinning me down now?", "again pin dowN"], 
            "fondle oppai":["You like these milkers?", "They are bouncy arent they?"], 
            "suck oppai":["I like this feeling. Keep sucking", "coming back to my milkers, You must like them?"], 
            "finger vegana":["Im sensitive there. I might come!", "I really like that!"],
            "lick vegana":["oh, This feels great", "amazing!!!"], 
            "bite":["marking me huh? thats pretty kinky.", "*bites back*"], 
            "insert pp":["its so big!!", "againinsert"], 
            "climax": "You are great {0}, I love you so much!"},  

            {"typename":"Sadodere", 
            "start":["Oh hey, {0}", "again?"], 
            "kiss":["hmm??? arent you taking initiative!", "these lips really turn you on huh?"], 
            "pin down":["I never knew this part of you, {0}!", "again pin dowN"], 
            "fondle oppai":["You go for my tits huh? Pervert!!!!!! hahahahaha, im joking, Go on,", "are my tits that bouncy?"], 
            "suck oppai":["ara ara, how do my tits taste?", "You like that dont you?"], 
            "finger vegana":["Is my pussy wetter than you imagined?", "hahaha! It feels great!!"],
            "lick vegana":["How does this pussy taste?", "damn, it tastes good huh?"], 
            "bite":["ooh, {0} is marking me as his! hahaha pervert!! but.. go on. I like it.", "*smacks*"], 
            "insert pp":["you finally took it out!", "againinsert"], 
            "climax": "Hey, {0}, youre not that bad. I.. I want 4 kids."},  

            {"typename":"Sweet", 
            "start":["oh hello {0}-kun!", "again?"], 
            "kiss":["huh, you really are taking initiative today!! <3", "I love you so so much!"], 
            "pin down":["*ehhh?* wha.. what are you doing {0}-kun?\n aha! I see how it is, go on!", "again pin dowN"], 
            "fondle oppai":["How do these feel? are they bouncy?", "that feels great!"], 
            "suck oppai":["{0}-kun, you really like my boobs, dont you?", "*mph* keep sucking!"], 
            "finger vegana":["{0}-kun.... Im really sensitive there!", "ah.. stop, I might come<3"],
            "lick vegana":["ohh gosh, thats amazing!", "You came back for more huh? Does my pussy taste that good to you?"], 
            "bite":["*ahh*, I love you too! *bites back*", "*ahhh*"], 
            "insert pp":["Its so big!!!! Im so happy! Its even better than I thought!!!!", "againinsert"], 
            "climax": "You are amazing {0}-kun. I love you so so so much! I wanna be with you forever! I wanna grow old together with you, {0}-kun!"},  

            {"typename":"Kamidere", 
            "start":["Oh, hello, {0}", "again?"], 
            "kiss":["*mph* haha, nice!", "I love you too <3"], 
            "pin down":["*hmmm?* what are you planning on doing? <3", "again pin dowN"], 
            "fondle oppai":["*ohh* How do me breasts feel? are they satisfactory?", "You really like my breasts dont you?"], 
            "suck oppai":["hmm, keep going <3", "oh god, this feels soo good."], 
            "finger vegana":["I am sensitive there, {0}", "You really want me to orgasm huh?"],
            "lick vegana":["How does this fresh taint taste? Is is salty? <3", "mmm, coming back for more huh?"], 
            "bite":["awww", "Again?"], 
            "insert pp":["Its.. bigger than I expected..", "againinsert"], 
            "climax": "That felt great, {0}, I cant wait to spend time with you again <3"},  
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
        global shopitems
        shopitems = [
            {"name":"phone", "value":800, "desc":"Text your Girlfriend!"},
            {"name": "laptop", "value": 1500, "desc":"Post memes, or play a game with your girlfriend"},
            {"name": "netflixsub", "value": 29, "desc": "Netflix and chill with your gf"},
            {"name": "lotterylicket", "value": 2, "desc": "A chance to win 1 million dollars"},
            {"name": "movieticket", "value" : 16, "desc":"watch a movie with your gf"},
            {"name": "ring", "value" : 10000, "desc":"propose to your gf"},
        ]

        global gftypes
        gftypes = [
            {"typename":"Tsundere", "letter":"a","textresponse": ["You are really bad at that, you know?", "That was fine, I guess.", "That was... Nice. t...tthank you."], "movieresponse": "thanks for taking me out!", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"I love you too! *squeezes*", "kissresponse": "... that was sudden. Youre a great kisser. I wouldnt mind another one <3", "proposeresponse": "YESSS!! YESS I LOVE YOU SOO MUCH {0}!!!"},
            {"typename":"Yandere", "letter":"b", "textresponse": ["maybe you should try harder? I will support you in any way I can.", "Thank you for the text.", "Thank you for the text. ily very much." ], "movieresponse": "I want to see more movies with you!", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"Dont move. I wanna stay like this for a few more hours.", "kissresponse": "stop. Dont leave. Kiss me again. Again. And again...", "proposeresponse": "of course Ill marry you!! i want to spend all my time with you! {0}!!!"},
            {"typename":"Dandere", "letter":"c", "textresponse": [".. thanks, but.. please try harder next time!","...I appreciate the text.", "Thank you for the text... I love you too."], "movieresponse": "Thank... you.. for taking me out!" , "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"T.. thank you.", "kissresponse": "...thanks.", "proposeresponse": ".. of course!!!! I love you so much, {0}!!!"},
            {"typename":"Kuudere", "letter":"d", "textresponse": ["That was terrible.", "Decent at best.", "This is great. I love you very much."], "movieresponse": "That was a good movie.", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"Squeeze me more. i like this feeling.", "kissresponse": "Kiss me again. I like that feeling", "proposeresponse": "marry you? yeh sure ig. I guess you are now my fiance, {0}!!!"},
            {"typename":"Sweet", "letter":"e", "textresponse": ["Thank you! but try a little bit better next time?", "Thank you! I appreciate what you do!!", "This is amazing!!! Thank you! ily so so much!"], "movieresponse": "woow! that was great! we should do this more often!!", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"aww thanks! I love you too!! *squeezes* I dont ever want to lose you!", "kissresponse": "... that was sudden. Youre a great kisser. I wouldnt mind another one <3 I love you so much!", "proposeresponse": "YES! Of course I want to marry you! I want to spend time with you, Have kids, Grow old together. I love you so much, {0}!!!"},
            {"typename":"Sadodere", "letter":"f", "textresponse": ["You are really bad at texting!! I find it amusing.", "That was a decent text! Only Decent though.", "Good job! I am satisfied with that."], "movieresponse": "Isnt that something? Taking your girlfriend out to watch a movie.", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"huh? youre hugging me? Fine. Ill allow it. Pervert.", "kissresponse": ".. AH.. AHAHAHA did you just kiss me? pervert <3", "proposeresponse": "Marry you? Haha, Of course. I love you, {0} <3"},
            {"typename":"Kamidere", "letter":"g", "textresponse": ["Your texting skill is poor; It can be improved though.", "That was good effort. However, your text was only decent.", "Excellent. I appreciate it.❤️"], "movieresponse": "Thank you for the invitation. I greatly appreciate it❤️", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"Thank you. I love your embrace.", "kissresponse": "Youre great at that <3.", "proposeresponse": "{0}. Regarding your marriage proposal, I gratefully accept. words cant describe how much you mean to me. I want to spend the rest of my life with you<3."},
        ]      
        global typeconplaint  
        typeconplaint = [
            {"typename": "Tsundere", 
            "strategy": "I dont really like strategy. but I guess its fine."},

            {"typename": "Yandere", 
            "strategy": "strategy isnt my forte. It isnt necessary either. I know everything about you already <3"},

            {"typename": "Dandere", 
            "strategy": "...I would prefer another genre.."},

            {"typename": "Kuudere", 
            "strategy": "strategy isnt fun."},

            {"typename": "Sweet", 
            "strategy": "I really appreciate the thought, but I think we could do another genre?"},

            {"typename": "Sadodere", 
            "strategy": "i dont like strategy. Its gross."},

            {"typename": "Kamidere", 
            "strategy": "I dont enjoy strategy games. They create an uptight atmosphere, that isnt ideal for our relationship."},

        ]
        global typegenrepraise
        typegenrepraise = [
            {"typename": "Tsundere", 
            "strategy": "I really like strategy!",
            "horror":"That wasnt scary at all!", 
            "fps":"I love FPS games!", 
            "creativity":"I think Creativity games are the best!",
            "adventure":"I think Adventure games are the best!", 
            "animation":"The animation was great! I think the creators did an amazing job dont you think?", 
            "action":"Action is great!!"},

            {"typename": "Yandere", 
            "strategy": "I love this uptight atmosphere.",
            "horror":"That wasnt scary at all!", 
            "fps":"I love FPS games!", 
            "creativity":"I think Creativity games are the best!",
            "adventure":"I think Adventure games are the best!", 
            "animation":"The animation was great! I think the creators did an amazing job dont you think?", 
            "action":"Action is great!!"},

            {"typename": "Dandere", 
            "strategy": "...I like this genre!",
            "horror":"That wasnt scary at all!", 
            "fps":"I love FPS games!", 
            "creativity":"I think Creativity games are the best!",
            "adventure":"I think Adventure games are the best!", 
            "animation":"The animation was great! I think the creators did an amazing job dont you think?", 
            "action":"Action is great!!"},

            {"typename": "Kuudere", 
            "strategy": "strategy is fun.",
            "horror":"That wasnt scary at all!", 
            "fps":"I love FPS games!", 
            "creativity":"I think Creativity games are the best!",
            "adventure":"I think Adventure games are the best!", 
            "animation":"The animation was great! I think the creators did an amazing job dont you think?", 
            "action":"Action is great!!"},

            {"typename": "Sweet", 
            "strategy": "woow! this is really fun! strategy is really fun!!",
            "horror":"That wasnt scary at all!", 
            "fps":"I love FPS games!", 
            "creativity":"I think Creativity games are the best!",
            "adventure":"I think Adventure games are the best!", 
            "animation":"The animation was great! I think the creators did an amazing job dont you think?", 
            "action":"Action is great!!"},

            {"typename": "Sadodere",
            "strategy": "strategy. That sounds so much like you!",
            "horror":"That wasnt scary at all!",
            "fps":"I love FPS games!",
            "creativity":"I think Creativity games are the best!",
            "adventure":"I think Adventure games are the best!",
            "animation":"The animation was great! I think the creators did an amazing job dont you think?", 
            "action":"Action is great!!"},

            {"typename": "Kamidere", 
            "strategy": "I enjoy strategy. I think its incredibly vital to act logically in a relationship.",
            "horror":"That wasnt scary at all!", 
            "fps":"I love FPS games!", 
            "creativity":"I think Creativity games are the best!",
            "adventure":"I think Adventure games are the best!", 
            "animation":"The animation was great! I think the creators did an amazing job dont you think?", 
            "action":"Action is great!!"},

        ]

        global gfgamingresponse
        gfgamingresponse = [
            {"typename":"Tsundere", "poor":"That wasnt really fun.", "medium": "I had a good time i guess, but thats to be expected! its a game after all.", "good":"Again! Lets play again! That was really nice!"},
            {"typename":"Yandere", "poor":"I will try to do better next time.", "medium": "That was mediocre at best. Developers are terrible!", "good":"That was amazing. please get more love points so you can do me <3."},
            {"typename":"Dandere", "poor":"I.. think we should try again?", "medium": "that was fine!", "good":"I... really enjoyed that! Lets do it again soon?"},
            {"typename":"Kuudere", "poor":"You are really bad! Its alright though.", "medium": "That was ok i guess, You arent really the best at this game are you?", "good":"You are pretty good actually."},
            {"typename":"Sweet", "poor":"You are really bad! Its alright though.", "medium": "That was ok i guess, You arent really the best at this game are you?", "good":"You are pretty good actually."},
            {"typename":"Sadodere", "poor":"You are really bad! Its alright though.", "medium": "That was ok i guess, You arent really the best at this game are you?", "good":"You are pretty good actually."},
            {"typename":"Kamidere", "poor":"You are really bad! Its alright though.", "medium": "That was ok i guess, You arent really the best at this game are you?", "good":"You are pretty good actually."},

        ]
        global typepraise
        typepraise = [
            {"typename": "Tsundere", "text": "we should text more often.. I care about you a lot.", "gaming":"I really like playing games!", "movies":"I love movies. ", "relaxing":"I love this quality time with you!"},
            {"typename": "Yandere", "text": "Lets text more! I want to know everything about you<3", "gaming":"Gaming is incredibly fun with you. We should do this more often.", "movies":"I love movies. ", "relaxing":"I love this quality time with you!"},
            {"typename": "Dandere", "text": "...lets do this more often?", "gaming":"I.. really enjoyed that!! maybe we could play more often?", "movies":"I love movies. ", "relaxing":"I love this quality time with you!"},
            {"typename": "Kuudere", "text": "Text me more often.", "gaming":"That was fun. We will play more often from now on.", "movies":"I love movies. ", "relaxing":"I love this quality time with you!"},
            {"typename": "Sweet", "text": "I love the text! Thank you for keeping me in touch!", "gaming":"wooW! Im so happy we could play games together! Im glad you remembered that I like gaming!", "movies":"I love movies. I love you so much!! ", "relaxing":"I love this quality time with you!"},
            {"typename": "Sadodere", "text": "I found that satisfactory! dont get any weird ideas, though!", "gaming":"I wonder how you knew I like gaming? Pervert!!", "movies":"I love movies. ", "relaxing":"I love this quality time with you!"},
            {"typename": "Kamidere", "text": "I found that enjoyable. Texting is in fact, the most practical form of communication. I appreciate you.", "gaming":"I found that enjoyable. Thank you for this. We should play more often.<3", "movies":"I love movies. ", "relaxing":"I love this quality time with you!"},

        ]              
    @commands.Cog.listener()
    async def setup(self, ctx):
        try:
            mulah.insert_one({"id":ctx.author.id, "setup":1})
            await ctx.channel.send("done!")
        except:
            await ctx.channel.send("you are already set up!")

    @commands.command()
    async def work(self, ctx):
        global achievementpercent
        workk = mulah.find_one({"id" : ctx.author.id}, {"money"})


        try:
            hourlywage = 15
            newmoney = workk["money"] + hourlywage
            mulah.update_one({"id":ctx.author.id},{"$set":{"money":newmoney}})
            embed = discord.Embed(title = "You have made %s dollars."%(hourlywage), description = "You now have $%s"%(newmoney),color = ctx.author.color)
            await ctx.channel.send(embed = embed)
        except KeyError:
            print(traceback.format_exc())
            mulah.update_one({"id":ctx.author.id}, {"$set":{"money":0}})
            await ctx.channel.send("Hey! I just finished making your economy profile. use `^work` to get money.")







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
                            embed.add_field(name = "%s| %s"%(x["name"],achievementcheck(p1,x["name"])), value = x["desc"], inline = False)

                if rawreaction == "❤️":
                    try:
                        gfval = mulah.find_one({"id":p1.id}, {"gf"})["gf"]
                        embed = discord.Embed(title = "%s's Relationship Achievements"%(p1.display_name), description = "If only %s was real."%(gfval["name"]), color = p1.color)
                    except:
                        embed = discord.Embed(title = "%s's Relationship Achievements"%(p1.display_name), description = "If only You had a gf", color = p1.color)
  
                    for x in achievements:
                        if x["category"]=="relationships":
                            embed.add_field(name = "%s| %s"%(x["name"],achievementcheck(p1,x["name"])), value = x["desc"], inline = False)                    
                if rawreaction == "🎮":
                    embed = discord.Embed(title = "%s's Gaming Achievements"%(p1.display_name), value = "Are you a true gamer?", color = p1.color)
                    for x in achievements:
                        if x["category"]=="gaming":
                            embed.add_field(name = "%s| %s"%(x["name"],achievementcheck(p1,x["name"])), value = x["desc"], inline = False)
                
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
                    embed = discord.Embed(title = "Choose your type!", description = "a| tsundere\n b| yandere\n c|dandere\n d|kuudere\n e|Sweet\n f|Sadodere\n g|Kamidere", color = ctx.author.color)
                    await ctx.channel.send(embed = embed)
                    try:
                        gftype = await self.client.wait_for('message', check = check, timeout = 30.0)
                        for z in gftypes:
                            print("here")
                            if ("letter", str(gftype.content)) in z.items():
                                print("here2")
                                
                                newdictionary["type"] = z["typename"]
                                print("this worked")
                                favoritesub = ["foreign language", "Math", "Computer Science", "biology", "chemistry", "Physics", "art", "gender studies", "business", "political sciences", "english."]

                                glikes = ["horror", "adventure", "creativity", "strategy", "fun", "thriller","fps", "comedy", "animation", "action", "romance", "drama"]
                                
                                likes = ["food", "texting", "gaming", "social media", "relaxing", "movies"]

                                randlikes = random.choice(likes)
                                randsub = random.choice(favoritesub)
                                genre = random.choice(glikes)
                                randdislikes = random.choice(glikes)
                                if randdislikes == genre:
                                    while randdislikes==genre:
                                        randdislikes = random.choice(glikes)
                                
                                newdictionary["likes"] = randlikes
                                newdictionary["favorite subject"] = randsub
                                newdictionary["dislikes"] = randdislikes
                                newdictionary["favorite genre"] = genre
                                newdictionary["tier"] = 1
                                
                                embed = discord.Embed(title = "You are now dating %s!"%(newdictionary["name"]), description = "Here is her profile! you can access this at anytime using `^gfstats`", color = ctx.author.color)
                                print("this also worked")
                                for x in newdictionary.keys():
                                    embed.add_field(name = "%s:"%(x), value = newdictionary[x])
                                await ctx.channel.send(embed = embed)  
                                relationships = mulah.find_one({"id":ctx.author.id}, {"relationships"})["relationships"]
                                relationships+=1
                                mulah.update_one({"id":ctx.author.id}, {"$set":{"relationships":relationships}})
                                mulah.update_one({"id":ctx.author.id}, {"$set":{"gf":newdictionary}})
                                mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":100}})
                                break                     
                    except asyncio.TimeoutError:
                        await ctx.channel.send("You took to long to respond! I guess we arent doing this.")


                except asyncio.TimeoutError:
                    await ctx.channel.send("You took to long to respond! I guess we arent doing this.")
                
                

            else:
                await ctx.channel.send("You already have a girlfriend! Infidelity is disgusting. Shame on you.")
        except:
            try:
                mulah.insert_one({"id":ctx.author.id, "gf":0})
                mulah.update_one({"id": ctx.author.id}, {"$set":{"gf":0}})
                print(exception)
                await ctx.channel.send("I have set up your dating profile! Try `^getgf` again!")
            except:
                mulah.update_one({"id": ctx.author.id}, {"$set":{"gf":0}})
                print(exception)
                await ctx.channel.send("I have set up your dating profile! Try `^getgf` again!")

    @commands.command()
    async def debug(self, ctx, dictionary:str, member:discord.Member):
        z = mulah.find_one({"id":member.id}, {dictionary})
        await ctx.channel.send("%s"%(z))
        x = z[dictionary]
        await ctx.channel.send("%s"%(x))



            





    @commands.command()
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
                    print(gfdict["image"])
                    if gfdict["image"].startswith("http"):
                        print("yes, it starts with http")
                        embed.set_image(url = gfdict["image"])
                except:
                    print(traceback.format_exc())
                await ctx.channel.send(embed=embed)
                        
            except:
                print(traceback.format_exc())
                await ctx.channel.send("Get a Gf.")
                
        except:
            await ctx.channel.send("you/they dont have a girlfriend")
      
        








    @commands.command()
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
    async def relationshipstat(self,ctx, name:discord.Member=None):
        if name is None:
            gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})
            lovevar = mulah.find_one({"id":ctx.author.id}, {"lp"})
            embed = discord.Embed(title = "%s's Relationship status"%(ctx.author.display_name), color = ctx.author.color)
            if gfvar is None or gfvar["gf"] ==0:
                embed.add_field(name = "single", value = "f")
            else:
                embed.add_field(name = "Dating.", value = "%s"%(gfvar["gf"]["name"]))
                embed.add_field(name = "love points", value = "%s"%(lovevar["lp"]))
            await ctx.send(embed = embed)

        else:
            gfvar = mulah.find_one({"id":name.id}, {"gf"})
            lovevar = mulah.find_one({"id":name.id}, {"lp"})
            embed = discord.Embed(title = "%s's Relationship status"%(name.display_name), color = ctx.author.color)
            if gfvar is None or gfvar["gf"] ==0:
                embed.add_field(name = "single", value = "f")
            else:
                embed.add_field(name = "Dating.", value = "%s"%(gfvar["gf"]["name"]))
                embed.add_field(name = "love points", value = "%s"%(lovevar["lp"]))
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




    @shop.command()
    async def gamestop(self, ctx):
        embed = discord.Embed(title = "Game Shop!", description = "Buy games to play with your girlfriend!", color = ctx.author.color)
        global gameitems
        for x in gameitems:
            finalstring = ""
            for z in x.keys():
                if not z == "name":
                    if not z=="value":
                        extrastring = "%s: %s\n"%(z,x[z])
                        finalstring+=extrastring
            embed.add_field(name = "%s -$%s"%(x["name"], x["value"]), value = finalstring)
        await ctx.channel.send(embed=embed)

    @shop.command()
    async def pcmr(self, ctx):      
        embed = discord.Embed(title = "PC SHOP!", description = "upgrade your PC. no one wants to see you play an AAA game on a chromebook", color=ctx.author.color)
        global pcitems
        for x in pcitems:
            finalstring = ""
            for z in x.keys():
                if x[z]!=0:
                    extrastring = "%s: %s\n"%(z,x[z])
                    finalstring+=extrastring
            embed.add_field(name = "%s - $%s"%(x["name"], x["value"]), value = finalstring)

                    
        await ctx.channel.send(embed = embed)




    @commands.group(invoke_without_command=True)
    async def gfinteract(self, ctx, pg:int=None):
        gfinteractlist = [
            {"name": "📱text", "lpincrease": 15, "lprequired": 0, "itemrequired": "phone","category":"texting", "desc": "Text your girlfriend! you need a phone for this."},
            {"name": "🎥watchmovie", "lpincrease": 23, "lprequired":0, "itemrequired": "movieticket","category":"gaming","desc": "watch a movie with your girlfriend!"},
            {"name": "📺netflix", "lpincrease": 10, "lprequired":0, "itemrequired": "netflixsub","category":"relax", "desc": "watch netflix with your girlfriend"},
            {"name": "🍴date", "lpincrease": 20, "lprequired":0, "itemrequired": None,"category":"relax", "desc": "go on a date with your girlfriend!"},
            {"name": "🎮Playmc", "lpincrease": 25, "lprequired": 0, "itemrequired": "laptop","category":"gaming", "desc":"Play Minecraft With your girlfriend! You need a laptop for this."},
            {"name": "💋Kiss", "lpincrease":40, "lprequired" : 200, "itemrequired": None,"category":None, "desc": "Kiss your girlfriend!"},
            {"name": "🤗hug", "lpincrease":25, "lprequired": 150, "itemrequired": None,"category":None,"desc": "Hug your girlfriend! A great way to bond."},
            {"name": "❤️boink", "lpincrease": 100, "lprequired": 800, "itemrequired": None,"category":None, "desc":"boink your girlfriend! Late game move."},
            {"name": "💍Propose", "lpincrease": 1000, "lprequired": 1600, "itemrequired": "ring","category":None, "desc": "Finally. You have the love of your life. Go live happily ever after."}]
        if pg is None:
            embed = discord.Embed(title = "Interact with Your Girlfriend!", description = "Use `^gf <command>`", color = ctx.author.color)
            for x in range(len(gfinteractlist)):
                value = gfinteractlist[x]
                embed.add_field(name = "%s➡️ +lp:%s"%(value["name"], value["lpincrease"]), value = "*love point requirement: %s \n Item requirement: %s \n Description:%s "%(value["lprequired"],value["itemrequired"],value["desc"], ), inline = False)
            embed.set_footer(text ="page 1")
            await ctx.channel.send(embed=embed)



    @commands.group(invoke_without_command=True)
    async def gf(self,ctx):
        await ctx.send("use a command, baka.")



    @gf.command()
    async def talk(self, ctx):
        global backgrounds
        alphlist = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
        global talkmap
        gfval = mulah.find_one({"id":ctx.author.id},{"gf"})["gf"]
        decidingint = random.randint(1,2)
        if decidingint == 1:
            embed = discord.Embed(title = "%s"%(gfval["name"]), description = "Hello! did something happen?", color = ctx.author.color)
            try:
                embed.set_image(url = gfval["image"])
            except:
                pass
            embed.set_footer(text="tell %s about your day!"%(gfval["name"]))
            await ctx.channel.send(embed=embed)
            def check(m):
                return m.author==ctx.author and m.channel==ctx.channel
            msg = await self.client.wait_for('message', check = check)
            emotiondict = te.get_emotion(msg.content)
            print(emotiondict)
            highestemotelen = 0
            highestemote=""
            for x in emotiondict.keys():
                if emotiondict[x]>highestemotelen:
                    highestemotelen = emotiondict[x]
                    highestemote=x
            highestemote = highestemote.lower()
            print(highestemote)
            if highestemote == "fear":
                highestemote = "scared"
            if highestemote == "surprise":
                highestemote = "sad"
            if highestemote == "":
                highestemote = random.choice(["angry", "sad", "happy", "scared"])
            action = highestemote
        elif decidingint == 2:
            action = random.choice(["sadgf", "angrygf", "scaredgf", "happygf"])
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
            print(action)
            if action in ["comfortgf", "yeah sure what?"]:
                action = random.choice(["comfortgf1", "comfortgf2", "comfortgf3","comfortgf4"])
            if action in ["gaming", "movies", "netflix"]:
                cmd = self.client.get_command("gf "+action)
                await cmd(ctx)
                break
            print(action)
            print(str(action))
            talkdict = next(x for x in talklistdict if x["action"] == str(action))
            print(talkdict["background"])
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
                        print(backgrounds)
                        print(backgroundict)
                        print(backgroundict["name"])
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
                    print("nonono")
                    print(traceback.format_exc())
                    embed.set_image(url = gfval[talkdict["img"]])
            except:
                try:
                    embed.set_image(url = gfval["image"])
                except:
                    print(traceback.format_exc())
                    print("cant get image smh")

            try:
                await editthis.delete()
                editthis = await ctx.channel.send(embed=embed, file = file)
            except:
                try:
                    print(traceback.format_exc())
                    print("yesss")
                    editthis = await ctx.channel.send(embed=embed, file = file)
                except:
                    editthis = await ctx.channel.send(embed=embed)

            if action == "leave":
                end = True
                break
            for x in reactions:
                await editthis.add_reaction(x)

            def check(reaction,user):
                return user==ctx.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'] and reaction.message == editthis  
            confirm = await self.client.wait_for('reaction_add', check=check)
            if confirm:
                action = emptydict[str(confirm[0])]
                print("this worked. the action is %s"%(action))





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
        
        
        
        
        
        
        




    @gf.command()
    async def text(self,ctx):
        global gftypes, typeconplaint, typepraise  
        try:
            textdict = {"name": "📱text", "lpincrease": 15, "lprequired": 0, "itemrequired": "phone","category":"texting", "desc": "Text your girlfriend! you need a phone for this."}
            authorgf = mulah.find_one({"id":ctx.author.id}, {"gf"})
            authorgfname = authorgf["gf"]["name"]
            authorgflikes = authorgf["gf"]["likes"]
            authorgfdislikes = authorgf["gf"]["dislikes"]
            authorgffavoritesub = authorgf["gf"]["favorite subject"]
            authorgftype = authorgf["gf"]["type"]
            authorgfgenre = authorgf["gf"]["favorite genre"]
            authorlp = mulah.find_one({"id":ctx.author.id}, {"lp"})
            authorlp = authorlp["lp"]
            if authorlp>=textdict["lprequired"]:
                if textdict["itemrequired"] is not None:
                    try:
                        authoritem = mulah.find_one({"id":ctx.author.id}, {"inv"})
                        authoritemlist = authoritem["inv"]
                        xlist = []
                        for x in authoritemlist:
                            
                            if ("name", textdict["itemrequired"]) in x.items():

                                xlist.append(x)
                                embed = discord.Embed(title = "You texted %s!"%(authorgfname), color = ctx.author.color)

                                listofwords = ["love", "dinner", "yogurt", "cake", "steak", "bed", "couch", "plans", "steak", "cuddle"]
                                randchoice = random.choice(listofwords)
                                nrandchoice = list(randchoice)
                                random.shuffle(nrandchoice)
                                nrandchoice = "".join(nrandchoice)
                                checklist = []
                                for x in range(3):
                                    await ctx.channel.send(" you have %s chances! Unscramble the word `%s`"%(3-x,nrandchoice))
                                    def check(m):
                                        return m.author == ctx.author and m.channel == ctx.channel
                                    try:
                                        guess = await self.client.wait_for('message', check=check, timeout=10.0)
                                    except asyncio.TimeoutError:
                                        await ctx.channel.send(f'you took too long. it was {randchoice}.')
                                        gfsat = random.randint(10,20)
                                        break
                                    if guess.content == randchoice:
                                        gfsat = random.randint(100-(x*20/1+x),150-(x*20/1+x))
                                        checklist.append(x)
                                        break
                                if not checklist:
                                    gfsat = 40
                                extrastring = " "

                                if authorgflikes == textdict["category"]:
                                    gfsat = gfsat*1.15
                                    for x in typepraise:
                                        if authorgftype == x["typename"]:
                                            extrastring = x["text"]
                                            break                                    
                                elif authorgfdislikes == textdict["category"]:
                                    gfsat = gfsat*.85
                                    for x in typeconplaint:
                                        if authorgftype == x["typename"]:
                                            extrastring = x["text"]
                                            break
                                else:
                                    print("shit didnt work!")
                                newgfsat = math.floor((gfsat/100)*textdict["lpincrease"])


                                for x in gftypes:
                                    if authorgftype == x["typename"]:
                                        if gfsat <50:
                                            embed.add_field(name = "%s:"%(authorgfname), value = "%s "%(x["textresponse"][0])+ "%s"%(extrastring))
                                        elif 50<=gfsat<100:
                                            embed.add_field(name = "%s:"%(authorgfname), value = "%s "%(x["textresponse"][1])+ "%s"%(extrastring))
                                        else:
                                            embed.add_field(name = "%s:"%(authorgfname), value = "%s "%(x["textresponse"][2])+ "%s"%(extrastring))

                                newauthorlp = authorlp+newgfsat
                                mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":newauthorlp}})
                                embed.set_footer(text = " You have gained %s love points"%(newgfsat))    
                                try:
                                    embed.set_image(url = "%s"%(authorgf["gf"]["image"]))      
                                except:
                                    print(traceback.format_exc())
                                    pass
                                await ctx.channel.send(embed = embed)
                                break
                        if len(xlist) ==0:
                            await ctx.channel.send("you need a %s"%(textdict["itemrequired"]))
                    except Exception as e:
                        print(traceback.format_exc())
                        await ctx.channel.send("you need a %s"%(textdict["itemrequired"]))


                else:
                    embed = discord.Embed(title = "You texted %s!"%(authorgfname), color = ctx.author.color)

                    listofwords = ["love", "dinner", "yogurt", "cake", "steak", "bed", "couch", "plans", "steak", "cuddle"]
                    randchoice = random.choice(listofwords)
                    nrandchoice = list(randchoice)
                    random.shuffle(nrandchoice)
                    nrandchoice = "".join(nrandchoice)
                    checklist = []
                    for x in range(3):
                        await ctx.channel.send(" you have %s chances! Unscramble the word `%s`"%(3-x,nrandchoice))
                        def check(m):
                            return m.author == ctx.author and m.channel == ctx.channel
                        try:
                            guess = await self.client.wait_for('message', check=check, timeout=10.0)
                        except asyncio.TimeoutError:
                            await ctx.channel.send(f'you took too long. it was {randchoice}.')
                            gfsat = random.randint(10,20)
                            break
                        if guess.content == randchoice:
                            gfsat = random.randint(100-(x*20/1+x),150-(x*20/1+x))
                            checklist.append(x)
                            break
                    if not checklist:
                        gfsat = 40

                    if authorgflikes == textdict["category"]:
                        gfsat = gfsat*1.15
                    elif authorgfdislikes == textdict["category"]:
                        gfsat = gfsat*.85
                    else:
                        print("shit didnt work!")
                    newgfsat = math.floor((gfsat/100)*textdict["lpincrease"])


                    for x in gftypes:
                        if authorgftype == x["typename"]:
                            if gfsat <50:
                                embed.add_field(name = "%s:"%(authorgfname), value = "%s"%(x["textresponse"][0]))
                            elif 50<=gfsat<100:
                                embed.add_field(name = "%s:"%(authorgfname), value = "%s"%(x["textresponse"][1]))
                            else:
                                embed.add_field(name = "%s:"%(authorgfname), value = "%s"%(x["textresponse"][2]))

                    newauthorlp = authorlp+newgfsat
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":newauthorlp}})
                    embed.set_footer(text = " You have gained %s love points"%(newgfsat))          
                    await ctx.channel.send(embed = embed)

            else:
                await ctx.channel.send("you dont have enough love points! You need %s more"%(textdict["lprequired"]-authorlp))
            
        except:
            await ctx.channel.send("You need a girlfriend for this, baaka.")

    @gf.command()
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
            print(emotionlist, emotionlist)
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
                            print(emptydict[reactionstr])
                            embed = discord.Embed(title = "input a url to update image", description = "url must be http or https", color = ctx.author.color)
                            await msg.clear_reactions()
                            await msg.edit(embed = embed)

                            def check3(m):
                                return m.author==ctx.author and m.channel==ctx.channel
                            confirm3 = await self.client.wait_for('message', check=check3)
                            turl = confirm3.content
                            emotion = emptydict[reactionstr]
                            print(emotion)
                            if emotion is None:
                                emotion = "image"
                            if emotion.lower() in emotionlist:
                                if turl.startswith('http'):
                                    print("yes it starts")
                                    print(turl)
                                    try:
                                        gfdict[emotion] = turl
                                        mulah.update_one({"id":ctx.author.id}, {"$set":{"gf":gfdict}})
                                        embed = discord.Embed(title = "You have updated %s's %s"%(gfdict["name"], emotion), color = ctx.author.color)
                                        embed.set_image(url = turl)
                                        await ctx.channel.send(embed = embed)
                                    except:
                                        print(traceback.format_exc())
                                        await ctx.channel.send("Get a girlfriend first")
                                else:
                                    await ctx.channel.send("make sure its http or https")
                            else:
                                await ctx.channel.send("you need a valid emotion! There is %s"%(",".join(emotionlist)))
                        if reactionstrr =='⬅️':
                            pass
                        await msg.clear_reactions()





    @gf.command()
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
        print(emptydict)
        print(pcnames)
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
                                        pass
                                        
                                    else:
                                        skillint =4

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
                                    responsedict = next(item for item in gfgamingresponse if item["typename"] == gfval["type"])
                                    finalstring = ""
                                    gflikesgaming = next(item for item in typepraise if item["typename"] == gfval["type"])
                                    gfgenrebad = next(item for item in typeconplaint if item["typename"] == gfval["type"])
                                    gfgenregood = next(item for item in typegenrepraise if item["typename"] == gfval["type"])
                                    gamedict = next(item for item in gameitems if item["name"] == newdict[msg.content])
                                    gfsat = gamedict["lpincrease"]*(skilldict[newdict[msg.content]]/100)
                                    if skilldict[newdict[msg.content]]<35:
                                        finalstring+="%s"%(responsedict["poor"])
                                        print(finalstring)
                                    elif 35<=skilldict[newdict[msg.content]]<45:
                                        finalstring+="%s"%(responsedict["medium"])
                                        print(finalstring)
                                    elif 45<=skilldict[newdict[msg.content]]:
                                        finalstring+="%s"%(responsedict["good"])
                                        print(finalstring)

                                    dislikes = False
                                    if gfval["likes"] == "gaming":
                                        finalstring+="%s"%(gflikesgaming["gaming"])
                                        gfsat= gfsat*(115/100)
                                        print(finalstring)
                                    if gfval["dislikes"] in gamedict["genre"]:
                                        dislikes = True
                                        finalstring+="%s"%(gfgenrebad[gfval["dislikes"]])
                                        gfsat= gfsat*(85/100)
                                        print(finalstring)
                                    elif gfval["favorite genre"] in gamedict["genre"]:
                                        finalstring+="%s"%(gfgenregood[gfval["favorite genre"]])
                                        gfsat= gfsat*(115/100)
                                        print(finalstring)

                                    

                                        
                                    embed = discord.Embed(title = "You played %s with %s!"%(newdict[msg.content], gfval["name"]), color = ctx.author.color)

                                    embed.add_field(name = "%s:"%(gfval["name"]), value = finalstring)
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
                                    await ctx.channel.send(embed=embed)
                                else:
                                    await ctx.channel.send("Your PC does not meet the requirements. You should look at system requirements before installing a game!")
                                    
                            else:
                                await ctx.channel.send("You were supposed to type a letter, Baka.")


                                


                                ##code
                        except asyncio.TimeoutError:
                            await ctx.channel.send("You took too long! i guess we arent doing this.")
                    else:
                        embed = discord.Embed(title = "%s"%(gfval["name"]), description = "you have any games on this pc, %s"%(ctx.author.display_name), color = ctx.author.color)
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
    async def give(self, ctx, itemtogive, p1:discord.Member):
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        p1invar = mulah.find_one({"id":p1.id}, {"inv"})
        p1inval = p1invar["inv"]
        itemcheck = []
        for x in inval:
            if x["name"].casefold() ==itemtogive: 
                print("this got here1")
                for z in p1inval:
                    if ("name", x["name"]) in z.items():
                        z["amount"]+=1
                        print("noo")
                        itemcheck.append("yes")
                        
                        x["amount"]-=1
                        if x["amount"] == 0:
                            inval.remove(x)
        print(itemcheck)
                        

        if not itemcheck:
            print("yes")
            for x in inval:
                if x["name"].casefold()==itemtogive.lower():
                    print("this got here2")
                    x["amount"]-=1
                    print(x)
                    if x["amount"] == 0:
                        inval.remove(x)
                    pdict = x
                    print(pdict)
                    pdict["amount"] = 1
                    p1inval.append(pdict)
                    print(p1inval)

        mulah.update_one({"id":p1.id}, {"$set":{"inv":p1inval}})
        mulah.update_one({"id":ctx.author.id}, {"$set":{"inv":inval}})
        embed = discord.Embed(title = "You have given %s one %s"%(p1.display_name, itemtogive), color = ctx.author.color)
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




    @gf.command()
    async def movies(self,ctx):
        global typegenrepraise
        global typeconplaint
        global typepraise
        global gftypes
        invar = mulah.find_one({"id":ctx.author.id},{"inv"})   
        inval = invar["inv"]     
        ticketcheck = next((item for item in inval if item["name"] == "movieticket"), None)
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
            print(movielist)
            print(emptydict)


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
                    print(genre)
                    print(gfval["favorite genre"])
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
                            print(traceback.format_exc())
                            pass
                        gfsat*=115/100
                    if gfval["likes"] == "movies":
                        dialogue += next(item for item in typepraise if item["typename"] == gfval["type"])["movies"]
                        gfsat+=115/100
                    embed = discord.Embed(title = "You watched %s with %s"%(emptydict[msg.content],gfval["name"]), color = ctx.author.color)
                    embed.add_field(name = "%s:"%(gfval["name"]), value = dialogue)
                    try:
                        embed.set_image(url = "%s"%(gfval["image"]))
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
    async def removegf(self,ctx,p1:discord.Member):
        if str(ctx.author) == "SentientPlatypus#1332":
            mulah.update_one({"id":p1.id},{"$set":{"gf":0}})
            mulah.update_one({"id":p1.id},{"$set":{"lp":0}})
            await ctx.channel.send("Ok creator senpai! I removed %s gf!"%(p1.display_name))





















    @gf.command()
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
                
            embed = discord.Embed(title = "%s:"%(gfval["name"]), description = random.choice(typemap["invite"]).format(author = ctx.author.display_name), color = ctx.author.color)
            embed.add_field(name = "Where do you take her?", value = finalstring)

            try:
                embed.set_image(url = gfval["image"])
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
                    print(order)
                    gforder = random.choice(menu)
                    try:
                        order = order.format(order = gforder)
                    except:
                        try:
                            order = order.format(order=gforder,author = ctx.author.display_name)
                        except:
                            pass

                    print(order)
                    count = 0
                    emptydict = {}
                    reactions = []
                    finalstring = ""
                    print(restaurant["menu"])
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
                    editthis = await ctx.channel.send(embed=embed,file = file)
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
                            print('ye')
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
                    editthis = await ctx.channel.send(embed=embed,file = file)    
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
                        embed.set_image(url = restaurant["waiter"])
                        walletval-=bill
                        mulah.update_one({"id":ctx.author.id}, {"$set":{"money":walletval}})
                        embed.set_footer(text = "your balance is now $%s!"%(walletval))

                        dates+=1
                        mulah.update_one({"id":ctx.author.id}, {"$set":{"dates":dates}})
                        await editthis.clear_reactions()
                        await editthis.delete()
                        editthis = await ctx.channel.send(embed=embed)                        

                    


        if choice == "react":
            embed = discord.Embed(title = "%s:"%(gfval["name"]), description = random.choice(typemap["react"]), color = ctx.author.color)
            try:
                embed.set_image(url = gfval["image"])
            except:
                pass
            editthis = await ctx.channel.send(embed=embed)
        




    @commands.command()
    async def buy(self,ctx, item:str, number:int=None):
        global shopitems
        global pcitems     
        global gameitems
        allitems = pcitems+shopitems+gameitems
        xvalue = []
        for x in itertools.chain(pcitems, shopitems, gameitems):
            itemm = x
            if item.lower() == itemm["name"].casefold():
                xvalue.append(x)
                itemvalue = itemm["value"]
                itemdesc = itemm["desc"]
                walletvar = mulah.find_one({"id":ctx.author.id}, {"money"})
                walletval = walletvar["money"]
                print(walletval, walletvar)
                if itemvalue<=walletval:
                    itemfind = mulah.find_one({"id":ctx.author.id}, {"inv"})
                    try:
                        if number is None:
                            number = 1                     
                        if itemvalue<=walletval*number:
                            listtt = itemfind["inv"]
                            listvr = []
                            newwallet = walletval-itemvalue*number
                            mulah.update_one({"id":ctx.author.id}, {"$set":{"money":newwallet}})                              
                            for x in range(len(listtt)):
                                z =  listtt[x]
                                if ("name", itemm["name"]) in z.items():
                                    z["amount"]+=number
                                    listvr.append(x)
                                    break

                            if not listvr:
                                listtt.append({"name":itemm["name"], "amount":number, "desc": "%s"%(itemdesc)})
                            mulah.update_one({"id":ctx.author.id}, {"$set":{"inv":listtt}})
                            embed = discord.Embed(title = "Purchase successfull!", description = "You have purchased %s %s"%(number,itemm["name"]), color = ctx.author.color)
                            await ctx.channel.send(embed = embed)
                            break         
                        else:
                            await ctx.channel.send("You dont have enough money") 
                    except:
                        mulah.update_one({"id":ctx.author.id}, {"$set":{"inv": []}})
                        await ctx.channel.send("I have set up your inventory! try buying something again!")         
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

        def dbcheck(user,key):
            try:
                mulah.find_one({"id":user.id}, {key})[key]
            except:
                mulah.update_one({"id":p1.id}, {"$set":{key:0}})
        for x in ["breakups", "kisses", "boinks"]:
            dbcheck(p1, x)
        breakupval = mulah.find_one({"id":p1.id}, {"breakups"})["breakups"]
        kissval = mulah.find_one({"id":p1.id}, {"kisses"})["kisses"]
        boinkval = mulah.find_one({"id":p1.id}, {"boinks"})["boinks"]
        proposeval = mulah.find_one({"id":p1.id}, {"proposes"})["proposes"]
        relationships = mulah.find_one({"id":p1.id}, {"relationships"})["relationships"]
        dates = mulah.find_one({"id":p1.id}, {"dates"})["dates"]
        embed = discord.Embed(title = "%s' Profile!"%(p1.display_name), description = "Use the reactions to navigate the profile!", color = ctx.author.color)
        embed.set_image(url = p1.avatar_url)
        reactions = ["💰","❤️","🎮", "🏆","💼", "🚪"]
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
                if rawreaction == "💰":
                    try:
                        walletval = mulah.find_one({"id":p1.id}, {"money"})["money"]
                        embed = discord.Embed(title = "%s's Financial stability!"%(p1.display_name), color = ctx.author.color)
                        embed.set_image(url = p1.avatar_url)
                        embed.add_field(name ="Current balance:", value = "$%s"%(walletval))
                    except:
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
                    global achievementcheck  
                    global achievements
                    try:
                        achievementval = mulah.find_one({"id":p1.id}, {"achievements"})["achievements"]
                        embed = discord.Embed(title = "%s's achievements!"%(p1.display_name), description = "use ^achievements for a more detailed view!", color = ctx.author.color)
                        for y in achievementval:
                            achievementdict = next(x for x in achievements if x["name"] ==y)
                            embed.add_field(name = y+" "+achievementcheck(p1,y), value = achievementdict["desc"], inline = False)


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

    @commands.command()
    async def editDB(self,ctx, key, val:int, p1:discord.Member=None):
        if str(ctx.author)=="SentientPlatypus#1332":
            if p1 ==None:
                p1=ctx.author
            mulah.update_one({"id":p1.id}, {"$set":{key:val}})
            await ctx.channel.send("ok creator senpai! i did it.")

    @gf.command()
    async def netflix(self,ctx):
        global typegenrepraise
        global typeconplaint
        global typepraise
        global gftypes
        invar = mulah.find_one({"id":ctx.author.id},{"inv"})   
        inval = invar["inv"]     
        ticketcheck = next((item for item in inval if item["name"] == "netflixsub"), None)   
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
            print(movielist)
            print(emptydict)


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
                            print(traceback.format_exc())
                            pass
                        gfsat*=115/100
                    if gfval["likes"] == "relaxing":
                        dialogue += next(item for item in typepraise if item["typename"] == gfval["type"])["relaxing"]
                        gfsat+=115/100
                    embed = discord.Embed(title = "You watched %s with %s"%(emptydict[msg.content.lower()],gfval["name"]), color = ctx.author.color)
                    embed.add_field(name = "%s:"%(gfval["name"]), value = dialogue)
                    try:
                        embed.set_image(url = "%s"%(gfval["image"]))
                    except:
                        pass
                    lpval+=math.floor(gfsat)
                    embed.set_footer(text="You gained %s Love points."%(math.floor(gfsat)))
                    await ctx.channel.send(embed=embed)
                    mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})

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

    @gf.command()
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
            if lpval>=150:
                embed = discord.Embed(title = "You hugged %s!"%(gfval["name"]), color = ctx.author.color)
                dialogue = next(item for item in gftypes if item["typename"] == gfval["type"])["hugresponse"]

                embed.add_field(name = "%s:"%(gfval["name"]), value = dialogue)
                try:
                    embed.set_image(url=gfval["image"])
                except:
                    pass
                embed.set_footer(text = "You have gained 25 Love points!")
                await ctx.channel.send(embed=embed)
                lpval+=25
                mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})
            else:
                await ctx.channel.send("You dont have enogh love points")
        except:
            await ctx.channel.send("You need a girlfriend lmao")
    @gf.command()
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
                dialogue = next(item for item in gftypes if item["typename"] == gfval["type"])["kissresponse"]

                embed.add_field(name = "%s:"%(gfval["name"]), value = dialogue)
                try:
                    embed.set_image(url=gfval["embarrased"])
                except:
                    try:
                        embed.set_image(url=gfval["image"])
                    except:
                        pass
                if gfval["tier"] == 1:
                    
                    gfval["tier"] = 2
                    embed.add_field(name = "%s levelled up!"%(gfval["name"]),value = "She is now a tier %s girlfriend!"%(gfval["tier"]))
                    mulah.update_one({"id":ctx.author.id},{"$set":{"gf":gfval}})
                else:
                    pass
                UserAchievements = mulah.find_one({"id":ctx.author.id},{"achievements"})["achievements"]
                kisses = mulah.find_one({"id":ctx.author.id},{"kisses"})["kisses"]
                kisses+=1
                mulah.update_one({"id":ctx.author.id},{"$set":{"kisses":kisses}})

                embed.set_footer(text = "You have gained 40 Love points!")
                await ctx.channel.send(embed=embed)
                lpval+=40
                mulah.update_one({"id":ctx.author.id},{"$set":{"lp":lpval}})
            else:
                await ctx.channel.send("You dont have enogh love points")
        except:
            await ctx.channel.send("You need a girlfriend lmao")










    @gf.command()
    async def boink(self,ctx):
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

                        


                    print(gfval["tier"])
                    if gfval["tier"]<3:
                        gfval["tier"] =3
                        embed.add_field(name = "%s levelled up!"%(gfval["name"]), value = "she is now tier %s"%(gfval["tier"]))
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"gf":gfval}})
                    lpval+=100
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"lp":lpval}})
                    await editthis.edit(embed=embed)
                    climaxx == True
                    break
                if action == "kiss":
                    kisses+=1
                    mulah.update_one({"id":ctx.author.id},{"$set":{"kisses":kisses}})


                if action == "pin down":
                    pinned = True
                if action in actionlist:
                    response = responsedict[action][1]
                else:
                    response = responsedict[action][0]
                if re.search("\{0\}", response):
                    print("this made it here")
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
                    editthis = await ctx.send(embed=embed) 
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
    async def propose(self,ctx):
        global gftypes
        gfvar = mulah.find_one({"id":ctx.author.id}, {"gf"})
        gfval = gfvar["gf"]
        lpvar = mulah.find_one({"id":ctx.author.id}, {"lp"})
        lpval = lpvar["lp"]    
        invar = mulah.find_one({"id":ctx.author.id}, {"inv"})
        inval = invar["inv"]
        if lpval>=1600:
            if next((x for x in inval if x["name"] == "ring"), None) is not None:
                if gfval["tier"] !=4:
                    response = next(x for x in gftypes if x["typename"] == gfval["type"])["proposeresponse"].format(ctx.author.display_name)
                    embed = discord.Embed(title = "You proposed to %s!"%(gfval["name"]), color = ctx.author.color)
                    embed.add_field(name = "%s"%(gfval["name"]), value=response)
                    try:
                        embed.set_image(url = gfval["image"])
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
                else:
                    if mulah.find_one({"id":ctx.author.id},{"proposes"})["proposes"]==0:
                        proposes = mulah.find_one({"id":ctx.author.id},{"proposes"})["proposes"]    
                        proposes+=1
                        mulah.update_one({"id":ctx.author.id}, {"$set":{"proposes":proposes}})
                    await ctx.channel.send("%s is already your fiance, baka."%(gfval["name"]))
            else:
                await ctx.channel.send("You need a ring to propose, bakaa. this is basic shit, man. come on.")

        else:
            await ctx.channel.send('You dont have enough Love points for that! come on bro, its gonna be weird if you move too quickly!')



    @commands.command()
    async def waitforclick(self, ctx):
        m = await ctx.send(
            "Buttons waiting for a click",
            components=[
                Button(style=ButtonStyle.red, label="Click Me!"),
            ],
        )

        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel

        try:
            res = await self.client.wait_for("button_click", check=check, timeout=15)
            await res.respond(
                type=InteractionType.ChannelMessageWithSource, content=f"{res.component.label} pressed"
            )

        except TimeoutError:
            await m.edit(
                "Prompt timed out!",
                components=[
                    Button(style=ButtonStyle.red, label="Timed out!", disabled=True),
                ],
            )

    @commands.command()
    async def button(self, ctx):
        await ctx.channel.send(
            "Here is an example of a button",
            components=[
                [
                    Button(style=ButtonStyle.red, label="EMOJI", emoji="😂"),
                    Button(style=ButtonStyle.green, label="GREEN"),
                    Button(style=ButtonStyle.red, label="RED", disabled=True),
                    Button(style=ButtonStyle.grey, label="GREY"),
                ],
                Button(style=ButtonStyle.blue, label="BLUE"),
                Button(style=ButtonStyle.URL, label="URL", url="https://www.example.com"),
            ],
        )







def setup(client):
    client.add_cog(currencysys(client))