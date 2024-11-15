#!/bin/bash

# パラメータの受け取り
USER_ID=$1
USER_PASS=$2
TRADE_PASS=$3
MY_PROJECT_ID=$4
WEB_HOOK_URL=$5
WEB_HOOK_URL_NOT_FOUND=$6

# 必要なファイルの解凍
unzip selenium_chrome/source/headless-chromium.zip -d selenium_chrome/source

# 不要なファイル削除
rm pandas_numpy/pack.zip
rm selenium_chrome/pack.zip
rm selenium_chrome/source/headless-chromium.zip
rm tensorflow2.0/pack.zip

cd selenium_chrome/source

# 必要なPythonパッケージのインストール
pip3 install -r requirements.txt

# .env ファイルの作成
echo "USER_ID=${USER_ID}" > .env
echo "USER_PASS=${USER_PASS}" >> .env
echo "TRADE_PASS=${TRADE_PASS}" >> .env
echo "MY_PROJECT_ID=${MY_PROJECT_ID}" >> .env
echo "WEB_HOOK_URL=${WEB_HOOK_URL}" >> .env
if [ ! -z "$WEB_HOOK_URL_NOT_FOUND" ]; then
    echo "WEB_HOOK_URL_NOT_FOUND=${WEB_HOOK_URL_NOT_FOUND}" >> .env
fi

# Firestoreの初期設定
python3 log/create_firestore_documents.py

# gcloud設定
gcloud config set project ${MY_PROJECT_ID}

# Google Cloud Functionのデプロイ
echo "Deploying Cloud Function..."
if ! gcloud functions deploy trader --runtime python312 --trigger-http --region asia-northeast1 --memory 512MB --timeout 540s; then
  echo "Deployment failed."
  exit 1
fi
echo "Cloud Function deployed successfully."

# Cloud Schedulerのジョブを作成
declare -A SCHEDULES
SCHEDULES=(
  ["trader"]="*/5 * * * *"
)

echo "Creating Cloud Scheduler jobs..."
for NAME in "${!SCHEDULES[@]}"; do
  echo "Creating job: ${NAME}"
  gcloud scheduler jobs create http ${NAME} \
    --schedule="${SCHEDULES[$NAME]}" \
    --time-zone="Asia/Tokyo" \
    --uri="https://asia-northeast1-${MY_PROJECT_ID}.cloudfunctions.net/trader" \
    --oidc-service-account-email="${MY_PROJECT_ID}@appspot.gserviceaccount.com" \
    --oidc-token-audience="https://asia-northeast1-${MY_PROJECT_ID}.cloudfunctions.net/trader" \
    --attempt-deadline="10m" \
    --location="asia-northeast1"
done
echo "Cloud Scheduler jobs created successfully."
