import json
import requests
from bs4 import BeautifulSoup


def get_addresses(url):
    """
    Функция для получения адресов (улиц и домов Краснодара).
    :param url: Адрес сайта со списком адресов.
    :return: Словарь адресов.
    """
    streets_dict, letter_dict = {}, {}
    letter = ' '
    html_all_streets = requests.get(url).text
    soup = BeautifulSoup(html_all_streets, 'lxml')
    # список улиц и объектов включенных в класс ulica_list
    streets_lst = soup.find('div', class_='ulica_list')
    # получение всех объектов div из streets_lst
    div = streets_lst.find_all('div')

    for d in div:
        # Проверяем букву
        if d.has_attr('class') and d['class'][0] == 'first_l':
            letter = d.text if d.text != ' ' else 'num'
            streets_dict[letter] = []
            letter_dict = {}
        # Название улицы
        if d.has_attr('class') and d['class'][0] == 'street_unit':
            building_numbers = []
            # street = str(d.find('a').text)
            current_street = d.find('a')['href']
            # переходим на страницу улицы
            current_url = f'https://krasnodar.ginfo.ru{current_street}'
            html_current_street = requests.get(current_url).text
            soup_2 = BeautifulSoup(html_current_street, 'lxml')
            # список номеров домов расположенных на улице
            street = " ".join(soup_2.find('h1').text.split()[:-2])
            print(street)
            building_num = soup_2.find('div', class_='dom_list')
            if building_num:
                building_numbers = [b.text for b in building_num if b.text != '\n']

            letter_dict[street] = building_numbers
            streets_dict[letter] = letter_dict

    with open('files/addresses_v2.json', 'w') as outfile:
        json.dump(streets_dict, outfile)

    return streets_dict

# 1705 улиц
# 1599
# 1646 !