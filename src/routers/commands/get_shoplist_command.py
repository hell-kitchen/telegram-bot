from aiogram import Router, types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.routers.commands.base_commands import Form

router = Router(name=__name__)


@router.message(Command("shoplist"))
async def handle_command(message: types.Message, state: FSMContext):
    await state.set_state(Form.first)
    await message.answer("Введите ваш email")
