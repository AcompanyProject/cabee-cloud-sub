import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack
from modules import order_pulldown, order_confirm

def operation_new_order(driver, is_buy_sign, sheet_num):
    if sheet_num == 0:
        slack.send_message('error', 'operation_new_order: 新規購入の枚数が0枚になっています')
        raise

    if is_buy_sign is None:
        slack.send_message('error', 'operation_new_order: サインがNoneになっています')
        raise

    try:
        slack.send_message('notice', '<!here> 新規注文します')

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-speed-order'))).click()
        time.sleep(3)

        order_kind = 'buy-orders' if is_buy_sign is True else 'sell-orders'
        order_kind2 = '.order-label.buy' if is_buy_sign is True else '.order-label.sell'

        order_pulldown.operation_pulldown(driver)

        driver.find_element_by_class_name('trade-unit-spinner').find_element_by_css_selector('.common-input.number-field').click()

        driver_actions = ActionChains(driver)
        driver_actions.send_keys(str(sheet_num))
        driver_actions.perform()

        order_confirm.operation_confirm(driver, order_kind, order_kind2, 'new_order')
    except Exception as err:
        driver.save_screenshot('log/image/error/new-order.png')
        slack.send_message('error', '新規注文中にエラー Error: ' + str(err))
        raise
