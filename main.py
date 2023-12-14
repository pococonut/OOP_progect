import json
import time
from coordinates import get_coordinates
from districts import get_districts_v1
from addresses import get_addresses
from buildings_info import get_buildings_info, get_buildings_info_domreestr

start_time = time.time()

url_buildings_info = 'https://аис.фрт.рф/myhouse'
url_buildings_info_domreesrt = 'https://domreestr.ru/'
url_addresses = 'https://krasnodar.ginfo.ru/ulicy/'
url_districts_v1 = 'https://krasnodar.kitabi.ru/map/street'
url_districts_v2 = "https://youkarta.ru/krasnodarskij-kraj/krasnodar-23/"
url_coordinates = 'https://docs.mapbox.com/playground/geocoding/'

with open(r'files/full_addresses.json', 'r') as openfile:
    j_object = json.load(openfile)

with open(r'files/coordinates.json', 'r') as openfile:
    c_object = json.load(openfile)

with open("files/buildings_info_domreestr.json", 'r') as openfile:
    b_object = json.load(openfile)

try:
    pass
    # addresses = get_addresses(url_addresses)
    # buildings_info = get_buildings_info(j_object, url_buildings_info)
    # districts = get_districts_v1(url_districts)
    coordinates = get_coordinates(j_object, url_coordinates)
    # buildings_info_dr = get_buildings_info_domreestr(j_object, url_buildings_info_domreesrt)

except Exception as e:
    print(e)

# 6232
# 7367

# 1707 - улиц в координатах, 1571 - в домах
# 80000, 7367

addr_coord = []
c = 0
for k, v in c_object.items():
    addr_coord.append([k, v])
    print(k, v)
    c += 1
print(len(addr_coord))

"""c = 0
addr_build = {}
for k, v in b_object.items():
    for i, j in v.items():
        # print(i, n)
        if j:
            nums = []
            for n in j:
                nums.append(n)
            addr_build[i] = nums
                #print(i, n)

for i, j in addr_build.items():
    print(i, j)
print(len(addr_build))"""

"""with open('files/full_addresses.json', 'w') as outfile:
    json.dump(addr_build, outfile)"""

# 497 непустых улиц
"""c = 0
for s1 in addr_build:
    for s2 in addr_coord:
        if s1[0] == s2[0] and s1[1]:
            print(s1[0])
            num1 = sorted([n for n in s1[1]])
            num2 = sorted([n for n in s2[1]])
            print(len(num1), num1)
            print(len(num2), num2)
            print()
            c += len(num1)
print(c)"""

# print("--- %s seconds ---" % ((time.time() - start_time) / 60))
