import time
import pytz
from datetime import datetime
from log import slack
from modules import new_order, repayment_order, utils
from api import cabee_signal

def operation_check_sign(driver, realtime_contract, sheet_num):
    try:
        contract_sign_map = {
            ('none', 'sell'): ('new_order', False),
            ('none', 'buy'): ('new_order', True),
            ('buy', 'none'): ('repayment_order', False),
            ('sell', 'none'): ('repayment_order', True),
            ('buy', 'sell'): ('repayment_and_new_order', False),
            ('sell', 'buy'): ('repayment_and_new_order', True),
        }

        for reload_count in range(15):
            now = datetime.now(pytz.timezone('Asia/Tokyo'))
            now_str = now.strftime("%H:%M:%S")

            # 複数回連続でサインを取得
            signal_json = cabee_signal.get_cabee_signal()
            sign = signal_json['sign']
            is_handover_order = signal_json['is_handover_order']
            purpose = None

            if reload_count == 0:
                slack.send_message('notice', f'{now_str} ... sign: {sign}, sheet_num: {sheet_num}, realtime_contract: {realtime_contract}')

            if is_handover_order:
                # SQ日の夜間
                slack.send_message('notice', f'【SQ日の夜間です】 {now_str} ... sign: {sign}, sheet_num: {sheet_num}')
                operation_handover_trade(driver, realtime_contract, sign, sheet_num)
                break
            else:
                purpose, is_buy_sign = contract_sign_map.get((realtime_contract, sign), (None, None))

                if purpose == 'new_order':
                    new_order.operation_new_order(driver, purpose, is_buy_sign, sheet_num)
                elif purpose == 'repayment_order':
                    repayment_order.operation_repayment_order(driver, purpose)
                elif purpose == 'repayment_and_new_order':
                    repayment_order.operation_repayment_order(driver, purpose)
                    new_order.operation_new_order(driver, 'new_order', is_buy_sign, sheet_num)

            if purpose is not None or not utils.is_in_update_graph(now_str):
                break
            
            time.sleep(2)
    except Exception as err:
        slack.send_message('error', 'operation_check_sign関数でエラー Error: ' + str(err))
        raise

# SQ日の引き継ぎ注文
def operation_handover_trade(driver, sign, sheet_num):
    try:
        contract_sign_map = {
            ('sell'): ('new_order', False),
            ('buy'): ('new_order', True),
        }

        purpose, is_buy_sign = contract_sign_map.get((sign), (None, None))

        if purpose == 'new_order':
            slack.send_message('notice', 'SQで建玉が自動決済されているため、新規注文を行います')
            new_order.operation_new_order(driver, purpose, is_buy_sign, sheet_num)
    except Exception as err:
        slack.send_message('error', 'operation_handover_trade関数でエラー Error: ' + str(err))
        raise