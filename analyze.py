from bs4 import BeautifulSoup
import requests
import time
import cloudscraper
from fake_useragent import UserAgent


MAX_ITER = 50 # for testing
analyzeFile = 'jpost.txt'

session = cloudscraper.create_scraper()

# ------- Jerusalem Post ------- #

jpost_text = []
test = False

f = open(analyzeFile)
urls = f.read().split()

i = 0
for u in urls:
    if (i >= MAX_ITER or not test):
        break
    i = i+1
    page = session.get(u)
    soup = BeautifulSoup(page.text.replace("<div class='fake-br-for-article-body'></div>", " "), 'html.parser')

    div = soup.find(class_='article-inner-content')
    jpost_text.append(div.get_text().strip())

    time.sleep(2)

# ------- Haaretz ------- #

analyzeFile = 'haaretz.txt'
test = False

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
ua = UserAgent()
hdr = {'User-Agent': ua.random,
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
      'Accept-Encoding': 'none',
      'Accept-Language': 'en-US,en;q=0.8',
      'Connection': 'keep-alive'}


haaretz_text = []

f = open(analyzeFile)
urls = f.read().split()

i = 0
skip = False
for u in urls:
    if (i >= MAX_ITER or not test):
        break
    i = i+1
    if (skip):
        skip = False
        continue
    page = session.get(u, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(page.text)

    # div = soup.find(attrs={'data-test': 'articleBody'})
    div = soup.find(id='article-entry')
    # print(div.get_text().strip().split('Send me email alerts')[0])
    haaretz_text.append(div.get_text().strip().split('Send me email alerts')[0])

    time.sleep(2)

    skip = True

# ------- Israel Hayom ------- #

analyzeFile = 'hayom_pages.txt'
test = True

hayom_text = []

f = open(analyzeFile)


pages = ['<!doctype html>'+p for p in f.read().split('<!doctype html>') if p.strip()]

for p in pages:
    soup = BeautifulSoup(p, 'html.parser')

    div = soup.find(attrs={'class': 'content-inner'})
    text = div.get_text().replace('Follow Israel Hayom on Facebook and Twitter', '').strip()
    text = text.split('Subscribe to Israel Hayom')[0]
    hayom_text.append(text)


# ANALYSIS



