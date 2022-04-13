from bs4 import BeautifulSoup
import requests
import time

analyzeFile = 'jpost.txt'

f = open(analyzeFile)
urls = f.read().split()

session = requests.Session()

for u in urls:
  page = session.get(u)
  print(page.text)
  time.sleep(2)
