#!/usr/bin/env python3
"""WordPress → Sanity 全記事移行 + アーティストタグ一括反映スクリプト

WordPress REST API から全公開記事を取得し、Sanity に未登録の記事を移行する。
さらに、全記事に対して Gemini 2.0 Flash でアーティストタグを抽出・反映する。

Usage:
    python scripts/migrate_wp_to_sanity.py                    # 全実行
    python scripts/migrate_wp_to_sanity.py --dry-run           # プレビューのみ
    python scripts/migrate_wp_to_sanity.py --tags-only          # アーティストタグのみ反映
    python scripts/migrate_wp_to_sanity.py --migrate-only       # 記事移行のみ
    python scripts/migrate_wp_to_sanity.py --force-tags          # 既存タグも上書き
"""

import argparse
import html as html_module
import json
import logging
import os
import re
import sys
import time
import uuid

import requests

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# .env / .env.yaml ファイルから環境変数をロード
def _load_dotenv():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Try .env first
    env_path = os.path.join(project_root, ".env")
    try:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and key not in os.environ:
                            os.environ[key] = value
    except PermissionError:
        pass  # .env がパーミッション保護されている場合はスキップ

    # Also try .env.yaml (Cloud Functions format)
    env_yaml_path = os.path.join(project_root, ".env.yaml")
    try:
        if os.path.exists(env_yaml_path):
            import yaml
            with open(env_yaml_path) as f:
                data = yaml.safe_load(f)
            if isinstance(data, dict):
                for k, v in data.items():
                    if k not in os.environ and v is not None:
                        os.environ[k] = str(v)
    except (PermissionError, ImportError):
        # yaml not installed or permission error
        # Fallback: simple key: value parser
        try:
            if os.path.exists(env_yaml_path):
                with open(env_yaml_path) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and ":" in line:
                            key, _, value = line.partition(":")
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if key and key not in os.environ:
                                os.environ[key] = value
        except PermissionError:
            pass

_load_dotenv()

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
WP_API_URL = os.environ.get("WORDPRESS_URL", "https://k-trendtimes.com")
WP_PER_PAGE = 50
MAX_RETRIES = 3
RETRY_DELAY = 2
SANITY_BATCH_SIZE = 50

# WordPress category ID → Sanity category slug
WP_CAT_MAP = {
    11: "artist",
    7: "beauty",
    10: "fashion",
    6: "gourmet",
    4: "koreantrip",
    5: "event",
    3: "trend",
    2: "trend",
    8: "trend",
    9: "lifestyle",
}

# カテゴリ参照キャッシュ
_category_ref_cache = {}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def make_key():
    return uuid.uuid4().hex[:12]


def decode_html_entities(text: str) -> str:
    if not text:
        return ""
    text = html_module.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def generate_slug(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s]+", "-", slug).strip("-")[:200]
    return slug or uuid.uuid4().hex[:20]


# ---------------------------------------------------------------------------
# WordPress API
# ---------------------------------------------------------------------------
def wp_auth():
    username = os.environ.get("WORDPRESS_USER", "admin")
    password = os.environ.get("WORDPRESS_APP_PASSWORD", "")
    if not password:
        logger.warning("WORDPRESS_APP_PASSWORD が未設定です。認証なしでアクセスします。")
        return None
    return (username, password)


def fetch_all_wp_posts() -> list:
    """WordPress REST API から全公開記事をページネーションで取得"""
    all_posts = []
    page = 1
    auth = wp_auth()

    while True:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"WordPress API: page={page} を取得中...")
                params = {
                    "per_page": WP_PER_PAGE,
                    "page": page,
                    "status": "publish",
                    "_embed": "true",
                }
                resp = requests.get(
                    f"{WP_API_URL}/wp-json/wp/v2/posts",
                    params=params,
                    auth=auth,
                    timeout=30,
                )

                if resp.status_code in (400, 404):
                    logger.info(f"WordPress API: page={page} → {resp.status_code} → 取得完了")
                    return all_posts

                resp.raise_for_status()
                posts = resp.json()

                if not posts:
                    logger.info(f"WordPress API: page={page} → 空 → 取得完了")
                    return all_posts

                all_posts.extend(posts)
                total_pages = int(resp.headers.get("X-WP-TotalPages", "1"))
                logger.info(f"  → {len(posts)} 件取得 (累計: {len(all_posts)}, 全{total_pages}ページ)")

                if page >= total_pages:
                    return all_posts
                break

            except requests.RequestException as e:
                logger.warning(f"WordPress API エラー (page={page}, attempt={attempt}): {e}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * attempt)
                else:
                    logger.error(f"page={page} の取得に失敗")
                    return all_posts

        page += 1

    return all_posts


# ---------------------------------------------------------------------------
# HTML → Portable Text 変換
# ---------------------------------------------------------------------------
def convert_html_to_portable_text(html_str: str) -> list:
    """HTMLをSanity Portable Textに変換"""
    if not html_str or not html_str.strip():
        return []

    from html.parser import HTMLParser

    blocks = []
    current_block = None
    current_children = []
    current_marks = []
    current_mark_defs = []
    current_style = "normal"
    list_style = None
    in_list = False

    class PTParser(HTMLParser):
        nonlocal blocks, current_block, current_children, current_marks
        nonlocal current_mark_defs, current_style, list_style, in_list

        def _flush_block(self):
            nonlocal current_children, current_mark_defs, current_style, list_style, in_list
            if current_children:
                block = {
                    "_type": "block",
                    "_key": make_key(),
                    "style": current_style,
                    "children": current_children,
                    "markDefs": current_mark_defs,
                }
                if in_list and list_style:
                    block["listItem"] = list_style
                    block["level"] = 1
                blocks.append(block)
            current_children = []
            current_mark_defs = []
            current_style = "normal"

        def handle_starttag(self, tag, attrs):
            nonlocal current_style, list_style, in_list, current_marks
            attrs_dict = dict(attrs)

            if tag in ("h2", "h3", "h4"):
                self._flush_block()
                current_style = tag
            elif tag == "p":
                self._flush_block()
                current_style = "normal"
            elif tag == "blockquote":
                self._flush_block()
                current_style = "blockquote"
            elif tag == "ul":
                self._flush_block()
                list_style = "bullet"
                in_list = True
            elif tag == "ol":
                self._flush_block()
                list_style = "number"
                in_list = True
            elif tag == "li":
                self._flush_block()
            elif tag in ("strong", "b"):
                current_marks.append("strong")
            elif tag in ("em", "i"):
                current_marks.append("em")
            elif tag == "a":
                href = attrs_dict.get("href", "")
                if href:
                    mark_key = make_key()
                    current_mark_defs.append({"_type": "link", "_key": mark_key, "href": href})
                    current_marks.append(mark_key)
            elif tag == "br":
                current_children.append({
                    "_type": "span", "_key": make_key(), "text": "\n", "marks": []
                })
            elif tag == "div":
                # div with class ktrend-checkpoint は無視
                cls = attrs_dict.get("class", "")
                if "ktrend-checkpoint" in cls:
                    pass  # Skip checkpoint divs

        def handle_endtag(self, tag):
            nonlocal in_list, list_style, current_marks
            if tag in ("h2", "h3", "h4", "p", "blockquote"):
                self._flush_block()
            elif tag in ("ul", "ol"):
                self._flush_block()
                in_list = False
                list_style = None
            elif tag == "li":
                self._flush_block()
            elif tag in ("strong", "b"):
                if "strong" in current_marks:
                    current_marks.remove("strong")
            elif tag in ("em", "i"):
                if "em" in current_marks:
                    current_marks.remove("em")
            elif tag == "a":
                # Remove the last link mark
                for i in range(len(current_marks) - 1, -1, -1):
                    if current_marks[i] not in ("strong", "em"):
                        current_marks.pop(i)
                        break

        def handle_data(self, data):
            text = data
            if text.strip():
                current_children.append({
                    "_type": "span",
                    "_key": make_key(),
                    "text": text,
                    "marks": list(current_marks),
                })

    try:
        parser = PTParser()
        parser.feed(html_str)
        parser._flush_block()
    except Exception as e:
        logger.warning(f"HTML→PT変換失敗: {e}")
        text = re.sub(r"<[^>]+>", "", html_str).strip()
        if text:
            blocks = [{
                "_type": "block", "_key": make_key(), "style": "normal",
                "children": [{"_type": "span", "_key": make_key(), "text": text, "marks": []}],
                "markDefs": [],
            }]

    # 空ブロックを除去
    blocks = [b for b in blocks if b.get("children")]
    return blocks


# ---------------------------------------------------------------------------
# Sanity helpers
# ---------------------------------------------------------------------------
def get_category_ref(slug: str) -> str:
    if slug in _category_ref_cache:
        return _category_ref_cache[slug]

    result = sanity_client.query_one(
        '*[_type == "category" && slug.current == $slug]{_id}',
        {"slug": slug}
    )
    if result:
        _category_ref_cache[slug] = result["_id"]
        return result["_id"]
    return ""


def get_or_create_tag(name: str) -> str:
    name = name.strip()
    if not name:
        return ""
    slug = re.sub(r"[^\w\s-]", "", name.lower())
    slug = re.sub(r"[\s]+", "-", slug).strip("-")[:96]

    existing = sanity_client.query_one(
        '*[_type == "tag" && (title == $name || slug.current == $slug)]{_id}',
        {"name": name, "slug": slug}
    )
    if existing:
        return existing["_id"]

    tag_id = sanity_client.generate_id()
    sanity_client.create({
        "_id": tag_id,
        "_type": "tag",
        "title": name,
        "slug": {"_type": "slug", "current": slug},
    })
    logger.info(f"  タグ作成: {name}")
    return tag_id


def upload_image_to_sanity(image_url: str) -> dict:
    """画像をSanityにアップロード"""
    if not image_url:
        return {}
    result = sanity_client.upload_image_from_url(image_url, max_retries=2)
    if result.get("_id"):
        return {
            "_type": "image",
            "asset": {"_type": "reference", "_ref": result["_id"]},
        }
    return {}


def get_existing_sanity_slugs() -> set:
    """Sanityに既に存在する記事のslugセットを取得"""
    articles = sanity_client.query(
        '*[_type == "article"]{"s": slug.current}'
    )
    return {a["s"] for a in articles if a.get("s")}



def get_all_sanity_articles() -> list:
    """Sanityの全記事を取得（アーティストタグ反映用）"""
    return sanity_client.query(
        '*[_type == "article" && defined(publishedAt)] | order(publishedAt desc) {_id, title, artistTags, "s": slug.current}'
    )


# ---------------------------------------------------------------------------
# 記事移行
# ---------------------------------------------------------------------------
def migrate_wp_post(wp_post: dict, existing_slugs: set, dry_run: bool = False) -> bool:
    """WordPress記事をSanityに移行"""
    raw_slug = wp_post.get("slug", "")
    slug = raw_slug  # WordPress slugをそのまま使う

    if slug in existing_slugs:
        logger.debug(f"  ✓ {slug} は移行済み")
        return False

    title = decode_html_entities(wp_post.get("title", {}).get("rendered", "Untitled"))
    html_body = wp_post.get("content", {}).get("rendered", "")
    excerpt = decode_html_entities(wp_post.get("excerpt", {}).get("rendered", ""))
    published_at = wp_post.get("date", "")

    if dry_run:
        logger.info(f"  [DRY-RUN] 移行対象: {title[:50]}... (slug: {slug})")
        return True

    # HTML → Portable Text
    body_pt = convert_html_to_portable_text(html_body)

    # 画像アップロード
    main_image = None
    embedded = wp_post.get("_embedded", {})
    featured_media = embedded.get("wp:featuredmedia", [])
    if featured_media and len(featured_media) > 0:
        feat_url = featured_media[0].get("source_url", "")
        if feat_url:
            main_image = upload_image_to_sanity(feat_url)
            if main_image:
                main_image["alt"] = title

    # カテゴリ参照
    category_ref = None
    wp_cats = wp_post.get("categories", [])
    for cat_id in wp_cats:
        cat_slug = WP_CAT_MAP.get(cat_id)
        if cat_slug:
            ref_id = get_category_ref(cat_slug)
            if ref_id:
                category_ref = {"_type": "reference", "_ref": ref_id}
                break

    # タグ参照（WordPress タグ）
    tag_refs = []
    wp_terms = embedded.get("wp:term", [])
    if len(wp_terms) > 1:
        for tag in wp_terms[1]:
            if tag.get("name"):
                tag_id = get_or_create_tag(tag["name"])
                if tag_id:
                    tag_refs.append({
                        "_type": "reference",
                        "_ref": tag_id,
                        "_key": make_key(),
                    })

    # Sanityドキュメント構築
    doc_id = sanity_client.generate_id()
    doc = {
        "_id": doc_id,
        "_type": "article",
        "title": title,
        "slug": {"_type": "slug", "current": slug},
        "publishedAt": published_at,
        "body": body_pt,
        "excerpt": excerpt,
        "seo": {
            "metaTitle": title,
            "metaDescription": excerpt,
        },
    }

    if main_image:
        doc["mainImage"] = main_image
    if category_ref:
        doc["category"] = category_ref
    if tag_refs:
        doc["tags"] = tag_refs

    # None値を除去
    doc = {k: v for k, v in doc.items() if v is not None}

    try:
        sanity_client.create_or_replace(doc)
        logger.info(f"  ✅ 移行完了: {title[:50]}... (slug: {slug})")
        existing_slugs.add(slug)
        return True
    except Exception as e:
        logger.error(f"  ❌ 移行失敗: {title[:50]}...: {e}")
        return False


# ---------------------------------------------------------------------------
# Gemini アーティストタグ抽出
# ---------------------------------------------------------------------------
def extract_artist_tags_with_gemini(title: str) -> list:
    """Gemini 2.0 Flash を使って記事タイトルからアーティストタグを抽出"""
    try:
        import google.generativeai as genai

        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            try:
                from google.cloud import secretmanager
                client = secretmanager.SecretManagerServiceClient()
                project_id = os.environ.get("GCP_PROJECT", "ktrend-autobot")
                name = f"projects/{project_id}/secrets/GEMINI_API_KEY/versions/latest"
                response = client.access_secret_version(request={"name": name})
                api_key = response.payload.data.decode("UTF-8")
            except Exception:
                pass

        if not api_key:
            logger.warning("GEMINI_API_KEY が未設定です。アーティストタグ抽出をスキップします。")
            return []

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""以下の韓国トレンド記事のタイトルから、関連するK-POPアーティスト名やグループ名を抽出してください。

タイトル: {title}

ルール:
- アーティスト名は公式のアルファベット表記で返してください（例: BTS, TWICE, BLACKPINK, NewJeans, ENHYPEN, aespa, Stray Kids, (G)I-DLE, IVE, LE SSERAFIM, ATEEZ, SEVENTEEN, EXO, NCT, Red Velvet, ITZY, TXT, TREASURE, BABYMONSTER）
- メンバー個人名もアルファベット表記で含めてOK（例: RM, Lisa, Jennie, Winter）
- アーティストに関連しない記事（グルメ、旅行、美容一般）は空の配列 [] を返してください
- ブランドやイベント名はアーティストタグに含めないでください
- JSON配列のみを返してください。説明は不要です。

出力例: ["BTS", "RM"] または []"""

        response = model.generate_content(prompt)
        text = response.text.strip()

        # JSON配列を抽出
        match = re.search(r'\[.*?\]', text, re.DOTALL)
        if match:
            tags = json.loads(match.group())
            return [t for t in tags if isinstance(t, str) and t.strip()]
        return []

    except Exception as e:
        logger.warning(f"Gemini タグ抽出失敗 ({title[:30]}...): {e}")
        return []


def backfill_artist_tags(dry_run: bool = False, force: bool = False) -> int:
    """全Sanity記事にアーティストタグを反映"""
    logger.info("Sanity から全記事を取得中...")
    articles = get_all_sanity_articles()
    logger.info(f"全 {len(articles)} 件の記事を取得")

    mutations = []
    processed = 0
    tagged = 0

    for article in articles:
        doc_id = article.get("_id", "")
        title = article.get("title", "")
        existing_tags = article.get("artistTags") or []

        # 既にタグがある場合はスキップ（--force でない限り）
        if existing_tags and not force:
            logger.debug(f"  ⏭ タグ済み: {title[:40]}... → {existing_tags}")
            continue

        processed += 1

        # Geminiでタグ抽出
        tags = extract_artist_tags_with_gemini(title)

        if tags:
            tagged += 1
            if dry_run:
                logger.info(f"  [DRY-RUN] {title[:50]}... → {tags}")
            else:
                mutations.append({
                    "patch": {
                        "id": doc_id,
                        "set": {"artistTags": tags},
                    }
                })
                logger.info(f"  🏷 {title[:50]}... → {tags}")
        else:
            logger.debug(f"  ⏭ タグなし: {title[:50]}...")

        # API レート制限対策
        if processed % 5 == 0:
            time.sleep(1)

    if dry_run:
        logger.info(f"[DRY-RUN] {tagged}/{processed} 件のタグを検出")
        return tagged

    # バッチでパッチ実行
    patched = 0
    for i in range(0, len(mutations), SANITY_BATCH_SIZE):
        batch = mutations[i:i + SANITY_BATCH_SIZE]
        batch_num = (i // SANITY_BATCH_SIZE) + 1
        total_batches = (len(mutations) + SANITY_BATCH_SIZE - 1) // SANITY_BATCH_SIZE

        logger.info(f"Sanity バッチ {batch_num}/{total_batches}: {len(batch)} 件をパッチ中...")
        try:
            sanity_client.transaction(batch)
            patched += len(batch)
            logger.info(f"  → 成功 ({patched}/{len(mutations)})")
        except Exception as e:
            logger.error(f"  → バッチ {batch_num} 失敗: {e}")
            # 個別リトライ
            for mutation in batch:
                doc_id = mutation["patch"]["id"]
                tags = mutation["patch"]["set"]["artistTags"]
                try:
                    sanity_client.patch(doc_id, set_fields={"artistTags": tags})
                    patched += 1
                except Exception as e2:
                    logger.error(f"    個別パッチ失敗: {doc_id}: {e2}")

    return patched


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="WordPress → Sanity 全記事移行 + アーティストタグ一括反映"
    )
    parser.add_argument("--dry-run", action="store_true", help="プレビューモード（実際の変更なし）")
    parser.add_argument("--tags-only", action="store_true", help="アーティストタグ反映のみ")
    parser.add_argument("--migrate-only", action="store_true", help="記事移行のみ")
    parser.add_argument("--force-tags", action="store_true", help="既存のアーティストタグも上書き")
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("WordPress → Sanity 全記事移行 + アーティストタグ反映")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("🔍 DRY-RUN モード (実際の変更は行いません)")

    migrated_count = 0
    skipped_count = 0
    tagged_count = 0

    # ===== Phase 1: 記事移行 =====
    if not args.tags_only:
        logger.info("\n" + "=" * 40)
        logger.info("[Phase 1] WordPress → Sanity 記事移行")
        logger.info("=" * 40)

        # WordPress記事を取得
        logger.info("WordPress から全記事を取得中...")
        wp_posts = fetch_all_wp_posts()
        logger.info(f"WordPress: {len(wp_posts)} 件の記事を取得")

        if not wp_posts:
            logger.error("WordPress から記事を取得できませんでした。")
            if not args.migrate_only:
                logger.info("アーティストタグ反映に進みます...")
        else:
            # 既存Sanity記事のslugを取得
            existing_slugs = get_existing_sanity_slugs()
            logger.info(f"Sanity: 既存 {len(existing_slugs)} 件の記事")

            for wp_post in wp_posts:
                result = migrate_wp_post(wp_post, existing_slugs, args.dry_run)
                if result:
                    migrated_count += 1
                else:
                    skipped_count += 1

            logger.info(f"\n移行結果: {migrated_count} 件移行, {skipped_count} 件スキップ")

    # ===== Phase 2: アーティストタグ反映 =====
    if not args.migrate_only:
        logger.info("\n" + "=" * 40)
        logger.info("[Phase 2] アーティストタグ一括反映")
        logger.info("=" * 40)

        tagged_count = backfill_artist_tags(args.dry_run, args.force_tags)
        logger.info(f"\nタグ反映結果: {tagged_count} 件")

    # ===== サマリー =====
    logger.info("\n" + "=" * 60)
    logger.info("実行サマリー")
    logger.info("=" * 60)
    if not args.tags_only:
        logger.info(f"  記事移行:        {migrated_count} 件")
        logger.info(f"  移行スキップ:    {skipped_count} 件")
    if not args.migrate_only:
        logger.info(f"  タグ反映:        {tagged_count} 件")
    if args.dry_run:
        logger.info("  (DRY-RUN: 実際の変更は行われていません)")
    logger.info("=" * 60)
    logger.info("完了 ✅")


if __name__ == "__main__":
    main()
