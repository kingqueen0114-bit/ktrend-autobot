"""
カテゴリ別の記事出力スキーマ（OpenAPI Schema Object形式）
既存の article_schema.py と同じ形式で、Gemini REST API の responseSchema に渡す。
"""

# 全カテゴリ共通の基本フィールド
_BASE_PROPERTIES = {
    "title": {
        "type": "STRING",
        "description": "記事タイトル。25-50文字"
    },
    "meta_description": {
        "type": "STRING",
        "description": "メタディスクリプション。60-120文字"
    },
    "body": {
        "type": "STRING",
        "description": "記事本文。ソースに基づく正確な内容"
    },
    "x_post_1": {
        "type": "STRING",
        "description": "X投稿テキスト1枚目。タメ語、ハッシュタグ3つ含む"
    },
    "x_post_2": {
        "type": "STRING",
        "description": "X投稿テキスト2枚目。補足情報、ハッシュタグ3つ含む"
    },
    "tags": {
        "type": "ARRAY",
        "items": {"type": "STRING"},
        "description": "記事タグ。3-5個"
    },
    "artist_tags": {
        "type": "ARRAY",
        "items": {"type": "STRING"},
        "description": "関連アーティスト名"
    },
    "highlights": {
        "type": "ARRAY",
        "items": {"type": "STRING"},
        "description": "記事の要点。3つ"
    },
    "research_report": {
        "type": "STRING",
        "description": "内部用リサーチ報告。200字以内"
    },
}

_BASE_REQUIRED = [
    "title", "meta_description", "body",
    "x_post_1", "x_post_2",
    "tags", "artist_tags", "highlights", "research_report"
]


def _make_schema(extra_properties: dict = None, extra_required: list = None) -> dict:
    """ベーススキーマにカテゴリ固有フィールドを追加"""
    props = {**_BASE_PROPERTIES}
    if extra_properties:
        props.update(extra_properties)
    required = list(_BASE_REQUIRED)
    if extra_required:
        required.extend(extra_required)
    return {
        "type": "OBJECT",
        "properties": props,
        "required": required,
    }


# --- カテゴリ別スキーマ ---

KPOP_SCHEMA = _make_schema(
    extra_properties={
        "source_company": {
            "type": "STRING",
            "description": "配信企業名"
        },
        "source_url": {
            "type": "STRING",
            "description": "ソースURL"
        },
        "event_date": {
            "type": "STRING",
            "description": "関連日時（あれば）"
        },
    }
)

COSME_SCHEMA = _make_schema(
    extra_properties={
        "brand_names": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "紹介ブランド名リスト"
        },
        "product_names": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "紹介製品名リスト"
        },
        "price_range": {
            "type": "STRING",
            "description": "価格帯（例: 1,500〜3,000円）"
        },
    }
)

FASHION_SCHEMA = _make_schema(
    extra_properties={
        "brand_names": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "紹介ブランド名リスト"
        },
        "season": {
            "type": "STRING",
            "description": "シーズン（例: 2026年春夏）"
        },
    }
)

GOURMET_SCHEMA = _make_schema(
    extra_properties={
        "spot_names": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "紹介スポット/店舗名"
        },
        "area": {
            "type": "STRING",
            "description": "エリア名（例: 新大久保、明洞）"
        },
    }
)

TRAVEL_SCHEMA = _make_schema(
    extra_properties={
        "area": {
            "type": "STRING",
            "description": "エリア名（ソウル、釜山等）"
        },
        "spots": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "紹介スポットのリスト"
        },
        "season": {
            "type": "STRING",
            "description": "推奨時期"
        },
    }
)

EVENT_SCHEMA = _make_schema(
    extra_properties={
        "source_company": {
            "type": "STRING",
            "description": "配信企業名"
        },
        "source_url": {
            "type": "STRING",
            "description": "ソースURL"
        },
        "event_name": {
            "type": "STRING",
            "description": "イベント正式名称"
        },
        "event_date": {
            "type": "STRING",
            "description": "開催日"
        },
        "event_venue": {
            "type": "STRING",
            "description": "会場名"
        },
        "ticket_info": {
            "type": "STRING",
            "description": "チケット情報の要約"
        },
    },
    extra_required=["event_name"]
)


# カテゴリIDとスキーマのマッピング
CATEGORY_SCHEMAS = {
    "kpop": KPOP_SCHEMA,
    "cosme": COSME_SCHEMA,
    "fashion": FASHION_SCHEMA,
    "gourmet": GOURMET_SCHEMA,
    "travel": TRAVEL_SCHEMA,
    "event": EVENT_SCHEMA,
}


def get_category_schema(category_id: str) -> dict:
    """カテゴリIDからスキーマを取得。不明なカテゴリの場合はベーススキーマ"""
    return CATEGORY_SCHEMAS.get(category_id, _make_schema())
