import json
from datetime import datetime, timedelta

def is_check_trading():
    try:
        # 取引開始時刻から4分以内ならtrue, それより時間が経っていればfalseを返す
        with open('log/status.json', 'r') as f:
            data = json.load(f)

        trade_start = datetime.strptime(data['trade_start'], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        return (now - trade_start) <= timedelta(minutes=4)
    except Exception as err:
        print("is_check_trading関数でエラー:" + str(err))
        raise

def write_trade_time():
    # 取引開始時刻をjsonに記録しておく
    try:
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        data = { 'trade_start': now_str }

        with open('log/status.json', 'w') as f:
            json.dump(data, f)
    except Exception as err:
        print("write_start_time通知関数でエラー:" + str(err))
        raise
