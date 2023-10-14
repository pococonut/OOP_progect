import time
from bs4 import BeautifulSoup
from selenium import webdriver as wd


def get_districts(url):
    """
    Функция для получения списков улиц по районам.
    :param url: Адрес сайта с информацией о районах.
    :return: Словарь со списками улиц по районам.
    """
    districts_dict = {}
    browser = wd.Chrome()
    browser.get(url)
    browser.implicitly_wait(15)
    time.sleep(15)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    div_page = soup.find('div', class_='bigblock row categories')
    div = div_page.find_all('div')
    key = ' '
    for d in div:
        if d.has_attr('class') and d['class'][0] == 'categories-list-title':
            key = d.text
            districts_dict[key] = []
        if d.has_attr('class') and d['class'][0] == 'categories-list-items-item':
            street = str(d.find('a').text)
            districts_dict[key].append(street)

    return districts_dict

