import requests
import json

WEB_HOOK_URL = "https://hooks.slack.com/services/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"  # あなたのWebhook URL

def send_message(type, username, message):
    icon = {
        'notice': ':cat',
        'error': ':fire:'
    }

    requests.post(WEB_HOOK_URL, data = json.dumps({
        'text': message,
        'username': username,
        'icon_emoji': (icon[type]),
    }))
