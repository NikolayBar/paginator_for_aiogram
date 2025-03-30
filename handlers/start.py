from aiogram import Router, types
from aiogram.filters import Command
from config.config import config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать! Используйте команду /search для поиска данных."
    )
