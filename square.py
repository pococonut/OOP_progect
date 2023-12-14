import time
import json

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Keys
from selenium import webdriver as wd
from selenium.webdriver.common.by import By

with open(r'files/addresses_v2.json', 'r') as openfile:
    json_addresses = json.load(openfile)

with open(r'files/buildings_info_domreestr.json', 'r') as openfile:
    b_object = json.load(openfile)

all_addresses = set()
build_addresses = set()

for letter, d1 in json_addresses.items():
    for street, num in d1.items():
        for n in num:
            all_addresses.add(f"{street} {n}")

for letter, d1 in b_object.items():
    for street, num in d1.items():
        for n in num:
            build_addresses.add(f"{street} {n}")

for_find_square = all_addresses-build_addresses
print(len(all_addresses))
print(len(build_addresses))
print(len(for_find_square))


browser = wd.Chrome()
browser.get("https://pkk.kartagov.net/")

#for key, value in json_addresses.items():

for addr in for_find_square:
    time.sleep(5)
    browser.implicitly_wait(15)
    # ищем информацию об улице
    search = browser.find_element(By.XPATH, f'//input[@class="input __input js__searchInput ui-autocomplete-input"]')
    search.send_keys(Keys.SHIFT + Keys.HOME + Keys.DELETE)
    # передаем адрес в поисковую строку

    search.send_keys(f"край. Краснодарский, г. Краснодар, {addr}")
    search.send_keys(Keys.ENTER)
    html_all_streets = requests.get(browser.current_url).text

    # button_element = browser.find_element(By.XPATH, f'//button[@class="btn btn-primary"]')
    # button_element.click()

    soup = BeautifulSoup(browser.page_source, 'lxml')

    list_addr = soup.find('div', class_="search__rb")
    print(html_all_streets)
