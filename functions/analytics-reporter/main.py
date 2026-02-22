"""
K-TREND TIMES Analytics Reporter - Cloud Functions
Google Cloud Scheduler から定期的に呼び出される
"""

import os
import functions_framework
from datetime import datetime, timedelta


@functions_framework.http
def daily_report(request):
    """日次レポートを生成してLINEに送信"""
    try:
        # 環境変数の確認
        property_id = os.getenv("GA4_PROPERTY_ID")
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if not property_id or not credentials_path:
            return {"error": "環境変数が設定されていません"}, 500

        # モジュールインポート
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.oauth2 import service_account

        # LINE Notifier
        from line_notifier import LineNotifier
        from analytics_helper import AnalyticsHelper, ReportFormatter

        # クライアント初期化
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = BetaAnalyticsDataClient(credentials=credentials)

        helper = AnalyticsHelper(property_id, client)
        formatter = ReportFormatter()
        notifier = LineNotifier()

        # 昨日のデータを取得
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        data = helper.get_daily_report(yesterday)

        # レポート生成
        report_text = formatter.format_daily_report(data, yesterday)

        # LINE送信
        messages = [{"type": "text", "text": report_text}]
        success = notifier.push_message(notifier.admin_user_id, messages)

        if success:
            return {"status": "success", "date": yesterday}, 200
        else:
            return {"error": "LINE送信に失敗しました"}, 500

    except Exception as e:
        print(f"エラー: {str(e)}")
        return {"error": str(e)}, 500


@functions_framework.http
def weekly_report(request):
    """週次レポートを生成してLINEに送信"""
    try:
        property_id = os.getenv("GA4_PROPERTY_ID")
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if not property_id or not credentials_path:
            return {"error": "環境変数が設定されていません"}, 500

        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.oauth2 import service_account
        from line_notifier import LineNotifier
        from analytics_helper import AnalyticsHelper, ReportFormatter

        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = BetaAnalyticsDataClient(credentials=credentials)

        helper = AnalyticsHelper(property_id, client)
        formatter = ReportFormatter()
        notifier = LineNotifier()

        # 昨日を終了日として過去7日間のデータ取得
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        data = helper.get_weekly_report(yesterday)
        top_pages = helper.get_top_pages(week_ago, yesterday, limit=10)

        # レポート生成
        report_text = formatter.format_weekly_report(data, week_ago, yesterday, top_pages)

        # LINE送信
        messages = [{"type": "text", "text": report_text}]
        success = notifier.push_message(notifier.admin_user_id, messages)

        if success:
            return {"status": "success", "period": f"{week_ago} - {yesterday}"}, 200
        else:
            return {"error": "LINE送信に失敗しました"}, 500

    except Exception as e:
        print(f"エラー: {str(e)}")
        return {"error": str(e)}, 500


@functions_framework.http
def monthly_report(request):
    """月次レポートを生成してLINEに送信"""
    try:
        property_id = os.getenv("GA4_PROPERTY_ID")
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if not property_id or not credentials_path:
            return {"error": "環境変数が設定されていません"}, 500

        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.oauth2 import service_account
        from line_notifier import LineNotifier
        from analytics_helper import AnalyticsHelper, ReportFormatter

        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = BetaAnalyticsDataClient(credentials=credentials)

        helper = AnalyticsHelper(property_id, client)
        formatter = ReportFormatter()
        notifier = LineNotifier()

        # 先月のデータを取得
        last_month = datetime.now().replace(day=1) - timedelta(days=1)
        year = last_month.year
        month = last_month.month

        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            end_date = (datetime(year, month + 1, 1) - timedelta(days=1)).strftime("%Y-%m-%d")

        data = helper.get_monthly_report(year, month)
        top_pages = helper.get_top_pages(start_date, end_date, limit=10)
        sources = helper.get_traffic_sources(start_date, end_date)

        # レポート生成
        report_text = formatter.format_monthly_report(data, year, month, top_pages, sources)

        # LINE送信
        messages = [{"type": "text", "text": report_text}]
        success = notifier.push_message(notifier.admin_user_id, messages)

        if success:
            return {"status": "success", "month": f"{year}-{month:02d}"}, 200
        else:
            return {"error": "LINE送信に失敗しました"}, 500

    except Exception as e:
        print(f"エラー: {str(e)}")
        return {"error": str(e)}, 500
