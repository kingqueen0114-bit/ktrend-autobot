"""
Gemini モデルバージョン自動チェッカー

現在使用中の gemini-2.5-flash の後継として安定版（gemini-3-flash）が
移行されたかを自動検出し、LINE通知を送る。

Cloud Scheduler で毎日1回呼び出す想定。
安定版が利用可能になったら通知し、手動で1行変更するだけで移行完了。

変更対象ファイル（通知メッセージに記載）:
  - src/content_generator.py: models_to_try のプライマリモデル
  - src/fetch_trends.py: models_to_try のプライマリモデル
  - test_raw.py
"""

import os
import requests
from typing import Optional
from utils.logging_config import log_event, log_error, mask_url_keys


# 現在使用中のモデル / 移行先のモデル
CURRENT_MODEL = "gemini-2.5-flash"
STABLE_MODEL = "gemini-3-flash"


def check_model_availability(api_key: str) -> dict:
    """
    Gemini APIのモデル一覧を確認し、安定版モデルが利用可能かチェック。

    Returns:
        {
            "stable_available": bool,
            "current_available": bool,
            "stable_model": str,
            "current_model": str,
            "action_needed": bool,
            "message": str,
        }
    """
    result = {
        "stable_available": False,
        "current_available": False,
        "stable_model": STABLE_MODEL,
        "current_model": CURRENT_MODEL,
        "action_needed": False,
        "message": "",
    }

    try:
        # models.get で安定版モデルの存在を確認
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{STABLE_MODEL}?key={api_key}"
        resp = requests.get(url, timeout=10)

        if resp.status_code == 200:
            result["stable_available"] = True
            model_info = resp.json()
            result["message"] = (
                f"✅ 安定版モデル '{STABLE_MODEL}' が利用可能です。\n"
                f"表示名: {model_info.get('displayName', 'N/A')}\n"
                f"説明: {model_info.get('description', 'N/A')[:100]}"
            )
        elif resp.status_code == 404:
            result["message"] = f"安定版 '{STABLE_MODEL}' はまだ未公開です。"
        else:
            result["message"] = f"APIチェック中にエラー: {resp.status_code}"

        # 現在のpreviewモデルが存在するかも確認
        url_current = f"https://generativelanguage.googleapis.com/v1beta/models/{CURRENT_MODEL}?key={api_key}"
        resp_current = requests.get(url_current, timeout=10)
        result["current_available"] = resp_current.status_code == 200

        # 判定: 安定版が利用可能になったらアクション必要
        if result["stable_available"]:
            result["action_needed"] = True

    except Exception as e:
        result["message"] = f"モデルチェック失敗: {mask_url_keys(str(e))}"

    return result


def notify_model_upgrade(api_key: str) -> Optional[str]:
    """
    モデルの安定版が利用可能か確認し、利用可能なら LINE 通知を送る。
    Cloud Scheduler から日次で呼び出す想定。

    Returns:
        通知メッセージ（通知不要ならNone）
    """
    check = check_model_availability(api_key)

    if not check["action_needed"]:
        log_event("MODEL_CHECK", f"Model check: {check['message']}")
        return None

    # LINE通知メッセージ
    message = (
        f"🔔 Geminiモデル更新通知\n\n"
        f"安定版 `{STABLE_MODEL}` が利用可能になりました。\n\n"
        f"【対応方法】\n"
        f"以下ファイルの models_to_try プライマリモデルを\n"
        f"gemini-3-flash に変更してください:\n\n"
        f"1. src/content_generator.py\n"
        f"2. src/fetch_trends.py\n"
        f"3. test_raw.py\n\n"
        f"変更後にデプロイすれば完了です。"
    )

    # LINE通知を試みる
    line_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    line_user_id = os.environ.get("LINE_USER_ID")

    if line_token and line_user_id:
        try:
            user_id = line_user_id.split(",")[0]
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {line_token}"
            }
            payload = {
                "to": user_id,
                "messages": [{"type": "text", "text": message}]
            }
            resp = requests.post(
                "https://api.line.me/v2/bot/message/push",
                headers=headers, json=payload, timeout=10
            )
            if resp.status_code == 200:
                log_event("MODEL_NOTIFY", "Model upgrade notification sent via LINE")
            else:
                log_error("MODEL_NOTIFY_FAILED", f"LINE notification failed: {resp.status_code}")
        except Exception as e:
            log_error("MODEL_NOTIFY_ERROR", f"LINE notification error: {mask_url_keys(str(e))}", error=e)
    else:
        log_event("MODEL_NOTIFY", "LINE credentials not configured, notification skipped")

    return message
