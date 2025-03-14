import glob
import os
import pytest_asyncio
import discord
import discord.ext.commands as commands
import discord.ext.test as dpytest
from utils.discord_bot.commands import get_channel_messages


@pytest_asyncio.fixture
async def bot():
    # Setup
  intents = discord.Intents.default()
  intents.members = True
  intents.message_content = True
  bot_test = commands.Bot(command_prefix="!",
                    intents=intents)
  
  @bot_test.command(name="document_with_LLM")
  async def trigger_search(ctx, channel_name: str, topic: str) -> None:
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    
    if not channel:
      await ctx.channel.send("Channel does not exist.")
      return None
  
    msgs = await get_channel_messages(channel)
    for msg in msgs:
      print(msg.content)
    

  await bot_test._async_setup_hook()
  dpytest.configure(client=bot_test, text_channels=["test","general"])

  yield bot_test

  # Teardown
  await dpytest.empty_queue() 

def pytest_sessionfinish(session, exitstatus):
  """ Code to execute after all tests. """

  # dat files are created when using attachements
  print("\n-------------------------\nClean dpytest_*.dat files")
  fileList = glob.glob('./dpytest_*.dat')
  for filePath in fileList:
      try:
          os.remove(filePath)
      except Exception:
          print("Error while deleting file : ", filePath)