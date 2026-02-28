"""
K-Trend Times 品質チェック関数
タスク4: 生成後の自動品質チェック。7項目の検証とスコアリング。

チェック項目:
1. URL実在チェック（HEAD リクエスト）
2. 文字数チェック（1000字以上）
3. 必須フィールドの充実度チェック
4. ハッシュタグ数チェック
5. Grounding信頼度チェック
6. ソース照合（日付の検証）
7. 禁止パターンのチェック
"""

import re
import requests
from typing import Dict, List, Optional


def quality_check(article_json: Dict, source_articles: List[Dict] = None,
                  grounding_metadata: Dict = None) -> Dict:
    """
    生成された記事の品質をチェックし、スコアを返す。

    Args:
        article_json: 生成された記事JSON
        source_articles: ソース記事のリスト（original_text含む）
        grounding_metadata: Groundingメタデータ（grounding_parser の戻り値）

    Returns:
        {
            "score": 0-100,
            "issues": [{"type": str, "detail": str, "severity": "CRITICAL"|"HIGH"|"MEDIUM"|"LOW"}],
            "publish_action": "auto_publish" | "review_needed" | "reject"
        }
    """
    issues = []

    # --- Check 1: URL実在チェック ---
    urls_in_body = re.findall(r'https?://[^\s\)]+', article_json.get("body", ""))
    for url in urls_in_body:
        url_clean = url.rstrip(".,;:!?)")  # 末尾の句読点を除去
        try:
            resp = requests.head(url_clean, timeout=5, allow_redirects=True,
                                 headers={"User-Agent": "K-Trend-QualityCheck/1.0"})
            if resp.status_code >= 400:
                issues.append({
                    "type": "DEAD_URL",
                    "detail": f"URL返却ステータス {resp.status_code}: {url_clean}",
                    "severity": "HIGH"
                })
        except requests.RequestException:
            issues.append({
                "type": "UNREACHABLE_URL",
                "detail": f"到達不能: {url_clean}",
                "severity": "HIGH"
            })

    # --- Check 2: 文字数チェック ---
    body_text = article_json.get("body", "")
    body_length = len(body_text)
    if body_length < 1000:
        issues.append({
            "type": "SHORT_ARTICLE",
            "detail": f"本文が{body_length}文字（目標1000字以上）",
            "severity": "CRITICAL"
        })

    # --- Check 3: 必須フィールドの充実度チェック ---
    required_fields = ["title", "meta_description", "body", "x_post_1", "x_post_2",
                       "artist_tags", "tags", "highlights", "research_report"]
    for field in required_fields:
        value = article_json.get(field)
        if not value or (isinstance(value, str) and len(value.strip()) < 5):
            issues.append({
                "type": "EMPTY_FIELD",
                "detail": f"フィールド '{field}' が空または不十分",
                "severity": "HIGH"
            })
        if isinstance(value, list) and len(value) == 0:
            issues.append({
                "type": "EMPTY_FIELD",
                "detail": f"フィールド '{field}' が空配列",
                "severity": "HIGH"
            })

    # --- Check 4: ハッシュタグ数チェック ---
    for field_name in ["x_post_1", "x_post_2"]:
        post_text = article_json.get(field_name, "")
        hashtag_count = len(re.findall(r'#\S+', post_text))
        if hashtag_count < 3:
            issues.append({
                "type": "INSUFFICIENT_HASHTAGS",
                "detail": f"{field_name}のハッシュタグが{hashtag_count}個（目標3個）",
                "severity": "LOW"
            })

    # --- Check 5: Grounding信頼度チェック（Grounding使用時のみ）---
    if grounding_metadata and grounding_metadata.get("low_confidence_segments"):
        for segment in grounding_metadata["low_confidence_segments"]:
            if segment.get("confidence", 1.0) < 0.5:
                issues.append({
                    "type": "LOW_GROUNDING_CONFIDENCE",
                    "detail": f"低信頼度({segment['confidence']:.2f}): '{segment.get('text', '')[:50]}...'",
                    "severity": "HIGH"
                })

    # --- Check 6: ソース照合（ソース原文がある場合）---
    if source_articles:
        # 記事内の日付をソースと照合
        dates_in_body = re.findall(
            r'\d{4}年\d{1,2}月\d{1,2}日|\d{4}/\d{1,2}/\d{1,2}|\d{4}-\d{2}-\d{2}',
            body_text
        )
        source_texts = " ".join([s.get("original_text", "") for s in source_articles])
        for date in dates_in_body:
            if date not in source_texts:
                issues.append({
                    "type": "UNVERIFIED_DATE",
                    "detail": f"ソースに見つからない日付: {date}",
                    "severity": "MEDIUM"
                })

    # --- Check 7: 禁止パターンのチェック ---
    forbidden_patterns = [
        (r'\*\*[^*]+\*\*', "マークダウン強調（**）の使用"),
        (r'(?<!\*)\*(?!\*)[^*]+\*(?!\*)', "マークダウン斜体（*）の使用（クレジット除く）"),
        (r'[■●▶▷◆◇]', "装飾記号の使用"),
    ]
    for pattern, desc in forbidden_patterns:
        # クレジット行を除外してチェック
        body_without_credit = re.sub(r'\*写真＝.*?\*', '', body_text)
        body_without_credit = re.sub(r'\*Photo.*?\*', '', body_without_credit)
        if re.search(pattern, body_without_credit):
            issues.append({
                "type": "FORBIDDEN_PATTERN",
                "detail": desc,
                "severity": "MEDIUM"
            })

    # --- スコア計算 ---
    score = 100
    for issue in issues:
        if issue["severity"] == "CRITICAL":
            score -= 25
        elif issue["severity"] == "HIGH":
            score -= 10
        elif issue["severity"] == "MEDIUM":
            score -= 5
        elif issue["severity"] == "LOW":
            score -= 2
    score = max(0, score)

    # --- 公開判定 ---
    if score >= 90:
        publish_action = "auto_publish"
    elif score >= 70:
        publish_action = "review_needed"
    else:
        publish_action = "reject"

    return {
        "score": score,
        "issues": issues,
        "publish_action": publish_action
    }
