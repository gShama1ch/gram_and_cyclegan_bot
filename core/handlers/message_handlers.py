from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.keyboards import kb
from core.other import text
from core.utils.states import Gen


router = Router()


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message, state: FSMContext):
    await msg.answer(text.menu, reply_markup=kb.menu)
    await state.set_state(Gen.main_menu)


@router.message(F.text)
async def trash(msg: Message, state: FSMContext):
    try:
        await msg.answer(text.trash.format(name=msg.from_user.full_name), reply_markup=kb.menu)
        await state.set_state(Gen.main_menu)
    except TypeError:
        await msg.answer(text.trash.format(name=msg.from_user.full_name), reply_markup=kb.menu)
        await state.set_state(Gen.main_menu)

