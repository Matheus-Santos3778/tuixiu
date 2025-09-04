from utils import general
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def execute(driver):
    
    general.codigo_js(driver, 'empresasUsu')
    general.codigo_js(driver, 'alt')

    companies_access = {'access_all': False, 'all_companies': [], 'all_groups': [], 'all_subgroups': []}

    companies_access['access_all'] = driver.find_element(By.ID, 'acessoTodasEmpresasUsuario').is_selected()

    if not companies_access['access_all']:

        #Lista de perfis de acessos do usuario
        companies = Select(driver.find_element(By.ID, "listaEmpSelecionada")).options
        companies_access['all_companies'] = [opt.get_attribute("value") for opt in companies]

        groups = Select(driver.find_element(By.ID, "grupo")).options
        companies_access['all_groups'] = [opt.get_attribute("value") for opt in groups]

        subgroups = Select(driver.find_element(By.ID, "subGrupo")).options
        companies_access['all_subgroups'] = [opt.get_attribute("value") for opt in subgroups]

        if companies_access['all_companies'] == [] and companies_access['all_groups'] == [] and companies_access['all_subgroups'] == []:
            return(False, 'Usuário espelho não tem nenhuma empresa vinculada')


    general.codigo_js(driver, 'can')

    general.codigo_js(driver, 'volta')
    return(True, companies_access)