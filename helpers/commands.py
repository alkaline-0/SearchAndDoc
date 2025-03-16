import discord
from discord.ext import commands

from models.channel import Channel
from views.discord_bot.bot import client as bot


@bot.command(name="document_with_LLM")
async def trigger_search(ctx, channel_name: str, topic: str) -> any:
  channel = discord.utils.get(ctx.guild.channels, name=channel_name)
  
  if not channel:
    await ctx.channel.send("Channel does not exist.")
    return None
  
  channel_obj = Channel(channel)
  messages = await channel_obj.get_channel_messages()
  
  
  


 