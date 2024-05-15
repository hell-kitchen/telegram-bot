import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher

import config
from routers import rt as main_router

dp = Dispatcher()
dp.include_router(main_router)


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=config.BOT_TOKEN,
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
