import requests
import datetime

def get_weather(city):
    api_key = "5f4cd582fd6e9342b63c53a145b86f2e"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_temperature = data["main"]["feels_like"]
        max_temperature = data["main"]["temp_max"]
        min_temperature = data["main"]["temp_min"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(int(data["sys"]["sunrise"]))
        sunset = datetime.datetime.fromtimestamp(int(data["sys"]["sunset"]))
        return f"Сегодня в городе {city} {weather_description}\nТемпература воздуха {temperature:.1f}°C," \
               f"ощущается как {feels_temperature:.1f}°C. Максимальная температура {max_temperature:.1f}°C," \
               f"минимальная температура {min_temperature:.1f}°C." \
               f"\nДавление {pressure} мм ртутного столба, влажность {humidity}%." \
               f"\nCкорость ветра {wind_speed:.2f} м/c." \
               f"\nРассвет сегодня в {sunrise.strftime('%H:%M:%S')}." \
               f"\nЗакат сегодня в {sunset.strftime('%H:%M:%S')}."

    else:
        return "Не удалось получить данные о погоде."



