# 画像アップロード＆クレジット表示ガイド

WordPressに画像を直接アップロードし、画像の下にクレジット（出典）を表示する機能の使い方

---

## 🎯 新機能

### ✨ できるようになったこと

1. **ローカルファイルから直接画像アップロード**
   - URLではなく、PC上の画像ファイルを直接アップロード可能
   - JPG, PNG, GIF, WebP 対応

2. **画像クレジット（出典）の自動表示**
   - 画像の下に小さく「Photo by...」などのクレジットを表示
   - WordPressのキャプション機能を使用

3. **記事内での画像挿入が簡単**
   - クレジット付きHTMLを自動生成
   - 複数画像も簡単に管理

---

## 📋 セットアップ

### 1. コード更新

`src/storage_manager.py` が更新されました。以下の関数が追加されています：

- `upload_image_from_file()` - ローカルファイルアップロード
- `create_image_with_credit_html()` - クレジット付きHTML生成
- `_update_media_metadata()` - メタデータ更新

### 2. WordPress CSS追加

画像クレジットを適切に表示するため、WordPressにCSSを追加します。

#### 方法A: WordPress管理画面から（推奨）

1. WordPress管理画面にログイン
2. **外観** → **カスタマイズ** → **追加CSS**
3. `wordpress-image-credit-style.css` の内容をコピー＆ペースト
4. 「公開」をクリック

#### 方法B: テーマファイルに直接追加

```bash
# サーバーにSSH接続
ssh your-server

# テーマのstyle.cssに追記
cat wordpress-image-credit-style.css >> /var/www/html/wp-content/themes/your-theme/style.css
```

---

## 🚀 使い方

### 基本的な使い方

#### 1. ローカル画像ファイルをアップロード

```python
from src.storage_manager import StorageManager

manager = StorageManager()

# 画像をアップロード
result = manager.upload_image_from_file(
    file_path="/path/to/your/image.jpg",
    title="画像の説明（ALTテキスト）",
    credit="Photo by Source Name"
)

# 結果
print(result)
# {
#   "id": 123,
#   "url": "https://k-trendtimes.com/wp-content/uploads/...",
#   "credit": "Photo by Source Name"
# }
```

#### 2. URLから画像をアップロード（クレジット付き）

```python
result = manager.upload_image_to_wordpress(
    image_url="https://example.com/image.jpg",
    title="画像の説明",
    credit="Photo by Photographer Name"
)
```

#### 3. クレジット付き画像HTMLを生成

```python
# 画像をアップロード
img = manager.upload_image_from_file(
    file_path="image.jpg",
    title="BTSジミンの最新ビジュアル",
    credit="Photo by BigHit Music"
)

# HTMLを生成
html = manager.create_image_with_credit_html(
    image_url=img['url'],
    alt_text="BTSジミンの最新ビジュアル",
    credit="Photo by BigHit Music"
)

print(html)
# <figure class="wp-block-image">
#     <img src="..." alt="BTSジミンの最新ビジュアル" />
#     <figcaption class="image-credit">Photo by BigHit Music</figcaption>
# </figure>
```

#### 4. 記事に画像を挿入

```python
# 1. 画像をアップロード
img1 = manager.upload_image_from_file(
    file_path="concert.jpg",
    title="コンサート会場の様子",
    credit="Photo by Music Bank / KBS"
)

# 2. HTMLを生成
img_html = manager.create_image_with_credit_html(
    image_url=img1['url'],
    alt_text="コンサート会場の様子",
    credit="Photo by Music Bank / KBS"
)

# 3. 記事コンテンツに埋め込む
content = f"""
<p>コンサートが盛況のうちに終了しました。</p>

{img_html}

<p>ファンからは感動の声が続出しています。</p>
"""

# 4. ドラフト保存または公開
draft_data = {
    "title": "コンサート大成功！",
    "content": content,
    "category": "event",
}

draft_id = manager.save_draft(draft_data)
```

---

## 📸 実践例

### 例1: 複数画像を含む記事

```python
manager = StorageManager()

# 画像1
img1 = manager.upload_image_from_file(
    "photo1.jpg",
    title="ステージ1",
    credit="Photo by HYBE"
)

# 画像2
img2 = manager.upload_image_from_file(
    "photo2.jpg",
    title="ステージ2",
    credit="Photo by Mnet"
)

# 記事作成
content = f"""
<p>今回のステージは2部構成でした。</p>

{manager.create_image_with_credit_html(img1['url'], img1['credit'])}

<p>第1部では...</p>

{manager.create_image_with_credit_html(img2['url'], img2['credit'])}

<p>第2部では...</p>
"""
```

### 例2: クレジットにリンクを含める

```python
credit_with_link = 'Photo by <a href="https://twitter.com/photographer">@photographer</a>'

html = manager.create_image_with_credit_html(
    image_url=img['url'],
    alt_text="画像説明",
    credit=credit_with_link
)
```

### 例3: 実際のワークフロー

```python
#!/usr/bin/env python3
"""記事作成ワークフロー例"""

from src.storage_manager import StorageManager
from src.notifier import LineNotifier

def create_article_with_images():
    manager = StorageManager()
    notifier = LineNotifier()

    # 1. 画像をアップロード
    print("📤 画像アップロード中...")
    featured_img = manager.upload_image_from_file(
        file_path="main_image.jpg",
        title="記事のメイン画像",
        credit="Photo by Source"
    )

    # 2. 記事コンテンツを作成
    content = f"""
<p>記事の導入部分...</p>

{manager.create_image_with_credit_html(
    featured_img['url'],
    featured_img.get('credit', '')
)}

<p>記事の本文...</p>
"""

    # 3. ドラフトとして保存
    draft_data = {
        "title": "新しい記事タイトル",
        "content": content,
        "category": "artist",
        "meta_description": "記事の説明文",
        "image_url": featured_img['url'],
    }

    draft_id = manager.save_draft(draft_data)
    print(f"✅ ドラフト保存: {draft_id}")

    # 4. LINE通知
    notifier.send_draft_notification(
        draft_id=draft_id,
        title=draft_data['title'],
        category=draft_data['category'],
        image_url=featured_img['url']
    )

    print("📱 LINE通知送信完了")

if __name__ == "__main__":
    create_article_with_images()
```

---

## 🎨 CSSカスタマイズ

### デフォルトスタイル

```css
.image-credit {
    font-size: 0.75rem;      /* 小さめ */
    color: #666;              /* グレー */
    font-style: italic;       /* イタリック */
    text-align: right;        /* 右寄せ */
}
```

### カスタマイズ例

#### 左寄せにする

```css
.image-credit {
    text-align: left;
}
```

#### 色を変更

```css
.image-credit {
    color: #999;              /* より薄いグレー */
}
```

#### 背景色を追加

```css
.image-credit {
    background: #f5f5f5;
    padding: 0.5rem;
    border-left: 3px solid #e0e0e0;
}
```

#### アイコンを変更

```css
.image-credit::before {
    content: "📸 ";           /* カメラアイコン */
    /* または */
    content: "© ";            /* コピーライト */
    /* または */
    content: "出典: ";        /* テキスト */
}
```

---

## 🔍 トラブルシューティング

### 画像がアップロードされない

**原因**: WordPressの認証情報が間違っている

**解決方法**:
```bash
# .envファイルを確認
cat .env | grep WORDPRESS

# 正しい値に更新
WORDPRESS_URL=https://k-trendtimes.com
WORDPRESS_USER=admin
WORDPRESS_APP_PASSWORD=your_app_password
```

### クレジットが表示されない

**原因**: CSSが適用されていない

**解決方法**:
1. WordPress管理画面 → 外観 → カスタマイズ → 追加CSS
2. `wordpress-image-credit-style.css` の内容を貼り付け
3. 「公開」をクリック

### 画像のサイズが大きすぎる

**解決方法**: アップロード前に画像を圧縮

```python
from PIL import Image

def compress_image(input_path, output_path, max_width=1200):
    """画像を圧縮"""
    img = Image.open(input_path)

    # リサイズ
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    # 保存（品質80%）
    img.save(output_path, quality=80, optimize=True)

# 使用例
compress_image("large_image.jpg", "compressed.jpg")

# 圧縮後の画像をアップロード
manager.upload_image_from_file("compressed.jpg", ...)
```

---

## 📝 よくある質問

### Q: 既存の画像にクレジットを追加できますか？

A: はい、メディアIDがわかれば可能です。

```python
manager._update_media_metadata(
    media_id=123,
    alt_text="画像の説明",
    credit="Photo by Source"
)
```

### Q: クレジットなしで画像をアップロードできますか？

A: はい、`credit` パラメータを省略してください。

```python
result = manager.upload_image_from_file(
    file_path="image.jpg",
    title="画像説明"
    # credit は省略
)
```

### Q: 一度に複数の画像をアップロードできますか？

A: はい、ループで処理できます。

```python
image_files = ["img1.jpg", "img2.jpg", "img3.jpg"]
results = []

for img_file in image_files:
    result = manager.upload_image_from_file(
        file_path=img_file,
        title=f"{img_file}の説明",
        credit="Photo by Source"
    )
    results.append(result)
```

---

## 🆘 サポート

問題が発生した場合:
1. `.env` ファイルの設定を確認
2. WordPress管理画面でメディアライブラリを確認
3. `example_image_upload_with_credit.py` を実行してテスト

---

## 📚 関連ファイル

- `src/storage_manager.py` - メイン機能
- `wordpress-image-credit-style.css` - CSS
- `example_image_upload_with_credit.py` - 使用例
- `IMAGE_UPLOAD_GUIDE.md` - このガイド
