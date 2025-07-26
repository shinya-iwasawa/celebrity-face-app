# app.py (Render対応版)

import os
import requests
# ... (他のimport文)

# ... (Flaskアプリの設定)

# --- データベースファイルのダウンロード処理 ---
DRIVE_FILE_ID = os.environ.get('GOOGLE_DRIVE_FILE_ID') # 環境変数からID取得
EMBEDDING_FILE = "celebrity_embeddings.pkl"

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download&confirm=1"
    session = requests.Session()
    response = session.get(URL, params={"id": id}, stream=True)
    
    # 初回アクセス時の確認ページをハンドル
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = {'id': id, 'confirm': value}
            response = session.get(URL, params=params, stream=True)
            break
            
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# アプリ起動時に一度だけデータベースファイルをダウンロード
if DRIVE_FILE_ID and not os.path.exists(EMBEDDING_FILE):
    print(f"Downloading database file from Google Drive (ID: {DRIVE_FILE_ID})...")
    download_file_from_google_drive(DRIVE_FILE_ID, EMBEDDING_FILE)
    print("Download complete.")

# --- find_similar_face 関数の修正 ---
# データベースファイルのパスをローカルのパスに変更
def find_similar_face(uploaded_image_path):
    try:
        # with open(os.path.join(DRIVE_PATH, EMBEDDING_FILE), 'rb') as f:
        with open(EMBEDDING_FILE, 'rb') as f: # ← この行を修正
             celebrity_embeddings = pickle.load(f)
    # ... (以降の関数の中身は同じ)

# ... (Flaskのルーティング部分は同じ)

# ... (if __name__ == '__main__': の部分はRenderでは不要なので削除してもOK)