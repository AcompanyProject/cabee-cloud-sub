#!/bin/bash
# パラメータの受け取り
USER_ID=$1
USER_PASS=$2
TRADE_PASS=$3
WEB_HOOK_URL=$4

# 必要なファイルの解凍
unzip selenium_chrome/source/headless-chromium.zip -d selenium_chrome/source

# 不要なファイル削除
rm pandas_numpy/pack.zip
rm selenium_chrome/pack.zip
rm selenium_chrome/source/headless-chromium.zip
rm tensorflow2.0/pack.zip

cd selenium_chrome/source

# 必要なPythonパッケージのインストール
pip3 install jpholiday pytz firebase_admin firestore load_dotenv

# .env ファイルの作成
echo "USER_ID=${USER_ID}" > .env
echo "USER_PASS=${USER_PASS}" >> .env
echo "TRADE_PASS=${TRADE_PASS}" >> .env
echo "WEB_HOOK_URL=${WEB_HOOK_URL}" >> .env

# プロジェクトIDの取得
PROJECT_ID=$(gcloud config get-value project)

# プロジェクトIDの設定
gcloud config set project $PROJECT_ID

# Google Cloud Functionのデプロイ
gcloud functions deploy trade_executor --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
