from aiogram.dispatcher.filters.state import State, StatesGroup
import json

class User:
    users = {}

    def __init__(self, name, city, chat_id, task_list={}, links=[]):
        self.__name = name
        self.__city = city
        self.chat_id = chat_id
        self.task_list = task_list
        self.links = links

    @classmethod
    def get_chat(cls, name, city, chat_id):
        if chat_id not in cls.users:
            cls.users[chat_id] = User(name, city, chat_id, task_list={}, links=[])
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

    def get_task(self):
        return self.task_list

    def add_tasks(self, n):
        dictionary = self.task_list
        temp = len(dictionary)
        self.task_list[temp + 1] = n
        self.save_tasks()
    def update_task(self, n):
        if str(n) in self.task_list:
            self.task_list[str(n)] = input("Введите новую задачу: ")
            self.save_tasks()
    def delete_task(self, n):
        str_n = str(n)
        if str_n in self.task_list:
            value = self.task_list.pop(str_n)
            for k in list(self.task_list.keys()):
                if int(k) > n:
                    self.task_list[str(int(k) - 1)] = self.task_list.pop(k)
                    self.save_tasks()

    def delete_all_task(self):
        self.task_list.clear()
        self.save_tasks()

    def save_tasks(self):
        user_data = {
            "name": self.__name,
            "city": self.__city,
            "chat_id": self.chat_id,
            "task_list": self.task_list,
            "links": self.links
        }
        with open("persons.json", "r",encoding="utf-8") as file:
            data = json.load(file)

        for i, person in enumerate(data):
            if person["chat_id"] == self.chat_id:
                data[i] = user_data
                break
        else:
            data.append(user_data)

        with open("persons.json", "w",encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def print(self):
        return (f"Имя: {self.__name}\n"
              f"Город: {self.__city}\n"
              f"Список дел: {self.task_list}\n")


class Test(StatesGroup):
    One = State()
    Two = State()
    Tree = State()
    Task = State()
    Movies = State()
    report1 = State()


