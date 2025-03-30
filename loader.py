from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import config
from handlers import start, search
from utils.pagination_handler import setup_pagination_handler
import logging


async def setup_bot():
    # Используем MemoryStorage для FSM
    storage = MemoryStorage()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=storage)

    # Регистрация роутеров
    dp.include_router(start.router)
    dp.include_router(search.router)

    # Настройка обработчика пагинации
    setup_pagination_handler(dp)

    # Установка команд бота
    await bot.set_my_commands(config.COMMANDS)

    return bot, dp