# K-Trend AutoBot - 開発者ガイド

このドキュメントは、K-Trend AutoBot の開発環境構築、デプロイメント、メンテナンスに関する詳細な手順を提供します。

## 📋 目次

1. [環境構築](#環境構築)
2. [秘密鍵の管理方法](#秘密鍵の管理方法)
3. [ローカル開発](#ローカル開発)
4. [デプロイメント](#デプロイメント)
5. [トラブルシューティング](#トラブルシューティング)

---

## 環境構築

### 前提条件

- Python 3.11 以上
- Google Cloud SDK (`gcloud` CLI)
- Google Cloud プロジェクト (`k-trend-autobot`)
- LINE Developers アカウント
- WordPress サイト（管理者権限）

### 初期セットアップ

1. **リポジトリのクローン**
   ```bash
   git clone <repository-url>
   cd ktrend-autobot
   ```

2. **Python 仮想環境の作成**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # または
   venv\Scripts\activate  # Windows
   ```

3. **依存関係のインストール**
   ```bash
   pip install -r requirements.txt
   ```

4. **Google Cloud SDK の認証**
   ```bash
   gcloud auth login
   gcloud config set project k-trend-autobot
   ```

---

## 秘密鍵の管理方法

### 🔐 基本方針

このプロジェクトでは、環境に応じて以下の方法で秘密鍵を管理します：

| 環境 | 管理方法 | 理由 |
|------|---------|------|
| **ローカル開発** | `.env` または `.env.yaml` ファイル | シンプルで開発効率が高い |
| **本番環境 (GCP)** | **Google Cloud Secret Manager** | セキュアで監査可能、IAMで権限管理 |

> **重要**: 1Password CLI (`op` コマンド) の使用は **禁止** されています。詳細は [.claudecode_context.md](./.claudecode_context.md) を参照してください。

---

### ローカル開発での秘密鍵管理

#### 1. `.env.yaml` ファイルの作成

プロジェクトルートに `.env.yaml` ファイルを作成し、以下の形式で環境変数を記述します：

```yaml
# Google Gemini API
GEMINI_API_KEY: "AIzaSy..."

# Google Custom Search
GOOGLE_CUSTOM_SEARCH_API_KEY: "AIzaSy..."
GOOGLE_CSE_ID: "30f0af..."

# LINE Bot
LINE_CHANNEL_ACCESS_TOKEN: "rZ3Cuo..."
LINE_CHANNEL_SECRET: "5d5cee..."
LINE_USER_ID: "Ubd61e..."

# Twitter/X (オプション)
X_API_KEY: ""
X_API_KEY_SECRET: ""
X_ACCESS_TOKEN: ""
X_ACCESS_TOKEN_SECRET: ""
X_BEARER_TOKEN: ""

# Google Cloud
GCP_PROJECT_ID: "k-trend-autobot"

# WordPress
WORDPRESS_URL: "https://your-wordpress-site.com"
WORDPRESS_USER: "admin"
WORDPRESS_APP_PASSWORD: "xxxx xxxx xxxx xxxx"
```

#### 2. `.gitignore` の確認

`.env.yaml` がリポジトリにコミットされないことを確認：

```bash
# .gitignore に以下が含まれていることを確認
.env
.env.yaml
.env.*.yaml
```

#### 3. ローカルでの環境変数の読み込み

Python コードでは、`os.getenv()` を使用して環境変数を取得します：

```python
import os
import yaml

# .env.yaml の読み込み (ローカル開発時)
if os.path.exists('.env.yaml'):
    with open('.env.yaml', 'r') as f:
        env_vars = yaml.safe_load(f)
        for key, value in env_vars.items():
            os.environ[key] = str(value)

# 環境変数の使用
gemini_api_key = os.getenv('GEMINI_API_KEY')
```

---

### 本番環境 (GCP) での秘密鍵管理

#### Option 1: `.env.yaml` を使用したデプロイ（現在の方法）

**メリット**: シンプルで素早くデプロイできる
**デメリット**: 秘密鍵がデプロイ履歴に残る可能性がある

```bash
# Cloud Functions に環境変数を含めてデプロイ
gcloud functions deploy view-draft \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=view_draft \
  --trigger-http \
  --allow-unauthenticated \
  --env-vars-file=.env.yaml \
  --timeout=540s \
  --memory=512MB
```

#### Option 2: Google Cloud Secret Manager を使用（推奨）

**メリット**: セキュアで監査可能、IAMで権限管理、ローテーション対応
**デメリット**: 初期セットアップが必要

##### Step 1: Secret Manager にシークレットを作成

```bash
# 各環境変数を Secret Manager に登録
echo -n "your-gemini-api-key" | gcloud secrets create GEMINI_API_KEY \
  --data-file=- \
  --replication-policy="automatic"

echo -n "your-line-token" | gcloud secrets create LINE_CHANNEL_ACCESS_TOKEN \
  --data-file=- \
  --replication-policy="automatic"

# 他の環境変数も同様に登録
```

##### Step 2: Secret Manager からシークレットを参照してデプロイ

```bash
gcloud functions deploy view-draft \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=view_draft \
  --trigger-http \
  --allow-unauthenticated \
  --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,LINE_CHANNEL_ACCESS_TOKEN=LINE_CHANNEL_ACCESS_TOKEN:latest,LINE_CHANNEL_SECRET=LINE_CHANNEL_SECRET:latest,WORDPRESS_APP_PASSWORD=WORDPRESS_APP_PASSWORD:latest" \
  --timeout=540s \
  --memory=512MB
```

##### Step 3: IAM 権限の設定

Cloud Functions が Secret Manager からシークレットを読み取れるように権限を付与：

```bash
# Cloud Functions のサービスアカウントに Secret Accessor ロールを付与
gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
  --member="serviceAccount:k-trend-autobot@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

##### Step 4: シークレットの更新（ローテーション）

```bash
# 既存のシークレットに新しいバージョンを追加
echo -n "new-api-key" | gcloud secrets versions add GEMINI_API_KEY --data-file=-

# Cloud Functions を再デプロイ（新しいバージョンを参照）
gcloud functions deploy view-draft --update-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest"
```

---

## ローカル開発

### ローカルでの関数テスト

Functions Framework を使用してローカルで HTTP トリガー関数をテストできます：

```bash
# 環境変数を読み込んで Functions Framework を起動
functions-framework --target=view_draft --debug --port=8080

# 別のターミナルでリクエストをテスト
curl "http://localhost:8080/?post_id=123"
```

### WordPress Application Password の生成

WordPress の画像アップロード機能を使用するには、Application Password が必要です：

1. **WordPress にログイン**
2. **ユーザー > プロフィール** に移動
3. **アプリケーションパスワード** セクションまでスクロール
4. 新しいアプリケーション名（例: "K-Trend AutoBot"）を入力
5. **新しいアプリケーションパスワードを追加** をクリック
6. 生成されたパスワードを `.env.yaml` の `WORDPRESS_APP_PASSWORD` に設定

> **注意**: Application Password はスペースを含む形式 (`xxxx xxxx xxxx xxxx`) で生成されますが、スペースを除いても動作します。

---

## デプロイメント

### 手動デプロイ

#### Cloud Functions (view-draft)

```bash
# view-draft 関数のデプロイ
gcloud functions deploy view-draft \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=view_draft \
  --trigger-http \
  --allow-unauthenticated \
  --env-vars-file=.env.yaml \
  --timeout=540s \
  --memory=512MB
```

#### Cloud Functions (他の関数)

```bash
# ktrend-daily-fetch のデプロイ例
gcloud functions deploy ktrend-daily-fetch \
  --gen2 \
  --runtime=python311 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=fetch_daily \
  --trigger-http \
  --env-vars-file=.env.yaml
```

### デプロイスクリプトの使用

プロジェクトには `deploy.sh` スクリプトが含まれており、複数の関数を一括デプロイできます：

```bash
# すべての関数をデプロイ
./deploy.sh

# 特定の関数のみデプロイ（スクリプトを編集）
```

---

## トラブルシューティング

### 画像アップロードが 401 エラーで失敗する

**原因**: WordPress Application Password が無効または期限切れ

**解決策**:
1. WordPress 管理画面で新しい Application Password を生成
2. `.env.yaml` の `WORDPRESS_APP_PASSWORD` を更新
3. 再デプロイ:
   ```bash
   gcloud functions deploy view-draft --env-vars-file=.env.yaml
   ```

### SSL 証明書エラー (`CERTIFICATE_VERIFY_FAILED`)

**原因**: WordPress サイトが自己署名証明書を使用している、またはIPアドレスでアクセスしている

**解決策**:
- コード内で `verify=False` を使用（開発環境のみ）:
  ```python
  response = requests.post(url, headers=headers, data=data, verify=False)
  ```
- 本番環境では適切な SSL 証明書を設定することを推奨

### 環境変数が読み込まれない

**原因**: `.env.yaml` の形式が正しくない、またはデプロイ時に指定していない

**解決策**:
1. `.env.yaml` の YAML 形式を確認（インデント、引用符）
2. デプロイコマンドに `--env-vars-file=.env.yaml` が含まれているか確認
3. Cloud Functions コンソールで環境変数が正しく設定されているか確認

### Secret Manager からシークレットを読み取れない

**原因**: IAM 権限が不足している

**解決策**:
```bash
# サービスアカウントに権限を付与
PROJECT_NUMBER=$(gcloud projects describe k-trend-autobot --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
```

---

## 付録

### 環境変数一覧

| 変数名 | 用途 | 必須 |
|-------|------|------|
| `GEMINI_API_KEY` | Google Gemini API 認証 | ✅ |
| `GOOGLE_CUSTOM_SEARCH_API_KEY` | Google Custom Search API 認証 | ✅ |
| `GOOGLE_CSE_ID` | Custom Search Engine ID | ✅ |
| `LINE_CHANNEL_ACCESS_TOKEN` | LINE Bot メッセージ送信 | ✅ |
| `LINE_CHANNEL_SECRET` | LINE Bot Webhook 検証 | ✅ |
| `LINE_USER_ID` | LINE 通知先ユーザー | ✅ |
| `GCP_PROJECT_ID` | Google Cloud プロジェクト | ✅ |
| `WORDPRESS_URL` | WordPress サイト URL | ✅ |
| `WORDPRESS_USER` | WordPress ユーザー名 | ✅ |
| `WORDPRESS_APP_PASSWORD` | WordPress Application Password | ✅ |
| `X_API_KEY` | Twitter/X API 認証 | ❌ |
| `X_API_KEY_SECRET` | Twitter/X API シークレット | ❌ |
| `X_ACCESS_TOKEN` | Twitter/X アクセストークン | ❌ |
| `X_ACCESS_TOKEN_SECRET` | Twitter/X アクセストークンシークレット | ❌ |
| `X_BEARER_TOKEN` | Twitter/X Bearer トークン | ❌ |

### 関連リンク

- [WORDPRESS_MANAGEMENT.md](./WORDPRESS_MANAGEMENT.md) - サーバー内でのWordPress管理ガイド
- [Google Cloud Secret Manager ドキュメント](https://cloud.google.com/secret-manager/docs)
- [Cloud Functions 環境変数ガイド](https://cloud.google.com/functions/docs/configuring/env-var)
- [WordPress REST API - Authentication](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/)
- [LINE Messaging API](https://developers.line.biz/ja/docs/messaging-api/)

---

**最終更新**: 2026-02-09
**メンテナ**: K-Trend Development Team
