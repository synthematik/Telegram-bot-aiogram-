from header import *


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

dp = Dispatcher(bot=Bot(token=config.bot_token.get_secret_value()), storage=MemoryStorage())


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    logging.info('Command "start" received')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Создать профиль"]
    keyboard.add(*buttons)
    await message.answer("Привет!\nЯ *Aide*, твой виртуальный помощник. Нажми *Создать профиль*, чтобы начать.", parse_mode='Markdown', reply_markup=keyboard)


@dp.message_handler(Text(equals=["Создать профиль"]), state=None)
async def profile_name(message: types.Message):
    await message.answer("*Как тебя зовут?*", parse_mode='Markdown')
    await Test.One.set()


@dp.message_handler(state=Test.One)
async def answer_name(message: types.Message, state: FSMContext):
    global answer_n
    answer_n = message.text  # answer хранит имя, которе напишет пользователь
    await state.update_data(answer_first=answer_n)
    await message.answer("*Имя сохранено*\nВ каком городе ты живешь?", parse_mode='Markdown')
    await Test.Two.set()



@dp.message_handler(state=Test.Two)
async def answer_city(message: types.Message, state: FSMContext):
    global answer_c
    answer_c = message.text
    user = User.get_chat(answer_n, answer_c, message.chat.id)# пользователь сохранен
    links = message.text.split(",")
    user = User.users[message.chat.id]
    for link in links:
        user.add_links(link.strip())
    #create_json(user)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Новости", "Погода", "Переводчик"]
    keyboard.add(*buttons)
    await state.update_data(answer_two=answer_c)
    await message.answer("*Отлично!\nДанные сохранены*\n\nВыбери нужную функцию, чтобы продолжить",
                         parse_mode='Markdown', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(commands=["myprofile"])
async def print_profile(message: types.Message, state:FSMContext):
    user = User.users.get(message.chat.id)
    if user:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Изменить имя", "Изменить город", "Заполнить профиль заново", "Вернуться в главное меню"]
        keyboard.add(*buttons)
        await message.answer(user.print(), reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Cоздать профиль"]
        keyboard.add(*buttons)
        await message.answer("У тебя еще нет профиля.\nНажми *'Создать профиль'*, чтобы продолжить", parse_mode='Markdown')



@dp.message_handler(commands=["message"])
async def msg(message: types.Message):
    user = User.users.get(message.chat.id)
    if user:
        await message.answer("*Напиши жалобу или предложение по улучшению работы бота.\nЯ обязательно передам ее разработчикам!*", parse_mode='Markdown')
        await Test.report1.set()
    else:
        await message.answer("У тебя еще нет профиля.\nНажми *'Создать профиль'*, чтобы продолжить", parse_mode='Markdown')
    #await state.set_state(None)


@dp.message_handler(state=Test.report1)
async def report(message: types.Message, state: FSMContext):
    user = User.users.get(message.chat.id)
    report = message.text  # report хранит cообщение, которе напишет пользователь
    await state.update_data(report_first=report)
    await message.answer("*Cпасибо за обратную связь!\nСообщение передано разработчикам*", parse_mode='Markdown')
    await dp.bot.send_message(chat_id=config.chat_id.get_secret_value(), text=f"*Сообщение от пользоватея!*\n{user.print()}\n\n*Сообщение:*\n{report}", parse_mode='Markdown')
    await state.finish()



@dp.message_handler(Text(equals=["Новости"]))
async def gnews(message: types.Message, state:FSMContext):
    #await state.set_state(Test.News)
    logging.info(f"Received 'Новости' command from user {message.chat.id}")
    user = User.get_chat(answer_n, answer_c, message.chat.id)
    links = get_link()
    str = ''
    for link in links:
        if link not in user.links:
            user.add_links(link)
            header = print_news_header(link)
            str += f"{header}\n{link}\n\n"
    if str:
        await message.answer(text=str)
    else:
        await message.answer(text="Новых новостей нет")


@dp.message_handler(Text(equals=["Погода"]))
async def get_w(message: types.Message, state:FSMContext):
    #await state.set_state(Test.Weather)
    user = User.get_chat(answer_n, answer_c, message.chat.id)
    city = user.get_city()
    await message.answer(get_weather(city))


@dp.message_handler(Text(equals="Вернуться в главное меню"))
async def print_profile(message: types.Message, state: FSMContext):
    user = User.users.get(message.chat.id)
    if user:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Новости", "Погода", "Переводчик"]
        keyboard.add(*buttons)
        await message.answer("Выбери нужную функцию, чтобы продолжить", reply_markup=keyboard)
    else:
        await message.answer("У тебя еще нет профиля.\nНажми *'Создать профиль'*, чтобы продолжить", parse_mode='Markdown')
        await state.set_state(None)


# TODO
@dp.message_handler(Text(equals=["Изменить имя"]))
async def setN(message: types.Message):
    await message.answer(f"_Функция пока недоступна, попробуй позже..._", parse_mode='Markdown')


# TODO
@dp.message_handler(Text(equals=["Изменить город"]))
async def setC(message: types.Message):
    await message.answer(f"_Функция пока недоступна, попробуй позже..._", parse_mode='Markdown')

# TODO
@dp.message_handler(Text(equals=["Заполнить профиль заново"]))
async def newP(message: types.Message, state: FSMContext):
    await message.answer(f"_Функция пока недоступна, попробуй позже..._", parse_mode='Markdown')
    #await dp.current_state(chat=message.chat.id).set_state(None)

async def main():
    await dp.start_polling()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
