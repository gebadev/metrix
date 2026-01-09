# metrix

シンプルな単位変換Webアプリケーション

## 概要

**metrix**は、様々な単位変換（長さ・重さ・温度）を行うWebアプリケーションです。FastAPIとJinja2を使用して構築されています。

## 技術スタック

- **言語**: Python 3.12+
- **フレームワーク**: FastAPI
- **テンプレートエンジン**: Jinja2
- **サーバー**: uvicorn

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/gebadev/metrix.git
cd metrix
```

### 2. 仮想環境の作成と有効化

```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4. 開発サーバーの起動

```bash
uvicorn main:app --reload --port 8080
```

ブラウザで http://localhost:8080 にアクセスしてアプリケーションを確認できます。

## プロジェクト構成

```
metrix/
├── main.py                 # FastAPIアプリケーションのエントリーポイント
├── requirements.txt        # Python依存パッケージ
├── converters/            # 単位変換ロジック
├── routers/               # APIルートハンドラー
├── templates/             # Jinja2 HTMLテンプレート
├── static/                # 静的ファイル（CSS, JS）
└── tests/                 # ユニットテスト
```

## 開発

### 開発サーバーの起動（自動リロード有効）

```bash
uvicorn main:app --reload --port 8080
```

### テストの実行

```bash
pytest
```

## 対応予定の単位

- **長さ**: m, km, cm, mm, in, ft, yd, mi
- **重さ**: g, kg, mg, lb, oz
- **温度**: °C, °F, K

## ライセンス

このプロジェクトは学習目的で作成されています。