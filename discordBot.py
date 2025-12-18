# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 21:19:51 2024

@author: bud
"""

import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()
import os


client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bud Bot Online")
    print("*********************")
    
@client.command()
async def hello(ctx):
    await ctx.send("This is Bud Bot")

@client.event
async def on_message(message):
    contentLower = message.content.lower()
    if "bud" in contentLower:
        await message.channel.send("huh")
    await client.process_commands(message)
    
client.run(os.environ.get("BOT_KEY"))

