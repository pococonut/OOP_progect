import json
import time
from get_addresses import get_addresses
from get_buildings_info import get_buildings_info

start_time = time.time()

url_buildings_info = 'https://аис.фрт.рф'
url_addresses = 'https://krasnodar.ginfo.ru/ulicy/'


with open('streets.json', 'r') as openfile:
    streets_object = json.load(openfile)

get_buildings_info(streets_object, url_buildings_info)
addresses = get_addresses(url_addresses)

for k, v in addresses.items():
    print(f'\n{k}:  {v}\n')

with open('streets.json', 'w') as outfile:
    json.dump(addresses, outfile)

print("--- %s seconds ---" % ((time.time() - start_time)/60))
