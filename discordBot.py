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

from model_wrapper import DiscordGPT


client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())
gpt_model = DiscordGPT(checkpoint_path='out-discord/ckpt.pt', device='cuda')

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
    
@client.command(name='ask')
async def ask_gpt(ctx, *, question):
    """Respond to user questions"""
    prompt = f"Q: {question}\nA:" # Add context later?
    
    response = gpt_model.generate(
        prompt, 
        max_new_tokens=100,  # concise
        temperature=0.95 # 1.2 is creative/random, 0.7 is more coherent, but can be repetitive
    )
    
    # Clean up response (stop at newlines for conciseness)
    response = response.split('\n')[0]
    
    await ctx.send(response)
    
client.run(os.environ.get("BOT_KEY"))

