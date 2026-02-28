"""
K-Trend Times ファクトチェッカー
事実検証: 生成記事内の固有名詞（人名×ブランド名）の組み合わせを抽出し、
Gemini + Google Search Grounding で検証する。

検証不能な主張は警告として返し、auto_fix で除去 or 注釈を付与する。
"""

import re
import json
import os
import requests
from typing import Dict, List, Tuple
from utils.logging_config import log_event, log_error, mask_url_keys


def verify_article_facts(article_json: Dict, api_key: str = None) -> Dict:
    """
    生成記事のファクトチェックを実行する。

    手順:
    1. 記事本文から固有名詞の主張（人名×ブランド、日付×イベント等）を抽出
    2. 各主張をGemini + Google Search Grounding で検証
    3. 検証結果を返す

    Args:
        article_json: 生成された記事JSON (title, body 等)
        api_key: Gemini API key

    Returns:
        {
            "verified_claims": [...],    # 検証OK
            "unverified_claims": [...],  # 検証NG（ハルシネーション疑い）
            "fact_score": 0-100,         # ファクトスコア
            "action": "pass" | "fix_needed" | "reject"
        }
    """
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return {"verified_claims": [], "unverified_claims": [],
                "fact_score": 100, "action": "pass",
                "note": "API key not available, skipped fact check"}

    body = article_json.get("body", "")
    title = article_json.get("title", "")
    full_text = f"{title}\n{body}"

    # Step 1: 主張を抽出してファクトチェック用プロンプトを構築
    fact_check_prompt = _build_fact_check_prompt(full_text)

    # Step 2: Gemini + Grounding でファクトチェック
    try:
        result = _call_fact_check_api(fact_check_prompt, api_key)
        return result
    except Exception as e:
        log_error("FACT_CHECK_FAILED", f"Fact check failed: {mask_url_keys(str(e))}", error=e)
        return {"verified_claims": [], "unverified_claims": [],
                "fact_score": 50, "action": "fix_needed",
                "note": f"Fact check API error: {mask_url_keys(str(e))[:100]}"}


def _build_fact_check_prompt(article_text: str) -> str:
    """ファクトチェック用プロンプトを構築"""
    from datetime import datetime, timezone, timedelta
    jst = timezone(timedelta(hours=9))
    today = datetime.now(jst).strftime("%Y年%m月%d日")

    return f"""あなたはファクトチェッカーです。本日は{today}です。

以下の記事テキストに含まれる【事実の主張】を検証してください。
Google検索で裏付けが取れるかどうかを確認し、JSON形式で結果を返してください。

特に以下を重点的にチェックしてください：
1. 人物名×ブランド名の組み合わせ（アンバサダー就任、コラボなど）
2. 具体的な日付×イベント（発売日、公演日、発表日など）
3. 数値データ（売上、ランキング、金額など）
4. 固有名詞の組み合わせ（人名×作品名、ブランド×商品名など）

【記事テキスト】
{article_text[:3000]}

【出力形式】JSON のみで回答してください：
{{
  "claims": [
    {{
      "claim": "検証した主張の内容",
      "status": "VERIFIED" または "UNVERIFIED" または "PARTIALLY_CORRECT",
      "evidence": "検証根拠の簡潔な説明",
      "correction": "UNVERIFIED/PARTIALLY_CORRECTの場合の正しい情報（分かる場合）"
    }}
  ]
}}

重要：
- 一般的な事実（「K-POPは世界的に人気」など）はチェック不要
- 具体的で検証可能な主張のみをチェックすること
- Google検索で確認できない主張は必ず UNVERIFIED にすること
- 最大5件までチェックすること（重要度の高い順）"""


def _call_fact_check_api(prompt: str, api_key: str) -> Dict:
    """Gemini API + Grounding でファクトチェックを実行"""
    models = ["gemini-2.5-flash", "gemini-2.0-flash"]

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"googleSearch": {}}],
            "generationConfig": {
                "temperature": 0.1  # 低温度でファクト重視
            }
        }

        try:
            response = requests.post(url, headers={"Content-Type": "application/json"},
                                     json=payload, timeout=60)
            if response.status_code in [503, 429]:
                log_error("FACT_CHECK_RETRY", f"Fact check: {model} returned {response.status_code}, trying next model")
                continue
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                raise requests.exceptions.HTTPError(
                    mask_url_keys(str(e)), response=e.response
                ) from None

            data = response.json()
            parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            text = "".join(part.get("text", "") for part in parts).strip()

            # JSONパース
            try:
                result = json.loads(text)
            except json.JSONDecodeError:
                json_match = re.search(r'\{[\s\S]*\}', text)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    continue

            # 結果を整理
            claims = result.get("claims", [])
            verified = [c for c in claims if c.get("status") == "VERIFIED"]
            unverified = [c for c in claims
                         if c.get("status") in ["UNVERIFIED", "PARTIALLY_CORRECT"]]

            total = len(claims)
            if total == 0:
                return {"verified_claims": [], "unverified_claims": [],
                        "fact_score": 100, "action": "pass"}

            fact_score = int((len(verified) / total) * 100)

            if len(unverified) == 0:
                action = "pass"
            elif len(unverified) <= 1:
                action = "fix_needed"
            else:
                action = "reject"

            return {
                "verified_claims": verified,
                "unverified_claims": unverified,
                "fact_score": fact_score,
                "action": action
            }

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            log_error("FACT_CHECK_TIMEOUT", f"Fact check timeout with {model}: {mask_url_keys(str(e))}", error=e)
            continue
        except Exception as e:
            log_error("FACT_CHECK_ERROR", f"Fact check error with {model}: {mask_url_keys(str(e))}", error=e)
            continue

    # 全モデル失敗
    return {"verified_claims": [], "unverified_claims": [],
            "fact_score": 50, "action": "fix_needed",
            "note": "All fact check models failed"}


def remove_unverified_claims(article_json: Dict, fact_result: Dict) -> Dict:
    """
    検証NGの主張を記事から除去または注釈付きに修正する。

    Args:
        article_json: 元の記事JSON
        fact_result: verify_article_facts の結果

    Returns:
        修正済みの記事JSON
    """
    fixed = article_json.copy()
    body = fixed.get("body", "")
    unverified = fact_result.get("unverified_claims", [])

    if not unverified:
        return fixed

    for claim in unverified:
        claim_text = claim.get("claim", "")
        correction = claim.get("correction", "")

        # 主張のキーワードで該当文を特定
        keywords = _extract_keywords(claim_text)
        if not keywords:
            continue

        lines = body.split("\n")
        new_lines = []
        for line in lines:
            # キーワードが2つ以上マッチする行を検出
            matches = sum(1 for kw in keywords if kw in line)
            if matches >= 2 and len(line.strip()) > 10:
                if correction:
                    # 正しい情報で置換
                    new_lines.append(f"（※編集部注: {correction}）")
                    log_event("FACT_FIX", "Replaced unverified claim with correction")
                else:
                    # 削除（空行にする）
                    log_event("FACT_FIX", "Removed unverified claim")
            else:
                new_lines.append(line)

        body = "\n".join(new_lines)

    # 連続空行を整理
    body = re.sub(r'\n{3,}', '\n\n', body)

    fixed["body"] = body
    return fixed


def _extract_keywords(text: str) -> List[str]:
    """主張テキストから検索用キーワードを抽出"""
    # 固有名詞やブランド名を抽出（カタカナ語、英語、漢字名）
    patterns = [
        r'[A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)*',   # 英語固有名詞
        r'[ァ-ヶー]{3,}',                            # カタカナ語
    ]

    keywords = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        keywords.extend(found)

    # 重複削除・短すぎるものを除外
    keywords = list(set(kw for kw in keywords if len(kw) >= 3))
    return keywords[:5]  # 最大5つ
