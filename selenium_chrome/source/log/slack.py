import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def send_message(type, message):
    try:
        icon = {
            'notice': ':cat',
            'warning': ':warning:',
            'error': ':rotating_light:'
        }

        user_name = {
            'notice': 'お知らせ',
            'warning': '警告（連続で通知される場合は要確認）',
            'error': 'エラー（要確認）'
        }

        if type == 'error':
            message = '<!here> ' + message

        requests.post(
            os.environ.get("WEB_HOOK_URL"),
            data = json.dumps({
                'username': user_name[type],
                'text': message ,
                'icon_emoji': (icon[type]),
            })
        )
    except Exception as err:
        print("slack通知関数でエラー:" + str(err))
        raise
