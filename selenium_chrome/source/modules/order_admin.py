import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log import slack
from modules import login, deposit, contract, new_order, repayment_order

def operation_switch_trade(driver, realtime_contract, sign, sheet_num):
    # テスト
    realtime_contract = 'buy'
    sign = 'none'

    # パターン（17時くらいまで稼働させて、SQ跨ぎも対応させる）
    contract_sign_map = {
        ('none', 'sell'): ('new_order', False),
        ('none', 'buy'): ('new_order', True),
        ('buy', 'none'): ('repayment_order', False),
        ('sell', 'none'): ('repayment_order', True),
        ('buy', 'sell'): ('repayment_and_new_order', False),
        ('sell', 'buy'): ('repayment_and_new_order', True),
    }

    purpose, is_buy_sign = contract_sign_map.get((realtime_contract, sign), (None, None))

    if purpose == 'new_order':
        new_order.operation_new_order(driver, purpose, is_buy_sign, sheet_num)
    elif purpose == 'repayment_order':
        repayment_order.operation_repayment_order(driver, purpose, is_buy_sign)
    elif purpose == 'repayment_and_new_order':
        repayment_order.operation_repayment_order(driver, purpose, is_buy_sign)
        new_order.operation_new_order(driver, 'new_order', is_buy_sign, sheet_num)
