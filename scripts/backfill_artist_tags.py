#!/usr/bin/env python3
"""WordPress アーティストタグ → Sanity 一括反映スクリプト

WordPressの記事タグ情報を取得し、Sanityの記事に artistTags として反映する。
さらに、タグが紐づいていない記事には、タイトル内のキーワードマッチで自動タグ付けする。

Usage:
    python scripts/backfill_artist_tags.py                    # 本番実行
    python scripts/backfill_artist_tags.py --dry-run           # プレビューのみ
    python scripts/backfill_artist_tags.py --force              # 既存タグも上書き
"""

import argparse
import json
import logging
import os
import re
import sys
import time
import urllib.parse

import requests

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
WP_URL = "https://k-trendtimes.com"
SANITY_PROJECT_ID = "3pe6cvt2"
SANITY_DATASET = "production"
SANITY_API_VERSION = "2024-01-01"
SANITY_BATCH_SIZE = 50

# アーティスト・人物タグのマスターリスト（WordPress の既存タグ + 追加）
# タイトルマッチングに使用。キーは検索用パターン、値はタグ表示名
ARTIST_TAGS_MASTER = {
    # K-POPグループ
    "BTS": "BTS",
    "防弾少年団": "BTS",
    "バンタン": "BTS",
    "TWICE": "TWICE",
    "トゥワイス": "TWICE",
    "BLACKPINK": "BLACKPINK",
    "ブラックピンク": "BLACKPINK",
    "ブルピン": "BLACKPINK",
    "NewJeans": "NewJeans",
    "ニュージーンズ": "NewJeans",
    "IVE": "IVE",
    "アイヴ": "IVE",
    "aespa": "aespa",
    "エスパ": "aespa",
    "SEVENTEEN": "SEVENTEEN",
    "セブチ": "SEVENTEEN",
    "LE SSERAFIM": "LE SSERAFIM",
    "ルセラフィム": "LE SSERAFIM",
    "BABYMONSTER": "BABYMONSTER",
    "ベビモン": "BABYMONSTER",
    "NCT DREAM": "NCT DREAM",
    "NCT": "NCT",
    "NMIXX": "NMIXX",
    "TWS": "TWS",
    "ZB1": "ZEROBASEONE",
    "ZEROBASEONE": "ZEROBASEONE",
    "ゼベワン": "ZEROBASEONE",
    "ILLIT": "ILLIT",
    "Stray Kids": "Stray Kids",
    "スキズ": "Stray Kids",
    "ストレイキッズ": "Stray Kids",
    "ENHYPEN": "ENHYPEN",
    "エンハイプン": "ENHYPEN",
    "TXT": "TXT",
    "TREASURE": "TREASURE",
    "ATEEZ": "ATEEZ",
    "ITZY": "ITZY",
    "イッチ": "ITZY",
    "Red Velvet": "Red Velvet",
    "レドベル": "Red Velvet",
    "(G)I-DLE": "(G)I-DLE",
    "アイドゥル": "(G)I-DLE",
    "GIDLE": "(G)I-DLE",
    "EXO": "EXO",
    "エクソ": "EXO",
    "MONSTA X": "MONSTA X",
    "SHINee": "SHINee",
    "シャイニー": "SHINee",
    "GOT7": "GOT7",
    "ASTRO": "ASTRO",
    "VIVIZ": "VIVIZ",
    "Kep1er": "Kep1er",
    "ケプラー": "Kep1er",
    "fromis_9": "fromis_9",
    "HYBE": "HYBE",
    "ADOR": "ADOR",
    "JYP": "JYP",
    "SM": "SM",
    "YG": "YG",
    "BOYNEXTDOOR": "BOYNEXTDOOR",
    "RIIZE": "RIIZE",
    "KISS OF LIFE": "KISS OF LIFE",
    "from20": "from20",
    "HELLO GLOOM": "HELLO GLOOM",
    "A.I.D": "A.I.D",
    "nævis": "nævis",
    "ネイビス": "nævis",
    "tripleS": "tripleS",
    "KATSEYE": "KATSEYE",
    # メンバー個人名
    "JIN": "JIN",
    "ジン": "JIN",
    "RM": "RM",
    "SUGA": "SUGA",
    "シュガ": "SUGA",
    "J-HOPE": "J-HOPE",
    "ジェイホープ": "J-HOPE",
    "JIMIN": "JIMIN",
    "ジミン": "JIMIN",
    "V": None,  # 1文字は誤マッチが多いので除外
    "テテ": "V",
    "JUNGKOOK": "JUNGKOOK",
    "ジョングク": "JUNGKOOK",
    "Lisa": "Lisa",
    "リサ": "Lisa",
    "Jennie": "Jennie",
    "ジェニ": "Jennie",
    "ジェニー": "Jennie",
    "JISOO": "JISOO",
    "ジス": "JISOO",
    "Rosé": "Rosé",
    "ロゼ": "Rosé",
    "Winter": None,  # 英単語と被るので除外
    "ウィンター": "Winter",
    "Karina": "Karina",
    "カリナ": "Karina",
    "ミナ": "MINA",
    "ダニエル": "Daniel",
    # 俳優
    "キム・スヒョン": "キム・スヒョン",
    "ピョン・ウソク": "ピョン・ウソク",
    "イ・ジョンソク": "イ・ジョンソク",
    "キム・ジウォン": "キム・ジウォン",
    "シン・セギョン": "シン・セギョン",
    "チョ・ジョンソク": "チョ・ジョンソク",
    "ソン・ジュンギ": "ソン・ジュンギ",
    "パク・ソジュン": "パク・ソジュン",
    "コン・ユ": "コン・ユ",
    "チョン・ヘイン": "チョン・ヘイン",
    # ブランド（アーティスト関連）
    "村上隆": "村上隆",
    # イベント
    "KCON": "KCON",
    "MAMA": None,  # 「ママ」と誤マッチするため除外
    "MAMA AWARDS": "MAMA AWARDS",
}


# ---------------------------------------------------------------------------
# WordPress API
# ---------------------------------------------------------------------------
def fetch_wp_posts_with_tags() -> dict:
    """WordPress REST API から全記事のslug → tag名リストのマッピングを作成"""
    # まずWordPressのタグ一覧を取得 (id → name)
    tag_map = {}
    page = 1
    while True:
        resp = requests.get(
            f"{WP_URL}/wp-json/wp/v2/tags",
            params={"per_page": 100, "page": page},
            timeout=15,
        )
        if resp.status_code != 200:
            break
        tags = resp.json()
        if not tags:
            break
        for t in tags:
            tag_map[t["id"]] = t["name"]
        if page >= int(resp.headers.get("X-WP-TotalPages", "1")):
            break
        page += 1

    logger.info(f"WordPress: {len(tag_map)} 個のタグを取得")

    # 記事のslug → タグ名リスト
    slug_to_tags = {}
    page = 1
    while True:
        logger.info(f"WordPress 記事取得: page={page}...")
        resp = requests.get(
            f"{WP_URL}/wp-json/wp/v2/posts",
            params={
                "per_page": 50,
                "page": page,
                "status": "publish",
                "_fields": "slug,tags",
            },
            timeout=30,
        )
        if resp.status_code in (400, 404) or not resp.json():
            break
        resp.raise_for_status()
        posts = resp.json()
        if not posts:
            break

        for post in posts:
            slug = post.get("slug", "")
            wp_tag_ids = post.get("tags", [])
            tag_names = [tag_map[tid] for tid in wp_tag_ids if tid in tag_map]
            if tag_names:
                slug_to_tags[slug] = tag_names

        total_pages = int(resp.headers.get("X-WP-TotalPages", "1"))
        if page >= total_pages:
            break
        page += 1

    return slug_to_tags


def match_artist_tags_from_title(title: str) -> list:
    """記事タイトルからマスターリストに基づいてアーティストタグを抽出"""
    found = set()

    for keyword, tag_name in ARTIST_TAGS_MASTER.items():
        if tag_name is None:
            continue  # 除外パターン

        # キーワードの長さが3文字以下の場合は完全単語マッチ
        if len(keyword) <= 3:
            # 英数字の場合、単語境界でマッチ
            if re.match(r'^[A-Za-z0-9]+$', keyword):
                pattern = r'(?<![A-Za-z0-9])' + re.escape(keyword) + r'(?![A-Za-z0-9])'
                if re.search(pattern, title, re.IGNORECASE):
                    found.add(tag_name)
            else:
                # 日本語の場合はそのまま含むかチェック
                if keyword in title:
                    found.add(tag_name)
        else:
            # 長いキーワードはケースインセンシティブで含むかチェック
            if keyword.lower() in title.lower():
                found.add(tag_name)

    return sorted(found)


# ---------------------------------------------------------------------------
# Sanity API
# ---------------------------------------------------------------------------
def sanity_query(groq: str) -> list:
    """Sanity GROQクエリ（認証不要の読み取り）"""
    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"
    resp = requests.get(url, params={"query": groq}, timeout=30)
    resp.raise_for_status()
    return resp.json().get("result", [])


def sanity_mutate(mutations: list, token: str) -> dict:
    """Sanity Mutations API（認証必須の書き込み）"""
    url = f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/mutate/{SANITY_DATASET}"
    resp = requests.post(
        url,
        json={"mutations": mutations},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="WordPress アーティストタグ → Sanity 一括反映"
    )
    parser.add_argument("--dry-run", action="store_true", help="プレビューモード")
    parser.add_argument("--force", action="store_true", help="既存タグも上書き")
    args = parser.parse_args()

    # Sanity API Token
    token = os.environ.get("SANITY_API_TOKEN", "")
    if not token and not args.dry_run:
        logger.error("SANITY_API_TOKEN が未設定です。export SANITY_API_TOKEN=xxx を実行してください。")
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("WordPress アーティストタグ → Sanity 一括反映")
    logger.info("=" * 60)
    if args.dry_run:
        logger.info("🔍 DRY-RUN モード")

    # Step 1: WordPress からタグ情報を取得
    logger.info("\n[Step 1] WordPress からタグ情報を取得中...")
    wp_slug_to_tags = fetch_wp_posts_with_tags()
    logger.info(f"  WordPress でタグ付きの記事: {len(wp_slug_to_tags)} 件")

    # Step 2: Sanity から全記事を取得
    logger.info("\n[Step 2] Sanity から全記事を取得中...")
    groq = '*[_type == "article"] | order(publishedAt desc) {_id, title, artistTags, "slug": slug.current}'
    sanity_articles = sanity_query(groq)
    logger.info(f"  Sanity 記事数: {len(sanity_articles)} 件")

    has_tags = sum(1 for a in sanity_articles if a.get("artistTags"))
    no_tags = len(sanity_articles) - has_tags
    logger.info(f"  タグあり: {has_tags} 件 / タグなし: {no_tags} 件")

    # Step 3: タグマッチング
    logger.info("\n[Step 3] アーティストタグをマッチング中...")
    mutations = []
    tagged_count = 0
    skipped_count = 0
    wp_match_count = 0
    title_match_count = 0

    for article in sanity_articles:
        doc_id = article.get("_id", "")
        title = article.get("title", "")
        slug = article.get("slug", "")
        existing_tags = article.get("artistTags") or []

        # 既にタグがある場合はスキップ（--force でない限り）
        if existing_tags and not args.force:
            skipped_count += 1
            continue

        # 方法1: WordPress タグから取得
        tags_from_wp = wp_slug_to_tags.get(slug, [])

        # 方法2: タイトルからキーワードマッチ
        tags_from_title = match_artist_tags_from_title(title)

        # 統合（重複排除）
        all_tags = list(set(tags_from_wp + tags_from_title))

        if all_tags:
            tagged_count += 1
            if tags_from_wp:
                wp_match_count += 1
            if tags_from_title:
                title_match_count += 1

            if args.dry_run:
                sources = []
                if tags_from_wp:
                    sources.append(f"WP:{tags_from_wp}")
                if tags_from_title:
                    sources.append(f"Title:{tags_from_title}")
                logger.info(f"  🏷 {title[:50]}... → {all_tags} ({', '.join(sources)})")
            else:
                mutations.append({
                    "patch": {
                        "id": doc_id,
                        "set": {"artistTags": all_tags},
                    }
                })

    logger.info(f"\n  マッチ結果: {tagged_count} 件にタグ付け")
    logger.info(f"    WordPress タグ由来: {wp_match_count} 件")
    logger.info(f"    タイトルマッチ由来: {title_match_count} 件")
    logger.info(f"    スキップ: {skipped_count} 件")

    if args.dry_run:
        logger.info("\n[DRY-RUN] 実際の更新は行いませんでした。")
        logger.info("=" * 60)
        return

    # Step 4: Sanity にバッチパッチ
    if not mutations:
        logger.info("\n更新対象の記事がありません。")
        return

    logger.info(f"\n[Step 4] Sanity に {len(mutations)} 件をパッチ中...")
    patched = 0
    for i in range(0, len(mutations), SANITY_BATCH_SIZE):
        batch = mutations[i:i + SANITY_BATCH_SIZE]
        batch_num = (i // SANITY_BATCH_SIZE) + 1
        total_batches = (len(mutations) + SANITY_BATCH_SIZE - 1) // SANITY_BATCH_SIZE

        logger.info(f"  バッチ {batch_num}/{total_batches}: {len(batch)} 件...")
        try:
            sanity_mutate(batch, token)
            patched += len(batch)
            logger.info(f"    → 成功 ({patched}/{len(mutations)})")
        except Exception as e:
            logger.error(f"    → バッチ失敗: {e}")
            # 個別リトライ
            for mutation in batch:
                try:
                    sanity_mutate([mutation], token)
                    patched += 1
                except Exception as e2:
                    doc_id = mutation["patch"]["id"]
                    logger.error(f"    個別失敗: {doc_id}: {e2}")
        time.sleep(0.5)  # レート制限対策

    # サマリー
    logger.info("\n" + "=" * 60)
    logger.info("実行サマリー")
    logger.info("=" * 60)
    logger.info(f"  全記事数:         {len(sanity_articles)} 件")
    logger.info(f"  タグ付け:         {patched} 件")
    logger.info(f"  スキップ:         {skipped_count} 件")
    logger.info("=" * 60)
    logger.info("完了 ✅")


if __name__ == "__main__":
    main()
