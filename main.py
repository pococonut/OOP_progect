import json
import time
from districts import get_districts
from addresses import get_addresses
from buildings_info import get_buildings_info

start_time = time.time()

url_buildings_info = 'https://аис.фрт.рф'
url_addresses = 'https://krasnodar.ginfo.ru/ulicy/'
url_districts = 'https://krasnodar.kitabi.ru/map/street'


with open('files/streets.json', 'r') as openfile:
    j_object = json.load(openfile)

try:
    # addresses = get_addresses(url_addresses)
    # buildings_info = get_buildings_info(j_object, url_buildings_info)
    districts = get_districts(url_districts)
except Exception as e:
    print(e)

"""for k, v in j_object.items():
    print(f'\n{k}:  {v}\n')"""


print("--- %s seconds ---" % ((time.time() - start_time)/60))
