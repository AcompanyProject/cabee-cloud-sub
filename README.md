# cabee-cloud-sub

## 初期設定

### Google Cloud Function のターミナルで以下を実行

"ログイン ID" "ログイン PASS" "取引暗礁番号" "Web_hook_url" は各自の値を当てはめる

```
git clone git@github.com:AcompanyProject/cabee-cloud-sub.git
cd gcf-packs/selenium_chrome/source
chmod +x deploy.sh
./deploy.sh "ログインID" "ログインPASS" "取引暗礁番号" "Web_hook_url"
```

### package install

```
pip3 install jpholiday pytz firebase_admin firestore load_dotenv
```

## GCF 上でデプロイ

※ 注意: デプロイ時にテストが走って売買が実行される可能性がある。
デバックする場合:

- Google Scheduler を一時停止すること
- サインの切り替わりのタイミング（出来れば買い売りサインがないとき）にデプロイすること

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
