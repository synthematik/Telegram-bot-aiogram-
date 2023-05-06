import requests
from bs4 import BeautifulSoup
from lxml import html


def get_link():
# Адрес RIA Novosti
    ria_url = "https://ria.ru"
# Получаем страницу с новостями
    page = requests.get("https://ria.ru/services/archive/widget/more.html?id=0&date=0&articlemask=lenta_common")
# Создаем объект BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")
# Извлекаем первые три ссылки
    links = []
    for link in soup.find_all("a", class_="lenta__item-size", href=True):
        links.append(link["href"])
        if len(links) == 5:
            break
# Добавляем ссылки к адресу RIA Novosti
    ria_links = [ria_url + link for link in links]
    return ria_links

def print_news_header(url):
# Отправить GET-запрос и получить HTML-код страницы
    response = requests.get(url)
    tree = html.fromstring(response.content)
# Найти заголовок новости и ссылку на источник
    header = tree.xpath('//h1[contains(@class, "title")]/text()')[0]
# Вывести заголовок новости с ссылкой на источник
    return header
