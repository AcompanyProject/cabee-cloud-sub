import time
from log import slack

def operation_login(driver, user_info):
    try:
        driver.get('https://trade.matsui.co.jp/mgap/logi')
        driver.find_element_by_id('login-id').send_keys(user_info["USER_ID"])
        driver.find_element_by_id('login-password').send_keys(user_info["USER_PASS"])
        driver.find_element_by_class_name('local-nav-login__button').click()
        time.sleep(5)
        driver.save_screenshot('log/images/login.png')
    except Exception as err:
        slack.send_message('error', 'エラー', 'ログイン操作が失敗しました。 Error: ' + str(err))
        raise
