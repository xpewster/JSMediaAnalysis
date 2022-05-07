from bs4 import BeautifulSoup
import requests
import time
import cloudscraper
import spacy
from fake_useragent import UserAgent

import nltk
from nltk.corpus import sentiwordnet as swn
# nltk.download('punkt')
# from PassivePySrc import PassivePy


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

print ("start")
nlp = spacy.load('en_core_web_sm')
# passivepy = PassivePy.PassivePyAnalyzer('en_core_web_sm')
print ("load")

palestinianWB = ['palestinian', 'palestinians', 'palestine', 'arab', 'arabs', 'west bank', 'gaza']
israeliWB = ['israeli', 'israelis', 'israel', 'jew', 'jews', 'settler', 'settlers', 'settlement', 'settlements']


hayom_palestinian_passive = []
hayom_israeli_passive = []
hayom_palestinian_active = []
hayom_israeli_active = []

for page in hayom_text:
    sentences = nltk.sent_tokenize(page)

    for sent in sentences:
        sentDoc = nlp(sent)
        tags = [token.dep_ for token in sentDoc]

        if (any(['agent' in sublist for sublist in tags]) or any(['nsubjpass' in sublist for sublist in tags])):
            
            for token in sentDoc:
                if ((token.dep_ == "nsubjpass" or token.dep_ == "csubjpass")):
                    if (token.text.lower() in palestinianWB):
                        hayom_palestinian_passive.append(sent)
                    elif (token.text.lower() in israeliWB):
                        hayom_israeli_passive.append(sent)
        else:
            for token in sentDoc:
                if ((token.dep_ == "nsubj" or token.dep_ == "csubj")):
                    if (token.text.lower() in palestinianWB):
                        hayom_palestinian_active.append(sent)
                    elif (token.text.lower() in israeliWB):
                        hayom_israeli_active.append(sent)

print("-----------palestinian passive:")
for s in hayom_palestinian_passive:
    print(s)
print("-----------israeli passive:")
for s in hayom_israeli_passive:
    print(s)
print("-----------palestinian active:")
for s in hayom_palestinian_active:
    print(s)
print("-----------israeli active:")
for s in hayom_israeli_active:
    print(s)
