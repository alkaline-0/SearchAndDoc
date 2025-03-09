from discord.ext import commands
import discord


_intents = discord.Intents.default()
_intents.typing = False
_intents.presences = False
_intents.message_content = True

client = commands.Bot(intents=_intents, command_prefix="!")

async def run(token: str):
  try:
    await client.start(token)
  except KeyboardInterrupt:
    await client.logout()
