from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from src.api import ingredients_client

router = Router(name=__name__)
dic = {}
a = ingredients_client.get_ingredients()
alist = [x.name for x in a]
split_alist = [alist[i: i+20] for i in range(0, len(alist), 20)]


async def ikb_updated(text: str):
    keyboard = [
        [InlineKeyboardButton(text="<", callback_data="previous"),
         InlineKeyboardButton(text=f"{text}/109", callback_data="page"),
         InlineKeyboardButton(text=">", callback_data="next"),
         ]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return inline_keyboard


@router.message(Command("get_all"))
async def handle_ingredients(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    dic[id_user] = 0
    await message.answer(
        f"- {'\n- '.join(split_alist[dic[id_user]])}",
        reply_markup=await ikb_updated(text=f"{dic[id_user]}"),
    )


@router.callback_query(F.data == 'next')
async def callback_next(callback_query: CallbackQuery):
    id_user = callback_query.from_user.id
    if dic[id_user] == 109:
        await callback_query.message.edit_text(
            f"- {'\n- '.join(split_alist[0])}",
            reply_markup=await ikb_updated(text=f"0"),
        )
        dic[id_user] = 0
    else:
        await callback_query.message.edit_text(
            f"- {'\n- '.join(split_alist[dic[id_user] + 1])}",
            reply_markup=await ikb_updated(text=f"{dic[id_user] + 1}"),
        )
        dic[id_user] += 1
    await callback_query.answer()


@router.callback_query(F.data == 'page')
async def callback_page(callback_query: CallbackQuery):
    await callback_query.answer(text="Текущая страница")


@router.callback_query(F.data == 'previous')
async def callback_previous(callback_query: CallbackQuery):
    id_user = callback_query.from_user.id
    if dic[id_user] == 0:
        await callback_query.message.edit_text(
            f"- {'\n- '.join(split_alist[109])}",
            reply_markup=await ikb_updated(text=f"109"),
        )
        dic[id_user] = 109
        print(dic)
    else:
        await callback_query.message.edit_text(
            f"- {'\n- '.join(split_alist[dic[id_user] - 1])}",
            reply_markup=await ikb_updated(text=f"{dic[id_user] - 1}"),
        )
        dic[id_user] -= 1
        print(dic)
    await callback_query.answer()
