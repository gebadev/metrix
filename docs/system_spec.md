# metrix 機能仕様書

## 1. プロジェクト概要

### 1.1 プロジェクト名
**metrix**

### 1.2 概要
metrixは、様々な単位変換を行うシンプルなWebアプリケーションです。
学習目的で作成し、Claude Codeを活用したステップバイステップの開発とGoogle Cloud Runへのデプロイを体験します。

### 1.3 技術スタック
| 項目 | 技術 |
|------|------|
| 言語 | Python 3.12 |
| フレームワーク | FastAPI |
| テンプレートエンジン | Jinja2 |
| コンテナ | Docker |
| デプロイ先 | Google Cloud Run |

---

## 2. 機能要件

### 2.1 単位変換機能（Phase 1: 初期実装）

#### 2.1.1 長さの変換
以下の単位間で相互変換が可能:
- メートル (m)
- キロメートル (km)
- センチメートル (cm)
- ミリメートル (mm)
- インチ (in)
- フィート (ft)
- ヤード (yd)
- マイル (mi)

#### 2.1.2 重さの変換
以下の単位間で相互変換が可能:
- グラム (g)
- キログラム (kg)
- ミリグラム (mg)
- ポンド (lb)
- オンス (oz)

#### 2.1.3 温度の変換
以下の単位間で相互変換が可能:
- 摂氏 (°C)
- 華氏 (°F)
- ケルビン (K)

### 2.2 将来の拡張機能（Phase 2: 外部API連携）

#### 2.2.1 通貨換算
- 外部為替レートAPIを利用した通貨変換
- 主要通貨（USD, EUR, JPY, GBP等）のサポート

---

## 3. 画面仕様

### 3.1 メイン画面
```
+------------------------------------------+
|              metrix                       |
|         単位変換ツール                     |
+------------------------------------------+
|                                          |
|  [カテゴリ選択: 長さ ▼]                   |
|                                          |
|  +------------------+  +---------------+ |
|  | 入力値: [     ]  |  | 変換元: [m ▼] | |
|  +------------------+  +---------------+ |
|                                          |
|           ⇅ [変換ボタン]                  |
|                                          |
|  +------------------+  +---------------+ |
|  | 結果: [        ] |  | 変換先: [km▼] | |
|  +------------------+  +---------------+ |
|                                          |
+------------------------------------------+
```

### 3.2 UIコンポーネント
| コンポーネント | 説明 |
|---------------|------|
| カテゴリ選択 | 長さ/重さ/温度を選択するドロップダウン |
| 入力フィールド | 変換する数値を入力 |
| 変換元単位 | 入力値の単位を選択 |
| 変換先単位 | 変換後の単位を選択 |
| 変換ボタン | 変換を実行 |
| 結果表示 | 変換結果を表示（読み取り専用） |

---

## 4. API仕様

### 4.1 エンドポイント一覧

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/` | メイン画面を表示 |
| GET | `/health` | ヘルスチェック |
| POST | `/api/convert` | 単位変換を実行 |
| GET | `/api/units/{category}` | カテゴリ別の単位一覧を取得 |

### 4.2 単位変換API

#### リクエスト
```
POST /api/convert
Content-Type: application/json
```

```json
{
  "value": 100,
  "from_unit": "m",
  "to_unit": "km",
  "category": "length"
}
```

#### レスポンス（成功時）
```json
{
  "success": true,
  "result": 0.1,
  "from_unit": "m",
  "to_unit": "km",
  "original_value": 100
}
```

#### レスポンス（エラー時）
```json
{
  "success": false,
  "error": "Invalid unit: xyz"
}
```

### 4.3 単位一覧API

#### リクエスト
```
GET /api/units/length
```

#### レスポンス
```json
{
  "category": "length",
  "units": [
    {"code": "m", "name": "メートル"},
    {"code": "km", "name": "キロメートル"},
    {"code": "cm", "name": "センチメートル"},
    {"code": "mm", "name": "ミリメートル"},
    {"code": "in", "name": "インチ"},
    {"code": "ft", "name": "フィート"},
    {"code": "yd", "name": "ヤード"},
    {"code": "mi", "name": "マイル"}
  ]
}
```

---

## 5. 実装ステップ（Claude Code用）

以下の順序でステップバイステップで実装を進めます。

### Step 1: プロジェクト初期化
- [ ] プロジェクトディレクトリの作成
- [ ] 仮想環境のセットアップ
- [ ] 必要なパッケージのインストール（FastAPI, uvicorn, jinja2）
- [ ] requirements.txtの作成

### Step 2: 基本的なFastAPIアプリケーション
- [ ] main.pyの作成
- [ ] ヘルスチェックエンドポイントの実装
- [ ] 動作確認

### Step 3: 単位変換ロジックの実装
- [ ] converters/ディレクトリの作成
- [ ] 長さ変換ロジックの実装
- [ ] 重さ変換ロジックの実装
- [ ] 温度変換ロジックの実装
- [ ] ユニットテストの作成

### Step 4: APIエンドポイントの実装
- [ ] 単位変換APIの実装
- [ ] 単位一覧APIの実装
- [ ] エラーハンドリングの実装

### Step 5: フロントエンドの実装
- [ ] templatesディレクトリの作成
- [ ] index.htmlテンプレートの作成
- [ ] staticディレクトリの作成（CSS/JS）
- [ ] UIの実装

### Step 6: Docker化
- [ ] Dockerfileの作成
- [ ] .dockerignoreの作成
- [ ] ローカルでのDocker動作確認

### Step 7: Cloud Runへのデプロイ
- [ ] GCPプロジェクトの設定
- [ ] Cloud Buildの設定
- [ ] Cloud Runへのデプロイ
- [ ] 動作確認

### Step 8: （将来）外部API連携
- [ ] 為替レートAPIの調査・選定
- [ ] 通貨換算機能の追加
- [ ] 環境変数によるAPIキー管理

---

## 6. ディレクトリ構成

```
metrix/
├── main.py                 # FastAPIアプリケーションのエントリーポイント
├── requirements.txt        # Pythonパッケージ依存関係
├── Dockerfile             # Dockerイメージ定義
├── .dockerignore          # Docker除外ファイル
├── .gitignore             # Git除外ファイル
├── README.md              # プロジェクト説明
│
├── converters/            # 変換ロジック
│   ├── __init__.py
│   ├── length.py          # 長さ変換
│   ├── weight.py          # 重さ変換
│   └── temperature.py     # 温度変換
│
├── routers/               # APIルーター
│   ├── __init__.py
│   └── convert.py         # 変換API
│
├── templates/             # Jinja2テンプレート
│   └── index.html         # メイン画面
│
├── static/                # 静的ファイル
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
└── tests/                 # テスト
    ├── __init__.py
    ├── test_length.py
    ├── test_weight.py
    └── test_temperature.py
```

---

## 7. 非機能要件

### 7.1 パフォーマンス
- レスポンスタイム: 200ms以内

### 7.2 エラーハンドリング
- 不正な入力値に対する適切なエラーメッセージ
- APIエラー時のHTTPステータスコード（400, 500等）の適切な返却

### 7.3 セキュリティ
- 入力値のバリデーション
- CORSの適切な設定

### 7.4 ログ
- リクエスト/レスポンスの基本的なログ出力

---

## 8. 開発環境

### 8.1 必要なツール
- Python 3.12+
- Docker
- Google Cloud SDK
- Claude Code（開発支援）

### 8.2 ローカル起動コマンド
```bash
# 仮想環境の作成・有効化
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt

# 開発サーバーの起動
uvicorn main:app --reload --port 8080
```

### 8.3 Docker起動コマンド
```bash
# イメージのビルド
docker build -t metrix .

# コンテナの起動
docker run -p 8080:8080 metrix
```

---
