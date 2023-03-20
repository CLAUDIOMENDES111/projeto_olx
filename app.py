from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from time import sleep

#import pyautogui

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1300,1000', '--incognito'] #,'--headless']
    for argument in arguments:
        chrome_options.add_argument(argument)
 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1
    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
 
    return driver
 
 
driver = iniciar_driver()
#driver.get('https://www.olx.com.br/estado-df?q=monitor')
#driver.get('https://www.olx.com.br/hobbies-e-colecoes/estado-df?q=HONDA%20CIVIC')
driver.get('https://www.olx.com.br/hobbies-e-colecoes/estado-df?q=cole%C3%A7%C3%A3o%20de%20cartoes%20telef%C3%B4nicos')
while True:

    sleep(30)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(2)
    #driver.maximize_window()

    titulos = driver.find_elements(By.XPATH,"//div[@class='sc-12rk7z2-7 kDVQFY']//h2")
    precos = driver.find_elements(By.XPATH,'//span[@class="m7nrfa-0 eJCbzj sc-ifAKCX jViSDP"]')
    links = driver.find_elements(By.XPATH,'//a[@data-lurker-detail="list_id"]')

    for titulo, preco, link in zip(titulos,precos,links):
        with open('colecao.csv','a', encoding='utf-8', newline='') as arquivo:
            link_processado = link.get_attribute('href')
            arquivo.write(f'{titulo.text};{preco.text};{link_processado}{os.linesep}')
    try:
        botao_proxima_pagina = driver.find_element(By.XPATH,'//span[text()="Próxima pagina"]')
        sleep(3)
        botao_proxima_pagina.click()
    except:
        print('Chegamos na última página!')
        break


input('')

driver.close() # Fecha janela atual
