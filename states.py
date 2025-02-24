from aiogram.fsm.state import State, StatesGroup


class Chat(StatesGroup):
    chat = State()
    random = State()
    talk = State()
    dialog_with_star = State()
    quiz = State()
    user_answer = State()
    next_step_in_quiz = State()