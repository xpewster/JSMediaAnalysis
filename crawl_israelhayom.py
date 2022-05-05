# import requests
# from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# ua=UserAgent()
# hdr = {'User-Agent': ua.random,
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#       'Accept-Encoding': 'none',
#       'Accept-Language': 'en-US,en;q=0.8',
#       'Connection': 'keep-alive'}

URL = 'https://www.israelhayom.com/tag/settlements/'
chromedriver_path = r'./chromedriver'
scrolls = 50

# data = requests.get(URL)
# page = BeautifulSoup('html.parser', data.text)

# print(page.text)

import os
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

import time

if (not os.path.exists(chromedriver_path)):
    print("chromedriver not found")

s = Service(chromedriver_path)

options = webdriver.ChromeOptions();
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option('useAutomationExtension', False)

print("a")
browser = uc.Chrome()
print("b")
browser.get(URL)
time.sleep(8)

urls = []

s = 0
while s < scrolls:
    links = browser.find_elements_by_css_selector("h3[class='jeg_post_title']")
    batch_urls = map(lambda x: x.find_element("a").get_attribute('href'), links)
    urls.append(batch_urls)

    # next batch
    showmore_button = browser.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[1]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/a[3]')
    showmore_button.click()
    time.sleep(2)

    s = s+1

links = browser.find_elements_by_css_selector("a[aria-label*='Go to the article']")
urls = map(lambda x: x.get_attribute('href'), links)

for u in urls:
    print(u)
# print(browser.page_source)