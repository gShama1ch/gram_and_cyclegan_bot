from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from core.keyboards import kb
from core.other import text
from gram.basic_style_transfer import delete_image
from gram import fast_gram_style_transfer
from core.utils.states import Gen

from cyclegan import CycleGAN

router = Router()

style_name = ''
content_name = ''
image_path = '.\core\images'



@router.callback_query(F.data == "help")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.answer(text.help, reply_markup=kb.menu)
    await state.set_state(Gen.main_menu)

@router.callback_query(F.data == "generate_image")
async def input_image_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(text.gen_image)
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
    await state.set_state(Gen.first_image)

@router.message(Gen.first_image)
async def download_style(msg: Message, bot: Bot, state: FSMContext):
    global style_name
    global image_path
    style_name = msg.photo[-1].file_id
    await bot.download(
        msg.photo[-1],
        destination=f"{image_path}\{style_name}.jpg"
    )
    await state.set_state(Gen.second_image)
    await msg.answer(text.gen_image_2)
    await msg.answer(text.gen_exit, reply_markup=kb.exit_kb)

@router.message(Gen.second_image)
async def download_content(msg: Message, bot: Bot, state: FSMContext):
    global content_name
    global image_path
    content_name = msg.photo[-1].file_id
    await bot.download(
        msg.photo[-1],
        destination=f"{image_path}\{content_name}.jpg"
    )
    await msg.answer(text.gen_wait)
    content_image = fast_gram_style_transfer.tensor_load_rgbimage(f'{image_path}\{content_name}.jpg', size=512, keep_asp=True).unsqueeze(0)
    style = fast_gram_style_transfer.tensor_load_rgbimage(f'{image_path}\{style_name}.jpg', size=512).unsqueeze(0)
    style = fast_gram_style_transfer.preprocess_batch(style)

    try:
        style_v =  fast_gram_style_transfer.Variable(style)
        content_image =  fast_gram_style_transfer.Variable(fast_gram_style_transfer.preprocess_batch(content_image))
        fast_gram_style_transfer.style_model.setTarget(style_v)
        output = fast_gram_style_transfer.style_model(content_image)
        fast_gram_style_transfer.tensor_save_bgrimage(output.data[0], f'{image_path}\{content_name}.jpg', False)


        with open(f'{image_path}\{content_name}.jpg', 'rb') as result_image:
            await msg.answer_photo(
                BufferedInputFile(
                    result_image.read(),
                    filename='Generated image.jpg'
                ),
                caption='Получившиеся изображение'
            )
    except Exception:
        await msg.answer(text.gen_error)  
        await msg.answer(text.menu, reply_markup=kb.menu)
        delete_image(f'{image_path}\{style_name}.jpg', 'style')
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        delete_image(f'{image_path}\{content_name}.jpg', 'result')
        await state.set_state(Gen.main_menu)

    
    delete_image(f'{image_path}\{style_name}.jpg', 'style')
    delete_image(f'{image_path}\{content_name}.jpg', 'content')
    delete_image(f'{image_path}\{content_name}.jpg', 'result')
    await state.set_state(Gen.main_menu)

@router.callback_query(F.data == 'ref')
async def help(clbck: CallbackQuery):
    await clbck.message.answer('Спасибо, что хотите поддержать проект, однако реферальная система еще не готова(', reply_markup=kb.menu)

@router.callback_query(F.data == "painters")
async def painter_styles(clbck: CallbackQuery, state: FSMContext):
        await clbck.message.edit_text('Выберите из списка', reply_markup=kb.painters_menu)
        await state.set_state(Gen.choose_painter)

@router.callback_query(F.data == 'monet')
async def await_monet(msg: Message, bot: Bot, state: FSMContext):
    await bot.send_message(msg.from_user.id,text='Отправьте изображение')
    await state.set_state(Gen.monet)

@router.message(Gen.monet)
async def monet_transform(msg: Message, bot: Bot, state: FSMContext):
    weights_path = '.\model_wts\monet_net_G.pth'
    global content_name
    global image_path
    content_name = msg.photo[-1].file_id
    await bot.download(
        msg.photo[-1],
        destination=f"{image_path}\{content_name}.jpg"
    )
    image = f'{image_path}\{content_name}.jpg'
    try:
        CycleGAN.run_gan(weights_path, image)
        with open(f'{image_path}\\result.jpg', 'rb') as result_image:
                await msg.answer_photo(
                    BufferedInputFile(
                        result_image.read(),
                        filename='Generated image.jpg'
                    ),
                    caption='Получившиеся изображение'
                )
        await bot.send_message(msg.chat.id, "Надеюсь, тебе понравилось.\n\n Хочешь попробовать еще раз?", reply_markup=kb.menu)
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        delete_image(f'{image_path}\\result.jpg', 'result')
        await state.set_state(Gen.main_menu)
    except Exception:
        await msg.answer(text.gen_error)  
        await msg.answer(text.menu, reply_markup=kb.menu)
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        await state.set_state(Gen.main_menu)

@router.callback_query(F.data == 'cezanne')
async def await_cezanne(msg: Message, bot: Bot, state: FSMContext):
    await bot.send_message(msg.from_user.id,text='Отправьте изображение')
    await state.set_state(Gen.cezanne)

@router.message(Gen.cezanne)
async def cezanne_transform(msg: Message, bot: Bot, state: FSMContext):
    weights_path = '.\model_wts\cezanne_net_G.pth'
    global content_name
    global image_path
    content_name = msg.photo[-1].file_id
    await bot.download(
        msg.photo[-1],
        destination=f"{image_path}\{content_name}.jpg"
    )
    image = f'{image_path}\{content_name}.jpg'
    try:
        CycleGAN.run_gan(weights_path, image)
        with open(f'{image_path}\\result.jpg', 'rb') as result_image:
                await msg.answer_photo(
                    BufferedInputFile(
                        result_image.read(),
                        filename='Generated image.jpg'
                    ),
                    caption='Получившиеся изображение'
                )
        await bot.send_message(msg.chat.id, "Надеюсь, тебе понравилось.\n\n Хочешь попробовать еще раз?", reply_markup=kb.menu)
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        delete_image(f'{image_path}\\result.jpg', 'result')
        await state.set_state(Gen.main_menu)
    except Exception:
        await msg.answer(text.gen_error)  
        await msg.answer(text.menu, reply_markup=kb.menu)
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        await state.set_state(Gen.main_menu)  

@router.callback_query(F.data == 'ukiyoe')
async def await_ukiyoe(msg: Message, bot: Bot, state: FSMContext):
    await bot.send_message(msg.from_user.id,text='Отправьте изображение')
    await state.set_state(Gen.ukiyoe)

@router.message(Gen.ukiyoe)
async def ukiyoe_transform(msg: Message, bot: Bot, state: FSMContext):
    weights_path = '.\model_wts\\ukiyoe_net_G.pth'
    global content_name
    global image_path
    content_name = msg.photo[-1].file_id
    await bot.download(
        msg.photo[-1],
        destination=f"{image_path}\{content_name}.jpg"
    )
    image = f'{image_path}\{content_name}.jpg'
    try:
        CycleGAN.run_gan(weights_path, image)
        with open(f'{image_path}\\result.jpg', 'rb') as result_image:
                await msg.answer_photo(
                    BufferedInputFile(
                        result_image.read(),
                        filename='Generated image.jpg'
                    ),
                    caption='Получившиеся изображение'
                )
        await bot.send_message(msg.chat.id, "Надеюсь, тебе понравилось.\n\n Хочешь попробовать еще раз?", reply_markup=kb.menu)
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        delete_image(f'{image_path}\\result.jpg', 'result')
        await state.set_state(Gen.main_menu)
    except Exception:
        await msg.answer(text.gen_error)  
        await msg.answer(text.menu, reply_markup=kb.menu)
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        await state.set_state(Gen.main_menu)

@router.callback_query(F.data == 'vangogh')
async def await_vangogh(msg: Message, bot: Bot, state: FSMContext):
    await bot.send_message(msg.from_user.id,text='Отправьте изображение')
    await state.set_state(Gen.vangogh)

@router.message(Gen.vangogh)
async def vangogh_transform(msg: Message, bot: Bot, state: FSMContext):
    weights_path = '.\model_wts\\vangogh_net_G.pth'
    global content_name
    global image_path
    content_name = msg.photo[-1].file_id
    await bot.download(
        msg.photo[-1],
        destination=f"{image_path}\{content_name}.jpg"
    )
    image = f'{image_path}\{content_name}.jpg'
    try:
        CycleGAN.run_gan(weights_path, image)
        with open(f'{image_path}\\result.jpg', 'rb') as result_image:
                await msg.answer_photo(
                    BufferedInputFile(
                        result_image.read(),
                        filename='Generated image.jpg'
                    ),
                    caption='Получившиеся изображение'
                )
        await bot.send_message(msg.chat.id, "Надеюсь, тебе понравилось.\n\n Хочешь попробовать еще раз?", reply_markup=kb.menu)
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        delete_image(f'{image_path}\\result.jpg', 'result')
        await state.set_state(Gen.main_menu)
    except Exception:
        await msg.answer(text.gen_error)  
        await msg.answer(text.menu, reply_markup=kb.menu)
        delete_image(f'{image_path}\{content_name}.jpg', 'content')
        await state.set_state(Gen.main_menu) 