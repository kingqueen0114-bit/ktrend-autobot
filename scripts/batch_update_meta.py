#!/usr/bin/env python3
"""
K-TREND TIMES meta description 一括更新スクリプト

seo.metaDescription が空もしくは50文字未満の記事に対して、
Gemini AIでmeta descriptionを生成し、Sanityにバッチパッチする。

Usage:
    python scripts/batch_update_meta.py --dry-run   # 確認のみ
    python scripts/batch_update_meta.py              # 実行
"""

import os
import sys
import time
import argparse

# プロジェクトルートをPATHに追加
from dotenv import load_dotenv
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
load_dotenv(os.path.join(project_root, '.env'), override=True)
load_dotenv(os.path.join(project_root, 'frontend', '.env.local'), override=True)

import src.sanity_client as sanity_client
import google.generativeai as genai


BATCH_SIZE = 50
SLEEP_BETWEEN_REQUESTS = 1  # Gemini APIレート制限対策


def get_articles_needing_meta() -> list:
    """seo.metaDescription が空 or 50文字未満の記事を取得"""
    query = """*[_type == "article" && defined(publishedAt) && (
        !defined(seo.metaDescription) ||
        seo.metaDescription == "" ||
        length(seo.metaDescription) < 50
    )] | order(publishedAt desc) {
        _id,
        title,
        excerpt,
        "bodyText": pt::text(body)[0...500],
        seo
    }"""
    return sanity_client.query(query)


def generate_meta_description(model, title: str, excerpt: str, body_text: str) -> str:
    """Gemini AIでmeta descriptionを生成"""
    prompt = f"""以下の記事のmeta descriptionを生成してください。

要件:
- 日本語で120文字以内
- 記事の核心を簡潔に伝える
- 読者がクリックしたくなるような内容
- キーワードを自然に含める
- 句読点を含めて自然な文章

タイトル: {title}
抜粋: {excerpt or '(なし)'}
本文冒頭: {body_text or '(なし)'}

meta descriptionのみを出力してください（説明や引用符は不要）:"""

    response = model.generate_content(prompt)
    result = response.text.strip()
    # 引用符が付いている場合は除去
    if result.startswith('"') and result.endswith('"'):
        result = result[1:-1]
    if result.startswith("'") and result.endswith("'"):
        result = result[1:-1]
    # 120文字で切り詰め
    if len(result) > 120:
        result = result[:117] + "..."
    return result


def batch_update(updates: list):
    """Sanity トランザクションでバッチ更新"""
    mutations = []
    for item in updates:
        mutations.append({
            "patch": {
                "id": item["_id"],
                "set": {
                    "seo.metaDescription": item["metaDescription"]
                }
            }
        })

    # BATCH_SIZE 件ずつ送信
    for i in range(0, len(mutations), BATCH_SIZE):
        batch = mutations[i:i + BATCH_SIZE]
        sanity_client.transaction(batch)
        print(f"  Patched {min(i + BATCH_SIZE, len(mutations))}/{len(mutations)} articles")


def main():
    parser = argparse.ArgumentParser(description="meta description 一括更新")
    parser.add_argument("--dry-run", action="store_true", help="生成結果の確認のみ（Sanityへの書き込みなし）")
    parser.add_argument("--limit", type=int, default=0, help="処理する記事数の上限（0=全件）")
    args = parser.parse_args()

    # 環境変数チェック
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY environment variable is required")
        sys.exit(1)

    # Gemini 初期化
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    # 対象記事取得
    print("Fetching articles with missing/short meta descriptions...")
    articles = get_articles_needing_meta()
    print(f"Found {len(articles)} articles needing meta description updates")

    if args.limit > 0:
        articles = articles[:args.limit]
        print(f"  Limited to {len(articles)} articles")

    if not articles:
        print("No articles to process. Exiting.")
        return

    # meta description 生成
    updates = []
    for i, article in enumerate(articles):
        title = article.get("title", "")
        excerpt = article.get("excerpt", "")
        body_text = article.get("bodyText", "")
        current_meta = article.get("seo", {}).get("metaDescription", "") if article.get("seo") else ""

        print(f"\n[{i + 1}/{len(articles)}] {title[:60]}")
        if current_meta:
            print(f"  Current ({len(current_meta)}字): {current_meta[:80]}...")

        try:
            new_meta = generate_meta_description(model, title, excerpt, body_text)
            print(f"  Generated ({len(new_meta)}字): {new_meta}")

            updates.append({
                "_id": article["_id"],
                "metaDescription": new_meta
            })
        except Exception as e:
            print(f"  Error generating meta: {e}")

        # レート制限対策
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"\n{'=' * 60}")
    print(f"Total: {len(updates)} meta descriptions generated")

    if args.dry_run:
        print("DRY RUN - No changes written to Sanity")
        return

    if not updates:
        print("No updates to apply.")
        return

    # Sanity バッチ更新
    print(f"\nApplying {len(updates)} updates to Sanity...")
    batch_update(updates)
    print("Done!")


if __name__ == "__main__":
    main()
