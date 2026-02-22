#!/usr/bin/env python3
"""
K-TREND TIMES スクレイピング テストスクリプト v3
Nuxt3の__NUXT_DATA__ JSON配列形式に対応
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


def parse_nuxt_data(html_content):
    """
    Nuxt3の__NUXT_DATA__形式をパース

    構造: [["Reactive",1], {data:2,...}, {slug:4, body:40,...}, ...]
    数値はペイロード配列のインデックスを参照
    """

    # __NUXT_DATA__ スクリプトタグを探す
    match = re.search(
        r'<script[^>]*id="__NUXT_DATA__"[^>]*>(\[[\s\S]*?\])</script>',
        html_content
    )

    if not match:
        return None

    try:
        payload = json.loads(match.group(1))
        return payload
    except json.JSONDecodeError as e:
        print(f"  JSON解析エラー: {e}")
        return None


def resolve_value(payload, index_or_value):
    """
    ペイロードから値を解決

    - 数値ならペイロード配列のインデックス参照
    - それ以外はそのまま返す
    """
    if isinstance(index_or_value, int) and 0 <= index_or_value < len(payload):
        resolved = payload[index_or_value]

        # Date型の処理 ["Date", "2024-10-11T09:24:43.000Z"]
        if isinstance(resolved, list) and len(resolved) == 2 and resolved[0] == "Date":
            return resolved[1]

        # 再帰的に解決（ネストした参照がある場合）
        if isinstance(resolved, int):
            return resolve_value(payload, resolved)

        return resolved

    return index_or_value


def extract_article_data(payload):
    """ペイロードから記事データを抽出"""

    article = {
        'slug': '',
        'title': '',
        'body': '',
        'cover': '',
        'published_at': '',
        'category': '',
    }

    # ペイロード構造を探索
    # 通常 payload[3] に記事データオブジェクトがある
    for item in payload:
        if isinstance(item, dict):
            # dynamicData キーを探す
            for key, value in item.items():
                if key.startswith('dynamicData'):
                    # 記事データへの参照インデックス
                    article_ref = resolve_value(payload, value)
                    if isinstance(article_ref, dict):
                        # 記事データを解決
                        if 'slug' in article_ref:
                            article['slug'] = resolve_value(payload, article_ref['slug'])
                        if 'title' in article_ref:
                            article['title'] = resolve_value(payload, article_ref['title'])
                        if 'body' in article_ref:
                            article['body'] = resolve_value(payload, article_ref['body'])
                        if 'cover' in article_ref:
                            article['cover'] = resolve_value(payload, article_ref['cover'])

                        # カテゴリを探す（ネストした構造）
                        for k, v in article_ref.items():
                            resolved = resolve_value(payload, v)
                            if isinstance(resolved, dict):
                                if 'slug' in resolved and resolved.get('slug') in ['news', 'trend', 'beauty', 'fashion', 'event', 'gourmet', 'interview', 'column', 'artist', 'koreantrip']:
                                    article['category'] = resolved.get('slug', '')
                                # publishedAt を探す
                                if '_meta' in resolved:
                                    meta = resolve_value(payload, resolved['_meta'])
                                    if isinstance(meta, dict) and 'publishedAt' in meta:
                                        article['published_at'] = resolve_value(payload, meta['publishedAt'])

    return article


def extract_article(url):
    """記事データを抽出"""
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

        # === OGPメタデータ取得（バックアップ用） ===

        og_title = soup.find('meta', property='og:title')
        if og_title:
            article['title'] = og_title.get('content', '').strip()

        og_image = soup.find('meta', property='og:image')
        if og_image:
            article['cover_image'] = og_image.get('content', '')

        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            article['meta_description'] = meta_desc.get('content', '').strip()

        # === __NUXT_DATA__から本文を取得 ===

        payload = parse_nuxt_data(html_content)
        if payload:
            nuxt_data = extract_article_data(payload)

            if nuxt_data.get('body'):
                article['body_html'] = nuxt_data['body']
                # HTMLからテキスト抽出
                body_soup = BeautifulSoup(nuxt_data['body'], 'html.parser')
                article['body_text'] = body_soup.get_text(separator='\n', strip=True)

            if nuxt_data.get('cover') and not article['cover_image']:
                article['cover_image'] = nuxt_data['cover']

            if nuxt_data.get('published_at'):
                article['published_at'] = nuxt_data['published_at']

            if nuxt_data.get('category'):
                article['category'] = nuxt_data['category']

        # === フォールバック: slugからカテゴリ・日付を推測 ===

        if not article['category']:
            slug = article['slug'].lower()
            categories = ['news', 'trend', 'koreantrip', 'gourmet', 'beauty',
                         'fashion', 'interview', 'column', 'artist', 'event']
            for cat in categories:
                if slug.startswith(cat):
                    article['category'] = cat
                    break

        if not article['published_at']:
            slug = article['slug']
            date_match = re.search(r'(\d{2})(\d{2})(\d{2})$', slug)
            if date_match:
                yy, mm, dd = date_match.groups()
                year = 2000 + int(yy)
                article['published_at'] = f"{year}-{mm}-{dd}T00:00:00Z"

        return article

    except Exception as e:
        print(f"  エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    print("=" * 60)
    print("K-TREND TIMES スクレイピング テスト v3")
    print("（Nuxt3 __NUXT_DATA__ 配列形式対応）")
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
    output_path = os.path.join(OUTPUT_DIR, "test_articles_v3.json")
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


if __name__ == "__main__":
    main()
