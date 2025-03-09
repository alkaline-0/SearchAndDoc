from fastapi import FastAPI
import asyncio
import os
from dotenv import load_dotenv
import utils.discord_bot

app = FastAPI()
load_dotenv()

asyncio.create_task(utils.discord_bot.bot.run(os.getenv("DISCORD_BOT_TOKEN")))
