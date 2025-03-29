from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum, auto
from typing import List, Any, Optional


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
        """
        Инициализация пагинатора
        :param data: данные для пагинации (список)
        :param items_per_page: количество элементов на странице
        :param callback_prefix: префикс для callback данных
        """
        self.data = data
        self.items_per_page = items_per_page
        self.current_page = 0
        self.callback_prefix = callback_prefix

    @property
    def total_pages(self) -> int:
        """Общее количество страниц"""
        return (len(self.data) + self.items_per_page - 1) // self.items_per_page

    def get_page_data(self) -> List[Any]:
        """Получаем данные для текущей страницы"""
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        return self.data[start:end]

    def get_markup(self) -> InlineKeyboardMarkup:
        """Создаем клавиатуру пагинации"""
        markup = InlineKeyboardMarkup()
        row_buttons = []

        # Кнопка "Назад"
        if self.current_page > 0:
            row_buttons.append(
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"{self.callback_prefix}:{PaginatorAction.PREV.name}:{self.current_page}"
                )
            )

        # Кнопка "Закрыть"
        row_buttons.append(
            InlineKeyboardButton(
                text="❌ Закрыть",
                callback_data=f"{self.callback_prefix}:{PaginatorAction.CLOSE.name}:{self.current_page}"
            )
        )

        # Кнопка "Вперед"
        if self.current_page < self.total_pages - 1:
            row_buttons.append(
                InlineKeyboardButton(
                    text="Вперед ➡️",
                    callback_data=f"{self.callback_prefix}:{PaginatorAction.NEXT.name}:{self.current_page}"
                )
            )

        markup.row(*row_buttons)
        return markup

    def format_page(self, page_data: List[Any]) -> str:
        """Форматируем текст сообщения для страницы (можно переопределить)"""
        return "\n".join(str(item) for item in page_data)

    async def get_message_params(self) -> dict:
        """Возвращает параметры для отправки/редактирования сообщения"""
        page_data = self.get_page_data()
        return {
            "text": self.format_page(page_data),
            "reply_markup": self.get_markup()
        }

    async def handle_action(self, action: str) -> bool:
        """
        Обрабатывает действие пагинации
        :param action: действие из callback
        :return: True если нужно обновить сообщение, False если пагинатор закрыт
        """
        if action == PaginatorAction.PREV.name:
            self.current_page -= 1
            return True
        elif action == PaginatorAction.NEXT.name:
            self.current_page += 1
            return True
        elif action == PaginatorAction.CLOSE.name:
            return False
        return True