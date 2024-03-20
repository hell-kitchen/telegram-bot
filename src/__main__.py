
import asyncio
import logging
import requests

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from aiogram.enums import ParseMode, ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import config
from api.ingredients import cli


class Form(StatesGroup):
    first = State()
    q_ingredient = State()


dp = Dispatcher()
# BASE_URL = 'https://hellchicken.ru/api'


# response = requests.get(f"{BASE_URL}/ingredients")
# print(response.json())


@dp.message(Command('help'))
async def handler_help(message: types.Message):
    help_text = 'пока беспомощный ботик'
    await message.answer(text=help_text)


@dp.message(Command("get_all"))
async def handle_ingredients(message: types.Message):
    await message.answer("wait...")


@dp.message(Command("search"))
async def handle_search(message: types.Message, state: FSMContext):
    await state.set_state(Form.first)
    await message.answer("Введите название ингредиента")


@dp.message(Form.first)
async def process_first(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.q_ingredient)
    ingredient = cli.get_ingredients(name=message.text)
    await message.answer(f"Найдено {len(ingredient)} ингрединтов с данным названием: {message.text}")

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
    bot = Bot(
        token=config.BOT_TOKEN,
        parse_mode=ParseMode.HTML
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())