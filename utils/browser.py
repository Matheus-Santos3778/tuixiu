from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import ast
import time
from utils import general

def get_driver(base):
    link = "https://sistema.soc.com.br/WebSoc/"
    chrome_options = Options()
    options_list = [
    #    '--headless', 
        '--no-sandbox', 
        '--disable-dev-shm-usage', 
        '--start-maximized', 
        'log-level=3', 
        '--lang=pt-BR',
        '--enable-unsafe-swiftshader'
        ]
    #'--window-size=1920x1080',

    for x in options_list:
        chrome_options.add_argument(x)
    
    prefs = {
    "profile.default_content_setting_values.notifications": 2  # 1=allow, 2=block
    }
    
    chrome_options.add_experimental_option("prefs", prefs)

    #Automatically accepts chrome prompt
    chrome_options.set_capability('unhandledPromptBehavior', 'accept')

    driver = webdriver.Chrome(options = chrome_options)
    driver.get(link)

    def logar():
        general.wait_for(driver, By.ID, "usu", visible=True)

        raw_acessos = {}
        with open('access//socs.txt', "r", encoding='utf-8') as arquivo:
            raw_acessos = ast.literal_eval(arquivo.readline())

        driver.find_element(By.ID, 'usu').send_keys(raw_acessos[base][0])

        cod = int(raw_acessos[base][1])
        driver.find_element(By.ID, 'senha').send_keys(raw_acessos[base][2][cod])

        values_positions = {}
        for i in range(10):
            values_positions[driver.find_element(By.ID, 'bt_' + str(i)).get_attribute("value")] = str(i)

        for i in raw_acessos[base][3][cod]:
            driver.find_element(By.ID, 'bt_' + values_positions[i]).click()

        driver.find_element(By.ID, 'bt_entrar').click()
        
        return(raw_acessos, cod)
    
    raw_acessos, cod = logar()

    att_senha = driver.find_elements(By.NAME, 'senhaDigite')
    if att_senha and att_senha[0].is_displayed():
        novo_cod = 0 if cod else 1

        att_senha[0].send_keys(raw_acessos[base][2][novo_cod])
        driver.find_elements(By.NAME, 'senhaDigite').send_keys(raw_acessos[base][2][novo_cod])

        general.codigo_js(driver, 'alt')
        time.sleep(0.5)
        driver.execute_script("javascript:fecharAviso();")

        raw_acessos[base][1] = str(novo_cod)
        
        with open('access//socs.txt', "w", encoding='utf-8') as arquivo:
            arquivo.write(str(raw_acessos))

        logar()

    general.wait_for(driver, By.XPATH, '//*[@id="botao"]/a/img', visible=True)

    driver.switch_to.default_content()
    aviso = driver.find_elements(By.ID, 'avisoAdmAge')
    if aviso and aviso[0].is_displayed():
        driver.find_element(By.ID, 'naoMostrarAvisoAdministrador').click()
        driver.find_element(By.ID, 'botaoOk').click()

    return driver
