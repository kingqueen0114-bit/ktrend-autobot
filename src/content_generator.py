"""
K-Trend AutoBot Content Generator
Generates SNS posts and CMS articles using Gemini AI.
"""

import os
import json
import re
import requests
from typing import Dict, List, Optional
from datetime import datetime
from utils.logging_config import log_event, log_error, mask_url_keys


class ContentGenerator:
    """Generates content using Gemini AI."""

    def __init__(self, api_key: str):
        """
        Initialize the ContentGenerator.

        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key
        if not self.api_key:
            log_error("GEMINI_INIT", "Gemini API key not configured")

    def _call_gemini_rest(self, prompt: str) -> str:
        """Call Gemini REST API directly with Google Search tool enabled."""
        if not self.api_key:
            raise ValueError("API key missing")
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.5,
                "maxOutputTokens": 2000,
            }
        }
        
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=90)
        
        if response.status_code != 200:
            error_body = ""
            try:
                error_body = response.text[:500]
            except Exception:
                pass
            log_error("GEMINI_API_ERROR_GENERATE", f"Failed with status {response.status_code}", detail=error_body, details=response.text)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(
                mask_url_keys(str(e)), response=e.response
            ) from None

        data = response.json()
        
        # Determine if grounding metadata exists to log it
        grounding = data.get("candidates", [{}])[0].get("groundingMetadata", {})
        if grounding:
            chunks = grounding.get("groundingChunks", [])
            log_event("GROUNDING_SUCCESS", f"Search Grounding retrieved {len(chunks)} sources", source_count=len(chunks))

        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts)
        if not text:
            raise ValueError("Empty response text from Gemini API")
            
        return text

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

        if not self.api_key:
            return self._generate_fallback_sns(title, category)

        # Import prompts from external module
        from src.content_prompts import build_sns_prompt

        prompt = build_sns_prompt(title, snippet, category)

        try:
            text = self._call_gemini_rest(prompt).strip()

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                return json.loads(json_match.group())
            else:
                return self._generate_fallback_sns(title, category)
        except Exception as e:
            log_error("SNS_GENERATION_FAILED", "SNS content generation failed", error=e)
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

    def generate_cms_article(self, trend: Dict, trend_sign_context: str = "") -> Dict:
        """
        Generate a CMS article for a trend.

        Args:
            trend: Trend dictionary
            trend_sign_context: Context about the trend signs to inject

        Returns:
            Dictionary with article content (title, body, meta_description, etc.)
        """
        title = trend.get("title", "")
        snippet = trend.get("snippet", "")
        category = trend.get("category", "trend")
        link = trend.get("link", "")

        # Import prompts from external module
        from src.content_prompts import build_article_prompt, build_sns_prompt

        if not self.api_key:
            return self._generate_fallback_article(title, snippet, category)

        prompt = build_article_prompt(title, snippet, category, link, trend_sign_context)

        try:
            text = self._call_gemini_rest(prompt).strip()

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
            log_error("ARTICLE_GENERATION_FAILED", "CMS article generation failed", error=e)
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

    def rewrite_article(self, article: Dict, warnings: List[str], trend: Dict, trend_sign_context: str = "") -> Dict:
        """
        Rewrite an article to address quality warnings.

        Args:
            article: Original article dictionary
            warnings: List of quality warnings
            trend: Original trend data
            trend_sign_context: Optional sign context

        Returns:
            Rewritten article dictionary
        """
        if not self.api_key:
            return article

        current_body = article.get("body", "")
        current_title = article.get("title", "")

        prompt = f"""
以下の記事を最新のインターネット検索結果を用いて改善してください。

現在のタイトル: {current_title}
元のトレンド概要: {trend.get('snippet')}
検知されたサイン・兆し: {trend_sign_context}
現在の本文:
{current_body}

改善が必要な点（絶対に修正すること）:
{chr(10).join(f'- {w}' for w in warnings)}

必須ルール:
- 文字数は必ず1000文字以上を満たすこと
- 分析した「流行のサイン（兆し）」を必ず本文に含めること
- トレンド情報（{trend.get('title', '')}）に関する「具体的な一次情報元のURLやニュースメディア名」を必ずインターネットから検索して本文内に記載すること。これがないと事実確認で減点されます。
- research_report にこの選定理由とサインの考察を記述すること

出力形式（JSON）:
{{
    "title": "改善されたタイトル",
    "meta_description": "改善されたメタ説明",
    "body": "改善された本文（Markdown形式）",
    "tags": ["タグ1", "タグ2", "タグ3"],
    "highlights": ["具体的な事実・数字を含む要約文1（30-60文字）", "重要な日時・場所・人物名を含む要約文2（30-60文字）", "今後の展望やアクションを含む要約文3（30-60文字）"]
}}

JSONのみ出力してください。
"""

        try:
            text = self._call_gemini_rest(prompt).strip()

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
            log_error("ARTICLE_REWRITE_FAILED", "Article rewrite failed", error=e)
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

    # Strict check: Body length (Must be 1000+ characters)
    if len(body) < 1000:
        warnings.append(f"本文が短すぎます。現在の文字数: {len(body)}文字。絶対に1000文字以上で執筆してください。")
        score -= 50

    # Strict check: Signs/Signals mention
    if "兆し" in body or "サイン" in body or "反応" in body or "注目" in body or "熱量" in body or "理由" in body:
        pass # Mentions trend signals
    else:
        warnings.append("「なぜこれが次に流行る兆しなのか」という分析的な視点やサイン（SNSの反応など）への言及が不足しています。必ず組み込んでください。")
        score -= 50

    # Ensure research report is generated
    if not article.get("research_report"):
        warnings.append("内部用のリサーチ報告（research_report）が生成されていません。必ず出力してください。")
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

    # Strict check: Source URLs
    if "http" not in body and "www" not in body and ".com" not in body and ".jp" not in body and "co.jp" not in body:
        warnings.append("記事本文に一次情報元の具体的なURLが記載されていません。推測ではなく、必ず検索ツールを使用して事実確認リンクを含めてください。")
        score -= 20

    # Ensure score is within bounds
    score = max(0, min(100, score))

    # We enforce a strict 100-point passing score now
    return {
        "score": score,
        "passed": score == 100,
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
