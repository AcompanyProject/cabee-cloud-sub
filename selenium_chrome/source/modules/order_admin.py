from datetime import datetime
from log import slack
from modules import new_order, repayment_order

now = datetime.now()
now_str = now.strftime("%H:%M:%S")
contract_sign_map = {
    ('none', 'sell'): ('new_order', False),
    ('none', 'buy'): ('new_order', True),
    ('buy', 'none'): ('repayment_order', False),
    ('sell', 'none'): ('repayment_order', True),
    ('buy', 'sell'): ('repayment_and_new_order', False),
    ('sell', 'buy'): ('repayment_and_new_order', True),
}

def operation_switch_trade(driver, realtime_contract, sign, sheet_num):
    purpose, is_buy_sign = contract_sign_map.get((realtime_contract, sign), (None, None))
    slack.send_message('notice', f'{now_str} ... sign: {sign}, sheet_num: {sheet_num}, realtime_contract: {realtime_contract}')

    if purpose == 'new_order':
        new_order.operation_new_order(driver, purpose, is_buy_sign, sheet_num)
    elif purpose == 'repayment_order':
        repayment_order.operation_repayment_order(driver, purpose)
    elif purpose == 'repayment_and_new_order':
        repayment_order.operation_repayment_order(driver, purpose)
        new_order.operation_new_order(driver, 'new_order', is_buy_sign, sheet_num)

####テスト注文#####
def test_operation_switch_trade(driver, realtime_contract, purpose_test, is_buy_sign_test, sheet_num_test):
    slack.send_message(
        'notice',
        f'テスト注文します: {now_str} ... purpose_test: {purpose_test}, is_buy_sign_test: {is_buy_sign_test}, sheet_num: {sheet_num_test}, realtime_contract: {realtime_contract}'
    )
    if purpose_test == 'new_order':
        new_order.operation_new_order(driver, purpose_test, is_buy_sign_test, sheet_num_test)
    elif purpose_test == 'repayment_order':
        repayment_order.operation_repayment_order(driver, purpose_test)
    elif purpose_test == 'repayment_and_new_order':
        repayment_order.operation_repayment_order(driver, purpose_test)
        new_order.operation_new_order(driver, 'new_order', is_buy_sign_test, sheet_num_test)

# SQ日の引き継ぎ注文
def operation_handover_trade(driver, sign, sheet_num):
    contract_sign_map = {
        ('sell'): ('new_order', False),
        ('buy'): ('new_order', True),
    }

    purpose, is_buy_sign = contract_sign_map.get((sign), (None, None))
    slack.send_message('notice', f'【SQ日の夜間です】 {now_str} ... sign: {sign}, sheet_num: {sheet_num}')

    if purpose == 'new_order':
        slack.send_message('notice', 'SQで建玉が自動決済されているため、新規注文を行います')
        new_order.operation_new_order(driver, purpose, is_buy_sign, sheet_num)
