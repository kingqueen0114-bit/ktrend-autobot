"""src/content_prompts.py のユニットテスト"""
import pytest


class TestBuildArticlePrompt:
    """build_article_prompt関数のテスト"""

    def test_returns_string(self):
        """戻り値が文字列であること"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="BTS 新アルバム",
            snippet="BTSが新アルバムをリリース",
            category="artist",
        )
        assert isinstance(result, str)

    def test_contains_title(self):
        """プロンプトにタイトルが含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="テストタイトル123",
            snippet="テスト概要",
            category="artist",
        )
        assert "テストタイトル123" in result

    def test_contains_snippet(self):
        """プロンプトに概要が含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="これはテスト概要文です",
            category="artist",
        )
        assert "これはテスト概要文です" in result

    def test_contains_category(self):
        """プロンプトにカテゴリが含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="beauty",
        )
        assert "beauty" in result

    def test_contains_link_when_provided(self):
        """リンクが指定された場合、プロンプトに含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
            link="https://example.com/article",
        )
        assert "https://example.com/article" in result

    def test_contains_trend_sign_context(self):
        """トレンドサイン情報が指定された場合、プロンプトに含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
            trend_sign_context="SNSでの急上昇が確認された",
        )
        assert "SNSでの急上昇が確認された" in result

    def test_default_link_is_empty(self):
        """linkのデフォルト値は空文字列"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        # 参照元: の後に空文字列が来る（エラーにならないこと）
        assert "参照元:" in result

    def test_default_trend_sign_context_is_empty(self):
        """trend_sign_contextのデフォルト値は空文字列"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        # エラーにならないことを確認
        assert isinstance(result, str)

    def test_contains_editor_role(self):
        """プロンプトに編集者ペルソナが含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "K-Trend Times" in result
        assert "専属編集者" in result

    def test_contains_basic_rules(self):
        """プロンプトに基本原則が含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "基本原則" in result

    def test_contains_input_type_rules(self):
        """プロンプトに入力タイプ別ルールが含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "入力タイプ別ルール" in result

    def test_contains_brand_rules(self):
        """プロンプトにブランドルールが含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "ブランド・コンテンツ別ルール" in result

    def test_contains_x_post_rules(self):
        """プロンプトにX投稿ルールが含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "X（旧Twitter）投稿ルール" in result

    def test_contains_output_format(self):
        """プロンプトにJSON出力形式の指示が含まれる"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "出力形式（JSON）" in result
        assert "title" in result
        assert "body" in result
        assert "x_post_1" in result

    def test_prompt_is_non_trivial_length(self):
        """プロンプトが十分な長さを持つこと"""
        from src.content_prompts import build_article_prompt

        result = build_article_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        # ペルソナ + ルール + フォーマットで相当な長さになるはず
        assert len(result) > 500


class TestBuildSnsPrompt:
    """build_sns_prompt関数のテスト"""

    def test_returns_string(self):
        """戻り値が文字列であること"""
        from src.content_prompts import build_sns_prompt

        result = build_sns_prompt(
            title="テストタイトル",
            snippet="テスト概要",
            category="artist",
        )
        assert isinstance(result, str)

    def test_contains_title(self):
        """プロンプトにタイトルが含まれる"""
        from src.content_prompts import build_sns_prompt

        result = build_sns_prompt(
            title="NewJeans 日本公演決定",
            snippet="概要",
            category="artist",
        )
        assert "NewJeans 日本公演決定" in result

    def test_contains_snippet(self):
        """プロンプトに内容が含まれる"""
        from src.content_prompts import build_sns_prompt

        result = build_sns_prompt(
            title="タイトル",
            snippet="SNS投稿用のテスト概要テキスト",
            category="artist",
        )
        assert "SNS投稿用のテスト概要テキスト" in result

    def test_contains_category(self):
        """プロンプトにカテゴリが含まれる"""
        from src.content_prompts import build_sns_prompt

        result = build_sns_prompt(
            title="タイトル",
            snippet="概要",
            category="fashion",
        )
        assert "fashion" in result

    def test_contains_sns_writer_persona(self):
        """プロンプトにSNSライターのペルソナが含まれる"""
        from src.content_prompts import build_sns_prompt

        result = build_sns_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "SNSライター" in result

    def test_contains_sns_output_format(self):
        """プロンプトにSNS用出力フォーマットが含まれる"""
        from src.content_prompts import build_sns_prompt

        result = build_sns_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "news_post" in result
        assert "luna_post_a" in result
        assert "luna_post_b" in result

    def test_mentions_three_types(self):
        """3種類のSNS投稿を作成する指示が含まれる"""
        from src.content_prompts import build_sns_prompt

        result = build_sns_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert "3種類" in result

    def test_prompt_is_non_trivial_length(self):
        """プロンプトが十分な長さを持つこと"""
        from src.content_prompts import build_sns_prompt

        result = build_sns_prompt(
            title="タイトル",
            snippet="概要",
            category="artist",
        )
        assert len(result) > 100


class TestPromptConstants:
    """プロンプト定数のテスト"""

    def test_editor_role_defined(self):
        """EDITOR_ROLEが定義されていること"""
        from src.content_prompts import EDITOR_ROLE

        assert isinstance(EDITOR_ROLE, str)
        assert len(EDITOR_ROLE) > 0

    def test_basic_rules_defined(self):
        """BASIC_RULESが定義されていること"""
        from src.content_prompts import BASIC_RULES

        assert isinstance(BASIC_RULES, str)
        assert "基本原則" in BASIC_RULES

    def test_input_type_rules_defined(self):
        """INPUT_TYPE_RULESが定義されていること"""
        from src.content_prompts import INPUT_TYPE_RULES

        assert isinstance(INPUT_TYPE_RULES, str)

    def test_brand_rules_defined(self):
        """BRAND_RULESが定義されていること"""
        from src.content_prompts import BRAND_RULES

        assert isinstance(BRAND_RULES, str)

    def test_x_post_rules_defined(self):
        """X_POST_RULESが定義されていること"""
        from src.content_prompts import X_POST_RULES

        assert isinstance(X_POST_RULES, str)

    def test_output_format_article_is_valid_json_template(self):
        """OUTPUT_FORMAT_ARTICLEが必要なJSONキーを含むこと"""
        from src.content_prompts import OUTPUT_FORMAT_ARTICLE

        assert "title" in OUTPUT_FORMAT_ARTICLE
        assert "meta_description" in OUTPUT_FORMAT_ARTICLE
        assert "body" in OUTPUT_FORMAT_ARTICLE
        assert "x_post_1" in OUTPUT_FORMAT_ARTICLE
        assert "x_post_2" in OUTPUT_FORMAT_ARTICLE
        assert "artist_tags" in OUTPUT_FORMAT_ARTICLE
        assert "tags" in OUTPUT_FORMAT_ARTICLE
        assert "highlights" in OUTPUT_FORMAT_ARTICLE
        assert "research_report" in OUTPUT_FORMAT_ARTICLE

    def test_output_format_sns_is_valid_json_template(self):
        """OUTPUT_FORMAT_SNSが必要なJSONキーを含むこと"""
        from src.content_prompts import OUTPUT_FORMAT_SNS

        assert "news_post" in OUTPUT_FORMAT_SNS
        assert "luna_post_a" in OUTPUT_FORMAT_SNS
        assert "luna_post_b" in OUTPUT_FORMAT_SNS

    def test_basic_rules_prohibit_markdown_asterisks(self):
        """基本ルールにマークダウン記号禁止が含まれていること"""
        from src.content_prompts import BASIC_RULES

        assert "アスタリスク" in BASIC_RULES or "**" in BASIC_RULES

    def test_basic_rules_require_1000_chars(self):
        """基本ルールに1000文字以上の要件が含まれていること"""
        from src.content_prompts import BASIC_RULES

        assert "1000文字" in BASIC_RULES

    def test_editor_role_contains_ktrendtimes(self):
        """編集者ペルソナにK-Trend Timesが含まれること"""
        from src.content_prompts import EDITOR_ROLE

        assert "K-Trend Times" in EDITOR_ROLE
