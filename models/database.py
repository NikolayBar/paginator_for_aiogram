class Database:
    async def get_data(self, query: str) -> list:
        """Заглушка для реальной реализации"""
        return [f"Результат {i} для '{query}'" for i in range(1, 21)]