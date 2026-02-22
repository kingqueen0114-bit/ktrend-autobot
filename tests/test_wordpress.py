"""
WordPress REST API 接続テストスクリプト

使用方法:
    python test_wordpress.py

環境変数が正しく設定されていることを確認してください。
"""

import os
import sys
from dotenv import load_dotenv

# .envを読み込み
load_dotenv()

# 環境変数チェック
required_vars = ["WORDPRESS_URL", "WORDPRESS_USER", "WORDPRESS_APP_PASSWORD"]
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"Error: Missing environment variables: {', '.join(missing)}")
    print("Please set them in .env file")
    sys.exit(1)

from src.storage_manager import StorageManager


def test_wordpress_connection():
    """WordPress接続テスト"""
    print("=" * 50)
    print("WordPress REST API 接続テスト")
    print("=" * 50)

    storage = StorageManager()

    print(f"\nWordPress URL: {storage.wp_url}")
    print(f"User: {storage.wp_user}")

    # カテゴリ取得テスト
    print("\n1. カテゴリ取得テスト...")
    categories = storage.get_categories()
    if categories:
        print(f"   成功: {len(categories)} カテゴリ取得")
        for cat in categories[:5]:
            print(f"   - {cat['id']}: {cat['slug']} ({cat['name']})")
    else:
        print("   失敗: カテゴリを取得できませんでした")
        return False

    return True


def test_draft_save():
    """Firestoreドラフト保存テスト"""
    print("\n2. Firestore ドラフト保存テスト...")

    storage = StorageManager()

    # テストドラフトを保存
    test_data = {
        "title": "テスト記事タイトル",
        "content": "<p>これはテスト記事の本文です。</p>",
        "image_url": "https://via.placeholder.com/800x400",
        "category": "trend",
        "meta_description": "テスト記事のメタディスクリプション",
        "gemini_summary": "AI生成のサマリー",
    }

    try:
        draft_id = storage.save_draft(test_data)
        print(f"   成功: ドラフト保存 (ID: {draft_id})")

        # 取得テスト
        retrieved = storage.get_draft(draft_id)
        if retrieved:
            print(f"   成功: ドラフト取得")
            print(f"   タイトル: {retrieved.get('title')}")

        return draft_id
    except Exception as e:
        print(f"   失敗: {e}")
        return None


def test_publish_draft(draft_id: str):
    """WordPress公開テスト（任意）"""
    print("\n3. WordPress公開テスト...")
    print("   注意: これは実際にWordPressに記事を公開します")

    confirm = input("   公開テストを実行しますか? (yes/no): ")
    if confirm.lower() != "yes":
        print("   スキップしました")
        return

    storage = StorageManager()

    try:
        result = storage.publish_draft(draft_id)
        if result:
            print(f"   成功: 記事を公開しました")
            print(f"   記事ID: {result['id']}")
            print(f"   URL: {result['url']}")
        else:
            print("   失敗: 公開に失敗しました")
    except Exception as e:
        print(f"   エラー: {e}")


def main():
    print("\nK-Trend AutoBot - WordPress連携テスト\n")

    # 接続テスト
    if not test_wordpress_connection():
        print("\n接続テスト失敗。設定を確認してください。")
        return

    # ドラフト保存テスト
    draft_id = test_draft_save()
    if not draft_id:
        print("\nドラフト保存テスト失敗。Firestore設定を確認してください。")
        return

    # 公開テスト（任意）
    test_publish_draft(draft_id)

    print("\n" + "=" * 50)
    print("テスト完了")
    print("=" * 50)


if __name__ == "__main__":
    main()
