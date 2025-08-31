from utils import general

def execute(driver, page):

    driver.switch_to.default_content()
    driver.execute_script("redirAction("+ page +");")
    general.waiter(driver)
    