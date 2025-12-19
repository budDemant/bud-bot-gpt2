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

from guild_settings_functions import update_guild_channel, is_channel_allowed
def is_allowed_channel():
    async def predicate(ctx):
        return is_channel_allowed(ctx.guild.id, ctx.channel.id)
    return commands.check(predicate)


client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())
gpt_model = DiscordGPT(checkpoint_path='out-discord/ckpt.pt', device='cuda')

@client.event
async def on_ready():
    print("Bud Bot Online")
    print("*********************")
    
@client.command()
async def hello(ctx):
    await ctx.send("This is Bud Bot")
    
@client.command()
async def setchannel(ctx, channel: discord.TextChannel):
    if ctx.author.guild_permissions.administrator:
        update_guild_channel(ctx.guild.id, channel.id)        

@client.event
async def on_message(message):
    contentLower = message.content.lower()
    if "bud" in contentLower:
        await message.channel.send("huh")
    await client.process_commands(message)  
    
@client.command(name='ask')
@is_allowed_channel()
async def ask_gpt(ctx, *, question):
    """Respond to user questions"""
    prompt = f"Q: {question}\nA:" # Add context later?
    
    response = gpt_model.generate(
        prompt, 
        max_new_tokens=100,  # concise
        temperature=0.65 # 1.2 is creative/random, 0.7 is more coherent, but can be repetitive
    )
    
    # Clean up response (stop at newlines for conciseness)
    response = response.split('\n')[0]
    
    await ctx.send(response)
    
@ask_gpt.error
async def ask_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Wrong channel.")
    else:
        raise error
    
client.run(os.environ.get("BOT_KEY"))

