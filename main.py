import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from fastapi import FastAPI

from utils.discord_bot.bot import client, run
import utils.discord_bot.commands

app = FastAPI()
load_dotenv()


async def main():
  task = asyncio.create_task(run(bot=client, token=os.getenv("DISCORD_BOT_TOKEN")))
  msgs = await task
  for msg in msgs.result():
    print (msg.content)
  
asyncio.create_task(main()) 