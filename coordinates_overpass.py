import json
import pandas as pd


def check_alphabet(text):
    """
    Функция для проверки того, что текст написан на русском
    :param text: Строка
    :return: Булево значение, False - текст не содержит русские буквы, True - текст на русском
    """
    alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    return not alphabet.isdisjoint(text.lower())


def write_coordinates_overpass():
    """
    Функция для обработки .txt файла с координатами, полученного с сайта https://overpass-turbo.eu
    :return: Словарь с координатами зданий Краснодара
    """
    coordinates = {}

    dataframe1 = pd.read_csv("files/coordinates_overpass.txt", delimiter="\t")
    dataframe1.to_csv('files/coordinates_overpass.csv', index=None)
    df = pd.read_csv('files/coordinates_overpass.csv', sep=',')
    df.drop(['name', 'addr:city', 'addr:postcode'], axis=1, inplace=True)
    pd.set_option('display.max_columns', None)
    df = df.sort_values(by=['addr:street'])
    df = df.reset_index()

    for index, row in df.iterrows():
        street = row['addr:street']
        house_number = row['addr:housenumber']
        latitude = row['@lat']
        longitude = row['@lon']

        if (type(street) is float) or (type(house_number) is float):
            continue

        if not check_alphabet(street):
            continue

        if street[0].isdigit():
            street = street.split()
            street = " ".join(street[0:1] + [street[1].capitalize()] + street[2:])
        else:
            street = street.capitalize()

        if street in coordinates:
            coordinates[street][house_number] = [latitude, longitude]
        else:
            coordinates[street] = {house_number: [latitude, longitude]}

    return coordinates


with open('files/coordinates_overpass.json', 'w') as outfile:
    json.dump(write_coordinates_overpass(), outfile)