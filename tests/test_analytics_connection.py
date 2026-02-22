#!/usr/bin/env python3
"""
Google Analytics 4 接続テスト
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
    from google.oauth2 import service_account

    print("✅ 必要なライブラリがインポートされました")
except ImportError as e:
    print(f"❌ エラー: 必要なライブラリがインストールされていません")
    print(f"   実行してください: pip install -r requirements.txt")
    print(f"   詳細: {e}")
    exit(1)

# 環境変数チェック
property_id = os.getenv("GA4_PROPERTY_ID")
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🔍 Google Analytics 4 接続テスト")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

if not property_id:
    print("❌ エラー: GA4_PROPERTY_ID が設定されていません")
    exit(1)

if not credentials_path:
    print("❌ エラー: GOOGLE_APPLICATION_CREDENTIALS が設定されていません")
    exit(1)

print(f"✅ GA4 プロパティID: {property_id}")
print(f"✅ 認証情報パス: {credentials_path}")

# 認証情報ファイルの存在確認
if not os.path.exists(credentials_path):
    print(f"❌ エラー: 認証情報ファイルが見つかりません: {credentials_path}")
    exit(1)

print(f"✅ 認証情報ファイル: 存在確認OK\n")

# クライアント初期化
try:
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = BetaAnalyticsDataClient(credentials=credentials)
    print("✅ Analytics クライアント初期化成功\n")
except Exception as e:
    print(f"❌ エラー: クライアント初期化に失敗しました")
    print(f"   {e}")
    exit(1)

# テストクエリ実行（過去7日間のデータ）
try:
    print("📊 テストクエリを実行中...\n")

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=week_ago, end_date=yesterday)],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="sessions"),
            Metric(name="screenPageViews"),
        ],
        dimensions=[
            Dimension(name="date"),
        ],
    )

    response = client.run_report(request)

    print("✅ データ取得成功！\n")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📅 期間: {week_ago} 〜 {yesterday}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    # 合計値表示
    if response.totals:
        total_row = response.totals[0]
        active_users = int(total_row.metric_values[0].value)
        sessions = int(total_row.metric_values[1].value)
        page_views = int(total_row.metric_values[2].value)

        print("【全体サマリー（過去7日間）】")
        print(f"👥 アクティブユーザー: {active_users:,}")
        print(f"🔄 セッション数: {sessions:,}")
        print(f"📄 ページビュー: {page_views:,}")
        print()

    # 日別データ
    if response.rows:
        print("【日別データ】")
        for row in response.rows:
            date = row.dimension_values[0].value
            users = int(row.metric_values[0].value)
            sessions = int(row.metric_values[1].value)
            page_views = int(row.metric_values[2].value)
            print(f"{date}: {page_views:,} PV / {users:,} ユーザー / {sessions:,} セッション")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ 接続テスト完了！すべて正常です")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

except Exception as e:
    print(f"❌ エラー: データ取得に失敗しました")
    print(f"\n詳細エラー:")
    print(f"{e}\n")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("🔍 トラブルシューティング:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("1. Google Analytics Data API が有効になっているか確認")
    print("   https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com")
    print()
    print("2. サービスアカウントがGA4プロパティに追加されているか確認")
    print(f"   メールアドレス: ktrend-bot@k-trend-autobot.iam.gserviceaccount.com")
    print(f"   権限: 閲覧者")
    print()
    print("3. GA4プロパティIDが正しいか確認")
    print(f"   現在の設定: {property_id}")
    print()
    exit(1)
