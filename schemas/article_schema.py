"""
K-Trend Times Article JSON Schema
タスク1-B: Gemini REST APIの responseSchema に渡すJSON Schema定義。
API レベルで出力形式を強制し、構造化されたJSON応答を保証する。
"""

# REST API の responseSchema に渡す形式（OpenAPI Schema Object）
ARTICLE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "title": {
            "type": "STRING",
            "description": "記事タイトル。30-50文字。読者がクリックしたくなる表現"
        },
        "meta_description": {
            "type": "STRING",
            "description": "メタディスクリプション。80-120文字で記事を要約"
        },
        "body": {
            "type": "STRING",
            "description": "記事本文。Markdown形式。1000字以上。各段落末にソース参照を明記。参照元の実際のURLを本文内にテキストとして記載すること"
        },
        "x_post_1": {
            "type": "STRING",
            "description": "X投稿文1枚目。タメ語、フック重視、ハッシュタグ3つ含む"
        },
        "x_post_2": {
            "type": "STRING",
            "description": "X投稿文2枚目。補足情報、ハッシュタグ3つ含む"
        },
        "artist_tags": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "関連するアーティスト名やキーワード"
        },
        "tags": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "記事タグ。3-5個"
        },
        "highlights": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "記事の要約サマリー。読者がこの3つを読むだけで記事の核心が分かるように、具体的な事実・数字・日付・場所を含めた要約文を3つ。各要約文は30-60文字。プレースホルダー（例：最新情報、情報1）は絶対に使わないこと"
        },
        "research_report": {
            "type": "STRING",
            "description": "内部用リサーチ報告。流行のサイン分析と記事選定理由。200字以内"
        },
    },
    "required": [
        "title", "meta_description", "body",
        "x_post_1", "x_post_2",
        "artist_tags", "tags", "highlights",
        "research_report"
    ],
}

# リライト用のスキーマ（一部フィールドのみ）
REWRITE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "title": {
            "type": "STRING",
            "description": "改善された記事タイトル"
        },
        "meta_description": {
            "type": "STRING",
            "description": "改善されたメタディスクリプション"
        },
        "body": {
            "type": "STRING",
            "description": "改善された記事本文（Markdown形式）"
        },
        "tags": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "記事タグ"
        },
        "highlights": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "記事の要約サマリー。具体的な事実・数字・日付・場所を含む要約文を3つ。各30-60文字"
        },
        "research_report": {
            "type": "STRING",
            "description": "内部用リサーチ報告"
        },
    },
    "required": ["title", "meta_description", "body", "tags", "highlights"],
}
