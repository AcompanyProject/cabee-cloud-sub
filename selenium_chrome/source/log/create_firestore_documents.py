from google.cloud import firestore

try:
    # Firestoreクライアントの初期化
    db = firestore.Client()

    # コレクションとドキュメントの作成
    collections = ['new_order', 'repayment_order']
    for collection in collections:
        doc_ref = db.collection('trader').document(collection)
        doc_ref.set({
            'datetime': '2024/01/22 06:28:09'
        })
except Exception as err:
    print(f"Firestoreの初期設定中にエラーが発生しました: {err}")
    raise
