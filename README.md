# cabee-cloud-sub
## lint
```
ruff --fix ./log/* ./modules/* ./main.py
ruff check ./log/* ./modules/* ./main.py
```

## 初期設定
```
chmod +x deploy.sh;
$ ./deploy.sh "ログインID" "ログインPASS" "取引暗礁番号" "project_id" "web_hook_url"
または
$ ./deploy.sh "ログインID" "ログインPASS" "取引暗礁番号" "project_id" "web_hook_url" "web_hook_url_for_notfound"


途中で「Allow unauthenticated invocations of new function [trade_executor]? (y/N)? 」と表示されたら、
「N」と入力してエンター
```

## GCF 上でデプロイ
main.pyの階層で実行
```
gcloud functions deploy trader --runtime python312 --trigger-http --region asia-northeast1 --memory 512MB --timeout 540s

# 並列実行
gcloud functions deploy trader \
  --runtime python312 \
  --trigger-http \
  --region asia-northeast1 \
  --memory 512MB \
  --timeout 1000s \
  --min-instances 1 \
  --max-instances 2 \
  --concurrency 1 \
```

## その他
### スクリーンショットを取る時に文字化けするのを防ぐ

driver.save_screenshot

```
$ sudo apt install fonts-ipafont-gothic
```
