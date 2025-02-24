from os import path


prompts_dir = path.join(path.dirname(path.abspath(__file__)), 'prompts')

def read_file(filename: str) -> str:
    with open(path.join(prompts_dir, filename), 'r', encoding="utf-8") as file:
        prompt = file.read()
    return prompt


LEXICON_RU: dict[str, str] = {
    '/start': 'Привет, name!\n'
              'Этот бот совмещает с себе удобство Telegram и мощь ChatGPT\n'
              '\nПолезные команды и ссылки:\n'
              '1. /start — главное меню бота\n'
              '2. /random - узнать рандомный факт · 🧠\n'
              '3. /gpt - Задать вопрос ChatGpt · 🤖\n'
              '4. /talk - поговорить с известной личностью · 👤\n'
              '5. /quiz - проверить свои знания ❓',
    '/help': 'name, добрый день!\n'
             'Выбери нужную кнопку меню',
    '/gpt': 'name!\nЗадай вопрос к ChatGPT:',
    '/random': 'name, вспоминаю интересный факт...',
    '/talk': 'name, \nВыберите известную личность, с которой хотите поговорить:\n'
             'Список доступных личностей:',
    '/quiz': 'name, \nПроверь свою эрудицию вместе с ChatGPT!'
             '\nВыбери тему, на которую будешь играть:'
}


PROMPTS_RU: dict[str, str] = {
    '/random': read_file('random.txt')
}


TALK_WITH_STAR_RU: dict[str, str] = {
    'Kurt_Kobain': '1. Курт Кобейн - Солист группы Nirvana 🎸',
    'ElizavetaII': '2. Елизавета II - Королева Соединённого Королевства 👑',
    'John_Tolkien': '3. Джон Толкиен - Автор книги "Властелин Колец" 📖',
    'Friedrich_Nietzsche': '4. Фридрих Ницше - Философ 🧠',
    'Stephen_Hawking': '5. Стивен Хокинг - Физик 🔬'
}


STARS: dict[str, str] = {
    'Kurt_Kobain' : read_file('talk_cobain.txt'),
    'ElizavetaII' : read_file('talk_queen.txt'),
    'John_Tolkien' : read_file('talk_tolkien.txt'),
    'Friedrich_Nietzsche' : read_file('talk_nietzsche.txt'),
    'Stephen_Hawking' : read_file('talk_hawking.txt')
}


QUIZ: dict[str, str] = {
    'system': read_file('quiz.txt')
}