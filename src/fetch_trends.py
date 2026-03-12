"""
K-Trend AutoBot Trend Fetcher
Fetches Korean trends using Google Custom Search API and Gemini AI.
"""

import os
import requests
import json
import random
import re
from typing import List, Dict, Optional
from datetime import datetime
from utils.logging_config import log_event, log_error, mask_url_keys

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class TrendFetcher:
    """Fetches trending Korean topics using Google Search and Gemini AI."""

    # KPOP related search queries
    KPOP_QUERIES = [
        "K-POP 最新 site:prtimes.jp",
        "韓国アイドル ニュース site:prtimes.jp",
        "BTS 最新情報",
        "BLACKPINK ニュース",
        "NewJeans 新曲 話題",
        "IVE 最新情報",
        "aespa トレンド",
        "Stray Kids ニュース",
        "TWICE 最新",
        "LE SSERAFIM 話題",
    ]

    # General Korean trend queries
    TREND_QUERIES = [
        "韓国 現地 トレンド 最新",
        "韓国で今流行っているもの 2026",
        "韓国コスメ 日本未上陸 人気",
        "韓国ファッション 最新 トレンド",
        "韓国グルメ 流行り",
        "韓国旅行 おすすめ 穴場",
        "韓国カフェ 最新 人気",
        "韓国スキンケア おすすめ",
        "韓国コスメ site:prtimes.jp",
        "韓国ファッション site:prtimes.jp",
        "韓国グルメ site:prtimes.jp",
    ]

    # Fallback images from Unsplash
    FALLBACK_IMAGES = [
        "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=600&fit=crop",  # Concert
        "https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=800&h=600&fit=crop",  # Seoul
        "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&h=600&fit=crop",  # Cosmetics
        "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?w=800&h=600&fit=crop",  # Food
        "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop",  # Fashion
    ]

    def __init__(self, api_key: str):
        """
        Initialize the TrendFetcher.

        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key
        self.search_api_key = os.environ.get("GOOGLE_CUSTOM_SEARCH_API_KEY")
        self.search_engine_id = os.environ.get("GOOGLE_CSE_ID")

    def _search_google(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search Google using Custom Search API.
        Falls back to Gemini if API Key is missing or quota is exceeded.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results
        """
        if not self.search_api_key or not self.search_engine_id:
            log_event("GOOGLE_SEARCH_BYPASS", "Google Search API keys missing, using Gemini fallback")
            return self._search_with_gemini(query)

        try:
            url = f"https://www.googleapis.com/customsearch/v1?key={self.search_api_key}&cx={self.search_engine_id}&q={query}&num={num_results}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 429: # Quota Exceeded
                log_event("GOOGLE_SEARCH_QUOTA", "Google Search API quota exceeded, using Gemini fallback")
                return self._search_with_gemini(query)
                
            response.raise_for_status()
            data = response.json()
            
            items = data.get("items", [])
            log_event("GOOGLE_SEARCH_SUCCESS", f"Found {len(items)} results for {query}")
            return items
            
        except Exception as e:
            log_error("GOOGLE_SEARCH_ERROR", "Google Search API failed, using Gemini fallback", error=e)
            return self._search_with_gemini(query)

    def _search_with_gemini(self, query: str) -> List[Dict]:
        """Fallback search using Gemini REST API with Google Search grounding."""
        if not self.api_key:
            log_error("GEMINI_API_KEY_MISSING", "Gemini API key not available for fallback search")
            return []

        try:
            prompt = f"""「{query}」に関する最新のトレンド情報を3つ、ウェブ検索結果に基づいて提供してください。
以下の条件を厳守：
1. SNSでの反応やコラボなど「流行のサイン（兆し）」を含めること。
2. 推測ではなく、検索で見つかった事実に基づくこと。

以下のJSON配列形式で回答（JSONのみ、他のテキスト不要）：
[
  {{
    "title": "トレンドのタイトル（魅力的で具体的なもの）",
    "snippet": "なぜ話題なのか、流行のサインを含めた150文字程度の解説。"
  }}
]"""

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "tools": [{"google_search": {}}],
                "generationConfig": {
                    "temperature": 0.7
                }
            }

            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=60)

            if response.status_code != 200:
                error_body = ""
                try:
                    error_body = response.text[:500]
                except Exception:
                    pass
                log_error("GEMINI_API_ERROR", f"Gemini API returned status {response.status_code}", detail=error_body)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise requests.exceptions.HTTPError(
                    mask_url_keys(str(e)), response=e.response
                ) from None

            data = response.json()
            candidate = data.get("candidates", [{}])[0]
            parts = candidate.get("content", {}).get("parts", [])
            text = "".join(part.get("text", "") for part in parts)

            # Extract grounding URLs from metadata
            grounding_metadata = candidate.get("groundingMetadata", {})
            grounding_chunks = grounding_metadata.get("groundingChunks", [])
            grounding_urls = []
            for chunk in grounding_chunks:
                web = chunk.get("web", {})
                if web.get("uri"):
                    grounding_urls.append(web["uri"])

            text = text.strip()

            # Clean markdown code blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            # Extract JSON from response robustly using regex
            json_match = re.search(r'\[[\s\S]*\]', text)
            if json_match:
                json_str = json_match.group()
                results = json.loads(json_str)
            else:
                raise ValueError(f"No JSON array found in response: {text[:100]}...")

            # Assign real grounding URLs to each result
            from urllib.parse import quote
            for i, result in enumerate(results):
                if i < len(grounding_urls):
                    result["link"] = grounding_urls[i]
                elif not result.get("link"):
                    result["link"] = f"https://www.google.com/search?q={quote(query)}"

            log_event("GEMINI_FALLBACK_SUCCESS", f"Gemini fallback generated trends",
                      count=len(results), grounding_urls=len(grounding_urls))
            return results
        except Exception as e:
            error_msg = f"Gemini fallback REST API failed: {type(e).__name__}: {mask_url_keys(str(e))}"
            if 'response' in locals() and hasattr(response, 'text'):
                error_msg += f"\nResponse body:\n{response.text[:1000]}"
            log_error("GEMINI_FALLBACK_FAILED", error_msg, error=e)
            raise RuntimeError(error_msg)

    def _extract_image(self, search_result: Dict) -> Optional[str]:
        """
        Extract image URL from search result.

        Args:
            search_result: Google search result item

        Returns:
            Image URL or None
        """
        # Try pagemap images
        pagemap = search_result.get("pagemap", {})

        # Try cse_image
        cse_images = pagemap.get("cse_image", [])
        if cse_images and cse_images[0].get("src"):
            return cse_images[0]["src"]

        # Try metatags og:image
        metatags = pagemap.get("metatags", [])
        if metatags:
            og_image = metatags[0].get("og:image")
            if og_image:
                return og_image

        # Try cse_thumbnail
        thumbnails = pagemap.get("cse_thumbnail", [])
        if thumbnails and thumbnails[0].get("src"):
            return thumbnails[0]["src"]

        return None

    def _categorize_trend(self, title: str, snippet: str) -> str:
        """
        Categorize a trend based on title and snippet.

        Args:
            title: Trend title
            snippet: Trend snippet

        Returns:
            Category string
        """
        text = (title + " " + snippet).lower()

        if any(word in text for word in ["bts", "blackpink", "twice", "k-pop", "kpop", "アイドル", "アーティスト"]):
            return "artist"
        elif any(word in text for word in ["コスメ", "スキンケア", "メイク", "美容"]):
            return "beauty"
        elif any(word in text for word in ["ファッション", "服", "コーデ", "スタイル"]):
            return "fashion"
        elif any(word in text for word in ["グルメ", "料理", "カフェ", "レストラン", "食べ物"]):
            return "food"
        elif any(word in text for word in ["旅行", "観光", "ソウル", "韓国旅"]):
            return "travel"
        elif any(word in text for word in ["ドラマ", "映画", "netflix", "放送"]):
            return "drama"
        elif any(word in text for word in ["イベント", "コンサート", "ライブ", "フェス"]):
            return "event"
        else:
            return "trend"

    def fetch_trends(self, include_kpop: bool = True, limit: int = 10, topic: str = None) -> List[Dict]:
        """
        Fetch trending Korean topics.

        Args:
            include_kpop: Whether to include KPOP-specific queries
            limit: Maximum number of trends to return
            topic: Specific topic to search for (overrides random selection)

        Returns:
            List of trend dictionaries
        """
        log_event("FETCH_TRENDS_START", "Fetching Korean trends", include_kpop=include_kpop, topic=topic)

        # Select queries
        if topic:
            # If topic is provided, use it as the specific query
            queries = [topic]
        else:
            # Otherwise use random selection
            queries = self.TREND_QUERIES.copy()
            if include_kpop:
                queries.extend(random.sample(self.KPOP_QUERIES, min(3, len(self.KPOP_QUERIES))))
            
            # Shuffle and limit queries
            random.shuffle(queries)
            queries = queries[:5]  # Limit API calls

        trends = []
        seen_titles = set()

        for query in queries:
            results = self._search_google(query)

            for result in results:
                title = result.get("title", "").strip()
                snippet = result.get("snippet", "").strip()
                link = result.get("link", "")

                # Skip duplicates
                if title in seen_titles:
                    continue
                seen_titles.add(title)

                # Extract image
                image_url = self._extract_image(result)
                image_source = "Google Search"

                # Use fallback if no image
                if not image_url:
                    image_url = random.choice(self.FALLBACK_IMAGES)
                    image_source = "Unsplash Fallback"

                # Categorize
                category = self._categorize_trend(title, snippet)

                trend = {
                    "title": title,
                    "snippet": snippet,
                    "link": link,
                    "image_url": image_url,
                    "image_source": image_source,
                    "category": category,
                    "query": query,
                    "fetched_at": datetime.utcnow().isoformat(),
                    "additional_images": [],
                }

                trends.append(trend)

                if len(trends) >= limit:
                    break

            if len(trends) >= limit:
                break

        log_event("FETCH_TRENDS_COMPLETE", "Trend fetching completed", count=len(trends))
        return trends


if __name__ == "__main__":
    # Test
    from dotenv import load_dotenv
    load_dotenv()

    fetcher = TrendFetcher(os.getenv("GEMINI_API_KEY"))
    trends = fetcher.fetch_trends(include_kpop=True, limit=3)

    for i, trend in enumerate(trends, 1):
        print(f"\n{i}. {trend['title']}")
        print(f"   Category: {trend['category']}")
        print(f"   Image: {trend['image_url'][:50]}...")
