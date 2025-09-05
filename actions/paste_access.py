import time
from utils import general
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC

def execute(driver, value_perfil):
    
    general.codigo_js(driver, 'usuario')
    general.codigo_js(driver, 'alt')
    
    #Removendo perfis selecionados
    perfis = driver.find_elements(By.XPATH, '//*[@id="codigoPerfilSelecionado"]/option')
    for perfil in perfis:
        AC(driver).double_click(perfil).perform()

    #Selecionando o novo perfil
    driver.execute_script("javascript:abrirModalSelecaoPerfis();")
    time.sleep(0.25)
    
    driver.find_element(By.XPATH, f"//tr[@data-codigo='{value_perfil}']").click()

    driver.execute_script("javascript:closeTagSelecionarPerfis();")
    time.sleep(0.25)

    general.codigo_js(driver, 'save')
    
    general.codigo_js(driver, 'volta')
    return(True)