import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


async def start_bot():
    load_dotenv()
    bot = Bot(token=os.getenv('TG_TOKEN'))


