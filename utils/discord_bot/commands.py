import discord
from discord.ext import commands

from models.channel import Channel
from utils.discord_bot.bot import client as bot


@bot.command(name="document_with_LLM")
async def trigger_search(ctx, channel_name: str, topic: str) -> discord.channel:
  channel = discord.utils.get(ctx.guild.channels, name=channel_name)
  
  if not channel:
    await ctx.channel.send("Channel does not exist.")
    return None
  
  channel_obj = Channel(channel)
  msgs = await channel_obj.get_channel_messages()
  return msgs
