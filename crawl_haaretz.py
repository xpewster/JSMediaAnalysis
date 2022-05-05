# from bs4 import BeautifulSoup
# import requests

URL = 'https://www.haaretz.com/misc/tags/TAG-israel-settlements-1.5598942'
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



s = 0
while s < scrolls:
    # print("scroll")
    # Scroll down to bottom
    browser.find_element_by_tag_name('body').send_keys(Keys.END)
    # Wait to load page
    time.sleep(2)
    # Load more
    showmore_button = browser.find_elements_by_xpath('/html/body/div[1]/div[4]/main/section[3]/div[2]/div/button')
    if (len(showmore_button) > 0):
        showmore_button[0].click()
    else:
        break
    # print("show more")
    time.sleep(2)
    
    s = s+1

links = browser.find_elements_by_css_selector("a[href*='/israel-news/']")
urls = map(lambda x: x.get_attribute('href'), links)

for u in urls:
    print(u)
# print(browser.page_source)