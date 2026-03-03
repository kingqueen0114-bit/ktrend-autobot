"""6カテゴリの設定を一元管理"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class CategoryConfig:
    id: str                    # WordPressカテゴリスラッグ
    name: str                  # 日本語名
    emoji: str                 # 表示用
    wp_category_id: int        # WordPressカテゴリID（要設定）
    min_chars: int             # 最小文字数
    max_chars: int             # 最大文字数
    prompt_file: str           # system_instructionファイル名
    source_type: str           # "prtimes" | "grounding" | "both"
    ai_discretion: str         # "low" | "medium" | "high"
    daily_target: int          # 1日の目標記事数
    grounding_enabled: bool    # Grounding検索を使うか
    speculation_strict: bool   # 推測表現チェックを厳しくするか
    source_citation_required: bool  # 出典記載必須か
    search_queries: List[str] = field(default_factory=list)
    prtimes_keywords: List[str] = field(default_factory=list)
    extra_checks: List[str] = field(default_factory=list)


# ★ wp_category_idはWordPress管理画面で確認して設定すること
CATEGORIES = {
    "kpop": CategoryConfig(
        id="kpop",
        name="K-pop",
        emoji="🎤",
        wp_category_id=11,  # アーティスト
        min_chars=400,
        max_chars=1000,
        prompt_file="system_instruction_kpop.txt",
        source_type="both",
        ai_discretion="low",
        daily_target=3,
        grounding_enabled=True,
        speculation_strict=True,
        source_citation_required=True,
        search_queries=[
            "K-POP 最新ニュース",
            "K-POP カムバック 新曲 2026",
            "韓国アイドル 日本 活動",
        ],
        prtimes_keywords=[
            "K-POP", "韓国アイドル", "韓流",
            "HYBE", "JYP", "SM Entertainment", "YG", "Starship",
            "BTS", "SEVENTEEN", "ENHYPEN", "NewJeans", "LE SSERAFIM",
            "IVE", "aespa", "Stray Kids", "ATEEZ", "TWICE", "NCT",
            "TXT", "ITZY", "NMIXX", "BOYNEXTDOOR", "ILLIT",
            "カムバック", "日本デビュー", "ワールドツアー",
        ],
        extra_checks=["speculation_check"],
    ),
    "cosme": CategoryConfig(
        id="cosme",
        name="コスメ",
        emoji="💄",
        wp_category_id=7,  # ビューティー
        min_chars=800,
        max_chars=1200,
        prompt_file="system_instruction_cosme.txt",
        source_type="both",
        ai_discretion="medium",
        daily_target=1,
        grounding_enabled=True,
        speculation_strict=False,
        source_citation_required=False,
        search_queries=[
            "韓国コスメ 新作 2026年",
            "韓国コスメ 人気 ランキング",
            "K-POPアイドル 愛用コスメ",
            "オリーブヤング 人気商品",
            "rom&nd CLIO innisfree 新商品",
        ],
        prtimes_keywords=[
            "韓国コスメ", "コスメ", "スキンケア", "メイク",
            "リップ", "アイシャドウ", "ファンデーション",
            "rom&nd", "CLIO", "innisfree", "ETUDE", "AMUSE",
            "LANEIGE", "Sulwhasoo", "HERA", "espoir",
            "オリーブヤング", "Qoo10", "メガ割",
            "アンバサダー", "ビューティー",
        ],
        extra_checks=["efficacy_check"],
    ),
    "fashion": CategoryConfig(
        id="fashion",
        name="ファッション",
        emoji="👗",
        wp_category_id=10,  # ファッション
        min_chars=800,
        max_chars=1200,
        prompt_file="system_instruction_fashion.txt",
        source_type="grounding",
        ai_discretion="medium",
        daily_target=1,
        grounding_enabled=True,
        speculation_strict=False,
        source_citation_required=False,
        search_queries=[
            "韓国ファッション トレンド 2026",
            "K-POPアイドル 私服 ファッション",
            "韓国 ストリートファッション 最新",
            "韓国ブランド 日本上陸",
        ],
        prtimes_keywords=[
            "韓国ファッション", "ファッション", "アパレル",
            "ADER ERROR", "GENTLE MONSTER", "MARDI MERCREDI",
            "KIRSH", "NERDY", "MLB Korea",
        ],
        extra_checks=[],
    ),
    "gourmet": CategoryConfig(
        id="gourmet",
        name="グルメ",
        emoji="🍜",
        wp_category_id=6,  # グルメ
        min_chars=800,
        max_chars=1200,
        prompt_file="system_instruction_gourmet.txt",
        source_type="grounding",
        ai_discretion="medium",
        daily_target=1,
        grounding_enabled=True,
        speculation_strict=False,
        source_citation_required=False,
        search_queries=[
            "韓国料理 トレンド 2026 日本",
            "韓国 カフェ 人気 ソウル",
            "韓国フード 新大久保 トレンド",
            "韓国 チキン トッポギ 新メニュー",
        ],
        prtimes_keywords=[
            "韓国料理", "韓国グルメ", "韓国フード",
            "チキン", "トッポギ", "ビビンバ", "サムギョプサル",
            "新大久保", "韓国カフェ",
        ],
        extra_checks=["freshness_check"],
    ),
    "travel": CategoryConfig(
        id="travel",
        name="旅行",
        emoji="✈️",
        wp_category_id=4,  # 韓国旅行
        min_chars=1000,
        max_chars=2000,
        prompt_file="system_instruction_travel.txt",
        source_type="grounding",
        ai_discretion="high",
        daily_target=1,
        grounding_enabled=True,
        speculation_strict=False,
        source_citation_required=False,
        search_queries=[
            "韓国旅行 ソウル 最新スポット 2026",
            "K-POP 聖地巡礼 おすすめ",
            "韓国 カフェ グルメ おすすめ",
            "韓国旅行 お土産 人気",
            "ソウル 弘大 明洞 江南 観光",
        ],
        prtimes_keywords=[
            "韓国旅行", "渡韓", "ソウル", "釜山",
            "明洞", "弘大", "江南", "聖地巡礼",
            "韓国観光", "仁川空港",
        ],
        extra_checks=["freshness_check"],
    ),
    "event": CategoryConfig(
        id="event",
        name="イベント",
        emoji="🎪",
        wp_category_id=5,  # イベント
        min_chars=500,
        max_chars=800,
        prompt_file="system_instruction_event.txt",
        source_type="both",
        ai_discretion="low",
        daily_target=1,
        grounding_enabled=True,
        speculation_strict=True,
        source_citation_required=True,
        search_queries=[
            "K-POP 来日公演 2026",
            "K-POP ファンミーティング 日本",
            "K-POP コンサート 東京 大阪",
            "KCON 日本 2026",
        ],
        prtimes_keywords=[
            "来日公演", "ライブ", "コンサート", "ファンミーティング",
            "ツアー", "チケット", "開催", "KCON",
            "アリーナ", "ドーム", "会場", "ファンミ",
            "オンラインイベント", "配信ライブ",
        ],
        extra_checks=["date_accuracy_check", "speculation_check"],
    ),
}


def get_category(category_id: str) -> CategoryConfig:
    """カテゴリ設定を取得"""
    if category_id not in CATEGORIES:
        raise ValueError(f"Unknown category: {category_id}")
    return CATEGORIES[category_id]


def get_all_categories() -> dict:
    """全カテゴリ設定を取得"""
    return CATEGORIES
