import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from log import slack

def operation_check_circuit_breaker(driver):
    # 先物OP注文照会ページに遷移
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-order-list'))).click()
        time.sleep(2)
    except Exception as err:
        driver.save_screenshot('log/image/error/order-reference.png')
        slack.send_message('warning', '先物OP注文照会への移動操作に失敗しました。 Error: ' + str(err))
        raise

    try:
        # 最新の注文状態を取得
        order_status_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.odrStatus'))
        )

        # 1番目の要素のテキストを取得
        if order_status_elements:
            order_status = order_status_elements[0].text

            if order_status == "失効":
                slack.send_message('warning', '値幅エラー（サーキットブレーカー）等による注文失効の可能性があります。時間が経つと解消されることがありますが、相場の変動が非常に高いときは目視で監視して手動で注文操作することをお勧めします')
            elif order_status == "受付済" or order_status == "発注済":
                slack.send_message('warning', '松井証券で注文を受付中のようです。これは時間が経つと約定される可能性があります。')

        time.sleep(2)
    except Exception as err:
        driver.save_screenshot('log/image/error/deposit.png')
        slack.send_message('warning', '余力情報の取得に失敗しました Error: ' + str(err))
        raise
