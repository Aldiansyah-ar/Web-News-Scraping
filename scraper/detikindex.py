import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup as bs
from datetime import datetime
hades = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def detik_index_page(tanggal):
  url = f'https://news.detik.com/berita/indeks/1?date={tanggal}'
  text = requests.get(url, hades).text
  sop = bs(text)

  try:
    paging = sop.find_all('div','pagination text-center mgt-16 mgb-16')[0].find_all('a')[-2]
    last_page = paging.text
    if last_page == '':
      last_page = 1
  except:
    last_page = 1

  return last_page

def scrape_index_detik(tanggal, file_name):
    global hades
    count = 0
    last_page = detik_index_page(tanggal)

    with open(f'{file_name}', 'a') as file:
      header = ['headline', 'date']
      wr = csv.writer(file, delimiter=',')
      wr.writerow(header)

    for page in range(1,int(last_page)+1):
        url = f'https://news.detik.com/berita/indeks/{page}?date={tanggal}'
        text = requests.get(url,hades).text
        soup = bs(text)
        articles_container = soup.find_all('article',class_='list-content__item')
        print(f'done_page[{page}]')
        for article in articles_container:
            date = article.find('div', 'media__date').find('span').text
            headline = article.find('div', 'media__text').find('a').text
            count += 1
            with open(f'{file_name}','a') as file:
              wr = csv.writer(file, delimiter=',')
              wr.writerow([headline,date])

    print("total scrapping article: ", count)

scrape_index_detik('2024-05-12', 'test4.csv')