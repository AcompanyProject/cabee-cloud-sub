# 現在のサインと証券会社の建玉が一致しているか判定 -> 一致していなければサインに一致するよう操作する
import os, random, json, time, requests
from datetime import datetime
from calendar import Calendar
import pytz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

download_dir = "/home/mjt_not_found_404/cabee-cloud/gcf-packs/selenium_chrome/source/Downloads"
prefs = { 'download.prompt_for_download': False, 'download.directory_upgrade': True }
params = { 'cmd': 'Page.setDownloadBehavior', 'params': { 'behavior': 'allow', 'downloadPath': download_dir }}
chrome_options = webdriver.ChromeOptions()
user_agent = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1; Valve Steam GameOverlay/1679680416) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_0; Valve Steam GameOverlay/1679680416) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 13_0_0; en-US; Valve Steam GameOverlay/1676336721; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
]
UA = random.choice(user_agent)

chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-level=0')
chrome_options.add_argument('--v=99')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('user-agent='+ UA)

chrome_options.add_experimental_option('prefs', prefs) # headlessモードでのダウンロードを可能にする
chrome_options.binary_location = os.getcwd() + "/headless-chromium"
driver = webdriver.Chrome(os.getcwd() + "/chromedriver",chrome_options=chrome_options)
driver.command_executor._commands["send_command"] = ('POST', '/session/$sessionId/chromium/send_command')
driver.execute("send_command", params)

# グローバル変数
# WEB_HOOK_URL = "https://hooks.slack.com/services/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"
USER_INFO_OPEN = open('./json/user_info.json', 'r')
USER_INFO = json.load(USER_INFO_OPEN)
REALTIME_DEPOSIT = 0
REALTIME_SHEET_NUM = 0
IS_SQ_TRADE = False
jst = pytz.timezone('Asia/Tokyo')
Date_NOW = datetime.now(jst)
headers = {
    'Access-Control-Allow-Origin': '*'
}

# メイン関数
def trade_executor(request):
    # Cabeeサイン取得
    sign = call_cloud_function() # サイン
    print("sign:" + str(sign))

    # ログイン
    operation_login()
    time.sleep(5)
    print("ログイン完了")

    # 余力情報ページクリック
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-power-info'))).click()
    except:
        # requests.post(WEB_HOOK_URL, data = json.dumps({
        #     'text': 'ログイン後に操作ができません。本エラーが連続する場合、松井証券のサイトで契約更新等のポップアップが出ていないか確認してください。',
        #     'username': u'エラー', 'icon_emoji': u':fire:', 'link_names': 1,
        # }))
        print("エラー")

    time.sleep(5)

    # 証拠金を見て建玉枚数取得
    operation_get_realtime_deposit()
    time.sleep(5)
    print("REALTIME_SHEET_NUM:" + str(REALTIME_SHEET_NUM))

    # HOMEに戻る
    driver.find_element(By.XPATH, '//li[@data-page="top"]').click()
    time.sleep(5)

    # 取引中の建玉情報を取得
    realtime_contract = operation_get_realtime_contract()
    time.sleep(5)
    print("REALTIME_CONTRACT:" + realtime_contract)

    # HOMEに戻る
    driver.find_element(By.XPATH, '//li[@data-page="top"]').click()
    time.sleep(5)

    # パターン（17時くらいまで稼働させて、SQ跨ぎも対応させる）
    purpose = 'none'
    is_buy_sign = False
    if realtime_contract == 'none' and sign == 'sell': # 新規売り
        purpose = 'new_order'
        is_buy_sign = False
    elif realtime_contract == 'none' and sign == 'buy': # 新規買い
        purpose = 'new_order'
        is_buy_sign = True
    elif realtime_contract == 'buy' and sign == 'none': # 返済売り
        purpose = 'repayment_order'
        is_buy_sign = False
    elif realtime_contract == 'sell' and sign == 'none': # 返済買い
        purpose = 'repayment_order'
        is_buy_sign = True
    elif realtime_contract == 'buy' and sign == 'sell': # 返済売り、新規売り
        purpose = 'repayment_and_new_order'
        is_buy_sign = False
    elif realtime_contract == 'sell' and sign == 'buy': # 返済買い、新規買い
        purpose = 'repayment_and_new_order'
        is_buy_sign = True

    try_count = 2 # 返済注文時の限月プルダウンの試行回数
    if purpose == 'new_order':
        # requests.post(WEB_HOOK_URL, data = json.dumps({
        #     'text': '新規注文します',
        #     'username': u'サイン', 'icon_emoji': u':cat:', 'link_names': 1,
        # }))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-speed-order'))).click()
        time.sleep(5)
        operation_new_order(purpose, is_buy_sign)
        # requests.post(WEB_HOOK_URL, data = json.dumps({
        #     'text': '新規注文を完了しました',
        #     'username': u'サイン', 'icon_emoji': u':cat:', 'link_names': 1,
        # }))
    elif purpose == 'repayment_order':
        # requests.post(WEB_HOOK_URL, data = json.dumps({
        #     'text': '返済注文します',
        #     'username': u'サイン', 'icon_emoji': u':cat:', 'link_names': 1,
        # }))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-speed-order'))).click()
        for i in range(try_count):
            try:
                operation_repayment_order(i+1) # 返済できるまでプルダウン（限月）の下キーを押す回数を増やして試行する
                # requests.post(WEB_HOOK_URL, data = json.dumps({
                #     'text': '返済注文を完了しました',
                #     'username': u'サイン', 'icon_emoji': u':cat:', 'link_names': 1,
                # }))
            except:
                continue
    elif purpose == 'repayment_and_new_order':
        # requests.post(WEB_HOOK_URL, data = json.dumps({
        #     'text': '返済注文と新規注文をします',
        #     'username': u'サイン', 'icon_emoji': u':cat:', 'link_names': 1,
        # }))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-speed-order'))).click()
        for i in range(try_count):
            try:
                driver.save_screenshot('repayment-start.png')
                operation_repayment_order(i+1) # 返済できるまでプルダウン（限月）の下キーを押す回数を増やして試行する
                # requests.post(WEB_HOOK_URL, data = json.dumps({
                #     'text': '返済注文を完了しました',
                #     'username': u'サイン', 'icon_emoji': u':cat:', 'link_names': 1,
                # }))
            except:
                continue
        operation_new_order('new_order', is_buy_sign)
        # requests.post(WEB_HOOK_URL, data = json.dumps({
        #     'text': '新規注文を完了しました',
        #     'username': u'サイン', 'icon_emoji': u':cat:', 'link_names': 1,
        # }))

    return response(request)

# ログイン
def operation_login():
    driver.get('https://trade.matsui.co.jp/mgap/login')
    driver.find_element_by_id('login-id').send_keys(USER_INFO["USER_ID"])
    driver.find_element_by_id('login-password').send_keys(USER_INFO["USER_PASS"])
    driver.find_element_by_class_name('local-nav-login__button').click()

# 建玉数の決定
def operation_get_realtime_deposit():
    global REALTIME_DEPOSIT
    global REALTIME_SHEET_NUM
    sheet_per_deposit = 750000 # いくらにつき1枚張りするか

    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'powerInfoMenuFutOp'))).click()
    time.sleep(2)
    REALTIME_DEPOSIT = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'powerInfoFutOpRealMgnDepoCapacity'))).text
    REALTIME_DEPOSIT = REALTIME_DEPOSIT.translate(str.maketrans({',':'', '円':''}))

    REALTIME_SHEET_NUM = 1 if int(REALTIME_DEPOSIT) < sheet_per_deposit else int(REALTIME_DEPOSIT) // sheet_per_deposit

# リアルタイム建玉情報を取得
def operation_get_realtime_contract():
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu-fut-op-repayment'))).click()
    time.sleep(5)

    try:
        # 建区分が売建or買建orなしか確認（.refundKbn）
        refundStatus = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".refundKbn"))).text
        if refundStatus == '買建':
            return 'buy'
        elif refundStatus == '売建':
            return 'sell'
        else:
            return 'none'
    except:
        return 'none'

# Cabeeの売買ステータスの確認
def call_cloud_function():
    url = "https://asia-northeast1-cabee-389803.cloudfunctions.net/signal"
    headers = {
        "Content-Type": "application/json",
    }
    data = {}
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=70)
    response_json = response.json()
    return response_json["sign"]

# 新規注文
def operation_new_order(purpose, is_buy_sign):
    order_kind = 'buy-orders' if is_buy_sign == True else 'sell-orders'
    order_kind2 = '.order-label.buy' if is_buy_sign == True else '.order-label.sell'

    if len(driver.find_element_by_class_name('common-key-input-field').get_attribute('value')) > 0:
        driver.find_element_by_class_name('dealing-type-new-futop').click()
    else:
        operation_pulldown('speed_order')
        print("pulldownを選択完了")

    time.sleep(5)
    driver.find_element_by_class_name('trade-unit-spinner').find_element_by_css_selector('.common-input.number-field').click()

    driver_actions = ActionChains(driver)
    driver_actions.send_keys(str(REALTIME_SHEET_NUM))
    driver_actions.perform()

    common_operation_order(order_kind, order_kind2, 'new_order')

# 返済注文
def operation_repayment_order(try_count = 1):
    order_kind = ''
    order_kind2 = ''

    operation_pulldown('speed_order', try_count)
    time.sleep(2)
    driver.save_screenshot('repayment-after-pulldown.png')
    driver.find_element_by_class_name('dealing-type-refund-futop').click()
    time.sleep(2)
    driver.find_element_by_id('fut-op-speed-order-input-position-list-button').click()

    if len(driver.find_elements_by_class_name('grid-body-empty')) == 0:
        order_kind = 'sell-orders'
        order_kind2 = '.order-label.sell'
    else:
        order_kind = 'buy-orders'
        order_kind2 = '.order-label.buy'
        driver.find_element_by_css_selector('.switch.sell-toggle').click()

    time.sleep(2)

    driver.find_element_by_class_name('select-position-btn').click()
    time.sleep(2)

    buttons = driver.find_elements_by_class_name('confirm-btn')
    buttons[len(buttons)-1].click()
    time.sleep(5)

    common_operation_order(order_kind, order_kind2, 'repayment_order')

# 注文の共通操作
def common_operation_order(order_kind, order_kind2, operation):
    if len(driver.find_element_by_class_name('common-key-input-field').get_attribute('value')) == 0:
        driver.find_element_by_class_name('common-omit-confirm-btn').click()
        driver.find_element_by_class_name('common-modal-confirm-btn').click()
        driver.find_element_by_class_name('common-key-input-field').click()
        driver_actions = ActionChains(driver)
        driver_actions.send_keys(USER_INFO["TRADE_PASS"])
        driver_actions.perform()

    driver.find_element_by_class_name('market-order').find_element_by_class_name(order_kind).click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, order_kind2))).click() #注文確定
    time.sleep(3)

# プルダウン操作
def operation_pulldown(page, try_count = 1):
    # 先物取引の選択
    future_trade_element = ""
    time.sleep(5)
    if len(driver.find_elements_by_class_name('index-select')) > 1:
        future_trade_element = driver.find_elements_by_class_name('index-select')[len(driver.find_elements_by_class_name('index-select'))-1]
    else:
        future_trade_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.index-select')))

    future_trade_element.click()
    driver_actions = ActionChains(driver)
    driver_actions.send_keys(Keys.DOWN)
    if page == 'speed_order':
        driver_actions.send_keys(Keys.DOWN)
    driver_actions.send_keys(Keys.ENTER)
    driver_actions.perform()

    # 直近のメジャー限月の選択
    contract_month_element = ""
    if len(driver.find_elements_by_class_name('del-month-select')) > 1:
        contract_month_element = driver.find_elements_by_class_name('del-month-select')[len(driver.find_elements_by_class_name('del-month-select'))-1]
    else:
        contract_month_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'del-month-select')))

    contract_month_element.click()
    # keydown_count = 1
    # if page == 'speed_order':
    #     contract_month_list = contract_month_element.text.split("\n")
    #     for i,month in enumerate(contract_month_list):
    #         if '03月' in month or '06月' in month or '09月' in month or '12月' in month:
    #             keydown_count += i
    #             break

    driver_actions = ActionChains(driver)
    # 建玉が見付かれるまでプルダウンの選択する回数を増やす（返済注文現在の操作）
    for i in range(try_count):
        driver_actions.send_keys(Keys.DOWN)
    driver_actions.send_keys(Keys.ENTER)
    driver_actions.perform()

# レスポンス
def response(request, error = None):
    if request:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }

            return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    if error:
        return (json.dumps({"response": "ok"}), 200, headers)
    else:
        return (json.dumps({"response": error}), 200, headers)

# trade_executor("")
