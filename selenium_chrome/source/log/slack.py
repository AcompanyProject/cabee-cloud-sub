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

        webhook_urls = []

        default_webhook = os.environ.get("WEB_HOOK_URL")
        not_found_webhook = os.environ.get("WEB_HOOK_URL_NOT_FOUND")

        if default_webhook:
            webhook_urls.append(default_webhook)
        if not_found_webhook:
            webhook_urls.append(not_found_webhook)

        for webhook_url in webhook_urls:
            requests.post(
                webhook_url,
                data = json.dumps({
                    'username': user_name[type],
                    'text': message,
                    'icon_emoji': (icon[type]),
                })
            )
    except Exception as err:
        print("slack通知関数でエラー:" + str(err))
        raise
