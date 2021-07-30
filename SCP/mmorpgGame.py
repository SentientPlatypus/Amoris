from asyncio.events import set_child_watcher
from datetime import date
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
mulah = cluster["discord"]["mulah"]



class mmorpgGame(commands.Cog):
    def __init__(self, client):
        self.client = client





    @commands.Cog.listener()
    async def on_ready(self):
        global Effect 
        class Effect(object):
            def __init__(self, name, type,Category, AffectsSender:bool, Value, length, ValSet=False):
                self.name=name
                self.type=type
                self.Category=Category
                self.AffectsSender=AffectsSender
                self.Value=Value
                self.length=length
                self.ValSet=ValSet


        global Attack
        class Attack(object):
            def __init__(self,name, type, damage, mana=None, effects:list=None):
                self.type=type
                self.damage=damage
                self.name=name
                self.effects=effects
                self.mana=mana

        global Defense
        class Defense(object):
            def __init__(self,name, type, WorksAgainst,defends, special=None, mana=None, effects:list=None):
                self.type=type
                self.name=name
                self.WorksAgainst = WorksAgainst
                self.defends=defends
                self.special=special
                self.effects=effects
                self.mana=mana

        global Support
        class Support(object):
            def __init__(self,name, type, attributeToSupport, value, special=None, mana=None,effects:list=None,SupportUser:bool=True, percentage=False):
                self.SupportUser = SupportUser
                self.type=type
                self.value=value
                self.attributeToSupport=attributeToSupport
                self.name=name
                self.special=special
                self.effects=effects
                self.mana=mana
                self.percentage=percentage


        global Opponent
        class Opponent(object):
            global Effect
            def __init__(self, Name, Image, CurrentHealth, TotalHealth, Defense, TotalDefense,Strength, TotalStrength, Mana, Intelligence, size, paste, Attacks:list=None, Defenses:list=None, support:list=None, OnCooldown:list=None,Player:discord.Member=None, Effects:list=None):
                self.CurrentHealth=CurrentHealth
                self.TotalHealth=TotalHealth
                self.Image=Image
                self.Name=Name
                self.Defense=Defense
                self.TotalDefense=TotalDefense
                self.Strength=Strength
                self.TotalStrength=TotalStrength
                self.Mana=Mana
                self.Intelligence= Intelligence
                self.size=size
                self.paste=paste
                self.Attacks=Attacks
                self.Defenses=Defenses
                self.support=support
                self.Player=Player
                self.OnCooldown=OnCooldown
                self.Effects=Effects


            def DamageOpponent(self, DamagePoints:int):
                self.CurrentHealth-=(DamagePoints)


            def SupportMe(self, Support:Support):
                ValueToEdit=Support.attributeToSupport
                if ValueToEdit == "health":
                    before = self.CurrentHealth
                    if Support.percentage==False:
                        self.CurrentHealth*=(Support.value/100)
                    else:
                        self.CurrentHealth+=Support.value
                    if self.CurrentHealth>self.TotalHealth:
                        self.CurrentHealth=self.TotalHealth
                    after = self.CurrentHealth
                elif ValueToEdit=="strength":
                    before = self.Strength
                    if Support.percentage==False:
                        self.Strength*=(Support.value/100)
                    else:
                        self.Strength+=Support.value
                    if self.Strength>self.TotalStrength:
                        self.Strength=self.TotalStrength
                    after = self.Strength
                elif ValueToEdit=="intelligence":
                    before = self.Mana
                    if Support.percentage==False:
                        self.Mana*=(Support.value/100)
                    else:
                        self.Mana+=Support.value
                    if self.Mana>self.Intelligence:
                        self.Mana=self.Intelligence
                    after = self.Mana
                elif ValueToEdit=="defense":
                    before = self.Defense
                    if Support.percentage==False:
                        self.Defense*=(Support.value/100)
                    else:
                        self.Defense+=Support.value
                    if self.Defense>self.TotalDefense:
                        self.Defense=self.TotalDefense
                    after = self.Defense

                finalval = after-before
                return finalval



            def AddToCooldown(self, category, name):
                global abilitydict
                DictionaryTOFInd = next(x for x in abilitydict if x["name"].lower()==name.lower() and x["category"].lower()==category.lower())
                if "cooldown" in DictionaryTOFInd.keys():
                    if {DictionaryTOFInd["name"]:DictionaryTOFInd["cooldown"]} in self.OnCooldown:
                        z = next(x for x in self.OnCooldown if Globals.GetFirstKey(x)==DictionaryTOFInd["name"])
                        z[DictionaryTOFInd["name"]]=DictionaryTOFInd["cooldown"]
                    else:  
                        self.OnCooldown.append({DictionaryTOFInd["name"]:DictionaryTOFInd["cooldown"]})
                else:
                    pass

            def CooldownCheck(self):
                if self.OnCooldown:
                    for x in self.OnCooldown:
                        x[Globals.GetFirstKey(x)]-=1
                        if x[Globals.GetFirstKey(x)]==0:
                            self.OnCooldown.remove(x)

            def IsDead(self):
                if self.CurrentHealth<=0:
                    return True
                else:
                    return False

            def EffectCooldown(self):
                if self.Effects:
                    for x in self.Effects:
                        x[Globals.GetFirstKey(x)]-=1
                        if x[Globals.GetFirstKey(x)]==0:
                            self.Effects.remove(x)
            
            def AddEffect(self, effect:Effect):
                self.Effects.append({effect.name:effect.length})


            def CallEffect(self):
                global effectdict
                if self.Effects:
                    for x in self.Effects:
                        ThisDict = next(z for z in effectdict if z["name"].lower()==Globals.GetFirstKey(x).lower())
                        Ef = Effect(ThisDict["name"], ThisDict["type"], ThisDict["category"], ThisDict["AffectsSender"], ThisDict["value"], ThisDict["length"], ThisDict["ValSet"])
                        thingtochange=""
                        if Ef.Category.lower()=="strength":
                            limit=self.TotalStrength
                            if Ef.ValSet:
                                if x[Globals.GetFirstKey(x)]== Ef.length:
                                    self.Strength*=(Ef.Value/100)
                                elif x[Globals.GetFirstKey(x)]==1:
                                    self.Strength*=(100/Ef.Value)
                                else:
                                    pass
                            else:
                                self.Strength*=(Ef.Value/100)
                                if self.Strength>limit:
                                    self.Strength=limit
                        if Ef.Category.lower()=="health":
                            limit=self.TotalHealth
                            if Ef.ValSet:
                                if x[Globals.GetFirstKey(x)]== Ef.length:
                                    self.CurrentHealth*=(Ef.Value/100)
                                elif x[Globals.GetFirstKey(x)]==1:
                                    self.CurrentHealth*=(100/Ef.Value)
                                else:
                                    pass
                            else:
                                self.CurrentHealth*=(Ef.Value/100)
                                if self.CurrentHealth>limit:
                                    self.CurrentHealth=limit
                        if Ef.Category.lower()=="intelligence":
                            limit=self.Intelligence
                            if Ef.ValSet:
                                if x[Globals.GetFirstKey(x)]== Ef.length:
                                    self.Mana*=(Ef.Value/100)
                                elif x[Globals.GetFirstKey(x)]==1:
                                    self.Mana*=(100/Ef.Value)
                                else:
                                    pass
                            else:
                                self.Mana*=(Ef.Value/100)
                                if self.Mana>limit:
                                    self.Mana=limit

                        if Ef.Category.lower()=="defense":
                            limit=self.TotalDefense
                            if Ef.ValSet:
                                if x[Globals.GetFirstKey(x)]== Ef.length:
                                    self.Defense*=(Ef.Value/100)
                                elif x[Globals.GetFirstKey(x)]==1:
                                    self.Defense*=(100/Ef.Value)
                                else:
                                    pass
                            else:
                                self.Defense*=(Ef.Value/100)
                                if self.Defense>limit:
                                    self.Defense=limit









 
        def Deflect(Attacker:Opponent, Defender:Opponent,attack:Attack, embed:discord.Embed):
            Attacker.CurrentHealth-=attack.damage
            embed.add_field(name = "%s used %s, but it was Deflected!"%(Attacker.Name, attack.name), value = "%s was hit with his own attack, and recieved %s points of damage"%(Attacker.Name, attack.damage))
            TotalDamage=0
            return [embed, TotalDamage]






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
    

        global GetAttribute
        def GetAttribute(att, user:discord.Member):
            abilities =mulah.find_one({"id":user.id}, {"mmorpg"})["mmorpg"]["abilities"]
            ReturnList = []
            print(abilities)
            for x in abilities.keys():
                AbilityDictionary = next(z for z in abilitydict if z["name"].lower()==x.lower())
                print(AbilityDictionary)
                Effects = []
                if AbilityDictionary["effect"]!=None:
                    for z in AbilityDictionary["effect"]:
                        print(z)
                        EffectDictionary = next((a for a in effectdict if a["name"].lower()==z.lower()), None)
                        Effects.append(
                            Effect(
                                EffectDictionary["name"], 
                                EffectDictionary["type"], 
                                EffectDictionary["category"], 
                                EffectDictionary["AffectsSender"],
                                EffectDictionary["value"],
                                EffectDictionary["length"],
                                EffectDictionary["ValSet"],

                            )
                        )
                if AbilityDictionary["category"]==att:
                    if att=="attack":
                        ReturnList.append(
                            Attack(
                                AbilityDictionary["name"],
                                AbilityDictionary["type"],
                                AbilityDictionary["damage"],
                                AbilityDictionary["mana"],
                                Effects

                            )
                        )

                    elif att=="defense":
                        ReturnList.append(
                            Defense(
                                AbilityDictionary["name"],
                                AbilityDictionary["type"],
                                AbilityDictionary["WorksAgainst"],
                                AbilityDictionary["defends"],
                                AbilityDictionary["special"],
                                AbilityDictionary["mana"],
                                Effects
                            )
                        )

                    elif att=="support":
                        ReturnList.append(
                            Support(
                                AbilityDictionary["name"],
                                AbilityDictionary["type"],
                                AbilityDictionary["attributeToSupport"],
                                AbilityDictionary["value"],
                                AbilityDictionary["special"],
                                AbilityDictionary["mana"],
                                Effects,
                                AbilityDictionary["SupportUser"],
                                AbilityDictionary["percentage"]
                            )
                        )     

            return ReturnList
                    


        global GetAttributeEnemy
        def GetAttributeEnemy(att, user):
            global abilitydict
            global Enemies
            ReturnList = []
            dictionary = next(x for x in Enemies if x["name"].lower()==user.lower())
            abilities = dictionary["abilities"]
            for x in abilities.keys():
                AbilityDictionary = next(z for z in abilitydict if z["name"].lower()==x.lower())
                Effects = []
                if AbilityDictionary["effect"]!=None:
                    for z in AbilityDictionary["effect"]:
                        EffectDictionary = next((a for a in effectdict if a["name"].lower()==z.lower()), None)
                        Effects.append(
                            Effect(
                                EffectDictionary["name"], 
                                EffectDictionary["type"], 
                                EffectDictionary["category"], 
                                EffectDictionary["AffectsSender"],
                                EffectDictionary["value"],
                                EffectDictionary["length"],
                                EffectDictionary["ValSet"],
                            )
                        )
                if AbilityDictionary["category"]==att:
                    if att=="attack":
                        ReturnList.append(
                            Attack(
                                AbilityDictionary["name"],
                                AbilityDictionary["type"],
                                AbilityDictionary["damage"],
                                AbilityDictionary["mana"],
                                Effects

                            )
                        )

                    elif att=="defense":
                        ReturnList.append(
                            Defense(
                                AbilityDictionary["name"],
                                AbilityDictionary["type"],
                                AbilityDictionary["WorksAgainst"],
                                AbilityDictionary["defends"],
                                AbilityDictionary["special"],
                                AbilityDictionary["mana"],
                                Effects
                            )
                        )

                    elif att=="support":
                        ReturnList.append(
                            Support(
                                AbilityDictionary["name"],
                                AbilityDictionary["type"],
                                AbilityDictionary["attributeToSupport"],
                                AbilityDictionary["value"],
                                AbilityDictionary["special"],
                                AbilityDictionary["mana"],
                                Effects,
                                AbilityDictionary["SupportUser"],
                                AbilityDictionary["percentage"]
                            )
                        )     

            return ReturnList


  




        global FinalDamage
        async def FinalDamage(self, ctx, WeaponOrAbility:Attack, Op:Opponent, You:Opponent, Defense:Defense=None):
            global Enemies
            global abilitydict
            global itemdict        

            if WeaponOrAbility.effects:
                for x in WeaponOrAbility.effects:
                    if x.AffectsSender==True:
                        You.AddEffect(x)
                    else:
                        Op.AddEffect(x)
            if Defense.effects:
                print("Yes this defense has effects")
                for x in Defense.effects:
                    if x.AffectsSender==True:
                        Op.AddEffect(x)
                    else:
                        You.AddEffect(x)

            if Defense!=None:
                if Defense.WorksAgainst== "All" or Defense.WorksAgainst== WeaponOrAbility.type:
                    print(Defense.special)
                    if Defense.special==None:
                        AmountOfDamage = int(WeaponOrAbility.damage+(You.Strength/150))
                        AmountOfDamage-=Defense.defends
                        if AmountOfDamage<0:
                            AmountOfDamage=0

                        TotalDamage = AmountOfDamage-Op.Defense
                        if TotalDamage<0:
                            TotalDamage=0
                        Op.DamageOpponent(TotalDamage)
                        bar = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")
                        embed = discord.Embed(title = "%s"%(Op.Name), description = bar+ "%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)

                    else:
                        bar = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")
                        embed = discord.Embed(title = "%s"%(Op.Name), description = bar+ "%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)

                        FunctionToCall = Defense.special
                        ret = FunctionToCall(You, Op, WeaponOrAbility,embed)
                        embed = ret[0]
                        TotalDamage = ret[1]

                else:
                    AmountOfDamage = int(WeaponOrAbility.damage+(You.Strength/150))
                    TotalDamage = AmountOfDamage-Op.Defense
                    if TotalDamage<0:
                        TotalDamage=0
                    Op.DamageOpponent(TotalDamage)   
                    bar = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")
                    embed = discord.Embed(title = "%s"%(Op.Name), description = bar+ "%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)

            else:
                AmountOfDamage = int(WeaponOrAbility.damage+(You.Strength/150))
                TotalDamage = AmountOfDamage-Op.Defense
                if TotalDamage<0:
                    TotalDamage=0
                Op.DamageOpponent(TotalDamage)   
                bar = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")
                embed = discord.Embed(title = "%s"%(Op.Name), description = bar+ "%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)


            You.CallEffect()
            Op.CallEffect()


            You.EffectCooldown()
            Op.EffectCooldown()
            print("this is the effects")
            print(Op.Effects)
            if Op.Effects:
                finalstr = ""
                for x in Op.Effects:
                    midstr="%s (%s/%s)"%(Globals.GetFirstKey(x), x[Globals.GetFirstKey(x)], next(z for z in effectdict if z["name"].lower()==Globals.GetFirstKey(x).lower())["length"])
                    finalstr+="%s\n%s\n"%(midstr, Globals.XpBar(x[Globals.GetFirstKey(x)], next(z for z in effectdict if z["name"].lower()==Globals.GetFirstKey(x).lower())["length"], NumOfSquares=5))
                embed.add_field(name = "%s' Current Effects"%(Op.Name), value = finalstr)
            embed.add_field(name="%s used %s!"%(You.Name, WeaponOrAbility.name), value = "%s recieved %s points of damage!"%(Op.Name, TotalDamage))

            embed.add_field(name = "%s' Mana"%(You.Name), value = "%s/%s"%(You.Mana, You.Intelligence))
            Yourbar = Globals.XpBar(You.CurrentHealth, You.TotalHealth, "❤️", "🖤")     
            embed.set_footer(text = "%s \n %s \n %s/%s"%(You.Name, Yourbar, You.CurrentHealth, You.TotalHealth))

            CreateBattlefield(You, Op)
            file = discord.File("FightScene.png")
            embed.set_image(url = "attachment://FightScene.png")
            print("Affects of Op:")
            print(Op.Effects)
            print(Op.Defense)
            return [embed, file, Op.CurrentHealth]
            
            


        global FightAction
        async def FightAction(self, ctx, Op:Opponent, You:Opponent):
            global abilitydict
            global itemdict
            global AttackDict

            embed = discord.Embed(title = Op.Name, description = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")+"%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)
            embed.set_footer(text = "%s\n%s\n%s/%s"%(You.Name, Globals.XpBar(You.CurrentHealth, You.TotalHealth, "❤️", "🖤"), You.CurrentHealth, You.TotalHealth))
            embed.add_field(name = "❤️Support", value = "Support yourself!", inline=True)
            embed.add_field(name = "⚔️Attack", value = "Attack Your Enemy!", inline=True)
            embed.add_field(name="🏃Retreat", value = "Shameless", inline=True)

            if You.OnCooldown:
                finlstr = ""
                for x in You.OnCooldown:
                    midstr = "%s (%s/%s)"%(Globals.GetFirstKey(x),x[Globals.GetFirstKey(x)], next(x for x in abilitydict if x["name"].lower()==Globals.GetFirstKey(x).lower())["cooldown"])
                    finlstr+="%s\n%s\n"%(midstr.center(20), Globals.XpBar(x[Globals.GetFirstKey(x)], next(x for x in abilitydict if x["name"].lower()==Globals.GetFirstKey(x).lower())["cooldown"], NumOfSquares=5))
                embed.add_field(name = "Abilities Still On Cooldown:", value = finlstr)


            CreateBattlefield(You, Op)
            file = discord.File("FightScene.png")
            embed.set_image(url = "attachment://FightScene.png")
            MessageToRef = await ctx.channel.send(embed=embed, file = file)

            done=False
            await asyncio.sleep(2)
            while done==False:
                if You.Player!=None:
                    Choices = await Globals.AddChoices(self, ctx, ["❤️", "⚔️", "🏃"], MessageToRef)
                    if Choices == "❤️":
                        if You.support:
                            ActionChoice = [x.name for x in You.support if You.Mana>=x.mana and x.name not in Globals.GetKeysFromDictInList(You.OnCooldown)]
                            ReturnedChoice = await Globals.ChoiceEmbed(self, ctx, ActionChoice, "Support!")
                            print(ReturnedChoice)
                            You.Mana-=next(z for z in abilitydict if z["name"]==ReturnedChoice[0])["mana"]
                            return [next(x for x in You.support if x.name==ReturnedChoice[0]), "Support"]
                            break
                        else:
                            await ctx.channel.send("You dont have any support abilities/items lmao, try again")
                            pass

                    elif Choices =="⚔️":
                        if You.Attacks:
                            print(You.Attacks)
                            ActionChoice = [x.name for x in You.Attacks if You.Mana>=x.mana and x.name not in Globals.GetKeysFromDictInList(You.OnCooldown)]
                            ReturnedChoice = await Globals.ChoiceEmbed(self, ctx, ActionChoice, "Attack!")
                            print(ReturnedChoice)
                            You.Mana-=next(z for z in abilitydict if z["name"]==ReturnedChoice[0])["mana"]
                            return [next(x for x in You.Attacks if x.name==ReturnedChoice[0]), "Attack"]
                            break
                        else:
                            await ctx.channel.send("You dont have any attacks lmao, try again")

                            pass

                    elif Choices=="🏃":
                        await ctx.channel.send(embed=discord.Embed(title = "%s Will Retreat."%(You.Name)))
                        return [None,"Retreat"]
                        break
                else:
                    print("This is an Enemy")
                    print(You.Attacks)
                    print(You.Defenses)
                    print(You.support)
                    Choices = "⚔️"
                    if You.CurrentHealth<You.TotalHealth:
                        Choices = random.choice(["❤️", "⚔️"])
                    else:
                        Choices = random.choice(["⚔️"])
                    if Choices == "❤️":
                        if You.support:                  
                            ActionChoice = [x.name for x in You.support if You.Mana>=x.mana and x.name not in Globals.GetKeysFromDictInList(You.OnCooldown)]
                            ReturnedChoice = random.choice(ActionChoice)
                            print(ReturnedChoice)
                            You.Mana-=next(z for z in abilitydict if z["name"]==ReturnedChoice)["mana"]

                            await ctx.channel.send(embed=discord.Embed(title = "%s Will use %s!"%(You.Name, ReturnedChoice)))

                            return [next(x for x in You.support if x.name==ReturnedChoice), "Support"]
                            break
                        else:
                            pass


                    elif Choices =="⚔️":
                        if You.Attacks:
                            ActionChoice = [x.name for x in You.Attacks if You.Mana>=x.mana and x.name not in Globals.GetKeysFromDictInList(You.OnCooldown)]
                            ReturnedChoice = random.choice(ActionChoice)
                            await ctx.channel.send(embed=discord.Embed(title = "%s Will use %s!"%(You.Name, ReturnedChoice)))
                            print(ReturnedChoice)
                            You.Mana-=next(z for z in abilitydict if z["name"]==ReturnedChoice)["mana"]
                            
                            return [next(x for x in You.Attacks if x.name==ReturnedChoice), "Attack"]
                            break
                        else:
                            pass

                    elif Choices=="🏃":
                        await ctx.channel.send(embed=discord.Embed(title = "%s Will Retreat."%(You.Name)))

                        return [None,"Retreat"]
                        break
            


                
        global SupportOpponent
        async def SupportOpponent(self, ctx, User:Opponent, Op:Opponent, ability:Support):
            finalval=0
            if ability.SupportUser==True:
                finalval = User.SupportMe(ability)
            else:
                finalval = Op.SupportMe(ability)
            embed = discord.Embed(title = Op.Name, description = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")+"%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)
            embed.set_footer(text = "%s\n%s\n%s/%s"%(User.Name, Globals.XpBar(User.CurrentHealth, User.TotalHealth, "❤️", "🖤"), User.CurrentHealth, User.TotalHealth))
            embed.add_field(name="%s Used %s"%(User.Name ,ability.name), value = "%s's %s is increased by %s"%(User.Name, ability.attributeToSupport, finalval))
            CreateBattlefield(User, Op)
            file = discord.File("FightScene.png")
            embed.set_image(url="attachment://FightScene.png")
            return [embed, file]







        global Defend
        async def Defend(self, ctx, You:Opponent, Op:Opponent, WeaponOrAbility:Attack):
            IsPlayer=False
            if Op.Player:
                IsPlayer=True

            bar = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")
            Yourbar = Globals.XpBar(You.CurrentHealth, You.TotalHealth, "❤️", "🖤")
            
            embed = discord.Embed(title = "%s is Using %s!"%(You.Name, WeaponOrAbility.name), description = "%s' health:\n"%(Op.Name) + bar+ "%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)
            
            ChoiceList = Globals.ChoiceParts([x.name for x in Op.Defenses])
            ChoiceDict = ChoiceList[0]
            ChoiceString = ChoiceList[1]
            ReactionList = ChoiceList[2]
            print(ReactionList)
            print(ChoiceString)
            print(ChoiceDict)
            if not ChoiceDict:
                return "Error"
            embed.add_field(name="%s can Defend!"%(Op.Name), value = "Make sure To defend In time!\n%s"%(ChoiceString))
            embed.set_footer(text = "%s \n %s \n %s/%s"%(You.Name, Yourbar, You.CurrentHealth, You.TotalHealth))
            CreateBattlefield(You, Op)
            file = discord.File("FightScene.png")
            embed.set_image(url = "attachment://FightScene.png")  

            Msg = await ctx.channel.send(embed=embed, file=file)
            if IsPlayer==False:
                ReturnChoices = random.choice(ReactionList)
            else:
                ReturnChoices = await Globals.AddChoices(self, ctx, ReactionList, Msg,Op.Player)
            await asyncio.sleep(2)
            try:
                Key = ChoiceDict[ReturnChoices]
                print(Key)
                print(Op.Defenses)
                for x in Op.Defenses:
                    print(x.name)
                DefenseSpec = next(x for x in Op.Defenses if x.name.lower()==Key.lower())
                if Op.Mana>=DefenseSpec.mana:
                    TheDefense = Defense(DefenseSpec.name, DefenseSpec.type, DefenseSpec.WorksAgainst, DefenseSpec.defends, DefenseSpec.special, DefenseSpec.mana, DefenseSpec.effects)
                    print("This made it here")
                    await ctx.channel.send(embed=discord.Embed(title = "%s Defends with %s!"%(Op.Name, TheDefense.name)))
                    return TheDefense
                else:
                    await ctx.channel.send(embed=discord.Embed(title = "You dont Have enough Mana!"))
                    print("Not enough mana")
                    return "Error"
            except:
                print("Didnt wrk")
                print(traceback.format_exc())
                return ReturnChoices





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
                        for x in CurrentItem["abilities"].keys():
                            try:
                                del mmorpg["abilities"][x]
                            except:
                                pass
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


        global effectdict
        effectdict = [
            {"name":"Bleed","type":"Physical", "category":"health", "AffectsSender":False, "value":95, "length":5, "ValSet":False},
            {"name":"Defenseless","type":"Physical", "category":"defense", "AffectsSender":False, "value":10, "length":3, "ValSet":True},
        ]


        global abilitydict
        abilitydict = [

            #suppor
            {"name":"Rage","category":"support","SupportUser":True , "percentage":True, "type":"Magic","desc":"Increase attack damage", "value":150,"attributeToSupport":"strength", "special":None, "mana":10, "effect":None},
            {"name":"Heal!","category":"support","SupportUser":True, "percentage":True, "type":"Magic","desc":"Recover your HP", "value":150, "attributeToSupport":"health", "special":None, "mana":10, "effect":None},
            {"name":"stealth","category":"support","SupportUser":True, "percentage":True, "type":"Magic","desc":"Become invisible! All attacks will deal full damage, ignoring opponents' defense stat.", "value":100, "attributeToSupport":"strength", "mana":10, "effect":["Defenseless"]},
            {"name":"vaccine","category":"support","SupportUser":True, "percentage":True, "type":"Magic", "desc":"Heal!", "value":100, "attributeToSupport":"health", "special":None, "mana":10, "effect":None},
            
            
            
            
            
            ##defend
            {"name":"Deflect","category":"defense", "type":"Physical", "WorksAgainst":"Magic","defends":1500, "desc":"Returns all magic damage to its sender!", "special":Deflect, "mana":10, "effect":["Defenseless"]},
            {"name":"Absorb","category":"defense", "type":"Magic", "WorksAgainst":"All","defends":1500, "desc":"Absorbs!", "special":None,"mana":10, "effect":None},
        
        
        
        
            #attacks
            {"name":"Necromancer", "category":"attack", "type":"Magic", "damage":0,"desc":"Turn your defeated enemies into your pawns!", "special":None, "mana":10},
            {"name":"Black Slash", "category":"attack", "type":"Physical", "damage":1800, "desc":"A devastating attack from the Black Divider", "special":None, "mana":10, "effect":["Bleed"]},
            {"name":"Fire Ball", "category":"attack", "type":"Magic", "damage":50, "desc":"A basic skill from mages", "special":None, "mana":10, "effect":None},
            {"name":"Punch", "category":"attack","type":"Physical", "damage":10, "desc":"A basic attack anyone can do.", "special":None, "mana":10, "effect":None},
        ]






        global itemdict
        itemdict = [
            {"name":"Necromancer", 
            "type":"Runestone", 
            "desc":"grants the ability of Necromancer", 
            "rarity":"Legendary"},

            {"name":"Vaccine", 
            "type":"Heal",
            "desc":"grants the ability of Necromancer", 
            "rarity":"Legendary",
            "abilities":{"vaccine":1}},

            {"name":"Saitamas Dish Gloves", 
            "type":"hands", 
            "desc":"The Most powerful item in the game.",
            "rarity":"illegal", 
            "attribute":{"strength":1000000}},

            {"name":"Black Divider", 
            "type":"primary", 
            "desc":"Can deflect spells completely!", 
            "rarity":"Legendary", 
            "abilities":{"Black Slash":1, "Deflect":1}
            },

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
            "paste":((468,125)),
            "abilities":{"Fire Ball":1,"Absorb":1,"vaccine":1}
            }
        ]























    @commands.group(invoke_without_command=True)
    async def mmorpg(self, ctx):
        embed = discord.Embed(title = "The MMORPG", description = "My creator senpai read solo leveling, and is now inspired.", color = ctx.author.color)
        embed.add_field(name = "Setup commands", value = "`begin`")
        await ctx.channel.send(embed=embed)



    @mmorpg.command()
    async def Test(self, ctx, person, IsPlayer=None):
        global abilitydict
        global Enemies
        global GetAttribute
        You = Opponent(
            ctx.author.display_name, 
            ctx.author.avatar_url, 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["health"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["health"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["defense"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["defense"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["strength"], 
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["strength"],
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["intelligence"],
            mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]["stats"]["intelligence"],
            ((123,123)),
            ((20,199)),
            GetAttribute("attack", ctx.author),
            GetAttribute("defense", ctx.author),
            GetAttribute("support", ctx.author),
            [],
            ctx.author,
            []
            )

        Op = next(x for x in Enemies if x["name"].lower()==person.lower())
        Op = Opponent(
            Op["name"],     
            Op["image"], 
            Op["health"], 
            Op["health"], 
            Op["defense"], 
            Op["defense"],
            Op["strength"], 
            Op["strength"],
            Op["intelligence"], 
            Op["intelligence"], 
            Op["size"], 
            Op["paste"],
            GetAttributeEnemy("attack", "acnologia"),
            GetAttributeEnemy("defense", "acnologia"),
            GetAttributeEnemy("support", "acnologia"),
            [],
            Player=None,
            Effects=[]

            )

        print(You.Attacks)
        
        GameOver=False
        while GameOver==False:
            You.CooldownCheck()
            await asyncio.sleep(2)
            await ctx.channel.send(embed=discord.Embed(title = "It is now %s' Turn."%(You.Name)))
            await asyncio.sleep(2)

            This1 = await FightAction(self, ctx, Op, You)
            if This1[1]=="Attack":
                ThisAttack = This1[0]
                You.AddToCooldown("Attack", ThisAttack.name)
                Thee = await Defend(self, ctx, You, Op, ThisAttack)
                await asyncio.sleep(2)
                if Thee == "Error":
                    print("No defense.")
                    This = await FinalDamage(self, ctx, ThisAttack, Op, You)
                else:
                    print("Is defense")
                    This = await FinalDamage(self, ctx, ThisAttack, Op, You, Defense = Thee)
                await ctx.channel.send(embed=This[0], file=This[1])
            
            elif This1[1]=="Support":
                await asyncio.sleep(2)
                ThisSupport = This1[0]
                You.AddToCooldown("support", ThisSupport.name)
                This = await SupportOpponent(self, ctx, You, Op, ThisSupport)
                await ctx.channel.send(embed=This[0], file=This[1])  

            elif This1[1]=="Retreat":
                break


            if You.IsDead() or Op.IsDead():
                break    

            Op.CooldownCheck()
            await asyncio.sleep(2)
            await ctx.channel.send(embed=discord.Embed(title = "It is now %s' Turn."%(Op.Name))) 
            await asyncio.sleep(2)
            This1 = await FightAction(self, ctx, You, Op)
            if This1[1]=="Attack":
                ThisAttack = This1[0]
                Op.AddToCooldown("Attack", ThisAttack.name)
                Thee = await Defend(self, ctx, Op, You, ThisAttack)
                await asyncio.sleep(2)
                if Thee == "Error":
                    This = await FinalDamage(self, ctx, ThisAttack, You, Op)
                else:
                    This = await FinalDamage(self, ctx, ThisAttack, You, Op, Defense = Thee)
                await ctx.channel.send(embed=This[0], file=This[1])
            
            elif This1[1]=="Support":
                await asyncio.sleep(2)
                ThisSupport = This1[0]
                Op.AddToCooldown("support", ThisSupport.name)
                This = await SupportOpponent(self, ctx, Op, You, ThisSupport)
                await ctx.channel.send(embed=This[0], file=This[1])  

            elif This1[1]=="Retreat":
                break

            if You.IsDead() or Op.IsDead():
                break    









    @mmorpg.command()
    async def equip(self, ctx, items:str):
        global EquipItem
        global itemdict
        if ctx.author.id==643764774362021899:
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
