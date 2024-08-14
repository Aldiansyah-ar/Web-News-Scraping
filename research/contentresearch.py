import requests
import pandas as pd
from bs4 import BeautifulSoup
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

link = f'https://news.detik.com/berita/d-7468912/menpan-rb-ungkap-3-upaya-penguatan-pengelolaan-pusat-data-nasional'
news = requests.get(link,user_agent).text
news_soup = BeautifulSoup(news, 'lxml')
date = news_soup.find('div', class_='detail__date').text
content_container = news_soup.find('div', class_='detail__body-text itp_bodycontent')
location = content_container.find('strong').text
contents = content_container.find_all('p', class_='')
text = []
for x in contents:
    y = x.text
    text.append(y)
    content = ' '.join(text).replace('ADVERTISEMENT','').replace('SCROLL TO RESUME CONTENT','')

content = location + ' - ' + content

print(content)
print(date)