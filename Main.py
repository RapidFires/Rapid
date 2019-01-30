import discord
from discord.ext import commands
import asyncio
import os
import inspect
import datetime
from discord import opus

bot = commands.Bot(command_prefix = "+")
bot.remove_command("help")

@bot.event 
async def on_ready():
	print('Logged in as')
	print("User name:", bot.user.name)
	print("User id:", bot.user.id)
	print('---------------')

def user_is_me(ctx):
	return ctx.message.author.id == "474257464368431144","277983178914922497"
  
@bot.command()
async def ping():
	await bot.say("pong!")
  
@bot.command(name="clean", pass_context=True, no_pm=True)
@commands.has_permissions(administrator=True)
async def _clean(ctx, amount=100):
	channel = ctx.message.channel
	messages = [ ]
	async for message in bot.logs_from(channel, limit=int(amount) + 1):
		messages.append(message)
	await bot.delete_messages(messages)
	msg = await bot.say(f"{amount} message has been deleted.")
	await asyncio.sleep(5)
	await bot.delete_message(msg)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True, administrator=True)
async def mute(ctx, user: discord.Member, *, arg = None):
	if arg is None:
		await bot.say("please provide a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	role = discord.utils.get(ctx.message.server.roles, name="Muted")
	await bot.add_roles(user, role)
	embed = discord.Embed(title="Mute", description=" ", color=0xFFA500)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True, administrator=True)
async def unmute(ctx, user: discord.Member, *, arg = None):
	if arg is None:
		await bot.say("please provide a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	role = discord.utils.get(ctx.message.server.roles, name="Muted")
	await bot.remove_roles(user, role)
	embed = discord.Embed(title="Unmute", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, arg = None):
	if arg is None:
		await bot.say("please provide a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	await bot.kick(user)
	embed = discord.Embed(title="Kick", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)
  
@bot.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, arg = None):
	if arg is None:
		await bot.say("please provide a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	await bot.ban(user)
	embed = discord.Embed(title="Ban", description=" ", color=0xFF0000)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def warn(ctx, user: discord.Member, *, arg = None):
	if arg is None:
		await bot.say("please provide a reason to {}".format(user.name))
		return False
	reason = arg
	author = ctx.message.author
	server = ctx.message.server
	embed = discord.Embed(title="Warn", description=" ", color=0x00ff00)
	embed.add_field(name="User: ", value="<@{}>".format(user.id), inline=False)
	embed.add_field(name="Moderator: ", value="{}".format(author.mention), inline=False)
	embed.add_field(name="Reason: ", value="{}\n".format(arg), inline=False)
	await bot.say(embed=embed)
	await bot.send_message(user, "You have been warned for: {}".format(reason))
	await bot.send_message(user, "from: {} server".format(server))

@bot.command(pass_context=True)
@commands.has_permissions(kick_members=True, ban_members=True, administrator=True)
async def unban(con,user:int):
	try:
		who=await bot.get_user_info(user)
		await bot.unban(con.message.server,who)
		await bot.say("User has been unbanned")
	except:
		await bot.say("Something went wrong")
	
@bot.command(pass_context=True)
async def info(ctx):
	author = ctx.message.author
	servers = list(bot.servers)
	embed = discord.Embed(description=" ", color=0xFFFF)
	embed.add_field(name="Servers:", value=f"{str(len(servers))}")
	embed.add_field(name="Users:", value=f"{str(len(set(bot.get_all_members())))}")
	embed.add_field(name="Invite", value=f"[Link](https://discordapp.com/api/oauth2/authorize?client_id=533431393342980116&permissions=2146958839&scope=bot)")
	embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/533431393342980116/ba516de0f934181305ed492c5abf780b.png?size=1024")
	embed.set_footer(text=" | {}".format(bot.user.name), icon_url="https://cdn.discordapp.com/avatars/533431393342980116/ba516de0f934181305ed492c5abf780b.png?size=1024")
	await bot.say(embed=embed)

@bot.command(name='eval', pass_context=True)
@commands.check(user_is_me)
async def _eval(ctx, *, command):
	res = eval(command)
	if inspect.isawaitable(res):
		await bot.say(await res)
	else:
		await bot.say(res)
	
@bot.command(pass_context=True, no_pm=True)
async def help(ctx):
	embed = discord.Embed(title="Help section", description=" ", color=0xFFFF)
	embed.add_field(name="+join", value="make the bot join voice channel")
	embed.add_field(name="+leave", value="make the bot leave the voice channel")
	embed.add_field(name="+play", value="please be careful when using this command it will break if theres music playing.")
	embed.add_field(name="+stop", value="to stop the music from playing")
	embed.add_field(name="+warn", value="+warn @user <reason>")
	embed.add_field(name="+mute", value="+mute @user <reason>")
	embed.add_field(name="+unmute", value="+unmute @user <reason>")
	embed.add_field(name="+kick", value="+kick @user <reason>")
	embed.add_field(name="+ban", value="+ban @user <reason>")
	embed.add_field(name="+unban", value="+unban <user id>")
	embed.add_field(name="+clean", value="+clean <amount of messages>")
	embed.add_field(name="+ping", value="test to see the bot is online or not")
	await bot.say(embed=embed)
  
bot.run(os.environ['BOT_TOKEN'])
