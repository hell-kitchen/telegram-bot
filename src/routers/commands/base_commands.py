from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


router = Router(name=__name__)


@router.message(Command('start'))
async def handler_start(message: types.Message):
    keyboard = [
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/help")],
        [KeyboardButton(text="/get_all")],
        [KeyboardButton(text="/search")],
        [KeyboardButton(text="/cancel")],
    ]

    ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.reply(text="Добро пожаловать в HellChickenBot!")


@router.message(Command('help'))
async def handler_help(message: types.Message):
    await message.reply(text="Вот список команд:"
                             "\n/start - запуск бота"
                             "\n/help - вызов справки"
                             "\n/cancel - отменить текущее действие"
                             "\n/search - поиск ингредиентов по названию"
                             "\n/get_all - вывод всех имеющихся ингредиентов"
                             "\n/shoplist - получение ваших списков покупок"
                        )


class Form(StatesGroup):
    first = State()
    q_ingredient = State()


@router.message(Command("cancel"))
async def cancel_cmd(message: types.Message, state: FSMContext):
    current_state = state.set_state()
    if current_state is None:
        return
    await message.reply('Отменено')
    await state.clear()
