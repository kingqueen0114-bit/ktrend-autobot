"""
K-TREND TIMES Analytics & AdSense Reporter
Google Analytics 4とAdSenseのデータを取得して日次・週次・月次レポートを生成
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Google Analytics Data API
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account

# LINE通知用
from src.notifier import Notifier


class AnalyticsReporter:
    """Google Analytics 4 データを取得して分析"""

    def __init__(self, property_id: str, credentials_path: str):
        """
        Args:
            property_id: GA4 プロパティID (例: "123456789")
            credentials_path: サービスアカウントJSONファイルのパス
        """
        self.property_id = property_id
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        self.client = BetaAnalyticsDataClient(credentials=self.credentials)

    def get_daily_report(self, date: Optional[str] = None) -> Dict:
        """
        日次レポートを取得

        Args:
            date: 取得日 (YYYY-MM-DD形式、Noneの場合は昨日)

        Returns:
            レポートデータ
        """
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=date, end_date=date)],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
                Metric(name="eventCount"),
            ],
            dimensions=[
                Dimension(name="date"),
            ],
        )

        response = self.client.run_report(request)
        return self._parse_response(response)

    def get_weekly_report(self, end_date: Optional[str] = None) -> Dict:
        """
        週次レポートを取得（過去7日間）

        Args:
            end_date: 終了日 (YYYY-MM-DD形式、Noneの場合は昨日)

        Returns:
            レポートデータ
        """
        if end_date is None:
            end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=6)).strftime("%Y-%m-%d")

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
                Metric(name="eventCount"),
            ],
            dimensions=[
                Dimension(name="date"),
            ],
        )

        response = self.client.run_report(request)
        return self._parse_response(response)

    def get_monthly_report(self, year: int, month: int) -> Dict:
        """
        月次レポートを取得

        Args:
            year: 年
            month: 月

        Returns:
            レポートデータ
        """
        start_date = f"{year}-{month:02d}-01"

        # 月末日を計算
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            end_date = (datetime(year, month + 1, 1) - timedelta(days=1)).strftime("%Y-%m-%d")

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
                Metric(name="eventCount"),
            ],
            dimensions=[
                Dimension(name="date"),
            ],
        )

        response = self.client.run_report(request)
        return self._parse_response(response)

    def get_top_pages(self, start_date: str, end_date: str, limit: int = 10) -> List[Dict]:
        """
        人気ページランキングを取得

        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)
            limit: 取得件数

        Returns:
            ページデータのリスト
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="activeUsers"),
            ],
            dimensions=[
                Dimension(name="pageTitle"),
                Dimension(name="pagePath"),
            ],
            limit=limit,
        )

        response = self.client.run_report(request)

        pages = []
        for row in response.rows:
            pages.append({
                "title": row.dimension_values[0].value,
                "path": row.dimension_values[1].value,
                "page_views": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
            })

        return pages

    def get_traffic_sources(self, start_date: str, end_date: str) -> List[Dict]:
        """
        トラフィックソースを取得

        Args:
            start_date: 開始日 (YYYY-MM-DD)
            end_date: 終了日 (YYYY-MM-DD)

        Returns:
            トラフィックソースのリスト
        """
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="sessions"),
                Metric(name="activeUsers"),
            ],
            dimensions=[
                Dimension(name="sessionSource"),
                Dimension(name="sessionMedium"),
            ],
        )

        response = self.client.run_report(request)

        sources = []
        for row in response.rows:
            sources.append({
                "source": row.dimension_values[0].value,
                "medium": row.dimension_values[1].value,
                "sessions": int(row.metric_values[0].value),
                "users": int(row.metric_values[1].value),
            })

        return sources

    def _parse_response(self, response) -> Dict:
        """APIレスポンスを解析"""
        if not response.rows:
            return {
                "total": {},
                "daily": []
            }

        # 合計値
        total = {}
        if response.totals:
            total_row = response.totals[0]
            total = {
                "active_users": int(total_row.metric_values[0].value),
                "sessions": int(total_row.metric_values[1].value),
                "page_views": int(total_row.metric_values[2].value),
                "avg_session_duration": float(total_row.metric_values[3].value),
                "bounce_rate": float(total_row.metric_values[4].value),
                "events": int(total_row.metric_values[5].value),
            }

        # 日別データ
        daily = []
        for row in response.rows:
            daily.append({
                "date": row.dimension_values[0].value,
                "active_users": int(row.metric_values[0].value),
                "sessions": int(row.metric_values[1].value),
                "page_views": int(row.metric_values[2].value),
                "avg_session_duration": float(row.metric_values[3].value),
                "bounce_rate": float(row.metric_values[4].value),
                "events": int(row.metric_values[5].value),
            })

        return {
            "total": total,
            "daily": daily
        }


class ReportFormatter:
    """レポートをフォーマットしてLINE通知用のテキストを生成"""

    @staticmethod
    def format_daily_report(data: Dict, date: str) -> str:
        """日次レポートをフォーマット"""
        total = data.get("total", {})

        report = f"""📊 K-TREND TIMES 日次レポート
📅 {date}

👥 アクティブユーザー: {total.get('active_users', 0):,}
🔄 セッション数: {total.get('sessions', 0):,}
📄 ページビュー: {total.get('page_views', 0):,}
⏱️ 平均セッション時間: {ReportFormatter._format_duration(total.get('avg_session_duration', 0))}
📈 直帰率: {total.get('bounce_rate', 0):.1%}
🎯 イベント数: {total.get('events', 0):,}
"""
        return report

    @staticmethod
    def format_weekly_report(data: Dict, start_date: str, end_date: str, top_pages: List[Dict]) -> str:
        """週次レポートをフォーマット"""
        total = data.get("total", {})
        daily = data.get("daily", [])

        report = f"""📊 K-TREND TIMES 週次レポート
📅 {start_date} 〜 {end_date}

【全体サマリー】
👥 アクティブユーザー: {total.get('active_users', 0):,}
🔄 セッション数: {total.get('sessions', 0):,}
📄 ページビュー: {total.get('page_views', 0):,}
⏱️ 平均セッション時間: {ReportFormatter._format_duration(total.get('avg_session_duration', 0))}
📈 直帰率: {total.get('bounce_rate', 0):.1%}

【日別推移】
"""
        for day in daily:
            report += f"{day['date']}: {day['page_views']:,} PV / {day['active_users']:,} ユーザー\n"

        if top_pages:
            report += "\n【人気記事 TOP5】\n"
            for i, page in enumerate(top_pages[:5], 1):
                report += f"{i}. {page['title']}\n   {page['page_views']:,} PV / {page['users']:,} ユーザー\n"

        return report

    @staticmethod
    def format_monthly_report(data: Dict, year: int, month: int, top_pages: List[Dict], sources: List[Dict]) -> str:
        """月次レポートをフォーマット"""
        total = data.get("total", {})
        daily = data.get("daily", [])

        report = f"""📊 K-TREND TIMES 月次レポート
📅 {year}年{month}月

【全体サマリー】
👥 アクティブユーザー: {total.get('active_users', 0):,}
🔄 セッション数: {total.get('sessions', 0):,}
📄 ページビュー: {total.get('page_views', 0):,}
⏱️ 平均セッション時間: {ReportFormatter._format_duration(total.get('avg_session_duration', 0))}
📈 直帰率: {total.get('bounce_rate', 0):.1%}

【日別平均】
📄 平均PV/日: {total.get('page_views', 0) / len(daily) if daily else 0:,.0f}
👥 平均ユーザー/日: {total.get('active_users', 0) / len(daily) if daily else 0:,.0f}
"""

        if top_pages:
            report += "\n【人気記事 TOP10】\n"
            for i, page in enumerate(top_pages[:10], 1):
                report += f"{i}. {page['title']}\n   {page['page_views']:,} PV / {page['users']:,} ユーザー\n"

        if sources:
            report += "\n【トラフィックソース TOP5】\n"
            for i, source in enumerate(sources[:5], 1):
                report += f"{i}. {source['source']} ({source['medium']})\n   {source['sessions']:,} セッション / {source['users']:,} ユーザー\n"

        return report

    @staticmethod
    def _format_duration(seconds: float) -> str:
        """秒数を読みやすい形式に変換"""
        if seconds < 60:
            return f"{seconds:.0f}秒"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}分"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}時間"


class ReportScheduler:
    """レポートのスケジュール実行を管理"""

    def __init__(self, analytics_reporter: AnalyticsReporter, line_notifier: Notifier):
        self.analytics = analytics_reporter
        self.notifier = line_notifier
        self.formatter = ReportFormatter()

    def send_daily_report(self, date: Optional[str] = None):
        """日次レポートを送信"""
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        print(f"📊 日次レポート生成中: {date}")
        data = self.analytics.get_daily_report(date)
        report_text = self.formatter.format_daily_report(data, date)

        messages = [{"type": "text", "text": report_text}]
        self.notifier._send_custom_messages(messages)
        print("✅ 日次レポート送信完了")

    def send_weekly_report(self, end_date: Optional[str] = None):
        """週次レポートを送信"""
        if end_date is None:
            end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=6)).strftime("%Y-%m-%d")

        print(f"📊 週次レポート生成中: {start_date} 〜 {end_date}")
        data = self.analytics.get_weekly_report(end_date)
        top_pages = self.analytics.get_top_pages(start_date, end_date, limit=10)

        report_text = self.formatter.format_weekly_report(data, start_date, end_date, top_pages)

        messages = [{"type": "text", "text": report_text}]
        self.notifier._send_custom_messages(messages)
        print("✅ 週次レポート送信完了")

    def send_monthly_report(self, year: Optional[int] = None, month: Optional[int] = None):
        """月次レポートを送信"""
        if year is None or month is None:
            last_month = datetime.now().replace(day=1) - timedelta(days=1)
            year = last_month.year
            month = last_month.month

        print(f"📊 月次レポート生成中: {year}年{month}月")
        data = self.analytics.get_monthly_report(year, month)

        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            end_date = (datetime(year, month + 1, 1) - timedelta(days=1)).strftime("%Y-%m-%d")

        top_pages = self.analytics.get_top_pages(start_date, end_date, limit=10)
        sources = self.analytics.get_traffic_sources(start_date, end_date)

        report_text = self.formatter.format_monthly_report(data, year, month, top_pages, sources)

        messages = [{"type": "text", "text": report_text}]
        self.notifier._send_custom_messages(messages)
        print("✅ 月次レポート送信完了")


def main():
    """メイン実行関数"""
    import yaml
    try:
        if os.path.exists('.env.yaml'):
            with open('.env.yaml', 'r') as f:
                env_vars = yaml.safe_load(f)
                if env_vars:
                    for k, v in env_vars.items():
                        os.environ[k] = str(v)
    except Exception as e:
        print(f"Warning: Could not load .env.yaml: {e}")
    
    # Try dotenv as fallback
    try:
        load_dotenv()
    except Exception:
        pass

    # 環境変数から設定を取得
    property_id = os.getenv("GA4_PROPERTY_ID")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not property_id or not credentials_path:
        print("❌ エラー: GA4_PROPERTY_ID と GOOGLE_APPLICATION_CREDENTIALS を .env.yaml に設定してください")
        return

    # レポーター初期化
    analytics = AnalyticsReporter(property_id, credentials_path)
    notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
    scheduler = ReportScheduler(analytics, notifier)

    # 実行例
    import sys
    if len(sys.argv) < 2:
        print("使用法:")
        print("  python -m src.analytics_reporter daily [日付]")
        print("  python -m src.analytics_reporter weekly [終了日]")
        print("  python -m src.analytics_reporter monthly [年] [月]")
        return

    report_type = sys.argv[1]

    if report_type == "daily":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        scheduler.send_daily_report(date)
    elif report_type == "weekly":
        end_date = sys.argv[2] if len(sys.argv) > 2 else None
        scheduler.send_weekly_report(end_date)
    elif report_type == "monthly":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        month = int(sys.argv[3]) if len(sys.argv) > 3 else None
        scheduler.send_monthly_report(year, month)
    else:
        print(f"❌ 不明なレポートタイプ: {report_type}")


if __name__ == "__main__":
    main()
