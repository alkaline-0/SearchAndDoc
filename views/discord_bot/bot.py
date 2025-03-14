import discord
from discord.ext import commands

_intents = discord.Intents.default()
_intents.typing = False
_intents.presences = False
_intents.message_content = True
_intents.members = True

client = commands.Bot(intents=_intents, command_prefix="!")

async def run(bot: any, token: str):
  try:
    await bot.start(token)
  except KeyboardInterrupt:
    await bot.logout()

