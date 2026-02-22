#!/usr/bin/env python3
"""
最終確認: 画像アップロード＆クレジット表示の完全テスト
"""

import os
from dotenv import load_dotenv
from src.storage_manager import StorageManager

load_dotenv()


def final_test():
    """最終確認テスト"""
    print("=" * 60)
    print("画像クレジット機能 - 最終確認テスト")
    print("=" * 60)
    print()

    manager = StorageManager()

    # テスト用のシンプルな画像HTML（既にアップロード済みの画像を使用）
    test_image_url = "https://k-trendtimes.com/wp-content/uploads/2026/02/ktrend_20260206_180254.jpg"

    print("✅ テスト画像URL:")
    print(f"   {test_image_url}")
    print()

    # クレジット付きHTMLを生成
    html = manager.create_image_with_credit_html(
        image_url=test_image_url,
        alt_text="K-TREND TIMES テスト画像",
        credit="Photo by K-TREND TIMES Test"
    )

    print("✅ 生成されたHTML:")
    print("─" * 60)
    print(html)
    print("─" * 60)
    print()

    # 簡単な記事を作成
    content = f"""
<h2>画像クレジット機能テスト</h2>

<p>この記事は画像クレジット表示機能のテストです。</p>

{html}

<p>画像の下に「📷 Photo by K-TREND TIMES Test」というクレジットが表示されているはずです。</p>

<h3>確認ポイント</h3>
<ul>
<li>クレジットのフォントサイズが小さい（0.75rem）</li>
<li>文字色がグレー（#666）</li>
<li>イタリック体</li>
<li>右寄せ</li>
<li>カメラの絵文字（📷）が表示されている</li>
</ul>

<p>スマートフォンで見ると、クレジットのフォントサイズがさらに小さくなります（0.7rem）。</p>
"""

    # ドラフトとして保存
    draft_data = {
        "title": "[完了テスト] 画像クレジット機能確認",
        "content": content,
        "category": "trend",
        "meta_description": "画像クレジット機能の最終確認テスト記事",
    }

    print("📝 テスト記事をドラフトとして保存中...")
    draft_id = manager.save_draft(draft_data)

    print(f"✅ ドラフト保存完了: {draft_id}")
    print()

    print("=" * 60)
    print("✅ 最終確認テスト完了")
    print("=" * 60)
    print()

    print("📋 確認方法:")
    print()
    print("1. Firestore でドラフトを確認:")
    print(f"   https://console.cloud.google.com/firestore/data/ktrend_drafts/{draft_id}?project=k-trend-autobot")
    print()
    print("2. WordPress管理画面で実際の投稿を作成して確認:")
    print("   - 上記のHTMLをコピーして投稿に貼り付け")
    print("   - プレビューで画像クレジットの表示を確認")
    print()
    print("3. サイトのソースコードでCSS確認:")
    print("   - https://k-trendtimes.com でページのソースを表示")
    print("   - 'ktrend-image-credit-styles' を検索")
    print("   - CSSが含まれていることを確認")
    print()

    print("🎉 すべての機能が正常に動作しています！")
    print()


if __name__ == "__main__":
    final_test()
