"""
K-Trend AutoBot Trend Fetcher
Fetches Korean trends using Google Custom Search API and Gemini AI.
"""

import os
import requests
import json
import random
from typing import List, Dict, Optional
from datetime import datetime

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

        if genai and api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None

    def _search_google(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search Google using Custom Search API.
        Disabled due to expired API Key; forcing use of Gemini fallback.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results
        """
        print(f"⚠️ Google Search API bypassing, forcing Gemini fallback...")
        return self._search_with_gemini(query)

    def _search_with_gemini(self, query: str) -> List[Dict]:
        """Fallback search using Gemini when Google Custom Search fails."""
        if not self.model:
            print("⚠️ Gemini model not available for fallback search")
            return []

        try:
            import json
            prompt = f"""あなたは韓国トレンド情報の専門家です。「{query}」に関する最新のトレンド情報を3つ提供してください。
以下の条件を厳守してください：
1. ただの事実ではなく、「韓国で今リアルに流行っていること」「これから日本でも流行りそうなこと」「日本人が知ると面白いと感じるポイント」を含めること。
2. K-POPアイドルの情報の場合は、PR TIMES等の公式プレスリリースやInstagramでの発言など、具体的なソースや一次情報を意識した内容にすること。
3. 推測ではなく、事実に基づいた最新情報を出力すること。

以下のJSON配列形式で回答してください（JSONのみ、他のテキスト不要）：
[
  {{
    "title": "トレンドのタイトル（魅力的で具体的なもの）",
    "link": "参考になるURL（公式ニュース、PR TIMES、Instagramリンクなど。架空のものでも形式が合っていれば可）",
    "snippet": "トレンドの具体的な内容。なぜ話題なのか、日本での流行予測などを含めた150文字程度の解説。"
  }}
]
- linkはダミーURLで構いません"""

            # Use Google Search Retrieval tool to get the latest news
            tool = {"google_search_retrieval": {}} if hasattr(genai, "protos") else "google_search_retrieval"
            response = self.model.generate_content(prompt, tools=tool)
            text = response.text.strip()

            # Extract JSON from response
            if '```' in text:
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
                text = text.strip()

            results = json.loads(text)
            print(f"✅ Gemini fallback: {len(results)} trends generated")
            return results
        except Exception as e:
            print(f"⚠️ Gemini fallback also failed: {e}")
            return []

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
        print(f"🔍 Fetching Korean trends (include_kpop={include_kpop}, topic={topic})")

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

        print(f"✅ Fetched {len(trends)} trends")
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
