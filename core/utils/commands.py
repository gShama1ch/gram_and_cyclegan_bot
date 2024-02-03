from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='menu',
            description='Вернуться в меню'
        ),
        BotCommand(
            command='cancel',
            description='Отменить действие'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())