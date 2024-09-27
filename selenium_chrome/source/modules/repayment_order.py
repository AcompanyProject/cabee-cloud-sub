import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack, firestore
from modules import contract

def operation_repayment_order(driver, order_steps):
    send_message_text = '<!here> 返済&新規注文をします。返済注文から開始中...' if order_steps == 'repayment_and_new_order' else '<!here> 返済注文します'
    slack.send_message('notice', send_message_text)

    # ホームからスピード注文ページに遷移
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-repayment'))).click()
    time.sleep(3)
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.repay-all-btn'))).click()
    except Exception as err:
        slack.send_message('error', '一括返済ボタン押下時にエラー: ' + str(err))
        raise

    password_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'future-option-position-password-box'))
    )
    key_input_field = password_box.find_element(By.CLASS_NAME, 'common-key-input-field')
    key_input_field.click()
    driver_actions = ActionChains(driver)
    driver_actions.send_keys(os.environ.get("TRADE_PASS"))
    driver_actions.perform()

    # 注文確定
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.common-modal-cancel-all-btn'))).click()
    except Exception as err:
        slack.send_message('error', '一括返済するボタン押下時（注文確定時）にエラー: ' + str(err))
        raise

    time.sleep(3)

    # HOMEに戻る
    driver.refresh()
    time.sleep(5)

    # 正しく注文されたか確認する
    contract_type, isSQ, contract_total, repay_button_count = contract.operation_get_contract(driver)
    slack.send_message('notice', '注文後の建玉確認 （建玉種類: ' + str(contract_type) + ', 建玉数: ' + str(contract_total) + '）')

    # 返済注文後、返済ボタンが存在する場合はエラーを出力
    if int(repay_button_count) > 0:
        firestore.refresh_trade_time('repayment_order')
        slack.send_message('error', '建玉がサイン通りになっていないため処理を中断します')
        raise
    else:
        slack.send_message('notice', '正常に取引処理が完了しました')


