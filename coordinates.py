import time
import json
from bs4 import BeautifulSoup
from common_func import get_dict
from selenium.webdriver import Keys
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from fuzzywuzzy import fuzz


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

        street_coord_dict = get_dict(f"files/coord_intermediate/coord_{key}.json")"""

    for street, number_building in json_addresses.items():
        if street in addresses_coord_dict:
            print('\nСОХРАНЕННАЯ УЛИЦА:', street)
            continue

        number_coord_dict = {}
        for num in number_building:
            search = browser.find_element(By.XPATH, "//input[@class='mapboxgl-ctrl-geocoder--input']")
            search.clear()
            time.sleep(1)
            search.send_keys(f"Краснодарский Край, Краснодар {street} {num} ")
            search.send_keys(Keys.ENTER)
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            grid_coordinates = soup.find('div', class_='w-full mt12 txt-ms').find('div', class_='relative')
            coordinates = []
            if grid_coordinates:
                mapbox_addr = str(grid_coordinates).split('"place_name":')[1].split('"matching_place_name"')[0]
                mapbox_addr = " ".join(mapbox_addr.replace(",\n", "").split(",")[-1].split()[:-1])
                mapbox_addr = mapbox_addr.replace("имени", "").replace("им", "").strip()
                if fuzz.token_sort_ratio(mapbox_addr, street) > 80:
                    coordinates = str(grid_coordinates).split('"center": [')[1].split('],')[0].split(', ')[::-1]
                else:
                    print('\nРАСХОЖДЕНИЕ')
                    print(mapbox_addr.lower(), "-", f"{street}".lower())
            if coordinates:
                number_coord_dict[num] = coordinates

        if number_coord_dict:
            print('\nstreet_coord_dict:', street)
            for k, v in number_coord_dict.items():
                print(f'{k} - {v}')

            addresses_coord_dict[street] = number_coord_dict

            with open('files/coordinates.json', 'w') as outfile:
                json.dump(addresses_coord_dict, outfile)

    return addresses_coord_dict
