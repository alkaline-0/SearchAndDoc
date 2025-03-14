import glob
import os
from http import client
from pydoc import cli

import discord.ext.commands as commands
import discord.ext.test as dpytest
import pytest_asyncio

from helpers import commands
from views.discord_bot.bot import client


@pytest_asyncio.fixture
async def bot():
    # Setup
    
  await client._async_setup_hook()
  dpytest.configure(client=client, text_channels=["test","general"], members=3)

  yield client

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