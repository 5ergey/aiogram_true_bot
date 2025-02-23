from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from lexicon.lexicon_ru import LEXICON_RU, PROMPTS_RU, TALK_WITH_STAR_RU
from keyboards.keyboards import kb_start, kb_random, kb_talk
from states import Chat
from gpt import gpt_text
from os import path

user_router = Router()
images_dir = path.join(path.dirname(path.abspath(__file__)), 'images')


@user_router.message(F.text == 'Закончить')
@user_router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=LEXICON_RU['/start'].replace('name', message.from_user.full_name),
        reply_markup=kb_start()
    )




@user_router.message(Command('help'))
async def process_help_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=LEXICON_RU['/help'].replace('name', message.from_user.full_name),
        reply_markup=kb_start()
    )


@user_router.message(F.text == 'Диалог с ИИ')
@user_router.message(Command('gpt'))
async def process_gpt_command(message: Message, state: FSMContext):
    await state.set_state(Chat.chat)
    photo_file = FSInputFile(path=path.join(images_dir, 'chat-gpt.jpg'))
    await message.answer_photo(photo=photo_file)
    await message.answer(
        text=LEXICON_RU['/gpt'].replace('name', message.from_user.full_name),
        reply_markup=ReplyKeyboardRemove()
    )

@user_router.message(F.text == 'Узнать случайный факт')
@user_router.message(Command('random'))
async def process_random_command(message: Message, state: FSMContext):
    await state.set_state(Chat.random)
    photo_file = FSInputFile(path=path.join(images_dir, 'fact.jpg'))
    await message.answer_photo(photo=photo_file)
    await message.answer(
        text=LEXICON_RU['/random'].replace('name', message.from_user.full_name),
    )
    response = await gpt_text(request='Напиши интересный факт', content=PROMPTS_RU['/random'])
    await message.answer(response, reply_markup=kb_random())



@user_router.message(F.text == 'Диалог со звездой')
@user_router.message(Command('talk'))
async def process_talk_command(message: Message, state: FSMContext):
    await state.set_state(Chat.talk)
    photo_file = FSInputFile(path=path.join(images_dir, 'star.jpg'))
    await message.answer_photo(photo=photo_file)
    await message.answer(
        text=LEXICON_RU['/talk'].replace('name', message.from_user.full_name),
        reply_markup=kb_talk(1, **TALK_WITH_STAR_RU)
    )


@user_router.message(StateFilter(Chat.chat))
async def process_chat(message: Message):
    response = await gpt_text(message.text, content="Ты персональный помощник, дающий подробные ответы")
    await message.answer(response)

@user_router.message(F.text == 'Хочу ещё факт')
@user_router.message(StateFilter(Chat.random))
async def process_random(message: Message):
    response = await gpt_text(request=message.text, content=PROMPTS_RU['/random'])
    await message.answer(response, reply_markup=kb_random())


@user_router.callback_query(StateFilter(Chat.talk))
async def process_talk(callback: CallbackQuery, state:FSMContext):
    photo_file = FSInputFile(path=path.join(images_dir, f'{callback.data}.jpg'))
    await callback.bot.send_photo(chat_id=callback.from_user.id, photo=photo_file)
    response = await gpt_text(request='Расскажи о себе, и попроси задать к себе вопрос',
                   content=f'Ты - мировая звезда {callback.data}'
                   )
    await state.update_data(star=callback.data)
    await callback.bot.send_message(chat_id=callback.from_user.id, text=response)
    await state.set_state(Chat.dialog_with_star)



@user_router.message(StateFilter(Chat.dialog_with_star))
async def process_dialog(message: Message, state:FSMContext):
    content = await state.get_data()
    #print(content['star'])
    response = await gpt_text(request=message.text, content=f'Ты = мировая звезда {content['star']}')
    await message.answer(response)



