from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import functions_framework
from google.cloud import firestore
from log import slack

load_dotenv()
MY_PROJECT_ID = os.environ.get("MY_PROJECT_ID")
DB = firestore.Client(project=MY_PROJECT_ID)

@functions_framework.cloud_event
# 取引時刻の更新
def update_trade_time(trade_kind):
    try:
        now = datetime.now()
        datetime_str = now.strftime("%Y/%m/%d %H:%M:%S")

        data = {
            "datetime": datetime_str,
        }

        doc_ref = DB.collection("trader").document(trade_kind)
        doc_ref.set(data)
    except Exception as err:
        slack.send_message('warning', 'update_trade_time Error: ' + str(err))
        raise

# 最新の取引時刻から4分以上経過しているか確認
def check_duplication_trade(trade_kind):
    try:
        doc_ref = DB.collection("trader").document(trade_kind)
        doc = doc_ref.get()

        trade_time = datetime.strptime(doc.to_dict()["datetime"], "%Y/%m/%d %H:%M:%S")
        now = datetime.now()
        can_trade = (now - trade_time) >= timedelta(minutes=4)
        slack.send_message('notice', f'前回の注文時刻: {trade_time}, 現在時刻: {now}')

        return can_trade
    except Exception as err:
        slack.send_message('warning', 'check_duplication_trade Error: ' + str(err))
        raise

# 最新の取引時刻をリセット
def refresh_trade_time(trade_kind):
    try:
        data = {
            "datetime": "2024/01/22 06:28:09",
        }

        doc_ref = DB.collection("trader").document(trade_kind)
        doc_ref.set(data)
    except Exception as err:
        slack.send_message('warning', 'refresh_trade_time Error: ' + str(err))
        raise
