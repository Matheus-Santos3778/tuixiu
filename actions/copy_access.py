from utils import general
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def execute(driver):
    
    general.codigo_js(driver, 'usuario')
    general.codigo_js(driver, 'alt')
    
    #Lista de perfis de acessos do usuario
    all_options = Select(driver.find_element(By.ID, "codigoPerfilSelecionado")).options
    perfis_acesso = [opt.get_attribute("value") for opt in all_options]

    general.codigo_js(driver, 'can')

    if len(perfis_acesso) > 1:

        return(False, 'Usuario espelho tem +1 perfil de acesso')
    
    elif len(perfis_acesso) < 1:

        return(False, 'Usuario espelho nao tem perfil de acesso')
    
    general.codigo_js(driver, 'volta')
    return(True, perfis_acesso[0])