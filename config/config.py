from dotenv import load_dotenv
import os
from aiogram.types import BotCommand

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в .env файле")

    COMMANDS = [
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="search", description="Поиск данных"),
        BotCommand(command="help", description="Помощь")
    ]

config = Config()