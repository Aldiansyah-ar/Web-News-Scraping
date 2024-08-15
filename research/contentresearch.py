import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

from selenium import webdriver

driver = webdriver.Chrome()
link = f'https://kumparan.com/kumparanbisnis/indeks-manufaktur-ri-turun-ke-49-3-fase-terendah-sejak-agustus-2021-23EzXLY668X/2'
driver.get(link)
time.sleep(2)
news_soup = BeautifulSoup(driver.page_source, 'lxml')

# date = news_soup.find('div', class_='detail__date').text
content_container = news_soup.select_one("div[class*='StoryRenderer__EditorWrapper-sc-1f9fbz3-0 ghydBU']")
contents = content_container.select("span[data-qa-id*='story-paragraph']")
text = []
for x in contents:
    y = x.text
    text.append(y)
    content = ' '.join(text)

print(content)