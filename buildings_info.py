import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver import Keys
from common_func import get_dict
from selenium import webdriver as wd
from selenium.webdriver.common.by import By


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
            if street == 'Улица Ленина':
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
                button_element = browser.find_element(By.XPATH, f'//{button_teg}[@class="{button_class}"]')
                button_element.click()

                search_class = "w-100 ui-autocomplete-input"
                button_class = "green-button-text green-button-outline"
                button_teg = 'input'

                soup = BeautifulSoup(browser.page_source, 'lxml')

                street_addresses = soup.find_all('a', class_='green-link-only-hover f-16')
                pagination = soup.find('ul', class_='pagination fl mb-0')

                if pagination:
                    pages = pagination.find_all('a', class_='page-link')
                    for i in range(2, int(pages[-2].text) + 1):
                        link = browser.find_element(By.LINK_TEXT, str(i))

                        # button_a = browser.find_element(By.XPATH, "//a[@aria-label='Next']")
                        browser.execute_script("arguments[0].click();", link)
                        browser.implicitly_wait(15)
                        time.sleep(1)
                        soup = BeautifulSoup(browser.page_source, 'lxml')
                        street_addresses.extend(soup.find_all('a', class_='green-link-only-hover f-16'))

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
                    num_building = soup.find('div', class_='house-description-address__title')
                    if not num_building:
                        print('ERROR', num_building)
                        continue
                    # получаем номер дома
                    num_building = num_building.text

                    not_allow = ['почтовое отделение', 'г. краснодар, х.',
                                 'г. краснодар, п.', 'г краснодар, х', 'ст-ца']
                    if [True for i in not_allow if i in num_building.lower()]:
                        continue

                    print('Номер дома до обработки:', num_building)
                    symbol = ' д ' if ' д. ' not in num_building else ' д. '
                    try:
                        if len(num_building.split(symbol)) >= 2:
                            num = num_building.split(symbol)[1]
                        else:
                            num = num_building.split('д.')[1]
                    except Exception as e:
                        print(e)
                        continue

                    num = "".join([i for i in num if i.isdigit() or i.isalpha() or i == '/'])
                    print('Номер дома после обработки:', num, '\n')
                    # получаем информацию о здании
                    all_info = soup.find('div', class_='house-description-info')
                    div = all_info.find_all('div')
                    div_classes = ('text-secondary', 'f-16', 'fw-500')
                    inf_from_div = [d.text for d in div if d.has_attr('class') and d['class'][0] in div_classes]
                    dict_info_building = dict(zip(inf_from_div[::2], inf_from_div[1::2]))
                    build_info_dict[num] = dict_info_building

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
