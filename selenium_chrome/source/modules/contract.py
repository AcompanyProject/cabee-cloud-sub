import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack

def operation_get_contract(driver):
    try:
        # 建玉照会ページに遷移
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-repayment'))).click()
        time.sleep(3)

        refundKbn_texts = []
        isSQ = False
        contract_type = 'none'
        contractAmt_texts = []
        contract_total = 0
        repay_button_count = 0

        try:
            # 建区分（売建or買建）の取得
            refundKbn_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".refundKbn")))
            refundKbn_texts = [element.text for element in refundKbn_elements]

            # 建枚数の合計
            contractAmt_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".contractAmt")))
            contractAmt_texts = [element.text for element in contractAmt_elements]

            # 返済ボタンの取得
            repay_button_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".common-label-repay")))
            repay_button_count = len(repay_button_elements)

            if len(refundKbn_texts) != repay_button_count:
                # 返済ボタンと建区分の個数が異なる場合はSQとみなす
                isSQ = True
        except Exception:
            contract_type = 'none'

        if len(refundKbn_texts) > 0:
            # 建玉数を取得
            contract_total = sum(int(text) for text in contractAmt_texts)

            # 建玉が存在する場合
            if all(text == '買建' for text in refundKbn_texts):
                contract_type = 'buy'
            elif all(text == '売建' for text in refundKbn_texts):
                contract_type = 'sell'
            elif '買建' in refundKbn_texts and '売建' in refundKbn_texts:
                slack.send_message('warning', '保有中の建玉に買建と売建の両方が存在しています')
                # SQの強制決済中にサインが変更された場合に起こりうる
                contract_type = 'both'
            else:
                contract_type = 'none'

        # HOMEに戻る
        time.sleep(3)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@data-page="top"]'))).click()
        time.sleep(2)

        return contract_type, isSQ, contract_total, repay_button_count
    except Exception as err:
        driver.save_screenshot('log/image/error/contract.png')
        slack.send_message('warning', '保持中の建玉情報の取得に失敗しました Error: ' + str(err))
        raise
