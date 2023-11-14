import json
from bot_user_class import *
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
            "tasks": user.get_task(),
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


mass = []


def create_person_from_json():
    with open("persons.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for i in data:
            a = User(i.get("name"), i.get("city"), i.get("chat_id"), i.get("tasks"), i.get("links"))
            mass.append(a)


def get_user_by_chat_id(chat_id):
    for user in mass:
        if user.chat_id == chat_id:
            return user
    return None