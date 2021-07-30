
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
cluster = MongoClient('mongodb+srv://SCPT:Geneavianina@scptsunderedatabase.fp8en.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mulah = cluster["discord"]["mulah"]
levelling = cluster["discord"]["levelling"]

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


def InvCheck(user, item, Id=False) -> bool:
    if Id==False:
        inv = mulah.find_one({"id":user.id}, {"inv"})["inv"]
        check = next((x for x in inv if x["name"].lower()==item.lower()), None)
        if check == None:
            return False
        else:
            return True
    else:
        inv = mulah.find_one({"id":user}, {"inv"})["inv"]
        check = next((x for x in inv if x["name"].lower()==item.lower()), None)
        if check == None:
            return False
        else:
            return True



















##----------------------------------------------------Achievement Functs
def XpBar(val, max, fill=":blue_square:", empty=":white_large_square:", NumOfSquares=20):
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


