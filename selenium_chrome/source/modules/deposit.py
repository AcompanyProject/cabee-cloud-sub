import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from log import slack

def operation_get_deposit(driver):
    sheet_per_deposit = 750000 # いくらにつき1枚張りするか

    # 余力情報ページに遷移
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-power-info'))).click()
        time.sleep(2)
    except Exception as err:
        driver.save_screenshot('log/image/error/after-login.png')
        slack.send_message(
            'warning',
            'ログイン後の操作に失敗しました。以下を確認してください： 松井証券のサイトログイン後に契約更新等のタスクが未完了か？ Error: ' + str(err),
        )
        raise

    try:
        # 先物のタブをクリック
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'powerInfoMenuFutOp'))).click()
        time.sleep(2)

        # 維持証拠金余力の取得
        deposit = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'powerInfoFutOpRealCashBalance'))).text
        deposit = deposit.translate(str.maketrans({',':'', '円':''}))

        # 先物評価損益の取得
        profit_loss = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'powerInfoFutOpRealFutUnrealized'))).text
        profit_loss = int(profit_loss.translate(str.maketrans({',':'', '円':''})))

        # 建玉枚数の決定
        sheet_num = 1 if int(deposit) < sheet_per_deposit else int(deposit) // sheet_per_deposit

        try:
            profit_loss_percentage = (profit_loss/sheet_num)/sheet_per_deposit*100
        except ValueError:
            slack.send_message('error', 'profit_loss_percentageの値が不正です: ' + str(profit_loss_percentage))
            raise

        print("profit_loss_percentage: " + str(profit_loss_percentage))

        if profit_loss_percentage < -4:
            # 4%以上の損失発生時に一応通知する
            slack.send_message(
                'warning',
                '4%を超える損失が発生しています。15分以内に自動で損切りしなければ、手動で損切りしてください。'
            )

        # HOMEに戻る
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//li[@data-page="top"]'))).click()
        time.sleep(5)

        return int(sheet_num)
    except Exception as err:
        driver.save_screenshot('log/image/error/deposit.png')
        slack.send_message('warning', '余力情報の取得に失敗しました Error: ' + str(err))
        raise
