from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def kb_start():
    kb_builder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = [
        KeyboardButton(text='Узнать случайный факт'),
        KeyboardButton(text='Диалог с ИИ'),
        KeyboardButton(text='Диалог со звездой'),
        KeyboardButton(text='Поиграть в квиз'),
        KeyboardButton(text='Перевести текст'),

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


def kb_talk(width: int, **kwargs):
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []
    for button, text in kwargs.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button
        ))


    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True)


def kb_dialog_with_star():
    kb_builder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = [
        KeyboardButton(text='Закончить')
    ]

    kb_builder.row(*buttons)
    return kb_builder.as_markup(resize_keyboard=True)

def kb_quiz_themes(width: int):
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text='Программирование', callback_data='quiz_prog'),
        InlineKeyboardButton(text='Математика', callback_data='quiz_math'),
        InlineKeyboardButton(text='Биология', callback_data='quiz_biology'),
        InlineKeyboardButton(text='Назад', callback_data='start'),
    ]

    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup(resize_keyboard=True)



def kb_quiz_game():
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(text='Задать новый вопрос\n на эту же тему', callback_data='quiz_more'),
        InlineKeyboardButton(text='Сменить тему', callback_data='quiz'),
        InlineKeyboardButton(text='Закончить квиз', callback_data='start'),
    ]
    kb_builder.row(*buttons)
    kb_builder.adjust(2, 1)
    return kb_builder.as_markup(resize_keyboard=True)


def kb_translate(*args):
    kb_builder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = []
    for button in args:
        buttons.append(KeyboardButton(text=button))

    kb_builder.row(*buttons)
    kb_builder.adjust(2, 2, 2)
    return kb_builder.as_markup(resize_keyboard = True)


def kb_translate_menu():
    kb_builder = ReplyKeyboardBuilder()

    buttons: list[KeyboardButton] = [
        KeyboardButton(text='Сменить язык'),
        KeyboardButton(text='Закончить')
    ]
    kb_builder.row(*buttons)
    return kb_builder.as_markup(resize_keyboard=True)