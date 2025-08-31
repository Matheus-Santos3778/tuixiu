from utils import browser, general
from actions import access_page, search_user
from selenium.webdriver.common.by import By
from datetime import date, datetime
import time

def execute(inputs):

    tempo = time.time()
    driver = browser.get_driver(inputs['Base SOC'])
    access_page.execute(driver, "189")
    
    if not search_user.execute(driver, inputs['Usuario']):
        print('Usuário não encontrado na base')
    else:
        general.codigo_js(driver, 'usuario')
        general.codigo_js(driver, 'alt')
        
        data = driver.find_element(By.XPATH, '//*[@name="dataLimiteAcesso"]')
        data_atual = data.get_attribute('value')

        #Ativa se inativo
        situacao = driver.find_element(By.NAME, 'usuarioAtivo')
        if not situacao.is_selected():
            situacao.click()

        #Atualiza data se nao for lasa, se for lasa remove data
        if data_atual != '':
            if 'lasa' not in inputs['Usuario']:
                hoje = datetime.strptime(str(date.today()), '%Y-%m-%d')
                data_acesso =  datetime.strptime(data_atual, '%d/%m/%Y')
                if (data_acesso - hoje).days < 32:
                    mes = hoje.month if hoje.month > 9 else '0' + str(hoje.month)
                    novo_ano = '01' + str(mes) + str(hoje.year+1)
                    data.clear()
                    data.send_keys(novo_ano)
            else:
                data.clear()
        
        #Checa se tem perfil de usuario
        perfil_acesso = driver.find_element(By.ID, 'codigoPerfilSelecionado')
        if not perfil_acesso:
            print('Usuario nao tem perfil de acesso vinculado')

        #Reseta a senha
        #driver.execute_script("abresenhas();")
        driver.find_element(By.NAME, 'trocaSenha').click()

        senha = driver.find_element(By.ID, 'senha')
        senha.send_keys('mudar123')
        
        resenha = driver.find_element(By.ID, 'senhaRedigitada')
        resenha.send_keys('mudar123')

        general.codigo_js(driver, 'save')
        general.waiter(driver)

        aviso = driver.find_elements(By.XPATH, '//*[@id="mensagemErro"]/div[2]/p/a')

        if aviso and aviso[0].is_displayed():
            aviso[0].click()
            #javascript:fechar('mensagemErro')

            senha = driver.find_element(By.ID, 'senha')
            resenha = driver.find_element(By.ID, 'senhaRedigitada')
            senha.send_keys('4')
            resenha.send_keys('4')
            
            general.codigo_js(driver, 'save')
            general.waiter(driver)

        usuario_resetado = driver.find_element(By.XPATH, '//*[@id="conteudosTable"]').text
        print(usuario_resetado)

    tempo = round(time.time() - tempo, 2)
    print("Process finished --- %s seconds" % (tempo))
