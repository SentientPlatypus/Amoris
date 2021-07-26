
from datetime import date
from inspect import trace
from logging import exception
from operator import mul
from os import name, path
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
from discord import Color
cluster = MongoClient('mongodb+srv://SCPT:Geneavianina@scptsunderedatabase.fp8en.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
mulah = cluster["discord"]["mulah"]



class mmorpgGame(commands.Cog):
    def __init__(self, client):
        self.client = client





    @commands.Cog.listener()
    async def on_ready(self):
        global Opponent
        class Opponent(object):
            def __init__(self, Name, Image, CurrentHealth, TotalHealth, Defense, Strength, Mana, Intelligence, size, paste, id=None):
                self.CurrentHealth=CurrentHealth
                self.TotalHealth=TotalHealth
                self.Image=Image
                self.Name=Name
                self.Defense=Defense
                self.Strength=Strength
                self.Mana=Mana
                self.Intelligence= Intelligence
                self.size=size
                self.paste=paste
                self.id=id


            def DamageOpponent(self, DamagePoints:int):
                self.CurrentHealth-=(DamagePoints-self.Defense)




        def CreateBattlefield(p1:Opponent, p2:Opponent, Effect=None):
            Battlefield = Image.open("Battlefield.jpg")
            p2ImageUrl = p2.Image
            p1ImgeUrl = p1.Image
            p2Image = Image.open(BytesIO(requests.get(p2ImageUrl).content))
            p1Image = Image.open(BytesIO(requests.get(p1ImgeUrl).content))
            p2Image = p2Image.resize(p2.size)
            p1Image = p1Image.resize(p1.size)
            try:
                Battlefield.paste(p2Image, p2.paste, p2Image)
            except:
                Battlefield.paste(p2Image, p2.paste)
            try:
                Battlefield.paste(p1Image, p1.paste, p1Image)
            except:
                Battlefield.paste(p1Image, p1.paste)
            Battlefield.save("FightScene.png")  
               






        global FinalDamage
        async def FinalDamage(self, ctx, WeaponOrAbility, Op:Opponent, You:Opponent):
            global Enemies
            global abilitydict
            global itemdict
            WeaponAndAbilityDict = itemdict+abilitydict
            DamageName = next(x for x in WeaponAndAbilityDict if x["name"].lower()==WeaponOrAbility.lower())

            AmountOfDamage = int(DamageName["damage"]+(You.Strength/150))

            TotalDamage = AmountOfDamage-Op.Defense
            Op.DamageOpponent(TotalDamage)

            bar = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")
            Yourbar = Globals.XpBar(You.CurrentHealth, You.TotalHealth, "❤️", "🖤")
            
            embed = discord.Embed(title = "%s"%(Op.Name), description = bar+ "%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)
            embed.add_field(name="You used %s!"%(WeaponOrAbility), value = "%s recieved %s points of damage!"%(Op.Name, TotalDamage))
            embed.set_footer(text = "%s \n %s \n %s/%s"%(You.Name, Yourbar, You.CurrentHealth, You.TotalHealth))
            
            CreateBattlefield(You, Op)
            

            file = discord.File("FightScene.png")
            embed.set_image(url = "attachment://FightScene.png")
            
            print(embed.to_dict())
            return [embed, file, Op.CurrentHealth]
            
            
        global FightAction
        async def FightAction(self, ctx, Op:Opponent, You:Opponent):
            global abilitydict
            global itemdict
            embed = discord.Embed(title = Op.Name, description = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")+"%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)
            embed.set_footer(text = "%s\n%s\n%s/%s"%(You.Name, Globals.XpBar(You.CurrentHealth, You.TotalHealth, "❤️", "🖤"), You.CurrentHealth, You.TotalHealth))
            embed.add_field(name = "❤️Heal", value = "Heal yourself!", inline=True)
            embed.add_field(name = "⚔️Attack", value = "Attack Your Enemy!", inline=True)
            embed.add_field(name="🏃Retreat", value = "Shameless", inline=True)
            CreateBattlefield(You, Op)
            file = discord.File("FightScene.png")
            embed.set_image(url = "attachment://FightScene.png")
            MessageToRef = await ctx.channel.send(embed=embed, file = file)
            Choices = await Globals.AddChoices(self, ctx, ["❤️", "⚔️", "🏃"], MessageToRef)
            if Choices == "❤️":
                ActionChoice = [x for x in itemdict if x["type"]=="Heal" and Globals.InvCheck(You.id, x, Id=True)==True]
                ReturnedChoice = await Globals.ChoiceEmbed(self, ctx, ActionChoice, "Heal!")
                return [ReturnedChoice[0], "Heal"]

            elif Choices =="⚔️":
                ActionChoice = []
                if mulah.find_one({"id":You.id}, {"mmorpg"})["mmorpg"]["loadout"]["primary"]!=None:
                    ActionChoice.append(mulah.find_one({"id":You.id}, {"mmorpg"})["mmorpg"]["loadout"]["primary"])
                if mulah.find_one({"id":You.id}, {"mmorpg"})["mmorpg"]["loadout"]["secondary"]!=None:
                    ActionChoice.append(mulah.find_one({"id":You.id}, {"mmorpg"})["mmorpg"]["loadout"]["secondary"])
                for x in mulah.find_one({"id":You.id}, {"mmorpg"})["mmorpg"]["abilities"].keys():
                    z = next(z for z in abilitydict if z["name"]==x)
                    if "damage" in z.keys():
                        ActionChoice.append(x)
                ReturnedChoice = await Globals.ChoiceEmbed(self, ctx, ActionChoice, "Attack!")
                return [ReturnedChoice[0], "Attack"]

            elif Choices=="🏃":
                return [None,"Retreat"]
            


                







        global EquipItem
        def EquipItem(user, item):
            global itemdict
            mmorpg = mulah.find_one({"id":user.id}, {"mmorpg"})["mmorpg"]
            loadout = mmorpg["loadout"]
            stats = mmorpg["stats"]
            inv = mulah.find_one({"id":user.id}, {"inv"})["inv"]
            SpecificItem = next(x for x in itemdict if x["name"].lower() == item.lower())
            if SpecificItem["type"] in loadout.keys():
                if loadout[SpecificItem["type"]]!=None:
                    CurrentItem = next(x for x in itemdict if x["name"] == loadout[SpecificItem["type"]])
                    Globals.AddToInventory(user, CurrentItem["name"], itemdict, 1)
                    Globals.RemoveFromInventory(user, SpecificItem["name"], 1)

                    if "attribute" in CurrentItem.keys():
                        for x in CurrentItem["attribute"].keys():
                            print(CurrentItem["attribute"])
                            print(stats)
                            print(x)
                            stats[x]-=CurrentItem["attribute"][x]
                    if "abilities" in CurrentItem.keys():
                        mmorpg["abilities"].remove(CurrentItem["abilities"])

                loadout[SpecificItem["type"]] = SpecificItem["name"]

                if "attribute" in SpecificItem.keys():
                    for x in SpecificItem["attribute"].keys():
                        print(x)
                        stats[x]+= SpecificItem["attribute"][x]
                if "abilities" in SpecificItem.keys():
                    for x in SpecificItem["abilities"]:
                        mmorpg["abilities"][x] = 1
                mulah.update_one({"id":user.id}, {"$set":{"mmorpg":mmorpg}})
                mulah.update_one({"id":user.id}, {"$set":{"inv":inv}})
            



        global classdict
        classdict = [
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
            "abilitydesc":"Recover 70%% of your HP!"}

        ]

        global abilitydict
        abilitydict = [
            {"name":"Punch","desc":"Lmao broke","damage":10},
            {"name":"Rage","desc":"Increase attack damage by 50%"},
            {"name":"Heal!","desc":"Recover 70%% of your HP"},
            {"name":"Fire ball","desc":"Send a fire ball at your enemies!", "damage":50},
            {"name":"stealth","desc":"Become invisible! All attacks will deal full damage, ignoring opponents' defense stat."},
            {"name":"Necromancer","desc":"Turn your defeated enemies into your pawns!"},
        ]

        global itemdict
        itemdict = [
            {"name":"Necromancer", 
            "type":"Runestone", 
            "desc":"grants the ability of Necromancer", 
            "rarity":"Legendary"},

            {"name":"Saitamas Dish Gloves", 
            "type":"hands", 
            "desc":"The Most powerful item in the game.",
            "rarity":"illegal", 
            "attribute":{"strength":1000000}},

            {"name":"Black Divider", 
            "type":"primary", 
            "desc":"Can deflect spells completely!", 
            "rarity":"Legendary", 
            "damage":1500, 
            "abilities":["Deflect"]},

            {"name":"Doma's Flames", 
            "type":"Runestone", 
            "desc":"Incinerate your enemies until one of you wins. Damage is slow, but undefendable.", 
            "rarity":"Epic"},

        ]

        global Enemies
        Enemies = [
            {"name":"Acnologia", 
            "health":5000, 
            "strength":800, 
            "defense":400, 
            "intelligence":1000,
            "mana":1000,
            "image":"https://static.wikia.nocookie.net/vsbattles/images/7/71/New_Human_Acnologia_Render.png/revision/latest/scale-to-width-down/400?cb=20200704092623", 
            "size":((160, 199)), 
            "paste":((468,125))}
        ]























    @commands.group(invoke_without_command=True)
    async def mmorpg(self, ctx):
        embed = discord.Embed(title = "The MMORPG", description = "My creator senpai read solo leveling, and is now inspired.", color = ctx.author.color)
        embed.add_field(name = "Setup commands", value = "`begin`")
        await ctx.channel.send(embed=embed)



    @mmorpg.command()
    async def Test(self, ctx, person, IsPlayer=None):
        global Enemies
        You = Opponent(
            ctx.author.display_name, 
            ctx.author.avatar_url, 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["health"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["health"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["defense"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["strength"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["intelligence"],
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["intelligence"],
            ((123,123)),
            ((20,199)),
            ctx.author.id
            )

        Op = next(x for x in Enemies if x["name"].lower()==person.lower())
        Op = Opponent(Op["name"], Op["image"], Op["health"], Op["health"], Op["defense"], Op["strength"], Op["mana"], Op["intelligence"], Op["size"], Op["paste"])
        This1 = await FightAction(self, ctx, Op, You)
        if This1[1]=="Attack":
            This = await FinalDamage(self, ctx, This1[0], Op, You)
            await ctx.channel.send(embed=This[0], file=This[1])






    @mmorpg.command()
    async def equip(self, ctx, items:str):
        global EquipItem
        global itemdict
        if str(ctx.author)=="SentientPlatypus#1332":
            allperms = True
        SpecificItem = next(x for x in itemdict if x["name"].lower()==items.lower())

        if allperms ==True:
            EquipItem(ctx.author, SpecificItem["name"])
        else:
            if Globals.InvCheck(ctx.author, item=items):
                EquipItem(ctx.author, SpecificItem["name"])
            else:
                await ctx.channel.send("You dont have this item in your inventory.")




    @mmorpg.command()
    async def begin(self, ctx):
        global StoryEmbed
        mmorpg = mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]
        print(mmorpg)
        if mmorpg["class"] == None:
            embedict = [
                {"title":"Game:", "description":"*So you want to be a player?*"},
                {"title":"Game:", "description":"*Do you think you are ready?*"},
                {"title":"Game:", "description":"*Do you fear death?*"},
                {"title":"Game:", "description":"*So be it...*"},
            ]
            global classdict
            await Globals.StoryEmbed(self, ctx, embedict=embedict)

            alphlist = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟', '🚪']
            count = 0
            reactionlist = []
            emptydict = {}
            finalstring = ""
            embed = discord.Embed(title = "Choose your class!", description = "each class has unique abilities!", color = ctx.author.color)

            for x in classdict:
                emptydict[alphlist[count]]=x["class"]
                reactionlist.append(alphlist[count])
                embed.add_field(name ="%s| %s"%(alphlist[count], x["class"]), value = "%s|\n basic stat increase:%s\n abilities:**%s**, %s"%(x["desc"], x["stats"], x["ability"], x["abilitydesc"]))

                count+=1
            editthis = await ctx.channel.send(embed=embed)
            for x in reactionlist:
                await editthis.add_reaction(x)
            def check(reaction,user):
                return user==ctx.author and str(reaction.emoji) in reactionlist and reaction.message==editthis
            confirm = await self.client.wait_for('reaction_add', check=check)
            if confirm:
                rawreaction = str(confirm[0])
                mmorpg["class"] = emptydict[rawreaction]
                YourClass = next(x for x in classdict if x["class"] == emptydict[rawreaction])
                print(YourClass)
                for x in mmorpg["stats"].keys():
                    for y in YourClass["stats"].keys():
                        if x==y:
                            mmorpg["stats"][x]+=YourClass["stats"][y]

                mmorpg["abilities"][YourClass["ability"]] = 1
                mulah.update_one({"id":ctx.author.id}, {"$set":{"mmorpg":mmorpg}})
                embed = discord.Embed(title = "You are now a %s"%(emptydict[rawreaction]), description = "Go explore!", color = ctx.author.color)
                await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("you already have a class lmao")









def setup(client):
    client.add_cog(mmorpgGame(client))
