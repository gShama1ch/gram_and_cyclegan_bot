import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware

import config_reader

from core.handlers import basic_handlers, comand_handlers, message_handlers
from core.utils.commands import set_commands
from core.utils.admin import admin_id

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(admin_id, 'Бот запущен!')

async def main():
    bot = Bot(token=config_reader.config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(ChatActionMiddleware())
    dp.startup.register(start_bot)
    dp.include_router(comand_handlers.router)
    dp.include_router(message_handlers.router)
    dp.include_router(basic_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())