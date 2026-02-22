# Cloud Scheduler セットアップガイド

Analytics レポートを Google Cloud Scheduler で自動実行する手順

---

## 📋 前提条件

- ✅ Google Cloud SDK (`gcloud`) がインストール済み
- ✅ プロジェクト: `k-trend-autobot`
- ✅ GA4プロパティID: `462773259`
- ✅ サービスアカウント: `ktrend-bot@k-trend-autobot.iam.gserviceaccount.com`

---

## 🚀 デプロイ手順

### 1. Google Cloud SDK のインストール（未インストールの場合）

```bash
# macOS
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# 初期化
gcloud init
```

### 2. プロジェクトにログイン

```bash
gcloud auth login
gcloud config set project k-trend-autobot
```

### 3. Cloud Functions & Scheduler をデプロイ

```bash
./deploy-analytics-reporter.sh
```

このスクリプトは以下を自動実行します：
- Cloud Functions API を有効化
- Cloud Scheduler API を有効化
- 3つのCloud Functions をデプロイ（日次/週次/月次）
- Cloud Scheduler ジョブを作成

---

## ⏰ 設定されるスケジュール

| レポート | 実行タイミング | スケジュール |
|---------|--------------|-------------|
| 📅 日次 | 毎日 09:00 (JST) | `0 9 * * *` |
| 📊 週次 | 毎週月曜 10:00 (JST) | `0 10 * * 1` |
| 📈 月次 | 毎月1日 11:00 (JST) | `0 11 1 * *` |

---

## 🧪 手動テスト実行

デプロイ後、以下のコマンドで手動テストできます：

```bash
# 日次レポート
gcloud scheduler jobs run ktrend-analytics-daily-schedule --location=asia-northeast1

# 週次レポート
gcloud scheduler jobs run ktrend-analytics-weekly-schedule --location=asia-northeast1

# 月次レポート
gcloud scheduler jobs run ktrend-analytics-monthly-schedule --location=asia-northeast1
```

---

## 📊 Cloud Console で確認

### Cloud Functions
https://console.cloud.google.com/functions?project=k-trend-autobot

以下の関数が表示されます：
- `ktrend-analytics-daily`
- `ktrend-analytics-weekly`
- `ktrend-analytics-monthly`

### Cloud Scheduler
https://console.cloud.google.com/cloudscheduler?project=k-trend-autobot

以下のジョブが表示されます：
- `ktrend-analytics-daily-schedule`
- `ktrend-analytics-weekly-schedule`
- `ktrend-analytics-monthly-schedule`

---

## 🔍 トラブルシューティング

### エラー: "gcloud command not found"

→ Google Cloud SDK をインストール: https://cloud.google.com/sdk/docs/install

### エラー: "Permission denied"

→ 以下のコマンドでログインし直す:
```bash
gcloud auth login
gcloud auth application-default login
```

### エラー: "API not enabled"

→ 以下のコマンドで手動で有効化:
```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable analyticsdata.googleapis.com
```

### Cloud Scheduler ジョブが実行されない

1. Cloud Scheduler のログを確認:
   ```bash
   gcloud scheduler jobs describe ktrend-analytics-daily-schedule --location=asia-northeast1
   ```

2. Cloud Functions のログを確認:
   ```bash
   gcloud functions logs read ktrend-analytics-daily --gen2 --region=asia-northeast1 --limit=50
   ```

---

## 💰 料金について

### Cloud Functions
- **無料枠**: 月200万リクエスト、40万GB秒、20万GHz秒
- **予想コスト**: 月3回実行 → 無料枠内

### Cloud Scheduler
- **無料枠**: 月3ジョブまで無料
- **予想コスト**: 3ジョブ → 無料

合計: **ほぼ無料**（無料枠内で収まります）

---

## 🔄 スケジュール変更方法

スケジュールを変更する場合:

```bash
# ジョブを削除
gcloud scheduler jobs delete ktrend-analytics-daily-schedule --location=asia-northeast1

# 新しいスケジュールで作成
gcloud scheduler jobs create http ktrend-analytics-daily-schedule \
    --location=asia-northeast1 \
    --schedule="0 10 * * *" \
    --uri="<FUNCTION_URL>" \
    --http-method=POST \
    --time-zone="Asia/Tokyo" \
    --project=k-trend-autobot
```

---

## 🗑️ アンインストール

すべてを削除する場合:

```bash
# Scheduler ジョブ削除
gcloud scheduler jobs delete ktrend-analytics-daily-schedule --location=asia-northeast1
gcloud scheduler jobs delete ktrend-analytics-weekly-schedule --location=asia-northeast1
gcloud scheduler jobs delete ktrend-analytics-monthly-schedule --location=asia-northeast1

# Cloud Functions 削除
gcloud functions delete ktrend-analytics-daily --gen2 --region=asia-northeast1
gcloud functions delete ktrend-analytics-weekly --gen2 --region=asia-northeast1
gcloud functions delete ktrend-analytics-monthly --gen2 --region=asia-northeast1
```

---

## 📞 サポート

問題が発生した場合:
1. ログを確認
2. 環境変数が正しく設定されているか確認
3. API が有効になっているか確認
