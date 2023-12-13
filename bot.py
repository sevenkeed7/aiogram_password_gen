import logging
from aiogram import Bot, Dispatcher, executor, types
import random
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Я бот-генератор паролей.", reply_markup=get_start_keyboard())


def get_start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    password_button = types.KeyboardButton(text="Сгенерировать пароль")
    help_button = types.KeyboardButton(text="Помощь")
    keyboard.add(password_button, help_button)
    return keyboard


@dp.message_handler(commands=['help'])
@dp.message_handler(lambda message: message.text == 'Помощь')
async def start(message: types.Message):
    await message.answer("Список команд:\n/start - перезапустить бота\n/help - узнать список команд\n/password - сгенерировать пароль", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['password'])
@dp.message_handler(lambda message: message.text == 'Сгенерировать пароль')
async def generate_password(message: types.Message):
    await message.answer("Введите длину пароля.", reply_markup=types.ReplyKeyboardRemove())

    @dp.message_handler()
    async def generate_password(message: types.Message):
        try:
            password_length = int(message.text)
            if password_length <= 0 or password_length >100:
                raise ValueError
            password = generate_random_password(password_length)
            await message.answer(f"Вот твой пароль:\n{password}", reply_markup=get_keyboard())
        except ValueError:
            await message.answer("Пожалуйста, введи число от 0 до 100.")



def generate_random_password(length: int):
    chars = []
    
    with open('data.txt') as file:
        for line in file:
            chars.extend(line.strip())
    
    
    password = []
    password = ''.join(random.choice(chars) for i in range(length))
    return password


def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    good_button = types.KeyboardButton(text="Хорошо")
    more_options_button = types.KeyboardButton(text="Еще вариант")
    keyboard.add(good_button, more_options_button)
    return keyboard


@dp.message_handler(text=["Хорошо", "Еще вариант"])
async def handle_keyboard_buttons(message: types.Message):
    if message.text == "Хорошо":
        await message.answer("Отлично! Если у тебя есть еще вопросы, задавай.", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Еще вариант":
        await message.answer("Хорошо, введи еще раз длину пароля, который тебе нужен.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Извини, я не понимаю эту команду.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
