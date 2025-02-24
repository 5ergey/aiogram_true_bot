from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from lexicon.lexicon_ru import LEXICON_RU, PROMPTS_RU, TALK_WITH_STAR_RU, STARS, QUIZ, TRANSLATE, LANGUAGES
from keyboards.keyboards import kb_start, kb_random, kb_talk, kb_dialog_with_star, kb_quiz_themes, kb_quiz_game, \
    kb_translate, kb_translate_menu
from states import Chat
from gpt import gpt_text
from os import path

user_router = Router()
images_dir = path.join(path.dirname(path.abspath(__file__)), 'images')


# ------------------------------------------------
# Базовые обработчики /start и /help

# Обработка команды /start
@user_router.callback_query(F.data == 'start', ~StateFilter(default_state))
@user_router.message(F.text == 'Закончить')
@user_router.message(CommandStart())
async def process_start_command(message: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if isinstance(message, Message):
        await message.answer(
            text=LEXICON_RU['/start'].replace('name', message.from_user.full_name),
            reply_markup=kb_start()
        )
    else:
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=LEXICON_RU['/start'].replace('name', message.from_user.full_name),
            reply_markup=kb_start()
        )


# Обработка команды help
@user_router.message(Command('help'))
async def process_help_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=LEXICON_RU['/help'].replace('name', message.from_user.full_name),
        reply_markup=kb_start()
    )


# ------------------------------------------------
# Обработчики чата с gpt

# Обработка команды /gpt, установка состояния chat
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


# Обработка сообщений из состояния chat
@user_router.message(StateFilter(Chat.chat))
async def process_chat(message: Message):
    response = await gpt_text(system_content="Ты персональный помощник, дающий подробные ответы",
                              user_request=message.text)
    await message.answer(response)


# ------------------------------------------------
# Обработчики выдачи случайного факта

# Обработка команды /random, установка состояния random
@user_router.message(F.text == 'Узнать случайный факт')
@user_router.message(Command('random'))
async def process_random_command(message: Message, state: FSMContext):
    await state.set_state(Chat.random)
    photo_file = FSInputFile(path=path.join(images_dir, 'fact.jpg'))
    await message.answer_photo(photo=photo_file)
    await message.answer(
        text=LEXICON_RU['/random'].replace('name', message.from_user.full_name),
    )
    response = await gpt_text(system_content=PROMPTS_RU['/random'], user_request='Напиши интересный факт')
    await message.answer(response, reply_markup=kb_random())


# Обработка сообщений из состояния random
@user_router.message(F.text == 'Хочу ещё факт')
@user_router.message(StateFilter(Chat.random))
async def process_random(message: Message):
    response = await gpt_text(system_content=PROMPTS_RU['/random'], user_request=message.text)
    await message.answer(response, reply_markup=kb_random())


# ------------------------------------------------
# Обработчики диалога со звездой

# Обработка команды /talk, установка состояния talk
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


# Обработка сообщений из состояния talk, установка состояния dialog_with_star при выборе звезды
@user_router.callback_query(StateFilter(Chat.talk))
async def process_talk(callback: CallbackQuery, state: FSMContext):
    photo_file = FSInputFile(path=path.join(images_dir, f'{callback.data}.jpg'))
    await callback.bot.send_photo(chat_id=callback.from_user.id, photo=photo_file)
    response = await gpt_text(system_content=f'Ты - мировая звезда {STARS[callback.data]}',
                              user_request='Расскажи кратко о себе, и попроси задать к себе вопрос'
                              )
    await state.update_data(name=callback.data, dialog=[])
    await callback.bot.send_message(chat_id=callback.from_user.id, text=response)
    await state.set_state(Chat.dialog_with_star)


# Обработка сообщений из состояния dialog_with_start
@user_router.message(StateFilter(Chat.dialog_with_star))
async def process_dialog(message: Message, state: FSMContext):
    content = await state.get_data()
    user_request = {
        "role": "user",
        "content": message.text
    }
    content['dialog'].append(user_request)
    await state.update_data(dialog=content['dialog'])
    response = await gpt_text(system_content=STARS[content['name']],
                              user_request='',
                              messages_list=content['dialog'])
    await message.answer(response, reply_markup=kb_dialog_with_star())

    star_response = {
        "role": "assistant",
        "content": response

    }
    content['dialog'].append(star_response)
    await state.update_data(dialog=content['dialog'])


# ------------------------------------------------
# Обработчики игры в квиз

# Обработка команды /quiz, установка состояния quiz
@user_router.callback_query(F.data == 'quiz', StateFilter(Chat.user_answer))
@user_router.message(F.text == 'Поиграть в квиз')
@user_router.message(Command('quiz'))
async def process_quiz_command(message: Message | CallbackQuery, state: FSMContext):
    if isinstance(message, Message):
        await state.update_data(score=0)
        photo_file = FSInputFile(path=path.join(images_dir, 'quiz.jpg'))
        await message.answer_photo(photo=photo_file)
        await message.answer(
            text=LEXICON_RU['/quiz'].replace('name', message.from_user.full_name),
            reply_markup=kb_quiz_themes(1)
        )

    else:
        await message.bot.send_message(
            chat_id=message.from_user.id,
            text=LEXICON_RU['/quiz'].replace('name', message.from_user.full_name),
            reply_markup=kb_quiz_themes(1)
        )
    await state.set_state(Chat.quiz)


# Обработка колбека quiz и передача их в чат gpt, установка состояния user_answer
@user_router.callback_query(StateFilter(Chat.quiz))
async def process_quiz(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    response = await gpt_text(system_content=QUIZ['system'], user_request=callback.data)
    await callback.bot.send_message(chat_id=callback.from_user.id, text=response)
    await state.update_data(question=response, score=data['score'], current_topic=callback.data)
    await state.set_state(Chat.user_answer)


# Отдельная обработка коллбека quiz_more
@user_router.callback_query(F.data == 'quiz_more', StateFilter(Chat.user_answer))
async def process_quiz_more(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    topic = data["current_topic"]
    response = await gpt_text(system_content=QUIZ['system'], user_request=topic)
    await callback.bot.send_message(chat_id=callback.from_user.id, text=response)
    await state.update_data(question=response, score=data['score'], current_topic=topic)
    await state.set_state(Chat.user_answer)


# Проверка корректности ответа пользователя
@user_router.message(StateFilter(Chat.user_answer))
async def process_quiz_check_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    result = await gpt_text(system_content=QUIZ['system'],
                            assistant_content=data['question'],
                            user_request=message.text)
    if result == 'Правильно!':
        data['score'] += 1
        await state.update_data(score=data['score'])
    await message.answer(f"{result}  \nВаш текущий счет: {data['score']}", reply_markup=kb_quiz_game())



# ------------------------------------------------
# Обработчики переводчика
@user_router.message(F.text == "Сменить язык")
@user_router.message(Command('translate'))
@user_router.message(F.text == "Перевести текст")
async def process_translate_command(message: Message, state: FSMContext):
    await state.set_state(Chat.get_language_to_translate)
    await message.answer(
        text=LEXICON_RU['/translate'].replace('name', message.from_user.full_name),
        reply_markup=kb_translate(*LANGUAGES)
    )


@user_router.message(StateFilter(Chat.get_language_to_translate))
async def process_get_language(message: Message, state: FSMContext):
    if message.text.capitalize() in LANGUAGES:
        await state.update_data(language=message.text)
        data = await state.get_data()
        await message.answer(f"Напишите текст для перевода на {data['language']} язык",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(Chat.translate)
    else:
        await message.answer('Данного языка нет в моем списке')


@user_router.message(StateFilter(Chat.translate))
async def process_translate(message: Message, state: FSMContext):
    user_text = message.text
    data = await state.get_data()
    response = await gpt_text(
        system_content=TRANSLATE['system'].replace('language', data['language']),
        user_request=user_text
    )
    await message.answer(response, reply_markup=kb_translate_menu())
