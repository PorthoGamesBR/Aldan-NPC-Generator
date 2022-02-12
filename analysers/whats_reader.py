from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time



class Whatsapp:
    def __init__(self) -> None:
        chr_service = Service("drivers/chromedriver.exe")
        self.driver = webdriver.Chrome(service=chr_service)

        self.driver.get("https://web.whatsapp.com")
        input("Read the QR code and print enter")
        print("Login complete!")
    
    def scroll_chat(self,scrolls=100):
        #Need to scroll the chat
        pass
        
def get_messages(whats : Whatsapp, contact : str) -> list:
    
    inp_xpath_search = "//button[@aria-label='Pesquisar ou começar uma nova conversa']"
    input_box_search = WebDriverWait(whats.driver,50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
    input_box_search.click()
    
    time.sleep(2)
    input_box_search.send_keys(contact)
    time.sleep(4)
    
    selected_contact = whats.driver.find_element_by_xpath("//span[@title='"+contact+"']")
    selected_contact.click()
    
    #_1Gy50
    

    