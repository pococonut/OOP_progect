import json
import time
from districts import get_districts_v1
from addresses import get_addresses
from buildings_info import get_buildings_info

start_time = time.time()

url_buildings_info = 'https://аис.фрт.рф'
url_addresses = 'https://krasnodar.ginfo.ru/ulicy/'
url_districts_v1 = 'https://krasnodar.kitabi.ru/map/street'
url_districts_v2 = "https://youkarta.ru/krasnodarskij-kraj/krasnodar-23/"

with open(r'files/districts_v1.json', 'r') as openfile:
    j_object1 = json.load(openfile)

with open(r'files/districts_v2.json', 'r') as openfile:
    j_object2 = json.load(openfile)

try:
    pass
    # addresses = get_addresses(url_addresses)
    #buildings_info = get_buildings_info(j_object, url_buildings_info)
    # districts = get_districts_v1(url_districts)
except Exception as e:
    print(e)

s1 = s2 = 0

for k, v in j_object1.items():
    s1 += len(v)

for k, v in j_object2.items():
    s2 += len(v)

print(s1, s2)
print("--- %s seconds ---" % ((time.time() - start_time)/60))

#233 #289