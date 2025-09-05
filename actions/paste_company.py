from utils import general
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def execute(driver, companies_access):
    
    general.codigo_js(driver, 'empresasUsu')
    general.codigo_js(driver, 'alt')

    curr_access_all = driver.find_element(By.ID, 'acessoTodasEmpresasUsuario').is_selected()

    if companies_access['access_all']:
        if not curr_access_all:
            driver.find_element(By.ID, 'acessoTodasEmpresasUsuario').click()
        else:
            print('As empresas já eram iguais')
    else:

        categories = {'company': ["listaEmpSelecionada", 'javascript:desassociarEmpresa("listaEmpSelecionada");', "empSel", 'all_companies', 'javascript:associar("empSel","listaEmpSelecionada");']
                     ,'group': ["grupo", "javascript:desassociar('grupo');", "grupoSel", 'all_groups', "javascript:associar('grupoSel','grupo');"]
                     ,'subgroup:': ["subGrupo", "javascript:desassociar('subGrupo');", "subGrupoSel", 'all_subgroups', "javascript:associar('subGrupoSel','subGrupo');"]
                     }

        for i in categories:
            #Removendo empresas selecionadas
            select_rem = Select(driver.find_element(By.ID, categories[i][0]))
            listagem_rem = [opt.get_attribute("value") for opt in select_rem.options]

            for elem in listagem_rem:
                select_rem.select_by_value(elem)

            driver.execute_script(categories[i][1])
            
            #Selecionando empresas copiadas
            select = Select(driver.find_element(By.ID, categories[i][2]))

            for elem in companies_access[categories[i][3]]:
                select.select_by_value(elem)            
            driver.execute_script(categories[i][4])

    general.codigo_js(driver, 'save')

    general.codigo_js(driver, 'volta')
    return(True)