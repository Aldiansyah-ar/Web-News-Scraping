import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
hades = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def kompas_page(date, month, year):
  url = f'https://indeks.kompas.com/?site=nasional&date={year}-{month}-{date}&page=1'
  text = requests.get(url, hades).text
  soup = BeautifulSoup(text, 'lxml')

  try:
    last_page = soup.find('a','paging__link paging__link--last')['data-ci-pagination-page']
  except:
    last_page = 1

  return last_page

def scrape_kompas(date, month, year):
    global hades
    count = 0
    last_page = kompas_page(date, month, year)

    data = []

    for page in range(1,int(last_page)+1):
        url = f'https://indeks.kompas.com/?site=nasional&date={year}-{month}-{date}&page={page}'
        text = requests.get(url,hades).text
        soup = BeautifulSoup(text)
        articles_container = soup.find_all('div', class_='articleItem')
        print(f'done_page[{page}]')
        for article in articles_container:
            link = article.find('a', class_='article-link')['href']
            headline = article.find('h2').text
            # date = f'{date}/{month}/{year}'
            data.append({'title': headline, 'link': link})
            count += 1
    
    print(len(data))
    print("total scrapping article: ", count)

scrape_kompas('31','07','2024')