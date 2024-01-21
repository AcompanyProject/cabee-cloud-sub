import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack
from modules import order_pulldown, order_confirm

def operation_repayment_order(driver, purpose, is_buy_sign):
    try:
        send_message_text = '<!here> 返済&新規注文をします。返済注文から開始中...' if purpose == 'repayment_and_new_order' else '<!here> 返済注文します'
        slack.send_message('notice', send_message_text)

        # ホームからスピード注文ページに遷移
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-speed-order'))).click()
        time.sleep(5)

        retry_count = 1
        retry_max = 5
        is_retry = True
        for retry_count in range(1, retry_max + 1):
            # 建玉が見つかるまで各限月をチェック
            if is_retry:
                order_pulldown.operation_pulldown(driver, retry_count)
                driver.find_element_by_class_name('dealing-type-refund-futop').click()
                time.sleep(2)
                driver.find_element_by_id('fut-op-speed-order-input-position-list-button').click()
                time.sleep(2)

                if len(driver.find_elements_by_class_name('grid-body-empty')) >= 1:
                    # 買い建玉が存在しない
                    driver.find_element_by_css_selector('.switch.sell-toggle').click()
                    time.sleep(1)

                    if len(driver.find_elements_by_class_name('grid-body-empty')) >= 1:
                        # 売り建玉が存在しない
                        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.common-modal-close-btn.cancel-btn'))).click() # モーダルを閉じる
                        time.sleep(2)
                    else:
                        # 売り建玉が存在する
                        order_kind = 'sell-orders'
                        order_kind2 = '.order-label.sell'
                        is_retry = False
                else:
                    # 買い建玉が存在する
                    order_kind = 'buy-orders'
                    order_kind2 = '.order-label.buy'
                    is_retry = False
            else:
                driver.find_element_by_class_name('select-position-btn').click()
                time.sleep(2)
                break

        try:
            buttons = driver.find_elements_by_class_name('confirm-btn')
            buttons[-1].click()
            time.sleep(5)
            order_confirm.operation_confirm(driver, order_kind, order_kind2)
        except:
            driver.save_screenshot('log/image/error/repayment-order-pulldown-notfound.png')
            slack.send_message('error', 'どの限月にも建玉を見つけられませんでした')
    except Exception as err:
        driver.save_screenshot('log/image/error/repayment-order.png')
        slack.send_message('error', '返済注文中にエラー Error: ' + str(err))
        raise
