"""
K-TREND TIMES AdSense Reporter
Google AdSenseの収益データを取得して日次・週次・月次レポートを生成

注意: AdSense Management APIは現在サポートされていないため、
このスクリプトではAdSense画面からエクスポートしたCSVデータを読み込む方式を使用します。
"""

import os
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv

# LINE通知用
from src.notifier import LineNotifier


class AdSenseReporter:
    """AdSenseデータを解析してレポートを生成"""

    def __init__(self, data_dir: str = "./adsense_data"):
        """
        Args:
            data_dir: AdSense CSVデータを保存するディレクトリ
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def parse_csv(self, csv_path: str) -> List[Dict]:
        """
        AdSense CSVファイルを解析

        Args:
            csv_path: CSVファイルのパス

        Returns:
            日別データのリスト
        """
        data = []
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "date": row.get("日付", row.get("Date", "")),
                    "page_views": int(row.get("ページビュー", row.get("Page views", "0")).replace(",", "")),
                    "clicks": int(row.get("クリック数", row.get("Clicks", "0")).replace(",", "")),
                    "ctr": float(row.get("クリック率", row.get("CTR", "0")).replace("%", "")),
                    "cpc": float(row.get("CPC", row.get("CPC", "0")).replace("$", "").replace("¥", "").replace(",", "")),
                    "rpm": float(row.get("RPM", row.get("RPM", "0")).replace("$", "").replace("¥", "").replace(",", "")),
                    "earnings": float(row.get("見積もり収益額", row.get("Estimated earnings", "0")).replace("$", "").replace("¥", "").replace(",", "")),
                })
        return data

    def get_daily_summary(self, data: List[Dict]) -> Dict:
        """日別データから合計を計算"""
        if not data:
            return {
                "total_page_views": 0,
                "total_clicks": 0,
                "avg_ctr": 0.0,
                "avg_cpc": 0.0,
                "avg_rpm": 0.0,
                "total_earnings": 0.0,
            }

        total_page_views = sum(d["page_views"] for d in data)
        total_clicks = sum(d["clicks"] for d in data)
        total_earnings = sum(d["earnings"] for d in data)

        return {
            "total_page_views": total_page_views,
            "total_clicks": total_clicks,
            "avg_ctr": (total_clicks / total_page_views * 100) if total_page_views > 0 else 0.0,
            "avg_cpc": (total_earnings / total_clicks) if total_clicks > 0 else 0.0,
            "avg_rpm": (total_earnings / total_page_views * 1000) if total_page_views > 0 else 0.0,
            "total_earnings": total_earnings,
        }

    def get_daily_report(self, date: str, csv_path: str) -> Dict:
        """
        日次レポートを取得

        Args:
            date: 取得日 (YYYY-MM-DD)
            csv_path: AdSense CSVファイルのパス

        Returns:
            レポートデータ
        """
        all_data = self.parse_csv(csv_path)
        daily_data = [d for d in all_data if d["date"] == date]

        if not daily_data:
            return {"summary": self.get_daily_summary([]), "data": []}

        return {
            "summary": self.get_daily_summary(daily_data),
            "data": daily_data
        }

    def get_weekly_report(self, end_date: str, csv_path: str) -> Dict:
        """
        週次レポートを取得（過去7日間）

        Args:
            end_date: 終了日 (YYYY-MM-DD)
            csv_path: AdSense CSVファイルのパス

        Returns:
            レポートデータ
        """
        end = datetime.strptime(end_date, "%Y-%m-%d")
        start = end - timedelta(days=6)

        all_data = self.parse_csv(csv_path)
        weekly_data = []

        for d in all_data:
            date_obj = datetime.strptime(d["date"], "%Y-%m-%d")
            if start <= date_obj <= end:
                weekly_data.append(d)

        return {
            "summary": self.get_daily_summary(weekly_data),
            "data": weekly_data,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end_date
        }

    def get_monthly_report(self, year: int, month: int, csv_path: str) -> Dict:
        """
        月次レポートを取得

        Args:
            year: 年
            month: 月
            csv_path: AdSense CSVファイルのパス

        Returns:
            レポートデータ
        """
        all_data = self.parse_csv(csv_path)
        monthly_data = []

        for d in all_data:
            date_obj = datetime.strptime(d["date"], "%Y-%m-%d")
            if date_obj.year == year and date_obj.month == month:
                monthly_data.append(d)

        return {
            "summary": self.get_daily_summary(monthly_data),
            "data": monthly_data,
            "year": year,
            "month": month
        }


class AdSenseFormatter:
    """AdSenseレポートをフォーマット"""

    @staticmethod
    def format_daily_report(data: Dict, date: str) -> str:
        """日次AdSenseレポートをフォーマット"""
        summary = data.get("summary", {})

        report = f"""💰 K-TREND TIMES AdSense 日次レポート
📅 {date}

📊 パフォーマンス:
📄 ページビュー: {summary.get('total_page_views', 0):,}
👆 クリック数: {summary.get('total_clicks', 0):,}
📈 CTR: {summary.get('avg_ctr', 0):.2f}%
💵 CPC: ¥{summary.get('avg_cpc', 0):.2f}
📊 RPM: ¥{summary.get('avg_rpm', 0):.2f}

💰 見積もり収益: ¥{summary.get('total_earnings', 0):,.2f}
"""
        return report

    @staticmethod
    def format_weekly_report(data: Dict) -> str:
        """週次AdSenseレポートをフォーマット"""
        summary = data.get("summary", {})
        start_date = data.get("start_date", "")
        end_date = data.get("end_date", "")
        daily_data = data.get("data", [])

        report = f"""💰 K-TREND TIMES AdSense 週次レポート
📅 {start_date} 〜 {end_date}

【全体サマリー】
📄 ページビュー: {summary.get('total_page_views', 0):,}
👆 クリック数: {summary.get('total_clicks', 0):,}
📈 CTR: {summary.get('avg_ctr', 0):.2f}%
💵 CPC: ¥{summary.get('avg_cpc', 0):.2f}
📊 RPM: ¥{summary.get('avg_rpm', 0):.2f}
💰 見積もり収益: ¥{summary.get('total_earnings', 0):,.2f}

【日別推移】
"""
        for day in daily_data:
            report += f"{day['date']}: ¥{day['earnings']:,.2f} ({day['clicks']} クリック)\n"

        if daily_data:
            avg_daily_earnings = summary.get('total_earnings', 0) / len(daily_data)
            report += f"\n📊 1日平均収益: ¥{avg_daily_earnings:,.2f}"

        return report

    @staticmethod
    def format_monthly_report(data: Dict) -> str:
        """月次AdSenseレポートをフォーマット"""
        summary = data.get("summary", {})
        year = data.get("year", "")
        month = data.get("month", "")
        daily_data = data.get("data", [])

        report = f"""💰 K-TREND TIMES AdSense 月次レポート
📅 {year}年{month}月

【全体サマリー】
📄 ページビュー: {summary.get('total_page_views', 0):,}
👆 クリック数: {summary.get('total_clicks', 0):,}
📈 CTR: {summary.get('avg_ctr', 0):.2f}%
💵 CPC: ¥{summary.get('avg_cpc', 0):.2f}
📊 RPM: ¥{summary.get('avg_rpm', 0):.2f}
💰 見積もり収益: ¥{summary.get('total_earnings', 0):,.2f}

【日別平均】
"""
        if daily_data:
            avg_daily_pv = summary.get('total_page_views', 0) / len(daily_data)
            avg_daily_clicks = summary.get('total_clicks', 0) / len(daily_data)
            avg_daily_earnings = summary.get('total_earnings', 0) / len(daily_data)

            report += f"📄 平均PV/日: {avg_daily_pv:,.0f}\n"
            report += f"👆 平均クリック/日: {avg_daily_clicks:,.1f}\n"
            report += f"💰 平均収益/日: ¥{avg_daily_earnings:,.2f}\n"

            # トップ5の日
            sorted_days = sorted(daily_data, key=lambda x: x["earnings"], reverse=True)
            report += "\n【収益トップ5の日】\n"
            for i, day in enumerate(sorted_days[:5], 1):
                report += f"{i}. {day['date']}: ¥{day['earnings']:,.2f}\n"

        return report


class AdSenseReportScheduler:
    """AdSenseレポートのスケジュール実行を管理"""

    def __init__(self, adsense_reporter: AdSenseReporter, line_notifier: LineNotifier):
        self.adsense = adsense_reporter
        self.notifier = line_notifier
        self.formatter = AdSenseFormatter()

    def send_daily_report(self, date: str, csv_path: str):
        """日次レポートを送信"""
        print(f"💰 AdSense 日次レポート生成中: {date}")
        data = self.adsense.get_daily_report(date, csv_path)
        report_text = self.formatter.format_daily_report(data, date)

        messages = [{"type": "text", "text": report_text}]
        self.notifier.push_message(self.notifier.admin_user_id, messages)
        print("✅ AdSense 日次レポート送信完了")

    def send_weekly_report(self, end_date: str, csv_path: str):
        """週次レポートを送信"""
        print(f"💰 AdSense 週次レポート生成中")
        data = self.adsense.get_weekly_report(end_date, csv_path)
        report_text = self.formatter.format_weekly_report(data)

        messages = [{"type": "text", "text": report_text}]
        self.notifier.push_message(self.notifier.admin_user_id, messages)
        print("✅ AdSense 週次レポート送信完了")

    def send_monthly_report(self, year: int, month: int, csv_path: str):
        """月次レポートを送信"""
        print(f"💰 AdSense 月次レポート生成中: {year}年{month}月")
        data = self.adsense.get_monthly_report(year, month, csv_path)
        report_text = self.formatter.format_monthly_report(data)

        messages = [{"type": "text", "text": report_text}]
        self.notifier.push_message(self.notifier.admin_user_id, messages)
        print("✅ AdSense 月次レポート送信完了")


def main():
    """メイン実行関数"""
    load_dotenv()

    # レポーター初期化
    adsense = AdSenseReporter()
    notifier = LineNotifier()
    scheduler = AdSenseReportScheduler(adsense, notifier)

    # 実行例
    import sys
    if len(sys.argv) < 3:
        print("使用法:")
        print("  python -m src.adsense_reporter daily <CSVパス> [日付]")
        print("  python -m src.adsense_reporter weekly <CSVパス> [終了日]")
        print("  python -m src.adsense_reporter monthly <CSVパス> [年] [月]")
        print("\n注意: AdSense管理画面からCSVファイルをエクスポートしてください")
        return

    report_type = sys.argv[1]
    csv_path = sys.argv[2]

    if not os.path.exists(csv_path):
        print(f"❌ エラー: CSVファイルが見つかりません: {csv_path}")
        return

    if report_type == "daily":
        date = sys.argv[3] if len(sys.argv) > 3 else (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        scheduler.send_daily_report(date, csv_path)
    elif report_type == "weekly":
        end_date = sys.argv[3] if len(sys.argv) > 3 else (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        scheduler.send_weekly_report(end_date, csv_path)
    elif report_type == "monthly":
        year = int(sys.argv[3]) if len(sys.argv) > 3 else datetime.now().year
        month = int(sys.argv[4]) if len(sys.argv) > 4 else datetime.now().month
        scheduler.send_monthly_report(year, month, csv_path)
    else:
        print(f"❌ 不明なレポートタイプ: {report_type}")


if __name__ == "__main__":
    main()
