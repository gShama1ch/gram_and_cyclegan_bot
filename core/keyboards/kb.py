from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="🖼 Стилизировать изображения", callback_data="generate_image")],
    [InlineKeyboardButton(text="🖼 Предустановленные стили", callback_data="painters")],
    [InlineKeyboardButton(text="💎 Поддержать разработчика", callback_data="ref")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]

painters_menu = [
    [InlineKeyboardButton(text="Мане", callback_data="monet"), InlineKeyboardButton(text="Сезанн", callback_data="cezanne")],
    [InlineKeyboardButton(text="Вангог", callback_data="vangogh"), InlineKeyboardButton(text="Укиё-э", callback_data="ukiyoe")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
painters_menu = InlineKeyboardMarkup(inline_keyboard=painters_menu)