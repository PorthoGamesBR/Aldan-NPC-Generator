from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys 
import time



class Whatsapp:
    def __init__(self) -> None:
        chr_service = Service("drivers/chromedriver.exe")
        self.driver = webdriver.Chrome(service=chr_service)

        self.driver.get("https://web.whatsapp.com")
        input("Read the QR code and print enter")
        print("Login complete!")
    
    def scroll_chat(self,scrolls=100):
        msg = self.driver.find_element_by_class_name("_1Gy50")
        body = self.driver.find_element_by_tag_name('body')
        body.click()
        for i in range(scrolls):           
            body.send_keys(Keys.HOME)
            time.sleep(0.05)
            #TODO:Adicionar trava para quando browser estiver carregando
        
def get_messages(whats : Whatsapp, contact : str) -> list:
    
    #Acha a barra de pesquisa e clica pra que ela pesquise
    inp_xpath_search = "//button[@aria-label='Pesquisar ou começar uma nova conversa']"
    input_box_search = WebDriverWait(whats.driver,50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
    input_box_search.click()
    
    #Espera um tempo para que o site carregue e coloca o que precisa ser pesquisado
    time.sleep(4)
    input_box_search.send_keys(contact)
    time.sleep(4)
    
    #Abre a conversa
    selected_contact = whats.driver.find_element_by_xpath("//span[@title='"+contact+"']")
    selected_contact.click()
    
    #Carrega mais mensagens da conversa
    whats.scroll_chat(100)
    
    #Abre todas as mensagens com "ler mais" e pega o conteudo delas, convertendo para texto
    msg_class_name = "_1Gy50"
    ler_mais_xpath = "//span[@class='_208p2']"
    message_list = whats.driver.find_elements_by_class_name(msg_class_name)
    lm_list = whats.driver.find_elements_by_xpath(ler_mais_xpath)
    message_text_list = []
    
    for lm in lm_list:
        lm.click()
    for m in message_list:
        #Encode para UTF8 por que as mensagens podem ter emojis
        message_text_list.append(m.text.encode('utf8'))
    

    