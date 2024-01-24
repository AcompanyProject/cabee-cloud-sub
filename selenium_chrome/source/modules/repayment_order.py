import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack
from modules import order_pulldown, order_confirm

def operation_repayment_order(driver, purpose):
    try:
        send_message_text = '<!here> 返済&新規注文をします。返済注文から開始中...' if purpose == 'repayment_and_new_order' else '<!here> 返済注文します'
        slack.send_message('notice', send_message_text)

        # ホームからスピード注文ページに遷移
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-speed-order'))).click()
        time.sleep(3)

        retry_count = 1
        order_kind, order_kind2 = None, None
        while retry_count < 5 and order_kind is None:
            retry_count += 1
            order_kind, order_kind2 = get_order_kind(driver, retry_count)

        if order_kind is None:
            raise Exception('get_order_kind returned None after 4 attempts')

        # 全数量選択
        driver.find_element_by_class_name('select-position-btn').click()
        time.sleep(1)

        # 確定ボタン押下
        buttons = driver.find_elements_by_class_name('confirm-btn')
        buttons[-1].click()
        time.sleep(3)

        try:
            order_confirm.operation_confirm(driver, order_kind, order_kind2, 'repayment_order')
        except Exception as err:
            driver.save_screenshot('log/image/error/repayment-order-contract-notfound.png')
            slack.send_message('error', f'建玉を見つけられませんでした: {err}')
    except Exception as err:
        driver.save_screenshot('log/image/error/repayment-order.png')
        slack.send_message('error', '返済注文中にエラー Error: ' + str(err))
        raise

def get_order_kind(driver, retry_count):
    order_kind = None
    order_kind2 = None

    order_pulldown.operation_pulldown(driver, retry_count)
    driver.find_element_by_class_name('dealing-type-refund-futop').click() # 返済を選択
    time.sleep(2)
    driver.find_element_by_id('fut-op-speed-order-input-position-list-button').click() # 建玉指定ボタン押下
    time.sleep(2)

    # 建玉選択モーダル内の操作
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
            order_kind = 'buy-orders'
            order_kind2 = '.order-label.buy'
    else:
        # 買い建玉が存在する
        order_kind = 'sell-orders'
        order_kind2 = '.order-label.sell'

    return order_kind, order_kind2
