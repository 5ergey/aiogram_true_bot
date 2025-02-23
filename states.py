from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    chat = State()
    random = State()
    talk = State()
    dialog_with_star = State()