import os
import time
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack

load_dotenv()

def operation_login(driver):
    try:
        driver.get('https://trade.matsui.co.jp/mgap/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-id'))).send_keys(os.environ.get("USER_ID"))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password'))).send_keys(os.environ.get("USER_PASS"))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'local-nav-login__button'))).click()
        time.sleep(3)
        driver.refresh() # 広告ポップアップを回避
        time.sleep(3)
    except Exception as err:
        driver.save_screenshot('log/image/error/login.png')
        slack.send_message('warning', 'ログイン操作が失敗しました。 Error: ' + str(err))
        raise
