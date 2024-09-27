import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack, firestore
from modules import order_pulldown, contract

load_dotenv()

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

        operation_confirm(driver, order_kind, order_kind2, 'new_order')
    except Exception as err:
        driver.save_screenshot('log/image/error/new-order.png')
        slack.send_message('error', '新規注文中にエラー Error: ' + str(err))
        raise

def operation_confirm(driver, order_kind, order_kind2, order_type):
    try:
        if len(driver.find_element_by_class_name('common-key-input-field').get_attribute('value')) == 0:
            driver.find_element_by_class_name('common-omit-confirm-btn').click()
            driver.find_element_by_class_name('common-modal-confirm-btn').click()
            driver.find_element_by_class_name('common-key-input-field').click()
            driver_actions = ActionChains(driver)
            driver_actions.send_keys(os.environ.get("TRADE_PASS"))
            driver_actions.perform()

        if firestore.check_duplication_trade(order_type):
            # 前回の注文操作から4分以上経過（重複実行防止の実装）
            firestore.update_trade_time(order_type) # 最新取引時刻を更新

            driver.find_element_by_class_name('market-order').find_element_by_class_name(order_kind).click()
            time.sleep(1)

            # 注文確定
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, order_kind2))).click()
            slack.send_message('notice', '注文が完了しました')
            time.sleep(2)

            # リロードするとHOMEに戻り、pulldownに設定された値も戻される
            driver.refresh()
            time.sleep(5)

            # 正しく注文されたか確認する
            contract_type, isSQ, contract_total, repay_button_count = contract.operation_get_contract(driver)
            slack.send_message('notice', '注文後の建玉確認 （建玉種類: ' + str(contract_type) + ', 建玉数: ' + str(contract_total) + '）')

            # 新規注文後、返済ボタンが存在しない場合はエラーを出力
            if order_type == "new_order" and int(repay_button_count) == 0:
                firestore.refresh_trade_time(order_type)
                slack.send_message('error', '建玉がサイン通りになっていないため処理を中断します')
                raise
            else:
                slack.send_message('notice', '正常に取引処理が完了しました')
        else:
            slack.send_message('notice', '重複注文をブロックしました')
            raise
    except Exception as err:
        driver.save_screenshot('log/image/error/order-confirm.png')
        slack.send_message('error', '注文確定操作時にエラー Error: ' + str(err))
        raise
