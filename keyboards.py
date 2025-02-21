from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def kb_start():
    kb_builder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = [
        KeyboardButton(text='Узнать случайный факт'),
        KeyboardButton(text='Диалог с ИИ'),
        KeyboardButton(text='Диалог со звездой'),
        KeyboardButton(text='Поиграть в квиз'),

    ]
    kb_builder.row(*buttons)
    kb_builder.adjust(2, 2)
    return kb_builder.as_markup(resize_keyboard = True)


