from fastapi import FastAPI, UploadFile, File
import shutil
from deepface import DeepFace
import os

app = FastAPI()

# アップロードされたファイルを保存するディレクトリ
UPLOAD_DIR = "uploaded_images"
# 芸能人の顔画像が保存されているディレクトリ
DB_PATH = "celebrity_images"

# 起動時にディレクトリを作成
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DB_PATH, exist_ok=True)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    アップロードされた顔画像を、DB内の芸能人画像と比較して、最も似ている人物を返します。
    """
    # 1. アップロードされた画像を保存
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 2. 最も似ている顔をDBから探す
        # enforce_detection=False にして、画像中に顔が検出できない場合もエラーにしない
        dfs = DeepFace.find(
            img_path=file_path,
            db_path=DB_PATH,
            enforce_detection=False,
            silent=True # 処理中のログを抑制
        )

        # 3. 結果を整形
        if not dfs or dfs[0].empty:
            return {"error": "似ている顔が見つかりませんでした。"}

        # 最も類似度が高い（distanceが小さい）結果を取得
        most_similar = dfs[0].iloc[0]
        identity = most_similar["identity"]

        # "celebrity_images/名前/画像ファイル" から "名前" を抽出
        celebrity_name = os.path.basename(os.path.dirname(identity))
        
        return {"celebrity_name": celebrity_name}

    except Exception as e:
        return {"error": f"処理中にエラーが発生しました: {str(e)}"}
    finally:
        # 4. アップロードされたファイルを削除
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Celebrity Face Recognition API!"}
