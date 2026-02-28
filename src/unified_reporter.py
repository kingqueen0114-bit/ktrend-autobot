"""
K-TREND TIMES 統合レポートシステム
Google AnalyticsとAdSenseのデータを統合して包括的なレポートを生成
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv

from src.analytics_reporter import AnalyticsReporter, ReportFormatter as AnalyticsFormatter
from src.adsense_reporter import AdSenseReporter, AdSenseFormatter
from src.notifier import Notifier
from utils.logging_config import log_event, log_error


class UnifiedReporter:
    """Analytics + AdSense の統合レポート"""

    def __init__(
        self,
        analytics_reporter: AnalyticsReporter,
        adsense_reporter: AdSenseReporter,
        line_notifier: Notifier
    ):
        self.analytics = analytics_reporter
        self.adsense = adsense_reporter
        self.notifier = line_notifier
        self.analytics_formatter = AnalyticsFormatter()
        self.adsense_formatter = AdSenseFormatter()

    def send_daily_unified_report(self, date: Optional[str] = None, adsense_csv: Optional[str] = None):
        """
        日次統合レポートを送信

        Args:
            date: 対象日 (YYYY-MM-DD、Noneの場合は昨日)
            adsense_csv: AdSense CSVファイルのパス
        """
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        log_event("UNIFIED_REPORT", f"統合日次レポート生成中: {date}")

        # Analyticsデータ取得
        analytics_data = self.analytics.get_daily_report(date)

        # 統合レポート作成
        report = f"""━━━━━━━━━━━━━━━━━━━━━━━
🎯 K-TREND TIMES 日次レポート
📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━

【📊 Google Analytics】
👥 アクティブユーザー: {analytics_data['total'].get('active_users', 0):,}
🔄 セッション数: {analytics_data['total'].get('sessions', 0):,}
📄 ページビュー: {analytics_data['total'].get('page_views', 0):,}
⏱️ 平均セッション時間: {self._format_duration(analytics_data['total'].get('avg_session_duration', 0))}
📈 直帰率: {analytics_data['total'].get('bounce_rate', 0):.1%}
"""

        # AdSenseデータがある場合は追加
        if adsense_csv and os.path.exists(adsense_csv):
            adsense_data = self.adsense.get_daily_report(date, adsense_csv)
            summary = adsense_data.get('summary', {})

            report += f"""
【💰 Google AdSense】
👆 クリック数: {summary.get('total_clicks', 0):,}
📈 CTR: {summary.get('avg_ctr', 0):.2f}%
💵 CPC: ¥{summary.get('avg_cpc', 0):.2f}
📊 RPM: ¥{summary.get('avg_rpm', 0):.2f}
💰 見積もり収益: ¥{summary.get('total_earnings', 0):,.2f}
"""

            # パフォーマンス指標
            if analytics_data['total'].get('page_views', 0) > 0:
                earnings_per_user = summary.get('total_earnings', 0) / analytics_data['total'].get('active_users', 1)
                report += f"""
【📈 パフォーマンス指標】
💰 ユーザーあたり収益: ¥{earnings_per_user:.2f}
📊 収益化率: {(summary.get('total_clicks', 0) / analytics_data['total'].get('page_views', 1) * 100):.2f}%
"""

        report += "\n━━━━━━━━━━━━━━━━━━━━━━━"

        messages = [{"type": "text", "text": report}]
        self.notifier._send_custom_messages(messages)
        log_event("UNIFIED_REPORT", "統合日次レポート送信完了")

    def send_weekly_unified_report(self, end_date: Optional[str] = None, adsense_csv: Optional[str] = None):
        """
        週次統合レポートを送信

        Args:
            end_date: 終了日 (YYYY-MM-DD、Noneの場合は昨日)
            adsense_csv: AdSense CSVファイルのパス
        """
        if end_date is None:
            end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=6)).strftime("%Y-%m-%d")

        log_event("UNIFIED_REPORT", f"統合週次レポート生成中: {start_date} - {end_date}")

        # Analyticsデータ取得
        analytics_data = self.analytics.get_weekly_report(end_date)
        top_pages = self.analytics.get_top_pages(start_date, end_date, limit=5)

        report = f"""━━━━━━━━━━━━━━━━━━━━━━━
📊 K-TREND TIMES 週次レポート
📅 {start_date} 〜 {end_date}
━━━━━━━━━━━━━━━━━━━━━━━

【📊 Google Analytics】
👥 アクティブユーザー: {analytics_data['total'].get('active_users', 0):,}
🔄 セッション数: {analytics_data['total'].get('sessions', 0):,}
📄 ページビュー: {analytics_data['total'].get('page_views', 0):,}
⏱️ 平均セッション時間: {self._format_duration(analytics_data['total'].get('avg_session_duration', 0))}
📈 直帰率: {analytics_data['total'].get('bounce_rate', 0):.1%}
"""

        # AdSenseデータがある場合は追加
        if adsense_csv and os.path.exists(adsense_csv):
            adsense_data = self.adsense.get_weekly_report(end_date, adsense_csv)
            summary = adsense_data.get('summary', {})

            report += f"""
【💰 Google AdSense】
👆 クリック数: {summary.get('total_clicks', 0):,}
📈 CTR: {summary.get('avg_ctr', 0):.2f}%
💵 CPC: ¥{summary.get('avg_cpc', 0):.2f}
📊 RPM: ¥{summary.get('avg_rpm', 0):.2f}
💰 見積もり収益: ¥{summary.get('total_earnings', 0):,.2f}
"""

        # 人気記事
        if top_pages:
            report += "\n【🔥 人気記事 TOP5】\n"
            for i, page in enumerate(top_pages, 1):
                report += f"{i}. {page['title']}\n   {page['page_views']:,} PV\n"

        report += "\n━━━━━━━━━━━━━━━━━━━━━━━"

        messages = [{"type": "text", "text": report}]
        self.notifier._send_custom_messages(messages)
        log_event("UNIFIED_REPORT", "統合週次レポート送信完了")

    def send_monthly_unified_report(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        adsense_csv: Optional[str] = None
    ):
        """
        月次統合レポートを送信

        Args:
            year: 年 (Noneの場合は先月)
            month: 月 (Noneの場合は先月)
            adsense_csv: AdSense CSVファイルのパス
        """
        if year is None or month is None:
            last_month = datetime.now().replace(day=1) - timedelta(days=1)
            year = last_month.year
            month = last_month.month

        log_event("UNIFIED_REPORT", f"統合月次レポート生成中: {year}年{month}月")

        # Analyticsデータ取得
        analytics_data = self.analytics.get_monthly_report(year, month)

        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            end_date = (datetime(year, month + 1, 1) - timedelta(days=1)).strftime("%Y-%m-%d")

        top_pages = self.analytics.get_top_pages(start_date, end_date, limit=10)
        sources = self.analytics.get_traffic_sources(start_date, end_date)

        days_count = len(analytics_data.get('daily', []))

        report = f"""━━━━━━━━━━━━━━━━━━━━━━━
📊 K-TREND TIMES 月次レポート
📅 {year}年{month}月
━━━━━━━━━━━━━━━━━━━━━━━

【📊 Google Analytics】
👥 アクティブユーザー: {analytics_data['total'].get('active_users', 0):,}
🔄 セッション数: {analytics_data['total'].get('sessions', 0):,}
📄 ページビュー: {analytics_data['total'].get('page_views', 0):,}
⏱️ 平均セッション時間: {self._format_duration(analytics_data['total'].get('avg_session_duration', 0))}
📈 直帰率: {analytics_data['total'].get('bounce_rate', 0):.1%}

📊 日別平均:
📄 PV/日: {analytics_data['total'].get('page_views', 0) / days_count if days_count > 0 else 0:,.0f}
👥 ユーザー/日: {analytics_data['total'].get('active_users', 0) / days_count if days_count > 0 else 0:,.0f}
"""

        # AdSenseデータがある場合は追加
        if adsense_csv and os.path.exists(adsense_csv):
            adsense_data = self.adsense.get_monthly_report(year, month, adsense_csv)
            summary = adsense_data.get('summary', {})
            adsense_days = len(adsense_data.get('data', []))

            report += f"""
【💰 Google AdSense】
👆 クリック数: {summary.get('total_clicks', 0):,}
📈 CTR: {summary.get('avg_ctr', 0):.2f}%
💵 CPC: ¥{summary.get('avg_cpc', 0):.2f}
📊 RPM: ¥{summary.get('avg_rpm', 0):.2f}
💰 見積もり収益: ¥{summary.get('total_earnings', 0):,.2f}

💰 日別平均収益: ¥{summary.get('total_earnings', 0) / adsense_days if adsense_days > 0 else 0:,.2f}
"""

        # 人気記事
        if top_pages:
            report += "\n【🔥 人気記事 TOP10】\n"
            for i, page in enumerate(top_pages, 1):
                report += f"{i}. {page['title'][:50]}...\n   {page['page_views']:,} PV\n"

        # トラフィックソース
        if sources:
            report += "\n【🌐 トラフィックソース TOP5】\n"
            for i, source in enumerate(sources[:5], 1):
                report += f"{i}. {source['source']} / {source['medium']}\n   {source['sessions']:,} セッション\n"

        report += "\n━━━━━━━━━━━━━━━━━━━━━━━"

        messages = [{"type": "text", "text": report}]
        self.notifier._send_custom_messages(messages)
        log_event("UNIFIED_REPORT", "統合月次レポート送信完了")

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


def main():
    """メイン実行関数"""
    import yaml
    try:
        with open('.env.yaml', 'r') as f:
            env_vars = yaml.safe_load(f)
            for k, v in env_vars.items():
                os.environ[k] = str(v)
    except Exception as e:
        print(f"Error loading .env.yaml: {e}")
        load_dotenv()

    # 環境変数から設定を取得
    property_id = os.getenv("GA4_PROPERTY_ID")
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    adsense_csv = os.getenv("ADSENSE_CSV_PATH")

    if not property_id or not credentials_path:
        print("❌ エラー: GA4_PROPERTY_ID と GOOGLE_APPLICATION_CREDENTIALS を .env.yaml に設定してください")
        return

    # レポーター初期化
    analytics = AnalyticsReporter(property_id, credentials_path)
    adsense = AdSenseReporter()
    notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
    unified = UnifiedReporter(analytics, adsense, notifier)

    # 実行例
    import sys
    if len(sys.argv) < 2:
        print("使用法:")
        print("  python -m src.unified_reporter daily [日付]")
        print("  python -m src.unified_reporter weekly [終了日]")
        print("  python -m src.unified_reporter monthly [年] [月]")
        return

    report_type = sys.argv[1]

    if report_type == "daily":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        unified.send_daily_unified_report(date, adsense_csv)
    elif report_type == "weekly":
        end_date = sys.argv[2] if len(sys.argv) > 2 else None
        unified.send_weekly_unified_report(end_date, adsense_csv)
    elif report_type == "monthly":
        year = int(sys.argv[2]) if len(sys.argv) > 2 else None
        month = int(sys.argv[3]) if len(sys.argv) > 3 else None
        unified.send_monthly_unified_report(year, month, adsense_csv)
    else:
        print(f"❌ 不明なレポートタイプ: {report_type}")


if __name__ == "__main__":
    main()
