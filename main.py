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

with open(r'files/buildings_info.json', 'r') as openfile:
    b_object = json.load(openfile)

try:
    # pass
    # addresses = get_addresses(url_addresses)
    buildings_info = get_buildings_info(j_object, url_buildings_info)
    # districts = get_districts_v1(url_districts)
    # coordinates = get_coordinates(j_object, url_coordinates)
except Exception as e:
    print(e)

"""unic_num = []
for k, v in j_object.items():
    # print(f'-----------------------------{k}-----------------------------')
    for s, n in v.items():
        for i in n:
            if i not in unic_num:
                unic_num.append(i)

print()

unic_num = {}
unic_key = []

not_null = 0
null = 0
for k, v in b_object.items():
    print()
    print(f'-----------------------------{k}-----------------------------')
    print()
    for s, n in v.items():
        if n:
            for i, j in n.items():
                if i not in unic_num:
                    unic_num[i] = s
                # print(f'{s} {i}:   {j}')
            not_null += 1
        else:
            null += 1
print(not_null, null)
for i, j in sorted(unic_num.items(), key=lambda x: (len(x[0]))):
    if '(' in i:
        print(f'{j} - {i}')"""


print("--- %s seconds ---" % ((time.time() - start_time)/60))
