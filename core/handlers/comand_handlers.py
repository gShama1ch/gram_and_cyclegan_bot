from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.fsm.context import FSMContext

from core.keyboards import kb
from core.other import text
from core.utils.states import Gen
from gram.basic_style_transfer import delete_image
from core.handlers.basic_handlers import style_name, content_name, image_path

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer(text.greet.format(name=msg.from_user.full_name))
    start_album = MediaGroupBuilder()
    start_album.add_photo(media='AgACAgIAAxkBAAMTZZ52RzFNCLz0SnQK7pHxE7M-ETcAAsbZMRvlquhIOIV_nnlssC8BAAMCAAN4AAM0BA', caption='Фото содержащие стиль')
    start_album.add_photo(media='AgACAgIAAxkBAAMVZZ52T6yZuKPiiUCdZT1MjoF_QakAAsfZMRvlquhIom4p8G-oc2cBAAMCAAN4AAM0BA', caption='Фото которое хочешь изменить')
    start_album.add_photo(media='AgACAgIAAxkBAAMXZZ52VhPKHad-IoR2EsuAw0A5WaYAAkrQMRvoZvBIDW25P8SBAwcBAAMCAAN4AAM0BA', caption='Получившийся результат')
    await msg.answer_media_group(start_album.build())
    await msg.answer(text.menu, reply_markup=kb.menu)
    await state.set_state(Gen.main_menu)
  
@router.message(Command('help'))
async def help_handler(msg: Message, state: FSMContext):
    await msg.answer(text.help, reply_markup=kb.menu)
    await state.set_state(Gen.main_menu)

@router.message(Command('menu'))
async def menu_handler(msg: Message, state: FSMContext):
    await msg.answer(text.menu, reply_markup=kb.menu)
    await state.set_state(Gen.main_menu)

@router.message(Command('cancel'))
async def cancel_handler(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Gen.main_menu:
        await msg.answer('Нет действия для отмены.\nВоспользуйтесь меню', reply_markup=kb.menu)
    elif current_state == Gen.first_image:
        await msg.answer('Вы вернулись в меню', reply_markup=kb.menu)
        delete_image(f'{image_path}\{style_name}.jpg', 'style')
        await state.set_state(Gen.main_menu) 
    elif current_state == Gen.second_image:
        await msg.answer(text.gen_image)  
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        await state.set_state(Gen.first_image)
    elif current_state == Gen.choose_painter:
        await msg.answer('Вы вернулись в меню', reply_markup=kb.menu)
        await state.set_state(Gen.main_menu)