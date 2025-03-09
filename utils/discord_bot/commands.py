import discord
from utils.discord_bot.bot import client


@client.command(name="document_with_LLM")
async def trigger_search(ctx, channel_name: str, topic: str) -> None:
    await ctx.send(topic)
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    
    if not channel:
        raise await ctx.channel.send("Channel does not exist.")
    
    await get_channel_messages(channel)

    
async def get_channel_messages(channel: any) -> list[discord.Message]:
  messages = []

  async for message in channel.history():
    messages.append(message)

  return messages
