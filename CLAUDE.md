# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

**metrix**は、様々な単位変換(長さ・重さ・温度、将来的には通貨)を行うシンプルなWebアプリケーションです。Claude Codeを活用したステップバイステップ開発とGoogle Cloud Runへのデプロイを学習目的で行うプロジェクトです。

- **言語**: Python 3.12+
- **フレームワーク**: FastAPI
- **テンプレートエンジン**: Jinja2
- **コンテナ化**: Docker
- **デプロイ先**: Google Cloud Run

## ブランチ戦略（GitHub Flow）

このプロジェクトは**GitHub Flow**を採用しています。

### 基本方針

- **mainブランチ**: 常にデプロイ可能な状態を保つ。リリース用ブランチ。
- **feature/issue-<番号>ブランチ**: 各issueに対応する作業用ブランチ。

### ワークフロー

```bash
# 1. 新しい作業を開始
git checkout main
git pull origin main
git checkout -b feature/issue-<番号>

# 2. 作業を進める
git add .
git commit -m "作業内容の説明

Closes #<番号>"

# 3. プッシュしてPR作成
git push origin feature/issue-<番号>
# GitHubでPull Requestを作成（ベース: main）

# 4. マージ後のクリーンアップ
git checkout main
git pull origin main
git branch -d feature/issue-<番号>
```

### リリース時のタグ作成

```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## 開発コマンド

### ローカル開発

```bash
# 仮想環境の作成・有効化
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt

# 開発サーバーの起動(自動リロード付き)
uvicorn main:app --reload --port 8080
```

### Docker

```bash
# Dockerイメージのビルド
docker build -t metrix .

# コンテナの起動
docker run -p 8080:8080 metrix
```

### テスト

```bash
# テストの実行
pytest

# カバレッジ付きテスト実行
pytest --cov=converters --cov=routers
```

### Google Cloud Runへのデプロイ

```bash
# プロジェクトの設定（YOUR-PROJECT-IDを実際のGCPプロジェクトIDに置き換える）
gcloud config set project YOUR-PROJECT-ID

# 必要なAPIの有効化（初回のみ）
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Cloud Runへのデプロイ
gcloud run deploy metrix \
  --source . \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated

# デプロイされたサービスの確認
gcloud run services describe metrix --region asia-northeast1

# ログの確認
gcloud run services logs read metrix --region asia-northeast1
```

## アーキテクチャ

### ディレクトリ構成

```
metrix/
├── main.py                 # FastAPIアプリケーションのエントリーポイント
├── requirements.txt        # Python依存パッケージ
├── Dockerfile
├── converters/            # 単位変換ロジック(コアビジネスロジック)
│   ├── length.py          # 長さ変換 (m, km, cm, mm, in, ft, yd, mi)
│   ├── weight.py          # 重さ変換 (g, kg, mg, lb, oz)
│   └── temperature.py     # 温度変換 (°C, °F, K)
├── routers/               # APIルートハンドラー
│   └── convert.py         # 変換APIエンドポイント
├── templates/             # Jinja2 HTMLテンプレート
│   └── index.html         # メインUI
├── static/                # 静的ファイル
│   ├── css/
│   └── js/
└── tests/                 # ユニットテスト
    ├── test_length.py
    ├── test_weight.py
    └── test_temperature.py
```

### 主要な設計原則

1. **関心の分離**: 変換ロジック(`converters/`)、APIルーティング(`routers/`)、プレゼンテーション層(`templates/`)を分離
2. **ステートレス変換**: すべての変換関数は入力値と単位を受け取り、変換結果を返す純粋関数
3. **カテゴリベースの構成**: 各変換カテゴリ(長さ・重さ・温度)ごとに独立したモジュール

### APIエンドポイント

| メソッド | パス | 目的 |
|---------|------|------|
| GET | `/` | メインUIの表示 |
| GET | `/health` | ヘルスチェック |
| POST | `/api/convert` | 単位変換の実行 |
| GET | `/api/units/{category}` | カテゴリ別の利用可能な単位一覧の取得 |

### 変換APIのリクエスト・レスポンス形式

**リクエスト**:
```json
{
  "value": 100,
  "from_unit": "m",
  "to_unit": "km",
  "category": "length"
}
```

**成功レスポンス**:
```json
{
  "success": true,
  "result": 0.1,
  "from_unit": "m",
  "to_unit": "km",
  "original_value": 100
}
```

**エラーレスポンス**:
```json
{
  "success": false,
  "error": "Invalid unit: xyz"
}
```

## 実装に関する注意事項

### 対応単位

- **長さ**: m, km, cm, mm, in, ft, yd, mi
- **重さ**: g, kg, mg, lb, oz
- **温度**: °C, °F, K

### 非機能要件

- レスポンスタイム目標: 200ms以内
- すべてのAPIエンドポイントで適切な入力バリデーションを実施
- 適切なHTTPステータスコードの使用(不正リクエスト: 400、サーバーエラー: 500)
- 基本的なリクエスト・レスポンスのログ出力
- Webフロントエンド用のCORS設定

### 将来のフェーズ

Phase 2では外部為替レートAPIを使用した通貨換算機能を追加予定。実装時の注意点:
- APIキーは環境変数で管理
- 外部API障害時の適切なエラーハンドリング
- API呼び出しを削減するための為替レート情報のキャッシング検討
