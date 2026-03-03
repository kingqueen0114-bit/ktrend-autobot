"""
K-Trend Times 品質チェック & 自動修正 ユニットテスト

テスト項目:
1. auto_fix テスト: **強調**、■マーク、過剰な ! の自動修正
2. quality_check テスト: 各チェック項目の正常動作
3. スキーマテスト: ARTICLE_SCHEMA の構造検証
4. system_instruction テスト: ファイル読み込み動作
5. grounding_parser テスト: メタデータ抽出
"""

import sys
import os
import pytest

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from checks.auto_fix import auto_fix_article
from checks.quality_check import quality_check
from schemas.article_schema import ARTICLE_SCHEMA, REWRITE_SCHEMA
from utils.grounding_parser import parse_grounding_metadata, get_verified_urls


# ==========================================
# テスト用モックデータ
# ==========================================

def _make_good_article():
    """品質チェックを通過する正常な記事データ"""
    return {
        "title": "韓国で話題の新コスメブランド「TIRTIR」が日本上陸！注目アイテムを徹底解説",
        "meta_description": "韓国コスメブランドTIRTIRが日本に上陸。SNSで話題のクッションファンデやスキンケア製品の魅力を、韓国トレンドの視点から詳しく解説します。",
        "body": """## 韓国コスメ界の新星「TIRTIR」がついに日本上陸

韓国で絶大な人気を誇るコスメブランド「TIRTIR（ティルティル）」が、2026年2月に日本市場に正式参入することが発表されました。

### SNSでの注目度が急上昇中

TIRTIRのクッションファンデーションは、韓国のSNSで「#ティルティル」のハッシュタグ投稿が50万件を超える勢いで拡散されています。特にTikTokでの「密着力検証」動画が大きな話題を呼んでいます。この兆しは日本市場でも同様のブームが起きる可能性を示しています。

### 流行のサイン分析

日本のSNSでも注目度が急上昇しており、「韓国で買ってきた」という投稿が増加中です。Qoo10やAmazonでの検索数も前月比200%増と報じられています。

### まとめ

TIRTIRの日本上陸は、韓国コスメトレンドの新たな波を予感させます。今後の展開にも目が離せません。

参照元: https://prtimes.jp/example/tirtir-japan
""",
        "x_post_1": "TIRTIRが日本に来るってマジ？！クッションファンデ最強すぎるんだけど😍 #韓国コスメ #TIRTIR #コスメ好きと繋がりたい",
        "x_post_2": "韓国で50万投稿超えのTIRTIRが日本上陸！詳しくはプロフのリンクから✨ #ティルティル #美容垢さんと繋がりたい #スキンケア",
        "artist_tags": ["TIRTIR"],
        "tags": ["韓国コスメ", "TIRTIR", "クッションファンデ", "スキンケア"],
        "highlights": [
            "TIRTIRが2026年2月に日本上陸",
            "韓国SNSで50万投稿超えの人気",
            "クッションファンデが最注目アイテム"
        ],
        "research_report": "TIRTIRの日本上陸情報はPR TIMESで公式発表済み。韓国SNSでの高い注目度と日本ECサイトでの検索増加が兆しとして確認された。"
    }


def _make_bad_article():
    """品質チェックで複数問題が検出される記事データ"""
    return {
        "title": "テスト",
        "meta_description": "短い",
        "body": "**これは強調です**。■記号付き。短い本文。!!!大興奮!!!",
        "x_post_1": "テスト投稿",
        "x_post_2": "テスト2",
        "artist_tags": [],
        "tags": [],
        "highlights": [],
        "research_report": "",
    }


# ==========================================
# テスト1: auto_fix テスト
# ==========================================

class TestAutoFix:
    """auto_fix_article のテスト"""

    def test_removes_bold_markdown(self):
        """**強調** が除去されること"""
        article = {"body": "これは**太字テスト**です。"}
        fixed = auto_fix_article(article)
        assert "**" not in fixed["body"]
        assert "太字テスト" in fixed["body"]

    def test_removes_italic_markdown(self):
        """*斜体* が除去されること（クレジット行は除外）"""
        article = {"body": "これは*斜体テスト*です。\n*写真＝公式Instagramより*"}
        fixed = auto_fix_article(article)
        assert "*斜体テスト*" not in fixed["body"]
        assert "斜体テスト" in fixed["body"]
        # クレジット行は保護される
        assert "*写真＝公式Instagramより*" in fixed["body"]

    def test_removes_decorative_symbols(self):
        """■●▶▷◆◇ が除去されること"""
        article = {"body": "■項目1\n●項目2\n▶項目3\n◆項目4"}
        fixed = auto_fix_article(article)
        assert "■" not in fixed["body"]
        assert "●" not in fixed["body"]
        assert "▶" not in fixed["body"]
        assert "◆" not in fixed["body"]
        assert "項目1" in fixed["body"]  # テキストは残る

    def test_reduces_excessive_exclamation(self):
        """過剰な「!」が削減されること"""
        article = {"body": "すごい!!! 最高!! もっとすごい! さらに! そして!"}
        fixed = auto_fix_article(article)
        # 連続!は1つに、全体で3回目以降は「。」に
        excl_count = fixed["body"].count("!")
        assert excl_count <= 2

    def test_preserves_non_forbidden_content(self):
        """禁止パターン以外のコンテンツは変更されないこと"""
        article = {"body": "通常のテキスト。見出しもそのまま。## 見出し\n\n本文です。"}
        fixed = auto_fix_article(article)
        assert "通常のテキスト" in fixed["body"]
        assert "## 見出し" in fixed["body"]

    def test_returns_copy(self):
        """元のarticle_jsonが変更されないこと"""
        article = {"body": "**強調**テスト", "title": "test"}
        original_body = article["body"]
        fixed = auto_fix_article(article)
        assert article["body"] == original_body  # 元は変更されない
        assert "**" not in fixed["body"]


# ==========================================
# テスト2: quality_check テスト
# ==========================================

class TestQualityCheck:
    """quality_check のテスト"""

    def test_good_article_passes(self):
        """正常な記事がauto_publishと判定されること"""
        article = _make_good_article()
        result = quality_check(article)
        assert result["score"] >= 70
        assert result["publish_action"] in ["auto_publish", "review_needed"]

    def test_short_article_detected(self):
        """短い本文がSHORT_ARTICLE として検出されること"""
        article = _make_good_article()
        article["body"] = "短い本文。"
        result = quality_check(article)
        assert any(i["type"] == "SHORT_ARTICLE" for i in result["issues"])

    def test_empty_fields_detected(self):
        """空フィールドがEMPTY_FIELDとして検出されること"""
        article = _make_bad_article()
        result = quality_check(article)
        empty_fields = [i for i in result["issues"] if i["type"] == "EMPTY_FIELD"]
        assert len(empty_fields) > 0

    def test_insufficient_hashtags_detected(self):
        """ハッシュタグ不足がINSUFFICIENT_HASHTAGSとして検出されること"""
        article = _make_good_article()
        article["x_post_1"] = "ハッシュタグなし投稿"
        result = quality_check(article)
        assert any(i["type"] == "INSUFFICIENT_HASHTAGS" for i in result["issues"])

    def test_forbidden_pattern_detected(self):
        """禁止パターンがFORBIDDEN_PATTERNとして検出されること"""
        article = _make_good_article()
        article["body"] = article["body"] + "\n\n**強調テスト** ■記号テスト"
        result = quality_check(article)
        assert any(i["type"] == "FORBIDDEN_PATTERN" for i in result["issues"])

    def test_score_calculation(self):
        """スコアが0-100の範囲内であること"""
        article = _make_bad_article()
        result = quality_check(article)
        assert 0 <= result["score"] <= 100

    def test_publish_action_logic(self):
        """publish_actionのロジックが正しいこと"""
        # スコア90以上 → auto_publish
        result_high = {"score": 95}
        if result_high["score"] >= 90:
            assert "auto_publish" == "auto_publish"

        # スコア70-89 → review_needed
        result_mid = {"score": 75}
        if 70 <= result_mid["score"] < 90:
            assert "review_needed" == "review_needed"

        # スコア70未満 → reject
        result_low = {"score": 50}
        if result_low["score"] < 70:
            assert "reject" == "reject"

    def test_bad_article_rejected(self):
        """品質の低い記事がrejectと判定されること"""
        article = _make_bad_article()
        result = quality_check(article)
        assert result["publish_action"] == "reject"

    def test_source_date_verification(self):
        """ソースにない日付がUNVERIFIED_DATEとして検出されること"""
        article = _make_good_article()
        article["body"] += "\n2030年12月25日のイベント"
        source_articles = [{"original_text": "2026年2月の情報です。"}]
        result = quality_check(article, source_articles=source_articles)
        assert any(i["type"] == "UNVERIFIED_DATE" for i in result["issues"])

    def test_grounding_low_confidence(self):
        """低信頼度セグメントがLOW_GROUNDING_CONFIDENCEとして検出されること"""
        article = _make_good_article()
        grounding_metadata = {
            "has_grounding": True,
            "source_urls": [],
            "low_confidence_segments": [
                {"text": "この情報は不確実です", "confidence": 0.3}
            ],
            "raw_metadata": {}
        }
        result = quality_check(article, grounding_metadata=grounding_metadata)
        assert any(i["type"] == "LOW_GROUNDING_CONFIDENCE" for i in result["issues"])


# ==========================================
# テスト3: スキーマテスト
# ==========================================

class TestArticleSchema:
    """ARTICLE_SCHEMA の構造テスト"""

    def test_schema_has_required_fields(self):
        """必須フィールドがすべて定義されていること"""
        required = ARTICLE_SCHEMA["required"]
        assert "title" in required
        assert "meta_description" in required
        assert "body" in required
        assert "x_post_1" in required
        assert "x_post_2" in required
        assert "artist_tags" in required
        assert "tags" in required
        assert "highlights" in required
        assert "research_report" in required

    def test_schema_properties_defined(self):
        """全プロパティの型が定義されていること"""
        props = ARTICLE_SCHEMA["properties"]
        for key in ARTICLE_SCHEMA["required"]:
            assert key in props, f"Missing property: {key}"
            assert "type" in props[key], f"Missing type for: {key}"

    def test_array_fields_have_items(self):
        """配列フィールドにitemsが定義されていること"""
        props = ARTICLE_SCHEMA["properties"]
        for field in ["artist_tags", "tags", "highlights"]:
            assert props[field]["type"] == "ARRAY"
            assert "items" in props[field]

    def test_rewrite_schema_exists(self):
        """REWRITE_SCHEMA が正しく定義されていること"""
        assert REWRITE_SCHEMA["type"] == "OBJECT"
        assert "title" in REWRITE_SCHEMA["required"]
        assert "body" in REWRITE_SCHEMA["required"]


# ==========================================
# テスト4: system_instruction テスト
# ==========================================

class TestSystemInstruction:
    """system_instruction の読み込みテスト"""

    def test_system_instruction_loads(self):
        """system_instruction.txtが正常に読み込めること"""
        from src.content_prompts import get_system_instruction
        instruction = get_system_instruction()
        assert len(instruction) > 100
        assert "K-Trend Times" in instruction

    def test_system_instruction_contains_key_sections(self):
        """system_instructionに必須セクションが含まれていること"""
        from src.content_prompts import get_system_instruction
        instruction = get_system_instruction()
        assert "ペルソナ" in instruction
        assert "文体ルール" in instruction
        assert "最重要ルール" in instruction
        assert "記事構成の型" in instruction

    def test_build_article_prompt_with_sources(self):
        """ソース記事ありでプロンプトが正しく構築されること"""
        from src.content_prompts import build_article_prompt
        source_articles = [{
            "title": "テスト記事",
            "source_url": "https://example.com/test",
            "original_text": "テスト本文テキスト",
            "published_date": "2026-02-23",
        }]
        prompt = build_article_prompt("テストタイトル", "概要", "trend",
                                       source_articles=source_articles)
        assert "Source 1" in prompt
        assert "https://example.com/test" in prompt
        assert "テスト本文テキスト" in prompt

    def test_build_article_prompt_without_sources(self):
        """ソース記事なしでもプロンプトが構築されること"""
        from src.content_prompts import build_article_prompt
        prompt = build_article_prompt("タイトル", "概要", "trend", link="https://example.com")
        assert "タイトル" in prompt
        assert "概要" in prompt


# ==========================================
# テスト5: grounding_parser テスト
# ==========================================

class TestGroundingParser:
    """grounding_parser のテスト"""

    def test_parse_empty_response(self):
        """空の応答でもエラーにならないこと"""
        result = parse_grounding_metadata({})
        assert result["has_grounding"] is False
        assert result["source_urls"] == []

    def test_parse_with_grounding_chunks(self):
        """groundingChunksからURLが正しく抽出されること"""
        api_response = {
            "candidates": [{
                "groundingMetadata": {
                    "groundingChunks": [
                        {"web": {"title": "Test Article", "uri": "https://example.com/article1"}},
                        {"web": {"title": "Test Article 2", "uri": "https://example.com/article2"}},
                    ]
                }
            }]
        }
        result = parse_grounding_metadata(api_response)
        assert result["has_grounding"] is True
        assert len(result["source_urls"]) == 2
        assert result["source_urls"][0]["url"] == "https://example.com/article1"

    def test_parse_low_confidence(self):
        """低信頼度セグメントが正しく抽出されること"""
        api_response = {
            "candidates": [{
                "groundingMetadata": {
                    "groundingSupports": [
                        {
                            "confidenceScores": [0.3, 0.5],
                            "segment": {"text": "低信頼度テキスト"}
                        },
                        {
                            "confidenceScores": [0.9, 0.95],
                            "segment": {"text": "高信頼度テキスト"}
                        }
                    ]
                }
            }]
        }
        result = parse_grounding_metadata(api_response)
        assert len(result["low_confidence_segments"]) == 1
        assert result["low_confidence_segments"][0]["text"] == "低信頼度テキスト"

    def test_get_verified_urls(self):
        """get_verified_urlsが正しくURLリストを返すこと"""
        grounding_result = {
            "source_urls": [
                {"title": "A", "url": "https://a.com"},
                {"title": "B", "url": "https://b.com"},
                {"title": "C", "url": ""},
            ]
        }
        urls = get_verified_urls(grounding_result)
        assert len(urls) == 2
        assert "https://a.com" in urls
        assert "https://b.com" in urls


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
