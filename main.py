from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.paginator import Paginator, PaginatorAction
import asyncio
from config_data.config import BOT_TOKEN
from logger import logger

# Хранилище пагинаторов (в реальном проекте используйте базу данных)
paginator_storage = {}


class Form(StatesGroup):
    query = State()


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def get_data(query: str) -> list:
    """Пример функции получения данных"""
    return [f"Результат {i} для '{query}'" for i in range(1, 21)]


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Введите запрос для поиска:")


@dp.message(Command("search"))
async def cmd_search(message: types.Message, state: FSMContext):
    await message.answer("Введите запрос для поиска данных:")
    await state.set_state(Form.query)


@dp.message(StateFilter(Form.query))
async def process_query(message: types.Message, state: FSMContext):
    data = await get_data(message.text)
    paginator = Paginator(data)

    # Получаем параметры сообщения от пагинатора
    message_params = await paginator.get_message_params()
    sent_message = await message.answer(**message_params)

    # Сохраняем пагинатор в хранилище
    paginator_storage[(message.chat.id, sent_message.message_id)] = paginator
    await state.clear()


@dp.callback_query(lambda c: c.data.startswith("paginator:"))
async def handle_pagination(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    key = (chat_id, message_id)

    if key not in paginator_storage:
        await callback.answer("Сессия истекла")
        return

    paginator = paginator_storage[key]
    action = callback.data.split(":")[1]

    need_update = await paginator.handle_action(action)

    if need_update:
        message_params = await paginator.get_message_params()
        await callback.message.edit_text(**message_params)
    else:
        await callback.message.delete()
        del paginator_storage[key]

    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Bot started")
    asyncio.run(main())