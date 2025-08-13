import os
import asyncio
import logging

from app.bot_instance import bot
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv
from app.database.models import async_main


load_dotenv()

TOKEN = os.getenv("TOKEN")

async def main():
    await async_main()
    logging.basicConfig(level=logging.INFO)
    logging.info("Бот запускается...")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())