import time
import json
from bs4 import BeautifulSoup
from common_func import get_dict
from selenium.webdriver import Keys
from selenium import webdriver as wd
from selenium.webdriver.common.by import By


def get_coordinates(json_addresses, url):
    """
    Функция для получения координат адреса.
    :param json_addresses: Словарь с адресами.
    :param url: Адрес сайта, с которого ведется парсинг.
    :return:
    """
    browser = wd.Chrome()
    browser.get(url)
    browser.implicitly_wait(15)
    addresses_coord_dict = get_dict("files/coordinates.json")

    for key, value in json_addresses.items():
        if key in addresses_coord_dict:
            continue

        street_coord_dict = get_dict(f"files/coord_intermediate/coord_{key}.json")
        for street, number_building in value.items():
            number_coord_dict = {}
            for num in number_building:
                if list(street_coord_dict.values()) and num in list(street_coord_dict.values())[0]:
                    print('\nСОХРАНЕННЫЙ АДРЕС:', street, num, '\n')  # изменить проверку с улицы на дом
                    continue

                search = browser.find_element(By.XPATH, "//input[@class='mapboxgl-ctrl-geocoder--input']")
                search.clear()
                time.sleep(1)
                search.send_keys(f"Краснодарский Край, Краснодар {street} {num} ")
                search.send_keys(Keys.ENTER)
                time.sleep(1)
                soup = BeautifulSoup(browser.page_source, 'lxml')
                grid_coordinates = soup.find('div', class_='w-full mt12 txt-ms').find('div', class_='relative')

                if grid_coordinates:
                    coordinates = str(grid_coordinates).split('"center": [')[1].split('],')[0].split(', ')[::-1]
                    print(street, num)
                    print(coordinates)
                    print()
                else:
                    print('Нет координат для адреса:', street, num)
                    coordinates = None

                number_coord_dict[num] = coordinates
            street_coord_dict[street] = number_coord_dict

            print('\nstreet_coord_dict')
            for k, v in street_coord_dict.items():
                print(f'{k}\n{v}\n')

            with open(f'files/coord_intermediate/coord_{key}.json', 'w') as outfile:
                json.dump(street_coord_dict, outfile)

        addresses_coord_dict[key] = street_coord_dict

        with open('files/coordinates.json', 'w') as outfile:
            json.dump(addresses_coord_dict, outfile)

    return addresses_coord_dict
