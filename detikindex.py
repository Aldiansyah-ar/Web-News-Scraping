import requests
import pandas as pd
from bs4 import BeautifulSoup
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def detik_index_page(date, month, year):
  global user_agent
  url = f'https://news.detik.com/berita/indeks/1?date={year}-{month}-{date}'
  text = requests.get(url, user_agent).text
  sop = BeautifulSoup(text, 'lxml')
  try:
    paging = sop.find('div','pagination text-center mgt-16 mgb-16').find_all('a')[-2]
    last_page = paging.text
  except:
    last_page = 1
  return last_page

def scrape_index_detik(date, month, year, file_name):
    global user_agent
    last_page = detik_index_page(date, month, year)
    data = []
    id = 0
    for page in range(1,int(last_page)+1):
        url = f'https://news.detik.com/berita/indeks/{page}?date={year}-{month}-{date}'
        text = requests.get(url,user_agent).text
        soup = BeautifulSoup(text, 'lxml')
        articles_container = soup.find_all('article', class_='list-content__item')
        print(f'page: {page}')
        for article in articles_container:
            id += 1
            headline = article.find('div', 'media__text').find('a').text
            link = article.find('div', 'media__text').find('a')['href']
            news = requests.get(link,user_agent).text
            news_soup = BeautifulSoup(news, 'lxml')
            date_ = news_soup.find('div', class_='detail__date').text
            content_container = news_soup.find('div', class_='detail__body-text itp_bodycontent')
            location = content_container.find('strong').text
            contents = content_container.find_all('p', class_='')
            text = []
            for x in contents:
                y = x.text
                text.append(y)
                content = ' '.join(text).replace('ADVERTISEMENT','').replace('SCROLL TO RESUME CONTENT','')
            
            print(f'article: {id}')                
            content = location + ' - ' + content
            data.append({'id': id,
                         'source': 'Detik',
                         'title': headline, 
                         'url': link,
                         'content': content, 
                         'date': date_})
        
    df = pd.DataFrame(data)
    df.to_csv(f'./file/{file_name}', index=False)

scrape_index_detik('12', '05', '2024', 'detikindex.csv')