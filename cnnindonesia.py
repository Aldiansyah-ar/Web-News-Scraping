import requests
import pandas as pd
from bs4 import BeautifulSoup
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

def cnn_indonesia_page(date, month, year):
  url = f'https://www.cnnindonesia.com/nasional/indeks/3/1?date={year}/{month}/{date}'
  text = requests.get(url, user_agent).text
  sop = BeautifulSoup(text, 'lxml')
  try:
    last_page = sop.find_all('a','text-cnn_black dark:text-white inline-flex items-center justify-center w-[30px] h-[30px] rounded-md hover:bg-cnn_grey dark:hover:bg-cnn_black')[-1].text
  except:
    last_page = 1
  return last_page

def scrape_cnn_indonesia(date, month, year, file_name):
    global user_agent
    last_page = cnn_indonesia_page(date, month, year)
    data = []
    id = 0
    for page in range(1,int(last_page)+1):
        url = f'https://www.cnnindonesia.com/nasional/indeks/3/{page}?date={year}/{month}/{date}'
        text = requests.get(url,user_agent).text
        soup = BeautifulSoup(text)
        articles_container = soup.find_all('article', class_='flex-grow')
        print(f'page: {page}')
        for article in articles_container:
            try:
              link = article.find('a')['href']
              headline = article.find('span', class_='flex-grow').find('h2').text
              news = requests.get(link,user_agent).text
              news_soup = BeautifulSoup(news, 'lxml')
              date_ = news_soup.find('div', class_='text-cnn_grey text-sm mb-4').text
              content_container = news_soup.find('div', class_='detail-text text-cnn_black text-sm grow min-w-0')
              contents = content_container.find_all('p')
              location = content_container.find('strong').text
              text = []
              for x in contents:
                y = x.text
                text.append(y)
                content = ' '.join(text).replace('ADVERTISEMENT','').replace('SCROLL TO CONTINUE WITH CONTENT','').replace('\r\n    \r\n \r\n    \r\n','')

              id += 1
              content = location + ' -- ' + content
              print(f'article: {id}')
              data.append({'id': id,
                          'source': 'CNN Indonesia',
                          'title': headline, 
                          'url': link,
                          'content': content, 
                          'date': date_})
            except:
              pass

    df = pd.DataFrame(data)
    df.to_csv(f'./{file_name}', index=False)

scrape_cnn_indonesia('12', '05', '2024', 'cnnindonesia.csv')