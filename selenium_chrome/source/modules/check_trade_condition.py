from log import slack

def is_trader_run_condition(signal_res):
    if signal_res["trade_type"] == "none":
        slack.send_message('notice', '取引時間外')
        return False
    elif signal_res["is_graph_updating"] is True:
        slack.send_message('notice', 'グラフ更新作業中のため一時停止中')
        return False
    return True
