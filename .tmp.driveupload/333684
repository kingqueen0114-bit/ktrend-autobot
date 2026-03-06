#!/usr/bin/env python3
"""Gemini AI による Sanity 記事ハイライト自動生成スクリプト

Sanity上のhighlightsが未設定またはプレースホルダーのままの記事を検出し、
Gemini 2.0 Flash で記事本文から要約ハイライト3件を自動生成してパッチする。

Usage:
    python generate_highlights.py              # 全件実行
    python generate_highlights.py --dry-run    # プレビューのみ
    python generate_highlights.py --limit 10   # 先頭10件のみ
    python generate_highlights.py --offset 20  # 21件目から開始
"""

import argparse
import json
import logging
import os
import sys
import time

import requests

# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

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
SANITY_PROJECT_ID = "3pe6cvt2"
SANITY_DATASET = "production"
SANITY_API_VERSION = "2024-01-01"
SANITY_QUERY_URL = (
    f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}"
    f"/data/query/{SANITY_DATASET}"
)
SANITY_MUTATE_URL = (
    f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}"
    f"/data/mutate/{SANITY_DATASET}"
)

GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_DELAY = 6  # seconds between API calls (rate limit対策)
GEMINI_MAX_RETRIES = 5
SANITY_BATCH_SIZE = 50
MIN_BODY_LENGTH = 50

GROQ_QUERY = """*[_type == "article" && (!defined(highlights) || count(highlights) == 0 || highlights[0] in ["情報1", "最新情報", "要点1"])]{_id, "slug": slug.current, title, "bodyText": pt::text(body)}"""

HIGHLIGHT_PROMPT_TEMPLATE = """以下の記事本文を読み、記事の要約サマリー（highlights）を3つ生成してください。

ルール:
- 読者がこの3つを読むだけで記事の核心が分かるように
- 具体的な事実・数字・日付・場所・人物名を含めること
- 各要約文は30〜60文字
- プレースホルダー（「最新情報」「情報1」等）は絶対に使わないこと
- JSON配列で出力: ["要約1", "要約2", "要約3"]

記事タイトル: {title}

記事本文:
{body_text}"""


# ---------------------------------------------------------------------------
# Token / Key Loaders
# ---------------------------------------------------------------------------
def load_sanity_token() -> str:
    """Load SANITY_API_TOKEN from environment variable or frontend/.env.local"""
    token = os.environ.get("SANITY_API_TOKEN")
    if token:
        return token
    env_path = os.path.join(PROJECT_ROOT, "frontend", ".env.local")
    try:
        with open(env_path) as f:
            for line in f:
                if line.startswith("SANITY_API_TOKEN="):
                    return line.strip().split("=", 1)[1]
    except FileNotFoundError:
        pass
    raise ValueError("SANITY_API_TOKEN が環境変数にも frontend/.env.local にも見つかりません")


def load_gemini_key() -> str:
    """Load GEMINI_API_KEY from .env.yaml or environment"""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    yaml_path = os.path.join(PROJECT_ROOT, ".env.yaml")
    with open(yaml_path) as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY:"):
                return line.strip().split(":", 1)[1].strip().strip('"')
    raise ValueError("GEMINI_API_KEY not found in .env.yaml or environment")


# ---------------------------------------------------------------------------
# Sanity API Helpers
# ---------------------------------------------------------------------------
def sanity_query(query: str, token: str) -> list:
    """Execute a GROQ query against Sanity and return the result list."""
    resp = requests.get(
        SANITY_QUERY_URL,
        params={"query": query},
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", [])


def sanity_mutate(mutations: list, token: str) -> dict:
    """Send a batch of mutations to Sanity."""
    resp = requests.post(
        SANITY_MUTATE_URL,
        json={"mutations": mutations},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def sanity_patch_single(doc_id: str, highlights: list, token: str) -> dict:
    """Patch a single document's highlights field."""
    mutations = [
        {
            "patch": {
                "id": doc_id,
                "set": {"highlights": highlights},
            }
        }
    ]
    return sanity_mutate(mutations, token)


# ---------------------------------------------------------------------------
# Gemini AI
# ---------------------------------------------------------------------------
def init_gemini(api_key: str):
    """Initialize the Gemini generative model and return it."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)

    generation_config = genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema={
            "type": "ARRAY",
            "items": {"type": "STRING"},
        },
        temperature=0.3,
    )

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        generation_config=generation_config,
    )
    return model


def generate_highlights_for_article(
    model, title: str, body_text: str
) -> list | None:
    """Call Gemini to generate 3 highlights for an article.

    Returns:
        list[str] of 3 highlights, or None on failure.
    """
    prompt = HIGHLIGHT_PROMPT_TEMPLATE.format(
        title=title,
        body_text=body_text[:8000],  # Truncate very long articles
    )

    for attempt in range(1, GEMINI_MAX_RETRIES + 1):
        try:
            response = model.generate_content(prompt)
            highlights = json.loads(response.text)

            # Validate
            if validate_highlights(highlights):
                return highlights

            logger.warning(
                f"  バリデーション失敗 (attempt {attempt}): {highlights}"
            )

        except json.JSONDecodeError as e:
            logger.warning(
                f"  JSON パースエラー (attempt {attempt}): {e}"
            )
        except Exception as e:
            logger.warning(
                f"  Gemini API エラー (attempt {attempt}): {e}"
            )
            # Exponential backoff (longer for rate limits)
            if attempt < GEMINI_MAX_RETRIES:
                is_rate_limit = "429" in str(e) or "Resource" in str(e)
                wait = (10 * attempt) if is_rate_limit else (2 ** attempt)
                logger.info(f"  {wait}秒待機してリトライ...")
                time.sleep(wait)

    return None


def validate_highlights(highlights: list) -> bool:
    """Validate that highlights meet quality criteria."""
    if not isinstance(highlights, list):
        return False
    if len(highlights) != 3:
        return False

    placeholder_words = {"情報1", "最新情報", "要点1", "要点2", "要点3", "情報2", "情報3"}

    for h in highlights:
        if not isinstance(h, str):
            return False
        length = len(h)
        if length < 10 or length > 100:
            return False
        if h in placeholder_words:
            return False

    return True


# ---------------------------------------------------------------------------
# Main Processing
# ---------------------------------------------------------------------------
def process_articles(
    articles: list,
    model,
    sanity_token: str,
    dry_run: bool = False,
) -> dict:
    """Process all articles: generate highlights and patch Sanity.

    Returns:
        dict with counts: total, successful, failed, skipped
    """
    stats = {"total": len(articles), "successful": 0, "failed": 0, "skipped": 0}
    mutations = []  # Buffer for batch patching
    mutation_map = {}  # doc_id -> highlights (for fallback individual patching)

    for idx, article in enumerate(articles):
        doc_id = article.get("_id", "")
        slug = article.get("slug", "")
        title = article.get("title", "")
        body_text = article.get("bodyText", "") or ""

        # Progress logging every 10 articles
        if idx > 0 and idx % 10 == 0:
            logger.info(
                f"--- 進捗: {idx}/{len(articles)} 件処理済み "
                f"(成功: {stats['successful']}, 失敗: {stats['failed']}, "
                f"スキップ: {stats['skipped']}) ---"
            )

        # Skip if body text is empty or too short
        if len(body_text.strip()) < MIN_BODY_LENGTH:
            logger.info(f"  [{idx+1}] SKIP (本文不足): {slug} ({len(body_text)}文字)")
            stats["skipped"] += 1
            continue

        logger.info(f"  [{idx+1}] 生成中: {slug} ({title[:40]}...)")

        # Generate highlights via Gemini
        highlights = generate_highlights_for_article(model, title, body_text)

        if highlights is None:
            logger.error(f"  [{idx+1}] FAIL: {slug} - ハイライト生成失敗")
            stats["failed"] += 1
            time.sleep(GEMINI_DELAY)
            continue

        logger.info(f"  [{idx+1}] OK: {highlights}")
        stats["successful"] += 1

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
            mutation_map[doc_id] = highlights

            # Flush batch when buffer reaches SANITY_BATCH_SIZE
            if len(mutations) >= SANITY_BATCH_SIZE:
                _flush_mutations(mutations, mutation_map, sanity_token)
                mutations = []
                mutation_map = {}

        # Rate limiting
        time.sleep(GEMINI_DELAY)

    # Flush remaining mutations
    if mutations and not dry_run:
        _flush_mutations(mutations, mutation_map, sanity_token)

    return stats


def _flush_mutations(
    mutations: list, mutation_map: dict, sanity_token: str
) -> None:
    """Send buffered mutations to Sanity, falling back to individual patches on error."""
    logger.info(f"Sanity バッチパッチ: {len(mutations)} 件送信中...")
    try:
        sanity_mutate(mutations, sanity_token)
        logger.info(f"  -> バッチパッチ成功 ({len(mutations)} 件)")
    except Exception as e:
        logger.error(f"  -> バッチパッチ失敗: {e}")
        logger.info("  -> 個別パッチにフォールバック...")
        for doc_id, highlights in mutation_map.items():
            try:
                sanity_patch_single(doc_id, highlights, sanity_token)
                logger.info(f"    個別パッチ成功: {doc_id}")
            except Exception as e2:
                logger.error(f"    個別パッチ失敗: {doc_id}: {e2}")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Gemini AI で Sanity 記事のハイライトを自動生成する"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際にはパッチせず、何が行われるかを表示するだけ",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="処理する記事の最大数（0 = 全件）",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="開始位置（N件目から処理開始）",
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Gemini AI ハイライト自動生成スクリプト")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("モード: DRY-RUN（実際のパッチは行いません）")
    if args.limit:
        logger.info(f"制限: 先頭 {args.limit} 件のみ処理")
    if args.offset:
        logger.info(f"オフセット: {args.offset} 件目から開始")

    # Step 1: Load credentials
    logger.info("[Step 1/4] 認証情報を読み込み中...")
    try:
        sanity_token = load_sanity_token()
        logger.info("  SANITY_API_TOKEN: OK")
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"  SANITY_API_TOKEN の読み込みに失敗: {e}")
        sys.exit(1)

    try:
        gemini_key = load_gemini_key()
        logger.info("  GEMINI_API_KEY: OK")
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"  GEMINI_API_KEY の読み込みに失敗: {e}")
        sys.exit(1)

    # Step 2: Query Sanity for articles needing highlights
    logger.info("[Step 2/4] Sanity からハイライト未設定の記事を取得中...")
    try:
        articles = sanity_query(GROQ_QUERY, sanity_token)
    except Exception as e:
        logger.error(f"  Sanity クエリ失敗: {e}")
        sys.exit(1)

    logger.info(f"  対象記事数: {len(articles)} 件")

    if not articles:
        logger.info("ハイライトが必要な記事がありません。終了します。")
        sys.exit(0)

    # Apply offset and limit
    if args.offset:
        articles = articles[args.offset:]
        logger.info(f"  オフセット適用後: {len(articles)} 件")

    if args.limit:
        articles = articles[: args.limit]
        logger.info(f"  制限適用後: {len(articles)} 件")

    if not articles:
        logger.info("処理対象の記事がありません。終了します。")
        sys.exit(0)

    # Step 3: Initialize Gemini
    logger.info("[Step 3/4] Gemini AI モデルを初期化中...")
    try:
        model = init_gemini(gemini_key)
        logger.info(f"  モデル: {GEMINI_MODEL}")
    except Exception as e:
        logger.error(f"  Gemini 初期化失敗: {e}")
        sys.exit(1)

    # Step 4: Process articles
    logger.info("[Step 4/4] ハイライト生成開始...")
    logger.info(f"  処理対象: {len(articles)} 件")
    logger.info(f"  推定所要時間: 約{len(articles) * (GEMINI_DELAY + 1):.0f}秒")
    logger.info("-" * 60)

    stats = process_articles(
        articles=articles,
        model=model,
        sanity_token=sanity_token,
        dry_run=args.dry_run,
    )

    # Summary
    logger.info("=" * 60)
    logger.info("実行サマリー")
    logger.info("=" * 60)
    logger.info(f"  対象記事数:    {stats['total']}")
    logger.info(f"  成功:          {stats['successful']}")
    logger.info(f"  失敗:          {stats['failed']}")
    logger.info(f"  スキップ:      {stats['skipped']}")
    if args.dry_run:
        logger.info("  (DRY-RUN: 実際のパッチは行われていません)")
    logger.info("=" * 60)
    logger.info("完了")


if __name__ == "__main__":
    main()
