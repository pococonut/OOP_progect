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

        types = ['улица', 'проезд', 'переулок', 'проспект', 'набережная',
                 'сквер', 'площадь', 'набережная', 'тупик', 'бульвар']

        check_num = street.split()
        for ch in check_num:
            for el in ch:
                if el.isdigit():
                    check_num.remove(ch)
                    street = " ".join(check_num)
                    break
            break

        check_street = street
        for t in types:
            if t in street.lower():
                check_street = street.lower().replace(t, '')
                break

        check_street = " ".join(check_street.split()) if check_street else street.lower()

        if check_street not in address_building.lower():
            """print('УЛИЦЫ НЕТ В НАЗВАНИИ')
            print(address_building, "|", street)
            print()"""
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
        time.sleep(60)
        return False
    return True


def make_beautiful_number(num_building, flag=0):
    """
    Функция для обработки и приведения к нужному формату номера здания
    :param flag:
    :param num_building: Строка с адресом здания
    :return: Номер здания
    """
    num = num_building
    if flag:
        symbol = ' д ' if ' д. ' not in num_building else ' д. '
        try:
            if len(num_building.split(symbol)) >= 2:
                num = num_building.split(symbol)[1]
            else:
                num = num_building.split('д.')[1]
        except Exception as e:
            print(e)
            return False

    num = num.split('(')[0] if "(" in num else num
    num = "".join([i for i in num if i.isdigit() or i.isalpha() or i == '/'])

    for_change = {'литеры': 'лит',
                  'литера': 'лит',
                  'литер': 'лит',
                  'ЛИТЕР': 'лит',
                  'корпус': 'к',
                  'стр': 'с',
                  'корп': 'к',
                  "c": "c"}

    for k, v in for_change.items():
        if k in num:
            num = num.replace(k, v)
            break

    if sum(map(lambda x: 1 if x.isalpha() else 0, num)) > 6:
        print('Большое кол-во букв', num)
        return False

    return num


def get_buildings_info(json_addresses, url):
    """
    Функция для получения информации о зданиях.
    :param json_addresses: Список адресов.
    :param url: Адрес сайта с информацией о зданиях.
    :return: Словарь с информацией о зданиях.
    """

    browser = wd.Chrome()
    browser.get(url)
    if not check_url(browser.current_url, url):
        if not check_url(browser.current_url, url):
            print("ЗАВЕРШЕНИЕ ПРОГРАММЫ")
            sys.exit()

    search_class = 'col-12 py-3 ui-autocomplete-input'
    button_class = 'col-12 find-button text-uppercase'
    button_teg = 'button'
    result_dict = get_dict("files/buildings_info.json")

    for key, value in json_addresses.items():
        if key in result_dict:
            continue

        street_info_dict = get_dict(f"files/buildings_intermediate/buildings_info_{key}.json")

        # Если словарь не пуст, удаляем последнее значение, так как из-за прерывания программы
        # информация могла сохраниться не полностью
        if street_info_dict:
            street_info_dict.popitem()

        streets = set(s.strip().split(',')[0] for s in value.keys())
        # перебираем улицы в множестве
        for street in streets:
            if street == "Краснодарская улица":
                continue
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
                        try:
                            time.sleep(2)
                            print(i)
                            link = browser.find_element(By.LINK_TEXT, str(i))
                        except Exception as e:
                            print(e)

                            # time.sleep(60)
                            # sys.exit()
                            # continue
                            break

                        browser.execute_script("arguments[0].click();", link)
                        browser.implicitly_wait(15)
                        time.sleep(2)
                        soup = BeautifulSoup(browser.page_source, 'lxml')
                        a_links = soup.find_all('a', class_='green-link-only-hover f-16')
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
                if not check_url(browser.current_url, address_url):
                    if not check_url(browser.current_url, address_url):
                        print("ЗАВЕРШЕНИЕ ПРОГРАММЫ")
                        sys.exit()

                soup = BeautifulSoup(browser.page_source, 'lxml')
                num_building = soup.find('div', class_='house-description-address__title')
                if not num_building:
                    print('ERROR', num_building)
                    continue

                # получаем номер дома
                print('Номер дома до обработки:', num_building.text)

                num = make_beautiful_number(num_building.text, 1)
                if not num:
                    continue

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

            street_info_dict[street] = {} if build_info_dict == {} else build_info_dict
            search_class = 'col-12 py-3 ui-autocomplete-input'
            button_class = 'col-12 find-button text-uppercase'
            button_teg = 'button'
            print(f'street_info_dict:')
            for k, v in street_info_dict.items():
                print(k, v)
            print()

            with open(f'files/buildings_intermediate/buildings_info_{key}.json', 'w') as outfile:
                json.dump(street_info_dict, outfile)

        result_dict[key] = street_info_dict
        with open('files/buildings_info.json', 'w') as outfile:
            json.dump(result_dict, outfile)

    return result_dict


def get_buildings_info_domreestr(json_addresses, url):
    """
    Функция для получения информации о зданиях.
    :param json_addresses: Список адресов.
    :param url: Адрес сайта с информацией о зданиях.
    :return: Словарь с информацией о зданиях.
    """

    def make_dict_info(s):
        """
        Функция для создания словаря с информацией о здании
        :param s:  объект BeautifulSoup
        :return: словарь с информацией о здании
        """

        table_building = s.find('table', class_='table table-light table-striped table-hover').find_all('td')
        keys_dict = {'Общая площадь дома, всего м2': 'Общая площадь, кв.м',
                     'Площадь жилых помещений м2': 'Общая площадь жилых помещений, кв.м',
                     'Наибольшее количество этажей': 'Количество этажей, ед.',
                     'Количество жителей': 'Численность жителей, чел.',
                     'Количество подъездов': 'Количество подъездов, ед.',
                     'Количество лифтов': 'Количество лифтов, ед.',
                     'Жилых помещений': 'Количество жилых помещений, ед.'}

        b_info = {}
        data = []
        c = 0
        for td in table_building:
            if c == 2:
                c = 0
                if data[0] in keys_dict.keys():
                    b_info[keys_dict.get(data[0])] = data[1]
                data = []
            c += 1
            data.append(td.text)

        return b_info

    browser = wd.Chrome()

    result_dict = get_dict("files/buildings_info.json")
    result_dict_domreestr = get_dict("files/buildings_info_domreestr.json")

    for key, value in result_dict.items():
        if key in result_dict_domreestr:
            print(key)
            continue

        street_info_dict = get_dict(f"files/buildings_intermediate_domreestr/buildings_info_{key}.json")
        # Если словарь не пуст, удаляем последнее значение, так как из-за прерывания программы
        # информация могла сохраниться не полностью
        if street_info_dict:
            street_info_dict.popitem()

        for street, numbers in value.items():

            if street in street_info_dict:
                print('СОХРАНЕННАЯ УЛИЦА:', street)
                continue

            browser.get(url)
            # time.sleep(1)
            browser.implicitly_wait(15)
            # ищем информацию об улице
            search = browser.find_element(By.XPATH, f'//input[@class="form-control"]')
            search.send_keys(Keys.SHIFT + Keys.HOME + Keys.DELETE)
            # передаем адрес в поисковую строку
            search.send_keys(f"край. Краснодарский, г. Краснодар, {street}")
            button_element = browser.find_element(By.XPATH, f'//button[@class="btn btn-danger btn-lg"]')
            button_element.click()

            soup = BeautifulSoup(browser.page_source, 'lxml')
            table = soup.find('tbody').find_all('a')
            all_links = [a for a in table if "Краснодар" in a.text.replace('Краснодарский', '')]
            right_links = check_address(street, all_links)
            if not right_links:
                continue

            for article in right_links:
                # time.sleep(1)
                address_url = 'https://domreestr.ru' + article['href']
                browser.get(address_url)
                browser.implicitly_wait(15)

                soup = BeautifulSoup(browser.page_source, 'lxml')

                num_building = soup.find('ul', class_='breadcrumb mt-2').find_all('li')[-1].text.strip()
                if not num_building:
                    print('ERROR', num_building)
                    continue

                # получаем номер дома
                print('Номер дома до обработки:', num_building)
                num = make_beautiful_number(num_building)
                if not num:
                    continue
                print('Номер дома после обработки:', num, '\n')

                if [True for n in numbers if num in n]:
                    continue

                print(f'Дополняем список домов {article.text} | {street}')
                print('num', num)
                print('numbers', *list(numbers.keys()))

                b_inf = make_dict_info(soup)
                if b_inf:
                    numbers[num] = b_inf
                    print('numbers', *list(numbers.keys()))
                    print(numbers, sep='\n')
            street_info_dict[street] = numbers
            print()
            print('street_info_dict')
            for k, v in street_info_dict.items():
                print(k, v)

            with open(f'files/buildings_intermediate_domreestr/buildings_info_{key}.json', 'w') as outfile:
                json.dump(street_info_dict, outfile)

        result_dict_domreestr[key] = street_info_dict
        with open('files/buildings_info_domreestr.json', 'w') as outfile:
            json.dump(result_dict_domreestr, outfile)
