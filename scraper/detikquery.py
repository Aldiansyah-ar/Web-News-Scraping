import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup as bs
from datetime import datetime
hades = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def detik_page(query, category_id, start_date, end_date):
  url = f'https://www.detik.com/search/searchnews?query={query}&siteid={category_id}&sortby=time&sorttime=1&fromdatex={start_date}&todatex={end_date}&result_type=latest'
  text = requests.get(url, hades).text
  sop = bs(text)

  try:
    paging = sop.find_all('div','pagination text-center mgt-16 mgb-48')[0].find_all('a')[-2]
    last_page = paging.text
  except:
    last_page = 1

  return last_page

def scrape_detik(query, category_id, start_date, end_date, file_name):
    global hades
    count = 0
    last_page = detik_page(query, category_id, start_date, end_date)

    with open(f'{file_name}', 'a') as file:
      header = ['headline', 'date']
      wr = csv.writer(file, delimiter=',')
      wr.writerow(header)

    for page in range(1,int(last_page)+1):
        url = f'https://www.detik.com/search/searchnews?query={query}&siteid={category_id}&sortby=time&sorttime=1&fromdatex={start_date}&todatex={end_date}&result_type=latest&page={page}'
        text = requests.get(url,hades).text
        soup = bs(text, 'lxml')
        articles_container = soup.find_all('article',class_='list-content__item')
        print(f'done_page[{page}]')
        for article in articles_container:
            date = article.find('div', 'media__date').find('span').text
            headline = article.find('div', 'media__text').find('a').text
            count += 1
            with open(f'{file_name}','a') as file:
              wr = csv.writer(file, delimiter=',')
              wr.writerow([headline,date])

    print("Total scrapping article:", count)

scrape_detik('Rafah', 3, '28/05/2024', '10/06/2024', 'rafah.csv')