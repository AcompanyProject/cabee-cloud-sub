
from datetime import datetime, timedelta
from log import slack

def is_trader_run_condition(signal_res):
    if not is_trading_time(signal_res):
        slack.send_message('notice', '取引時間外')
        return False
    return True

def is_trading_time(signal_res):
    date_now = datetime.now() + timedelta(hours=9)
    current_time = date_now.strftime("%H:%M")

    start_time_str = signal_res["start_time"]
    end_time_str = signal_res["end_time"]
    
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
    current_time = datetime.strptime(current_time, "%H:%M").time()

    return start_time <= current_time <= end_time
