from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states.search_states import SearchStates
from models.database import Database
from utils.paginator import Paginator
from utils.pagination_handler import PaginatorStorage
from config.config import config

router = Router()
db = Database()


@router.message(Command("search"))
async def cmd_search(message: types.Message, state: FSMContext):
    await message.answer("Введите запрос для поиска данных:")
    await state.set_state(SearchStates.query)


@router.message(StateFilter(SearchStates.query))
async def process_query(message: types.Message, state: FSMContext):
    data = await db.get_data(message.text)
    paginator = Paginator(data)

    message_params = await paginator.get_message_params()
    sent_message = await message.answer(**message_params)

    PaginatorStorage.add_paginator(
        chat_id=message.chat.id,
        message_id=sent_message.message_id,
        paginator=paginator
    )
    await state.clear()