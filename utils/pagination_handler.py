from aiogram import Router, types
from aiogram.filters import Filter
from utils.paginator import Paginator, PaginatorAction
from typing import Dict, Tuple


class PaginatorStorage:
    _storage: Dict[Tuple[int, int], Paginator] = {}

    @classmethod
    def add_paginator(cls, chat_id: int, message_id: int, paginator: Paginator):
        cls._storage[(chat_id, message_id)] = paginator

    @classmethod
    def get_paginator(cls, chat_id: int, message_id: int) -> Paginator | None:
        return cls._storage.get((chat_id, message_id))

    @classmethod
    def remove_paginator(cls, chat_id: int, message_id: int):
        cls._storage.pop((chat_id, message_id), None)


class PaginatorCallbackFilter(Filter):
    async def __call__(self, callback: types.CallbackQuery) -> bool:
        return callback.data.startswith("paginator:")


def setup_pagination_handler(router: Router):
    @router.callback_query(PaginatorCallbackFilter())
    async def handle_pagination(callback: types.CallbackQuery):
        paginator = PaginatorStorage.get_paginator(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )

        if not paginator:
            await callback.answer("Время действия истекло")
            return

        action = callback.data.split(":")[1]
        need_update = await paginator.handle_action(action)

        if need_update:
            message_params = await paginator.get_message_params()
            await callback.message.edit_text(**message_params)
        else:
            await callback.message.delete()
            PaginatorStorage.remove_paginator(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id
            )

        await callback.answer()