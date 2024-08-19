import requests
import pandas as pd
from bs4 import BeautifulSoup
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def scrape_tempo(date, month, year, file_name):
    global user_agent
    data = []
    id = 0
    url = f'https://www.tempo.co/indeks/{year}-{month}-{date}/nasional'
    text = requests.get(url,user_agent).text
    soup = BeautifulSoup(text, 'lxml')
    articles_container = soup.find_all('div', class_='card-box ft240 margin-bottom-sm')
    for article in articles_container:
        id += 1
        link = article.find('a')['href']
        headline = article.find('h2', class_='title').text
        news = requests.get(link,user_agent).text
        news_soup = BeautifulSoup(news, 'lxml')
        date_ = news_soup.find('p', class_='date margin-bottom-sm').text
        text = []
        for page in range(1,3):
          link_ = link + f'?page_num={page}'
          news_ = requests.get(link_,user_agent).text
          news_soup_ = BeautifulSoup(news_, 'lxml')
          content_container = news_soup_.find('div', class_='detail-konten')
          contents = content_container.find_all('p')
          for x in contents:
            y = x.text
            text.append(y)
            content = ' '.join(text)

          content = content.replace('12','').replace('\n','')

        print(f'article: {id}')
        data.append({'id': id,
                     'source': 'Tempo',
                     'title': headline, 
                     'url': link,
                     'content': content, 
                     'date': date_})
    
    df = pd.DataFrame(data)
    df.to_csv(f'./{file_name}', index=False)

scrape_tempo('08', '08', '2024', 'tempo.csv')