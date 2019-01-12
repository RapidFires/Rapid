import discord
from discord.ext import commands
import asyncio
import os

bot = commands.Bot(command_prefix = ":")

@bot.event
async def on_ready():
  print("Logged in as")
  print("User name:", bot.user.name)
  print("User ID:", bot.user.id)
  
@bot.command()
async def ping():
  await bot.say("pong!")
  
bot.run(os.environ['BOT_TOKEN'])
