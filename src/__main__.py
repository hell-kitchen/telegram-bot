import asyncio
import logging
import requests

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

import config
from api.ingredients import cli


class Form(StatesGroup):
    first = State()
    q_ingredient = State()


dp = Dispatcher()
# BASE_URL = 'https://hellchicken.ru/api'

# response = requests.get(f"{BASE_URL}/ingredients")
# print(response.json())


keyboard = [
    [InlineKeyboardButton(text="<", callback_data="previous"),
     InlineKeyboardButton(text="0/100", callback_data="pages"),
     InlineKeyboardButton(text=">", callback_data="next")]
]
ikb = InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(Command('help'))
async def handler_help(message: types.Message):
    help_text = 'пока беспомощный ботик'
    await message.answer(text=help_text)


@dp.message(Command("get_all"))
async def handle_ingredients(message: types.Message, state: FSMContext):
    await message.answer(f"тип список",
                         reply_markup=ikb)


@dp.callback_query(F.data == 'previous')
async def callback_previous(callback_query: CallbackQuery):
    await callback_query.message.edit_text("предыдущая страница",
                                           reply_markup=ikb)
    await callback_query.answer()


@dp.callback_query(F.data == 'next')
async def callback_next(callback_query: CallbackQuery):
    await callback_query.message.edit_text("следующая страница",
                                           reply_markup=ikb)
    await callback_query.answer()


@dp.message(Command("cancel"))
async def cancel_cmd(message: types.Message, state: FSMContext):
    current_state = state.set_state()
    if current_state is None:
        return
    await message.reply('Отменено')
    await state.clear()


@dp.message(Command("search"))
async def handle_search(message: types.Message, state: FSMContext):
    await state.set_state(Form.first)
    await message.answer("Введите название ингредиента")


@dp.message(Form.first)
async def process_first(message: types.Message, state: FSMContext):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await state.update_data(name=message.text)
    await state.set_state(Form.q_ingredient)
    ingredient = cli.get_ingredients(name=message.text)
    ingredient_list = [x.name for x in ingredient]
    await message.answer(f"Найдено {len(ingredient)} ингрединтов с данным названием <{message.text}>:\n-{'\n-'.join(ingredient_list)}")
    await state.set_state(Form.first)


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
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())