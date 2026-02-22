#!/bin/bash
# K-TREND TIMES Analytics & AdSense レポート実行スクリプト

set -e

# 色付き出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# .envファイルの確認
if [ ! -f .env ]; then
    echo -e "${RED}❌ エラー: .envファイルが見つかりません${NC}"
    echo "  .env.exampleをコピーして.envを作成してください"
    exit 1
fi

# 使用法を表示
usage() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📊 K-TREND TIMES アナリティクスレポート${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "使用法:"
    echo "  $0 <レポートタイプ> [オプション]"
    echo ""
    echo "レポートタイプ:"
    echo "  daily              日次レポート（昨日）"
    echo "  daily <日付>       日次レポート（指定日）"
    echo "  weekly             週次レポート（過去7日間）"
    echo "  weekly <終了日>    週次レポート（指定期間）"
    echo "  monthly            月次レポート（先月）"
    echo "  monthly <年> <月>  月次レポート（指定月）"
    echo ""
    echo "例:"
    echo "  $0 daily                    # 昨日のレポート"
    echo "  $0 daily 2026-02-07         # 2026-02-07のレポート"
    echo "  $0 weekly                   # 過去7日間のレポート"
    echo "  $0 weekly 2026-02-07        # 2026-02-01〜2026-02-07のレポート"
    echo "  $0 monthly                  # 先月のレポート"
    echo "  $0 monthly 2026 1           # 2026年1月のレポート"
    echo ""
    exit 1
}

# 引数チェック
if [ $# -lt 1 ]; then
    usage
fi

REPORT_TYPE=$1

# レポートタイプに応じて実行
case $REPORT_TYPE in
    daily)
        echo -e "${GREEN}📅 日次レポートを生成しています...${NC}"
        if [ $# -ge 2 ]; then
            python -m src.unified_reporter daily "$2"
        else
            python -m src.unified_reporter daily
        fi
        ;;

    weekly)
        echo -e "${GREEN}📊 週次レポートを生成しています...${NC}"
        if [ $# -ge 2 ]; then
            python -m src.unified_reporter weekly "$2"
        else
            python -m src.unified_reporter weekly
        fi
        ;;

    monthly)
        echo -e "${GREEN}📈 月次レポートを生成しています...${NC}"
        if [ $# -ge 3 ]; then
            python -m src.unified_reporter monthly "$2" "$3"
        else
            python -m src.unified_reporter monthly
        fi
        ;;

    help|--help|-h)
        usage
        ;;

    *)
        echo -e "${RED}❌ エラー: 不明なレポートタイプ: $REPORT_TYPE${NC}"
        echo ""
        usage
        ;;
esac

# 完了メッセージ
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ レポート送信完了！${NC}"
else
    echo ""
    echo -e "${RED}❌ レポート送信に失敗しました${NC}"
    exit 1
fi
