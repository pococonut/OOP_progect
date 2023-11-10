import sys
import time
import json
from bs4 import BeautifulSoup
from common_func import get_dict
from selenium.webdriver import Keys
from selenium import webdriver as wd
from selenium.webdriver.common.by import By


def check_address(street, a_links, street_addresses=None):
    """
    Функция для проверки адресов на соответствующий формат.
    Если адрес не подходит, он не будет учтен
    :param street: Улица
    :param a_links: Текст ссылки, содержащий адрес
    :param street_addresses: Список ссылок на адреса, подходящих под формат
    :return: Список ссылок на адреса, подходящих под формат
    """

    if street_addresses is None:
        street_addresses = []

    for a in a_links:
        address_building = a.text

        not_allow = ['почтовое отделение', 'г. краснодар, х.',
                     'г. краснодар, п.', 'г краснодар, х', 'ст-ца']

        types = ['проезд', 'переулок', 'улица', 'проспект', 'бульвар',
                 'набережная', 'сквер', 'площадь', 'набережная', 'тупик']

        check_num = street.split()
        for ch in check_num:
            for j in ch:
                if j.isdigit():
                    check_num.remove(ch)
                    street = " ".join(check_num)
                    break
            break

        check_street = "".join([street.lower().replace(t, '') for t in types if t in street.lower()]).strip()
        check_street = " ".join(check_street.split()) if check_street else street.lower()

        if check_street not in address_building.lower():
            print('УЛИЦЫ НЕТ В НАЗВАНИИ')
            print(address_building, "|", street)
            continue

        if [True for i in not_allow if i in address_building.lower()]:
            continue

        street_addresses.append(a)

    return street_addresses


def check_url(browser_url, a_url):
    """
    Функция для проверки текущего url адреса.
    Если текущий url адрес не совпадает с переданным в браузер, происходит завершение выполнения программы
    :param browser_url: Текущий url адрес
    :param a_url: Переданный в браузер url адрес
    """

    c_url = browser_url.split('/')
    c_url = "/".join(c_url[0:2] + ['аис.фрт.рф'] + c_url[3:])
    if c_url != a_url:
        print(c_url, a_url)
        time.sleep(30)
        print("ЗАВЕРШЕНИЕ ПРОГРАММЫ")
        sys.exit()


def get_buildings_info(json_addresses, url):
    """
    Функция для получения информации о зданиях.
    :param json_addresses: Список адресов.
    :param url: Адрес сайта с информацией о зданиях.
    :return: Словарь с информацией о зданиях.
    """

    browser = wd.Chrome()
    browser.get(url)
    check_url(browser.current_url, url)
    search_class = 'col-12 py-3 ui-autocomplete-input'
    button_class = 'col-12 find-button text-uppercase'
    button_teg = 'button'
    result_dict = get_dict("files/buildings_info.json")

    for key, value in json_addresses.items():
        if key in result_dict:
            continue

        street_info_dict = get_dict(f"files/buildings_intermediate/buildings_info_{key}.json")
        streets = set(s.strip().split(',')[0] for s in value.keys())
        # перебираем улицы в множестве
        for street in streets:
            if street in street_info_dict:
                print('СОХРАНЕННАЯ УЛИЦА:', street)
                continue

            time.sleep(5)
            browser.implicitly_wait(15)
            # ищем информацию об улице
            search = browser.find_element(By.XPATH, f'//input[@class="{search_class}"]')
            search.send_keys(Keys.SHIFT + Keys.HOME + Keys.DELETE)
            # передаем адрес в поисковую строку
            search.send_keys(f"край. Краснодарский, г. Краснодар, {street}")
            button_element = browser.find_element(By.XPATH, f'//{button_teg}[@class="{button_class}"]')
            button_element.click()

            search_class = "w-100 ui-autocomplete-input"
            button_class = "green-button-text green-button-outline"
            button_teg = 'input'

            soup = BeautifulSoup(browser.page_source, 'lxml')
            a_links = soup.find_all('a', class_='green-link-only-hover f-16')
            street_addresses = check_address(street, a_links)
            pagination = soup.find('ul', class_='pagination fl mb-0')

            if pagination:
                pages = pagination.find_all('a', class_='page-link')
                if len(pages) > 1:
                    for i in range(2, int(pages[-2].text) + 1):
                        link = browser.find_element(By.LINK_TEXT, str(i))
                        browser.execute_script("arguments[0].click();", link)
                        browser.implicitly_wait(15)
                        time.sleep(2)
                        soup = BeautifulSoup(browser.page_source, 'lxml')
                        try:
                            a_links = soup.find_all('a', class_='green-link-only-hover f-16')
                        except Exception as e:
                            print(e)
                            continue
                        street_addresses = check_address(street, a_links, street_addresses)

            # если информация не найдена пропускаем итерацию
            if not street_addresses:
                print('\nНет адресов для улицы:', street, '\n')
                street_info_dict[street] = None
                continue

            # перебираем ссылки на адреса
            build_info_dict = {}
            for article in street_addresses:
                time.sleep(2)
                address_url = 'https://аис.фрт.рф' + article['href']
                browser.get(address_url)
                browser.implicitly_wait(15)
                check_url(browser.current_url, address_url)

                soup = BeautifulSoup(browser.page_source, 'lxml')
                num_building = soup.find('div', class_='house-description-address__title')
                if not num_building:
                    print('ERROR', num_building)
                    continue

                # получаем номер дома
                num_building = num_building.text
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

                # собираемые параметры здания
                keys = ('Общая площадь, кв.м',
                        'Общая площадь жилых помещений, кв.м',
                        'Количество этажей, ед.',
                        'Численность жителей, чел.',
                        'Количество подъездов, ед.',
                        'Количество лифтов, ед.',
                        'Количество жилых помещений, ед.')

                building_keys, building_values = inf_from_div[::2], inf_from_div[1::2]
                dict_info_building = dict((building_keys[k], building_values[k]) for k in range(len(building_keys))
                                          if building_keys[k] in keys)
                print('dict_info_building', dict_info_building)
                print()

                # dict_info_building = dict(zip(inf_from_div[::2], inf_from_div[1::2]))
                # empty = all(value is None for value in v.values())
                if dict_info_building:
                    build_info_dict[num] = dict_info_building

            street_info_dict[street] = None if build_info_dict == {} else build_info_dict
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
