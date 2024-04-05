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

# response = requests4.get(f"{BASE_URL}/ingredients")
# print(response.json())


dic = {}
a = cli.get_ingredients()
alist = [x.name for x in a]
split_alist = [alist[i: i+20] for i in range(0, len(alist), 20)]


async def ikb_updated(text: str):
    keyboard = [
        [InlineKeyboardButton(text="<", callback_data="previous"),
         InlineKeyboardButton(text=f"{text}/109", callback_data="page"),
         InlineKeyboardButton(text=">", callback_data="next")]
    ]
    ikb = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return ikb


@dp.message(Command('help'))
async def handler_help(message: types.Message):
    help_text = 'пока беспомощный ботик'
    await message.answer(text=help_text)


@dp.message(Command("get_all"))
async def handle_ingredients(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    dic[id_user] = 0
    await message.answer(f"- {'\n- '.join(split_alist[dic[id_user]])}",
                         reply_markup=await ikb_updated(text=f"{dic[id_user]}"))


@dp.callback_query(F.data == 'next')
async def callback_next(callback_query: CallbackQuery):
    id_user = callback_query.from_user.id
    if dic[id_user] == 109:
        await callback_query.message.edit_text(f"- {'\n- '.join(split_alist[0])}",
                                               reply_markup=await ikb_updated(text=f"0"))
        dic[id_user] = 0
    else:
        await callback_query.message.edit_text(f"- {'\n- '.join(split_alist[dic[id_user] + 1])}",
                                               reply_markup=await ikb_updated(text=f"{dic[id_user] + 1}"))
        dic[id_user] += 1
    await callback_query.answer()


@dp.callback_query(F.data == 'page')
async def callback_page(callback_query: CallbackQuery):
    await callback_query.answer(text="Текущая страница")


@dp.callback_query(F.data == 'previous')
async def callback_previous(callback_query: CallbackQuery):
    id_user = callback_query.from_user.id
    if dic[id_user] == 0:
        await callback_query.message.edit_text(f"- {'\n- '.join(split_alist[109])}",
                                               reply_markup=await ikb_updated(text=f"109"))
        dic[id_user] = 109
        print(dic)
    else:
        await callback_query.message.edit_text(f"- {'\n- '.join(split_alist[dic[id_user] - 1])}",
                                               reply_markup=await ikb_updated(text=f"{dic[id_user] - 1}"))
        dic[id_user] -= 1
        print(dic)
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