#!/usr/bin/env python3
"""
K-TREND TIMES スクレイピングスクリプト
STUDIO → WordPress 移行用データ抽出

対応形式: Nuxt3 __NUXT_DATA__ JSON配列形式

使用方法:
    python scraper.py

出力:
    - articles.json: 全記事データ (JSON)
    - wordpress_import.xml: WordPress用WXRファイル
    - images/: ダウンロードした画像
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time
from datetime import datetime
from urllib.parse import urlparse
import html

# 設定
SITEMAP_URL = "https://k-trendtimes.com/sitemap-dynamic/sitemap-dynamic-notes-s--c-slug.xml"
OUTPUT_DIR = "output"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
DELAY_BETWEEN_REQUESTS = 0.3  # サーバー負荷軽減用

# カテゴリマッピング (STUDIO → WordPress)
CATEGORY_MAP = {
    "news": "ニュース",
    "trend": "トレンド",
    "koreantrip": "韓国旅行",
    "gourmet": "グルメ",
    "beauty": "ビューティー",
    "fashion": "ファッション",
    "interview": "インタビュー",
    "column": "コラム",
    "artist": "アーティスト",
    "event": "イベント",
}


def setup_directories():
    """出力ディレクトリを作成"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    print(f"✓ ディレクトリ作成完了: {OUTPUT_DIR}")


def get_article_urls():
    """サイトマップから全記事URLを取得"""
    print(f"サイトマップを取得中: {SITEMAP_URL}")
    response = requests.get(SITEMAP_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]

    print(f"✓ {len(urls)} 件の記事URLを取得")
    return urls


def parse_nuxt_data(html_content):
    """
    Nuxt3の__NUXT_DATA__形式をパース

    構造: [["Reactive",1], {data:2,...}, {slug:4, body:40,...}, ...]
    数値はペイロード配列のインデックスを参照
    """
    match = re.search(
        r'<script[^>]*id="__NUXT_DATA__"[^>]*>(\[[\s\S]*?\])</script>',
        html_content
    )

    if not match:
        return None

    try:
        payload = json.loads(match.group(1))
        return payload
    except json.JSONDecodeError:
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


def scrape_article(url):
    """単一記事をスクレイピング"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        article = {
            'url': url,
            'slug': url.split('/')[-1],
            'title': '',
            'body': '',
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
                article['body'] = nuxt_data['body']

            if nuxt_data.get('cover') and not article['cover_image']:
                article['cover_image'] = nuxt_data['cover']

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

        # 公開日をslugから推測（より正確な日付）
        slug = article['slug']
        date_match = re.search(r'(\d{2})(\d{2})(\d{2})$', slug)
        if date_match:
            yy, mm, dd = date_match.groups()
            year = 2000 + int(yy)
            article['published_at'] = f"{year}-{mm}-{dd}T00:00:00Z"

        return article

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None  # 404は静かにスキップ
        raise
    except Exception as e:
        print(f" エラー: {e}")
        return None


def download_image(image_url, slug):
    """画像をダウンロード"""
    try:
        if not image_url:
            return None

        # ファイル名を生成
        parsed = urlparse(image_url)
        ext = os.path.splitext(parsed.path)[1] or '.jpg'
        filename = f"{slug}{ext}"
        filepath = os.path.join(IMAGES_DIR, filename)

        # 既にダウンロード済みならスキップ
        if os.path.exists(filepath):
            return filename

        response = requests.get(image_url, timeout=30)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(response.content)

        return filename

    except Exception:
        return None


def generate_wxr(articles, output_path):
    """WordPress WXRファイルを生成"""

    wxr_header = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/">
<channel>
    <title>K-TREND TIMES</title>
    <link>https://k-trendtimes.com</link>
    <description>K-POPと韓国トレンドの最新情報</description>
    <pubDate>{pub_date}</pubDate>
    <language>ja</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <wp:base_site_url>https://k-trendtimes.com</wp:base_site_url>
    <wp:base_blog_url>https://k-trendtimes.com</wp:base_blog_url>
'''

    wxr_footer = '''
</channel>
</rss>'''

    item_template = '''
    <item>
        <title><![CDATA[{title}]]></title>
        <link>{url}</link>
        <pubDate>{pub_date}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">{url}</guid>
        <description></description>
        <content:encoded><![CDATA[{content}]]></content:encoded>
        <excerpt:encoded><![CDATA[{excerpt}]]></excerpt:encoded>
        <wp:post_id>{post_id}</wp:post_id>
        <wp:post_date>{post_date}</wp:post_date>
        <wp:post_date_gmt>{post_date_gmt}</wp:post_date_gmt>
        <wp:post_modified>{post_date}</wp:post_modified>
        <wp:post_modified_gmt>{post_date_gmt}</wp:post_modified_gmt>
        <wp:comment_status>open</wp:comment_status>
        <wp:ping_status>open</wp:ping_status>
        <wp:post_name>{slug}</wp:post_name>
        <wp:status>publish</wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type>post</wp:post_type>
        <wp:post_password></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        <category domain="category" nicename="{category_slug}"><![CDATA[{category_name}]]></category>
    </item>'''

    pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(wxr_header.format(pub_date=pub_date))

        for idx, article in enumerate(articles, 1):
            if not article:
                continue

            # 日付処理
            try:
                if article.get('published_at'):
                    dt = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
                else:
                    dt = datetime.now()
                post_date = dt.strftime("%Y-%m-%d %H:%M:%S")
                post_date_gmt = dt.strftime("%Y-%m-%d %H:%M:%S")
                rss_date = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
            except:
                post_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                post_date_gmt = post_date
                rss_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

            # カテゴリ
            cat_slug = article.get('category', 'news').lower()
            cat_name = CATEGORY_MAP.get(cat_slug, article.get('category', 'ニュース'))

            # 本文
            body = article.get('body', '')
            # アイキャッチ画像を本文の先頭に追加
            if article.get('cover_image'):
                alt_text = html.escape(article.get('title', ''))
                body = f'<img src="{article["cover_image"]}" alt="{alt_text}" class="wp-post-image" />\n{body}'

            item = item_template.format(
                title=html.escape(article.get('title', 'Untitled')),
                url=article.get('url', ''),
                pub_date=rss_date,
                content=body,
                excerpt=html.escape(article.get('meta_description', '')),
                post_id=idx,
                post_date=post_date,
                post_date_gmt=post_date_gmt,
                slug=article.get('slug', f'post-{idx}'),
                category_slug=cat_slug,
                category_name=cat_name,
            )
            f.write(item)

        f.write(wxr_footer)

    print(f"✓ WXRファイル生成完了: {output_path}")


def main():
    """メイン処理"""
    print("=" * 60)
    print("K-TREND TIMES スクレイピング")
    print("STUDIO → WordPress 移行ツール")
    print("=" * 60)

    # 準備
    setup_directories()

    # 記事URL取得
    urls = get_article_urls()

    # 記事スクレイピング
    print(f"\n記事データを取得中...")
    articles = []
    failed = []
    skipped = 0

    for i, url in enumerate(urls, 1):
        slug = url.split('/')[-1]
        print(f"\r  [{i}/{len(urls)}] {slug[:30]:<30}", end="", flush=True)

        article = scrape_article(url)
        if article:
            if article.get('body'):
                articles.append(article)
            else:
                skipped += 1
        else:
            failed.append(url)

        # サーバー負荷軽減
        time.sleep(DELAY_BETWEEN_REQUESTS)

    print()  # 改行
    print(f"\n✓ スクレイピング完了")
    print(f"  成功: {len(articles)} 件")
    print(f"  スキップ (本文なし): {skipped} 件")
    print(f"  失敗 (404等): {len(failed)} 件")

    if failed:
        failed_path = os.path.join(OUTPUT_DIR, "failed_urls.txt")
        with open(failed_path, 'w') as f:
            f.write('\n'.join(failed))
        print(f"  失敗リスト: {failed_path}")

    # JSONとして保存
    json_path = os.path.join(OUTPUT_DIR, "articles.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"\n✓ JSON保存完了: {json_path}")

    # WXRファイル生成
    wxr_path = os.path.join(OUTPUT_DIR, "wordpress_import.xml")
    generate_wxr(articles, wxr_path)

    # 画像ダウンロード
    print(f"\n画像をダウンロード中...")
    downloaded = 0
    for i, article in enumerate(articles, 1):
        if article.get('cover_image'):
            print(f"\r  [{i}/{len(articles)}]", end="", flush=True)
            result = download_image(article['cover_image'], article['slug'])
            if result:
                downloaded += 1
    print()
    print(f"✓ 画像ダウンロード完了: {downloaded} 件")

    # 完了レポート
    print("\n" + "=" * 60)
    print("処理完了!")
    print("=" * 60)
    print(f"  記事数: {len(articles)}")
    print(f"  画像数: {downloaded}")
    print(f"  出力先: {OUTPUT_DIR}/")
    print(f"    - articles.json (全記事データ)")
    print(f"    - wordpress_import.xml (WPインポート用)")
    print(f"    - images/ (アイキャッチ画像)")
    print("=" * 60)


if __name__ == "__main__":
    main()
