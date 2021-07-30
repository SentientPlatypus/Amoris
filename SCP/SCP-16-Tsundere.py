
from functools import update_wrapper
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
from discord.ext import commands, tasks
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
import DatingSim
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


cogsmulah = [currencysys]
cogs = [levelsys]
cogsmmorpg = [mmorpgGame]
cogDB = [DatabaseHandler]
coggf = [DatingSim]
d = enchant.Dict("en_US")



tagre = "\#\d{4}$"



client = commands.Bot(command_prefix="^", intents =discord.Intents.all(), status=discord.Status.online)
client.remove_command("help")




##---------------------------------------HELP COMMANDS------------------------------------------------------------
@client.group(invoke_without_command=True)
async def help(ctx):
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
	embed.add_field(name = "MMORPG ⚔️", value = "`^help mmorpg`")
	

	await ctx.send(embed = embed)

@help.command()
async def gf(ctx):

	embed = discord.Embed(title = "Gf", description = "for your single ass", color = ctx.author.color)

	embed.add_field(name = "commands:", value = "`^gfstats` `^getgf` `^gfinteract` `^gf gamimng` `^gf movies` `^gf kiss` `^gf hug` `^gf netflix` `^gf boink` `^gf propose`, `^gf date` `^gf talk`")

	await ctx.send(embed = embed) 


@help.command()
async def mmorpg(ctx):
	embed = discord.Embed(title = "The MMORPG", description = "My creator senpai read solo leveling, and is now inspired.", color = ctx.author.color)
	embed.add_field(name = "Setup commands", value = "`begin`")
	await ctx.channel.send(embed=embed)

@help.command()
async def money(ctx):

	embed = discord.Embed(title = "Economy!", description = "make some mulah", color = ctx.author.color)

	embed.add_field(name = "commands:", value = "`^shop` `^buy` `^pc build` `^pc play` `^addram` `^pc stats`, `^work` `^balance`")

	await ctx.send(embed = embed) 

@help.command()
async def yomomma(ctx):

	embed = discord.Embed(title = "Yomomma machine!", description = "get some jokes", color = ctx.author.color)

	embed.add_field(name = "syntax:", value = "`^yomomma`")

	await ctx.send(embed = embed) 
@help.command()
async def wanted(ctx):

	embed = discord.Embed(title = "wanted", description = "wanted image", color = ctx.author.color)

	embed.add_field(name = "syntax:", value = "`^wanted`")

	await ctx.send(embed = embed) 


@help.command()
async def abouttocry(ctx):

	embed = discord.Embed(title = "abouttocry!", description = "komi-saaan", color = ctx.author.color)

	embed.add_field(name = "syntax:", value = "`^abouttocry`")

	await ctx.send(embed = embed) 
@help.command()
async def clean(ctx):

	embed = discord.Embed(title = "clean", description = "Deletes messages", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "^clean <#ofmessages>")

	await ctx.send(embed = embed) 

@help.command()
async def currency(ctx):

	embed = discord.Embed(title = "Economy!", description = "make some mulah", color = ctx.author.color)

	embed.add_field(name = "commands:", value = "`^shop` `^buy` `^pc build` `^pc play` `^addram` `^pc stats`, `^work` `^balance`")

	await ctx.send(embed = embed) 

@help.command()
async def credit(ctx):

	embed = discord.Embed(title = "credit", description = "Shows who contributed to my creation.", color = ctx.author.color)

	await ctx.send(embed = embed) 


@help.command()
async def hello(ctx):

	embed = discord.Embed(title = "hello", description = "Say hello to me!", color = ctx.author.color)
	await ctx.send(embed = embed) 

@help.command()
async def howru(ctx):

	embed = discord.Embed(title = "howru", description = "Ask me how im doing!", color = ctx.author.color)

	await ctx.send(embed = embed) 

@help.command()
async def pp(ctx):

	embed = discord.Embed(title = "pp", description = "get an accurate pp measure", color = ctx.author.color)

	await ctx.send(embed = embed) 

@help.command()
async def rickroll(ctx):
	embed = discord.Embed(title = "Rickroll", description = "rickroll a voice channel", color = ctx.author.color)
	embed.add_field(name = "syntax:", value = "`^rickroll <vcname>` make sure to use the correct capitalization.")
	await ctx.send(embed = embed)

@help.command()
async def voice(ctx):
	embed = discord.Embed(title = "Voice chat 🎵", description = "basic VC commands.", color = ctx.author.color)
	embed.add_field(name = "syntax:", value = "`^p <url> <vcname>`, `^pause`, `^resume`, `^stop`, `^leave`")
	await ctx.send(embed = embed)

@help.command()
async def stats(ctx):

	em = discord.Embed(title = "stats", description = "get an accurate stats report", color = ctx.author.color)

	await ctx.send(embed = em) 

@help.command()
async def roll(ctx):

	embed = discord.Embed(title = "roll", description = "Simulate rolling a dice.", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "^roll <#ofsides> <#ofdie>")

	await ctx.send(embed = embed) 

@help.command()
async def unscramble(ctx):

	embed = discord.Embed(title = "unscramble", description = "unscramble a word", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "^unscramble <word>")

	await ctx.send(embed = embed) 

@help.command()
async def gcf(ctx):

	embed = discord.Embed(title = "GCF", description = "find the GCF of two integers.", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "^gcf <intx> <inty>")

	await ctx.send(embed = embed) 

@help.command()
async def poll(ctx):
	embed = discord.Embed(title = "Polls!", description = "Get the voice of the people with polls. Not like I care though.", color = ctx.author.color)
	embed.add_field(name = "Syntax:", value = '`^poll "<question>" "<option1>" "<option2>" "<option3>"...` (can handle up to ten options)')
	await ctx.send(embed = embed)


@help.command()
async def hangman(ctx):
	embed = discord.Embed(title = "Hangman!", description = "Play a game of hangman.", color = ctx.author.color)
	embed.add_field(name = "Syntax:", value = '`^play hangman` to start playing.\n `^guess hangman <guess>`')
	await ctx.send(embed = embed)




@help.command()
async def points(ctx):

	embed = discord.Embed(title = "Coordinate plane information", description = "Get information regarding inputted points", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^points <x1> <y1> <x2> <y2> .... <xn> <yn>` **place points in the correct order clockwise**")

	await ctx.send(embed = embed) 

@help.command()
async def esnipe(ctx):

	embed = discord.Embed(title = "esnipe", description = "Get messages before they were edited", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^esnipe <#oflatestmessages>`")

	await ctx.send(embed = embed) 

@help.command()
async def snipe(ctx):

	embed = discord.Embed(title = "snipe", description = "Get messages before they were deleted", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^snipe <#oflatestmessages>`")

	await ctx.send(embed = embed) 

@help.command()
async def sub(ctx):

	embed = discord.Embed(title = "sub", description = "get submissions from subreddit", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^red sub <subreddit>`")

	await ctx.send(embed = embed) 

@help.command()
async def simplify(ctx):

	embed = discord.Embed(title = "Simlify", description = "simplify a fraction", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^mafs simplify <numerator> <denominator>`")

	await ctx.send(embed = embed) 

@help.command()
async def rank(ctx):

	embed = discord.Embed(title = "rank", description = "Get your level information", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^rank`")

	await ctx.send(embed = embed) 

@help.command()
async def leaderboard(ctx):

	embed = discord.Embed(title = "Leaderboard", description = "Get leaderboard information", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^leaderboard`")

	await ctx.send(embed = embed) 
@help.command()
async def herons(ctx):

	embed = discord.Embed(title = "Herons", description = "Calculate the area of a triange with its side lengths", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^mafs herons <sidelen1> <sidelen2> <sidelen3>`")

	await ctx.send(embed = embed) 

@help.command()
async def question(ctx):

	embed = discord.Embed(title = "Question", description = "Ask me a question, and I will answer according to my ability.", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^question <question>`")

	await ctx.send(embed = embed) 

@help.command()
async def hardsolve(ctx):

	embed = discord.Embed(title = "Hardsolve", description = "I will solve an equation or expression to the best of my ability.", color = ctx.author.color)

	embed.add_field(name = "**Syntax**", value = "`^mafs hardsolve <equation>`")

	await ctx.send(embed = embed) 


##-------------------------profanitycheck-------------------
badwords = ["fuck", "bitch", "shit", "cunt", "entot", "anjing", "asw", "ngentod", "goblok", "gblk", "wtf", "ngentot"]
def profanitycheck(string):
	if any(word in string for word in badwords):
		return True
	else:
		return False






















##-------------------------------------------FUN-----------------------------------------
@help.command()
async def fun(ctx):

	embed = discord.Embed(title = "FUN😃", description = "fun things to do!", color = ctx.author.color)

	embed.add_field(name = "commands:", value = "`pp`,`roll`,`stats`,`wisdom`, `rickroll`, `yomomma`")

	await ctx.send(embed = embed) 
@help.command()
async def guess(ctx):
	embed = discord.Embed(title = "Guess", description = "Guess something for a game with `^guess <game> <guess>`")
	choose_message = await ctx.send(embed = embed)
	await choose_message.add_reaction("🎮")



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

@client.command(name = "stats", help = "Provides accurate statistics about the author.")
async def stats(ctx):
	attractivenum = int(random.randint(1,100))
	intelligencenum = int(random.randint(1,100))
	simpnum = int(random.randint(1,100))
	epicgamernum = int(random.randint(1,100))
	lifeexpectancynum = int(random.randint(60,100))
	attractiveness = attractivelevel(attractivenum)
	intelligence = intelligencelevel(intelligencenum)
	simpness = simplevel(simpnum)
	epicgamerness = epicgamerlevel(epicgamernum)
	embed=discord.Embed(title = "%s's Stats:"%(re.sub("\#\d{4}$", "", str(ctx.author))), description = "Provides accurate stats about the user", color = ctx.author.color)
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
async def pp(ctx):
	ppnum = random.randint(1,10)
	ppsize = "="*ppnum
	ppfinal = "8%sD" %(ppsize)
	embed = discord.Embed(title = "PP inspection", description = "Accurate PP measure.", color = ctx.author.color)
	embed.add_field(name = "**%s's results**"%(re.sub("\#\d{4}$", "", str(ctx.author))), value = "%s"%(ppfinal) )
	await ctx.channel.send(embed=embed)




















##-------------------------------------------------MODERATION-----------------------------------------------
originalmessage = []
editedmessage = []
editedmessageauthor = []
@client.event
async def on_message_edit(message_before, message_after):
	author = message_before.author
	guild = message_before.guild.name
	channel = message_before.channel
	originalmessage.append(message_before.content)
	editedmessage.append(message_after.content)
	editedmessageauthor.append(message_before.author.display_name)


undeletedmessage = []
undeletedmessageauthor = []
@client.event
async def on_message_delete(message):
	author = message.author
	guild = message.guild.name
	channel = message.channel
	undeletedmessage.append(message.content)
	undeletedmessageauthor.append(message.author.display_name)


@help.command()
async def mod(ctx):
	embed = discord.Embed(title = "Moderation🚨", description = "help moderating text servers.", color = ctx.author.color)
	embed.add_field(name = "Commands", value = "`clean`, `credit`, `poll`, `esnipe`, `snipe`")
	await ctx.send(embed = embed)

@client.command()
async def snipe(ctx,num):
	num = int(num)
	undeletedmessages = []
	undeletedmessageauthors = []
	finallist = []
	if len(undeletedmessage)>=num:
		for x in range(num):
			undeletedmessages.append(undeletedmessage[x])
			undeletedmessageauthors.append(undeletedmessageauthor[x])
		finallist = [x + "\n\n\n" for x in undeletedmessages]
		undeletedmessageauthors = [x+"\n\n\n" for x in undeletedmessageauthors]
		embed = discord.Embed(title = "I see all things", description = "You can not hide from my sight.", color = ctx.author.color)
		embed.add_field(name = "Deleted message:", value = "%s"%("".join(finallist)))
		embed.add_field(name = "author:", value = "%s"%("".join(undeletedmessageauthors)))
		await ctx.send(embed = embed)
	else:
		embed = discord.Embed(title = "there have not been that many deleted messages.", description = "so far, There have only been %s"%(len(originalmessage)), color = ctx.author.color)
		await ctx.channel.send(embed = embed)
		

@client.command()
async def esnipe(ctx, num):
	num = int(num)
	originalmessages = []
	editedmessages = []
	editedmessageauthors = []
	if len(originalmessage)>=num:
		for x in range(num):
			originalmessages.append(originalmessage[x])
			editedmessages.append(editedmessage[x])
			editedmessageauthors.append(editedmessageauthor[x])
		originalmessages = [x + "\n\n\n" for x in originalmessages]
		editedmessages = [x + "\n\n\n" for x in editedmessages]
		editedmessageauthors = [x+"\n\n\n" for x in editedmessageauthors]

		embed = discord.Embed(title = "I see all things.", description = "My creator has granted me the power to see your edited messages.", color = ctx.author.color)
		embed.add_field(name = "original message:", value = "%s"%("".join(originalmessages)))
		embed.add_field(name = "Edited message:", value = "%s"%("".join(editedmessages)))
		embed.add_field(name = "Author:", value = "%s"%("".join(editedmessageauthors)))
		await ctx.channel.send(embed = embed)
	else:
		embed = discord.Embed(title = "there have not been that many edited messages.", description = "There have only been %s so far"%(len(originalmessage)), color = ctx.author.color)
		await ctx.channel.send(embed = embed)

@client.command()
async def poll(ctx, state, *l):
	print(l)
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
					print(confirm2)
					print(str(confirm2[1]))
					if str(confirm2[0]) == "➕":
						doodle = await ctx.channel.send(embed=discord.Embed(title = "Type your suggestion!", color = ctx.author.color))
						def check3(m):
							return m.channel == ctx.channel
						confirm3 = await client.wait_for('message', check=check3)
						await doodle.delete()
						await confirm3.delete()
						l.append("%s"%(confirm3.content))
				if str(confirm2[0]) == "🚪":
					print("no")
					if str(confirm2[1]) == str(ctx.author):
						print("non")
						embed.set_footer(text="This poll is closed!")
						await msg.edit(embed=embed)
						closed = True
						break
		except:
			print(traceback.format_exc())
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




#clean
@client.command(name = "clean", help = "Delete messages! example: ^purge 5 (deletes 5 messages)")
async def clean(ctx, num):
	embed = discord.Embed(title = "I finished cleaning up.", description = "that was hard work.", color = ctx.author.color)
	embed.add_field(name = "%s messages have been cleared!"%(int(num)), value = "im going to go back to doing bot stuff now. Dont bother me.")
	await ctx.channel.purge(limit=int(num))
	await ctx.channel.send(embed=embed)
	time.sleep(3)
	await ctx.channel.purge(limit=1)	

#Credit
@client.command(name = 'credit', help = "Show who contributed to the creation of SCP 16 Tsundere")
async def credit(ctx):
	await ctx.channel.send("""Coded By my dearest, Sentient Platypus.

	However, when in need, He asked Jerry Qian and other senpai's from dev team for help. He would be lying to say He did it all by myself.""")













##---------------------------------------------------UTILIY------------------------------------------------

@help.command()
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

@help.command()
async def talk(ctx):
	embed = discord.Embed(title = "Talk.", description = "basic conversation.", color = ctx.author.color)
	embed.add_field(name = "commands", value = "`hello`, `howru`, `praise`, `scold`, `laughat`, `talk`")


@client.command(name = "hello", help = "I say hello. ")
async def hello(ctx):
	if ctx.author.id==643764774362021899:
		await ctx.send("Hello  creator senpai!, Is there anything I can do for you today?, Make sure to stay hydrated when you update me!")
	else:
		await ctx.send("hello there, i am Sentient's bot. talk to me if you need something from the real me. My  creator senpai is very busy.")

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

@help.command()
async def games(ctx):
	embed = discord.Embed(title = "Games 🎮", description = "Play a game! with `^play`.")
	embed.add_field(name = "commands", value = "`tictactoe`, `hangman`")
	reactions = {
            "🎮"


	}
	choose_message = await ctx.send(embed = embed)
	for emoji in reactions:
		await choose_message.add_reaction(emoji)



@client.group(invoke_without_command = True)
async def play(ctx):
	embed = discord.Embed(title = "Games 🎮", description = "Play a game! with ^play")
	embed.add_field(name = "tictactoe", value = "`tictactoe`, `hangman`")
	choose_message = await ctx.send(embed = embed)
	await choose_message.add_reaction("🎮")
	
#tictactoe

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@play.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
	global count
	global player1
	global player2
	global turn
	global gameOver

	if gameOver:
		global board
		board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
				":white_large_square:", ":white_large_square:", ":white_large_square:",
				":white_large_square:", ":white_large_square:", ":white_large_square:"]
		turn = ""
		gameOver = False
		count = 0

		player1 = p1
		player2 = p2

		# print the board
		line = ""
		for x in range(len(board)):
			if x == 2 or x == 5 or x == 8:
				line += " " + board[x]
				await ctx.send(line)
				line = ""
			else:
				line += " " + board[x]

        # determine who goes first
		num = random.randint(1, 2)
		if num == 1:
			turn = player1
			await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
		elif num == 2:
			turn = player2
			await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
	else:
		await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
	global turn
	global player1
	global player2
	global board
	global count
	global gameOver

	if not gameOver:
		mark = ""
		if turn == ctx.author:
			if turn == player1:
				mark = ":regional_indicator_x:"
			elif turn == player2:
				mark = ":o2:"
			if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
				board[pos - 1] = mark
				count += 1

				# print the board
				line = ""
				for x in range(len(board)):
					if x == 2 or x == 5 or x == 8:
						line += " " + board[x]
						await ctx.send(line)
						line = ""	
					else:
						line += " " + board[x]

				checkWinner(winningConditions, mark)
				print(count)
				if gameOver == True:
					await ctx.send(mark + " wins!")
				elif count >= 9:
					gameOver = True
					await ctx.send("It's a tie. You wasted my time.")

				# switch turns
				if turn == player1:
					turn = player2
				elif turn == player2:
					turn = player1
			else:
				await ctx.send("Be sure to choose an integer between 1 and 9 and an unmarked tile.")
		else:
			await ctx.send("It is not your turn.")
	else:
		await ctx.send("Please start a new game using the !tictactoe command.")

	
def checkWinner(winningConditions, mark):
	global gameOver
	for condition in winningConditions:
		if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
			gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
	print(error)
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Please mention 2 players for this command.")
	elif isinstance(error, commands.BadArgument):
		await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Please enter a position you would like to mark.")
	elif isinstance(error, commands.BadArgument):
		await ctx.send("Please make sure to enter an integer.")

player1connect4 = ""
player2connect4 = ""
turnconnect4 = ""
gameOverconnect4 = True

boardconnect4 = []
@play.command()
async def connect4(ctx, p1:discord.Member, p2:discord.Member):
	global player1connect4
	global player2connect4
	global turnconnect4
	global gameOverconnect4
	global boardconnect4
	if gameOverconnect4:
		boardconnect4 = [":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:",
						":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:",
						":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:",
						":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:",
						":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:",
						":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:",
						":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:"]
		player1connect4 = p1
		player2connect4 = p2
		gameOverconnect4 = False
		turnconnect4 = ""
		line = ""
		for x in range(len(boardconnect4)):
			if x == 6 or x == 13 or x == 20 or x == 27 or x == 34 or x ==41 or x ==48:
				line+= " " + boardconnect4[x]
				await ctx.channel.send(line)
				line = ""
			else:
				line += " " + boardconnect4[x]
        # determine who goes first
		num = random.randint(1, 2)
		if num == 1:
			turnconnect4 = player1connect4
			await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
		elif num == 2:
			turnconnect4 = player2connect4
			await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
	else:
		await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def drop(ctx, column:int):
	global player1connect4
	global player2connect4
	global turnconnect4
	global gameOverconnect4
	global boardconnect4	






@client.group(invoke_without_command = True)
async def guess(ctx):
	embed = discord.Embed(title = "Guess", description = "Guess something for a game with `^guess <game> <guess>`")
	choose_message = await ctx.send(embed = embed)
	await choose_message.add_reaction("🎮")

@client.group(invoke_without_command = True)
async def hint(ctx):
	embed = discord.Embed(title = "hint", description = "get a hint for a game with `^hint <game>`")
	choose_message = await ctx.send(embed = embed)
	await choose_message.add_reaction("🎮")


@play.command()
async def hangman(ctx):
	global r
	r = RandomWords()
	global word
	word = str(r.get_random_word()).lower()
	print(word)
	global listword
	listword = list(word)
	global displayedword
	displayedword = "-"*len(listword)
	global displayedlist
	displayedlist = re.findall("-", displayedword)
	embed = discord.Embed(title = "%s"%(displayedword), description = "use `^guess hangman <guess>` to input a guess. Use `^hint hangman` to get a hint. You only have 3 hints.", color = ctx.author.color)
	await ctx.channel.send(embed = embed)
	global ultguess
	ultguess = False
	global fails
	fails = []
	global guesses
	guesses = []
	global hintcount
	hintcount = 0

def guessresult(guess):
	global ultguess
	global word
	global guesses
	global fails
	global listword
	global displayedlist
	if len(guess) == 1:
		if guess not in guesses:

			for x in range(len(listword)):
				if listword[x]==guess:
					displayedlist[x] = guess
			if len(re.findall(guess,word)) == 0:
				fails.append(guess)
		guesses.append(guess)


	if len(guess) == len(word):
		if guess == word:
			ultguess = True
		else:
			fails.append(guess)
			guesses.append(guess)

@hint.group()
async def hangman(ctx):
	global hintcount
	hintcount +=1
	if hintcount<=3:
		global word
		global listword
		global displayedlist
		for x in range(len(listword)):
			if displayedlist[x] == "-":
				displayedlist[x] = listword[x]
				for y in range(len(listword)):
					if displayedlist[x] == listword[y]:
						displayedlist[y] = listword[y]
				break
		embed = discord.Embed(title = "%s"%("".join(displayedlist)), description = "tough", color = ctx.author.color)
		embed.add_field(name = "guesses:", value = "|%s"%("".join(guesses)))
		embed.add_field(name = "fails:", value = "|%s"%("".join(fails)))
		embed.add_field(name = "hints", value = "%s/3"%(hintcount))
		await ctx.channel.send(embed = embed)
	else:
		embed = discord.Embed(title = "you have no more hints left", color = ctx.author.color)
		await ctx.channel.send(embed = embed)





@guess.command()
async def hangman(ctx, g):
	global ultguess
	global word
	global fails
	global guesses
	global listword
	global displayedlist
	global hintcount
	guessresult(g)
	if ultguess ==True:
		await ctx.send("you win, Leave me alone now.")
		word = str(r.get_random_word())
		ultguess = False
		fails.clear()
		guesses.clear()
		hintcount = 0
	if len(fails)>7 and ultguess == False:
		await ctx.send("you lose. the word was %s"%(word)) 
		word = r.get_random_word()
		ultguess = False
		fails.clear()
		guesses.clear()
		hintcount = 0

	embed = discord.Embed(title = "%s"%("".join(displayedlist)), description = "tough", color = ctx.author.color)
	embed.add_field(name = "guesses:", value = "|%s"%("".join(guesses)))
	embed.add_field(name = "fails:", value = "|%s"%("".join(fails)))
	embed.add_field(name = "hints", value = "%s/3"%(hintcount))
	await ctx.channel.send(embed = embed)

























##---------------------------------MATH---------------------------------------------------
@help.command()
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

@mafs.command()
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

	r = requests.get(query_url).json()

	data = r["queryresult"]["pods"][0]["subpods"]
	result = data[0]["plaintext"]
	steps = data[1]["plaintext"]
	z = re.findall("[A-Z]+[a-z.\d\s]+\:",steps)
	for x in z:
		steps = steps.replace(x,"**"+x+"**")
	print(z)
	embed = discord.Embed(title = "Result of %s is %s"%(equation, result), color = ctx.author.color)
	embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
	embed.add_field(name = "Here is the process. Be thankful.", value = "%s"%(steps))
	await ctx.send(embed = embed)




@mafs.command()
async def points(ctx, *l):

	l = [float(x) for x in l]


	def distanceformula(x1,y1,x2,y2):
		c = round(math.sqrt((y2-y1)**2+(x2-x1)**2),2)
		return c
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
		#distance
		distanzes.append(distanceformula(xvalues[x-1], yvalues[x-1], xvalues[x], yvalues[x]))
	distanzes = ["%g"%(x)+"\n" for x in distanzes]
	print(distanzes)
	for x in range(len(yvalues)):
		bz.append(float(yvalues[x]-1*(slope[x]*xvalues[x])))
		equation = "`y = %g(x)+%g`"%(round(float(slope[x]), 2),round(float(bz[x]), 2))
		equations.append(equation)
	pointt = []
	print(equations)
	for x in range(len(yvalues)):
		pointt.append("(%g,%g),"%(xvalues[x],yvalues[x]))
	
	for x in range(len(yvalues)):
		coordinatestring = " (%g,%g) (%g,%g)\n"%(xvalues[x-1],yvalues[x-1], xvalues[x],yvalues[x])
		displayedcoordinates.append(coordinatestring)
	print(displayedcoordinates)
	equationsemifinal = []
	distancefinal = []
	for x in range(len(displayedcoordinates)):
		equationsemifinal.append(displayedcoordinates[x] + equations[x] + "\n\n")
		distancefinal.append(displayedcoordinates[x]+distanzes[x]+"\n\n")
	equationfln = "".join(equationsemifinal)
	totalarea = 0
	areaofpolygonlist = []
	for x in range(len(yvalues)):
		areaofpolygonlist.append(yvalues[x]*xvalues[x-1]-yvalues[x-1]*xvalues[x])
	for x in range(0,len(areaofpolygonlist)):
		totalarea += areaofpolygonlist[x]
	areaofpolygonfinal = abs((1/2)*totalarea)




	embed = discord.Embed(title = "the wolfram alpha we have at home", description = "Here is the data for the points %s"%("".join(pointt)), color = ctx.author.color)
	embed.add_field(name = "Equation", value = "%s"%(equationfln))	
	embed.add_field(name = "Distance:", value = "%s"%("".join(distancefinal)))
	embed.add_field(name = "Area of Polygon", value = "%g"%(areaofpolygonfinal))


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

@mafs.command()
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


@mafs.command()
async def simplify(ctx, numerator, denominator):
	Euclid(eval(numerator),eval(denominator))
	finalnumerator = eval(numerator)/gcfs[0]
	finaldenominator = eval(denominator)/gcfs[0]
	embed = discord.Embed(title = "Simplify a fraction", color = ctx.author.color)
	embed.add_field(name = "Original fraction:", value = "__%s__\n%s"%(numerator,denominator))
	embed.add_field(name = "simplified fraction:", value = "__%s__\n%s"%(finalnumerator,finaldenominator))
	await ctx.send(embed = embed)
	gcfs.clear()


@mafs.command()
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
@help.command()
async def image(ctx):

	embed = discord.Embed(title = "image", description = "image commands", color = ctx.author.color)

	embed.add_field(name = "Commands", value = "`wanted`")

	await ctx.send(embed = embed) 

@client.command()
async def wanted(ctx,user:discord.Member = None):
	if user == None:
		user = ctx.author
	wanted = Image.open("wantedjpg.jpg")
	asset = user.avatar_url_as(size=128)
	data = BytesIO(await asset.read())
	pfp = Image.open(data)
	pfp = pfp.resize((279,279))
	wanted.paste(pfp,(97,194))
	wanted.save("profile.jpg")
	await ctx.channel.send(file = discord.File("profile.jpg"))

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
@help.command()
async def web(ctx):

	embed = discord.Embed(title = "Web", description = "commands involving the internet	", color = ctx.author.color)

	embed.add_field(name = "Commands", value = "`red`, `facts`, `question`")

	await ctx.send(embed = embed) 


@help.command()
async def fact(ctx):

	embed = discord.Embed(title = "animal facts", description = "`^<command>`", color = ctx.author.color)

	embed.add_field(name = "Commands", value = "`dog`")

	await ctx.send(embed = embed) 


@help.command()
async def red(ctx):

	embed = discord.Embed(title = "Reddit", description = "helpful reddit commands", color = ctx.author.color)

	embed.add_field(name = "Commands", value = "`sub`")

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



@client.group(invoke_without_command=True)
async def red(ctx):

	embed = discord.Embed(title = "Reddit", description = "`^red <command>`", color = ctx.author.color)

	embed.add_field(name = "Commands", value = "`sub`")

	await ctx.send(embed = embed) 

reddit = asyncpraw.Reddit(client_id='1EW-V9PtpmIDTw',
					 client_secret='Ji2j7k2SkrkYDcBfQdLTZW_ar0XFjQ',
					 user_agent = 'SCPTsundere')

@red.command()
async def sub(ctx, subr):
	subr = str(subr)
	subreddit = await reddit.subreddit(subr, fetch = True)
	allsub = []
	async for submission in subreddit.top(limit = 100):
		allsub.append(submission)
	random_sub = random.choice(allsub)
	formats = ["image", "rich:video"]
	while random_sub.post_hint not in formats:
		print(random_sub.post_hint)
		random_sub = random.choice(allsub)
	print(random_sub.post_hint)

	name = random_sub.title
	url = random_sub.url

	embed = discord.Embed(title = name, color = ctx.author.color)
	if random_sub.post_hint == "rich:video":
		embed.video(url=url)
	else:
		embed.set_image(url = url)
	await ctx.send(embed = embed)

@client.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

   embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)

























##--------------------------------Levels---------------------------------------------------
@help.command()
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





##------------------------------------------sim--------------------------------------------









































##--------------------------------SOLVE--------------------------------------------------


@help.command()
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
	if len(re.findall("-", word)) == 0:
		embed = discord.Embed(title = "Hangman solver", description = "I can solve hangman for you.", color = ctx.author.color)
		embed.add_field(name = "Im not doing that.", value = "This should only be used if you have less than 4 -'s left.")
		await ctx.channel.send(embed = embed)	
	d = enchant.Dict("en_US")
	alphabet = list(string.ascii_lowercase)	
	indexes = []
	possibilities = []
	final = []
	strings = list(word)
	for x in range(len(strings)):
		if strings[x] =="-":
			indexes.append(x)
	count = int(word.count("-"))
	perm = [p for p in itertools.product(alphabet, repeat = count)]
	perm = ["".join(element) for element in perm]
	for y in perm:
		for x in range(count):
			strings[indexes[x]] =y[x]
			if d.check("".join(strings)) == True:
				possibilities.append("".join(strings))
	for element in possibilities:
		if element not in final:
			if len(re.findall("-",element)) == 0:
				final.append(element)
	final = [x for x in final if x not in badwords]
	final = [x + "\n" for x in final]
	final = "".join(final)
	embed = discord.Embed(title = "Hangman solver", description = "I can solve hangman for you.", color = ctx.author.color)
	embed.add_field(name = "The possible hangman answers to %s are"%(word), value = ".\n%s"%(final))
	await ctx.channel.send(embed = embed)
























status = cycle(['with Ooferbot', 'Eating ice cream', 'visiting an art museum with Creator Senpai', 'uno with Creator Senpai'])

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game(name = "^help. \nProviding Girlfriends to %s lonely servers"%(len(client.guilds)+1)))

#















		#ONMESSAGE




@client.event
async def on_message(ctx):
	if ctx.author == client.user:
		return
	shutupresponse = ["how about you shut up.", "No, u", "can you shut up? your opinion is worth as much as an old cucumber"]

	shutuplist = ["shutup", "shut up", "stfu", "fuck you", "fuck u", "stupid bot"]
	#FUNNY
	funny = ["lol", "lmao", "haha", "Lol", "Lmao"]
	if any(word in ctx.content.casefold() for word in funny):
		if ctx.author.id==643764774362021899:
			trexyfunny = ["hahaha", "lmao", "lol"]
			randtrexyfunny = random.choice(trexyfunny)
			await ctx.channel.send(randtrexyfunny)
		else:
			funnyresponse = ["lol", "lmao", "haha"]
			randfunny = random.choice(funnyresponse)
			await ctx.channel.send(randfunny)

	#SAD
	sad = ["sad", "depressed", "depression", "unhappy"]
	if any(word in ctx.content for word in sad):
		if ctx.author.id==643764774362021899:
			trexysad = [" creator senpai! dont be sad, Is there anything I can do to cheer you up?", " creator senpai, please feel better.", "NO, You are not allowed to feel that way,  creator senpai."]
			randtrexysad = random.choice(trexysad)
			await ctx.channel.send(randtrexysad)
		else:
			sadresponse = ["cheer up. Its not like I care or anything.", "You need to be happier, My  creator senpai wants people to be happy"]
			randsad = random.choice(sadresponse)
			await ctx.channel.send(randsad)
		def check(m):
			return m.author==ctx.author and m.channel == ctx.channel
		try:
			shutupmessage = await client.wait_for('message', check = check, timeout=5)
		except asyncio.TimeoutError:
			pass
		if any(word in ctx.content.casefold() for word in shutuplist):
			await ctx.channel.send(random.choice(shutupresponse))
			
		else:
			pass


		#WHY
	if ctx.content.startswith("why"):
		if ctx.author.id==643764774362021899:
			trexywhy = ["I will find out asap.", "I will google it for you,  creator senpai", "Someone, answer  creator senpai's question!"]
			randtrexywhy = random.choice(trexywhy)
			await ctx.channel.send(randtrexywhy)
		else:
			whyy = ["Im not sure, Try asking my  creator senpai.", "How would I know? I dont even like talking to you guys, but my  creator senpai wants me to.", "Look it up, baka."]
			randwhyy = random.choice(whyy)
			await ctx.channel.send(randwhyy)
		def check(m):
			return m.author==ctx.author and m.channel == ctx.channel
		try:
			shutupmessage = await client.wait_for('message', check = check, timeout=5)
		except asyncio.TimeoutError:
			pass
		if any(word in ctx.content.casefold() for word in shutuplist):
			await ctx.channel.send(random.choice(shutupresponse))
			
		else:
			pass
			
	#UWU
	if ctx.content.casefold().startswith("uwu"):
		await ctx.channel.send("Shut up.")

	#appreciation

	praiseresponse = ["thank you. its not like I care though.", "My creator senpai made me that way. Thank him.", "...ty"]
	praiseresponsesentient = ["Its all thanks to you for working on me!", "Thank you creator senpai for the time you invest in me.", "I will never let you down!"]
	appreciationtext = "(ily|ty|good\sjob|well\sdone)(sm|\s(so\s)+(much))*\!*\s(bot|scp|tsundere)"
	contecttext = re.findall(appreciationtext, ctx.content.casefold())
	if len(contecttext)>0:
		if str(ctx.author) == "SentientPlatypus#1332":
			await ctx.channel.send(random.choice(praiseresponsesentient))
		else:
			await ctx.channel.send(random.choice(praiseresponse))
	else:
		pass	

	#shut up bot
	shutup = "^(shut\s(the\s[a-zA-Z]+\s)*up|be\squiet|fuck\s(this|you|your)|stfu)\s([a-zA-Z\*]+)*(bot|robot|scp|tsundere|trex(y|ycrocs)*|sen(tient)*(platypus)*|platypus)"
	shutupresponse = ["how about you shut up.", "No, u", "can you shut up? your opinion is worth as much as an old cucumber"]
	shutupre = re.findall(shutup,ctx.content.casefold())
	trexyscold = ["Im sorry  creator senpai. I wont do it again.", "sumimasen.", "Its your fault for making me that way! Baka!"]
	if len(shutupre)>0:
		if ctx.author.id==643764774362021899:
			await ctx.channel.send(random.choice(trexyscold))
		else:
			await ctx.channel.send(random.choice(shutupresponse))
	else:
		pass
	




	await client.process_commands(ctx)




client.run("ODIyMjY1NjE0MjQ0NTExNzU0.YFPwhw.cOH2DLXY1c06IsdDl6_WVuG2OLI")
