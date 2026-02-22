#!/usr/bin/env python3
"""
K-TREND TIMES スクレイピング テストスクリプト v2
__NUXT__データから本文を直接抽出
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import os
import html

# テスト用URL
TEST_URLS = [
    "https://k-trendtimes.com/notes/news260201",
    "https://k-trendtimes.com/notes/trend260201",
    "https://k-trendtimes.com/notes/event251231",
    "https://k-trendtimes.com/notes/beauty251224",
]

OUTPUT_DIR = "test_output"


def extract_nuxt_data(html_content):
    """__NUXT__データを抽出してパース"""

    # パターン1: window.__NUXT__ = (function(...){...})()
    # STUDIOは関数形式でデータを埋め込むことがある

    # パターン2: window.__NUXT__={...}
    patterns = [
        # 単純なJSON形式
        r'window\.__NUXT__\s*=\s*(\{[\s\S]+?\});?\s*(?:</script>|$)',
        # 関数形式（Nuxt3）
        r'window\.__NUXT__\s*=\s*\(function[^{]*\{return\s*(\{[\s\S]+?\})\}\)',
    ]

    for pattern in patterns:
        match = re.search(pattern, html_content)
        if match:
            try:
                json_str = match.group(1)
                # JSONとしてパース試行
                return json.loads(json_str)
            except json.JSONDecodeError:
                continue

    return None


def extract_body_from_html(html_content):
    """HTMLから本文部分を正規表現で抽出"""

    # body フィールドを探す（JSON内のHTMLコンテンツ）
    # "body":"<p>本文...</p>"
    body_patterns = [
        r'"body"\s*:\s*"((?:[^"\\]|\\.)*)"\s*[,}]',
        r'"content"\s*:\s*"((?:[^"\\]|\\.)*)"\s*[,}]',
    ]

    for pattern in body_patterns:
        match = re.search(pattern, html_content)
        if match:
            body = match.group(1)
            # エスケープを解除
            body = body.encode().decode('unicode_escape')
            # HTMLエンティティをデコード
            body = html.unescape(body)
            return body

    return None


def extract_article(url):
    """記事データを抽出（改良版）"""
    print(f"\n取得中: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        article = {
            'url': url,
            'slug': url.split('/')[-1],
            'title': '',
            'body_html': '',
            'body_text': '',
            'cover_image': '',
            'published_at': '',
            'category': '',
            'meta_description': '',
        }

        # === メタデータ取得 ===

        # タイトル
        og_title = soup.find('meta', property='og:title')
        if og_title:
            article['title'] = og_title.get('content', '').strip()

        # アイキャッチ画像
        og_image = soup.find('meta', property='og:image')
        if og_image:
            article['cover_image'] = og_image.get('content', '')

        # Meta Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            article['meta_description'] = meta_desc.get('content', '').strip()

        # === 本文取得（__NUXT__データから） ===

        body_html = extract_body_from_html(html_content)
        if body_html:
            article['body_html'] = body_html
            # HTMLタグを除去してテキスト化
            body_soup = BeautifulSoup(body_html, 'html.parser')
            article['body_text'] = body_soup.get_text(separator='\n', strip=True)

        # === 日付・カテゴリ取得 ===

        # publishedAt を探す
        pub_match = re.search(r'"publishedAt"\s*:\s*"([^"]+)"', html_content)
        if pub_match:
            article['published_at'] = pub_match.group(1)

        # 公開日がない場合、slugから推測
        if not article['published_at']:
            slug = article['slug']
            date_match = re.search(r'(\d{2})(\d{2})(\d{2})$', slug)
            if date_match:
                yy, mm, dd = date_match.groups()
                year = 2000 + int(yy)
                article['published_at'] = f"{year}-{mm}-{dd}T00:00:00Z"

        # カテゴリをslugから推測
        slug = article['slug'].lower()
        categories = ['news', 'trend', 'koreantrip', 'gourmet', 'beauty',
                     'fashion', 'interview', 'column', 'artist', 'event']
        for cat in categories:
            if slug.startswith(cat):
                article['category'] = cat
                break

        return article

    except Exception as e:
        print(f"  エラー: {e}")
        return None


def main():
    print("=" * 60)
    print("K-TREND TIMES スクレイピング テスト v2")
    print("（__NUXT__データから本文抽出）")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    articles = []
    for url in TEST_URLS:
        article = extract_article(url)
        if article:
            articles.append(article)
            print(f"  ✓ タイトル: {article['title'][:40]}...")
            print(f"    カテゴリ: {article['category']}")
            print(f"    公開日: {article['published_at'][:10] if article['published_at'] else 'なし'}")
            print(f"    画像: {'あり' if article['cover_image'] else 'なし'}")
            body_len = len(article['body_html'])
            print(f"    本文: {body_len} 文字 {'✓' if body_len > 100 else '✗ 少ない'}")

    # 結果を保存
    output_path = os.path.join(OUTPUT_DIR, "test_articles_v2.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"テスト完了: {len(articles)}/{len(TEST_URLS)} 件成功")
    print(f"結果: {output_path}")
    print("=" * 60)

    # サンプル本文を表示
    if articles and articles[0].get('body_text'):
        print("\n【サンプル本文（最初の500文字）】")
        print("-" * 40)
        print(articles[0]['body_text'][:500])
        print("-" * 40)

    # HTML構造を表示
    if articles and articles[0].get('body_html'):
        print("\n【本文HTML構造（最初の300文字）】")
        print("-" * 40)
        print(articles[0]['body_html'][:300])
        print("-" * 40)


if __name__ == "__main__":
    main()
