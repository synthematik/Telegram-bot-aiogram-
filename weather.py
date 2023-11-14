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
        message =  f"*Сегодня в городе* {city}\n\n" \
              f"*Погода:* {weather_description}\n" \
              f"*Температура воздуха:* {temperature:.1f}°C\n" \
              f"*Ощущается как:* {feels_temperature:.1f}°C\n" \
              f"*Максимальная температура:* {max_temperature:.1f}°C\n" \
              f"*Минимальная температура:* {min_temperature:.1f}°C\n" \
              f"\n*Давление:* {pressure} мм ртутного столба\n" \
              f"*Влажность:* {humidity}%\n" \
              f"*Скорость ветра:* {wind_speed:.2f} м/c\n" \
              f"\n*Рассвет:* {sunrise.strftime('%H:%M:%S')}\n" \
              f"*Закат:* {sunset.strftime('%H:%M:%S')}"
        separator = "-" * 30
        message = f"{separator}\n{message}\n{separator}"
        return message
    else:
        return "Не удалось получить данные о погоде."


