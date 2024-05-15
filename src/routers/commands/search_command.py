from aiogram import Router, types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.api.ingredients import cli
from src.routers.commands.base_commands import Form

router = Router(name=__name__)


@router.message(Command("search"))
async def handle_search(message: types.Message, state: FSMContext):
    await state.set_state(Form.first)
    await message.answer("Введите название ингредиента")


@router.message(Form.first)
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
