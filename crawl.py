# from bs4 import BeautifulSoup
# import requests

URL = 'https://www.jpost.com/jpost-search-page#/search;query=settlements;sortBy=_score;isDesc=1;resultCount=24;layout=Rows/advanced'
chromedriver_path = r'/usr/bin/chromedriver'

# page = requests.get(URL)

# print(page.text)

import os
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

if (not os.path.exists(chromedriver_path)):
    print("chromedriver not found")

s = Service(chromedriver_path)

browser = webdriver.Chrome(service=s)
browser.get(URL)
time.sleep(2)

print(browser.page_source)