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

        refundKbn_texts = []
        contractAmt_texts = []
        try:
            # 建区分が売建or買建orなしか確認
            refundKbn_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".refundKbn")))
            refundKbn_texts = [element.text for element in refundKbn_elements]
            contractAmt_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".contractAmt")))
            contractAmt_texts = [element.text for element in contractAmt_elements]
        except Exception as err:
            contract = 'none'
            slack.send_message('warning', f'建区分の取得でエラー: {err}')

        contractAmt_total = 0
        if(len(refundKbn_texts) > 0 and len(contractAmt_texts) > 0):
            if all(text == '買建' for text in refundKbn_texts):
                contract = 'buy'
            elif all(text == '売建' for text in refundKbn_texts):
                contract = 'sell'
            elif '買建' in refundKbn_texts and '売建' in refundKbn_texts:
                multi_error_text = '返済注文時にエラーが発生したようです: 保有中の建玉に買建と売建の両方が存在しています'
                slack.send_message('error', multi_error_text)
                raise Exception(multi_error_text)
            else:
                contract = 'none'

            # 建玉数を取得
            contractAmt_total = sum(int(text) for text in contractAmt_texts)

            time.sleep(5)

        # HOMEに戻る
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@data-page="top"]'))).click()
        time.sleep(5)

        return contract, contractAmt_total
    except Exception as err:
        driver.save_screenshot('log/image/error/contract.png')
        slack.send_message('warning', '保持中の建玉情報の取得に失敗しました Error: ' + str(err))
        raise
