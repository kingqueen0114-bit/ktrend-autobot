#!/usr/bin/env python3
"""
K-Trend AutoBot - Rich Menu Setup Script
Creates and sets a rich menu using the LINE Messaging API.

Usage:
    python setup_richmenu.py [--image PATH_TO_IMAGE]
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
if not CHANNEL_ACCESS_TOKEN:
    print("❌ LINE_CHANNEL_ACCESS_TOKEN not found in .env")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Rich Menu Definition - 3 columns side-by-side (2500x843)
RICH_MENU_BODY = {
    "size": {
        "width": 2500,
        "height": 843
    },
    "selected": True,
    "name": "K-Trend AutoBot Menu v7 (Minimal)",
    "chatBarText": "メニュー",
    "areas": [
        {
            # Left column: 記事作成
            "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
            "action": {"type": "message", "text": "カテゴリ"}
        },
        {
            # Middle column: 記事一覧 (Web Link)
            "bounds": {"x": 833, "y": 0, "width": 834, "height": 843},
            "action": {"type": "uri", "uri": "https://ktrend-autobot-nnfhuwwfiq-an.a.run.app/drafts"}
        },
        {
            # Right column: レポート (統計)
            "bounds": {"x": 1667, "y": 0, "width": 833, "height": 843},
            "action": {"type": "message", "text": "統計"}
        }
    ]
}


def delete_existing_rich_menus():
    """Delete all existing rich menus."""
    print("🗑️  既存のリッチメニューを確認中...")
    resp = requests.get(
        "https://api.line.me/v2/bot/richmenu/list",
        headers=HEADERS
    )
    if resp.status_code == 200:
        menus = resp.json().get("richmenus", [])
        if menus:
            for menu in menus:
                rid = menu["richMenuId"]
                print(f"   削除: {rid} ({menu.get('name', 'unknown')})")
                requests.delete(
                    f"https://api.line.me/v2/bot/richmenu/{rid}",
                    headers=HEADERS
                )
            print(f"   ✅ {len(menus)}件のリッチメニューを削除しました")
        else:
            print("   既存のリッチメニューはありません")
    else:
        print(f"   ⚠️ リスト取得に失敗: {resp.status_code}")


def create_rich_menu():
    """Create a new rich menu and return its ID."""
    print("📋 リッチメニューを作成中...")
    resp = requests.post(
        "https://api.line.me/v2/bot/richmenu",
        headers=HEADERS,
        json=RICH_MENU_BODY
    )
    if resp.status_code == 200:
        rich_menu_id = resp.json()["richMenuId"]
        print(f"   ✅ 作成成功: {rich_menu_id}")
        return rich_menu_id
    else:
        print(f"   ❌ 作成失敗: {resp.status_code} {resp.text}")
        sys.exit(1)


def upload_image(rich_menu_id, image_path):
    """Upload the rich menu image."""
    print(f"🖼️  画像をアップロード中: {image_path}")

    # Determine content type
    if image_path.lower().endswith(".png"):
        content_type = "image/png"
    else:
        content_type = "image/jpeg"

    with open(image_path, "rb") as f:
        resp = requests.post(
            f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content",
            headers={
                "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
                "Content-Type": content_type
            },
            data=f.read()
        )

    if resp.status_code == 200:
        print("   ✅ 画像アップロード成功")
    else:
        print(f"   ❌ 画像アップロード失敗: {resp.status_code} {resp.text}")
        sys.exit(1)


def set_default(rich_menu_id):
    """Set the rich menu as the default for all users."""
    print("🔗 デフォルトリッチメニューに設定中...")
    resp = requests.post(
        f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}",
        headers=HEADERS
    )
    if resp.status_code == 200:
        print("   ✅ デフォルト設定完了！")
    else:
        print(f"   ❌ デフォルト設定失敗: {resp.status_code} {resp.text}")


def main():
    # Parse args
    image_path = None
    if "--image" in sys.argv:
        idx = sys.argv.index("--image")
        if idx + 1 < len(sys.argv):
            image_path = sys.argv[idx + 1]

    if not image_path:
        # Default image path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_path = os.path.join(script_dir, "assets", "rich_menu.png")
        if os.path.exists(default_path):
            image_path = default_path
        else:
            print("❌ 画像ファイルが見つかりません。--image オプションで指定してください。")
            print(f"   例: python setup_richmenu.py --image /path/to/rich_menu.png")
            sys.exit(1)

    if not os.path.exists(image_path):
        print(f"❌ 画像ファイルが見つかりません: {image_path}")
        sys.exit(1)

    print("=" * 50)
    print("🎨 K-Trend AutoBot リッチメニュー セットアップ")
    print("=" * 50)

    # Step 1: Delete existing
    delete_existing_rich_menus()

    # Step 2: Create new
    rich_menu_id = create_rich_menu()

    # Step 3: Upload image
    upload_image(rich_menu_id, image_path)

    # Step 4: Set as default
    set_default(rich_menu_id)

    print("\n" + "=" * 50)
    print("🎉 セットアップ完了！")
    print(f"   Rich Menu ID: {rich_menu_id}")
    print("=" * 50)


if __name__ == "__main__":
    main()
