"""PR TIMESからK-POP/韓国関連プレスリリースを取得"""

import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from src.category_config import CATEGORIES


PRTIMES_BASE_URL = "https://prtimes.jp"
PRTIMES_KPOP_URL = f"{PRTIMES_BASE_URL}/topics/keywords/K-POP"

HEADERS = {
    "User-Agent": "K-TREND-TIMES-Bot/1.0",
}

REQUEST_INTERVAL = 5  # 秒。PR TIMESへのリクエスト間隔


def fetch_prtimes_articles(max_articles: int = 20) -> List[Dict]:
    """
    PR TIMESのK-POPキーワードページからプレスリリースを取得。

    Returns:
        list of dict: [{title, url, date, lead, company, full_text}, ...]
    """
    articles = []

    try:
        resp = requests.get(PRTIMES_KPOP_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # PR TIMESの記事リストをパース
        # 複数のセレクタパターンに対応（構造変更対応）
        article_elements = (
            soup.select("article.list-article__item")
            or soup.select(".list-article li")
            or soup.select("[data-testid='article-list'] article")
            or soup.select(".article-list-item")
        )

        for elem in article_elements[:max_articles]:
            try:
                title_tag = (
                    elem.select_one("h2")
                    or elem.select_one(".list-article__title")
                    or elem.select_one("a[href] .title")
                )
                link_tag = elem.select_one("a[href]")
                company_tag = (
                    elem.select_one(".list-article__company")
                    or elem.select_one(".company-name")
                    or elem.select_one(".company")
                )
                date_tag = (
                    elem.select_one("time")
                    or elem.select_one(".list-article__date")
                    or elem.select_one(".date")
                )
                lead_tag = (
                    elem.select_one(".list-article__summary")
                    or elem.select_one(".list-article__lead")
                    or elem.select_one(".summary")
                )

                if not link_tag:
                    continue

                title = title_tag.get_text(strip=True) if title_tag else ""
                if not title:
                    title = link_tag.get_text(strip=True)
                if not title:
                    continue

                url = link_tag.get("href", "")
                if url.startswith("/"):
                    url = PRTIMES_BASE_URL + url

                article = {
                    "title": title,
                    "url": url,
                    "date": date_tag.get_text(strip=True) if date_tag else "",
                    "lead": lead_tag.get_text(strip=True) if lead_tag else "",
                    "company": company_tag.get_text(strip=True) if company_tag else "",
                    "full_text": "",
                }
                articles.append(article)

            except Exception as e:
                print(f"[prtimes] Error parsing article element: {e}")
                continue

    except Exception as e:
        print(f"[prtimes] Error fetching PRTIMES page: {e}")

    return articles


def fetch_article_detail(url: str) -> dict:
    """
    個別記事ページから本文と画像を取得。
    リクエスト間隔を5秒以上空ける。

    Returns:
        {"full_text": str, "images": [url, ...]}
    """
    time.sleep(REQUEST_INTERVAL)

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # 複数のセレクタパターンに対応
        body_elem = (
            soup.select_one("#pressrelease-body")
            or soup.select_one(".rich-text")
            or soup.select_one(".article-body")
            or soup.select_one("[data-testid='press-release-body']")
        )

        full_text = ""
        images = []

        if body_elem:
            # 画像URLを抽出（本文内の <img> タグ）
            for img_tag in body_elem.select("img[src]"):
                img_src = img_tag.get("src", "")
                if img_src and not img_src.startswith("data:"):
                    # 相対URLを絶対URLに変換
                    if img_src.startswith("//"):
                        img_src = "https:" + img_src
                    elif img_src.startswith("/"):
                        img_src = PRTIMES_BASE_URL + img_src
                    # 小さいアイコンやロゴを除外（最小200px幅）
                    width = img_tag.get("width", "")
                    if width and width.isdigit() and int(width) < 100:
                        continue
                    images.append(img_src)

            # OGP画像もフォールバックとして取得
            if not images:
                og_image = soup.select_one('meta[property="og:image"]')
                if og_image and og_image.get("content"):
                    images.append(og_image["content"])

            # 不要なタグを除去
            for tag in body_elem.select("script, style, iframe"):
                tag.decompose()
            full_text = body_elem.get_text("\n", strip=True)[:5000]

        return {"full_text": full_text, "images": images[:5]}  # 最大5枚

    except Exception as e:
        print(f"[prtimes] Error fetching detail: {url} - {e}")
        return {"full_text": "", "images": []}


def classify_article_category(title: str, lead: str) -> str:
    """
    PR TIMES記事をカテゴリに振り分ける。
    タイトルとリード文のキーワードマッチで判定。

    優先順位: event > cosme > travel > gourmet > fashion > kpop（デフォルト）
    """
    text = (title + " " + lead).upper()

    # イベント（最優先）— 固有ワードが必要
    event_specific = [
        "来日公演", "ライブ", "コンサート", "チケット",
        "ファンミーティング", "ファンミ", "開催", "ツアー",
        "アリーナ", "ドーム",
    ]
    if any(kw.upper() in text for kw in event_specific):
        return "event"

    # コスメ
    cosme_specific = [
        "コスメ", "スキンケア", "メイク", "リップ", "アイシャドウ",
        "ファンデ", "美容液", "ROM&ND", "CLIO", "INNISFREE",
        "ETUDE", "オリーブヤング", "QOO10",
    ]
    if any(kw in text for kw in cosme_specific):
        return "cosme"

    # 旅行
    travel_specific = [
        "旅行", "渡韓", "観光", "聖地巡礼",
        "ソウル", "釜山", "明洞", "弘大", "江南", "仁川空港",
    ]
    if any(kw.upper() in text for kw in travel_specific):
        return "travel"

    # グルメ
    gourmet_specific = [
        "韓国料理", "グルメ", "フード", "カフェ", "チキン",
        "トッポギ", "サムギョプサル", "新大久保",
    ]
    if any(kw.upper() in text for kw in gourmet_specific):
        return "gourmet"

    # ファッション
    fashion_specific = [
        "ファッション", "アパレル", "ブランド", "コレクション",
        "GENTLE MONSTER", "NERDY", "MLB",
    ]
    if any(kw.upper() in text for kw in fashion_specific):
        return "fashion"

    # デフォルト: K-pop
    return "kpop"


def select_articles_for_today(
    articles: List[Dict],
    existing_urls: set = None,
    max_per_category: Dict[str, int] = None,
) -> Dict[str, List[Dict]]:
    """
    取得した記事から、カテゴリごとに本日分を選定。

    Args:
        articles: fetch_prtimes_articles の結果
        existing_urls: 既に処理済みのURLセット（重複排除用）
        max_per_category: カテゴリ別上限

    Returns:
        {category_id: [article, ...], ...}
    """
    if max_per_category is None:
        max_per_category = {cat_id: cat.daily_target for cat_id, cat in CATEGORIES.items()}

    if existing_urls is None:
        existing_urls = set()

    categorized = {cat_id: [] for cat_id in CATEGORIES}

    for article in articles:
        if article["url"] in existing_urls:
            continue

        category = classify_article_category(article["title"], article["lead"])

        if len(categorized[category]) < max_per_category.get(category, 0):
            categorized[category].append(article)

    return categorized


def run_prtimes_fetch(existing_urls: set = None) -> Dict[str, List[Dict]]:
    """
    メインの実行関数。

    1. PR TIMESからK-POP関連記事を取得
    2. カテゴリに振り分け
    3. 各記事の本文を取得
    4. カテゴリ別にリストを返す
    """
    print("[prtimes] Starting PR TIMES fetch...")

    # Step 1: 一覧取得
    articles = fetch_prtimes_articles(max_articles=20)
    print(f"[prtimes] Fetched {len(articles)} articles from PR TIMES")

    if not articles:
        print("[prtimes] No articles found")
        return {}

    # Step 2: カテゴリ振り分け + 選定
    selected = select_articles_for_today(articles, existing_urls=existing_urls)

    # Step 3: 選定された記事の本文と画像を取得
    for category_id, cat_articles in selected.items():
        for article in cat_articles:
            if not article["full_text"]:
                detail = fetch_article_detail(article["url"])
                article["full_text"] = detail["full_text"]
                article["images"] = detail["images"]
                img_count = len(detail['images'])
                print(f"[prtimes] Fetched detail for: {article['title'][:30]}... ({len(detail['full_text'])}字, {img_count}画像)")

    # 結果サマリー
    for cat_id, cat_articles in selected.items():
        if cat_articles:
            print(f"[prtimes] {cat_id}: {len(cat_articles)} articles selected")

    return selected
