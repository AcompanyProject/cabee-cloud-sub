import os, random, json, requests
from selenium import webdriver
from modules import login, deposit, contract, order_admin
from api import cabee_signal
from log import slack

# download_dir = "/home/mjt_not_found_404/cabee-cloud-sub/selenium_chrome/source/Downloads"
# prefs = { 'download.prompt_for_download': False, 'download.directory_upgrade': True }
# params = { 'cmd': 'Page.setDownloadBehavior', 'params': { 'behavior': 'allow', 'downloadPath': download_dir }}
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

options = [
    '--headless',
    '--disable-gpu',
    '--window-size=1920x1080',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--hide-scrollbars',
    '--enable-logging',
    '--log-level=0',
    '--v=99',
    '--single-process',
    '--ignore-certificate-errors',
    'user-agent=' + UA
]

for option in options:
    chrome_options.add_argument(option)

# chrome_options.add_experimental_option('prefs', prefs) # headlessモードでのダウンロードを可能にする
chrome_options.binary_location = os.getcwd() + "/headless-chromium"
driver = webdriver.Chrome(os.getcwd() + "/chromedriver", options=chrome_options)
driver.command_executor._commands["send_command"] = ('POST', '/session/$sessionId/chromium/send_command')
# driver.execute("send_command", params)

def trade_executor(request):
    sign = cabee_signal.get_cabee_signal() # サイン取得
    # print("sign: " + sign)

    login.operation_login(driver) # ログイン
    # print("ログインしました")

    sheet_num = deposit.operation_get_deposit(driver) # 建玉枚数取得
    # print("sheet_num: " + str(sheet_num))

    ### テスト ###
    # sign = 'buy'
    # sheet_num = 1
    ############

    realtime_contract, contractAmt_total = contract.operation_get_contract(driver) # 保持中の建玉情報（売りor買い）を取得
    # print("建玉種類: " + str(realtime_contract) + ', 建玉数: ' + str(contractAmt_total))

    order_admin.operation_switch_trade(driver, realtime_contract, sign, sheet_num) # 取引

    return response(request)

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

trade_executor("")
