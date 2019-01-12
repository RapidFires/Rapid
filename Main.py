import discord
from discord.ext import commands
import inspect
import requests, bs4
import youtube_dl
import asyncio
import os
from discord import opus

bot = commands.Bot(command_prefix = ":")
bot.remove_command("help")

players = {}	

@bot.event 
async def on_ready():
	print('Logged in as')
	print("User name:", bot.user.name)
	print("User id:", bot.user.id)
	print('---------------')

@bot.event
async def on_message(message):
  if message.content == ':stop':
      serverid = message.server.id
      players[serverid].stop()
      await bot.send_message(message.channel, "Player stopped")
  if message.content == ':pause':
      serverid = message.server.id
      players[serverid].pause()
      await bot.send_message(message.channel, "Player paused")
  if message.content == ':resume':
      serverid = message.server.id
      players[serverid].resume()
      await bot.send_message(message.channel, "Player resumed")
  if message.content.startswith(':play '):
      author = message.author
      name = message.content.replace(":play ", '')                 
      fullcontent = ('http://www.youtube.com/results?search_query=' + name)
      text = requests.get(fullcontent).text
      soup = bs4.BeautifulSoup(text, 'html.parser')
      img = soup.find_all('img')
      div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
      a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
      title = (a[0]['title'])
      a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
      url = ('http://www.youtube.com'+a0['href'])
      delmsg = await bot.send_message(message.channel, 'Now Playing ** >> ' + title + '**')
      server = message.server
      voice_client = bot.voice_client_in(server)
      player = await voice_client.create_ytdl_player(url)
      players[server.id] = player
      print("User: {} From Server: {} is playing {}".format(author, server, title))
      player.start()
  await bot.process_commands(message)

def user_is_me(ctx):
	return ctx.message.author.id == "277983178914922497", "474257464368431144"
  
@bot.command()
async def ping():
  await bot.say("pong!")

@bot.command(pass_context=True, no_pm=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)
    await bot.say('Connected to voice channel: **[' + str(channel) + ']**')

@bot.command(pass_context=True, no_pm=True)
async def leave(ctx):
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()
    await bot.say("Successfully disconnected from ***[{}]***".format(channel))
  
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
async def mute(ctx, user: discord.Member, *, arg):
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
async def unmute(ctx, user: discord.Member, *, arg):
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
async def kick(ctx, user: discord.Member, *, arg):
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
async def ban(ctx, user: discord.Member, *, arg):
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
	embed.add_field(name=":join", value="make the bot join voice channel")
	embed.add_field(name=":leave", value="make the bot leave the voice channel")
	embed.add_field(name=":play", value="please be careful when using this command it will break if theres music playing.")
	embed.add_field(name=":stop", value="to stop the music from playing")
	embed.add_field(name=":ping", value="test to see the bot is online or not")
	await bot.say(embed=embed)
  
bot.run(os.environ['BOT_TOKEN'])
