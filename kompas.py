import requests
import pandas as pd
from bs4 import BeautifulSoup
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def kompas_page(date, month, year):
  url = f'https://indeks.kompas.com/?site=nasional&date={year}-{month}-{date}&page=1'
  text = requests.get(url, user_agent).text
  soup = BeautifulSoup(text, 'lxml')
  try:
    last_page = soup.find('a','paging__link paging__link--last')['data-ci-pagination-page']
  except:
    last_page = 1
  return last_page

def scrape_kompas(date, month, year, file_name):
    global hades
    last_page = kompas_page(date, month, year)
    data = []
    id = 0
    for page in range(1,int(last_page)+1):
        url = f'https://indeks.kompas.com/?site=nasional&date={year}-{month}-{date}&page={page}'
        text = requests.get(url,user_agent).text
        soup = BeautifulSoup(text)
        articles_container = soup.find_all('div', class_='articleItem')
        print(f'page: {page}')
        for article in articles_container:
            id += 1
            link = article.find('a', class_='article-link')['href']
            headline = article.find('h2').text
            news = requests.get(link,user_agent).text
            news_soup = BeautifulSoup(news)
            date_ = news_soup.find('div', class_='read__time').text
            content_container = news_soup.find('div', class_='read__content')
            contents = content_container.find_all('p')
            text = []
            for x in contents:
                y = x.text
                text.append(y)
                content = ' '.join(text)

            print(f'article: {id}')
            data.append({'id': id,
                         'source': 'kompas',
                         'title': headline, 
                         'url': link,
                         'content': content, 
                         'date': date_})
    
    df = pd.DataFrame(data)
    df.to_csv(f'./file/{file_name}', index=False)

scrape_kompas('31','07','2024', 'kompas.csv')