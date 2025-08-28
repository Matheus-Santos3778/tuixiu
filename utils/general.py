import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Waits for the 'loading' element to disappear
def waiter(driver):

    time.sleep(0.25)
    driver.switch_to.default_content()
    time.sleep(0.25)
    while driver.find_element(By.ID, 'divCarregandoSub').get_attribute('style') == 'display: block;':
        time.sleep(0.5)
    time.sleep(0.25)        
    driver.switch_to.frame("socframe")

#Runs the common pattern js scripts doAcao
def codigo_js(driver, nome):
    
    time.sleep(0.25)
    driver.execute_script("javascript:doAcao('"+ nome +"');")
    time.sleep(0.25)

#Waits for an element to be visible
def wait_for(driver, by, identifier, timeout=10, visible=False):
    condition = EC.visibility_of_element_located if visible else EC.presence_of_element_located
    return WebDriverWait(driver, timeout).until(condition((by, identifier)))

