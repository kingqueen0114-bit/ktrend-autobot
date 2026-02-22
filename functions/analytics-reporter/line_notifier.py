"""LINE Notifier for Cloud Functions"""

import os
import requests


class LineNotifier:
    """LINE通知クラス"""

    def __init__(self):
        self.channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
        self.admin_user_id = os.getenv("LINE_ADMIN_USER_ID", "")
        self.push_endpoint = "https://api.line.me/v2/bot/message/push"

    def push_message(self, user_id: str, messages: list) -> bool:
        """プッシュメッセージ送信"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.channel_access_token}",
            }

            payload = {
                "to": user_id,
                "messages": messages,
            }

            response = requests.post(self.push_endpoint, json=payload, headers=headers)
            response.raise_for_status()

            print(f"LINE通知送信成功: {user_id}")
            return True

        except Exception as e:
            print(f"LINE通知送信失敗: {e}")
            return False
