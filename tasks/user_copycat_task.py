import time
from utils import browser
from actions import access_page, search_user, copy_access, copy_company, copy_schedule, paste_access, paste_company, paste_schedule

def execute(inputs):

    tempo = time.time()

    driver = browser.get_driver(inputs['Base SOC'])
    access_page.execute(driver, "189")

    if not search_user.execute(driver, inputs['Usuario Espelho']):
        print('Usuário Espelho não encontrado na base')
    else:

        copies = {'access': [inputs['Acessos'], copy_access.execute, '', paste_access.execute]
                  ,'company': [inputs['Empresas'], copy_company.execute, {}, paste_company.execute]
                  ,'schedule': [inputs['Agenda'], copy_schedule.execute, {}, paste_schedule.execute]}

        for i in copies:
            
            if copies[i][0]:

                status = copies[i][1](driver)

                if not status[0]:
                    print(status[1])
                    tempo = round(time.time() - tempo, 2)
                    print("Process finished --- %s seconds" % (tempo))
                    return(False)

                copies[i][2] = status[1]
                print(copies[i][2])

        access_page.execute(driver, "189")
        if not search_user.execute(driver, inputs['Usuario']):
            print('Usuário não encontrado na base')
        else:

            for i in copies:

                if copies[i][0]:

                    status = copies[i][3](driver, copies[i][2])
        

    tempo = round(time.time() - tempo, 2)
    print("Process finished --- %s seconds" % (tempo))