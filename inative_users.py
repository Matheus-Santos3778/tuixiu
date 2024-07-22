pip install selenium

#Imports
import time
from datetime import date, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

service = Service(executable_path=r'/bin/chromedriver')

#Wait for t seconds for the presence of the xpath/id/alerta 
def wait(x,y,t=5):
  if x == 'xpath':
    return WebDriverWait(driver, t).until(EC.presence_of_element_located((By.XPATH, f'{y}')))
  if x == 'id':
    return WebDriverWait(driver, t).until(EC.presence_of_element_located((By.ID, f'{y}')))
  if x == 'id':
    return WebDriverWait(driver, t).until(EC.presence_of_element_located((By.NAME, f'{y}')))
  if x == 'alerta':
    WebDriverWait(driver, t).until(EC.alert_is_present())
    return driver.switch_to.alert.accept()

#Save prints of the executions in the drive
def print_screenshot():
  global count_prints
  driver.save_screenshot('drive/MyDrive/roboPeruano/print' + str(count_prints) + '.png')
  count_prints += 1

#Change to the frame SOC
def soc_frame():
  try:
    driver.switch_to.frame("socframe")
    soc_frames.append(1)
  except:
    soc_frames.append(0)

#Wait for the 'carregando' (loading) message of SOC to pass
def wait_loading():
  driver.switch_to.default_content()
  while driver.find_element(By.ID, 'divCarregandoSub').get_attribute('style') == 'display: block;':
    time.sleep(0.5)
  soc_frame()

#Execute one of the javascripts
def codigo_js(code_name):
  cods = {'save': "javascript:doAcao('save');", 'usuario': "javascript:doAcao('usuario');", 'empresasUsu': "javascript:doAcao('empresasUsu')",'alt': "javascript:doAcao('alt')",
             'can': "javascript:doAcao('can')", 'ant': "javascript:doAcao('ant')", 'prox': "javascript:doAcao('prox')", 'browse':"javascript:doAcao('browse');", 'grupo':"javascript:doAcao('grupo');",
             'incluiGrupo':"javascript:doAcao('incluiGrupo');", 'incluiSubGrupo':"javascript:doAcao('incluiSubGrupo');", 'exc':"javascript:doAcao('exc');", 'incItem':"javascript:doAcao('incItem');"}
  driver.execute_script(cods[code_name])

#Try to log in the base
def login_base(user, passwrd = "example", id = "1111"):

  global driver
  link = "https://sistema.soc.com.br/WebSoc/"
  chrome_options = Options()
  lista_options = ['--headless', '--no-sandbox', '--disable-dev-shm-usage', '--window-size=1920x1080']
  for x in lista_options:
    chrome_options.add_argument(x)
  driver = webdriver.Chrome(options = chrome_options)
  driver.get(link)

  if user in ['base1', 'base2', 'base3']:
    user = "exemplo.user" + user

  assert "SOC" in driver.title
  try:

    #log in the base
    try:
      elem = driver.find_element(By.ID, "usu")
    except:
      print("Didn't find field user")
    elem.clear()
    elem.send_keys(user)
    driver.find_element(By.NAME, 'senha').send_keys(passwrd)

    for j in id:
      for i in range(10):
        if driver.find_element(By.NAME, 'bt_' + str(i)).get_attribute("value") == j:
          driver.find_element(By.NAME, 'bt_' + str(i)).click()

    wait('id', 'bt-entrar-0').click()
  except Exception as err:
    print_screenshot()
    driver.quit()
    print("Erro Login:")
    print(err)

#select company
def select_company(company):

  def searching_window():

    print_screenshot()
    wait_loading()
    driver.find_element(By.XPATH, '//*[@id="cproemp"]').send_keys(str(company))
    wait_loading()
    print_screenshot()
    driver.execute_script('javascript:travaEscEmp();')
    wait_loading()

    print_screenshot()
    if wait('xpath', '//*[@id="listaemop"]/table/tbody/tr/td[1]').text == str(company):
      driver.execute_script('javascript:choiceemp(' + str(company) + ');')
    else:
      print('Didn't find the company')

  try:
    try:
      print_screenshot()
      driver.find_element(By.ID,'avisoAdmAge')
      AC(driver).click(wait('id', 'naoMostrarAvisoAdministrador')).click(wait('id', 'botaoOk')).perform()
      print_screenshot()
      searching_window()
    except:
      searching_window()
    print_screenshot()
  except Exception as err:
    print_screenshot()
    driver.quit()
    print("Erro selecting company:")
    print(err)

#Select window
def select_window(window):

  try:
    print_screenshot()
    driver.switch_to.default_content()
    AC(driver).double_click(driver.find_element(By.XPATH, '//*[@id="cod_programa"]')).perform()
    print_screenshot()
    AC(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).send_keys(window).perform()
    print_screenshot()
    wait('id', 'btn_programa').click()
    print_screenshot()

  except Exception as err:
    print_screenshot()
    driver.quit()
    print("Error finding window:")
    print(err)

#Inactivate
def inactivate(personalization, questions):
  try:

    print_screenshot()
    wait_loading()
    Select(driver.find_element(By.XPATH, '//*[@id="personalizacao"]')).select_by_value(personalization)
    print_screenshot()
    wait_loading()

    for i in questions:
      print_screenshot()

      if 'NÃO' not in driver.find_element(By.XPATH, '//*[@id="socContent"]/form[1]/table/tbody/tr[1]/td/table['+ str(i) +']/tbody/tr/td[4]').text:
        wait('xpath', '//*[@id="socContent"]/form[1]/table/tbody/tr[1]/td/table['+ str(i) +']/tbody/tr/td[3]/a').click()
        Alert(driver).accept()
        wait_loading()

    print_screenshot()
    driver.switch_to.default_content()
    driver.execute_script('javascript:Empresas(); hideall();hidemenus('');menu_close();avisoLogin();')

    wait_loading()
    print_screenshot()

  except Exception as err:
    print_screenshot()
    driver.quit()
    print("Error inactivate:")
    print(err)

#Main line of code
count_prints = 1
soc_frames = []

#Base where the personalization is and the code of the personalization
base, perso = '3778', '1'

#Client companies codes to inactivate the questions
companies = [920522, 1243590]

#Questions to inactivate from the main company
questions = list(range(3, 12))
login_base(base)
for company in companies:
  select_company(company)
  select_window(209)
  inactive_questions(perso, questions)
  print(f'Company {company} finished')
