from bs4 import BeautifulSoup
import requests
import time
import cloudscraper
import spacy
from fake_useragent import UserAgent

import nltk
from nltk.corpus import sentiwordnet as swn
# nltk.download('punkt')
# nltk.download('sentiwordnet')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
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
nlp = spacy.load('en_core_web_lg')
# passivepy = PassivePy.PassivePyAnalyzer('en_core_web_sm')
print ("load")

palestinianWB = ['palestinian', 'palestinians', 'palestine', 'arab', 'arabs', 'west bank', 'gaza']
israeliWB = ['israeli', 'israelis', 'israel', 'jew', 'jews', 'settler', 'settlers', 'settlement', 'settlements', 'idf', 'i.d.f.']


hayom_palestinian_passive = []
hayom_israeli_passive = []
hayom_palestinian_active = []
hayom_israeli_active = []

def is_passive(sentDoc):
    tags = [token.dep_ for token in sentDoc]
    sents = list(sentDoc.sents)[0]

    if (any(['agent' in sublist for sublist in tags]) or any(['nsubjpass' in sublist for sublist in tags])):
        return (True, sents.root)

    if (sents.root.tag_ == "VBN"):
        return (True, sents.root)
    for w in sents.root.children:
        if (w.dep_ == "aux" and w.tag_ == "VBN"):
            return (True, w)

    return (False, None)
        

for page in hayom_text:
    sentences = nltk.sent_tokenize(page)

    assoc = {} 
    SUBJS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]

    for sent in sentences:
        sentDoc = nlp(sent)

        for token in sentDoc:
            if (token.dep_ in SUBJS):
                if (token.text not in assoc.keys()):
                    assoc[token.text] = set()

                for w in range(token.i+1, token.head.i):
                    assoc[token.text].add(sentDoc[w].text)

                for child in token.children:
                    assoc[token.text].add(child.text)

    for sent in sentences:
        sentDoc = nlp(sent)
        
        voice = is_passive(sentDoc)

        palestinian = False
        israeli = False
        

        if (voice[0]): 
            for token in sentDoc:
                if ((token.dep_ == "nsubjpass" or token.dep_ == "csubjpass")):
                    if (token.text.lower() in palestinianWB):
                        palestinian = True         
                    if (token.text.lower() in israeliWB):
                        israeli = True
                    if not palestinian and not israeli:
                        palestinian = any([w in assoc[token.text] for w in palestinianWB])
                        israeli = any([w in assoc[token.text] for w in israeliWB])

                    if palestinian or israeli:
                        if (token.head.pos_ == "VERB"):
                            synsets = swn.senti_synsets(token.head.text, 'v')
                        elif (token.head.pos_ == "ADJ"):
                            synsets = swn.senti_synsets(token.head.text, 'a')

                        words = list(synsets)
                        if len(words) > 1:
                            w = words[0]
                            obj = {
                                "pos_score": w.pos_score(),
                                "neg_score": w.neg_score(),
                                "obj_score": w.obj_score(),
                                "sentence": sent,
                                "subject": token.text,
                                "verb": token.head.text
                            }
                            if palestinian:
                                hayom_palestinian_passive.append(obj)
                            if israeli:
                                hayom_israeli_passive.append(obj)
        else:
            for token in sentDoc:
                if ((token.dep_ == "nsubj" or token.dep_ == "csubj")):
                    if (token.text.lower() in palestinianWB):
                        palestinian = True         
                    if (token.text.lower() in israeliWB):
                        israeli = True
                    if not palestinian and not israeli:
                        palestinian = any([w in assoc[token.text] for w in palestinianWB])
                        israeli = any([w in assoc[token.text] for w in israeliWB])

                    if palestinian or israeli:
                        if (token.head.pos_ == "VERB"):
                            synsets = swn.senti_synsets(token.head.text, 'v')
                        elif (token.head.pos_ == "ADJ"):
                            synsets = swn.senti_synsets(token.head.text, 'a')

                        words = list(synsets)
                        if len(words) > 1:
                            w = words[0]
                            obj = {
                                "pos_score": w.pos_score(),
                                "neg_score": w.neg_score(),
                                "obj_score": w.obj_score(),
                                "sentence": sent,
                                "subject": token.text,
                                "verb": token.head.text
                            }

                        if palestinian:
                            hayom_palestinian_active.append(obj)
                        if israeli:
                            hayom_israeli_active.append(obj)


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

print(len(hayom_palestinian_passive)/len(hayom_palestinian_active))
print(len(hayom_israeli_passive)/len(hayom_israeli_active))

print((sum(item['pos_score'] for item in hayom_palestinian_passive) - (sum(item['neg_score'] for item in hayom_palestinian_passive)))/len(hayom_palestinian_passive))
print((sum(item['pos_score'] for item in hayom_palestinian_active) - (sum(item['neg_score'] for item in hayom_palestinian_active)))/len(hayom_palestinian_active))

print((sum(item['pos_score'] for item in hayom_israeli_passive) - (sum(item['neg_score'] for item in hayom_israeli_passive)))/len(hayom_israeli_passive))
print((sum(item['pos_score'] for item in hayom_israeli_active) - (sum(item['neg_score'] for item in hayom_israeli_active)))/len(hayom_israeli_active))

print(sum(item['obj_score'] for item in hayom_palestinian_passive)/len(hayom_palestinian_passive))
print(sum(item['obj_score'] for item in hayom_palestinian_active)/len(hayom_palestinian_active))
print(sum(item['obj_score'] for item in hayom_israeli_passive)/len(hayom_israeli_passive))
print(sum(item['obj_score'] for item in hayom_israeli_active)/len(hayom_israeli_active))