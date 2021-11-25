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
from discord import reaction
from discord.embeds import Embed
from discord.ext.commands.cooldowns import BucketType
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
from pymongo.ssl_support import _load_wincerts
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
from datetime import date, datetime, timedelta
import pymongo
import ssl

cluster = Globals.getMongo()
mulah = cluster["discord"]["mulah"]
levelling = cluster["discord"]["levelling"]




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
            def __init__(self,name, type, damage,cooldown,ult=False, special=None, mana=None, effects:list=None,):
                self.type=type
                self.damage=damage
                self.name=name
                self.effects=effects
                self.mana=mana
                self.special=special
                self.ult=ult
                self.cooldown=cooldown

        global Defense
        class Defense(object):
            def __init__(self,name, type, WorksAgainst,defends,cooldown,ult=False, special=None, mana=None, effects:list=None):
                self.type=type
                self.name=name
                self.WorksAgainst = WorksAgainst
                self.defends=defends
                self.special=special
                self.effects=effects
                self.mana=mana
                self.ult=ult
                self.cooldown=cooldown

        global Support
        class Support(object):
            def __init__(self,name, type, attributeToSupport, value,cooldown,ult=False, special=None, mana=None,effects:list=None,SupportUser:bool=True, percentage=False):
                self.SupportUser = SupportUser
                self.type=type
                self.value=value
                self.attributeToSupport=attributeToSupport
                self.name=name
                self.special=special
                self.effects=effects
                self.mana=mana
                self.ult=ult
                self.percentage=percentage
                self.cooldown=cooldown


        global Opponent
        class Opponent(object):
            global Effect
            def __init__(self, Name, Image, CurrentHealth, TotalHealth, Defense, TotalDefense,Strength, TotalStrength, Mana, Intelligence, xp,abilityxp,duelwins, duelloses,duelretreats,size, paste, Attacks:list=None, Defenses:list=None, support:list=None, OnCooldown:list=None,Player:discord.Member=None, Effects:list=None):
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
                self.xp=xp
                self.abilityxp=abilityxp
                self.duelwins=duelwins
                self.duelloses=duelloses
                self.duelretreats=duelretreats


            def DamageOpponent(self, DamagePoints:int):
                self.CurrentHealth-=(DamagePoints)

            def incAbilityXp(self, ability):
                for x in self.abilityxp:
                    if x==ability.name:
                        x[ability.name]+=5

            def updateDb(self):
                levelling.update_one({"id":self.Player.id}, {"$set":{"xp":self.xp}})
                mulah.update_one({"id":self.Player.id}, {"$set":{"abilityxp":self.abilityxp}})
                mulah.update_one({"id":self.Player.id}, {"$set":{"duelloses":self.duelloses}})
                mulah.update_one({"id":self.Player.id}, {"$set":{"duelwins":self.duelwins}})
                mulah.update_one({"id":self.Player.id}, {"$set":{"duelretreats":self.duelretreats}})



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



            def AddToCooldown(self, Thing):
                global abilitydict
                if Thing.cooldown:
                    found = False
                    for x in self.OnCooldown:
                        obje = Globals.GetFirstKey(x)
                        if Thing.name == obje.name:
                            x[obje]=Thing.cooldown
                            found = True
                    if not found:
                        self.OnCooldown.append({Thing:Thing.cooldown})
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
                self.Effects.append({effect:effect.length})
            
            def RemoveEffect(self, effect:Effect):
                for x in self.Effects:
                    if x.name == effect.name:
                        self.Effects.remove(x)


            def CallEffect(self):
                global effectdict
                if self.Effects:
                    for x in self.Effects:
                        for a in Globals.GetFirstKey(x).Category:
                            if a.lower()=="strength":
                                limit=self.TotalStrength
                                if Globals.GetFirstKey(x).ValSet:
                                    if x[Globals.GetFirstKey(x)]== Globals.GetFirstKey(x).length:
                                        self.Strength*=(Globals.GetFirstKey(x).Value/100)
                                    elif x[Globals.GetFirstKey(x)]==1:
                                        self.Strength*=(100/Globals.GetFirstKey(x).Value)
                                    else:
                                        pass
                                else:
                                    self.Strength*=(Globals.GetFirstKey(x).Value/100)
                                    if self.Strength>limit:
                                        self.Strength=limit
                            if a.lower()=="health":
                                limit=self.TotalHealth
                                if Globals.GetFirstKey(x).ValSet:
                                    if x[Globals.GetFirstKey(x)]== Globals.GetFirstKey(x).length:
                                        self.CurrentHealth*=(Globals.GetFirstKey(x).Value/100)
                                    elif x[Globals.GetFirstKey(x)]==1:
                                        self.CurrentHealth*=(100/Globals.GetFirstKey(x).Value)
                                    else:
                                        pass
                                else:
                                    self.CurrentHealth*=(Globals.GetFirstKey(x).Value/100)
                                    if self.CurrentHealth>limit:
                                        self.CurrentHealth=limit
                            if a.lower()=="intelligence":
                                limit=self.Intelligence
                                if Globals.GetFirstKey(x).ValSet:
                                    if x[Globals.GetFirstKey(x)]== Globals.GetFirstKey(x).length:
                                        self.Mana*=(Globals.GetFirstKey(x).Value/100)
                                    elif x[Globals.GetFirstKey(x)]==1:
                                        self.Mana*=(100/Globals.GetFirstKey(x).Value)
                                    else:
                                        pass
                                else:
                                    self.Mana*=(Globals.GetFirstKey(x).Value/100)
                                    if self.Mana>limit:
                                        self.Mana=limit

                            if a.lower()=="defense":
                                limit=self.TotalDefense
                                if Globals.GetFirstKey(x).ValSet:
                                    if x[Globals.GetFirstKey(x)]== Globals.GetFirstKey(x).length:
                                        self.Defense*=(Globals.GetFirstKey(x).Value/100)
                                    elif x[Globals.GetFirstKey(x)]==1:
                                        self.Defense*=(100/Globals.GetFirstKey(x).Value)
                                    else:
                                        pass
                                else:
                                    self.Defense*=(Globals.GetFirstKey(x).Value/100)
                                    if self.Defense>limit:
                                        self.Defense=limit


        def updateDuelDb(Op:Opponent):
            levelling.update_one({"id":Op.Player.id}, {"$set":{"xp":Op.xp}})
            mulah.update_one({"id":Op.Player.id}, {"$set":{"abilityxp":Op.abilityxp}})
            mulah.update_one({"id":Op.Player.id}, {"$set":{"duelloses":Op.duelloses}})
            mulah.update_one({"id":Op.Player.id}, {"$set":{"duelwins":Op.duelwins}})
            mulah.update_one({"id":Op.Player.id}, {"$set":{"duelretreats":Op.duelretreats}})







 
        def Deflect(Attacker:Opponent, Defender:Opponent,attack:Attack, embed:discord.Embed):

            Attacker.CurrentHealth-=attack.damage
            for i in attack.effects:
                if not i.AffectsSender:
                    Attacker.AddEffect(i)
                    Defender.RemoveEffect(i)
            Defender.CallEffect()
            Attacker.CallEffect()

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
            abilityxp = mulah.find_one({"id":user.id}, {"mmorpg"})["mmorpg"]["abilities"]
            ReturnList = []
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
                                AbilityDictionary["damage"]*(abilityxp[AbilityDictionary["name"]]*0.15+1),
                                AbilityDictionary["cooldown"],
                                AbilityDictionary["ult"],
                                AbilityDictionary["special"],
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
                                AbilityDictionary["defends"]*(abilityxp[AbilityDictionary["name"]]*0.15+1),
                                AbilityDictionary["cooldown"],
                                AbilityDictionary["ult"],
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
                                AbilityDictionary["value"]*(abilityxp[AbilityDictionary["name"]]*0.15+1),
                                AbilityDictionary["cooldown"],
                                AbilityDictionary["ult"],
                                AbilityDictionary["special"],
                                AbilityDictionary["mana"],
                                Effects,
                                AbilityDictionary["SupportUser"],
                                AbilityDictionary["percentage"]
                            )
                        )     

            return ReturnList
                    
        global classdict
        classdict = Globals.getClassDict()


        global effectdict
        effectdict = Globals.getEffectDict()


        global abilitydict
        abilitydict = [

            #suppor
            {"name":"Rage","category":"support","SupportUser":True , "percentage":True, "type":"Magic","desc":"Increase attack damage", "value":150,"cooldown":0,"ult":False,"attributeToSupport":"strength", "special":None, "mana":10, "effect":None},
            {"name":"Heal!","category":"support","SupportUser":True, "percentage":True, "type":"Magic","desc":"Recover your HP", "value":150,"cooldown":0,"ult":False, "attributeToSupport":"health", "special":None, "mana":10, "effect":None},
            {"name":"stealth","category":"support","SupportUser":True, "percentage":True, "type":"Magic","desc":"Become invisible! All attacks will deal full damage, ignoring opponents' defense stat.", "value":100,"cooldown":0, "attributeToSupport":"strength", "mana":10, "effect":["Defenseless"]},
            {"name":"vaccine","category":"support","SupportUser":True, "percentage":True, "type":"Magic", "desc":"Heal!", "value":100,"cooldown":0,"ult":False, "attributeToSupport":"health", "special":None, "mana":10, "effect":None},
            
            
            
            
            
            ##defend
            {"name":"Deflect","category":"defense", "type":"Physical", "WorksAgainst":"Magic","defends":1500, "desc":"Returns all magic damage to its sender!","cooldown":0,"ult":False, "special":Deflect, "mana":10, "effect":["Defenseless"]},
            {"name":"Absorb","category":"defense", "type":"Magic", "WorksAgainst":"All","defends":1500, "desc":"Absorbs!", "special":None, "cooldown":0,"ult":False, "mana":10, "effect":None},
            {"name":"Susanoo", "category":"attack", "type":"Magic", "damage":100, "desc":"The Perfect Defense","cooldown":4,"ult":True, "special":None, "mana":70, "effect":["Susanoo"]},

        
        
        
            #attacks
            {"name":"Necromancer", "category":"attack", "type":"Magic", "damage":0,"desc":"Turn your defeated enemies into your pawns!","cooldown":0,"ult":False, "special":None, "mana":10},
            {"name":"Black Slash", "category":"attack", "type":"Physical", "damage":1800, "desc":"A strong attack from the Demon Destroyer","cooldown":3,"ult":False, "special":None, "mana":10, "effect":["Bleed"]},
            {"name":"Fire Ball", "category":"attack", "type":"Magic", "damage":50, "desc":"A basic skill from mages", "special":None,"cooldown":0,"ult":False, "mana":10, "effect":None},
            {"name":"Punch", "category":"attack","type":"Physical", "damage":10, "desc":"A basic attack anyone can do.", "special":None,"cooldown":0,"ult":False, "mana":10, "effect":None},
            {"name":"Black Divider", "category":"attack", "type":"Physical", "damage":2000, "desc":"A devastating attack from the Demon Destroyer","cooldown":4,"ult":True, "special":None, "mana":10, "effect":["Bleed"]},
            {"name":"Amaterasu", "category":"attack", "type":"Magic", "damage":100, "desc":"Burns infinitely","cooldown":4,"ult":True, "special":None, "mana":70, "effect":["Amaterasu"]},
            {"name":"Slash", "category":"attack", "type":"Physical", "damage":25, "desc":"basic slash attack","cooldown":0,"ult":False, "special":None, "mana":0, "effect":None},
            {"name":"Pierce", "category":"attack", "type":"Physical", "damage":45, "desc":"basic spear attack","cooldown":2,"ult":False, "special":None, "mana":0, "effect":None},

        ]






        global itemdict
        itemdict = Globals.getBattleItems()

        global Enemies
        Enemies = Globals.getEnemyList()



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
                                AbilityDictionary["cooldown"],
                                AbilityDictionary["ult"],
                                AbilityDictionary["special"],
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
                                AbilityDictionary["cooldown"],
                                AbilityDictionary["ult"],
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
                                AbilityDictionary["cooldown"],
                                AbilityDictionary["ult"],
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
            z = Op.CurrentHealth
            global Enemies
            global abilitydict
            global itemdict        
            bar = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")
            embed = discord.Embed(title = "%s"%(Op.Name), description = bar+ "%s/%s"%(Op.CurrentHealth, Op.TotalHealth), color = ctx.author.color)

            if WeaponOrAbility.effects:
                for x in WeaponOrAbility.effects:
                    if x.AffectsSender==True:
                        You.AddEffect(x)
                    else:
                        Op.AddEffect(x)
            if Defense:
                if Defense.effects:
                    for x in Defense.effects:
                        if x.AffectsSender==True:
                            Op.AddEffect(x)
                        else:
                            You.AddEffect(x)

            if WeaponOrAbility.special:
                em = WeaponOrAbility.special(You, Op, WeaponOrAbility, embed)
                embed = em[0]

            if Defense!=None:
                if Defense.WorksAgainst== "All" or Defense.WorksAgainst== WeaponOrAbility.type:
                    if Defense.special==None:

                        You.CallEffect()
                        Op.CallEffect()
                        You.EffectCooldown()
                        Op.EffectCooldown()

                        AmountOfDamage = int(WeaponOrAbility.damage+(You.Strength/15))
                        AmountOfDamage-=Defense.defends
                        if AmountOfDamage<0:
                            AmountOfDamage=0

                        TotalDamage = AmountOfDamage-Op.Defense
                        if TotalDamage<0:
                            TotalDamage=0
                        Op.DamageOpponent(TotalDamage)
                    else:
                        pass

                else:
                    You.CallEffect()
                    Op.CallEffect()
                    You.EffectCooldown()
                    Op.EffectCooldown()

                    AmountOfDamage = int(WeaponOrAbility.damage+(You.Strength/15))
                    TotalDamage = AmountOfDamage-Op.Defense
                    if TotalDamage<0:
                        TotalDamage=0
                    Op.DamageOpponent(TotalDamage)   
            else:
                You.CallEffect()
                Op.CallEffect()
                You.EffectCooldown()
                Op.EffectCooldown()

                AmountOfDamage = int(WeaponOrAbility.damage+(You.Strength/15))
                TotalDamage = AmountOfDamage-Op.Defense
                if TotalDamage<0:
                    TotalDamage=0
                Op.DamageOpponent(TotalDamage)   

            if Defense:
                if Defense.WorksAgainst== "All" or Defense.WorksAgainst== WeaponOrAbility.type:
                    if Defense.special:
                        FunctionToCall = Defense.special
                        ret = FunctionToCall(You, Op, WeaponOrAbility,embed)
                        You.EffectCooldown()
                        Op.EffectCooldown()

                        embed = ret[0]
                        TotalDamage = ret[1]

            bar = Globals.XpBar(Op.CurrentHealth, Op.TotalHealth, ":blue_square:", ":white_large_square:")
            embed.title = "%s"%(Op.Name)
            embed.description = bar+ "%s/%s"%(Op.CurrentHealth, Op.TotalHealth)
            if Op.Effects:
                finalstr = ""
                for x in Op.Effects:
                    midstr="%s (%s/%s)"%(Globals.GetFirstKey(x).name, x[Globals.GetFirstKey(x)], Globals.GetFirstKey(x).length)
                    finalstr+="%s\n%s\n"%(midstr, Globals.XpBar(x[Globals.GetFirstKey(x)], Globals.GetFirstKey(x).length, NumOfSquares=5))
                embed.add_field(name = "%s' Current Effects"%(Op.Name), value = finalstr)
            embed.add_field(name="%s used %s!"%(You.Name, WeaponOrAbility.name), value = "%s recieved %s points of damage!"%(Op.Name, z-Op.CurrentHealth))

            embed.add_field(name = "%s' Mana"%(You.Name), value = "%s/%s"%(You.Mana, You.Intelligence))
            Yourbar = Globals.XpBar(You.CurrentHealth, You.TotalHealth, "❤️", "🖤")     
            embed.set_footer(text = "%s \n %s \n %s/%s"%(You.Name, Yourbar, You.CurrentHealth, You.TotalHealth))

            CreateBattlefield(You, Op)
            file = discord.File("FightScene.png")
            embed.set_image(url = "attachment://FightScene.png")
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
                finlstri = ""
                finlstring=""
                check = False
                HasUlt = False
                for x in You.OnCooldown:
                    if not Globals.GetFirstKey(x).ult:
                        check = True
                        midstrri = "%s (%s/%s)"%(Globals.GetFirstKey(x).name,x[Globals.GetFirstKey(x)], Globals.GetFirstKey(x).cooldown)
                        finlstring+="%s\n%s\n"%(midstrri.center(20), Globals.XpBar(x[Globals.GetFirstKey(x)], Globals.GetFirstKey(x).cooldown, NumOfSquares=5))
                    else:
                        HasUlt=True
                        midstri = "%s (%s%%)"%(Globals.GetFirstKey(x).name,(Globals.GetFirstKey(x).cooldown-x[Globals.GetFirstKey(x)])/Globals.GetFirstKey(x).cooldown*100)
                        finlstri+="%s\n%s\n"%(midstri.center(20), Globals.XpBar(x[Globals.GetFirstKey(x)], Globals.GetFirstKey(x).cooldown,":white_large_square:", ":blue_square:",NumOfSquares=5, righttoleft=True))
                 
                if check==True:
                    embed.add_field(name = "Abilities Still On Cooldown:", value = finlstring)
                if HasUlt==True:
                    embed.add_field(name="Ultimate Status:",value= finlstri)
                else:
                    for x in You.Attacks+You.Defenses+You.support:
                        if x.ult:
                            embed.add_field(name = "Ultimate Status:", value = "Your ultimate, %s is ready!"%(x.name))



            CreateBattlefield(You, Op)
            file = discord.File("FightScene.png")
            embed.set_image(url = "attachment://FightScene.png")
            MessageToRef = await ctx.channel.send(embed=embed, file = file)
            print(You.OnCooldown)
            done=False
            await asyncio.sleep(2)
            while done==False:
                if You.Player!=None:
                    Choices = await Globals.AddChoices(self, ctx, ["❤️", "⚔️", "🏃"], MessageToRef, You.Player)
                    if Choices == "❤️":
                        if You.support:
                            CoolDownLIst = [x.name for x in Globals.GetKeysFromDictInList(You.OnCooldown)]
                            ActionChoice = [x.name for x in You.support if You.Mana>=x.mana and x.name not in CoolDownLIst]
                            ReturnedChoice = await Globals.ChoiceEmbed(self, ctx, ActionChoice, "Support!", p=You.Player)
                            You.Mana-=next(z for z in abilitydict if z["name"]==ReturnedChoice[0])["mana"]
                            You.abilityxp[ReturnedChoice[0]]+=10
                            return [next(x for x in You.support if x.name==ReturnedChoice[0]), "Support"]
                            break
                        else:
                            await ctx.channel.send("You dont have any support abilities/items lmao, try again")
                            pass

                    elif Choices =="⚔️":
                        if You.Attacks:
                            CoolDownLIst = [x.name for x in Globals.GetKeysFromDictInList(You.OnCooldown)]
                            ActionChoice = [x.name for x in You.Attacks if You.Mana>=x.mana and x.name not in CoolDownLIst]
                            ReturnedChoice = await Globals.ChoiceEmbed(self, ctx, ActionChoice, "Attack!", p=You.Player)
                            You.Mana-=next(z for z in abilitydict if z["name"]==ReturnedChoice[0])["mana"]
                            You.abilityxp[ReturnedChoice[0]]+=10
                            print(You.abilityxp)

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
                    Choices = "⚔️"
                    if You.CurrentHealth<You.TotalHealth:
                        Choices = random.choice(["❤️", "⚔️"])
                    else:
                        Choices = random.choice(["⚔️"])
                    if Choices == "❤️":
                        if You.support:                  
                            ActionChoice = [x.name for x in You.support if You.Mana>=x.mana and x.name not in Globals.GetKeysFromDictInList(You.OnCooldown)]
                            ReturnedChoice = random.choice(ActionChoice)
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
            
            if ability.effects:
                for x in ability.effects:
                    if x.AffectsSender==True:
                        User.AddEffect(x)
                    else:
                        Op.AddEffect(x)
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
            
            ChoiceList = Globals.ChoiceParts([x.name for x in Op.Defenses if x.mana<=Op.Mana and x not in Globals.GetKeysFromDictInList(Op.OnCooldown)])
            if Op.OnCooldown:
                finlstr = ""
                finlstrr=""
                check = False
                HasUlt = False
                for x in Op.OnCooldown:
                    if not Globals.GetFirstKey(x).ult:
                        check = True
                        midstrr = "%s (%s/%s)"%(Globals.GetFirstKey(x).name,x[Globals.GetFirstKey(x)], Globals.GetFirstKey(x).cooldown)
                        finlstrr+="%s\n%s\n"%(midstrr.center(20), Globals.XpBar(x[Globals.GetFirstKey(x)], Globals.GetFirstKey(x).cooldown, NumOfSquares=5))
                    else:
                        HasUlt=True
                        midstr = "%s (%s%%)"%(Globals.GetFirstKey(x).name,(Globals.GetFirstKey(x).cooldown-x[Globals.GetFirstKey(x)])/Globals.GetFirstKey(x).cooldown*100)
                        finlstr+="%s\n%s\n"%(midstr.center(20), Globals.XpBar(x[Globals.GetFirstKey(x)], Globals.GetFirstKey(x).cooldown,":white_large_square:", ":blue_square:",NumOfSquares=5, righttoleft=True))
                 
                if check==True:
                    embed.add_field(name = "Abilities Still On Cooldown:", value = finlstrr)
                if HasUlt==True:
                    embed.add_field(name="Ultimate Status:",value= finlstr)

            ChoiceDict = ChoiceList[0]
            ChoiceString = ChoiceList[1]
            ReactionList = ChoiceList[2]

            if ChoiceString:
                embed.add_field(name="%s can Defend!"%(Op.Name), value = "Make sure To defend In time!\n%s"%(ChoiceString))
            else:
                embed.add_field(name="%s cant Defend!"%(Op.Name), value = "You dont have any defense abilities!")
                await ctx.channel.send(embed=embed)
                return None
          
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
                DefenseSpec = next(x for x in Op.Defenses if x.name.lower()==Key.lower())
                if Op.Mana>=DefenseSpec.mana:
                    TheDefense = Defense(DefenseSpec.name, DefenseSpec.type, DefenseSpec.WorksAgainst, DefenseSpec.defends, DefenseSpec.cooldown, DefenseSpec.ult,DefenseSpec.special, DefenseSpec.mana, DefenseSpec.effects)
                    await ctx.channel.send(embed=discord.Embed(title = "%s Defends with %s!"%(Op.Name, TheDefense.name)))
                    You.abilityxp[TheDefense.name]+=10
                    return TheDefense
                else:
                    await ctx.channel.send(embed=discord.Embed(title = "You dont Have enough Mana!"))
                    return "Error"
            except:
                return ReturnChoices





        global EquipItem
        def EquipItem(user, item):
            global itemdict
            mmorpg = mulah.find_one({"id":user.id}, {"mmorpg"})["mmorpg"]
            loadout = mmorpg["loadout"]
            stats = mmorpg["stats"]
            inv = mulah.find_one({"id":user.id}, {"inv"})["inv"]
            SpecificItem = next(x for x in itemdict if x["name"].lower() == item.lower() and "parts" not in x.keys())
            if SpecificItem["type"] in loadout.keys():
                if loadout[SpecificItem["type"]]!=None:
                    print(SpecificItem)
                    CurrentItem = next(x for x in itemdict if x["name"] == loadout[SpecificItem["type"]])
                    print(CurrentItem)
                    Globals.AddToInventory(user, SpecificItem["name"], itemdict, 1)

                    if "attribute" in CurrentItem.keys():
                        for x in CurrentItem["attribute"].keys():
                            stats[x]-=CurrentItem["attribute"][x]
                    if "abilities" in CurrentItem.keys():
                        for x in CurrentItem["abilities"].keys():
                            try:
                                del mmorpg["abilities"][x]
                            except:
                                pass
                loadout[SpecificItem["type"]] = SpecificItem["name"]
                Globals.RemoveFromInventory(user, SpecificItem["name"], 1)

                if "attribute" in SpecificItem.keys():
                    for x in SpecificItem["attribute"].keys():
                        stats[x]+= SpecificItem["attribute"][x]
                if "abilities" in SpecificItem.keys():
                    for x in SpecificItem["abilities"]:
                        mmorpg["abilities"][x] = 1
                mulah.update_one({"id":user.id}, {"$set":{"mmorpg":mmorpg}})
                mulah.update_one({"id":user.id}, {"$set":{"inv":inv}})
            else:
                print("failure")
            



        global duelPlayer
        async def duelPlayer(ctx, PersonToDuel):
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
                levelling.find_one({"id":ctx.author.id}, {"xp"})["xp"],
                mulah.find_one({"id":ctx.author.id}, {"abilityxp"})["abilityxp"],
                mulah.find_one({"id":ctx.author.id}, {"duelwins"})["duelwins"],
                mulah.find_one({"id":ctx.author.id}, {"duelloses"})["duelloses"],
                mulah.find_one({"id":ctx.author.id}, {"duelretreats"})["duelretreats"],
                ((123,123)),
                ((20,199)),
                GetAttribute("attack", ctx.author),
                GetAttribute("defense", ctx.author),
                GetAttribute("support", ctx.author),
                [],
                ctx.author,
                []
                )

            Op = Opponent(
                PersonToDuel.display_name, 
                PersonToDuel.avatar_url, 
                mulah.find_one({"id":PersonToDuel.id}, {"mmorpg"})["mmorpg"]["stats"]["health"], 
                mulah.find_one({"id":PersonToDuel.id}, {"mmorpg"})["mmorpg"]["stats"]["health"], 
                mulah.find_one({"id":PersonToDuel.id}, {"mmorpg"})["mmorpg"]["stats"]["defense"], 
                mulah.find_one({"id":PersonToDuel.id}, {"mmorpg"})["mmorpg"]["stats"]["defense"], 
                mulah.find_one({"id":PersonToDuel.id}, {"mmorpg"})["mmorpg"]["stats"]["strength"], 
                mulah.find_one({"id":PersonToDuel.id}, {"mmorpg"})["mmorpg"]["stats"]["strength"],
                mulah.find_one({"id":PersonToDuel.id}, {"mmorpg"})["mmorpg"]["stats"]["intelligence"],
                mulah.find_one({"id":PersonToDuel.id}, {"mmorpg"})["mmorpg"]["stats"]["intelligence"],
                levelling.find_one({"id":PersonToDuel.id}, {"xp"})["xp"],
                mulah.find_one({"id":PersonToDuel.id}, {"abilityxp"})["abilityxp"],
                mulah.find_one({"id":PersonToDuel.id}, {"duelwins"})["duelwins"],
                mulah.find_one({"id":PersonToDuel.id}, {"duelloses"})["duelloses"],
                mulah.find_one({"id":PersonToDuel.id}, {"duelretreats"})["duelretreats"],
                ((123,123)),
                ((468,125)),
                GetAttribute("attack", PersonToDuel),
                GetAttribute("defense", PersonToDuel),
                GetAttribute("support", PersonToDuel),
                [],
                PersonToDuel,
                []
                )
            for x in GetAttribute("attack", ctx.author)+GetAttribute("defense", ctx.author)+GetAttribute("support", ctx.author):
                if x.ult:
                    You.AddToCooldown(x)
            for x in GetAttribute("attack", PersonToDuel)+GetAttribute("defense", PersonToDuel)+GetAttribute("support", PersonToDuel):
                if x.ult:
                    Op.AddToCooldown(x)

            winner=None
            loser=None
            retreater=None
            GameOver=False
            while GameOver==False:
                You.CooldownCheck()
                await asyncio.sleep(2)
                await ctx.channel.send(embed=discord.Embed(title = "It is now %s' Turn."%(You.Name)))
                await asyncio.sleep(2)

                This1 = await FightAction(self, ctx, Op, You)
                if This1[1]=="Attack":
                    ThisAttack = This1[0]
                    You.AddToCooldown(ThisAttack)
                    Thee = await Defend(self, ctx, You, Op, ThisAttack)
                    await asyncio.sleep(2)
                    if Thee == "Error":
                        This = await FinalDamage(self, ctx, ThisAttack, Op, You)
                    else:
                        This = await FinalDamage(self, ctx, ThisAttack, Op, You, Defense = Thee)
                    await ctx.channel.send(embed=This[0], file=This[1])
                
                elif This1[1]=="Support":
                    await asyncio.sleep(2)
                    ThisSupport = This1[0]
                    You.AddToCooldown(ThisSupport)
                    This = await SupportOpponent(self, ctx, You, Op, ThisSupport)
                    await ctx.channel.send(embed=This[0], file=This[1])  

                elif This1[1]=="Retreat":
                    You.duelretreats+=1
                    retreater=You
                    break


                if You.CurrentHealth<=0:
                    winner=Op
                    loser=You
                    Op.duelwins+=1
                    You.duelloses+=1
                    break

                if Op.CurrentHealth<=0:
                    winner=You
                    loser=Op

                    You.duelwins+=1
                    Op.duelloses+=1
                    break    

                Op.CooldownCheck()
                await asyncio.sleep(2)
                await ctx.channel.send(embed=discord.Embed(title = "It is now %s' Turn."%(Op.Name))) 
                await asyncio.sleep(2)
                This1 = await FightAction(self, ctx, You, Op)
                if This1[1]=="Attack":
                    ThisAttack = This1[0]
                    Op.AddToCooldown(ThisAttack)
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
                    Op.AddToCooldown(ThisSupport)
                    This = await SupportOpponent(self, ctx, Op, You, ThisSupport)
                    await ctx.channel.send(embed=This[0], file=This[1])  

                elif This1[1]=="Retreat":
                    Op.duelretreats+=1
                    retreater=Op
                    break


                if You.CurrentHealth<=0:
                    winner=Op
                    loser=You
                    Op.duelwins+=1
                    You.duelloses+=1
                    break

                if Op.CurrentHealth<=0:
                    winner=You
                    loser=Op
                    You.duelwins+=1
                    Op.duelloses+=1
                    break    
            updateDuelDb(You)
            updateDuelDb(Op)
            return {"winner":winner, "loser":loser, "retreater":retreater}





















    @commands.command()
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
        YouWins =mulah.find_one({"id":ctx.author.id}, {"duelwins"})["duelwins"] 
        Youloss =mulah.find_one({"id":ctx.author.id}, {"duelloses"})["duelloses"] 

        for x in GetAttribute("attack", ctx.author)+GetAttribute("defense", ctx.author)+GetAttribute("support", ctx.author):
            if x.ult:
                You.AddToCooldown(x)
        print(You.Defenses)
        GameOver=False
        while GameOver==False:
            You.CooldownCheck()
            await asyncio.sleep(2)
            await ctx.channel.send(embed=discord.Embed(title = "It is now %s' Turn."%(You.Name)))
            await asyncio.sleep(2)

            This1 = await FightAction(self, ctx, Op, You)
            if This1[1]=="Attack":
                ThisAttack = This1[0]
                You.AddToCooldown(ThisAttack)
                Thee = await Defend(self, ctx, You, Op, ThisAttack)
                await asyncio.sleep(2)
                if Thee == "Error":
                    This = await FinalDamage(self, ctx, ThisAttack, Op, You)
                else:
                    This = await FinalDamage(self, ctx, ThisAttack, Op, You, Defense = Thee)
                await ctx.channel.send(embed=This[0], file=This[1])
            
            elif This1[1]=="Support":
                await asyncio.sleep(2)
                ThisSupport = This1[0]
                You.AddToCooldown(ThisSupport)
                This = await SupportOpponent(self, ctx, You, Op, ThisSupport)
                await ctx.channel.send(embed=This[0], file=This[1])  

            elif This1[1]=="Retreat":
                break

            if You.CurrentHealth<=0:
                await ctx.channel.send("%s has perished. %s is victorious!"%(You.Name, Op.Name))
                Youloss+=1
                break

            if Op.CurrentHealth<=0:
                await ctx.channel.send("%s has perished. %s is victorious!"%(Op.Name, You.Name))
                YouWins+=1
                break       

            Op.CooldownCheck()
            await asyncio.sleep(2)
            await ctx.channel.send(embed=discord.Embed(title = "It is now %s' Turn."%(Op.Name))) 
            await asyncio.sleep(2)
            for x in GetAttributeEnemy("attack", "acnologia")+GetAttributeEnemy("defense", "acnologia")+GetAttributeEnemy("support", "acnologia"):
                if x.ult:
                    You.AddToCooldown(x)
            This1 = await FightAction(self, ctx, You, Op)
            if This1[1]=="Attack":
                ThisAttack = This1[0]
                Op.AddToCooldown(ThisAttack)
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
                Op.AddToCooldown(ThisSupport)
                This = await SupportOpponent(self, ctx, Op, You, ThisSupport)
                await ctx.channel.send(embed=This[0], file=This[1])  

            elif This1[1]=="Retreat":
                break

            if You.CurrentHealth<=0:
                await ctx.channel.send("%s has perished. %s is victorious!"%(You.Name, Op.Name))
                OpWins+=1
                Youloss+=1
                beak

            if Op.CurrentHealth<=0:
                await ctx.channel.send("%s has perished. %s is victorious!"%(Op.Name, You.Name))
                YouWins+=1
                Oploss+=1
                break     







    @commands.command()
    async def rob(self, ctx, PersonToRob:discord.Member):
        global abilitydict
        global Enemies
        global GetAttribute
        embed = discord.Embed(title = "You are being robbed by %s"%(ctx.author.display_name), description = "Think You can defend your hard earned coins?, %s"%(PersonToRob.mention), color = discord.Color.red())
        embed.add_field(name = "Will you defend your cash?", value = "react with ✅ to accept \n react with ❌ to decline")
        embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text = datetime.now().strftime("%Y-%m-%d, %H:%M"))
        msg = await ctx.channel.send(embed=embed)
        for x in ["✅", "❌"]:
            await msg.add_reaction(x)
        def check(reaction, user):
            return user==PersonToRob and str(reaction.emoji) in ["✅", "❌"] and reaction.message==msg
        try:
            confirm = await self.client.wait_for('reaction_add', check=check, timeout=10)
            if confirm:
                rawreaction = str(confirm[0])
                print(rawreaction)
                if rawreaction == "❌":
                    await ctx.channel.send("%s refuses to defend himself, what a coward"%(PersonToRob.display_name))
                    return
                else:
                    await ctx.channel.send("%s has caught you. Square tf up"%(PersonToRob.display_name))
        except asyncio.TimeoutError:
            embed = discord.Embed(title = "Robbery", description = "Victim: %s"%(PersonToRob.display_name), color = discord.Color.green())
            embed.set_thumbnail(url=PersonToRob.avatar_url)
            embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
            embed.add_field(name="Status",value="`unnoticed`")
            
            wallet = mulah.find_one({"id":PersonToRob.id}, {"money"})["money"]
            steal = wallet*0.05
            embed.set_footer(text="You have stolen $%g"%(steal))
            await ctx.channel.send(embed=embed)
            mulah.update_one({"id":ctx.author.id}, {"$inc":{"money":steal}})
            mulah.update_one({"id":PersonToRob.id}, {"$inc":{"money":steal*(-1)}})

            return
        resultdict=await duelPlayer(ctx, PersonToRob)
        winner=resultdict["winner"]
        loser=resultdict["loser"]
        retreater=resultdict["retreater"]

        try:
            if winner.Name ==ctx.author.display_name:
                embed = discord.Embed(title = "Robbery", description = "Victim: %s"%(PersonToRob.display_name), color = discord.Color.green())
                embed.set_thumbnail(url=PersonToRob.avatar_url)
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
                embed.add_field(name="Status",value="`victorious`")
                
                wallet = mulah.find_one({"id":PersonToRob.id}, {"money"})["money"]
                steal = wallet*0.08
                embed.set_footer(text="You have stolen $%g"%(steal))
                await ctx.channel.send(embed=embed)
                mulah.update_one({"id":winner.Player.id}, {"$inc":{"money":steal}})
                mulah.update_one({"id":loser.Player.id}, {"$inc":{"money":steal*(-1)}})
                return
            if retreater.Name==ctx.author.display_name:
                embed = discord.Embed(title = "Robbery", description = "Victim: %s"%(PersonToRob.display_name), color = discord.Color.green())
                embed.set_thumbnail(url=PersonToRob.avatar_url)
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
                embed.add_field(name="Status",value="`retreated`")
                
                wallet = mulah.find_one({"id":PersonToRob.id}, {"money"})["money"]
                steal = wallet*0.08
                embed.set_footer(text="pussy")
                mulah.update_one({"id":loser.Player.id}, {"$inc":{"money":steal*(-1)}})
                mulah.update_one({"id":winner.Player.id}, {"$inc":{"money":steal}})

                await ctx.channel.send(embed=embed)   
            if winner.Name==PersonToRob.display_name:
                embed = discord.Embed(title = "Robbery", description = "Victim: %s"%(PersonToRob.display_name), color = discord.Color.green())
                embed.set_thumbnail(url=PersonToRob.avatar_url)
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.display_name)
                embed.add_field(name="Status",value="`defeated`")
                
                wallet = mulah.find_one({"id":PersonToRob.id}, {"money"})["money"]
                steal = wallet*0.05
                embed.set_footer(text="You have lost $%g"%(steal))
                mulah.update_one({"id":winner.Player.id}, {"$inc":{"money":steal}})
                mulah.update_one({"id":loser.Player.id}, {"$inc":{"money":steal*(-1)}})   
        except:
            print(traceback.format_exc())















    @commands.command()
    async def duel(self, ctx, PersonToDuel:discord.Member):
        global abilitydict
        global Enemies
        global GetAttribute
        embed = discord.Embed(title = "You recieved a Duel Invitation from %s"%(ctx.author.display_name), description = "Answer quickly, %s"%(PersonToDuel.mention), color = discord.Color.red())
        embed.add_field(name = "Will you accept this duel?", value = "react with ✅ to accept \n react with ❌ to decline")
        embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text = datetime.now().strftime("%Y-%m-%d, %H:%M"))
        msg = await ctx.channel.send(embed=embed)
        for x in ["✅", "❌"]:
            await msg.add_reaction(x)
        def check(reaction, user):
            return user==PersonToDuel and str(reaction.emoji) in ["✅", "❌"] and reaction.message==msg
        try:
            confirm = await self.client.wait_for('reaction_add', check=check, timeout=60)
            if confirm:
                rawreaction = str(confirm[0])
                print(rawreaction)
                if rawreaction == "❌":
                    await ctx.channel.send("%s declined the duel request"%(PersonToDuel.display_name))
                    return
                else:
                    await ctx.channel.send("%s accepted. the duel will begin shortly."%(PersonToDuel.display_name))
        except TimeoutError:
            await ctx.channel.send("%s took too long."%(PersonToDuel.display_name))
            return
        resultdict=await duelPlayer(ctx, PersonToDuel)
        winner=resultdict["winner"]
        loser=resultdict["loser"]
        retreater=resultdict["retreater"]
        try:
            embed = discord.Embed(title = "Duel Outcome", description = "Victor:%s\n Defeated:%s"%(winner.Name,loser.Name), color=discord.Color.gold())
            embed.add_field(name="Reward:", value="%s has been granted 200xp"%(winner.Name))
            embed.set_footer(text = datetime.now().strftime("%Y-%m-%d, %H:%M"))
            levelling.update_one({"id":winner.Player.id}, {"$inc":{"xp":200}})
            await ctx.channel.send(embed=embed)
        except:
            embed = discord.Embed(title = "Duel Outcome", description = "null"%(winner.Name,loser.Name), color=discord.Color.gold())
            embed.add_field(name="Status:", value="%s has retreated"%(retreater.Name))
            embed.set_footer(text = datetime.now().strftime("%Y-%m-%d, %H:%M"))
            await ctx.channel.send(embed=embed)
     

    @commands.command()
    async def equip(self, ctx, items:str):
        global EquipItem
        global itemdict
        allperms=False
        if ctx.author.id==643764774362021899:
            allperms = True
        SpecificItem = next(x for x in itemdict if x["name"].lower()==items.lower())

        if allperms ==True:
            EquipItem(ctx.author, SpecificItem["name"])
            embed = discord.Embed(title = "Successfull equip", description = "You have equipped `%s` to your `%a` slot"%(SpecificItem["name"], SpecificItem["type"]), color = discord.Color.green())
            await ctx.channel.send(embed=embed)

        else:
            if Globals.InvCheck(ctx.author, item=items):
                EquipItem(ctx.author, SpecificItem["name"])
                embed = discord.Embed(title = "Successfull equip", description = "You have equipped `%s` to your `%a` slot"%(SpecificItem["name"], SpecificItem["type"]), color = discord.Color.green())
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send("You dont have this item in your inventory.")


    @commands.command()
    async def upgrade(self, ctx):
        first = True
        leave = False
        while leave ==False:
            mmorpg = mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]
            stats = mmorpg["stats"]
            Points = Globals.InvCheckWithItem(ctx.author, "UpgradePoint", False)
            print(Points)
            try:
                embed = discord.Embed(title = "Upgrade station- You have %g Upgrade Points!"%(Points["amount"]), desription = "Use `UpgradePoint`'s to upgrade your stats! an upgrade point can add either `3 strength`, `3 defense`, `3 intelligence` or `3 health`", color = discord.Color.blue())
            except:
                embed = discord.Embed(title = "Upgrade station- You dont have anymore Upgrade Points!", description = "Go duel someone or be more active in text channels!", color = discord.Color.gold())
            for x in stats:
                embed.add_field(name = x, value = stats[x], inline=False)
            try:
                await msg.edit(embed=embed)
            except:
                msg = await ctx.channel.send(embed=embed)
            if Points["amount"]>0:
                choices = ["⚔️", "❤️", "🧪", "🛡️", "🚪"]
                if first:
                    for x in choices:
                        await msg.add_reaction(x)
                else:
                    await msg.remove_reaction(reaction, ctx.author)
                
                ReactionDict = {"⚔️":"strength", "❤️":"health","🧪":"intelligence","🛡️":"defense"}
                def check(reaction, user):
                    return user==ctx.author and str(reaction.emoji) in choices and reaction.message == msg
                try:
                    confirm = await self.client.wait_for('reaction_add',check=check, timeout = 60)
                except TimeoutError:
                    break
                if confirm:
                    reaction = str(confirm[0])
                print(reaction)
                if reaction == "Timeout" or reaction=="🚪":
                    print("it is")
                    break
                else:
                    stats[ReactionDict[reaction]]+=3
                    mmorpg["stats"]=stats
                    Globals.RemoveFromInventory(ctx.author, "UpgradePoint", 1)
                    mulah.update_one({"id":ctx.author.id}, {"$set":{"mmorpg":mmorpg}})
                    first = False
            else:
                print("no upgrade points")
                break
        embed =discord.Embed(title = "you left!")
        
        await ctx.channel.send(embed=embed)

                


    @commands.command()
    async def begin(self, ctx):
        global StoryEmbed
        mmorpg = mulah.find_one({"id":ctx.author.id}, {"mmorpg"})["mmorpg"]
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
