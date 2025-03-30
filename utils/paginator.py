from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum, auto
from typing import List, Any


class PaginatorAction(Enum):
    PREV = auto()
    NEXT = auto()
    CLOSE = auto()


class Paginator:
    def __init__(
            self,
            data: List[Any],
            items_per_page: int = 5,
            callback_prefix: str = "paginator"
    ):
        self.data = data
        self.items_per_page = items_per_page
        self.current_page = 0
        self.callback_prefix = callback_prefix

    @property
    def total_pages(self) -> int:
        return (len(self.data) + self.items_per_page - 1) // self.items_per_page

    def get_page_data(self) -> List[Any]:
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        return self.data[start:end]

    def get_markup(self) -> InlineKeyboardMarkup:
        # Создаем список рядов кнопок
        keyboard = []
        row_buttons = []

        if self.current_page > 0:
            row_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"{self.callback_prefix}:{PaginatorAction.PREV.name}:{self.current_page}"
                )
            )

        row_buttons.append(
            InlineKeyboardButton(
                text="❌ Закрыть",
                callback_data=f"{self.callback_prefix}:{PaginatorAction.CLOSE.name}:{self.current_page}"
            )
        )

        if self.current_page < self.total_pages - 1:
            row_buttons.append(
                InlineKeyboardButton(
                    text="Вперед ➡️",
                    callback_data=f"{self.callback_prefix}:{PaginatorAction.NEXT.name}:{self.current_page}"
                )
            )

        # Добавляем ряд кнопок в клавиатуру
        keyboard.append(row_buttons)

        # Создаем клавиатуру с явным указанием inline_keyboard
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def format_page(self, page_data: List[Any]) -> str:
        return "\n".join(str(item) for item in page_data)

    async def get_message_params(self) -> dict:
        page_data = self.get_page_data()
        return {
            "text": self.format_page(page_data),
            "reply_markup": self.get_markup()
        }

    async def handle_action(self, action: str) -> bool:
        if action == PaginatorAction.PREV.name:
            self.current_page -= 1
            return True
        elif action == PaginatorAction.NEXT.name:
            self.current_page += 1
            return True
        elif action == PaginatorAction.CLOSE.name:
            return False
        return True