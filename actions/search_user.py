from selenium.webdriver.common.by import By
from utils import general

def execute(driver, user):

        driver.find_element(By.NAME, "nomeSeach").send_keys(user)
        driver.find_element(By.NAME, "botao-pesquisar-padrao-soc").click()
        general.waiter(driver)

        rows = driver.find_elements(By.XPATH, '//*[@id="socContent"]/form[1]/table/tbody/tr[2]/td/table/tbody/tr/td[3]')

        usuarios = [row.text for row in rows[1:]]

        if user in usuarios:
                driver.find_element(By.XPATH, '//*[@id="socContent"]/form[1]/table/tbody/tr[2]/td/table/tbody/tr['+ str(usuarios.index(user) + 2) +']/td[1]/a').click()      
                general.waiter(driver)
                return(True)
        else:
                return(False)