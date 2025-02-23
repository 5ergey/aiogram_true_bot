from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


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


def kb_random():
    kb_builder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = [
        KeyboardButton(text='Хочу ещё факт'),
        KeyboardButton(text='Закончить')
    ]
    kb_builder.row(*buttons)
    return kb_builder.as_markup(resize_keyboard=True)


def kb_talk(width: int, **kwargs: dict):
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []
    for button, text in kwargs.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button
        ))


    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True)

