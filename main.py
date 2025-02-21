import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import user_handlers

async def start_bot():
    '''
    Асинхронная функция, запускающая бота
    '''
    #Загружаем переменные окружения
    load_dotenv()
    bot = Bot(token=os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    #Регистрируем роутеры
    dp.include_router(user_handlers.user_router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print('Shutdown bot...')
