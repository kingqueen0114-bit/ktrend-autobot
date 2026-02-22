"""Analytics Helper for Cloud Functions"""

from datetime import datetime, timedelta
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest


class AnalyticsHelper:
    """Google Analytics 4 データ取得ヘルパー"""

    def __init__(self, property_id: str, client):
        self.property_id = property_id
        self.client = client

    def get_daily_report(self, date: str):
        """日次レポート取得"""
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=date, end_date=date)],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="averageSessionDuration"),
                Metric(name="bounceRate"),
            ],
            dimensions=[Dimension(name="date")],
        )
        response = self.client.run_report(request)
        return self._parse_response(response)

    def get_weekly_report(self, end_date: str):
        """週次レポート取得"""
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
            ],
            dimensions=[Dimension(name="date")],
        )
        response = self.client.run_report(request)
        return self._parse_response(response)

    def get_monthly_report(self, year: int, month: int):
        """月次レポート取得"""
        start_date = f"{year}-{month:02d}-01"
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
            ],
            dimensions=[Dimension(name="date")],
        )
        response = self.client.run_report(request)
        return self._parse_response(response)

    def get_top_pages(self, start_date: str, end_date: str, limit: int = 10):
        """人気ページ取得"""
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

    def get_traffic_sources(self, start_date: str, end_date: str):
        """トラフィックソース取得"""
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

    def _parse_response(self, response):
        """レスポンス解析"""
        total = {}
        if response.totals:
            total_row = response.totals[0]
            total = {
                "active_users": int(total_row.metric_values[0].value),
                "sessions": int(total_row.metric_values[1].value),
                "page_views": int(total_row.metric_values[2].value),
                "avg_session_duration": float(total_row.metric_values[3].value),
                "bounce_rate": float(total_row.metric_values[4].value),
            }

        daily = []
        for row in response.rows:
            daily.append({
                "date": row.dimension_values[0].value,
                "active_users": int(row.metric_values[0].value),
                "sessions": int(row.metric_values[1].value),
                "page_views": int(row.metric_values[2].value),
                "avg_session_duration": float(row.metric_values[3].value),
                "bounce_rate": float(row.metric_values[4].value),
            })

        return {"total": total, "daily": daily}


class ReportFormatter:
    """レポートフォーマッター"""

    @staticmethod
    def format_daily_report(data, date):
        """日次レポート"""
        total = data.get("total", {})
        return f"""━━━━━━━━━━━━━━━━━━━━━━━
🎯 K-TREND TIMES 日次レポート
📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━

【📊 Google Analytics】
👥 アクティブユーザー: {total.get('active_users', 0):,}
🔄 セッション数: {total.get('sessions', 0):,}
📄 ページビュー: {total.get('page_views', 0):,}
⏱️ 平均セッション時間: {ReportFormatter._format_duration(total.get('avg_session_duration', 0))}
📈 直帰率: {total.get('bounce_rate', 0):.1%}

━━━━━━━━━━━━━━━━━━━━━━━"""

    @staticmethod
    def format_weekly_report(data, start_date, end_date, top_pages):
        """週次レポート"""
        total = data.get("total", {})
        report = f"""━━━━━━━━━━━━━━━━━━━━━━━
📊 K-TREND TIMES 週次レポート
📅 {start_date} 〜 {end_date}
━━━━━━━━━━━━━━━━━━━━━━━

【📊 Google Analytics】
👥 アクティブユーザー: {total.get('active_users', 0):,}
🔄 セッション数: {total.get('sessions', 0):,}
📄 ページビュー: {total.get('page_views', 0):,}
⏱️ 平均セッション時間: {ReportFormatter._format_duration(total.get('avg_session_duration', 0))}
📈 直帰率: {total.get('bounce_rate', 0):.1%}
"""
        if top_pages:
            report += "\n【🔥 人気記事 TOP5】\n"
            for i, page in enumerate(top_pages[:5], 1):
                report += f"{i}. {page['title'][:50]}...\n   {page['page_views']:,} PV\n"

        report += "\n━━━━━━━━━━━━━━━━━━━━━━━"
        return report

    @staticmethod
    def format_monthly_report(data, year, month, top_pages, sources):
        """月次レポート"""
        total = data.get("total", {})
        days = len(data.get("daily", []))

        report = f"""━━━━━━━━━━━━━━━━━━━━━━━
📊 K-TREND TIMES 月次レポート
📅 {year}年{month}月
━━━━━━━━━━━━━━━━━━━━━━━

【📊 Google Analytics】
👥 アクティブユーザー: {total.get('active_users', 0):,}
🔄 セッション数: {total.get('sessions', 0):,}
📄 ページビュー: {total.get('page_views', 0):,}
⏱️ 平均セッション時間: {ReportFormatter._format_duration(total.get('avg_session_duration', 0))}
📈 直帰率: {total.get('bounce_rate', 0):.1%}

📊 日別平均:
📄 PV/日: {total.get('page_views', 0) / days if days > 0 else 0:,.0f}
👥 ユーザー/日: {total.get('active_users', 0) / days if days > 0 else 0:,.0f}
"""
        if top_pages:
            report += "\n【🔥 人気記事 TOP10】\n"
            for i, page in enumerate(top_pages[:10], 1):
                report += f"{i}. {page['title'][:50]}...\n   {page['page_views']:,} PV\n"

        if sources:
            report += "\n【🌐 トラフィックソース TOP5】\n"
            for i, source in enumerate(sources[:5], 1):
                report += f"{i}. {source['source']} / {source['medium']}\n   {source['sessions']:,} セッション\n"

        report += "\n━━━━━━━━━━━━━━━━━━━━━━━"
        return report

    @staticmethod
    def _format_duration(seconds):
        """秒数を読みやすく"""
        if seconds < 60:
            return f"{seconds:.0f}秒"
        elif seconds < 3600:
            return f"{seconds/60:.1f}分"
        else:
            return f"{seconds/3600:.1f}時間"
