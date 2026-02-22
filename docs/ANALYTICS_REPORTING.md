# K-TREND TIMES アナリティクス & AdSense レポートシステム

Google Analytics 4とAdSenseのデータを自動的に取得・分析して、日次・週次・月次レポートをLINEで送信するシステムです。

## 📋 目次

- [機能概要](#機能概要)
- [セットアップ](#セットアップ)
- [使い方](#使い方)
- [レポートの種類](#レポートの種類)
- [自動スケジュール実行](#自動スケジュール実行)

---

## 🎯 機能概要

### ✨ 主な機能

1. **Google Analytics 4 レポート**
   - アクティブユーザー数
   - セッション数
   - ページビュー数
   - 平均セッション時間
   - 直帰率
   - 人気ページランキング
   - トラフィックソース分析

2. **AdSense レポート**
   - ページビュー数
   - クリック数
   - CTR（クリック率）
   - CPC（クリック単価）
   - RPM（1000インプレッションあたりの収益）
   - 見積もり収益

3. **統合レポート**
   - AnalyticsとAdSenseのデータを1つのレポートにまとめて表示
   - パフォーマンス指標（ユーザーあたり収益など）
   - LINEで自動通知

---

## 🔧 セットアップ

### 1. 必要なライブラリのインストール

```bash
pip install -r requirements.txt
```

### 2. Google Cloud プロジェクトの設定

#### Google Analytics Data API の有効化

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを選択
3. 「APIとサービス」→「ライブラリ」
4. 「Google Analytics Data API」を検索して有効化

#### サービスアカウントの作成

1. 「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「サービスアカウント」
3. サービスアカウント名を入力（例: `ktrend-analytics`）
4. 「キーを追加」→「新しいキーを作成」→「JSON」
5. JSONファイルをダウンロードして安全な場所に保存

#### GA4 プロパティへのアクセス権付与

1. [Google Analytics](https://analytics.google.com/)にアクセス
2. 管理 → プロパティ → プロパティのアクセス管理
3. 「+」ボタンでユーザーを追加
4. サービスアカウントのメールアドレスを入力（例: `ktrend-analytics@project-id.iam.gserviceaccount.com`）
5. 「閲覧者」権限を付与

### 3. GA4 プロパティIDの取得

1. Google Analytics → 管理 → プロパティ → プロパティの詳細
2. プロパティID（数字のみ、例: `123456789`）をコピー

### 4. 環境変数の設定

`.env`ファイルに以下を追加:

```bash
# Google Analytics 4
GA4_PROPERTY_ID=123456789
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# AdSense (オプション)
ADSENSE_CSV_PATH=/path/to/adsense-data.csv
```

### 5. AdSense データの準備（オプション）

AdSense Management APIは現在サポートが限定的なため、CSVファイルを使用します。

1. [AdSense管理画面](https://www.google.com/adsense/)にアクセス
2. 「レポート」→ 対象期間を選択
3. 「ダウンロード」→「CSV」を選択
4. ダウンロードしたCSVファイルを保存
5. `.env`の`ADSENSE_CSV_PATH`にパスを設定

---

## 📊 使い方

### 日次レポート

#### Analyticsのみ
```bash
python -m src.analytics_reporter daily
```

特定の日付を指定:
```bash
python -m src.analytics_reporter daily 2026-02-07
```

#### AdSenseのみ
```bash
python -m src.adsense_reporter daily /path/to/adsense.csv
```

#### 統合レポート（推奨）
```bash
python -m src.unified_reporter daily
```

### 週次レポート（過去7日間）

```bash
python -m src.unified_reporter weekly
```

特定の終了日を指定:
```bash
python -m src.unified_reporter weekly 2026-02-07
```

### 月次レポート

```bash
python -m src.unified_reporter monthly
```

特定の年月を指定:
```bash
python -m src.unified_reporter monthly 2026 1
```

---

## 📈 レポートの種類

### 📅 日次レポート

```
━━━━━━━━━━━━━━━━━━━━━━━
🎯 K-TREND TIMES 日次レポート
📅 2026-02-07
━━━━━━━━━━━━━━━━━━━━━━━

【📊 Google Analytics】
👥 アクティブユーザー: 1,234
🔄 セッション数: 2,345
📄 ページビュー: 3,456
⏱️ 平均セッション時間: 2.5分
📈 直帰率: 45.6%

【💰 Google AdSense】
👆 クリック数: 12
📈 CTR: 0.35%
💵 CPC: ¥45.67
📊 RPM: ¥123.45
💰 見積もり収益: ¥456.78

【📈 パフォーマンス指標】
💰 ユーザーあたり収益: ¥0.37
📊 収益化率: 0.35%
━━━━━━━━━━━━━━━━━━━━━━━
```

### 📊 週次レポート（過去7日間）

- 期間の合計データ
- 日別推移
- 人気記事TOP5
- パフォーマンス指標

### 📈 月次レポート

- 月間合計データ
- 日別平均
- 人気記事TOP10
- トラフィックソースTOP5
- 収益トップ5の日

---

## ⏰ 自動スケジュール実行

### Cloud Functionsでスケジュール実行（推奨）

#### 1. Cloud Schedulerの設定

```bash
# 日次レポート（毎日午前9時）
gcloud scheduler jobs create http daily-analytics-report \
  --schedule="0 9 * * *" \
  --uri="https://asia-northeast1-your-project.cloudfunctions.net/ktrend-analytics-daily" \
  --http-method=POST \
  --time-zone="Asia/Tokyo"

# 週次レポート（毎週月曜日午前10時）
gcloud scheduler jobs create http weekly-analytics-report \
  --schedule="0 10 * * 1" \
  --uri="https://asia-northeast1-your-project.cloudfunctions.net/ktrend-analytics-weekly" \
  --http-method=POST \
  --time-zone="Asia/Tokyo"

# 月次レポート（毎月1日午前11時）
gcloud scheduler jobs create http monthly-analytics-report \
  --schedule="0 11 1 * *" \
  --uri="https://asia-northeast1-your-project.cloudfunctions.net/ktrend-analytics-monthly" \
  --http-method=POST \
  --time-zone="Asia/Tokyo"
```

#### 2. Cloud Functions関数の作成

`functions/analytics_report/main.py`:

```python
import functions_framework
from src.unified_reporter import UnifiedReporter
from src.analytics_reporter import AnalyticsReporter
from src.adsense_reporter import AdSenseReporter
from src.notifier import LineNotifier
import os

@functions_framework.http
def daily_report(request):
    """日次レポート"""
    analytics = AnalyticsReporter(
        os.getenv("GA4_PROPERTY_ID"),
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    adsense = AdSenseReporter()
    notifier = LineNotifier()
    unified = UnifiedReporter(analytics, adsense, notifier)

    unified.send_daily_unified_report()
    return "日次レポート送信完了", 200

@functions_framework.http
def weekly_report(request):
    """週次レポート"""
    analytics = AnalyticsReporter(
        os.getenv("GA4_PROPERTY_ID"),
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    adsense = AdSenseReporter()
    notifier = LineNotifier()
    unified = UnifiedReporter(analytics, adsense, notifier)

    unified.send_weekly_unified_report()
    return "週次レポート送信完了", 200

@functions_framework.http
def monthly_report(request):
    """月次レポート"""
    analytics = AnalyticsReporter(
        os.getenv("GA4_PROPERTY_ID"),
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    adsense = AdSenseReporter()
    notifier = LineNotifier()
    unified = UnifiedReporter(analytics, adsense, notifier)

    unified.send_monthly_unified_report()
    return "月次レポート送信完了", 200
```

### Cronでローカル実行

`crontab -e`で以下を追加:

```bash
# 日次レポート（毎日午前9時）
0 9 * * * cd /path/to/ktrend-autobot && python -m src.unified_reporter daily

# 週次レポート（毎週月曜日午前10時）
0 10 * * 1 cd /path/to/ktrend-autobot && python -m src.unified_reporter weekly

# 月次レポート（毎月1日午前11時）
0 11 1 * * cd /path/to/ktrend-autobot && python -m src.unified_reporter monthly
```

---

## 🔍 トラブルシューティング

### エラー: "GA4_PROPERTY_ID と GOOGLE_APPLICATION_CREDENTIALS を設定してください"

→ `.env`ファイルに必要な環境変数が設定されているか確認

### エラー: "Permission denied"

→ サービスアカウントにGA4プロパティへのアクセス権が付与されているか確認

### AdSenseデータが表示されない

→ `ADSENSE_CSV_PATH`が正しく設定されているか、CSVファイルが存在するか確認

### レポートがLINEに届かない

→ `LINE_CHANNEL_ACCESS_TOKEN`と`LINE_ADMIN_USER_ID`が正しく設定されているか確認

---

## 📝 補足情報

### 指標の説明

- **アクティブユーザー**: サイトを訪問したユニークユーザー数
- **セッション**: 訪問回数（30分間操作がないと新しいセッションとしてカウント）
- **ページビュー**: ページが表示された回数
- **直帰率**: 1ページのみ閲覧して離脱したセッションの割合
- **CTR**: クリック率（クリック数 ÷ 広告表示数）
- **CPC**: クリック単価（収益 ÷ クリック数）
- **RPM**: 1000ページビューあたりの収益

### データの更新タイミング

- **Google Analytics**: リアルタイムデータは数分、完全なデータは24-48時間後
- **AdSense**: 通常24-48時間後に確定

---

## 🆘 サポート

問題が発生した場合は、以下を確認してください:

1. `.env`ファイルの設定
2. Google Cloud プロジェクトのAPI有効化状態
3. サービスアカウントの権限
4. GA4プロパティIDの正確性
5. ネットワーク接続

---

## 📄 ライセンス

K-TREND TIMES プロジェクト © 2026
