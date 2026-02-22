#!/usr/bin/env python3
"""
K-TREND TIMES スクレイピング テストスクリプト
5件だけ取得してデータ構造を確認
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import os

# テスト用URL（最新5件）
TEST_URLS = [
    "https://k-trendtimes.com/notes/news260201",
    "https://k-trendtimes.com/notes/trend260201",
    "https://k-trendtimes.com/notes/koreantrip260201",
    "https://k-trendtimes.com/notes/event251231",
    "https://k-trendtimes.com/notes/beauty251224",
]

OUTPUT_DIR = "test_output"


def extract_article(url):
    """記事データを抽出"""
    print(f"\n取得中: {url}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        article = {
            'url': url,
            'slug': url.split('/')[-1],
            'title': '',
            'body_preview': '',
            'cover_image': '',
            'published_at': '',
            'category': '',
            'meta_description': '',
        }

        # タイトル
        og_title = soup.find('meta', property='og:title')
        if og_title:
            article['title'] = og_title.get('content', '')
        elif soup.title:
            article['title'] = soup.title.string.split('|')[0].strip() if soup.title.string else ''

        # アイキャッチ画像
        og_image = soup.find('meta', property='og:image')
        if og_image:
            article['cover_image'] = og_image.get('content', '')

        # Meta Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            article['meta_description'] = meta_desc.get('content', '')

        # 本文 (プレビュー: 最初の500文字)
        # まずrichTextクラスを探す
        body_elem = soup.find(class_='richText')
        if not body_elem:
            # 代替: 記事本文らしき要素を探す
            body_elem = soup.find('article') or soup.find('main')

        if body_elem:
            # HTMLタグを除去してテキストのみ
            text = body_elem.get_text(separator=' ', strip=True)
            article['body_preview'] = text[:500] + '...' if len(text) > 500 else text
            article['body_html_length'] = len(str(body_elem))

        # __NUXT__データから日付・カテゴリを抽出
        nuxt_match = re.search(r'window\.__NUXT__\s*=\s*(\{.+?\});\s*</script>', html, re.DOTALL)
        if nuxt_match:
            try:
                # 簡易的なパース（完全なJSONではない場合がある）
                nuxt_str = nuxt_match.group(1)

                # publishedAt を探す
                pub_match = re.search(r'"publishedAt"\s*:\s*"([^"]+)"', nuxt_str)
                if pub_match:
                    article['published_at'] = pub_match.group(1)

                # category を探す
                cat_match = re.search(r'"category"\s*:\s*"([^"]+)"', nuxt_str)
                if cat_match:
                    article['category'] = cat_match.group(1)

            except Exception as e:
                print(f"  Nuxtパースエラー: {e}")

        # 公開日がない場合、slugから推測
        if not article['published_at']:
            slug = article['slug']
            date_match = re.search(r'(\d{2})(\d{2})(\d{2})$', slug)
            if date_match:
                yy, mm, dd = date_match.groups()
                year = 2000 + int(yy)
                article['published_at'] = f"{year}-{mm}-{dd}"

        # カテゴリがない場合、slugから推測
        if not article['category']:
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
    print("K-TREND TIMES スクレイピング テスト")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    articles = []
    for url in TEST_URLS:
        article = extract_article(url)
        if article:
            articles.append(article)
            print(f"  ✓ タイトル: {article['title'][:50]}...")
            print(f"    カテゴリ: {article['category']}")
            print(f"    公開日: {article['published_at']}")
            print(f"    画像: {'あり' if article['cover_image'] else 'なし'}")

    # 結果を保存
    output_path = os.path.join(OUTPUT_DIR, "test_articles.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"テスト完了: {len(articles)}/{len(TEST_URLS)} 件成功")
    print(f"結果: {output_path}")
    print("=" * 60)

    # サンプル出力
    if articles:
        print("\n【サンプル記事データ】")
        sample = articles[0]
        for key, value in sample.items():
            if key == 'body_preview':
                print(f"  {key}: {value[:100]}...")
            elif key == 'cover_image' and value:
                print(f"  {key}: {value[:60]}...")
            else:
                print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
