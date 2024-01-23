# cabee-cloud-sub
## lint
```
ruff --fix ./log/* ./modules/* ./main.py
ruff check ./log/* ./modules/* ./main.py
```

## GCF 上でデプロイ
main.pyの階層で実行
```
gcloud functions deploy trader --runtime python312 --trigger-http --region asia-northeast1 --memory 512MB --timeout 540s --docker-registry=artifact-registry
```

## その他
### スクリーンショットを取る時に文字化けするのを防ぐ

driver.save_screenshot

```
$ sudo apt install fonts-ipafont-gothic
```
