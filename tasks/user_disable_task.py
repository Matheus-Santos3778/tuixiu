from utils import browser, general
from actions import access_page, search_user
from selenium.webdriver.common.by import By
import time

def execute(inputs):

    tempo = time.time()
    driver = browser.get_driver(inputs['Base SOC'])
    access_page.execute(driver, "189")

    if not search_user.execute(driver, inputs['Usuario']):
        print('Usuário não encontrado na base')
    else:
        general.codigo_js(driver, 'usuario')
        situacao = driver.find_element(By.XPATH, '/html/body/age_nao_gravar/div[2]/div/form/age_substituir_cabec_log/table/tbody/tr[1]/td/table/tbody/tr[4]/td[2]').text
        if situacao == 'Sim':
            general.codigo_js(driver, 'alt')
            driver.find_element(By.NAME, 'usuarioAtivo').click()
            general.codigo_js(driver, 'save')
            situacao = driver.find_element(By.XPATH, '/html/body/age_nao_gravar/div[2]/div/form/age_substituir_cabec_log/table/tbody/tr[1]/td/table/tbody/tr[4]/td[2]')
            if situacao == 'Sim':
                print('Erro ao tentar inativar!')
            else:
                print('Usuario inativado com sucesso!')
        else:
            print('Usuario ja esta inativo!')

    tempo = round(time.time() - tempo, 2)
    print("Process finished --- %s seconds" % (tempo))