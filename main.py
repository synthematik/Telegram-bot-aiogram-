from aiogram import Bot, executor, Dispatcher, types
from aiogram.dispatcher.filters import Text, Command
from config_reader import config
from news import *
from weather import *
from bot_user_class import User

dp = Dispatcher(bot = Bot(token=config.bot_token.get_secret_value()))


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    first_str = "Привет!\nЯ Aide, твой виртуальный помощник. Нажми 'Создать профиль', чтобы начать."
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Создать профиль", "Связь с разработчиками"]
    keyboard.add(*buttons)
    await message.answer(f"*{first_str}*", parse_mode='Markdown', reply_markup=keyboard)

@dp.message_handler(Text(equals=["Город"]))
async def with_puree(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Ростов-на-Дону", "Москва","Краснодар", "Ейск", "Сальск", "Батайск"]
    keyboard.add(*buttons)
    await message.answer(get_weather("Ейск"))

@dp.message_handler(Text(equals=["Новости"]))
async def with_puree(message: types.Message):
    links = get_link()
    str = ''
    for i in links:
        str += print_news_header(i)
        str += "\n"
        str += "Прочитать продолжение вы сможете в источнике: " + i
        str += "\n\n\n"
    await message.answer(f"*{str}\n*", parse_mode='Markdown')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
