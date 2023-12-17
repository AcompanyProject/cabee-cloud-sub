import json, requests

def get_cabee_signal():
    url = "https://asia-northeast1-cabee-389803.cloudfunctions.net/signal"
    headers = {
        "Content-Type": "application/json",
    }
    data = {}
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=70)
    response_json = response.json()
    return response_json["sign"]
