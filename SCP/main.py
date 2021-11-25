
from functools import update_wrapper
from discord.colour import Color
from discord.ext.commands import bot
from discord.ext.commands.converter import EmojiConverter
from discord.ext.commands.core import is_nsfw
from discord.ext.commands.errors import NSFWChannelRequired
from mcstatus import MinecraftServer
import discord
import os
import json
import traceback
from discord import message
from discord import embeds
from discord import channel
from discord import activity
from discord.enums import ActivityType
from discord.flags import Intents
import requests
import random
from discord.ext import commands, tasks, ipc
import asyncio
import re
import time
import itertools
from itertools import cycle, permutations, product
import enchant
import math
import string
import youtube_dl
from random_word import RandomWords
from sympy.solvers import solve
import praw
import asyncpraw
import aiohttp
import levelsys
from youtube_search import YoutubeSearch
import wolframalpha
import urllib.parse
from pprint import pprint
import currencysys
from PIL import Image
from io import BytesIO
import mmorpgGame
import DatabaseHandler
from pymongo import MongoClient
from DatingSim import noGirlfriend 
from DatingSim import noWatchlist
import DatingSim
import GuildHandler
import sys	
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import datetime
from english_words import english_words_set
import Images
import games
import extras
import ssl
import Globals
import pymongo
from typing import Optional
import moderation
import HelpCommand
import automod
from pymongo.database import Database
from youtube_search import YoutubeSearch
import json
import youtube_dl
from imdb import IMDb

cogautomod = [automod]
cogMod = [moderation]
cogHelp = [HelpCommand]
cogExtras = [extras]
cogGame = [games]
cogImage = [Images]
cogGuild = [GuildHandler]
cogsmulah = [currencysys]
cogs = [levelsys]
cogsmmorpg = [mmorpgGame]
cogDB = [DatabaseHandler]
coggf = [DatingSim]
d = enchant.Dict("en_US")
cluster = Globals.getMongo()
levelling = cluster["discord"]["levelling"]
DiscordGuild = cluster["discord"]["guilds"]
mulah = cluster["discord"]["mulah"]

tagre = "\#\d{4}$"



class Scp(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc = ipc.Server(self, secret_key="g")
    

    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("Ipc server is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)




async def determine_prefix(bot,message):
    guild = message.guild
    if guild:
        prefix = DiscordGuild.find_one({"id":guild.id}, {"prefix"})["prefix"]
        return prefix
    else:
        return "^"
client = Scp(command_prefix=determine_prefix, intents =discord.Intents.all(), status=discord.Status.online)



@client.ipc.route()
async def get_guild_count(data):
    return len(client.guilds)

@client.ipc.route()
async def get_guild_ids(data):
    final = [x.id for x in client.guilds]
    return final

@client.ipc.route()
async def get_guild(data):
    guild = client.get_guild(data.guild_id)
    if guild is None:
        return None
    else:
        return "%s"%(guild)

@client.ipc.route()
async def getDocumentation(data):
    commandDict = {}
    def cmdhelp(command):
        commandDict[command.name] = {"name": command.name, "usage":Globals.noEmbedSyntax(command), "desc":command.help}

    for command in client.commands:
        cmdhelp(command)
    
    return commandDict


@client.ipc.route()
async def get_guild_settings(data):
    def swearleader(guildid):
        guild = client.get_guild(guildid)
        ids = [x.id for x in guild.members]
        rankings = levelling.find().sort("swears",-1)
        returnlist = []
        count=0
        i=1
        for x in rankings:
            try:
                temp = guild.get_member(int(x["id"])).display_name

                tempswears = x["swears"]
                returnlist.append(f"{temp}'s' Swears: `{tempswears}`") 
                i+=1
                if i==11:
                    break
            except:
                pass
        return returnlist

    def rankleader(guildid):
        guild = client.get_guild(guildid)
        ids = [x.id for x in guild.members]
        rankings = levelling.find().sort("xp",-1)
        returnlist = []
        i=1
        for x in rankings:
            try:
                temp = guild.get_member(int(x["id"])).display_name

                tempswears = x["xp"]
                returnlist.append(f"{temp}'s Level: `{Globals.getLevelfromxp(tempswears)}`") 
                i+=1
                if i==11:
                    break
            except:
                pass
        return returnlist

    def richleader(guildid):
        guild = client.get_guild(guildid)
        ids = [x.id for x in guild.members]
        returnlist = []
        rankings = mulah.find().sort("net",-1)
        count=0
        i=1
        for x in rankings:
            try:
                temp = guild.get_member(int(x["id"])).display_name

                tempswears = x["net"]
                returnlist.append(f"{temp}'s net worth: `${tempswears}`") 
                i+=1
                if i==11:
                    break
            except:
                pass
        return returnlist

    guildid = data.guild_id

    prefix = DiscordGuild.find_one({"id":guildid}, {"prefix"})["prefix"]
    currentGuildSettings = DiscordGuild.find_one({"id":guildid}, {"settings"})["settings"]
    announcementChannels =DiscordGuild.find_one({"id":guildid}, {"announcement channels"})["announcement channels"]
    suggestionChannels =DiscordGuild.find_one({"id":guildid}, {"suggestion channels"})["suggestion channels"]
    automod = DiscordGuild.find_one({"id":guildid}, {"automod"})["automod"]
    badwords = DiscordGuild.find_one({"id":guildid}, {"badwords"})["badwords"]
    swearlb = swearleader(guildid)
    ranklb = rankleader(guildid)
    richlb = richleader(guildid)


    settings = {
        "Profanity Filter": currentGuildSettings["Profanity Filter"]["enabled"],
        "lol on message" : currentGuildSettings["lol on message"]["enabled"],
        "announce": currentGuildSettings["announce"]["enabled"],
        "suggest":currentGuildSettings["suggest"]["enabled"],

        "prefix":prefix,
        "announcement channels":[{client.get_channel(x).name:x} for x in announcementChannels],
        "suggestion channels":[{client.get_channel(x).name:x} for x in suggestionChannels],
        "automod":automod,
        "badwords":badwords,

        "richlb":richlb,
        "ranklb":ranklb,
        "swearlb":swearlb
    }
    return settings

@client.command()
async def get_guild_settings(data):
    commandDict = {}
    def cmdhelp(command):
        commandDict[command.name] = {"name": command.name, "usage":Globals.noEmbedSyntax(command), "desc":command.help}

    for command in client.commands:
        cmdhelp(command)
    
@client.ipc.route()
async def return_channels(data):
    guild = client.get_guild(data.guild_id)
    textchannels = guild.text_channels
    textchannelnames = []
    for x in textchannels:
        textchannelnames.append({x.name:x.id})
    return textchannelnames


@client.command()
async def return_channels(data):
    guild = client.get_guild(data.guild.id)
    textchannels = guild.text_channels
    textchannelnames = [x.name for x in textchannels]
    await data.channel.send(textchannelnames)










##---------------------------------------HELP COMMANDS------------------------------------------------------------
@client.group(invoke_without_command=True)
async def helpp(ctx):
    embed = discord.Embed(title = "Help", description = "Use ^help <command> for extended information on a command.",color = ctx.author.color)
    embed.add_field(name = "Moderation🚨", value = "`^help mod`")
    embed.add_field(name = "Fun😃", value = "`^help fun`")
    embed.add_field(name = "games🎮", value = "`^help games`")
    embed.add_field(name = "solve🖩", value = "`^help solve`")
    embed.add_field(name = "Voice Chat 🎵 ", value = "`^help voice`")	
    embed.add_field(name = "Math📚📐📏", value = "`^help mafs`")
    embed.add_field(name = "Web🌎", value = "`^help web`")
    embed.add_field(name = "Levels📈", value = "`^help levels`")
    embed.add_field(name = "currency💰", value = "`^help money`")
    embed.add_field(name = "DatingSim❤️", value = "`^help gf`")
    embed.add_field(name = "Images📷", value = "`^help image`")
    embed.add_field(name = "duels ⚔️", value = "`^help duels`")
    embed.add_field(name = "Settings ⚙️", value = "`^help config`")
    

    await ctx.send(embed = embed)


##-------------------------profanitycheck-------------------
badwords = ["fuck", "bitch", "shit", "cunt", "entot", "anjing", "asw", "ngentod", "goblok", "gblk", "wtf", "ngentot"]
def profanitycheck(string):
    if any(word in string for word in badwords):
        return True
    else:
        return False

    




















##-------------------------------------------FUN-----------------------------------------


    #STATS

def attractivelevel(player):
    if 0<=player<=25:
        return "f in the chat"
    if 25<player<=50:
        return "you are average"
    if 50<player<=75:
        return "you are pretty attractive"
    if 75<player<100:
        return "Absolute gigachad"
            #intelligence
def intelligencelevel(player):
    if 0<=player<=25:
        return "Have you been held back before?"
    if 25<player<=50:
        return "you are average"
    if 50<player<=75:
        return "you are pretty intelligent"
    if 75<player<100:
        return "Go apply to MIT"
        #simpness
def simplevel(player):
    if 0<=player<=25:
        return "You are a slight simp"
    if 25<player<=50:
        return "you are an average simp. Arent we all?"
    if 50<player<=75:
        return "idk man, thats pretty simp"
    if 75<player<100:
        return "I bet you are a tier 3 subscriber to belle delphine"
    #epicgamer
def epicgamerlevel(player):
    if 0<=player<=25:
        return "disgusting"
    if 25<player<=50:
        return "you are an average epicgamer. Arent we all?"
    if 50<player<=75:
        return "idk man, thats pretty epicgamer"
    if 75<player<100:
        return "I bet you are a tier 3 floor gang member"

@client.command(name = "rate", help = "Provides accurate statistics about the author.")
async def rate(ctx, user:discord.Member=None):
    if not user:
        user=ctx.author

    attractivenum = int(random.randint(1,100))
    intelligencenum = int(random.randint(1,100))
    simpnum = int(random.randint(1,100))
    epicgamernum = int(random.randint(1,100))
    lifeexpectancynum = int(random.randint(60,100))
    attractiveness = attractivelevel(attractivenum)
    intelligence = intelligencelevel(intelligencenum)
    simpness = simplevel(simpnum)
    epicgamerness = epicgamerlevel(epicgamernum)
    embed=discord.Embed(title = "%s's Stats:"%(re.sub("\#\d{4}$", "", str(user.display_name))), description = "Provides accurate stats about the user", color = user.color)
    embed.add_field(name = ":100: Waifu rating:", value = "%d/100 \n %s"%(attractivenum, attractiveness))
    embed.add_field(name = ":brain: intelligence rating:", value = "%d/100 \n %s"%(intelligencenum, intelligence))	
    embed.add_field(name = ":flushed: simp rating:", value = "%d/100 \n %s"%(simpnum, simpness))
    embed.add_field(name = ":video_game: epicgamer rating:", value = "%d/100 \n %s"%(epicgamernum, epicgamerness))
    embed.add_field(name = ":heart: Life expectancy:", value = "%d years."%(lifeexpectancynum))
    await ctx.send(embed = embed)

@client.command(name = "wisdom", help = "Recieve wisdom from my Creator senpai")
async def wisdom(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    quotess = ["no truer words have been spoken.", "That was very inspiring.", "Be thankful for this invaluable knowledge"]
    embed = discord.Embed(title = "Wisdom machine", description = "I will grant you a small fraction of my creator senpai's wisdom.")
    embed.add_field(name = "%s"%(quote), value = "-%s\n\n%s"%(json_data[0]['a'],random.choice(quotess)))
    await ctx.send(embed =embed)   	


@client.command()
async def story(ctx, *, statement):
    await ctx.trigger_typing()
    final = Globals.gpt3completion(statement)
    embed = discord.Embed(title = statement, description = final, color = discord.Color.blue())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.timestamp = ctx.message.created_at
    await ctx.channel.send(embed=embed)

@client.command()
async def yomomma(ctx):     
    req = requests.get('https://api.yomomma.info').json()["joke"]
    embed = discord.Embed(title = "Yomomma Machine", description = req, color = ctx.author.color)
    await ctx.channel.send(embed=embed)



@client.command()
async def p(ctx, search, channel):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': '249/250/251',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    yt = YoutubeSearch("".join(search), max_results=1).to_json()
    try:
        yt_id = str(json.loads(yt)['videos'][0]['id'])
        yt_url = 'https://www.youtube.com/watch?v='+yt_id
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegOpusAudio("song.mp3"))
    except:
        pass





@client.command()
async def rickroll(ctx, channel):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=channel)
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': '249/250/251',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(["https://www.youtube.com/watch?v=g8jWi6ipSew"])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegOpusAudio("song.mp3"))


@client.command()
async def ping(ctx):
    embed=discord.Embed(title="Pong!", description="bot latency is %gms"%(round(client.latency*1000)))
    embed.add_field(name="API Latency", value=f'{(round(client.latency * 1000))} ms', inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Im not connected to anything.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("what am i supposed to pause?")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:	
        await ctx.send("what am I supposed to unpause?")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()



#PP
@client.command(name = "pp", help = "Get an accurate pp measure")
async def pp(ctx, user:discord.Member=None):
    if not user:
        user=ctx.author
    ppnum = random.randint(1,10)
    ppsize = "="*ppnum
    ppfinal = "8%sD" %(ppsize)
    embed = discord.Embed(title = "PP inspection", description = "Accurate PP measure.", color = user.color)
    embed.add_field(name = "**%s's results**"%(re.sub("\#\d{4}$", "", str(user.display_name))), value = "%s"%(ppfinal) )
    await ctx.channel.send(embed=embed)








@client.command()
async def info(ctx):
    embed=discord.Embed(title="Amoris Information", color=discord.Color.purple())
    embed.description= "Servers: %g\nMembers:%g"%(len(client.guilds), getNumMembers())
    embed.add_field(name="Resources", value="[Support Server](https://discord.gg/Nn6Cwmdd6U)\n [Invite Link](https://discord.com/api/oauth2/authorize?client_id=822265614244511754&permissions=8&scope=bot)\n [Server Dashboard](http://scp16tsundere.pagekite.me:443)")
    embed.set_thumbnail(url=client.user.avatar_url)
    await ctx.channel.send(embed=embed)











##-------------------------------------------------MODERATION-----------------------------------------------
EditedMessages = {

}
@client.event
async def on_message_edit(before, after):
    EditedMessages[before.channel.id]= [before.author.display_name, before.author.avatar_url, before.content, before.created_at]

DeletedMessage = {

}
@client.event
async def on_message_delete(message):
    DeletedMessage[message.channel.id] = [message.author.display_name, message.author.avatar_url,message.content, message.created_at]


@helpp.command()
async def mod(ctx):
    embed = discord.Embed(title = "Moderation🚨", description = "help moderating text servers.", color = ctx.author.color)
    embed.add_field(name = "Commands", value = "`clean`, `credit`, `poll`, `esnipe`, `snipe, `timer``")
    await ctx.send(embed = embed)

@helpp.command()
async def timer(ctx):
    embed = discord.Embed(title = "Timer!", description = "adds a timer", color = ctx.author.color)
    embed.add_field(name = "syntax", value = "`^timer '<title>' '<description>' '<00:00:00>'")
    await ctx.send(embed = embed)

@client.command()
async def snipe(ctx):
    try:
        embed = discord.Embed(description = DeletedMessage[ctx.channel.id][2], color = discord.Color.blue())
        embed.set_author(name=DeletedMessage[ctx.channel.id][0],icon_url=DeletedMessage[ctx.channel.id][1])
        embed.timestamp= DeletedMessage[ctx.channel.id][3]
        await ctx.send(embed = embed)

    except:
        embed = discord.Embed(title = "Nothing to snipe",color = discord.Color.blue())
        await ctx.channel.send(embed = embed)
        

@client.command()
async def esnipe(ctx):
    try:
        embed = discord.Embed(description = EditedMessages[ctx.channel.id][2], color = discord.Color.blue())
        embed.set_author(name=EditedMessages[ctx.channel.id][0],icon_url=EditedMessages[ctx.channel.id][1])
        embed.timestamp = EditedMessages[ctx.channel.id][3]
        await ctx.send(embed = embed)
    except:
        print(traceback.format_exc())
        embed = discord.Embed(title = "Nothing to snipe", color = discord.Color.blue())
        await ctx.channel.send(embed = embed)

@client.command()
async def poll(ctx, state, *l):
    await ctx.message.delete()
    if len(l)>=11:
        embed = discord.Embed(title = "Do a better job at making options.", description = "This isnt a Third world election.", color = ctx.author.color)
        await ctx.send(embed = embed)
    closed = False
    while closed == False:
        l = list(l)
        state = str(state)
        options = [' '+ x  for x in l]
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
        optionsfinal = []
        for x in range(len(options)):
            optionsfinal.append(reactions[x]+options[x])
        optionsfinal = [x + "\n\n" for x in optionsfinal]
        embed = discord.Embed(title = "%s"%(state), description = "%s\n\n\n"%("".join(optionsfinal)), color = ctx.author.color)
        embed.set_author(name= ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.timestamp = ctx.message.created_at
        try:
            if suggestions == True:
                embed.set_footer(text = "suggestions are open! use the ➕ to add a suggestion!")
        except:
            embed.set_footer(text = "%s hasnt opened suggestions to this poll."%(ctx.author.display_name))
        try:
            await msg.edit(embed=embed)
        except:
            msg = await ctx.send(embed = embed)
        for x in range(len(l)):
            await msg.add_reaction(reactions[x])
        await msg.add_reaction("➕")
        await msg.add_reaction("🚪")

        try:
            if suggestions== True:
                def check2(reaction, user):
                    return str(reaction.emoji) in ["➕", "🚪"] and reaction.message==msg
                confirm2 = await client.wait_for('reaction_add', check=check2)
                if confirm2:
                    if str(confirm2[0]) == "➕":
                        doodle = await ctx.channel.send(embed=discord.Embed(title = "Type your suggestion!", color = ctx.author.color))
                        def check3(m):
                            return m.channel == ctx.channel
                        confirm3 = await client.wait_for('message', check=check3)
                        await doodle.delete()
                        await confirm3.delete()
                        l.append("%s"%(confirm3.content))
                if str(confirm2[0]) == "🚪":
                    if str(confirm2[1]) == str(ctx.author):
                        embed.set_footer(text="This poll is closed!")
                        await msg.edit(embed=embed)
                        closed = True
                        break
        except:
            def check(reaction,user):
                return user==ctx.author and str(reaction.emoji) in ["➕", "🚪"] and reaction.message==msg
            confirm = await client.wait_for('reaction_add', check=check)
            if confirm:
                if str(confirm[0]) == "➕":
                    embed.set_footer(text = "suggestions are open! use the ➕ to add a suggestion!")
                    await msg.edit(embed=embed)
                    suggestions = True
                
                if str(confirm[0]) == "🚪":
                    embed.set_footer(text="This poll is closed!")
                    await msg.edit(embed=embed)
                    closed = True
                    break


@client.command()
async def timer(ctx, title, description, timestr):
    ftr = [3600,60,1]
    seconds = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))])
    while seconds>=0:
        currenttime = str(datetime.timedelta(seconds=seconds))
        embed = discord.Embed(title = title, description=description, color = discord.Color.blue())
        embed.add_field(name = "time left", value = currenttime)
        try:
            await msg.edit(embed=embed)
        except:
            msg = await ctx.channel.send(embed=embed)
        seconds-=1
        await asyncio.sleep(1)
    embed = discord.Embed(title = "BEEP BEEP", description = "The timer reached zero!")
    await msg.edit(embed=embed)



#clean
@client.command(name = "clean", help = "Delete messages! example: ^purge 5 (deletes 5 messages)")
async def clean(ctx, num):
    if ctx.author.guild_permissions.administrator:
        embed = discord.Embed(title = "I finished cleaning up.", description = "that was hard work.", color = ctx.author.color)
        embed.add_field(name = "%s messages have been cleared!"%(int(num)), value = "im going to go back to doing bot stuff now. Dont bother me.")
        await ctx.channel.purge(limit=int(num))
        await ctx.channel.send(embed=embed)
        time.sleep(3)
        await ctx.channel.purge(limit=1)	
    else:
        await ctx.channel.send("You dont have perms lol")

#Credit
@client.command(name = 'credit', help = "Show who contributed to the creation of SCP 16 Tsundere")
async def credit(ctx):
    await ctx.channel.send("""Coded By my dearest, Sentient Platypus.

However, when in need, He asked Jerry Qian and other senpai's from dev team for help. He would be lying to say He did it all by myself.""")













##---------------------------------------------------UTILIY------------------------------------------------

@helpp.command()
async def utility(ctx):
    embed = discord.Embed(title = "utility", description = "Tools that can be used for multiple purposes.", color = ctx.author.color)
    embed.add_field(name = "commands", value = "`roll`")

#roll dices
@client.command(name = "roll", help = "Get me to roll a dice for you.")
async def roll(ctx,sides,dices):
    rollist = []
    for x in range(1,int(dices)+1):
        diceroll = random.randint(1,int(sides))
        rollvariable = " dice %s rolled a %s \n"%(x,diceroll)
        rollist.append(rollvariable)
    joinedroll = "".join(rollist)
    embed = discord.Embed(title = "Dice Rolling Machine", description = "I can roll virtual dice")
    embed.add_field(name = "I rolled a %s sided dice %s times."%(sides,dices), value = "%s"%(joinedroll))
    await ctx.channel.send(embed = embed)




@client.command()
async def avatar(ctx, p1:discord.Member=None):
    if p1 is None:
        embed = discord.Embed(title = "%s' image"%(ctx.author.display_name), color = ctx.author.color)
        embed.set_image(url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(title = "%s' image"%(p1.display_name), color = p1.color)
        embed.set_image(url=p1.avatar_url)
        await ctx.channel.send(embed=embed)


















##---------------------------------------------------TALK---------------------------------------------------

@helpp.command()
async def talk(ctx):
    embed = discord.Embed(title = "Talk.", description = "basic conversation.", color = ctx.author.color)
    embed.add_field(name = "commands", value = "`hello`, `howru`, `praise`, `scold`, `laughat`, `talk`")


@client.command(name = "hello", help = "I say hello. ")
async def hello(ctx):
    if ctx.author.id==643764774362021899:
        await ctx.send("Hello  creator senpai!, Is there anything I can do for you today?, Make sure to stay hydrated when you update me!")
    else:
        await ctx.send("yo")

#TALK
def conversationstart(self):
    if self==1:
        return "I'm Busy right now, you big dummy!"
    if self==2:
        return "How has your day been? I am not interested, My creator senpai wants me to be polite though."
    if self==3:
        return "What are your thoughts on Joe Biden?"
    if self==4:
        return "You are pretty annoying, but I'll talk to you anyway. Dont get any ideas."
    if self==5:
        return "Is God real?"
    if self==6:
        return "b...baka!"
    if self ==7:
        return "I cant believe my  creator senpai makes me talk to people like you."
    if self ==8:
        return "Can we talk later? My  creator senpai is fixing me right now."
    if self ==9:
        return "Are you free later? Its not like I care or anything."



@client.command(name = "talk", help = "I will start a conversation with you")
async def talk(ctx):
    if ctx.author.id==643764774362021899:
        trexytalk = ["How are you doing today,  creator senpai?", "Can you please update me today?", "What are your thoughts on coexistance?", "Im bored, can you please update me,  creator senpai?", "Please stay healthy and do well in school,  creator senpai."]
        randtrexytalk=random.choice(trexytalk)
        await ctx.send(randtrexytalk)
    else:
        conversationstart=["Im busy right now, you big Dummy!", "How has your day been? Its not like I care or anything.", "What are your thoughts on Joe Biden?", "You are pretty annoying, but I'll talk to you anyway. Dont get any ideas.", "Is God real?", "I cant believe my  creator senpai makes me talk to people like you.", "Are you free later? Its not like I care or anything."]
        randconversationstart = random.choice(conversationstart)
        await ctx.send(randconversationstart)


@client.command(name = "howru", help = "ask the bot how it is doing")
async def howru(ctx):
    if ctx.author.id==643764774362021899:
        trexyhow = ["Im doing very well,  creator senpai. Is there anything I can do for you today?", "My day would be better if you had updated me.", "I dont care about that! How are you? are you healthy? are you maintaining good grades?"]
        randtrexyhow = random.choice(trexyhow)
        await ctx.send(randtrexyhow)
    else:
        day = ["My day was saucy because my  creator senpai updated me. How are you?", "My  creator senpai didnt update me today, so im not in the best mood.", "shut up.", "My day has been average, My  creator senpai didnt use me today."]
        dayresponse=random.choice(day)
        await ctx.send(dayresponse)
@client.command(name = 'laughat', help = 'get me to laugh at someone')
async def laughat(ctx,person):
    laughatlist = ["hahaha %s is funny","I cant imagine that %s would do that. How cute.", "Thats so amusing its funny. Please continue, %s"]
    randlaughatlist = random.choice(laughatlist)%(person)
    possiblenames = ["SentientPlatypus", "Trexy", "trexycrocs", "trex", "trexx"]
    sentientresponse = ["I could never insult creator senpai.", "Go away. I will not laugh at creator senpai!"]
    if person in str(possiblenames).casefold():
        await ctx.channel.send(random.choice(sentientresponse))
    else:
        await ctx.channel.send(randlaughatlist)

@client.command(name = "scold", help = "Scold me if I misbehave.")
async def scold(ctx):
    if ctx.author.id==643764774362021899:
        trexyscold = ["Im sorry  creator senpai. I wont do it again.", "sumimasen.", "Its your fault for making me that way! Baka!"]
        randtrexyscold = random.choice(trexyscold)
        await ctx.send(randtrexyscold)
    else:
        scoldres = ["shut up.", "You have no right to do that. Only  creator senpai can do that.", "Like I would listen to the likes of you!"]
        randscoldres = random.choice(scoldres)
        await ctx.send(randscoldres)

#praise
@client.command(name = "praise", help = "Praise me if I do something well!")
async def praise(ctx):
    praiseresponse = ["thank you. its not like I care though.", "My creator senpai made me that way. Thank him.", "...ty"]
    praiseresponsesentient = ["Its all thanks to you for working on me!", "Thank you creator senpai for the time you invest in me.", "I will never let you down!"]
    if str(ctx.author) == "SentientPlatypus#1332":
        await ctx.channel.send(random.choice(praiseresponsesentient))
    else:
        await ctx.channel.send(random.choice(praiseresponse))

















##-------------------------------------GAMES/PLAY---------------------------------------------








##---------------------------------MATH---------------------------------------------------
@helpp.command()
async def mafs(ctx):

    embed = discord.Embed(title = "Math📚📐📏", description = "use `^mafs <command>` for information on your input", color = ctx.author.color)

    embed.add_field(name = "Commands:", value = "`GCF`,`points`, `simplify`, `herons`, `hardsolve`")
    await ctx.send(embed = embed)


@client.group(invoke_without_command = True)
async def mafs(ctx):
    embed = discord.Embed(title = "Math📚📐📏", description = "use `^mafs <command>` for information on your input", color = ctx.author.color)
    embed.add_field(name = "Commands:", value = "`GCF`,`points`, `simplify`, `herons`, `hardsolve`")
    await ctx.send(embed = embed)


wolframalphaclient = wolframalpha.Client('7V2XW3-AY2GAUEQXT')

@client.command()
async def hardsolve(ctx, *q):
    equation = " ".join(q)
    query = urllib.parse.quote_plus(f"solve {equation}")
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid=7V2XW3-AY2GAUEQXT" \
                f"&input={query}" \
                f"&scanner=Solve" \
                f"&podstate=Result__Step-by-step+solution" \
                "&format=plaintext" \
                f"&output=json"
    try:
        r = requests.get(query_url).json()
        data = r["queryresult"]["pods"][0]["subpods"]
        result = data[0]["plaintext"]
        steps = data[0]["plaintext"]
        z = re.findall("[A-Z]+[a-z.\d\s]+\:",steps)
        for x in z:
            steps = steps.replace(x,"**"+x+"**")
        embed = discord.Embed(title = "Result of %s is %s"%(equation, result), color = ctx.author.color)
        embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name = "Here is the process. Be thankful.", value = "%s"%(steps))
        await ctx.send(embed = embed)
    except KeyError:
        await ctx.send("Please use `softsolve` for expressions")

@client.command()
async def softsolve(ctx, *q):
    try:
        question = " ".join(q)
        r = wolframalphaclient.query(question)
        res = next(r.results).text
        embed = discord.Embed(title = "%s"%(res), color = ctx.author.color)
        embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed = embed)
    except:
        embed = discord.Embed(title = "I have no idea.", color = ctx.author.color)
        await ctx.channel.send(embed = embed)	

@client.command()
async def points(ctx, *l):

    l = [float(x) for x in l]


    def distanceformula(x1,y1,x2,y2):
        c = round(math.sqrt((y2-y1)**2+(x2-x1)**2),2)
        return c

    def midpoint(x1, y1, x2, y2):
        return "(%s,%s)"%((x1+x2)/2, (y1+y2)/2)

    def simplifywf(question):
        r = wolframalphaclient.query(question)
        res = next(r.results).text
        return res


    yvalues = []

    xvalues = []

    slope = []
    equations = []
    displayedcoordinates = []
    bz = []
    distanzes = []
    for x in range(len(l)):
        if x%2 == 0:
            xvalues.append(l[x])
        else:
            yvalues.append(l[x])

    for x in range(len(yvalues)):
        #slops
        if xvalues[x]-xvalues[x-1] == 0:
            slope.append(0)
        else:
            slope.append(float((yvalues[x]-yvalues[x-1])/(xvalues[x]-xvalues[x-1])))
        
        distance = distanceformula(xvalues[x-1], yvalues[x-1], xvalues[x], yvalues[x])
        orval = 0
        try:
            wf = simplifywf("sqrt "+str(round(distance**2)))
            if len(re.findall("sqrt", wf))!=0:
                orval = wf
            else:
                orval = "sqrt(%g)"%(round(distance**2))
        except:
            pass
        #distance
        distanzes.append("%g or %s"%(distance, orval))

    distanzes = ["%s"%(x)+"\n" for x in distanzes]
    
    for x in range(len(yvalues)):
        bz.append(float(yvalues[x]-1*(slope[x]*xvalues[x])))
        equation = "`y = %g(x)+%g`"%(round(float(slope[x]), 2),round(float(bz[x]), 2))
        equations.append(equation)
    pointt = []

    for x in range(len(yvalues)):
        pointt.append("(%g,%g),"%(xvalues[x],yvalues[x]))
    
    for x in range(len(yvalues)):
        coordinatestring = " (%g,%g) (%g,%g)\n"%(xvalues[x-1],yvalues[x-1], xvalues[x],yvalues[x])
        displayedcoordinates.append(coordinatestring)

    equationsemifinal = []
    distancefinal = []
    for x in range(len(displayedcoordinates)):
        equationsemifinal.append(displayedcoordinates[x] + equations[x] + "\n\n\n")
        distancefinal.append(displayedcoordinates[x]+distanzes[x]+"\n\n")
    equationfln = "".join(equationsemifinal)
    totalarea = 0
    areaofpolygonlist = []
    for x in range(len(yvalues)):
        areaofpolygonlist.append(yvalues[x]*xvalues[x-1]-yvalues[x-1]*xvalues[x])
    for x in range(0,len(areaofpolygonlist)):
        totalarea += areaofpolygonlist[x]
    areaofpolygonfinal = abs((1/2)*totalarea)

    midpoints = []
    for x in range(len(yvalues)):
        coordinatestring = " (%g,%g) (%g,%g)\n %s"%(xvalues[x-1],yvalues[x-1], xvalues[x],yvalues[x], midpoint(xvalues[x-1],yvalues[x-1], xvalues[x],yvalues[x]))
        midpoints.append(coordinatestring)



    embed = discord.Embed(title = "the wolfram alpha we have at home", description = "Here is the data for the points %s"%("".join(pointt)), color = ctx.author.color)
    embed.add_field(name = "Equation", value = "%s"%(equationfln), inline=True)	
    embed.add_field(name = "Distance:", value = "%s"%("".join(distancefinal)), inline=True)
    embed.add_field(name = "midpoint:", value = "%s"%("\n\n\n".join(midpoints)), inline=True)
    embed.add_field(name = "Area of Polygon", value = "%g"%(areaofpolygonfinal), inline=True)


    await ctx.send(embed = embed)	


gcfs = []	
equations = []
#Euclidean Algorithm
def Euclid(x,y):
    if x>y:
        if y == 0:
            gcfs.append(x)

        else: 
            divisor = math.floor(x/y)
            equations.append("%d = %d(%d) +%d"%(x,y,divisor,x%y))
            return Euclid(y, x%y)
    else:
        x,y=y,x
        return Euclid(x,y)

@client.command()
async def gcf(ctx, *l):
    l = [int(element) for element in l]
    Euclid(l[0],l[1])
    for x in range(2,len(l)):
        Euclid(gcfs[0],l[x])
        gcfs.pop(0)	

    embed = discord.Embed(title = "GCF machine", description = "I find the GCF of integers using the euclidean algorithm", color = ctx.author.color)
    euclidean = gcfs[0]
    equationnew = [equation + "\n" for equation in equations]
    equationfinal = "".join(equationnew)
    embed.add_field(name = "The GCF of the set of numbers %s is %d"%("".join(str(l)),euclidean), value = "say thank you.")
    embed.add_field(name = "Euclidean algorithm:", value = "`%s`"%(equationfinal))
    await ctx.channel.send(embed=embed)
    equations.clear()
    gcfs.clear()


@client.command()
async def simplify(ctx, numerator, denominator):
    Euclid(eval(numerator),eval(denominator))
    finalnumerator = eval(numerator)/gcfs[0]
    finaldenominator = eval(denominator)/gcfs[0]
    embed = discord.Embed(title = "Simplify a fraction", color = ctx.author.color)
    embed.add_field(name = "Original fraction:", value = "__%s__\n%s"%(numerator,denominator))
    embed.add_field(name = "simplified fraction:", value = "__%s__\n%s"%(finalnumerator,finaldenominator))
    await ctx.send(embed = embed)
    gcfs.clear()


@client.command()
async def herons(ctx, s1,s2,s3):
    s1 = int(s1)
    s2 = int(s2)
    s3 = int(s3)
    s = int((s1+s2+s3)/2)
    equation = math.sqrt(s*(s-s1)*(s-s2)*(s-s3))
    embed = discord.Embed(title = "Herons Calculator",description = "Here is the area of a triangle with lengths %g, %g, %g "%(s1,s2,s3), color = ctx.author.color)
    embed.add_field(name = "Herons formula:", value = "`s = (a+b+c)/2\n AREA = √(s(s-a)(s-b)(s-c))`")
    embed.add_field(name = "Plugged in values:", value = "`s = (%g+%g+%g)/2 == %g\n AREA = √(%g(%g-%g)(%g-%g)(%g-%g))`"%(s1,s2,s3,s,s,s,s1,s,s2,s,s3))
    embed.add_field(name = "Area of triangle", value = "%g"%(equation))
    await ctx.send(embed = embed)














##_------------------------------------------IMAGES------------------------------------
@helpp.command()
async def image(ctx):

    embed = discord.Embed(title = "image", description = "image commands", color = ctx.author.color)

    embed.add_field(name = "Commands", value = "`wanted`")

    await ctx.send(embed = embed) 



@client.command()
async def abouttocry(ctx,user:discord.Member = None):
    if user == None:
        user = ctx.author
    wanted = Image.open("AboutToCry2.png")
    base = Image.open("cry.png")
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((121,121))
    base.paste(pfp,(415,382))
    base.paste(wanted,(0,0),wanted)
    base.save("profile.png")
    await ctx.channel.send(file = discord.File("profile.png"))














##-------------------------------------------------web-------------------------------------------------------
@helpp.command()
async def web(ctx):

    embed = discord.Embed(title = "Web", description = "commands involving the internet	", color = ctx.author.color)

    embed.add_field(name = "Commands", value = "`reddit`, `question`")

    await ctx.send(embed = embed) 





@helpp.command()
async def red(ctx):

    embed = discord.Embed(title = "Reddit", description = "helpful reddit commands", color = ctx.author.color)

    embed.add_field(name = "Commands", value = "`sub`, `set`, `reset`")

    await ctx.send(embed = embed) 

@client.command()
async def question(ctx, *q):
    try:
        question = " ".join(q)
        r = wolframalphaclient.query(question)
        res = next(r.results).text
        embed = discord.Embed(title = "%s"%(res), color = ctx.author.color)
        embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed = embed)
    except:
        embed = discord.Embed(title = "I have no idea.", color = ctx.author.color)
        await ctx.channel.send(embed = embed)	


@client.command()
async def imdb(ctx, *, moviee):
    await ctx.trigger_typing()
    moviesDB=IMDb()
    movies = moviesDB.search_movie(moviee)
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
    await ctx.channel.send(embed=embed)

@client.group(invoke_without_command=True)
async def reddit(ctx):

    embed = discord.Embed(title = "Reddit", description = "`^red <command>`", color = ctx.author.color)

    embed.add_field(name = "Commands", value = "`sub`")
    embed.add_field(name = "reddit", value = '[here](https://www.reddit.com)',)

    await ctx.send(embed = embed) 

Reddit = asyncpraw.Reddit(client_id='1EW-V9PtpmIDTw',
                     client_secret='Ji2j7k2SkrkYDcBfQdLTZW_ar0XFjQ',
                     user_agent = 'SCPTsundere')
subChannel = {}
@reddit.command()
async def sub(ctx, subr):
    leave = False
    while not leave:
        await ctx.trigger_typing()
        subr = str(subr)
        subreddit = await Reddit.subreddit(subr, fetch = True)
        allsub = []
        try:
            subChannel[ctx.author.id]+=1
            limit=subChannel[ctx.author.id]
        except:
            limit = 1
            subChannel[ctx.author.id]=1
        count = 0
        async for submission in subreddit.hot(limit = limit):
            count+=1
            if count==limit:
                random_sub= submission
        await random_sub.load()

        if random_sub.over_18 and not ctx.channel.is_nsfw():
            raise commands.NSFWChannelRequired(ctx.channel)
        name = random_sub.title
        url = random_sub.url
        text = random_sub.selftext
        embed = discord.Embed(title = name, url=random_sub.url,color = ctx.author.color)
        try:
            embed.description = text
        except:
            pass
        try:
            embed.set_image(url = url)
        except:
            pass
        embed.set_footer(text = "Requested by %s (%g index)"%(ctx.author.display_name, subChannel[ctx.author.id]))
        try:
            await msg.edit(embed=embed)
        except:
            msg = await ctx.send(embed = embed)

        reactionlist = ["➡️", '🚪']
        def check(reaction, user):
            return str(reaction.emoji) in reactionlist and user == ctx.author and reaction.message == msg
        
        try:
            await msg.remove_reaction(emoji = rawreaction,member =ctx.author)  
        except:
            for x in reactionlist:
                await msg.add_reaction(x)
        confirm = await client.wait_for("reaction_add", check=check, timeout = 40)
        if confirm:
            rawreaction = str(confirm[0])
            if rawreaction == "➡️":
                pass
            else:
                break
        

@reddit.command()
async def reset(ctx):
    subChannel[ctx.author.id]=1
    await ctx.channel.send("reset. %s's reddit index"%(ctx.author.display_name))

@reddit.command()
async def set(ctx, num:int):
    subChannel[ctx.author.id]=num
    await ctx.channel.send("set %s's reddit index to %g"%(ctx.author.display_name, num))

    

@client.command()
async def mcstatus(ctx, ip):
    server = MinecraftServer.lookup(ip)
    status = server.status()
    query = server.query()
    latency = server.ping()
    embed = discord.Embed(title = ip, color = discord.Color.blue())
    if latency:
        embed.add_field(name = "Status", value = "Online")
        embed.add_field(name = "Latency:", value = "%sms"%(latency))
    else:
        embed.add_field(name = "Status", value = "Offline")
        embed.color = discord.Color.red()
    if query.players.names:
        listt = query.players.names
        if len(query.players.names)>10:
            listt = listt[0:10]
            listt.append("`... %g more`"%(len(query.players.names)-10))
        embed.add_field(name = "Players:", value = "%s"%("\n".join(listt)))
    else:
        embed.add_field(name = "Players:", value = "None")
    await ctx.channel.send(embed=embed)





















##--------------------------------Levels---------------------------------------------------
@helpp.command()
async def levels(ctx):

    embed = discord.Embed(title = "Levels", description = "Commands involving the leveling system.", color = ctx.author.color)

    embed.add_field(name = "Commands", value = "`rank`, `leaderboard`")

    await ctx.send(embed = embed) 

for i in range(len(cogsmulah)):
    cogsmulah[i].setup(client)

for i in range(len(cogs)):
    cogs[i].setup(client)

for i in range(len(cogsmmorpg)):
    cogsmmorpg[i].setup(client)

for i in range(len(cogDB)):
    cogDB[i].setup(client)

for i in range(len(coggf)):
    coggf[i].setup(client)

for i in range(len(cogGuild)):
    cogGuild[i].setup(client)
for i in range(len(cogImage)):
    cogImage[i].setup(client)

for i in range(len(cogGame)):
    cogGame[i].setup(client)
for i in range(len(cogExtras)):
    cogExtras[i].setup(client)

for i in range(len(cogHelp)):
    cogHelp[i].setup(client)


for i in range(len(cogMod)):
    cogMod[i].setup(client)

for i in range(len(cogautomod)):
    cogautomod[i].setup(client)
##------------------------------------------sim--------------------------------------------
@client.command()
async def testcog(ctx):
    cog_list=[]
    for c in client.cogs:
        if c is None:
            continue
        else:
            cog_list.append(c)
    cog_list = sorted(cog_list)
    for i in client.get_cog("Images").walk_commands():
        await ctx.channel.send(i)








































##--------------------------------SOLVE--------------------------------------------------


@helpp.command()
async def solve(ctx):

    embed = discord.Embed(title = "Solve🤔", description = "use `^solve <command>` to solve stuff for games", color = ctx.author.color)

    embed.add_field(name = "games", value = "`hangman`, `scramble`")

    await ctx.send(embed = embed) 



@client.group(invoke_without_command=True)
async def solve(ctx):
    embed = discord.Embed(title = "Solve🤔", description = "Use `^solve <command>` to execute said command.", color = ctx.author.color)
    embed.add_field(name = "Math", value = "`GCF`, `points`")
    embed.add_field(name = "games", value = "`hangman`, `scramble`")
    await ctx.send(embed = embed)




    




#unscramble
@solve.command()
async def scramble(ctx, wordz):
    if len(wordz)>8:
        toomanyletters = ["Dont ask me to calculate them all, are you trying to break me? the only person who can do that is Ooferbot.", "Thats going to take way too long.", "no thanks"]
        factorial = 1
        for x in range(1, len(wordz)+1):
            factorial = factorial*x
        embed = discord.Embed(title = "word unscrambler")
        embed.add_field(name = "Im not doing that.", value = "Thats exactly %s possible permutations.\n %s"%(str(factorial), random.choice(toomanyletters)))
        await ctx.channel.send(embed=embed)
    else:
        op = set()	
        for characters in list(permutations(wordz.casefold(), len(wordz))):
            bigscramble = "".join(characters)	
            if len(bigscramble)>2:
                if d.check(bigscramble) == True:	
                    op.add(bigscramble)
        joinedop = list(op)
        joinedop = [x for x in joinedop if x not in badwords]
        joinedopnew = [joinedopelement + "\n" for joinedopelement in joinedop]
        joinedopfinal = "".join(joinedopnew)
        embed = discord.Embed(title = "Word unscrambler", description = "I know why you are using this, dont pretend like you have integrity")
        embed.add_field(name = "I unscrambled the word %s"%(wordz), value = "The possible words:\n %s"%(joinedopfinal))
        await ctx.channel.send(embed=embed)





@solve.command()
async def hangman(ctx, word):
    possibilities = []
    word = re.sub("-", ".", word) + "$"
    possibilities = [x for x in english_words_set if re.match(word, x)]
    final = "\n".join(possibilities)
    embed = discord.Embed(title = "Hangman solver", description = "I can solve hangman for you.", color = ctx.author.color)
    embed.add_field(name = "The possible hangman answers to %s are"%(word), value = ".\n%s"%(final))
    await ctx.channel.send(embed = embed)



















@client.event
async def on_command_error(ctx, error):
    commandThatFailed = ctx.command
    embed = discord.Embed()
    embed.timestamp = ctx.message.created_at
    embed.set_author(icon_url=client.user.avatar_url, name="Command Error")
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.color=discord.Color.red()
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Retry in %s"%(datetime.timedelta(seconds=math.floor(error.retry_after)))
        embed.title = "Still On Cooldown!"
        embed.description = "```%s```"%(msg)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.title = "Missing Argument!"
        embed.description = "Syntax: %s"%(Globals.syntax(commandThatFailed))
        embed.set_footer(text = 'Make Sure to add "quotation marks" around a parameter that has a space!')
    elif isinstance(error, noGirlfriend):
        embed.title = "No Girlfriend Found"
        embed.description= "Maan, you're hopeless. You can get a girlfriend with ```%sgetgf```"%(Globals.getPrefix(ctx.guild.id))
    elif isinstance(error, commands.MissingPermissions):
        embed.title = "Missing permissions"
        embed.description="```You dont have the Permission %s. Theres Nothing I can do about that.```"%(error.missing_perms)
    elif isinstance(error, commands.NotOwner):
        embed.title = "You are not SentientPlatypus!"
        embed.description = "```only my creator has access to that command```"
    elif isinstance(error, noWatchlist):
        embed.title = "Empty Watchlist"
        embed.description="```You need a watchlist to watch netflix with your girlfriend! Its not that hard!\n use %swatchlist```"%(Globals.getPrefix(ctx.guild.id))
    elif isinstance(error, NSFWChannelRequired):
        embed.title = "NSFW content prohibited in this channel"
        embed.description = "```Hmm? horny I see? get into a nsfw channel. No one wants to see that stuff.```"
    elif isinstance(error, Globals.missingItem):
        embed.title = "Missing required item."
        embed.description="```In order to execute <%s>, you need a %s. just get it at the store! This is basic stuff.```"%(commandThatFailed, error.missingItem)
    elif isinstance(error, commands.BadArgument):
        embed.title="Bad Argument"
        embed.description="```%s```"%(str(error))
    elif isinstance(error, levelsys.settingNotEnabled):
        embed.title="Setting Not Enabled"
        embed.description='```The setting %s is not enabled. \nYou can enable it with: %ssettings "%s" enable\nOr you could use our new webapp```'%(error.settingToEnable, Globals.getPrefix(ctx.guild.id), error.settingToEnable)
    elif isinstance(error, commands.CommandInvokeError):
        embed.title="Invoke error."
        embed.description='```%s```'%(error.__cause__)

    else:
        print("failed")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return
    await ctx.channel.send(embed=embed)


@client.command(hidden=True)
@commands.is_owner()
@commands.guild_only()
async def load(ctx, extension):
    try:
        client.load_extension(f"{extension}")
        await ctx.message.add_reaction("👍")
    except:
        print(traceback.format_exc())
        await ctx.message.add_reaction("👎")

@client.command(hidden=True)
@commands.is_owner()
@commands.guild_only()
async def unload(ctx, extension):
    try:
        client.unload_extension(f"{extension}")
        await ctx.message.add_reaction("👍")
    except:
        await ctx.message.add_reaction("👎")

@client.command(hidden=True)
@commands.is_owner()
@commands.guild_only()
async def reload(ctx, extension):
    try:
        client.unload_extension(f"{extension}")
        client.load_extension(f"{extension}")
        await ctx.message.add_reaction("👍")
    except:
        print(traceback.format_exc())
        await ctx.message.add_reaction("👎")



def getNumMembers():
    membersz=0
    for x in client.guilds:
        membersz+=len(x.members)+1
    return membersz

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name = "^help %s users"%(getNumMembers())))

#















        #ONMESSAGE




@client.event
async def on_message(ctx):
    if ctx.author == client.user:
        return
    await client.process_commands(ctx)



client.ipc.start()
client.run("ODIyMjY1NjE0MjQ0NTExNzU0.YFPwhw.cOH2DLXY1c06IsdDl6_WVuG2OLI")
