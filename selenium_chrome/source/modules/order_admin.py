import time
from log import slack
from modules import new_order, repayment_order
from api import cabee_signal

def operation_check_sign(driver, contract_type, sheet_num, isSQ):
    # 各ケースごとの操作方法をまとめた辞書
    # 現在の建区分, サイン, SQフラグ => 売買操作の種類, 取引区分
    contract_sign_map = {
        ('none', 'buy', False): ('new_order', True),
        ('none', 'sell', False): ('new_order', False),
        ('buy', 'none', False): ('repayment_order', False),
        ('sell', 'none', False): ('repayment_order', True),
        ('sell', 'buy', False): ('repayment_and_new_order', True),
        ('buy', 'sell', False): ('repayment_and_new_order', False),
        ('buy', 'buy', False): (None, None),
        ('sell', 'sell', False): (None, None),
        ('none', 'buy', True): ('new_order', True),
        ('none', 'sell', True): ('new_order', False),
        ('buy', 'none', True): (None, None),
        ('sell', 'none', True): (None, None),
        ('sell', 'buy', True): ('new_order', True),
        ('buy', 'sell', True): ('new_order', False),
        ('buy', 'buy', True): ('new_order', True),
        ('sell', 'sell', True): ('new_order', False),
        ('both', 'buy', False): ('repayment_order', True),
        ('both', 'sell', False): ('repayment_order', False),
        ('both', 'none', False): ('repayment_order', None),
        ('both', 'buy', True): ('new_order', True),
        ('both', 'sell', True): ('new_order', False),
        ('both', 'none', True): (None, None),
    }

    if contract_type == "both":
        slack.send_message('warning', "買建玉と売建玉の両方が入っています")

    if isSQ:
        slack.send_message('notice', "本日がSQ日であることを検知しました")

    for reload_count in range(15):
        # 複数回連続でサインを取得（なるべく最速で売買を開始したいので）
        signal_json = (cabee_signal.get_cabee_signal())['sign']
        if reload_count == 0:
            slack.send_message('notice', f'sign: {signal_json}, sheet_num: {sheet_num}, contract_type: {contract_type}')

        purpose, is_buy_sign = contract_sign_map.get((contract_type, signal_json, isSQ), (None, None))

        if purpose == 'new_order':
            new_order.operation_new_order(driver, purpose, is_buy_sign, sheet_num)
        elif purpose == 'repayment_order':
            repayment_order.operation_repayment_order(driver, purpose)
        elif purpose == 'repayment_and_new_order':
            repayment_order.operation_repayment_order(driver, purpose)
            new_order.operation_new_order(driver, 'new_order', is_buy_sign, sheet_num)
        else:
            print("なにもしない")

        if purpose is not None:
            break

        time.sleep(2)
