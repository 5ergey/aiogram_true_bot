from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, StateFilter
from lexicon.lexicon_ru import LEXICON_RU, PROMPTS_RU
from keyboards import kb_start
from states import Chat
from gpt import gpt_text

user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/start'].replace('name', message.from_user.full_name),
        reply_markup=kb_start()
    )




@user_router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer(
        text=LEXICON_RU['/help'].replace('name', message.from_user.full_name),
        reply_markup=kb_start()
    )


@user_router.message(F.text == 'Диалог с ИИ')
@user_router.message(Command('gpt'))
async def process_gpt_command(message: Message, state: FSMContext):
    await state.set_state(Chat.chat)
    await message.answer(
        text=LEXICON_RU['/gpt'].replace('name', message.from_user.full_name),
        reply_markup=ReplyKeyboardRemove()
    )

@user_router.message(F.text == 'Узнать случайный факт')
@user_router.message(Command('random'))
async def process_random_command(message: Message, state: FSMContext):
    await state.set_state(Chat.random)
    await message.answer(
        text=LEXICON_RU['/random'].replace('name', message.from_user.full_name),
    )
    response = await gpt_text(request='Напиши интересный факт', content=PROMPTS_RU['/random'])
    await message.answer(response)


@user_router.message(Chat.chat)
async def process_chat(message: Message):
    response = await gpt_text(message.text, content="Ты персональный помощник, дающий подробные ответы")
    await message.answer(response)


@user_router.message(Chat.random)
async def process_random(message: Message):
    response = await gpt_text(request=message.text, content=PROMPTS_RU['/random'])
    await message.answer(response)
