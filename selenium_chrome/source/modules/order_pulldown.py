import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from log import slack
from datetime import datetime, timedelta

def operation_pulldown(driver, retry_count = 1):
    try:
        # 先物取引の中から日経225miniを選択する
        future_trade_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'index-select')))
        future_trade_select = Select(future_trade_element)
        future_trade_select.select_by_value('19')
        selected_option = next((option.text for option in future_trade_select.options if option.get_attribute('value') == '19'), None)

        if selected_option != "日経225mini":
            slack.send_message('error', 'プルダウン操作時にエラー: 先物取引の選択で日経225mini以外が選択されています。')
            raise ValueError("選択されたオプションが '日経225mini' ではありません")
        
        # 直近の月限を選択
        contract_month_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'del-month-select')))
        contract_month_select = Select(contract_month_element)
        now = datetime.now() + timedelta(hours=9)
        month_str = now.strftime('%y年%m月限')
        contract_option = None

        for option in contract_month_select.options:
            if option.text and option.text >= month_str:
                contract_option = option
                break

        if contract_option:
            contract_month_select.select_by_visible_text(contract_option.text) # 限月に当てはまるオプションを選択
            driver.save_screenshot('log/image/info/pulldown-select.png')
        else:
            slack.send_message('error', f'プルダウン操作時にエラー: {month_str} 以降の限月が見つかりません。')
            raise

        time.sleep(2)
    except Exception as err:
        driver.save_screenshot('log/image/error/order-pulldown.png')
        slack.send_message('error', 'プルダウン操作時にエラー Error: ' + str(err))
        raise
