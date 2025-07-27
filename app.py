# app.py (最終・完全版)

from flask import Flask, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename
import os
import urllib.parse
from deepface import DeepFace
import numpy as np
from scipy.spatial.distance import cosine
import pickle
import cv2
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

MODEL_NAME = "SFace"
EMBEDDING_FILE = "celebrity_embeddings.pkl" # ローカルにダウンロードして使う

# --- Google Driveからファイルをダウンロードする関数 ---
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download&confirm=1"
    session = requests.Session()
    response = session.get(URL, params={"id": id}, stream=True)
    
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            params = {'id': id, 'confirm': value}
            response = session.get(URL, params=params, stream=True)
            break
            
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# --- アプリ起動時に一度だけデータベースファイルをダウンロード ---
DRIVE_FILE_ID = os.environ.get('GOOGLE_DRIVE_FILE_ID')
if DRIVE_FILE_ID and not os.path.exists(EMBEDDING_FILE):
    print(f"Downloading database file from Google Drive (ID: {DRIVE_FILE_ID})...")
    download_file_from_google_drive(DRIVE_FILE_ID, EMBEDDING_FILE)
    print("Download complete.")

# --- 顔認識のメイン関数 ---
def find_similar_face(uploaded_image_path):
    try:
        with open(EMBEDDING_FILE, 'rb') as f:
            celebrity_embeddings = pickle.load(f)
    except FileNotFoundError:
        return f"データベースファイル({EMBEDDING_FILE})が見つかりません。", 0, None, True
    
    try:
        img = cv2.imread(uploaded_image_path)
        if img is None:
            return "アップロードされた画像を読み込めませんでした。", 0, None, True
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        uploaded_embedding_objs = DeepFace.represent(img_path=img_rgb, model_name=MODEL_NAME, enforce_detection=True)
        uploaded_embedding = uploaded_embedding_objs[0]['embedding']
    except ValueError:
        return "顔が検出できませんでした。別の写真でお試しください。", 0, None, True
    except Exception as e:
        return f"予期せぬエラーが発生しました: {e}", 0, None, True

    best_match_name = None
    highest_similarity = -1
    for celeb in celebrity_embeddings:
        celeb_embedding = celeb['embedding']
        similarity = 1 - cosine(np.array(uploaded_embedding), np.array(celeb_embedding))
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match_name = celeb['name']
    
    similarity_percent = (highest_similarity + 1) / 2 * 100
    encoded_name = urllib.parse.quote(best_match_name)
    wiki_url = f"https://ja.wikipedia.org/wiki/{encoded_name}"
    return best_match_name, similarity_percent, wiki_url, False

# --- Webページのルーティング ---
@app.route('/')
def index(): return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files: return redirect(request.url)
    file = request.files['file']
    if file.filename == '': return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        name, score, wiki_url, is_error = find_similar_face(filepath)
        image_path_for_html = os.path.join('uploads', filename)
        return render_template('result.html', name=name, score=score, wiki_url=wiki_url, image_path=image_path_for_html, is_error=is_error)

# --- HTMLテンプレートの定義 ---
os.makedirs('templates', exist_ok=True)
if not os.path.exists('templates/index.html'):
    index_html = """
    <!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>芸能人そっくりさん判定</title><style>body{font-family:sans-serif;text-align:center;margin-top:50px;} h1{color:#333;} form{margin-top:30px;} input[type=file]{border:1px solid #ccc;padding:10px;} button{background-color:#4CAF50;color:white;padding:12px 20px;border:none;border-radius:4px;cursor:pointer;font-size:16px;} button:hover{background-color:#45a049;}</style></head><body><h1>芸能人そっくりさん判定アプリ</h1><p>あなたの顔がどの芸能人に似ているか判定します。</p><form action="/predict" method="post" enctype="multipart/form-data"><input type="file" name="file" accept="image/*" required><br><br><button type="submit">判定する</button></form></body></html>
    """
    with open('templates/index.html', 'w', encoding='utf-8') as f: f.write(index_html)

if not os.path.exists('templates/result.html'):
    result_html = """
    <!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8"><title>判定結果</title><style>body{font-family:sans-serif;text-align:center;margin-top:50px;} h1,h2{color:#333;} .result-box{border:1px solid #ddd;padding:20px;margin:20px auto;max-width:400px;border-radius:8px;} .error{color:red;} a{color:#1a73e8;text-decoration:none;} a:hover{text-decoration:underline;}</style></head><body><h1>判定結果</h1><div class="result-box">{% if is_error %}<p class="error">エラー: {{ name }}</p>{% else %}<p>あなたに最も似ている芸能人は...</p><h2>{{ name }} さんです！</h2><p>(類似度: {{ score | round(2) }} %)</p><p><a href="{{ wiki_url }}" target="_blank" rel="noopener noreferrer"><b>{{ name }}さんについてもっと知る (Wikipedia)</b></a></p>{% endif %}<hr><p><b>あなたがアップロードした画像:</b></p><img src="{{ url_for('static', filename=image_path) }}" width="200" style="border-radius:8px;"></div><br><a href="/">もう一度試す</a></body></html>
    """
    with open('templates/result.html', 'w', encoding='utf-8') as f: f.write(result_html)

# --- Renderで実行するための設定 ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))