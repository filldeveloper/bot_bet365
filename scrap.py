import config
from functions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pprint import pprint
from time import sleep
from datetime import datetime

today = datetime.today().strftime('%d-%m-%Y %H:%M')
time_execution = today.split(' ')[1]
time_execution = time_execution.split(':')[1]
date = today.split(' ')[0]

LOGIN = config.login
PASSWORD = config.password

hour_table = [
    '02', '05', '08', '11', '14', '17', '20', '23', '26', '29',
    '32', '35', '38', '41', '44', '47', '50', '53', '56', '59'
    ]

url = 'https://bbtips.com.br/login'
PATH_DRIVER = './chromedriver'

# Navegador no modo oculto
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')

chrome = webdriver.Chrome(PATH_DRIVER, 
                            #options=options
)
chrome.get(url)
sleep(5)

# Digitar o email e password
chrome.find_element(By.ID, 'email').send_keys(LOGIN)
chrome.find_element(By.ID, 'password').send_keys(PASSWORD, Keys.ENTER)
sleep(6)

# Acessar o quadro de resultados do Futebol
chrome.find_element(By.CLASS_NAME, 'fa-futbol-o').click()
sleep(3)

# table = chrome.find_elements(
#     By.TAG_NAME, 'tbody'
#     )
# Testes preliminares com a Euro
# Lógica onde será definido qual metade dos resultados o script irá avaliar
# Código será efetuado 05 minutos de toda hora
if int(time_execution) < 15:
    results = get_results(chrome, 2)
    sleep(1)
    # Pegar a hora da linha de aposta mais recente
    hour = results[0].find_element(By.CLASS_NAME, 'dfHorarios')
    text_hour = outer_html(hour)

    # Pegar os resultados e tentar filtrar somente o último resultado
    count = 10
    results = results[0].find_elements(By.CLASS_NAME, 'resultado')

    for result in results[10:]:
        text_result = outer_html(result)
        if text_result == '1-3':
            hour = f'{text_hour.strip()}:{hour_table[count]}'
            print(f'{text_result} as {hour}')
            unique_key = f'{date}{text_result}{hour}EURO'
            dados = (date, text_result, hour, 'EURO', unique_key)
            try:
                feed_table(dados)
            except:
                print('Valor existente')

        count += 1
# Código será efetuado 35 minutos de toda hora
else:
    results = get_results(chrome, 1)
    sleep(1)
    # Pegar a hora da linha de aposta mais recente
    hour = results[0].find_element(By.CLASS_NAME, 'dfHorarios')
    text_hour = outer_html(hour)

    # Pegar os resultados e tentar filtrar somente o último resultado
    count = 0
    results = results[0].find_elements(By.CLASS_NAME, 'resultado')

    for result in results[:10]:
        text_result = outer_html(result)
        if text_result == '1-3':
            hour = f'{text_hour.strip()}:{hour_table[count]}'
            print(f'{text_result} as {hour}')
            unique_key = f'{date}{text_result}{hour}EURO'
            dados = (date, text_result, hour, 'EURO', unique_key)
            try:
                feed_table(dados)
            except:
                print('Valor existente')

        count += 1


sleep(10)
chrome.close()