import json
import os
import time
from selenium import webdriver as wd


def browser_connect(url):
    browser = wd.Chrome()
    browser.get(url)
    browser.implicitly_wait(15)
    time.sleep(10)
    return browser


def get_dict(path):
    if os.path.exists(path):
        with open(path, 'r') as json_file:
            dict_res = json.load(json_file)
    else:
        dict_res = {}
    return dict_res
