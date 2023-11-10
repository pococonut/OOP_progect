import json
import time
from coordinates import get_coordinates
from districts import get_districts_v1
from addresses import get_addresses
from buildings_info import get_buildings_info

start_time = time.time()

url_buildings_info = 'https://аис.фрт.рф/myhouse'
url_addresses = 'https://krasnodar.ginfo.ru/ulicy/'
url_districts_v1 = 'https://krasnodar.kitabi.ru/map/street'
url_districts_v2 = "https://youkarta.ru/krasnodarskij-kraj/krasnodar-23/"
url_coordinates = 'https://docs.mapbox.com/playground/geocoding/'

with open(r'files/addresses_v2.json', 'r') as openfile:
    j_object = json.load(openfile)


try:
    # pass
    # addresses = get_addresses(url_addresses)
    buildings_info = get_buildings_info(j_object, url_buildings_info)
    # districts = get_districts_v1(url_districts)
    # coordinates = get_coordinates(j_object, url_coordinates)
except Exception as e:
    print(e)


print("--- %s seconds ---" % ((time.time() - start_time) / 60))

