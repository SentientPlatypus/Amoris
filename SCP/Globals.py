
from datetime import date
from inspect import trace
from logging import exception
from operator import mul
from os import name
from typing import AsyncContextManager, final
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
import pymongo
import ssl

uri = "mongodb+srv://scptsunderedatabase.fp8en.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
cluster = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=r'C:\Users\trexx\Documents\PYTHON CODE LOL\SCP-16-Tsundere-Discord-Bot\SCP\cert.pem')
mulah = cluster["discord"]["mulah"]
levelling = cluster["discord"]["levelling"]
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
def gamble(odds:int, times:int):
    count = 0
    wins = 0
    while count<=times:
        number = random.randint(1,odds)
        if number == 1:
            wins+=1
        else:
            pass
        count+=1
    return wins
    




def GetFirstKey(dict:dict):
    for x in dict:
        return x









##-------------------------------------------------------------INV FUNCTS
def RemoveFromInventory(user, item, AmountToRemove:int=None):
    if AmountToRemove==None:
        AmountToRemove=1
    inv = mulah.find_one({"id":user.id}, {"inv"})["inv"]
    itemdict = next(x for x in inv if x["name"].lower() ==item.lower())
    itemdict["amount"]-=AmountToRemove
    if itemdict["amount"]==0:
        inv.remove(itemdict)
    mulah.update_one({"id":user.id}, {"$set":{"inv":inv}})

def AddToInventory(user, item, ReferenceList:list, AmountToAdd:int=None):
    if AmountToAdd==None:
        AmountToAdd=1
    inv = mulah.find_one({"id":user.id}, {"inv"})["inv"]
    itemdict = next((x for x in inv if x["name"].lower() ==item.lower()), None)
    ThingToAdd = next(x for x in ReferenceList if x["name"].lower()==item.lower())
    if itemdict != None:
        itemdict["amount"]+=AmountToAdd
    else:
        inv.append({"name":ThingToAdd["name"], "amount":AmountToAdd, "desc": "%s"%(ThingToAdd["desc"])})
    mulah.update_one({"id":user.id}, {"$set":{"inv":inv}})


def InvCheck(user, item:str, Id=False, amount:int=1) -> bool:
    if Id==False:
        inv = mulah.find_one({"id":user.id}, {"inv"})["inv"]
        check = next((x for x in inv if x["name"].lower()==item.lower() and x["amount"]>=amount), None)
        if check == None:
            return False
        else:
            return True
    else:
        inv = mulah.find_one({"id":user}, {"inv"})["inv"]
        check = next((x for x in inv if x["name"].lower()==item.lower() and x["amount"]>=amount), None)
        if check == None:
            return False
        else:
            return True


def InvCheckWithItem(user, item:str, Id=False, amount:int=1):
    if Id==False:
        user = user.id
    inv = mulah.find_one({"id":user}, {"inv"})["inv"]
    check = next((x for x in inv if x["name"].lower()==item.lower() and x["amount"]>=amount and "parts" not in x.keys()), None)
    if check == None:
        return False
    else:
        return check
















##----------------------------------------------------Achievement Functs
def XpBar(val, max, fill=":blue_square:", empty=":white_large_square:", NumOfSquares=20, righttoleft=False):
    if righttoleft:
        valueOfBlue = math.floor((val/max)*NumOfSquares)
        if valueOfBlue<0:
            return empty*NumOfSquares
        valueofWhite = NumOfSquares-valueOfBlue
        finalstr = empty*valueofWhite+fill*valueOfBlue
        return finalstr   
    else:
        valueOfBlue = math.floor((val/max)*NumOfSquares)
        if valueOfBlue<0:
            return empty*NumOfSquares
        valueofWhite = NumOfSquares-valueOfBlue
        finalstr = fill*valueOfBlue+empty*valueofWhite
        return finalstr
    
    
def GetKeysFromDictInList(list:list):
    keys= []
    for x in list:
        for z in x.keys():
            keys.append(z)
    return keys

def GetLevel(id):
    xp = levelling.find_one({"id":id}, {"xp"})["xp"]
    lvl = 0
    while True:
        if xp < ((50*(lvl**2))+(50*(lvl))):
            break
        lvl+=1
    return lvl

def achievementcheck(user,achievement:str):
    try:
        value = mulah.find_one({"id":user.id}, {"achievements"})["achievements"]
        if achievement in value:
            return "✅"
        else:
            return "❌"
    except:
        return "❌"
        
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

def ChoiceParts(choices:list, ReactionsList = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']):
    count = 0
    reactionlist = []
    emptydict = {}
    finalstr = ""
    for x in choices:
        emptydict[ReactionsList[count]]=x
        reactionlist.append(ReactionsList[count])
        finalstr+="%s %s\n"%(ReactionsList[count], x)
        count+=1
    return [emptydict, finalstr, reactionlist]


async def AchievementEmbed(ctx, EarnedAchievement):

    UserAchievements = mulah.find_one({"id":ctx.author.id}, {"achievements"})["achievements"]
    if EarnedAchievement not in UserAchievements:
        AchievementDict = next(x for x in achievements if x["name"]==EarnedAchievement)
        embed = discord.Embed(title = "Congratulations! you earned the achievement %s"%(AchievementDict["name"]), description = AchievementDict["desc"], color = ctx.author.color)
        embed.set_image(url = 'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/socialmedia/apple/271/trophy_1f3c6.png')
        UserAchievements.append(EarnedAchievement)
        mulah.update_one({"id":ctx.author.id}, {"$set":{"achievements":UserAchievements}})
        embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)    





##-------------------------------------------------------------------------GLOBAL VARIABLES, DATASETS

def getEmotionList():
    return ["embarrassed", "horny","surprised","climax", "image", "bed", "angry", "fear", "sad", "dissapointed"]


def getAchievementList():
    return achievements

def getWorkLists():
    return [
            {"name":"McDonalds worker", "salary":15, "req":1, "words":["bigmac", "burger", "broken"], "sentences":["sorry, the icecream machine is broken", "what can I get for you?", "welcome to mcdonalds"]},
            {"name":"Gamer", "salary":150, "req": 5, "words":["dorito", "mechanical", "virgin"], "sentences":["i hate lag", "hes one tap", "what a sweat"]},
            {"name":"Business Man", "salary":160, "req":20, "words":["business", "passive", "pigeon"], "sentences":["sorry thats not passive income", "it is ten times cheaper to keep a customer than to get a new one"]},
            {"name":"Jeff bezos", "salary":1000000000, "req":100, "words":["bigmac", "burger", "broken"]},
        ]

def getShopItems():
    return [
            {"name":"phone", "value":800, "desc":"Text your Girlfriend!"},
            {"name": "netflixsub", "value": 29, "desc": "Netflix and chill with your gf"},
            {"name": "lotteryticket", "value": 2, "desc": "A chance to win 1 million dollars"},
            {"name": "movieticket", "value" : 16, "desc":"watch a movie with your gf"},
            {"name": "ring", "value" : 10000, "desc":"propose to your gf"},

        ]

def getBattleItems():
    return [
            {"name":"UpgradePoint", "value":2000, "desc":"`^upgrade` one of your stats!"},

            {"name":"Vaccine", 
            "type":"Heal",
            "desc":"Heal ig", 
            "rarity":"Legendary",
            "value":2000,
            "abilities":{"vaccine":1}},

            {"name":"Saitamas Dish Gloves", 
            "type":"hands", 
            "desc":"The Most powerful item in the game.",
            "rarity":"illegal", 
            "value":2000,
            "attribute":{"strength":1000000}},

            {"name":"Sharingan", 
            "type":"head", 
            "desc":"Op doujutsu",
            "rarity":"Legendary", 
            "value":2000,
            "abilities":{"Amaterasu":1, "Susanoo":1}},


            {"name":"Demon Destroyer", 
            "type":"primary", 
            "desc":"Can deflect spells completely!", 
            "rarity":"Legendary", 
            "value":2000,
            "abilities":{"Black Slash":1, "Deflect":1, "Black Divider":1}
            },

        ]

def getToolValues():
    return [
            {"name": "rifle", "value" : 400, "desc":"`^hunt` to get animals!"},
            {"name": "fishpole", "value" : 100, "desc":"`^fish` to catch fish!"},
            {"name":"pickaxe", "durability":59, "fortune":1, "craft":{"wood":5}, "value":25, "desc":"cheap mining"},
            {"name":"iron pickaxe", "durability":250, "fortune":2, "craft":{"wood":2, "iron":3}, "value":25, "desc":"better mining"},
            {"name":"gold pickaxe", "durability":33, "fortune":4, "craft":{"wood":2, "gold":3}, "value":115, "desc":"fine mining"},
            {"name":"diamond pickaxe", "durability":1562, "fortune":4, "craft":{"wood":2, "diamond":3}, "value":13010, "desc":"best mining"},

            {"name":"axe", "durability":59, "fortune":1, "craft":{"wood":4}, "value":29, "desc":"Chop wood"},
            {"name":"iron axe", "durability":250, "fortune":2, "craft":{"wood":2, "iron":3}, "value":25, "desc":"Chop more wood"},
            {"name":"gold axe", "durability":33, "fortune":4, "craft":{"wood":2, "gold":3}, "value":115, "desc":"Chop lots of wood"},
            {"name":"diamond axe", "durability":1562, "fortune":4, "craft":{"wood":2, "diamond":3}, "value":13010, "desc":"Chop even more wood"},

            {"name":"hoe", "durability":59, "fortune":1, "craft":{"wood":2}, "value":10, "desc":"Farm stuff idk"},
            {"name":"iron hoe", "durability":250, "fortune":2, "craft":{"wood":2, "iron":2}, "value":20, "desc":"Farm stuff idk"},
            {"name":"gold hoe", "durability":32, "fortune":4, "craft":{"wood":2, "gold":2}, "value":80, "desc":"Farm stuff idk"},
            {"name":"diamond hoe", "durability":1561, "fortune":4, "craft":{"wood":2, "diamond":2}, "value":8810, "desc":"Farm stuff idk"},
        ]

def getFarmItems():
    return [
            {"name":"uncommon fish", "value":10, "desc":"cheap fish to sell"},
            {"name":"common fish", "value":20, "desc":"a mediocre fish"},
            {"name":"rare fish", "value":50, "desc":"high quality fish"},
            {"name":"legendary fish", "value":150, "desc":"very valuable fish"},
            {"name":"mouse", "value":10, "desc":"idk why someone would even bother"},
            {"name":"rabbit", "value":50, "desc":"tste great in stew"},
            {"name":"deer", "value":150, "desc":"sells well"},
            {"name":"bigfoot", "value":1000, "desc":"make some mulah"},
            {"name":"coal", "value":1, "desc":"non renewable energy source"},
            {"name":"iron", "value":5, "desc":"for what"},
            {"name":"gold", "value":35, "desc":"terrible durability"},
            {"name":"diamond", "value":4400, "desc":"sells for a lot"},
            {"name":"ruby", "value":10000, "desc":"One of the most precious things in this world"},
            {"name":"wheat", "value":10, "desc":"carbs"},
            {"name":"beetroot", "value":20, "desc":"why do people eat this"},
            {"name":"melon", "value":50, "desc":"mmm"},
            {"name":"pumpkin", "value":150, "desc":"pumpkin pie tastes great"},
            {"name":"wood", "value":5, "desc":"profits pile up"},

        ]
def getPcItems():
    return [
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

def getGameItems():
    return [
            {"name":"Minecraft", "genre":["adventure", "creativity"],"space":1500, "value":26, "desc": "anything can run Minecraft!", "lpincrease":30, "recommendedspecs":{"totalram":8000, "power":1500}},
            {"name":"Fortnite", "genre":["fps"],"space":49000, "value":0, "desc": "How much lp were you expecting for fortnite?", "lpincrease":5, "recommendedspecs":{"totalram":8000, "power":2500}},
            {"name":"Valorant", "genre":["fps"],"space":14400, "value":0, "desc": "spend 80% of the game spectating.", "lpincrease":25, "recommendedspecs":{"totalram":8000, "power":3000}},
            {"name":"Terraria", "genre":["adventure", "creativity"],"space":100, "value":5, "desc": "A great friend of Mc", "lpincrease":20, "recommendedspecs":{"totalram":8000, "power":1500}},
            {"name":"Microsoft Flight simulator", "genre":["creativity"],"space":150000, "value":60, "desc": "You probably cant run this.", "lpincrease":40, "recommendedspecs":{"totalram":16000, "power":5000}},
            {"name":"Crysis 3", "genre":["adventure"],"space":17000, "value":5, "desc": "Your pc simply cant run this.", "lpincrease":50, "recommendedspecs":{"totalram":32000, "power":7800}},
            {"name":"League of Legends", "genre":["strategy"],"space":22000, "value":0, "desc": "Dont do it.", "lpincrease":-50, "recommendedspecs":{"totalram":8000, "power":2800}}
        ]

def getGameWords():
    return [
            {"name": "Minecraft", "words":["block", "redstone", "blockhit", "endcrystal"]},
            {"name": "Fortnite", "words":["build", "ninja", "virgin", "clap"]},
            {"name": "Valorant", "words":["hipfire", "slow", "spectator", "Operator"]},
            {"name": "Terraria", "words":["Terraria", "cheap", "fun", "pewdiepie"]},
            {"name": "Microsoft Flight Simulator", "words":["plane", "aviation", "pilot", "graphics"]},
            {"name": "Crysis 3", "words":["Block", "redstone", "blockhit", "endcrystal"]},
            {"name": "League of Legends", "words":["virgin", "discordmod", "glasses", "asian"]},
        ]

def getEnemyList():
    return [
            {"name":"Acnologia", 
            "health":5000, 
            "strength":800, 
            "defense":400, 
            "intelligence":1000,
            "mana":1000,
            "image":"https://static.wikia.nocookie.net/vsbattles/images/7/71/New_Human_Acnologia_Render.png/revision/latest/scale-to-width-down/400?cb=20200704092623", 
            "size":((160, 199)), 
            "paste":((468,125)),
            "abilities":{"Fire Ball":1,"Absorb":1,"vaccine":1}
            }
        ]

def getClassDict():
    return [
            {"class":"warrior", 
            "desc":"Warrior class. Great all around class.", 
            "stats":{"strength":50, "defense":50, "intelligence":30, "sense":20, "health":100, "CurrentHealth":100}, 
            "ability":"Rage", 
            "abilitydesc":"Increase attack damage by 50%"},

            {"class":"assassin", 
            "desc":"Assassin class. deadly damage output, low defense.", 
            "stats":{"strength":110, "defense":15, "intelligence":30, "sense":50, "health":80, "CurrentHealth":100}, 
            "ability":"stealth", 
            "abilitydesc":"Become invisible! All attacks will deal full damage, ignoring opponents' defense stat."},

            {"class":"Mage", 
            "desc":"Mage class. Uses movie science", 
            "stats":{"strength":40, "defense":30, "intelligence":100, "sense":60, "health":100, "CurrentHealth":100}, 
            "ability":"Fire ball", 
            "abilitydesc":"Send a fire ball at your enemies!"},

            {"class":"Healer", 
            "desc":"Healer class. Can heal. A lot.", 
            "stats":{"strength":40, "defense":50, "intelligence":80, "sense":30, "health":150, "CurrentHealth":150}, 
            "ability":"Heal!", 
            "abilitydesc":"50% HP boost!"}

        ]

def getEffectDict():
    return [
            {"name":"Bleed","type":"Physical", "category":["health"], "AffectsSender":False, "value":95, "length":4, "ValSet":False},
            {"name":"Defenseless","type":"Physical", "category":["defense"], "AffectsSender":False, "value":10, "length":3, "ValSet":True},
            {"name":"Regeneration","type":"Physical", "category":["health"], "AffectsSender":False, "value":115, "length":4, "ValSet":True},
            {"name":"Amaterasu","type":"Magic", "category":["health"], "AffectsSender":False, "value":80, "length":1000, "ValSet":False},
            {"name":"Susanoo","type":"Magic", "category":["defense"], "AffectsSender":True, "value":1000, "length":1000, "ValSet":False},


        ]


def getBackgroundList():
    return [
            {"name":"house.jpg", "paste":(378,167), "size":(377,467)},
            {"name":"nightsky.jpg", "paste":(60,82), "size":(195,279)},
            {"name":"macd.jpg", "paste":(72,6), "size":(204,310)},
        ]

def getRestaurants():
    return [
            {"name":"mcdonalds", "menu":{"bigmac":6, "QuarterPounder":3, "Bacon Clubhouse Burger":4, "fillet-o-fish":3, "happy meal":4}, "background":"macd.jpg", "img":"image", "waiter":"http://pilerats.com/assets/Uploads/_resampled/SetWidth940-mcdonalds-japan-anime-ad.jpg"}
        ]

def getDateTalkMap():
    return [
            {"typename":"Tsundere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Dandere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Kuudere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Sadodere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Kamidere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
            {"typename":"Sweet", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, darling?"]},
            {"typename":"Yandere", "invite":["{author}! Im hungry! lets go eat!"], "react":["hmm, lets eat at {restaurant}!"], "whattoeat":["hmm, I'll order the {order}!, what will you have, {author}?"]},
        ]


def getTalkMap():
    return [
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

def getBoinkResponse():
    return [
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

def getGfTypes():
    return [
            {"typename":"Tsundere", "letter":"a","textresponse": ["You are really bad at that, you know?", "That was fine, I guess.", "That was... Nice. t...tthank you."], "movieresponse": "thanks for taking me out!", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"I love you too! *squeezes*", "kissresponse": "... that was sudden. Youre a great kisser. I wouldnt mind another one <3", "proposeresponse": "YESSS!! YESS I LOVE YOU SOO MUCH {0}!!!"},
            {"typename":"Yandere", "letter":"b", "textresponse": ["maybe you should try harder? I will support you in any way I can.", "Thank you for the text.", "Thank you for the text. ily very much." ], "movieresponse": "I want to see more movies with you!", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"Dont move. I wanna stay like this for a few more hours.", "kissresponse": "stop. Dont leave. Kiss me again. Again. And again...", "proposeresponse": "of course Ill marry you!! i want to spend all my time with you! {0}!!!"},
            {"typename":"Dandere", "letter":"c", "textresponse": [".. thanks, but.. please try harder next time!","...I appreciate the text.", "Thank you for the text... I love you too."], "movieresponse": "Thank... you.. for taking me out!" , "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"T.. thank you.", "kissresponse": "...thanks.", "proposeresponse": ".. of course!!!! I love you so much, {0}!!!"},
            {"typename":"Kuudere", "letter":"d", "textresponse": ["That was terrible.", "Decent at best.", "This is great. I love you very much."], "movieresponse": "That was a good movie.", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"Squeeze me more. i like this feeling.", "kissresponse": "Kiss me again. I like that feeling", "proposeresponse": "marry you? yeh sure ig. I guess you are now my fiance, {0}!!!"},
            {"typename":"Sweet", "letter":"e", "textresponse": ["Thank you! but try a little bit better next time?", "Thank you! I appreciate what you do!!", "This is amazing!!! Thank you! ily so so much!"], "movieresponse": "woow! that was great! we should do this more often!!", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"aww thanks! I love you too!! *squeezes* I dont ever want to lose you!", "kissresponse": "... that was sudden. Youre a great kisser. I wouldnt mind another one <3 I love you so much!", "proposeresponse": "YES! Of course I want to marry you! I want to spend time with you, Have kids, Grow old together. I love you so much, {0}!!!"},
            {"typename":"Sadodere", "letter":"f", "textresponse": ["You are really bad at texting!! I find it amusing.", "That was a decent text! Only Decent though.", "Good job! I am satisfied with that."], "movieresponse": "Isnt that something? Taking your girlfriend out to watch a movie.", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"huh? youre hugging me? Fine. Ill allow it. Pervert.", "kissresponse": ".. AH.. AHAHAHA did you just kiss me? pervert <3", "proposeresponse": "Marry you? Haha, Of course. I love you, {0} <3"},
            {"typename":"Kamidere", "letter":"g", "textresponse": ["Your texting skill is poor; It can be improved though.", "That was good effort. However, your text was only decent.", "Excellent. I appreciate it.❤️"], "movieresponse": "Thank you for the invitation. I greatly appreciate it❤️", "netflixresponse":["That show sucked lmao","that show was ok","Netflix is fun with you!"], "hugresponse":"Thank you. I love your embrace.", "kissresponse": "Youre great at that <3.", "proposeresponse": "{0}. Regarding your marriage proposal, I gratefully accept. words cant describe how much you mean to me. I want to spend the rest of my life with you<3."},
        ]      












##-------------------------------------------------------------------ASYNC FUNCTS
async def ChoiceEmbed(self, ctx, choices:list, TitleOfEmbed:str, ReactionsList=['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'],p:discord.Member=None,EmbedToEdit=None):
    count = 0
    reactionlist = []
    emptydict = {}
    finalstr = ""
    for x in choices:
        emptydict[ReactionsList[count]]=x
        reactionlist.append(ReactionsList[count])
        finalstr+="%s %s\n"%(ReactionsList[count], x)
        count+=1
    embed = discord.Embed(title = TitleOfEmbed, description = finalstr, color = ctx.author.color)
    if EmbedToEdit!=None:
        EmbedToEdit = await EmbedToEdit.edit(embed=embed)
        EmbedToEdit.clear_reactions()
        for x in reactionlist:
            await EmbedToEdit.add_reaction(x)
    else:
        ThisMessage = await ctx.channel.send(embed=embed)
        for x in reactionlist:
            await ThisMessage.add_reaction(x)
    if not p:
        p=ctx.author

    def check(reaction, user):
        return user==p and str(reaction.emoji) in reactionlist and reaction.message == ThisMessage
    confirm = await self.client.wait_for('reaction_add',check=check, timeout = 60)
    try:
        if confirm:
            rawreaction = str(confirm[0])
            if EmbedToEdit!=None:
                return[emptydict[rawreaction], EmbedToEdit]
            else:
                return [emptydict[rawreaction], ThisMessage]
    except TimeoutError:
        await ctx.channel.send("You took too long! I guess we arent doing this.")




async def AddChoices(self, ctx, choices:list, MessageToAddTo, p:discord.Member=None):
    for x in choices:
        await MessageToAddTo.add_reaction(x)
    if p==None:
        p=ctx.author
    def check(reaction, user):
        return user==p and str(reaction.emoji) in choices and reaction.message == MessageToAddTo
     
    confirm = await self.client.wait_for('reaction_add',check=check, timeout = 60)
    try:
        if confirm:
            print("Yes, This check worked")
            return str(confirm[0])
    except TimeoutError:
        await ctx.channel.send("You took too long!")
        return "Timeout"







async def StoryEmbed(self, ctx, embedict:list):
    complete = False
    count = 0
    while complete == False:
        if count==len(embedict):
            complete = True
            break
        currentembed = embedict[count]
        embed = discord.Embed(title = currentembed["title"], description = currentembed["description"] ,color =ctx.author.color)
        try:
            if "file" in currentembed.keys():
                await editthis.edit(embed=embed, file = discord.File(currentembed["file"]))
            else:
                await editthis.edit(embed=embed)
        except:
            if "file" in currentembed.keys():
                editthis = await ctx.channel.send(embed=embed, file = discord.File(currentembed["file"]))
            else:
                editthis = await ctx.channel.send(embed=embed)
        await editthis.add_reaction("▶️")
        def check(reaction,userr):
            return userr==ctx.author and str(reaction.emoji)=="▶️" and reaction.message==editthis
        confirm = await self.client.wait_for('reaction_add', check=check, timeout = 60)
        try:
            if confirm:
                await editthis.clear_reactions()
                pass
                count+=1
        except asyncio.TimeoutError:
            await editthis.edit(embed=discord.Embed(title = "You took too long", color = ctx.author.color))


