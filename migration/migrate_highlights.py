#!/usr/bin/env python3
"""WordPress CHECKPOINT highlights -> Sanity highlights 移行スクリプト

WordPress記事の <div class="ktrend-checkpoint"> 内の <li> 要素を抽出し、
対応するSanityドキュメントの highlights 配列にセットする。

Usage:
    python migrate_highlights.py            # 実行
    python migrate_highlights.py --dry-run  # プレビューのみ
"""

import argparse
import html
import logging
import os
import re
import sys
import time

import requests

# プロジェクトルートをパスに追加して src モジュールをインポート可能にする
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import sanity_client  # noqa: E402

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
WP_API_URL = "https://k-trendtimes.com/wp-json/wp/v2/posts"
WP_PER_PAGE = 50
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
SANITY_BATCH_SIZE = 50

# CHECKPOINT HTML パターン
# <div class="ktrend-checkpoint"> ... <ul> ... <li>...</li> ... </ul> ... </div>
CHECKPOINT_PATTERN = re.compile(
    r'<div\s+class="ktrend-checkpoint"[^>]*>.*?<ul>(.*?)</ul>',
    re.DOTALL | re.IGNORECASE,
)
LI_PATTERN = re.compile(r"<li>(.*?)</li>", re.DOTALL | re.IGNORECASE)
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")


# ---------------------------------------------------------------------------
# WordPress API
# ---------------------------------------------------------------------------
def _wp_auth() -> tuple:
    """WordPress Basic Auth credentials を返す"""
    username = os.environ.get("WORDPRESS_USER", "admin")
    password = os.environ.get("WORDPRESS_APP_PASSWORD", "")
    if not password:
        raise ValueError(
            "WORDPRESS_APP_PASSWORD 環境変数が設定されていません。"
            "実行前に export WORDPRESS_APP_PASSWORD=xxx を設定してください。"
        )
    return (username, password)


def fetch_all_wp_posts() -> list:
    """WordPress REST API から全記事をページネーションで取得する"""
    all_posts = []
    page = 1
    auth = _wp_auth()

    while True:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"WordPress API: page={page} を取得中...")
                resp = requests.get(
                    WP_API_URL,
                    params={
                        "per_page": WP_PER_PAGE,
                        "page": page,
                        "status": "publish,draft",
                        "_fields": "id,slug,content",
                    },
                    auth=auth,
                    timeout=30,
                )

                # 400 = ページ範囲外 (WordPress は最終ページ超過で 400 を返す場合あり)
                if resp.status_code == 400:
                    logger.info(f"WordPress API: page={page} で 400 応答 -> 取得完了")
                    return all_posts

                resp.raise_for_status()
                posts = resp.json()

                if not posts:
                    logger.info(f"WordPress API: page={page} で空レスポンス -> 取得完了")
                    return all_posts

                all_posts.extend(posts)
                logger.info(f"  -> {len(posts)} 件取得 (累計: {len(all_posts)})")
                break

            except requests.RequestException as e:
                logger.warning(
                    f"WordPress API エラー (page={page}, attempt={attempt}/{MAX_RETRIES}): {e}"
                )
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * attempt)
                else:
                    logger.error(f"WordPress API: page={page} の取得に最終的に失敗しました")
                    return all_posts

        page += 1

    return all_posts


# ---------------------------------------------------------------------------
# CHECKPOINT Parser
# ---------------------------------------------------------------------------
def parse_checkpoint_highlights(content_rendered: str) -> list:
    """WordPress記事の content.rendered から CHECKPOINT の <li> 要素を抽出する

    Returns:
        list[str]: ハイライトテキストのリスト。CHECKPOINT がなければ空リスト。
    """
    if not content_rendered:
        return []

    match = CHECKPOINT_PATTERN.search(content_rendered)
    if not match:
        return []

    ul_content = match.group(1)
    li_matches = LI_PATTERN.findall(ul_content)

    highlights = []
    for li_html in li_matches:
        # HTML タグを除去
        text = HTML_TAG_PATTERN.sub("", li_html)
        # HTML エンティティをデコード
        text = html.unescape(text)
        # 前後の空白を除去
        text = text.strip()
        if text:
            highlights.append(text)

    return highlights


# ---------------------------------------------------------------------------
# Main Logic
# ---------------------------------------------------------------------------
def build_slug_highlights_map(posts: list) -> dict:
    """WordPress 記事リストから slug -> highlights の辞書を構築する

    Returns:
        dict[str, list[str]]: slug をキー、highlights リストを値とする辞書
    """
    slug_map = {}
    checkpoint_count = 0

    for post in posts:
        slug = post.get("slug", "")
        content = post.get("content", {})
        rendered = content.get("rendered", "") if isinstance(content, dict) else ""

        highlights = parse_checkpoint_highlights(rendered)
        if highlights:
            slug_map[slug] = highlights
            checkpoint_count += 1
            logger.debug(f"  CHECKPOINT 検出: {slug} -> {len(highlights)} 件")

    logger.info(
        f"CHECKPOINT 解析完了: {checkpoint_count}/{len(posts)} 件の記事にCHECKPOINTあり"
    )
    return slug_map


def fetch_sanity_articles_without_highlights() -> list:
    """Sanity から highlights が未設定の記事を取得する"""
    groq = '*[_type == "article" && (!defined(highlights) || count(highlights) == 0)]{_id, "slug": slug.current}'
    logger.info("Sanity: highlights 未設定の記事を取得中...")
    articles = sanity_client.query(groq)
    logger.info(f"Sanity: {len(articles)} 件の記事が highlights 未設定")
    return articles


def batch_patch_highlights(
    sanity_articles: list, slug_map: dict, dry_run: bool = False
) -> int:
    """Sanity 記事に highlights をバッチでパッチする

    Returns:
        int: パッチした記事数
    """
    # slug -> Sanity article のマッピング
    mutations = []
    matched_count = 0

    for article in sanity_articles:
        slug = article.get("slug", "")
        doc_id = article.get("_id", "")

        if slug in slug_map:
            highlights = slug_map[slug]
            matched_count += 1

            if dry_run:
                logger.info(f"  [DRY-RUN] {slug} ({doc_id}): {highlights}")
            else:
                mutations.append(
                    {
                        "patch": {
                            "id": doc_id,
                            "set": {"highlights": highlights},
                        }
                    }
                )

    if dry_run:
        logger.info(f"[DRY-RUN] {matched_count} 件の記事がパッチ対象")
        return matched_count

    # バッチ実行
    patched = 0
    for i in range(0, len(mutations), SANITY_BATCH_SIZE):
        batch = mutations[i : i + SANITY_BATCH_SIZE]
        batch_num = (i // SANITY_BATCH_SIZE) + 1
        total_batches = (len(mutations) + SANITY_BATCH_SIZE - 1) // SANITY_BATCH_SIZE

        logger.info(
            f"Sanity バッチ {batch_num}/{total_batches}: {len(batch)} 件をパッチ中..."
        )
        try:
            sanity_client.transaction(batch)
            patched += len(batch)
            logger.info(f"  -> 成功 ({patched}/{len(mutations)})")
        except Exception as e:
            logger.error(f"  -> バッチ {batch_num} 失敗: {e}")
            # 個別にリトライ
            for mutation in batch:
                doc_id = mutation["patch"]["id"]
                highlights = mutation["patch"]["set"]["highlights"]
                try:
                    sanity_client.patch(doc_id, set_fields={"highlights": highlights})
                    patched += 1
                    logger.info(f"    個別パッチ成功: {doc_id}")
                except Exception as e2:
                    logger.error(f"    個別パッチ失敗: {doc_id}: {e2}")

    return patched


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="WordPress CHECKPOINT highlights を Sanity に移行する"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際にはパッチせず、何が行われるかを表示するだけ",
    )
    args = parser.parse_args()

    if args.dry_run:
        logger.info("=== DRY-RUN モード ===")

    logger.info("=" * 60)
    logger.info("CHECKPOINT highlights 移行スクリプト開始")
    logger.info("=" * 60)

    # Step 1: WordPress から全記事を取得
    logger.info("[Step 1/4] WordPress から記事を取得中...")
    wp_posts = fetch_all_wp_posts()
    logger.info(f"WordPress: {len(wp_posts)} 件の記事を取得")

    if not wp_posts:
        logger.error("WordPress から記事を取得できませんでした。終了します。")
        sys.exit(1)

    # Step 2: CHECKPOINT を解析
    logger.info("[Step 2/4] CHECKPOINT を解析中...")
    slug_map = build_slug_highlights_map(wp_posts)
    logger.info(f"CHECKPOINT あり: {len(slug_map)} 件")

    if not slug_map:
        logger.info("CHECKPOINT が含まれる記事がありません。終了します。")
        sys.exit(0)

    # Step 3: Sanity から highlights 未設定の記事を取得
    logger.info("[Step 3/4] Sanity から highlights 未設定の記事を取得中...")
    sanity_articles = fetch_sanity_articles_without_highlights()

    if not sanity_articles:
        logger.info("Sanity に highlights 未設定の記事がありません。終了します。")
        sys.exit(0)

    # Step 4: マッチングとパッチ
    logger.info("[Step 4/4] マッチングとパッチ...")
    patched_count = batch_patch_highlights(sanity_articles, slug_map, args.dry_run)

    # サマリー
    logger.info("=" * 60)
    logger.info("移行サマリー")
    logger.info("=" * 60)
    logger.info(f"  WordPress 記事総数:          {len(wp_posts)}")
    logger.info(f"  CHECKPOINT あり:             {len(slug_map)}")
    logger.info(f"  Sanity highlights 未設定:    {len(sanity_articles)}")
    logger.info(f"  slug マッチ & パッチ済み:    {patched_count}")
    if args.dry_run:
        logger.info("  (DRY-RUN: 実際のパッチは行われていません)")
    logger.info("=" * 60)
    logger.info("完了")


if __name__ == "__main__":
    main()
