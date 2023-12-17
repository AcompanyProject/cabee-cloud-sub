# cabee-cloud-sub

## 初期設定

### 解凍

```
cd cabee-cloud-sub/selenium_chrome/source
unzip headless-chromium.zip
```

### package install

```
pip3 install jpholiday pytz firebase_admin firestore load_dotenv
```

## GCF 上でデプロイ

```
// main.pyの置き場所まで移動する
cd gcf-packs/selenium_chrome/source

// deploy
gcloud functions deploy handler --runtime python37 --trigger-http --region asia-northeast1 --memory 512MB
```

## その他

### 稼働開始のタイミング

sign が発生してないときに Cloud Scheduler を実行してください

### スクリーンショットを取る時に文字化けするのを防ぐ

driver.save_screenshot

```
$ sudo apt install fonts-ipafont-gothic
```
