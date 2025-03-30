from aiogram.fsm.state import State, StatesGroup

class SearchStates(StatesGroup):
    query = State()