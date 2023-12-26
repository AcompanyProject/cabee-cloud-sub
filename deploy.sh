#!/bin/bash
# パラメータの受け取り
USER_ID=$1
USER_PASS=$2
TRADE_PASS=$3
WEB_HOOK_URL=$4

# ディレクトリの変更
cd cabee-cloud-sub/selenium_chrome/source

# 必要なファイルの解凍
unzip headless-chromium.zip

# 必要なPythonパッケージのインストール
pip3 install jpholiday pytz firebase_admin firestore load_dotenv

# .env ファイルの作成
echo "USER_ID=${USER_ID}" > .env
echo "USER_PASS=${USER_PASS}" >> .env
echo "TRADE_PASS=${TRADE_PASS}" >> .env
echo "WEB_HOOK_URL=${WEB_HOOK_URL}" >> .env

# Google Cloud Functionのデプロイ
gcloud functions deploy trade_executor --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
