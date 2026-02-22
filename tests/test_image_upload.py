#!/usr/bin/env python3
"""
画像アップロード機能のテスト
実際に画像をアップロードして、クレジット表示機能を確認
"""

import os
import sys
from dotenv import load_dotenv
from src.storage_manager import StorageManager

# 環境変数読み込み
load_dotenv()


def create_test_image():
    """テスト用の画像を生成"""
    try:
        from PIL import Image, ImageDraw, ImageFont

        # 800x600のテスト画像を作成
        img = Image.new('RGB', (800, 600), color=(73, 109, 137))
        d = ImageDraw.Draw(img)

        # テキストを追加
        text = "K-TREND TIMES\nTest Image"
        d.text((400, 300), text, fill=(255, 255, 0), anchor="mm")

        # 保存
        test_image_path = "test_image.jpg"
        img.save(test_image_path, quality=90)

        print(f"✅ テスト画像を生成しました: {test_image_path}")
        return test_image_path

    except ImportError:
        print("⚠️  Pillowがインストールされていません")
        print("   pip install Pillow")
        print()
        print("   手動で画像ファイルを用意してください")
        return None


def test_1_local_file_upload():
    """テスト1: ローカルファイルから画像アップロード"""
    print("\n" + "━" * 60)
    print("テスト1: ローカルファイルから画像アップロード")
    print("━" * 60 + "\n")

    manager = StorageManager()

    # テスト画像を生成
    test_image = create_test_image()

    if not test_image:
        print("⏭️  スキップ: テスト画像がありません\n")
        return None

    # 画像をアップロード
    print("📤 WordPressに画像をアップロード中...")
    result = manager.upload_image_from_file(
        file_path=test_image,
        title="K-TREND TIMES テスト画像",
        credit="Test Credit / K-TREND TIMES"
    )

    if result:
        print(f"✅ アップロード成功！")
        print(f"   メディアID: {result['id']}")
        print(f"   画像URL: {result['url']}")
        print(f"   クレジット: {result.get('credit', 'なし')}")
        print()

        # クリーンアップ
        if os.path.exists(test_image):
            os.remove(test_image)

        return result
    else:
        print("❌ アップロード失敗")
        print()
        return None


def test_2_create_html_with_credit():
    """テスト2: クレジット付きHTMLの生成"""
    print("\n" + "━" * 60)
    print("テスト2: クレジット付きHTMLの生成")
    print("━" * 60 + "\n")

    manager = StorageManager()

    # テスト用のURL
    test_url = "https://k-trendtimes.com/wp-content/uploads/test.jpg"

    html = manager.create_image_with_credit_html(
        image_url=test_url,
        alt_text="BTSジミンの最新ビジュアル",
        credit="Photo by BigHit Music"
    )

    print("生成されたHTML:")
    print("─" * 60)
    print(html)
    print("─" * 60)
    print()

    return html


def test_3_create_article_with_image(image_data):
    """テスト3: 画像を含む記事を作成"""
    print("\n" + "━" * 60)
    print("テスト3: 画像を含む記事をドラフトとして保存")
    print("━" * 60 + "\n")

    if not image_data:
        print("⏭️  スキップ: 画像データがありません\n")
        return

    manager = StorageManager()

    # クレジット付きHTMLを生成
    image_html = manager.create_image_with_credit_html(
        image_url=image_data['url'],
        alt_text="テスト画像",
        credit=image_data.get('credit', '')
    )

    # 記事コンテンツを作成
    content = f"""
<p>これは画像クレジット機能のテスト記事です。</p>

{image_html}

<p>画像の下に「📷 Test Credit / K-TREND TIMES」というクレジットが表示されているはずです。</p>

<h2>クレジット表示の特徴</h2>
<ul>
<li>小さめのフォントサイズ</li>
<li>グレーの文字色</li>
<li>イタリック体</li>
<li>右寄せ</li>
<li>カメラの絵文字付き</li>
</ul>

<p>スマートフォンで見ると、さらに小さく表示されます。</p>
"""

    # ドラフトとして保存
    draft_data = {
        "title": "[テスト] 画像クレジット機能の確認",
        "content": content,
        "category": "trend",
        "meta_description": "画像クレジット機能のテスト記事です。",
        "image_url": image_data['url'],
    }

    print("📝 ドラフトを保存中...")
    draft_id = manager.save_draft(draft_data)

    print(f"✅ ドラフト保存完了！")
    print(f"   ドラフトID: {draft_id}")
    print()
    print("📋 確認方法:")
    print("   1. Firestore コンソールで確認:")
    print("      https://console.cloud.google.com/firestore")
    print(f"   2. コレクション: ktrend_drafts")
    print(f"   3. ドキュメント: {draft_id}")
    print()

    return draft_id


def test_4_verify_css():
    """テスト4: CSSが適用されているか確認"""
    print("\n" + "━" * 60)
    print("テスト4: CSS適用の確認")
    print("━" * 60 + "\n")

    print("📋 CSS確認手順:")
    print()
    print("1. WordPress サイトにアクセス:")
    print("   https://k-trendtimes.com")
    print()
    print("2. ブラウザの開発者ツールを開く (F12)")
    print()
    print("3. Elements タブで `.image-credit` を検索")
    print()
    print("4. 以下のスタイルが適用されているか確認:")
    print("   - font-size: 0.75rem")
    print("   - color: #666")
    print("   - font-style: italic")
    print("   - text-align: right")
    print()
    print("5. 適用されていない場合:")
    print("   → WordPress管理画面 → 外観 → カスタマイズ → 追加CSS")
    print("   → wordpress-image-credit-style.css の内容を貼り付け")
    print()


def main():
    """メイン実行"""
    print("\n" + "=" * 60)
    print("K-TREND TIMES 画像アップロード機能テスト")
    print("=" * 60)

    # WordPress設定確認
    wp_url = os.getenv("WORDPRESS_URL")
    wp_user = os.getenv("WORDPRESS_USER")
    wp_password = os.getenv("WORDPRESS_APP_PASSWORD")

    if not all([wp_url, wp_user, wp_password]):
        print("\n❌ エラー: WordPress設定が不足しています")
        print("   .envファイルに以下を設定してください:")
        print("   - WORDPRESS_URL")
        print("   - WORDPRESS_USER")
        print("   - WORDPRESS_APP_PASSWORD")
        print()
        sys.exit(1)

    print(f"\n✅ WordPress URL: {wp_url}")
    print(f"✅ WordPress User: {wp_user}")
    print()

    # テスト実行
    try:
        # テスト1: 画像アップロード
        image_data = test_1_local_file_upload()

        # テスト2: HTML生成
        test_2_create_html_with_credit()

        # テスト3: 記事作成
        test_3_create_article_with_image(image_data)

        # テスト4: CSS確認
        test_4_verify_css()

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("デバッグ情報:")
        print("  WordPress URL:", os.getenv("WORDPRESS_URL"))
        print("  WordPress User:", os.getenv("WORDPRESS_USER"))

    print("\n" + "=" * 60)
    print("✅ テスト完了")
    print("=" * 60 + "\n")

    print("📋 次のステップ:")
    print("   1. WordPress管理画面でドラフトを確認")
    print("   2. CSSが適用されているか確認")
    print("   3. 実際のサイトで表示を確認")
    print()


if __name__ == "__main__":
    main()
