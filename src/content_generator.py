"""
K-Trend AutoBot Content Generator
Generates SNS posts and CMS articles using Gemini AI.
"""

import os
import json
import re
from typing import Dict, List, Optional
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class ContentGenerator:
    """Generates content using Gemini AI."""

    def __init__(self, api_key: str):
        """
        Initialize the ContentGenerator.

        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key

        if genai and api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
            print("⚠️ Gemini API not configured")

    def generate_content(self, trend: Dict) -> Dict:
        """
        Generate SNS content for a trend.

        Args:
            trend: Trend dictionary with title, snippet, category, etc.

        Returns:
            Dictionary with SNS content (news_post, luna_post_a, luna_post_b)
        """
        title = trend.get("title", "")
        snippet = trend.get("snippet", "")
        category = trend.get("category", "trend")

        if not self.model:
            return self._generate_fallback_sns(title, category)

        # Import prompts from external module
        from src.content_prompts import build_sns_prompt

        if not self.model:
            return self._generate_fallback_sns(title, category)

        prompt = build_sns_prompt(title, snippet, category)

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._generate_fallback_sns(title, category)
        except Exception as e:
            print(f"⚠️ SNS generation failed: {e}")
            return self._generate_fallback_sns(title, category)

    def _generate_fallback_sns(self, title: str, category: str) -> Dict:
        """Generate fallback SNS content."""
        emojis = {
            "artist": "🎤✨",
            "beauty": "💄✨",
            "fashion": "👗✨",
            "food": "🍜😋",
            "travel": "✈️🇰🇷",
            "drama": "📺🎬",
            "event": "🎉🎊",
            "trend": "🔥📢",
        }

        emoji = emojis.get(category, "📢✨")

        return {
            "news_post": f"{emoji} 【速報】{title}\n\n詳細は記事をチェック！\n\n#韓国 #トレンド #ktrend",
            "luna_post_a": f"{emoji} みんな〜！{title}って知ってる？気になる〜！\n\n#韓国好き #韓国情報",
            "luna_post_b": f"{emoji} これ絶対チェックして！{title}\n\nマジで話題になってる🔥\n\n#韓国トレンド",
        }

    def generate_cms_article(self, trend: Dict) -> Dict:
        """
        Generate a CMS article for a trend.

        Args:
            trend: Trend dictionary

        Returns:
            Dictionary with article content (title, body, meta_description, etc.)
        """
        title = trend.get("title", "")
        snippet = trend.get("snippet", "")
        category = trend.get("category", "trend")
        link = trend.get("link", "")

        # Import prompts from external module
        from src.content_prompts import build_article_prompt, build_sns_prompt

        if not self.model:
            return self._generate_fallback_article(title, snippet, category)

        prompt = build_article_prompt(title, snippet, category, link)

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                article = json.loads(json_match.group())
                article["category"] = category
                article["source_link"] = link
                return article
            else:
                return self._generate_fallback_article(title, snippet, category)
        except Exception as e:
            print(f"⚠️ Article generation failed: {e}")
            return self._generate_fallback_article(title, snippet, category)

    def _generate_fallback_article(self, title: str, snippet: str, category: str) -> Dict:
        """Generate fallback article content."""
        return {
            "title": title,
            "meta_description": snippet[:160] if len(snippet) > 160 else snippet,
            "body": f"""## {title}

{snippet}

### 詳細情報

この話題について、最新情報をお届けします。

韓国では今、この話題が大きな注目を集めています。

### まとめ

今後も最新情報をチェックしていきましょう！
""",
            "tags": ["韓国", "トレンド", category],
            "highlights": [
                "韓国で話題のトレンド情報",
                "最新ニュースをお届け",
                "詳細は記事をチェック",
            ],
            "category": category,
        }

    def rewrite_article(self, article: Dict, warnings: List[str], trend: Dict) -> Dict:
        """
        Rewrite an article to address quality warnings.

        Args:
            article: Original article dictionary
            warnings: List of quality warnings
            trend: Original trend data

        Returns:
            Rewritten article dictionary
        """
        if not self.model:
            return article

        current_body = article.get("body", "")
        current_title = article.get("title", "")

        prompt = f"""
以下の記事を改善してください。

現在のタイトル: {current_title}
現在の本文:
{current_body}

改善が必要な点:
{chr(10).join(f'- {w}' for w in warnings)}

出力形式（JSON）:
{{
    "title": "改善されたタイトル",
    "meta_description": "改善されたメタ説明",
    "body": "改善された本文（Markdown形式）",
    "tags": ["タグ1", "タグ2", "タグ3"],
    "highlights": ["ポイント1", "ポイント2", "ポイント3"]
}}

JSONのみ出力してください。
"""

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()

            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                rewritten = json.loads(json_match.group())
                # Preserve original metadata
                rewritten["category"] = article.get("category", trend.get("category", "trend"))
                rewritten["source_link"] = article.get("source_link", trend.get("link", ""))
                return rewritten
            else:
                return article
        except Exception as e:
            print(f"⚠️ Rewrite failed: {e}")
            return article


def check_article_quality(article: Dict, trend: Dict) -> Dict:
    """
    Check the quality of an article.

    Args:
        article: Article dictionary
        trend: Original trend data

    Returns:
        Dictionary with score, passed, warnings, and was_rewritten
    """
    warnings = []
    score = 100

    title = article.get("title", "")
    body = article.get("body", "")
    meta_description = article.get("meta_description", "")

    # Check title length
    if len(title) < 20:
        warnings.append("タイトルが短すぎます（20文字以上推奨）")
        score -= 15
    elif len(title) > 80:
        warnings.append("タイトルが長すぎます（80文字以下推奨）")
        score -= 10

    # Check body length
    if len(body) < 800:
        warnings.append("本文が短すぎます（最低800文字、1000文字以上必須）")
        score -= 40
    elif len(body) < 1000:
        warnings.append("本文が短めです（1000文字以上でより充実した内容にしてください）")
        score -= 20

    # Check meta description
    if len(meta_description) < 50:
        warnings.append("メタ説明が短すぎます（50文字以上推奨）")
        score -= 10
    elif len(meta_description) > 200:
        warnings.append("メタ説明が長すぎます（200文字以下推奨）")
        score -= 5

    # Check for headings
    if "##" not in body:
        warnings.append("見出しがありません（##を使用してください）")
        score -= 15

    # Check for highlights
    highlights = article.get("highlights", [])
    if len(highlights) < 2:
        warnings.append("ハイライトが少ないです（2つ以上推奨）")
        score -= 10

    # Check for tags
    tags = article.get("tags", [])
    if len(tags) < 2:
        warnings.append("タグが少ないです（2つ以上推奨）")
        score -= 5

    # Ensure score is within bounds
    score = max(0, min(100, score))

    return {
        "score": score,
        "passed": score >= 60,
        "warnings": warnings,
        "was_rewritten": False,
    }


if __name__ == "__main__":
    # Test
    from dotenv import load_dotenv
    load_dotenv()

    generator = ContentGenerator(os.getenv("GEMINI_API_KEY"))

    test_trend = {
        "title": "NewJeansの新曲が話題に",
        "snippet": "K-POPグループNewJeansの最新曲がチャートを席巻中",
        "category": "artist",
        "link": "https://example.com/news",
    }

    # Test SNS content
    sns = generator.generate_content(test_trend)
    print("SNS Content:")
    print(json.dumps(sns, ensure_ascii=False, indent=2))

    # Test CMS article
    article = generator.generate_cms_article(test_trend)
    print("\nCMS Article:")
    print(json.dumps(article, ensure_ascii=False, indent=2))

    # Test quality check
    quality = check_article_quality(article, test_trend)
    print("\nQuality Check:")
    print(json.dumps(quality, ensure_ascii=False, indent=2))
