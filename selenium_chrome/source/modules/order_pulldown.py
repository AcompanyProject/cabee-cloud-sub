import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from log import slack

def operation_pulldown(driver, retry_count = 1):
    try:
        # 先物取引の選択
        time.sleep(5)
        future_trade_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'index-select')))
        future_trade_select = Select(future_trade_element)
        future_trade_select.select_by_value('19')

        # 直近のメジャー限月の選択
        contract_month_element = driver.find_elements_by_class_name('del-month-select')[len(driver.find_elements_by_class_name('del-month-select'))-1]
        contract_month_select = Select(contract_month_element)
        contract_month_select.select_by_value(str(retry_count))
        time.sleep(2)
    except Exception as err:
        driver.save_screenshot('log/image/error/order-pulldown.png')
        slack.send_message('error', 'プルダウン操作時にエラー Error: ' + str(err))
        raise
