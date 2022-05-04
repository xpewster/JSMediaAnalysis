# from bs4 import BeautifulSoup
# import requests

URL = 'https://www.jpost.com/jpost-search-page#/search;query=settlements;sortBy=_score;isDesc=1;resultCount=24;layout=Rows/advanced'
chromedriver_path = r'./chromedriver'
scrolls = 50

# page = requests.get(URL)

# print(page.text)

import os
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

if (not os.path.exists(chromedriver_path)):
    print("chromedriver not found")

s = Service(chromedriver_path)

browser = webdriver.Chrome(executable_path=chromedriver_path)
browser.get(URL)
time.sleep(4)

showmore_button = browser.find_element_by_xpath('/html/body/zoomd-widget-root/zd-widget/div/div[2]/div/zoomd-search-results[2]/section/button')
showmore_button.click()
# print("show more")
time.sleep(2)

s = 0
while s < scrolls:
    # print("scroll")
    # Scroll down to bottom
    browser.find_element_by_tag_name('body').send_keys(Keys.END)
    # Wait to load page
    time.sleep(2)
    s = s+1

links = browser.find_elements_by_css_selector("a[aria-label*='Go to the article']")
urls = map(lambda x: x.get_attribute('href'), links)

for u in urls:
    print(u)
# print(browser.page_source)