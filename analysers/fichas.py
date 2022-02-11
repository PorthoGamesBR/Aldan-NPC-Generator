from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

chr_service = Service("drivers/chromedriver.exe")
driver = webdriver.Chrome(service=chr_service)
driver.get("https://google.com")
time.sleep(10)
driver.close()
