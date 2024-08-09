from selenium import webdriver
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
url = 'https://olx.co.id'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)

# while True:
for i in range(4):
    time.sleep(2)
    try:
        element = driver.find_element(By.CLASS_NAME, "rui-apowA.rui-htytx.rui-UGVY0")
        element.click()
        time.sleep(1)
    except NoSuchElementException:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")