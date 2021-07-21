
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


def InvCheck(user, item) -> bool:
    inv = mulah.find_one({"id":user.id}, {"inv"})["inv"]
    check = next((x for x in inv if x["name"].lower()==item.lower()), None)
    if check == None:
        return True
    else:
        return False


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