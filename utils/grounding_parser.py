"""
K-Trend Times Grounding Metadata Parser
タスク1-C: Gemini REST APIの応答からGroundingメタデータ（ソースURL・信頼度）を抽出する。
"""

from typing import Dict, List, Optional


def parse_grounding_metadata(api_response: Dict) -> Dict:
    """
    Gemini REST APIのJSON応答からGroundingメタデータを抽出する。

    Args:
        api_response: Gemini REST APIの生のJSON応答（response.json()）

    Returns:
        {
            "source_urls": [{"title": str, "url": str}, ...],
            "low_confidence_segments": [{"text": str, "confidence": float}, ...],
            "has_grounding": bool,
            "raw_metadata": dict  # 生のgroundingMetadata（後続処理用）
        }
    """
    result = {
        "source_urls": [],
        "low_confidence_segments": [],
        "has_grounding": False,
        "raw_metadata": {},
    }

    candidate = api_response.get("candidates", [{}])[0]
    grounding = candidate.get("groundingMetadata", {})

    if not grounding:
        return result

    result["has_grounding"] = True
    result["raw_metadata"] = grounding

    # ソースURL一覧を取得（groundingChunks）
    chunks = grounding.get("groundingChunks", [])
    for chunk in chunks:
        web = chunk.get("web", {})
        if web:
            result["source_urls"].append({
                "title": web.get("title", ""),
                "url": web.get("uri", ""),
            })

    # 各記述の信頼度スコアを取得（groundingSupports）
    supports = grounding.get("groundingSupports", [])
    for support in supports:
        confidence_scores = support.get("confidenceScores", [])
        if confidence_scores:
            min_confidence = min(confidence_scores)
            if min_confidence < 0.7:
                segment = support.get("segment", {})
                result["low_confidence_segments"].append({
                    "text": segment.get("text", ""),
                    "confidence": min_confidence,
                })

    if result["source_urls"]:
        print(f"🔍 Grounding: {len(result['source_urls'])} sources found")
    if result["low_confidence_segments"]:
        print(f"⚠️ Grounding: {len(result['low_confidence_segments'])} low-confidence segments detected")

    return result


def get_verified_urls(grounding_result: Dict) -> List[str]:
    """
    Grounding結果から信頼できるURLのリストを取得する。

    Args:
        grounding_result: parse_grounding_metadata() の戻り値

    Returns:
        URL文字列のリスト
    """
    return [s["url"] for s in grounding_result.get("source_urls", []) if s.get("url")]
