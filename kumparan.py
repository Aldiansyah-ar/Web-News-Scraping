from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

driver = webdriver.Chrome()
url = "https://kumparan.com/topic/indeks"
driver.get(url)

def scroll_down():
    time.sleep(2)
    previous_height = driver.execute_script("return document.body.scrollHeight;")

    while True:
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight;")
        if new_height == previous_height:
            break
        else:
            previous_height = new_height

# def kumparan_page(link):
#     driver = webdriver.Chrome()
#     driver.get(link)
#     time.sleep(2)
#     news_soup = BeautifulSoup(driver.page_source, 'lxml')
#     content_container = news_soup.select_one("div[class*='StoryRenderer__EditorWrapper-sc-1f9fbz3-0 ghydBU']")
#     contents = content_container.select("span[data-qa-id*='story-paragraph']")
#     text = []
#     for x in contents:
#         y = x.text
#         text.append(y)
#         content = ' '.join(text)

#     print(content)

def scrape_kumparan(file_name):
    scroll_down()
    soup = BeautifulSoup(driver.page_source, "html.parser")
    containers = soup.find_all('div', style="width:100%")
    containers_ = soup.find_all('div', style="width: 100%;")
    data = []
    id = 0
    for container in containers:
        id += 1
        headline = container.find('a').find('span').text
        date = container.select_one("span[data-qa-id*='card-footer-date']").text
        link = container.find('a')['href']
        link = 'https://kumparan.com' + link
        data.append({'id': id, 
                     'source': 'kumparan', 
                     'title': headline,
                     'url': link, 
                     'content': None, 
                     'date': date})

    for container_ in containers_:
        id += 1
        headline_ = container_.find('a').find('span').text
        date_ = container_.select_one("span[data-qa-id*='card-footer-date']").text
        link_ = container.find('a')['href']
        link_ = 'https://kumparan.com' + link_
        data.append({'id': id, 
                     'source': 'kumparan', 
                     'title': headline_,
                     'url': link_,
                     'content': None, 
                     'date': date_})

    df = pd.DataFrame(data)
    df.to_csv(f'./file/{file_name}', index=False)

    driver.quit()

scrape_kumparan('kumparan.csv')
