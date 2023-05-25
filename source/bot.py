import json
import os
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')

bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

users_base = {}


async def open_data_event():
    with open('../resource/data.json', 'r', encoding='utf-8') as json_file:
        return random.choice(json.load(json_file))


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру '
                         '"Угадай дату по фото"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправьте команду /help')
    users_base[f'user_{message.from_user.id}'] = message.from_user.id
    users_base[f'in_game_{message.from_user.id}'] = False


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Правила игры:\n\nЯ пришлю фото и несколько дат.\n'
                         'Нужно угадать, какая дата на фото.\n\n'
                         'Доступные команды:\n'
                         '/help - правила игры и список команд\n'
                         '/cancel - выйти из игры\n'
                         'Для начала игры напишите любую из фраз: Да, Давай, '
                         'Сыграем, Игра, Играть, Хочу играть')


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    try:
        if users_base[f'user_{message.from_user.id}']:
            users_base[f'in_game_{message.from_user.id}'] = False
            await message.answer('Вы вышли из игры. Если захотите сыграть '
                                 'снова - напишите об этом')
        else:
            await message.answer('А мы итак с вами не играем. '
                                 'Может, сыграем разок?')
    except KeyError:
        await message.answer('Мы сейчас  не играем. Хотите поиграть?')


@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра',
                       'Играть', 'Хочу играть'], ignore_case=True))
async def process_positive_answer(message: Message):
    users_base[f'user_{message.from_user.id}'] = message.from_user.id
    users_base[f'in_game_{message.from_user.id}'] = False

    if not users_base[f'in_game_{message.from_user.id}']:
        await message.answer('Отлично. Сейчас я пришлю фото и даты!')
        data_event = await open_data_event()
        await message.answer(data_event['description_answer'])
        await bot.send_photo(message.chat.id, data_event['image_path_event'])
        await message.answer(
            f'Какой год на фото?\n{data_event["answer_options"]}')
        users_base[f'in_game_{message.from_user.id}'] = True
        users_base['secret_date'] = data_event['date_event']
        users_base['answer_options'] = data_event['answer_options']
        users_base['description_event'] = data_event['description_event']
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только ввод года'
                             'и команды /cancel и /stat')


@dp.message(lambda x: x.text and x.text.isdigit())
async def process_numbers_answer(message: Message):
    try:
        if users_base[f'in_game_{message.from_user.id}']:
            if int(message.text) == users_base['secret_date']:
                await message.answer(
                    'Правильно! Вы отлично разбираетесь в датах.\n\n'
                    f'{users_base["description_event"]}')
                users_base[f'in_game_{message.from_user.id}'] = False
            else:
                await message.answer(f'К сожалению, ответ неправильный.\n\n'
                                     f'Правильный ответ - {users_base["secret_date"]}\n\n'
                                     f'{users_base["description_event"]}')
                users_base[f'in_game_{message.from_user.id}'] = False
        else:
            await message.answer('Мы еще не играем. Хотите сыграть?')
    except KeyError:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message()
async def process_other_text_answers(message: Message):
    await message.answer('Я довольно ограниченный бот, давайте '
                         'просто сыграем в игру?\n\nПришлите год события.')


if __name__ == '__main__':
    dp.run_polling(bot)
