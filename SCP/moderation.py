from os import name
import discord
from discord.ext import commands
import datetime

from discord.ext.commands.errors import BadArgument
# This prevents staff members from being punished 
class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
        permission = argument.guild_permissions.manage_messages # can change into any permission
        if not permission: # checks if user has the permission
            return argument # returns user object
        else:
            raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member

# Checks if you have a muted role
class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
        muted = discord.utils.get(ctx.guild.roles, name="Muted") # gets role object
        if muted in argument.roles: # checks if user has muted role
            return argument # returns member object if there is muted role
        else:
            raise commands.BadArgument("The user was not muted.") # self-explainatory
            
# Checks if there is a muted role on the server and creates one if there isn't
async def mute(ctx, user, reason):
    role = discord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't 
    hell = discord.utils.get(ctx.guild.text_channels, name="muted") # retrieves channel named hell returns none if there isn't
    if not role: # checks if there is muted role
        try: # creates muted role 
            muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
            for channel in ctx.guild.channels: # removes permission to view and send in the channels 
                await channel.set_permissions(muted, send_messages=False,
                                              read_message_history=False,
                                              read_messages=False)
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make a muted role") # self-explainatory
        await user.add_roles(muted) # adds newly created muted role
    else:
        await user.add_roles(role) # adds already existing muted role
       
    if not hell: # checks if there is a channel named hell
        try:
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
                        ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                        muted: discord.PermissionOverwrite(read_message_history=True)} # permissions for the channel
        except:
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
                        ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                        role: discord.PermissionOverwrite(read_message_history=True)} # permissions for the channel

        try: # creates the channel and sends a message
            channel = await ctx.guild.create_text_channel('muted', overwrites=overwrites)
            await channel.send("enjoy the silence")
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make #muted")
async def kickmember(ctx, user: Sinner=None, *,reason=None):
    if not user: # checks if there is a user 
        return await ctx.send("You must specify a user")
    
    try: # tries to kick user
        await ctx.guild.kick(user, f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
        embed = discord.Embed(title = "%s has been kicked"%(user.display_name), description = "This action was done by %s"%(ctx.author.mention), color = discord.Color.red())
        embed.add_field(name="Reason:", value = reason or "None specified")
        embed.set_author(icon_url=ctx.author.avatar_url, name= ctx.author.display_name)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"))
        await ctx.channel.send(embed=embed)
    except discord.Forbidden:
        return await ctx.send("Are you trying to kick someone higher than the bot?")
            
class Moderation(commands.Cog):
    """Commands used to moderate your guild"""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def __error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)
            
    @commands.command(aliases=["banish"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Sinner=None, *,reason=None):
        """Casts users out of heaven."""
        
        if not user: # checks if there is a user
            return await ctx.send("You must specify a user")
        
        try: # Tries to ban user
            await user.ban(reason=f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified")
            await user.kick(reason=f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
            embed = discord.Embed(title = "%s has been banned"%(user.display_name), description = "This action was done by %s"%(ctx.author.mention), color = discord.Color.red())
            embed.add_field(name="Reason:", value = reason or "None specified")
            embed.set_author(icon_url=ctx.author.avatar_url, name= ctx.author.display_name)
            embed.set_thumbnail(url=user.avatar_url)
            embed.timestamp = ctx.message.created_at
            embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"))
            await ctx.channel.send(embed=embed)
        except discord.Forbidden:
            return await ctx.send("Are you trying to ban someone higher than the bot")

    @commands.command()
    @commands.has_permissions(administrator=True)

    async def softban(self, ctx, user: Sinner=None, *,reason=None):
        """Temporarily restricts access to heaven."""
        
        if not user: # checks if there is a user
            return await ctx.send("You must specify a user")
        
        try: # Tries to soft-ban user
            await user.ban(reason=f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
            await user.unban(reason="Temporarily Banned")
            await user.kick(reason=f"By {ctx.author} for {reason}" or f"By {ctx.author} for None Specified") 
            embed = discord.Embed(title = "%s has been softbanned"%(user.display_name), description = "This action was done by %s"%(ctx.author.mention), color = discord.Color.red())
            embed.add_field(name="Reason:", value = reason or "None specified")
            embed.set_author(icon_url=ctx.author.avatar_url, name= ctx.author.display_name)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"))
            await ctx.channel.send(embed=embed)
        except discord.Forbidden:
            return await ctx.send("Are you trying to soft-ban someone higher than the bot?")
    
    @commands.command()
    @commands.has_permissions(administrator=True)

    async def mute(self, ctx, user: Sinner,*, reason=None):
        """Gives them hell."""
        await mute(ctx, user, reason or "treason") # uses the mute function
        embed = discord.Embed(title = "%s has been muted"%(user.display_name), description = "This action was done by %s"%(ctx.author.mention), color = discord.Color.red())
        embed.add_field(name="Reason:", value = reason or "None specified")
        embed.set_author(icon_url=ctx.author.avatar_url, name= ctx.author.display_name)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"))
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)

    async def kick(self, ctx, member: discord.Member, *, reason=None):
        embed = discord.Embed(title = "%s has been kicked"%(member.display_name), description = "This action was done by %s"%(ctx.author.mention), color = discord.Color.red())
        embed.add_field(name="Reason:", value = reason or "None specified")
        embed.set_author(icon_url=ctx.author.avatar_url, name= ctx.author.display_name)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"))
        await ctx.channel.send(embed=embed)
        await member.kick(reason=reason)


    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, user: Redeemed):
        """Unmutes a muted user"""
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
        embed = discord.Embed(title = "%s has been unmuted"%(user.display_name), description = "This action was done by %s"%(ctx.author.mention), color = discord.Color.green())
        embed.set_author(icon_url=ctx.author.avatar_url, name= ctx.author.display_name)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"))
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def block(self, ctx, user: Sinner=None):
        """
        Blocks a user from chatting in current channel.
           
        Similar to mute but instead of restricting access
        to all channels it restricts in current channel.
        """
        try:
            if not user: # checks if there is user
                return await ctx.send("You must specify a user")
            embed = discord.Embed(title = "%s has been blocked"%(user.display_name), description = "This action was done by %s"%(ctx.author.mention), color = discord.Color.red())
            embed.set_author(icon_url=ctx.author.avatar_url, name= ctx.author.display_name)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"))
            await ctx.channel.send(embed=embed)                                    
            await ctx.channel.set_permissions(user, send_messages=False) # sets permissions for current channel

        except BadArgument:
            await ctx.channel.send("you cant punish other admins")

    @commands.command()
    @commands.has_permissions(administrator=True)

    async def unblock(self, ctx, user: Sinner=None):
        """Unblocks a user from current channel"""
                                
        if not user: # checks if there is user
            return await ctx.send("You must specify a user")
        
        await ctx.channel.set_permissions(user, send_messages=True) # gives back send messages permissions
        embed = discord.Embed(title = "%s has been unblocked"%(user.display_name), description = "This action was done by %s"%(ctx.author.mention), color = discord.Color.green())
        embed.set_author(icon_url=ctx.author.avatar_url, name= ctx.author.display_name)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d, %H:%M"))
        await ctx.channel.send(embed=embed)
                                
def setup(bot):
    bot.add_cog(Moderation(bot))