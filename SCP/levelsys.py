import asyncio
from logging import makeLogRecord
import discord
from discord import errors
from discord import message
from discord import reaction
from discord.ext import commands
import imdb
from pymongo import MongoClient
import random
import re
from better_profanity import profanity
import asyncio
import youtube_dl
from youtube_search import YoutubeSearch
import json
import traceback

cluster = MongoClient('mongodb+srv://SCPT:Geneavianina@scptsunderedatabase.fp8en.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
levelling = cluster["discord"]["levelling"]
class levelsys(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        global badwords
        badwords = ["fuck", "bitch", "shit", "cunt", "entot", "anjing", "asw", "ngentod", "goblok", "gblk", "wtf", "ngentot"]
        global badwordresponse
        badwordresponse = ["Language. My  creator senpai does not support that vulgar language.", "Shut up. Dont taint this server with those words.", "Do not swear. use of those words is unacceptable."]
        profanity.load_censor_words()
        if any(word in message.content.casefold() for word in badwords):
            await message.delete()
            randbadwords = random.choice(badwordresponse)
            count = 0
            for badwordint in range(0,len(badwords)):
                count+= len(re.findall(badwords[badwordint], message.content.casefold()))
                message.content = message.content.casefold().replace(badwords[badwordint],"*censor*")

            embed = discord.Embed(title = "Hey. I noticed that you tried to swear.", description = "%s"%(randbadwords))
            embed.add_field(name = "%s intended to say,"%(re.sub("\#\d{4}$", "", str(message.author))), value = "%s"%(message.content))
            await message.channel.send(embed = embed)
            try:
                swearvar = levelling.find_one({"id":message.author.id}, {"swears"})
                swearval = swearvar["swears"]
                swearval+=count
                levelling.update_one({"id":message.author.id},{"$set":{"swears":swearval}})
            except:
                levelling.update_one({"id":message.author.id},{"$set":{"swears":1}})
        else:
            pass



        stats = levelling.find_one({"id" : message.author.id})
        if not message.author.bot:
            if stats is None:
                newuser = {"id" : message.author.id, "xp" :100}
                levelling.insert_one(newuser)
            else:
                xp = stats["xp"] + 5
                levelling.update_one({"id":message.author.id}, {"$set":{"xp":xp}})
                lvl = 0
                while True:
                    if xp < ((50*(lvl**2))+(50*(lvl))):
                        break
                    lvl+=1
                xp-=((50*((lvl-1)**2))+(50*(lvl-1)))
                if xp ==0:
                    embed = discord.Embed(title = "You have leveled up to level %s"%(lvl))
                    embed.set_thumbnail(url = message.author.avatar_url)
                    await message.channel.send(embed=embed)


    @commands.command()
    async def swear(self,ctx, p1:discord.Member=None):
        if p1 is None:
            try:
                swearvar = levelling.find_one({"id":ctx.author.id},{"swears"})
                swearval = swearvar["swears"]
                id = ctx.guild
                for x in ctx.guild.members:
                    print(x)
                embed = discord.Embed(title = "You have sworn %s times."%(swearval), color = ctx.author.color)
                embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            except:
                await ctx.channel.send("You need to swear, motherfucker.")
        else:
            try:
                swearvar = levelling.find_one({"id":p1.id},{"swears"})
                swearval = swearvar["swears"]
                id = p1.guild
                for x in p1.guild.members:
                    print(x)
                embed = discord.Embed(title = "%s has sworn %s times."%(p1.display_name, swearval), color = ctx.author.color)
                embed.set_author(name = p1.display_name, icon_url=p1.avatar_url)
                await ctx.channel.send(embed=embed)
            except:
                await ctx.channel.send("they need to swear first, motherfucker.")            



    @commands.command()
    async def rank(self, ctx):
        stats = levelling.find_one({"id": ctx.author.id})
        if stats is None:
            embed = discord.Embed(title = "You havnt sent any messages yet.")
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
            embed = discord.Embed(title = "%s level stats"%(ctx.author.name))
            embed.add_field(name = "Name", value = ctx.author.mention, inline = True)
            embed.add_field(name = "xp", value =f"{xp}/{int(200*((1/2)*lvl))}", inline = True)   
            embed.add_field(name = "progress bar", value = boxes*":blue_square:" + (20-boxes) *":white_large_square:", inline = False)  
            embed.set_thumbnail(url = ctx.author.avatar_url)    
            await ctx.channel.send(embed = embed)

    

    @commands.command()
    async def swearlb(self, ctx):
        ids = [x.id for x in ctx.guild.members]
        rankings = levelling.find().sort("swears",-1)
        count=0
        for x in levelling.find():
            print(x["xp"])
            count+=1
        print(count)
        i=1
        embed = discord.Embed(title = "Swear Leaderboard", color = ctx.author.color)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(int(x["id"])).display_name

                tempswears = x["swears"]
                embed.add_field(name = f"{i}: {temp}", value = f"Swears: {tempswears}", inline = False) 
                i+=1
                if i==11:
                    break
            except:
                pass
        await ctx.channel.send(embed=embed)


    @commands.group(invoke_without_command=True)
    async def summon(self,ctx):
        if str(ctx.author) == "SentientPlatypus#1332":
            await ctx.channel.send("summon someone, creator senpai.")
        else:
            await ctx.channel.send("begone!")
    @summon.group()
    async def jesus(self, ctx):
        if str(ctx.author) == "SentientPlatypus#1332":
            rankings = levelling.find().sort("swears",-1)
            for x in rankings:
                levelling.update_one({"id":x["id"]}, {"$set":{"swears":0}})
            await ctx.channel.send(embed=discord.Embed(title = "Creator senpai has summoned Jesus.", description = "Sin no more!", color = ctx.author.color))
        else:
            await ctx.channel.send("begone!")        

def setup(client):
    client.add_cog(levelsys(client))




