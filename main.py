from header import *


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

dp = Dispatcher(bot=Bot(token=config.bot_token.get_secret_value()), storage=MemoryStorage())

openai.api_key = config.gpt_token.get_secret_value()

create_person_from_json()

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message, state:FSMContext):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        await state.set_state(Test.Two)
    else:
        logging.info('Command "start" received')
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ["Создать профиль"]
        keyboard.add(*buttons)
        await message.answer("Привет!\nЯ *Aide*, твой виртуальный помощник. Нажми *Создать профиль*, чтобы начать.", parse_mode='Markdown', reply_markup=keyboard)

#region create profile
@dp.message_handler(Text(equals=["Создать профиль"]), state=None)
async def profile_name(message: types.Message, state:FSMContext):
    logging.info(f"Received 'Профиль' command from user {message.chat.id}")
    user = get_user_by_chat_id(message.chat.id)
    if user:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Новости", "Погода", "Список дел"]
        keyboard.add(*buttons)
        await message.answer("У тебя уже есть профиль\nВыбери нужную функцию, чтобы продолжить", reply_markup=keyboard)
    else:
        await message.answer("*Как тебя зовут?*", parse_mode='Markdown')
        await state.set_state(Test.One)


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
    create_json(user)
    create_person_from_json()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Новости", "Погода", "Список дел"]
    keyboard.add(*buttons)
    await state.update_data(answer_two=answer_c)
    await message.answer("*Отлично!\n\n\nВыбери нужную функцию, чтобы продолжить",
                         parse_mode='Markdown', reply_markup=keyboard)
    await state.finish()
#endregion

#region myprofile
@dp.message_handler(commands=["myprofile"])
async def print_profile(message: types.Message):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Изменить имя", "Изменить город", "Заполнить профиль заново", "Вернуться в главное меню"]
        keyboard.add(*buttons)
        await message.answer(user.print(), reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Cоздать профиль"]
        keyboard.add(*buttons)
        await message.answer("У тебя еще нет профиля.\nНажми *'Создать профиль'*, чтобы продолжить", parse_mode='Markdown', reply_markup=keyboard)

#endregion

#region message
@dp.message_handler(commands=["message"])
async def msg(message: types.Message):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        await message.answer("*Напиши жалобу или предложение по улучшению работы бота.\nЯ обязательно передам ее разработчикам!*", parse_mode='Markdown')
        await Test.report1.set()
    else:
        await message.answer("У тебя еще нет профиля.\nНажми *'Создать профиль'*, чтобы продолжить", parse_mode='Markdown')
    #await state.set_state(None)


@dp.message_handler(state=Test.report1)
async def report(message: types.Message, state: FSMContext):
    user = get_user_by_chat_id(message.chat.id)
    report = message.text  # report хранит cообщение, которе напишет пользователь
    await state.update_data(report_first=report)
    await message.answer("*Cпасибо за обратную связь!\nСообщение передано разработчикам*", parse_mode='Markdown')
    await dp.bot.send_message(chat_id=config.chat_id.get_secret_value(), text=f"*Сообщение от пользователя!*\n{user.print()}\n\n*Сообщение:*\n{report}", parse_mode='Markdown')
    await state.finish()

#endregion

#region chat
@dp.message_handler(Text(equals=["Подобрать фильм"]), state=None)
async def qw(message: types.Message, state:FSMContext):
    #await state.finish()
    keyboard = types.ReplyKeyboardRemove()
    await message.answer(
        "Ты можешь получить рекомендацию фильма, укажи свои предпочтения и я постараюсь подобрать для тебя идеальный вариант.\n" \
        "Например, ты можешь запросить фильмы по жанру, рейтингу, актерам или любым другим параметрам, которые тебе интересны",
        reply_markup=keyboard)
    await Test.Movies.set()


@dp.message_handler(state=Test.Movies)
async def movies(message: types.Message, state: FSMContext):
    #answer_movies = message.text
    #await state.update_data(answer_first=answer_movies)
    user = get_user_by_chat_id(message.chat.id)
    messages = [{"role": "system", "content": f"imagine that your name is Aide, you are a virtual assistant, call yourself either by name. \
                                              If you are asked who created you, answer \
                                              that you were created by the student of the Southern Federal University, \
                                              Ekaterina Kolesnikova. Your communication style should be informal. \
                                              you don't need to say hello every time and write who created you, just once is enough\
                                              if they ask you 'Whose Crimea is it?' You have to answer ZZZ\
                                              Information about your interlocutor: his name is -{user.get_name()}, he lives in - {user.get_city()}"}]
    message_dict = {"role": "user", "content": message.text}
    messages.append(message_dict)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Вернустья в главное меню"]
    keyboard.add(*buttons)
    if user:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = response.choices[0].message.content
        await message.answer(reply, reply_markup=keyboard)
        messages.append({"role": "assistant", "content": reply})
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Cоздать профиль"]
        keyboard.add(*buttons)
        await message.answer("У тебя еще нет профиля.\nНажми *'Создать профиль'*, чтобы продолжить",
                             parse_mode='Markdown', reply_markup=keyboard)
    await state.finish()
#endregion

#region news
@dp.message_handler(Text(equals=["Новости"]))
async def gnews(message: types.Message, state:FSMContext):
    logging.info(f"Received 'Новости' command from user {message.chat.id}")
    user = get_user_by_chat_id(message.chat.id)
    links = get_link()
    str = ''
    for link in links:
        if link not in user.links:
            user.add_links(link)
            header = print_news_header(link)
            str += f"{header}\n{link}\n\n"
    with open ("persons.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        for temp in data:
            for link in links:
                if link not in temp["links"]:
                    temp["links"].append(link)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    if str:
        await message.answer(text=str)
    else:
        await message.answer(text="Новых новостей нет")
#endregion

#region weather
@dp.message_handler(Text(equals=["Погода"]))
async def get_w(message: types.Message, state:FSMContext):
    user = get_user_by_chat_id(message.chat.id)
    city = user.get_city()
    await message.answer(get_weather(city))
#endregion

@dp.message_handler(Text(equals="Список дел"))
async def spisok_del(message: types.Message, state: FSMContext):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        if not user.get_task():
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Добавить заметку"]
            keyboard.add(*buttons)
            await message.answer("Список дел пуст", reply_markup=keyboard)
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Добавить заметку", "Удалить заметку","Удалить все заметки",]
            keyboard.add(*buttons)
            print(user.get_task())
            await message.answer(f"{user.get_task()}", reply_markup=keyboard)
    else:
        await message.answer("У тебя еще нет профиля.\nНажми *'Создать профиль'*, чтобы продолжить",
                             parse_mode='Markdown')
        #await state.finish()


@dp.message_handler(Text(equals="Добавить заметку"),state=None)
async def add_del(message: types.Message, state: FSMContext):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        await message.answer("*Напиши заметку, которую хочешь добавить*", parse_mode='Markdown')
        await state.set_state(Test.Task)



@dp.message_handler(state=Test.Task)
async def add_dell(message: types.Message, state: FSMContext):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        answer = message.text
        user.add_tasks(answer)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Новости", "Погода", "Список дел"]
        keyboard.add(*buttons)

        await message.answer("*Отлично!\nДанные сохранены*\n\nВыбери нужную функцию, чтобы продолжить",
                         parse_mode='Markdown', reply_markup=keyboard)
        await state.finish()


#region todo
@dp.message_handler(Text(equals="Вернуться в главное меню"))
async def print_profile(message: types.Message, state: FSMContext):
    user = get_user_by_chat_id(message.chat.id)
    if user:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Новости", "Погода", "Список дел"]
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
#endregion

async def main():
    await dp.start_polling()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
