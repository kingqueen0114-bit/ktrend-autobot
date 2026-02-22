#!/usr/bin/env python3
"""
K-TREND TIMES 画像アップロード＆クレジット表示の使用例
"""

import os
from dotenv import load_dotenv
from src.storage_manager import StorageManager

# 環境変数読み込み
load_dotenv()


def example_1_upload_local_image():
    """例1: ローカル画像ファイルを直接アップロード"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("例1: ローカル画像を直接アップロード")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    manager = StorageManager()

    # ローカルの画像ファイルをアップロード
    image_path = "path/to/your/image.jpg"  # ← あなたの画像ファイルパス

    if not os.path.exists(image_path):
        print(f"❌ エラー: 画像ファイルが見つかりません: {image_path}")
        print("   実際の画像ファイルパスを指定してください\n")
        return

    result = manager.upload_image_from_file(
        file_path=image_path,
        title="BTSジミンの最新ビジュアル",
        credit="Photo by BigHit Music"
    )

    if result:
        print(f"✅ アップロード成功！")
        print(f"   メディアID: {result['id']}")
        print(f"   画像URL: {result['url']}")
        print(f"   クレジット: {result['credit']}")
        print()
    else:
        print("❌ アップロード失敗\n")


def example_2_upload_url_image():
    """例2: URL指定で画像をアップロード（既存機能＋クレジット）"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("例2: URL指定で画像をアップロード")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    manager = StorageManager()

    # URLから画像をアップロード
    image_url = "https://example.com/image.jpg"  # ← 実際の画像URL

    result = manager.upload_image_to_wordpress(
        image_url=image_url,
        title="ニュージーンズのカムバックステージ",
        credit="Photo by ADOR / Mnet"
    )

    if result:
        print(f"✅ アップロード成功！")
        print(f"   メディアID: {result['id']}")
        print(f"   画像URL: {result['url']}")
        print(f"   クレジット: {result['credit']}")
        print()
    else:
        print("❌ アップロード失敗\n")


def example_3_create_article_with_images():
    """例3: クレジット付き画像を含む記事を作成"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("例3: クレジット付き画像を含む記事作成")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    manager = StorageManager()

    # 画像1をアップロード
    image1_path = "path/to/image1.jpg"

    if not os.path.exists(image1_path):
        print(f"⚠️  画像ファイルが見つからないため、スキップします")
        print(f"   実際の画像パスに変更してください: {image1_path}\n")
        return

    print("📤 画像1をアップロード中...")
    img1 = manager.upload_image_from_file(
        file_path=image1_path,
        title="SEVENTEEN ホシのソロステージ",
        credit="Photo by Pledis Entertainment"
    )

    if not img1:
        print("❌ 画像アップロード失敗\n")
        return

    print(f"✅ 画像1アップロード完了 (ID: {img1['id']})\n")

    # クレジット付き画像HTMLを生成
    image_html = manager.create_image_with_credit_html(
        image_url=img1['url'],
        alt_text="SEVENTEEN ホシのソロステージ",
        credit="Photo by Pledis Entertainment"
    )

    # 記事コンテンツを作成
    article_content = f"""
<p>SEVENTEENのホシが、新曲「Spider」のソロステージで圧倒的なパフォーマンスを披露しました。</p>

{image_html}

<p>この日のステージでは、ホシ特有のパワフルなダンスと情熱的な歌声が会場を魅了しました。</p>

<h2>ファンの反応</h2>
<p>SNSでは「ホシのパフォーマンスが鳥肌もの」「さすがパフォーマンスチームリーダー」などの絶賛の声が相次いでいます。</p>
"""

    # 記事をドラフトとして保存
    draft_data = {
        "title": "SEVENTEEN ホシ、新曲「Spider」のソロステージで魅了",
        "content": article_content,
        "category": "artist",
        "meta_description": "SEVENTEENのホシが新曲ソロステージで圧倒的なパフォーマンスを披露。ファンから絶賛の声が続出。",
    }

    draft_id = manager.save_draft(draft_data)
    print(f"✅ ドラフト保存完了！")
    print(f"   ドラフトID: {draft_id}")
    print(f"   画像クレジットが記事内に含まれています")
    print()


def example_4_multiple_images_in_article():
    """例4: 複数の画像（それぞれクレジット付き）を含む記事"""
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("例4: 複数画像を含む記事（各画像にクレジット）")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    manager = StorageManager()

    # 記事コンテンツの構築例
    images_data = [
        {
            "url": "https://example.com/img1.jpg",
            "alt": "LE SSERAFIMのステージ",
            "credit": "Photo by Source Music"
        },
        {
            "url": "https://example.com/img2.jpg",
            "alt": "ファンとの交流シーン",
            "credit": "Photo by Music Bank / KBS"
        },
    ]

    article_parts = [
        "<p>LE SSERAFIMが音楽番組でカムバックステージを披露しました。</p>",
    ]

    # 各画像のHTMLを生成
    for img_data in images_data:
        image_html = manager.create_image_with_credit_html(
            image_url=img_data["url"],
            alt_text=img_data["alt"],
            credit=img_data["credit"]
        )
        article_parts.append(image_html)
        article_parts.append(f"<p>{img_data['alt']}の詳細...</p>")

    content = "\n\n".join(article_parts)

    print("✅ 複数画像を含む記事コンテンツを生成しました")
    print(f"   画像数: {len(images_data)}")
    print(f"   各画像にクレジットが付いています")
    print()
    print("生成されたHTML（抜粋）:")
    print("─" * 50)
    print(content[:500] + "...")
    print("─" * 50)
    print()


def main():
    """メイン実行"""
    print("\n" + "=" * 60)
    print("K-TREND TIMES 画像アップロード＆クレジット表示")
    print("使用例デモ")
    print("=" * 60 + "\n")

    # 実行する例を選択（コメントアウトを外して実行）

    # example_1_upload_local_image()      # ローカル画像アップロード
    # example_2_upload_url_image()        # URL指定アップロード
    # example_3_create_article_with_images()  # 記事作成例
    example_4_multiple_images_in_article()  # 複数画像の記事例

    print("=" * 60)
    print("✅ デモ完了")
    print("=" * 60 + "\n")

    print("💡 使い方:")
    print("   1. 画像ファイルパスを実際のパスに変更")
    print("   2. 実行したい example 関数のコメントアウトを外す")
    print("   3. python example_image_upload_with_credit.py を実行")
    print()


if __name__ == "__main__":
    main()
