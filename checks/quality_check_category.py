"""カテゴリに応じた品質チェックの分岐処理"""

import re
from typing import Dict, List, Optional
from src.category_config import get_category


def quality_check_by_category(
    article: dict,
    category_id: str,
    sources: list = None,
    grounding_metadata: dict = None,
) -> dict:
    """
    カテゴリに応じた品質チェックを実行。

    Returns:
        {
            "quality_score": int,
            "checks": [{"name": str, "status": str, "detail": str, "deduction": int}, ...],
            "publish_action": "publish" | "review" | "reject",
            "category": str,
        }
    """
    config = get_category(category_id)
    checks = []
    score = 100

    body = article.get("body", "")
    title = article.get("title", "")

    # --- 共通チェック ---

    # 1. 文字数チェック（カテゴリ別基準）
    char_count = len(body)
    if char_count < config.min_chars:
        checks.append({
            "name": "文字数チェック",
            "status": "fail",
            "detail": f"{char_count}字（最低{config.min_chars}字必要）",
            "deduction": -10,
        })
        score -= 10
    elif char_count > config.max_chars:
        checks.append({
            "name": "文字数チェック",
            "status": "warn",
            "detail": f"{char_count}字（上限{config.max_chars}字超過）",
            "deduction": -5,
        })
        score -= 5
    else:
        checks.append({
            "name": "文字数チェック",
            "status": "pass",
            "detail": f"{char_count}字（{config.min_chars}-{config.max_chars}字の範囲内）",
            "deduction": 0,
        })

    # 2. 必須フィールドチェック
    required_fields = ["title", "body", "tags"]
    missing = [f for f in required_fields if not article.get(f)]
    if missing:
        checks.append({
            "name": "必須フィールド",
            "status": "fail",
            "detail": f"未入力: {', '.join(missing)}",
            "deduction": -10,
        })
        score -= 10
    else:
        checks.append({
            "name": "必須フィールド",
            "status": "pass",
            "detail": "全て入力済み",
            "deduction": 0,
        })

    # 3. ハッシュタグチェック
    x_post = article.get("x_post_1", "")
    hashtag_count = x_post.count("#")
    if hashtag_count < 3:
        checks.append({
            "name": "ハッシュタグ",
            "status": "warn",
            "detail": f"{hashtag_count}個（3個以上推奨）",
            "deduction": -2,
        })
        score -= 2
    else:
        checks.append({
            "name": "ハッシュタグ",
            "status": "pass",
            "detail": f"{hashtag_count}個",
            "deduction": 0,
        })

    # 4. 禁止パターンチェック
    forbidden_patterns = ["**", "■", "###", "---"]
    found_patterns = [p for p in forbidden_patterns if p in body]
    if found_patterns:
        checks.append({
            "name": "禁止パターン",
            "status": "fail",
            "detail": f"検出: {', '.join(found_patterns)}",
            "deduction": -5,
        })
        score -= 5
    else:
        checks.append({
            "name": "禁止パターン",
            "status": "pass",
            "detail": "なし",
            "deduction": 0,
        })

    # --- カテゴリ固有チェック ---

    # 5. 推測表現チェック（kpop, event）
    if "speculation_check" in config.extra_checks:
        speculation_phrases = [
            "と予想される", "が期待される", "と見られている",
            "注目が集まりそう", "話題になりそう", "期待が高まる",
            "と思われる", "可能性がある",
        ]
        found_speculation = [p for p in speculation_phrases if p in body]
        if found_speculation:
            checks.append({
                "name": "推測表現チェック",
                "status": "warn",
                "detail": f"検出: {', '.join(found_speculation[:3])}",
                "deduction": -5,
            })
            score -= 5
        else:
            checks.append({
                "name": "推測表現チェック",
                "status": "pass",
                "detail": "推測表現なし",
                "deduction": 0,
            })

    # 6. 出典記載チェック（source_citation_required）
    if config.source_citation_required:
        has_citation = any(kw in body for kw in ["出典", "PR TIMES", "prtimes.jp", "https://"])
        if not has_citation:
            checks.append({
                "name": "出典記載チェック",
                "status": "fail",
                "detail": "出典の記載がありません",
                "deduction": -10,
            })
            score -= 10
        else:
            checks.append({
                "name": "出典記載チェック",
                "status": "pass",
                "detail": "出典記載あり",
                "deduction": 0,
            })

    # 7. 効果効能チェック（cosme）
    if "efficacy_check" in config.extra_checks:
        efficacy_phrases = [
            "シワが消える", "シミが消える", "美白になる",
            "若返る", "治る", "改善される",
            "アンチエイジング効果", "痩せる",
        ]
        found_efficacy = [p for p in efficacy_phrases if p in body]
        if found_efficacy:
            checks.append({
                "name": "効果効能チェック",
                "status": "fail",
                "detail": f"薬機法的に問題の可能性: {', '.join(found_efficacy[:3])}",
                "deduction": -10,
            })
            score -= 10
        else:
            checks.append({
                "name": "効果効能チェック",
                "status": "pass",
                "detail": "問題のある表現なし",
                "deduction": 0,
            })

    # 8. 日時正確性チェック（event）
    if "date_accuracy_check" in config.extra_checks:
        if article.get("event_date"):
            checks.append({
                "name": "日時正確性チェック",
                "status": "pass",
                "detail": f"イベント日時: {article['event_date']}",
                "deduction": 0,
            })
        else:
            checks.append({
                "name": "日時正確性チェック",
                "status": "warn",
                "detail": "イベント日時が未設定",
                "deduction": -5,
            })
            score -= 5

    # 9. 鮮度チェック（gourmet, travel）
    if "freshness_check" in config.extra_checks:
        stale_phrases = ["※閉店", "閉業", "営業終了", "移転しました", "閉店"]
        found_stale = [p for p in stale_phrases if p in body]
        if found_stale:
            checks.append({
                "name": "鮮度チェック",
                "status": "fail",
                "detail": f"古い情報の可能性: {', '.join(found_stale)}",
                "deduction": -10,
            })
            score -= 10
        else:
            checks.append({
                "name": "鮮度チェック",
                "status": "pass",
                "detail": "問題なし",
                "deduction": 0,
            })

    # --- 判定 ---
    score = max(0, score)

    if score >= 90:
        publish_action = "publish"
    elif score >= 70:
        publish_action = "review"
    else:
        publish_action = "reject"

    return {
        "quality_score": score,
        "checks": checks,
        "publish_action": publish_action,
        "category": category_id,
    }
