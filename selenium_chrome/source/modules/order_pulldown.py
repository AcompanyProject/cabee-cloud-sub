import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack

def operation_pulldown(driver, page):
    try:
        # 先物取引の選択
        future_trade_element = ""
        time.sleep(5)
        if len(driver.find_elements_by_class_name('index-select')) > 1:
            future_trade_element = driver.find_elements_by_class_name('index-select')[len(driver.find_elements_by_class_name('index-select'))-1]
        else:
            future_trade_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.index-select')))

        future_trade_element.click()
        driver_actions = ActionChains(driver)
        driver_actions.send_keys(Keys.DOWN)
        if page == 'speed_order':
            driver_actions.send_keys(Keys.DOWN)
        driver_actions.send_keys(Keys.ENTER)
        driver_actions.perform()

        # 直近のメジャー限月の選択
        contract_month_element = ""
        if len(driver.find_elements_by_class_name('del-month-select')) > 1:
            contract_month_element = driver.find_elements_by_class_name('del-month-select')[len(driver.find_elements_by_class_name('del-month-select'))-1]
        else:
            contract_month_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'del-month-select')))

        contract_month_element.click()
        keydown_count = 1
        if page == 'speed_order':
            contract_month_list = contract_month_element.text.split("\n")
            for i,month in enumerate(contract_month_list):
                if '03月' in month or '06月' in month or '09月' in month or '12月' in month:
                    keydown_count += i
                    break

        driver_actions = ActionChains(driver)
        for i in range(keydown_count):
            driver_actions.send_keys(Keys.DOWN)
        driver_actions.send_keys(Keys.ENTER)
        driver_actions.perform()
        time.sleep(2)
    except Exception as err:
        driver.save_screenshot('log/image/error/order-pulldown.png')
        slack.send_message('error', 'プルダウン操作時にエラー page: ' + page + ', Error: ' + str(err))
        raise
