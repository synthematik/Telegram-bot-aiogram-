from aiogram.dispatcher.filters.state import State, StatesGroup
import json


class User:
    users = {}
    def __init__(self, name, city, chat_id):
        self.__name = name
        self.__city = city
        self.chat_id = chat_id
        self.links = []

    @classmethod
    def get_chat(cls, name, city, chat_id):
        if chat_id not in cls.users:
            cls.users[chat_id] = User(name, city, chat_id)
        return cls.users[chat_id]

    def set_name(self, name):
        self.__name = name

    def set_city(self, city):
        self.__city = city

    def get_name(self):
        return self.__name

    def get_city(self):
        return self.__city

    def add_links(self, link):
        self.links.append(link)

    def get_links(self):
        return self.links

    def get_chat_id(self):
        return self.chat_id

    def print(self):
        return (f"Имя: {self.__name}\n" \
                f"Город: {self.__city}")


class Test(StatesGroup):
    One = State()
    Two = State()
    News = State()
    Movies = State()
    Weather = State()
    Translator = State()
    Profile = State()
    report1 = State()
    report2 = State()



mass = []

def check_is(chat_id):  # айди пользователя
    f = open("persons.json", "r", encoding="utf-8")
    try:
        data = json.load(f)
        f.close()
        for temp in data:
            if temp.get("chat_id") == chat_id:
                return False
        return True
    except json.decoder.JSONDecodeError:
        return True


def create_json(user):
    if check_is(user.chat_id):
        person_dict = {
            "name": user.get_name(),
            "chat_id": user.get_chat_id(),
            "city": user.get_city(),
            "links": user.get_links()
        }
        try:
            with open("persons.json", "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = []
        data.append(person_dict)
        with open("persons.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

mass  = []
def create_person():
    with open("persons.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for i in data:
            a = User(i.get("name"), i.get("city"), i.get("chat_id"))
            b = i.get("links")
            for j in b:
                a.add_links(j)
            mass.append(a)


c = User("Kolya", "Piter", 252325235)

create_json(c)

create_person()

for i in mass:
    print(i.print())