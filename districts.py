import json
from bs4 import BeautifulSoup
from common_func import browser_connect


def get_districts_v1(url):
    """
    Функция для получения списков улиц по районам.
    :param url: Адрес сайта с информацией о районах.
    :return: Словарь со списками улиц по районам.
    """
    districts_dict = {}
    browser = browser_connect(url)
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


def get_content(key, divs, dict_content):
    for div in divs:
        if div.has_attr('class') and div['class'][0] == 'content-item':
            dict_content[key].append(div.text.replace('\n', ''))
    return dict_content


def get_districts_v2(url):
    """
    Функция для получения списков улиц по районам.
    :param url: Адрес сайта с информацией о районах.
    :return: Словарь со списками улиц по районам.
    """
    districts_dict = {}

    browser = browser_connect(url)
    soup = BeautifulSoup(browser.page_source, "lxml")
    div_content = soup.find('div', class_='col-sm-8').find('div', class_='row')
    div_districts = div_content.find_all('a')
    links_dict = dict((" ".join(a.text.split()[:2]), a['href']) for a in div_districts)

    for k, v in links_dict.items():
        districts_dict[k] = []
        browser.get(v)
        browser.implicitly_wait(5)
        soup_district = BeautifulSoup(browser.page_source, 'lxml')

        a_district = soup_district.find('div', class_='col-sm-8').find('div', class_='content-note').find('a')['href']
        print(a_district)
        browser.get(a_district)
        browser.implicitly_wait(5)
        soup_streets = BeautifulSoup(browser.page_source, 'lxml')
        div_content = soup_streets.find_all('div')

        districts_dict = get_content(k, div_content, districts_dict)

        ul = soup_streets.find_all('ul')
        for u in ul:
            if u.has_attr('class') and u['class'][0] == 'pagination':
                next_page = u.find_all('a')
                for a in next_page:
                    page_url = 'https://youkarta.ru' + a['href']
                    browser.get(page_url)
                    browser.implicitly_wait(5)
                    soup_n_page = BeautifulSoup(browser.page_source, 'lxml')
                    div_content = soup_n_page.find_all('div')

                    districts_dict = get_content(k, div_content, districts_dict)

    with open('files/districts_v2.json', 'w') as outfile:
        json.dump(districts_dict, outfile)

    return districts_dict



