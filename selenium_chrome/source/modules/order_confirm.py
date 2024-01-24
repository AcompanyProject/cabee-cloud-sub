import os
import time
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from modules import contract
from log import slack, firestore

load_dotenv()

def operation_confirm(driver, order_kind, order_kind2, trade_kind):
    try:
        if len(driver.find_element_by_class_name('common-key-input-field').get_attribute('value')) == 0:
            driver.find_element_by_class_name('common-omit-confirm-btn').click()
            driver.find_element_by_class_name('common-modal-confirm-btn').click()
            driver.find_element_by_class_name('common-key-input-field').click()
            driver_actions = ActionChains(driver)
            driver_actions.send_keys(os.environ.get("TRADE_PASS"))
            driver_actions.perform()

        driver.find_element_by_class_name('market-order').find_element_by_class_name(order_kind).click()
        time.sleep(2)

        if firestore.check_duplication_trade(trade_kind):
            # 前回の注文操作から4分以上経過（重複実行防止の実装）
            firestore.update_trade_time(trade_kind) # 最新取引時刻を更新

            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, order_kind2))).click() #注文確定
                slack.send_message('notice', '注文が完了しました')
                time.sleep(2)

                # リロードするとHOMEに戻り、pulldownに設定された値も戻される
                driver.refresh()
                time.sleep(5)

                # 正しく注文されたか確認する
                realtime_contract, contractAmt_total = contract.operation_get_contract(driver)
                slack.send_message('notice', '注文後の建玉確認 （建玉種類: ' + str(realtime_contract) + ', 建玉数: ' + str(contractAmt_total) + '）')
            except Exception as err:
                firestore.refresh_trade_time(trade_kind)
                slack.send_message('error', f'注文確定時にエラーが出たのでFirestoreの{trade_kind}のtimestampをリセットしました: ' + str(err))
    except Exception as err:
        driver.save_screenshot('log/image/error/order-confirm.png')
        slack.send_message('error', '注文確定操作時にエラー Error: ' + str(err))
        raise
