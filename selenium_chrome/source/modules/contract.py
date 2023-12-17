import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack

def operation_get_contract(driver):
    try:
        # 建玉照会ページに遷移
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-repayment'))).click()
        time.sleep(5)

        try:
            # 建区分が売建or買建orなしか確認（.refundKbn）
            refundStatus = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".refundKbn"))).text

            if refundStatus == '買建':
                contract = 'buy'
            elif refundStatus == '売建':
                contract = 'sell'
            else:
                contract = 'none'
        except:
            contract = 'none'

        time.sleep(5)

        # HOMEに戻る
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@data-page="top"]'))).click()
        time.sleep(5)

        return contract
    except Exception as err:
        driver.save_screenshot('log/image/error/contract.png')
        slack.send_message('warning', '保持中の建玉情報の取得に失敗しました Error: ' + str(err))
        raise