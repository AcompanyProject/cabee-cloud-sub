# cabee-cloud-sub
初期設定
```
cd cabee-cloud-sub/selenium_chrome/source
unzip headless-chromium.zip
```

デプロイ
```
gcloud functions deploy trade_executor --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
```
