import time
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_buildings_info(json_addresses, url):
    """
    Функция для получения информации о зданиях.
    :param json_addresses: Список адресов.
    :param url: Адрес сайта с информацией о зданиях.
    :return:
    """
    # открываем браузер
    browser = wd.Chrome()
    # перебираем списки улиц полученные с сайта krasnodar.ginfo.ru
    result_dict = {}
    for key, value in json_addresses.items():
        # tuple - 1599,  set - 1542
        streets = set(s.strip().split(',')[0] for s in value.keys())
        # перебираем улицы в множестве
        street_info_dict = {}
        for street in streets:
            browser.get("https://аис.фрт.рф/search/houses")
            browser.implicitly_wait(10)
            print(street)
            # ищем информацию об улице
            search = browser.find_element(By.XPATH, "//input[@class='w-100 ui-autocomplete-input']")
            search.send_keys(f"край. Краснодарский, г. Краснодар, {street}")
            button_element = browser.find_element(By.XPATH, "//input[@class='green-button-text green-button']")
            button_element.click()
            search.clear()
            time.sleep(3)
            soup = BeautifulSoup(browser.page_source, 'lxml')
            street_addresses = soup.find_all('a', class_='green-link-only-hover f-16')
            # если информация не найдена пропускаем итерацию
            if not street_addresses:
                print('\nНет адресов для улицы:', street, '\n')
                street_info_dict[street] = None
                continue
            # перебираем ссылки на адреса
            build_info_dict = {}
            for article in street_addresses:
                current_url = url+article['href']
                browser.get(current_url)
                browser.implicitly_wait(10)
                soup = BeautifulSoup(browser.page_source, 'lxml')
                num_building_info = soup.find('div', class_='col-12 lg-bold-gilroy text-white mt-40 p-0')

                if not num_building_info:
                    print('ERROR', num_building_info)
                    continue
                # получаем номер дома
                num_building_info = num_building_info.text
                symbol = ' д ' if ' д. ' not in num_building_info else ' д. '
                try:
                    if len(num_building_info.split(symbol)) >= 2:
                        num_building = num_building_info.split(symbol)[1]
                    else:
                        num_building = num_building_info.split('д.')[1]
                except Exception as e:
                    print(e)
                print('Номер дома:', num_building, '\n')
                # получаем информацию о здании
                all_info = soup.find('div', class_='house-description-info')
                div = all_info.find_all('div')
                div_classes = ('text-secondary', 'f-16', 'fw-500')
                inf_from_div = [d.text for d in div if d.has_attr('class') and d['class'][0] in div_classes]
                dict_info_building = dict(zip(inf_from_div[::2], inf_from_div[1::2]))
                build_info_dict[num_building] = dict_info_building
            street_info_dict[street] = build_info_dict
            print(f'street_info_dict:')
            for k, v in street_info_dict.items():
                print(f'{k}: {v}')
            print()

        result_dict[key] = street_info_dict
        print(result_dict, '\n')
