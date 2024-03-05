# meow meow meow meow meow meow meow meow
# kys? - keep yourself safe
# kiss - keep it simple stupid


import asyncio
import logging
import requests

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command

import config


dp = Dispatcher()
# BASE_URL = 'https://hellchicken.ru/api'


# response = requests.get(f"{BASE_URL}/ingredients")
# print(response.json())


@dp.message(Command('help'))
async def handler_help(message: types.Message):
    help_text = 'пока беспомощный ботик'
    await message.answer(text=help_text)


@dp.message()
async def echo_message(message: types.Message):
    await message.answer(
        text='Думаю как ответить..'
    )
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='чт')


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(config.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())