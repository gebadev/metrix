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

### Dockerを使用する場合（推奨）

```bash
# イメージのビルド
docker build -t metrix .

# コンテナの起動
docker run -p 8080:8080 metrix
```

ブラウザで http://localhost:8080 にアクセスしてアプリケーションを確認できます。

### ローカル環境で実行する場合

#### 1. リポジトリのクローン

```bash
git clone https://github.com/gebadev/metrix.git
cd metrix
```

#### 2. 仮想環境の作成と有効化

```bash
# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化
# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

#### 3. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

#### 4. 開発サーバーの起動

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

## Google Cloud Runへのデプロイ

### 前提条件

- Google Cloud Platform（GCP）アカウント
- gcloudコマンドラインツールのインストールと認証
- プロジェクトIDの準備

### デプロイ手順

#### 1. gcloudの認証とプロジェクト設定

```bash
# gcloudにログイン
gcloud auth login

# プロジェクトを設定（YOUR-PROJECT-IDを実際のGCPプロジェクトIDに置き換えてください）
gcloud config set project YOUR-PROJECT-ID

# Cloud Run APIを有効化（初回のみ）
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### 2. Cloud Runへのデプロイ

```bash
# ソースコードから直接デプロイ
gcloud run deploy metrix \
  --source . \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated
```

デプロイオプションの説明:
- `--source .`: カレントディレクトリのソースコードを使用（Dockerfileが自動検出される）
- `--platform managed`: フルマネージドのCloud Runを使用
- `--region asia-northeast1`: 東京リージョンにデプロイ
- `--allow-unauthenticated`: 認証なしでアクセス可能にする（公開アプリケーション）

#### 3. デプロイ後の確認

デプロイが完了すると、サービスURLが表示されます:

```
Service [metrix] revision [metrix-00001-xxx] has been deployed and is serving 100 percent of traffic.
Service URL: https://metrix-xxxxxxxxxx-an.a.run.app
```

ブラウザでこのURLにアクセスして、アプリケーションが正常に動作することを確認します。

#### 4. サービスの管理

```bash
# サービスの一覧表示
gcloud run services list

# サービスの詳細情報を表示
gcloud run services describe metrix --region asia-northeast1

# ログの確認
gcloud run services logs read metrix --region asia-northeast1

# サービスの削除（必要な場合）
gcloud run services delete metrix --region asia-northeast1
```

### トラブルシューティング

デプロイ時にエラーが発生した場合:

1. **ビルドエラー**: Dockerfileの構文やPythonの依存関係を確認
2. **権限エラー**: GCPプロジェクトの権限設定を確認
3. **リージョンエラー**: 指定したリージョンがCloud Runで利用可能か確認

詳細なログは以下のコマンドで確認できます:

```bash
gcloud run services logs read metrix --region asia-northeast1 --limit 50
```

## ライセンス

このプロジェクトは学習目的で作成されています。