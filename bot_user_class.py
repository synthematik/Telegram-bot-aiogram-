class User:
    def __init__(self, name, city):
        self.__name = name
        self.__city = city

    def set_name(self, name):
        self.__name = name

    def set_city(self, city):
        self.__city = city

    def get_name(self):
        return self.__name

    def get_city(self):
        return self.__city
