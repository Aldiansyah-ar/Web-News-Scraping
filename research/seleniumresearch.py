from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

url = 'https://webscraper.io/test-sites/e-commerce/more/computers/laptops'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
time.sleep(2)

# while True:
for i in range(10):
    time.sleep(2)
    try:
        element = driver.find_element(By.LINK_TEXT, "More")
        element.click()
        time.sleep(2)
    except NoSuchElementException:
        break