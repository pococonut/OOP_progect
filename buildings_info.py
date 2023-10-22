import time
import json
import os
from bs4 import BeautifulSoup
from selenium.webdriver import Keys

from common_func import get_dict
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from common_func import browser_connect


def get_buildings_info(json_addresses, url):
    """
    Функция для получения информации о зданиях.
    :param json_addresses: Список адресов.
    :param url: Адрес сайта с информацией о зданиях.
    :return:
    """
    browser = wd.Chrome()
    browser.get(url)

    search_class = 'col-12 py-3 ui-autocomplete-input'
    button_class = 'col-12 find-button text-uppercase'
    button_teg = 'button'

    result_dict = get_dict("files/buildings_info.json")
    # открываем браузер
    # перебираем списки улиц полученные с сайта krasnodar.ginfo.ru
    for key, value in json_addresses.items():
        if key in result_dict:
            continue

        street_info_dict = get_dict(f"files/buildings_intermediate/buildings_info_{key}.json")
        # tuple - 1599,  set - 1542
        streets = set(s.strip().split(',')[0] for s in value.keys())
        # перебираем улицы в множестве
        print(street_info_dict)
        for street in streets:
            if street in street_info_dict:
                print('СОХРАНЕННАЯ УЛИЦА:', street)
                continue

            time.sleep(5)
            browser.implicitly_wait(15)
            # ищем информацию об улице

            search = browser.find_element(By.XPATH, f'//input[@class="{search_class}"]')
            search.send_keys(Keys.SHIFT + Keys.HOME + Keys.DELETE)

            # w-100 ui-autocomplete-input
            search.send_keys(f"край. Краснодарский, г. Краснодар, {street}")
            button_element = browser.find_element(By.XPATH, f'//{button_teg}[@class="{button_class}"]') # green-button-text green-button
            button_element.click()

            search_class = "w-100 ui-autocomplete-input"
            button_class = "green-button-text green-button-outline"
            button_teg = 'input'

            soup = BeautifulSoup(browser.page_source, 'lxml')
            street_addresses = soup.find_all('a', class_='green-link-only-hover f-16') # green-link-only-hover f-16
            # если информация не найдена пропускаем итерацию
            if not street_addresses:
                print('\nНет адресов для улицы:', street, '\n')
                street_info_dict[street] = None
                continue
            # перебираем ссылки на адреса
            build_info_dict = {}
            for article in street_addresses:
                time.sleep(2)
                current_url = 'https://аис.фрт.рф' + article['href']
                browser.get(current_url)
                browser.implicitly_wait(15)
                soup = BeautifulSoup(browser.page_source, 'lxml')
                num_building_info = soup.find('div', class_='house-description-address__title') # col-12 lg-bold-gilroy text-white mt-40 p-0
                if not num_building_info:
                    print('ERROR', num_building_info)
                    continue
                # получаем номер дома
                num_building_info = num_building_info.text
                print('Номер дома до обработки:', num_building_info)
                symbol = ' д ' if ' д. ' not in num_building_info else ' д. '
                try:
                    if len(num_building_info.split(symbol)) >= 2:
                        num_building = num_building_info.split(symbol)[1]
                    else:
                        num_building = num_building_info.split('д.')[1]
                except Exception as e:
                    print(e)
                    continue

                num_building = "".join([i for i in num_building if i.isdigit() or i.isalpha() or i == '/'])
                print('Номер дома после обработки:', num_building, '\n')
                # получаем информацию о здании
                all_info = soup.find('div', class_='house-description-info')
                div = all_info.find_all('div')
                div_classes = ('text-secondary', 'f-16', 'fw-500')
                inf_from_div = [d.text for d in div if d.has_attr('class') and d['class'][0] in div_classes]
                dict_info_building = dict(zip(inf_from_div[::2], inf_from_div[1::2]))
                build_info_dict[num_building] = dict_info_building
            street_info_dict[street] = build_info_dict

            search_class = 'col-12 py-3 ui-autocomplete-input'
            button_class = 'col-12 find-button text-uppercase'
            button_teg = 'button'

            print(f'street_info_dict:')
            for k, v in street_info_dict.items():
                print(f'{k}: {v}')
            print()

            with open(f'files/buildings_intermediate/buildings_info_{key}.json', 'w') as outfile:
                json.dump(street_info_dict, outfile)

        result_dict[key] = street_info_dict

        with open('files/buildings_info.json', 'w') as outfile:
            json.dump(result_dict, outfile)

    return result_dict
