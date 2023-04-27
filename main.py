from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher import FSMContext
from config_reader import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from news import *
from weather import *
from bot_user_class import *

dp = Dispatcher(bot = Bot(token=config.bot_token.get_secret_value()), storage=MemoryStorage())


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    first_str = "Привет!\nЯ Aide, твой виртуальный помощник. Нажми 'Создать профиль', чтобы начать"
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Создать профиль"]
    keyboard.add(*buttons)
    await message.answer(f"*{first_str}*", parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(Text(equals=["Создать профиль"]),state=None)
async def profile_name(message: types.Message):
    await message.answer(f"*Как тебя зовут?*", parse_mode='Markdown')
    await Test.One.set()


@dp.message_handler(state=Test.One)
async def answer_name(message: types.Message, state: FSMContext):
    global answer_n
    answer_n = message.text #answer хранит имя, которе напишет пользователь
    await state.update_data(answer_first=answer_n)
    await message.answer(f"*Имя сохранено*\nВ каком городе ты живешь?", parse_mode='Markdown')
    await Test.Two.set()


@dp.message_handler(state=Test.Two)
async def answer_city(message: types.Message, state: FSMContext):
    global user, answer_c
    answer_c = message.text
    user = User(answer_n, answer_c) #пользователь сохранен
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Новости", "Погода", "Переводчик"]
    keyboard.add(*buttons)
    await state.update_data(answer_two=answer_c)
    await message.answer(f"*Отлично!\nДанные сохранены*\n\nВыбери нужную функцию, чтобы продолжить", parse_mode='Markdown', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(commands=["myprofile"])
async def print_profile(message: types.Message):
    await message.answer(user.print())


@dp.message_handler(Text(equals=["Новости"]))
async def get_news(message: types.Message):
    links = get_link()
    str = ''
    for i in links:
        str += print_news_header(i)
        str += "\n"
        str += "Прочитать продолжение вы сможете в источнике: " + i
        str += "\n\n\n"
    await message.answer(f"*{str}\n*", parse_mode='Markdown')


@dp.message_handler(Text(equals=["Погода"]))
async def get_w(message: types.Message):
    city = user.get_city()
    await message.answer(get_weather(city))


@dp.message_handler(Text(equals=["Переводчик"]))
async def trans(message: types.Message):
    await message.answer(f"_Функция пока недоступна..._", parse_mode='Markdown')



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
