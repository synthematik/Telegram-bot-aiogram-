#buttons = ["Город", "Новости"]
#keyboard.add(*buttons)
#await message.answer("Нажми: \nГород - для выбора своего города\nНовости - для просмотра актуальных новостей", reply_markup=keyboard)
#f"Ваш город: ", reply_markup=keyboard)

# cделать :продолжение: курсивом
#print_news_header(i)

#city = input("Введите название города: ")
#print(get_weather(city))

#keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #buttons = ["Имя", "Город проживания"]
    #keyboard.add(*buttons)

#await message.answer(f"В каком городе ты живешь?", parse_mode='Markdown')


#str += print_news_header(i)
       # str += "\n"
      #  str += "Прочитать продолжение вы сможете в источнике: " + i
     #   str += "\n\n\n"
    #await message.answer(f"*{str}\n*", parse_mode='Markdown')


#chat_id = message.chat.id
   # user = User.get_chat(None, None, chat_id)
   # name = user.get_name(chat_id)
   # city = user.get_city(chat_id)
   # user.get_chat(name, city, chat_id)

@dp.message_handler(Text(equals=["Создать профиль"]), state=None)
async def profile_name(message: types.Message):
    await message.answer(f"*Как тебя зовут?*", parse_mode='Markdown')
    await Test.One.set()


@dp.message_handler(state=Test.One)
async def answer_name(message: types.Message, state: FSMContext):
    global answer_n
    answer_n = message.text  # answer хранит имя, которе напишет пользователь
    await state.update_data(answer_first=answer_n)
    await message.answer(f"*Имя сохранено*\nВ каком городе ты живешь?", parse_mode='Markdown')
    await Test.Two.set()


@dp.message_handler(state=Test.Two)
async def answer_city(message: types.Message, state: FSMContext):
    global answer_c
    answer_c = message.text
    user = User.get_chat(answer_n, answer_c, message.chat.id)  # пользователь сохранен
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Новости", "Погода", "Переводчик"]
    keyboard.add(*buttons)
    await state.update_data(answer_two=answer_c)
    await message.answer(f"*Отлично!\nДанные сохранены*\n\nВыбери нужную функцию, чтобы продолжить",
                         parse_mode='Markdown', reply_markup=keyboard)
    await state.finish()


@dp.message_handler(commands=["myprofile"])
async def print_profile(message: types.Message):
    user = User.users.get(message.chat.id)
    if user:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Изменить имя", "Изменить город"]
        keyboard.add(*buttons)
        await message.answer(user.print(), reply_markup=keyboard)
    else:
        await message.answer("У тебя еще нет профиля.\nНажми *'Создать профиль'*, чтобы продолжить", parse_mode='Markdown')


# TODO
# @dp.message_handler(Text(equals=["Профиль не найден"]))
# async def notfound(message: types.Message):
#     await message.answer(profile_name(types.Message))


# TODO
@dp.message_handler(Text(equals=["Переводчик"]))
async def trans(message: types.Message):
    await message.answer(f"_Функция пока недоступна, попробуй позже..._", parse_mode='Markdown')



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
    #await message.answer(f"_Функция пока недоступна, попробуй позже..._", parse_mode='Markdown')
    await dp.current_state(chat=message.chat.id).set_state(None)

def create_the_user(answer_n, answer_c, chat_id, links):
    user = User.get_chat(answer_n, answer_c, chat_id)
    user = User.users[chat_id]
    for link in links:
        user.add_links(link.strip())
