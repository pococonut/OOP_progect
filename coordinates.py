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

    """for key, value in json_addresses.items():
        if key in addresses_coord_dict:
            continue

        street_coord_dict = get_dict(f"files/coord_intermediate/coord_{key}.json")

        for street, number_building in value.items():
            number_coord_dict = {}
            for num in number_building:
                if num in list(street_coord_dict.values())[0]:
                    print('\nСОХРАНЕННЫЙ АДРЕС:', street, num)  # изменить проверку с улицы на дом
                    continue

                coordinates = []
                time.sleep(2)
                print(street, num)

                search = browser.find_element(By.XPATH, "//input[@class='custom-input__input']")
                search.send_keys(Keys.SHIFT + Keys.HOME + Keys.DELETE)
                button_element = browser.find_element(By.XPATH, "//button[@class='demo-form__button accented xxx-big']")
                search.send_keys(f"г. Краснодар, {street} {num}")

                try:
                    button_element.click()
                except Exception as e:
                    print(e)
                    continue

                soup = BeautifulSoup(browser.page_source, 'lxml')
                grid_coordinates = soup.find_all('div', class_='grid-2-cols--withMobile')  # green-link-only-hover f-16
                if grid_coordinates:
                    grid_coordinates = grid_coordinates[0].find_all('span')[:5]
                    for el in grid_coordinates:
                        if not el.has_attr('class'):
                            coordinates.append(el.text)
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

    return addresses_coord_dict"""


def get_coordinates_0(json_addresses, url):
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
                if num in list(street_coord_dict.values())[0]:
                    print('\nСОХРАНЕННЫЙ АДРЕС:', street, num)  # изменить проверку с улицы на дом
                    continue

                coordinates = []
                time.sleep(2)
                print(street, num)

                search = browser.find_element(By.XPATH, "//input[@class='custom-input__input']")
                search.send_keys(Keys.SHIFT + Keys.HOME + Keys.DELETE)
                button_element = browser.find_element(By.XPATH, "//button[@class='demo-form__button accented xxx-big']")
                search.send_keys(f"г. Краснодар, {street} {num}")

                try:
                    button_element.click()
                except Exception as e:
                    print(e)
                    continue

                soup = BeautifulSoup(browser.page_source, 'lxml')
                grid_coordinates = soup.find_all('div', class_='grid-2-cols--withMobile')  # green-link-only-hover f-16
                if grid_coordinates:
                    grid_coordinates = grid_coordinates[0].find_all('span')[:5]
                    for el in grid_coordinates:
                        if not el.has_attr('class'):
                            coordinates.append(el.text)
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