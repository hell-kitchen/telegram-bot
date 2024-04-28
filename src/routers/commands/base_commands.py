from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


rt = Router(name=__name__)


@rt.message(Command('start'))
async def handler_start(message: types.Message):
    kb = [
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/help")],
        [KeyboardButton(text="/get_all")],
        [KeyboardButton(text="/search")],
        [KeyboardButton(text="/cancel")],

    ]
    rkb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(text="Добро пожаловать в HellChickenBot!")


@rt.message(Command('help'))
async def handler_help(message: types.Message):
    await message.reply(text=f"Вот список команд:"
                             f"\n/start - запуск бота"
                             f"\n/help - вызов справки"
                             f"\n/cancel - отменить текущее действие"
                             f"\n/search - поиск ингредиентов по названию"
                             f"\n/get_all - вывод всех имеющихся ингредиентов"
                        )


class Form(StatesGroup):
    first = State()
    q_ingredient = State()


@rt.message(Command("cancel"))
async def cancel_cmd(message: types.Message, state: FSMContext):
    current_state = state.set_state()
    if current_state is None:
        return
    await message.reply('Отменено')
    await state.clear()
