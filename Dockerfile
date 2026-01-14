# Python 3.12ベースイメージを使用
FROM python:3.12-slim

# 作業ディレクトリの設定
WORKDIR /app

# 依存パッケージのインストール（キャッシュ効率化のため先に実行）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードのコピー
COPY . .

# ポート8080の公開
EXPOSE 8080

# uvicornでアプリケーションを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
