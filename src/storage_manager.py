import os
import re
import json
import base64
import requests
from datetime import datetime
from google.cloud import firestore
from google.cloud import storage
from google.oauth2.service_account import Credentials

# WordPressカテゴリslug → ID マッピング
CATEGORY_IDS = {
    "artist": 11,
    "beauty": 7,
    "fashion": 10,
    "gourmet": 6,
    "koreantrip": 4,
    "event": 5,
    "trend": 3,
    "news": 2,
    "interview": 8,
    "column": 9,
}

# トレンドカテゴリ → WordPressカテゴリマッピング
TREND_TO_WP_CATEGORY = {
    "artist": "artist",      # K-pop, アイドル
    "beauty": "beauty",      # コスメ、スキンケア
    "fashion": "fashion",    # ファッション
    "food": "gourmet",       # グルメ、カフェ
    "travel": "koreantrip",  # 韓国旅行
    "event": "event",        # イベント、コンサート
    "drama": "trend",        # ドラマ
    "other": "trend",        # その他
}


def get_wp_category_id(trend_category: str) -> int:
    """トレンドカテゴリからWordPressカテゴリIDを取得"""
    wp_category = TREND_TO_WP_CATEGORY.get(trend_category, "trend")
    return CATEGORY_IDS.get(wp_category, CATEGORY_IDS["trend"])

class StorageManager:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.bucket_name = "k-trend-autobot"
        self.collection_name = "article_drafts"
        self.logs_collection = "execution_logs"
        self.stats_collection = "daily_stats"
        self.sessions_collection = "edit_sessions"

        # WordPress設定
        self.wp_url = os.getenv("WORDPRESS_URL", "https://k-trendtimes.com")
        self.wp_user = os.getenv("WORDPRESS_USER", "admin")
        self.wp_app_password = os.getenv("WORDPRESS_APP_PASSWORD", "")

        # Load Credentials
        key_path = os.getenv("GCP_SA_KEY_PATH")
        creds = None

        scopes = [
            'https://www.googleapis.com/auth/cloud-platform',
        ]

        if key_path and os.path.exists(key_path):
             creds = Credentials.from_service_account_file(key_path, scopes=scopes)

        # Firestore & Storage
        self.db = firestore.Client(project=self.project_id, credentials=creds)
        self.storage_client = storage.Client(project=self.project_id, credentials=creds)
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def _get_wp_auth_header(self) -> dict:
        """WordPress Application Password認証ヘッダーを生成"""
        credentials = f"{self.wp_user}:{self.wp_app_password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded}",
        }


    def get_or_create_tag(self, tag_name: str) -> int:
        """
        WordPressでタグを取得または作成してIDを返す

        Args:
            tag_name: タグ名

        Returns:
            タグID（失敗時は None）
        """
        try:
            headers = self._get_wp_auth_header()

            # 1. 既存タグを検索
            search_response = requests.get(
                f"{self.wp_url}/wp-json/wp/v2/tags",
                headers=headers,
                params={"search": tag_name, "per_page": 10},
                timeout=30
            )

            if search_response.status_code == 200:
                existing_tags = search_response.json()
                for tag in existing_tags:
                    if tag.get('name', '').lower() == tag_name.lower():
                        print(f"📌 Found existing tag: {tag_name} (ID: {tag['id']})")
                        return tag['id']

            # 2. タグが見つからない場合は作成
            headers["Content-Type"] = "application/json"
            create_response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/tags",
                headers=headers,
                json={"name": tag_name},
                timeout=30
            )

            if create_response.status_code == 201:
                new_tag = create_response.json()
                print(f"✨ Created new tag: {tag_name} (ID: {new_tag['id']})")
                return new_tag['id']
            elif create_response.status_code == 400:
                # タグが既に存在する場合（term_existsエラー）
                error_data = create_response.json()
                if 'data' in error_data and 'term_id' in error_data.get('data', {}):
                    return error_data['data']['term_id']

            print(f"⚠️ Failed to create tag {tag_name}: {create_response.text}")
            return None

        except Exception as e:
            print(f"Tag error for '{tag_name}': {e}")
            return None

    def get_tag_ids(self, tag_names: list) -> list:
        """
        複数のタグ名からタグIDリストを取得

        Args:
            tag_names: タグ名のリスト

        Returns:
            タグIDのリスト
        """
        tag_ids = []
        for name in tag_names:
            name = name.strip()
            if name:
                tag_id = self.get_or_create_tag(name)
                if tag_id:
                    tag_ids.append(tag_id)
        return tag_ids

    def save_draft(self, article_data, draft_id=None):
        """Saves the generated article drafted by Gemini to Firestore."""
        try:
            if draft_id:
                doc_ref = self.db.collection(self.collection_name).document(draft_id)
            else:
                doc_ref = self.db.collection(self.collection_name).document()
            article_data['created_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.set(article_data)
            return doc_ref.id
        except Exception as e:
            print(f"Firestore Save Error: {e}")
            return None

    def get_draft(self, draft_id):
        """Retrieves draft from Firestore by ID."""
        try:
            doc_ref = self.db.collection(self.collection_name).document(draft_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            print(f"Firestore Get Error: {e}")
            return None

    def create_blank_draft(self, user_id):
        """Creates a blank draft in Firestore for manual article creation."""
        try:
            doc_ref = self.db.collection(self.collection_name).document()
            
            # Initial blank structure
            article_data = {
                'created_at': firestore.SERVER_TIMESTAMP,
                'status': 'pending',
                'user_id': user_id,
                'cms_content': {
                    'title': '',
                    'body': '',
                    'meta_description': '',
                    'x_post_1': '',
                    'x_post_2': ''
                },
                'sns_content': {
                    'news_post': '',
                    'luna_post_a': '',
                    'luna_post_b': ''
                },
                'trend_source': {
                    'category': 'trend',
                    'image_url': '',
                    'artist_tags': []
                }
            }
            
            doc_ref.set(article_data)
            return doc_ref.id
        except Exception as e:
            print(f"Firestore Create Blank Draft Error: {e}")
            return None

    def store_edit_session(self, user_id: str, draft_id: str, edit_type: str):
        """Store an edit session for a user in Firestore."""
        try:
            doc_ref = self.db.collection(self.sessions_collection).document(user_id)
            doc_ref.set({
                'draft_id': draft_id,
                'edit_type': edit_type,
                'timestamp': firestore.SERVER_TIMESTAMP
            })
            print(f"📝 Edit session stored for user {user_id[:10]}... (type: {edit_type}, draft: {draft_id})")
            return True
        except Exception as e:
            print(f"Firestore Store Edit Session Error: {e}")
            return False

    def get_edit_session(self, user_id: str) -> dict:
        """Get and clear an edit session for a user from Firestore."""
        try:
            doc_ref = self.db.collection(self.sessions_collection).document(user_id)
            
            # Using transaction to read and delete atomically
            @firestore.transactional
            def read_and_delete_session(transaction, ref):
                snapshot = ref.get(transaction=transaction)
                if snapshot.exists:
                    data = snapshot.to_dict()
                    # Delete the session after reading
                    transaction.delete(ref)
                    return data
                return None

            transaction = self.db.transaction()
            session = read_and_delete_session(transaction, doc_ref)
            
            if session:
                # Check expiration (5 minutes)
                from datetime import datetime, timezone, timedelta
                session_time = session.get('timestamp')
                if session_time:
                    # session_time is a DatetimeWithNanoseconds object
                    now = datetime.now(timezone.utc)
                    if now - session_time > timedelta(minutes=5):
                        print(f"⚠️ Edit session expired for user {user_id[:10]}...")
                        return None
                return session
            return None

        except Exception as e:
            print(f"Firestore Get Edit Session Error: {e}")
            return None

    def upload_image_to_gcs(self, image_url, filename_prefix="img", max_retries: int = 3):
        """Downloads image from URL and uploads to GCS with retry logic."""
        import time

        for attempt in range(max_retries):
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "image/*,*/*;q=0.8"
                }
                response = requests.get(image_url, stream=True, timeout=30, headers=headers)
                if response.status_code != 200:
                    print(f"Failed to download image: HTTP {response.status_code}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    return None

                ext = "jpg"
                if "png" in image_url: ext = "png"

                filename = f"{filename_prefix}_{int(datetime.now().timestamp())}.{ext}"
                blob = self.bucket.blob(filename)

                blob.upload_from_string(response.content, content_type=response.headers.get('Content-Type'))
                return blob.public_url
            except Exception as e:
                print(f"GCS Upload Error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return None
        return None

    def upload_bytes_to_gcs(self, image_data: bytes, content_type: str = "image/jpeg") -> str:
        """Uploads raw image bytes to GCS."""
        try:
            ext = "jpg"
            if "png" in content_type: ext = "png"

            filename = f"line_upload_{int(datetime.now().timestamp())}.{ext}"
            blob = self.bucket.blob(filename)

            blob.upload_from_string(image_data, content_type=content_type)
            return blob.public_url
        except Exception as e:
            print(f"GCS Byte Upload Error: {e}")
            return None

    def upload_image_to_wordpress(self, image_url: str, title: str = "", max_retries: int = 3) -> dict:
        """
        画像をWordPress Media Libraryにアップロード（リトライ付き）

        Args:
            image_url: 画像URL
            title: ALTテキスト用タイトル
            max_retries: 最大リトライ回数

        Returns:
            {"id": media_id, "url": media_url} または None
        """
        import time

        # Fallback images for when original fails
        fallback_images = [
            "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800",  # Concert
            "https://images.unsplash.com/photo-1517154421773-0529f29ea451?w=800",  # Seoul
            "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800",  # Cosmetics
        ]

        urls_to_try = [image_url] + fallback_images
        last_error = None

        for url_idx, current_url in enumerate(urls_to_try):
            if url_idx > 0:
                print(f"🔄 Trying fallback image {url_idx}: {current_url[:50]}...")

            for attempt in range(max_retries):
                try:
                    # 1. 画像をダウンロード（User-Agent付き）
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Accept": "image/*,*/*;q=0.8",
                        "Referer": "https://www.google.com/"
                    }
                    response = requests.get(current_url, timeout=30, headers=headers, allow_redirects=True)
                    response.raise_for_status()

                    # Check if we got actual image data
                    content_type = response.headers.get("Content-Type", "")
                    if "text/html" in content_type:
                        print(f"⚠️ Got HTML instead of image, skipping...")
                        break  # Try next URL

                    image_data = response.content
                    if len(image_data) < 1000:  # Too small to be a valid image
                        print(f"⚠️ Image data too small ({len(image_data)} bytes), skipping...")
                        break  # Try next URL

                    # Content-Typeから拡張子を推測
                    ext_map = {
                        "image/jpeg": ".jpg",
                        "image/png": ".png",
                        "image/gif": ".gif",
                        "image/webp": ".webp",
                    }
                    ext = ext_map.get(content_type.split(";")[0], ".jpg")

                    # ファイル名を生成
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ktrend_{timestamp}{ext}"

                    # 2. WordPress Media APIへアップロード
                    wp_headers = self._get_wp_auth_header()
                    wp_headers["Content-Type"] = content_type.split(";")[0] or "image/jpeg"
                    wp_headers["Content-Disposition"] = f'attachment; filename="{filename}"'

                    wp_response = requests.post(
                        f"{self.wp_url}/wp-json/wp/v2/media",
                        headers=wp_headers,
                        data=image_data,
                        timeout=60,
                    )
                    wp_response.raise_for_status()

                    media_data = wp_response.json()

                    # ALTテキストを設定
                    if title:
                        self._update_media_alt(media_data["id"], title)

                    print(f"✅ Image uploaded successfully (attempt {attempt + 1}, URL index {url_idx})")
                    return {
                        "id": media_data["id"],
                        "url": media_data.get("source_url", media_data.get("guid", {}).get("rendered", "")),
                        "used_fallback": url_idx > 0
                    }

                except requests.exceptions.HTTPError as e:
                    last_error = e
                    status_code = e.response.status_code if e.response else 0
                    print(f"⚠️ HTTP Error {status_code} (attempt {attempt + 1}/{max_retries})")

                    # 404/403 errors - don't retry, try next URL
                    if status_code in [404, 403, 401]:
                        break

                    # Other errors - retry with backoff
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        print(f"🔄 Retrying in {wait_time}s...")
                        time.sleep(wait_time)

                except requests.exceptions.Timeout as e:
                    last_error = e
                    print(f"⚠️ Timeout (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(2)

                except Exception as e:
                    last_error = e
                    print(f"⚠️ Error: {str(e)[:100]} (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(1)

        print(f"❌ All image upload attempts failed: {last_error}")
        return None

    def _update_media_alt(self, media_id: int, alt_text: str) -> bool:
        """メディアのALTテキストを更新"""
        try:
            headers = self._get_wp_auth_header()
            headers["Content-Type"] = "application/json"
            response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/media/{media_id}",
                headers=headers,
                json={"alt_text": alt_text},
                timeout=30,
            )
            response.raise_for_status()
            return True
        except Exception:
            return False

    def _enable_public_preview(self, post_id: int) -> str:
        """
        Public Post Previewプラグインを有効化してプレビューURLを取得

        Args:
            post_id: WordPress投稿ID

        Returns:
            プレビューURL または None
        """
        try:
            headers = self._get_wp_auth_header()
            headers["Content-Type"] = "application/json"

            # カスタムREST APIエンドポイントを使用してプレビューを有効化
            response = requests.post(
                f"{self.wp_url}/wp-json/public-preview/v1/enable/{post_id}",
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()
            preview_url = result.get("preview_url")

            if preview_url:
                print(f"Public Preview enabled: {preview_url}")
                return preview_url

            return None

        except Exception as e:
            print(f"Public Preview Enable Error: {e}")
            return None

    def publish_to_wordpress(self, draft_data: dict, image_url: str = None, category: str = None, artist_tags: list = None, wp_post_id: int = None) -> dict:
        """
        記事をWordPressに公開（REST API使用）

        Args:
            draft_data: CMS記事データ (title, body, meta_description等)
            image_url: アイキャッチ画像URL（オプション）
            category: カテゴリ（trend/artist/beauty等）
            artist_tags: アーティストタグのリスト（オプション）
            wp_post_id: 既存のWordPress下書き投稿ID（あればステータスを更新）

        Returns:
            {"id": post_id, "url": post_url} または None
        """
        try:
            # 1. 画像をWordPressにアップロード
            featured_media_id = None
            if image_url and not image_url.startswith("https://via.placeholder"):
                media_result = self.upload_image_to_wordpress(
                    image_url,
                    draft_data.get('title', '')
                )
                if media_result:
                    featured_media_id = media_result["id"]

            # 2. カテゴリを判定
            category_id = get_wp_category_id(category) if category else CATEGORY_IDS.get("trend", 3)
            print(f"📂 Publish Category: {category} → WordPress ID: {category_id}")

            # 3. タグIDを取得
            tag_ids = []
            if artist_tags:
                tag_ids = self.get_tag_ids(artist_tags)
                print(f"🏷️ Tags: {artist_tags} → IDs: {tag_ids}")

            # 4. 投稿データを構築
            meta_description = draft_data.get('meta_description', '')
            title = draft_data.get('title', '')

            post_data = {
                "title": title,
                "content": draft_data.get('body', ''),
                "status": "publish",
                "categories": [category_id],
                "excerpt": meta_description,
            }

            # タグを追加
            if tag_ids:
                post_data["tags"] = tag_ids

            # アイキャッチ画像
            if featured_media_id:
                post_data["featured_media"] = featured_media_id

            # 5. WordPress REST APIで投稿を作成または更新
            headers = self._get_wp_auth_header()
            headers["Content-Type"] = "application/json"

            if wp_post_id and wp_post_id != 999999:
                # 既存の下書きを公開に更新
                print(f"📝 Updating existing WordPress post {wp_post_id} to 'publish'...")
                response = requests.post(
                    f"{self.wp_url}/wp-json/wp/v2/posts/{wp_post_id}",
                    headers=headers,
                    json=post_data,
                    timeout=60,
                )
            else:
                # 新規投稿として作成
                print("📝 Creating new WordPress post as 'publish'...")
                response = requests.post(
                    f"{self.wp_url}/wp-json/wp/v2/posts",
                    headers=headers,
                    json=post_data,
                    timeout=60,
                )

            response.raise_for_status()
            post_result = response.json()
            post_id = post_result["id"]
            post_url = post_result.get("link", f"{self.wp_url}/?p={post_id}")

            print(f"✅ WordPress published! ID: {post_id}, URL: {post_url}")
            return {
                "id": post_id,
                "url": post_url,
                "slug": post_result.get("slug", ""),
            }

        except requests.exceptions.RequestException as e:
            print(f"WordPress Publish Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text[:500]}")
            return None
        except Exception as e:
            print(f"Unexpected WordPress Publish Error: {e}")
            return None

    def save_draft_to_wordpress(self, draft_data: dict, image_url: str = None, additional_images: list = None, category: str = None, artist_tags: list = None) -> dict:
        """
        記事をWordPressに下書きとして保存

        ⚠️ Application Password認証が無効のため、Firestoreのみに保存
        公開時に管理画面ログイン経由でWordPressに投稿作成

        Args:
            draft_data: CMS記事データ (title, body, meta_description等)
            image_url: アイキャッチ画像URL（オプション）
            additional_images: 追加画像URLのリスト（オプション）
            category: トレンドカテゴリ（artist/beauty/fashion等）
            artist_tags: アーティストタグのリスト（オプション）

        Returns:
            {"id": post_id, "preview_url": preview_url, "edit_url": edit_url} または None
        """
        try:
            # Helper function to check if image URL is valid
            def is_valid_image_url(url):
                return (
                    url and
                    not url.startswith("https://via.placeholder") and
                    "example.com" not in url and
                    "placeholder" not in url.lower()
                )

            # 1. アイキャッチ画像をWordPressにアップロード
            featured_media_id = None

            if is_valid_image_url(image_url):
                media_result = self.upload_image_to_wordpress(
                    image_url,
                    draft_data.get('title', '')
                )
                if media_result:
                    featured_media_id = media_result["id"]
                    print(f"✅ Featured image uploaded: Media ID {featured_media_id}")
                else:
                    print(f"⚠️ Featured image upload failed")
            else:
                print(f"⚠️ Invalid featured image URL: {image_url}, skipping")

            # 2. 追加画像をアップロードしてプレースホルダーを置換
            body_content = draft_data.get('body', '')

            if additional_images:
                for idx, add_img_url in enumerate(additional_images[:3]):  # Max 3 additional images
                    if is_valid_image_url(add_img_url):
                        add_media_result = self.upload_image_to_wordpress(
                            add_img_url,
                            f"{draft_data.get('title', '')} - 画像{idx + 1}"
                        )
                        if add_media_result:
                            # Create WordPress image block HTML
                            img_html = f'''
<figure class="wp-block-image size-large">
<img src="{add_media_result['url']}" alt="{draft_data.get('title', '')}"/>
</figure>
'''
                            # Replace placeholder with actual image
                            placeholder = f"[IMAGE_{idx + 1}]"
                            body_content = body_content.replace(placeholder, img_html)
                            print(f"✅ Additional image {idx + 1} uploaded: {add_media_result['url']}")
                        else:
                            # Remove placeholder if upload failed
                            body_content = body_content.replace(f"[IMAGE_{idx + 1}]", "")
                            print(f"⚠️ Additional image {idx + 1} upload failed")
                    else:
                        # Remove placeholder for invalid URLs
                        body_content = body_content.replace(f"[IMAGE_{idx + 1}]", "")

            # Remove any remaining placeholders
            import re
            body_content = re.sub(r'\[IMAGE_\d+\]', '', body_content)

            # 3. カテゴリを判定（トレンドカテゴリから自動マッピング）
            category_id = get_wp_category_id(category) if category else CATEGORY_IDS.get("trend", 3)
            print(f"📂 Category: {category} → WordPress ID: {category_id}")

            # 3.5 タグIDを取得
            tag_ids = []
            if artist_tags:
                tag_ids = self.get_tag_ids(artist_tags)
                print(f"🏷️ Tags: {artist_tags} → IDs: {tag_ids}")

            # 4. 投稿データを構築（下書きとして保存）
            meta_description = draft_data.get('meta_description', '')
            title = draft_data.get('title', '')

            post_data = {
                "title": title,
                "content": body_content,
                "status": "draft",
                "categories": [category_id],
                "excerpt": meta_description,
                # SEO メタデータ（Yoast SEO対応）
                "meta": {
                    "_yoast_wpseo_metadesc": meta_description,
                    "_yoast_wpseo_title": f"{title} | K-Trend Times",
                    "_yoast_wpseo_focuskw": category if category else "韓国トレンド",
                }
            }

            # タグを追加
            if tag_ids:
                post_data["tags"] = tag_ids

            if featured_media_id:
                post_data["featured_media"] = featured_media_id
                # OGP画像設定
                post_data["meta"]["_yoast_wpseo_opengraph-image-id"] = str(featured_media_id)

            # 5. WordPress Posts APIへPOST
            headers = self._get_wp_auth_header()
            headers["Content-Type"] = "application/json"

            response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/posts",
                headers=headers,
                json=post_data,
                timeout=60,
            )
            response.raise_for_status()

            post_result = response.json()
            post_id = post_result["id"]

            # Public Post Previewを有効化してプレビューURLを取得
            preview_url = self._enable_public_preview(post_id)
            if not preview_url:
                preview_url = f"{self.wp_url}/wp-admin/post.php?post={post_id}&action=edit"

            return {
                "id": post_id,
                "preview_url": preview_url,
                "edit_url": f"{self.wp_url}/wp-admin/post.php?post={post_id}&action=edit",
                "slug": post_result.get("slug", ""),
            }

        except requests.exceptions.RequestException as e:
            print(f"WordPress Draft Save Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"Unexpected WordPress Draft Error: {e}")
            return None


    def delete_wordpress_draft(self, wp_post_id: int) -> bool:
        """
        WordPressの下書きを削除

        Args:
            wp_post_id: WordPress投稿ID

        Returns:
            成功したかどうか
        """
        try:
            headers = self._get_wp_auth_header()

            response = requests.delete(
                f"{self.wp_url}/wp-json/wp/v2/posts/{wp_post_id}?force=true",
                headers=headers,
                timeout=60,
            )
            response.raise_for_status()
            return True

        except Exception as e:
            print(f"WordPress Delete Error: {e}")
            return False

    def log_execution(self, execution_data: dict) -> str:
        """
        実行ログをFirestoreに保存

        Args:
            execution_data: {
                'timestamp': datetime,
                'trends_fetched': int,
                'drafts_created': int,
                'images_uploaded': int,
                'errors': list,
                'duration_seconds': float
            }

        Returns:
            ログID
        """
        try:
            execution_data['created_at'] = firestore.SERVER_TIMESTAMP
            doc_ref = self.db.collection(self.logs_collection).document()
            doc_ref.set(execution_data)
            print(f"📝 Execution log saved: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            print(f"Failed to save execution log: {e}")
            return None

    def update_daily_stats(self, date_str: str, stats: dict) -> bool:
        """
        日次統計を更新

        Args:
            date_str: 日付 (YYYY-MM-DD)
            stats: {
                'total_trends': int,
                'total_drafts': int,
                'official_images': int,
                'fallback_images': int,
                'categories': dict
            }

        Returns:
            成功したかどうか
        """
        try:
            doc_ref = self.db.collection(self.stats_collection).document(date_str)
            doc = doc_ref.get()

            if doc.exists:
                # 既存の統計を更新
                existing = doc.to_dict()
                stats['total_trends'] = existing.get('total_trends', 0) + stats.get('total_trends', 0)
                stats['total_drafts'] = existing.get('total_drafts', 0) + stats.get('total_drafts', 0)
                stats['official_images'] = existing.get('official_images', 0) + stats.get('official_images', 0)
                stats['fallback_images'] = existing.get('fallback_images', 0) + stats.get('fallback_images', 0)

                # Merge category counts
                existing_categories = existing.get('categories', {})
                new_categories = stats.get('categories', {})
                merged_categories = existing_categories.copy()
                for cat, count in new_categories.items():
                    merged_categories[cat] = merged_categories.get(cat, 0) + count
                stats['categories'] = merged_categories

            stats['updated_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.set(stats, merge=True)
            print(f"📊 Daily stats updated for {date_str}")
            return True
        except Exception as e:
            print(f"Failed to update daily stats: {e}")
            return False

    def increment_approval_stat(self, approved: bool = True) -> bool:
        """
        承認/却下の統計をインクリメント

        Args:
            approved: True=承認, False=却下

        Returns:
            成功したかどうか
        """
        try:
            from datetime import datetime
            date_str = datetime.now().strftime('%Y-%m-%d')
            doc_ref = self.db.collection(self.stats_collection).document(date_str)

            field = 'approved_count' if approved else 'rejected_count'
            doc_ref.set({field: firestore.Increment(1)}, merge=True)
            print(f"📊 {'Approved' if approved else 'Rejected'} count incremented for {date_str}")
            return True
        except Exception as e:
            print(f"Failed to increment approval stat: {e}")
            return False

    def get_stats_summary(self, days: int = 7) -> dict:
        """
        直近N日間の統計サマリーを取得

        Args:
            days: 取得する日数

        Returns:
            統計サマリー
        """
        try:
            from datetime import datetime, timedelta

            summary = {
                'total_trends': 0,
                'total_drafts': 0,
                'official_images': 0,
                'fallback_images': 0,
                'days_collected': 0,
                'categories': {},
                'approved_count': 0,
                'rejected_count': 0
            }

            for i in range(days):
                date_str = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                doc = self.db.collection(self.stats_collection).document(date_str).get()

                if doc.exists:
                    data = doc.to_dict()
                    summary['total_trends'] += data.get('total_trends', 0)
                    summary['total_drafts'] += data.get('total_drafts', 0)
                    summary['official_images'] += data.get('official_images', 0)
                    summary['fallback_images'] += data.get('fallback_images', 0)
                    summary['approved_count'] += data.get('approved_count', 0)
                    summary['rejected_count'] += data.get('rejected_count', 0)
                    summary['days_collected'] += 1

                    # Aggregate categories
                    for cat, count in data.get('categories', {}).items():
                        summary['categories'][cat] = summary['categories'].get(cat, 0) + count

            # 画像成功率を計算
            total_images = summary['official_images'] + summary['fallback_images']
            summary['official_image_rate'] = (summary['official_images'] / total_images * 100) if total_images > 0 else 0

            # 承認率を計算
            total_decisions = summary['approved_count'] + summary['rejected_count']
            summary['approval_rate'] = (summary['approved_count'] / total_decisions * 100) if total_decisions > 0 else 0

            # Get article performance data
            article_stats = self.get_article_performance(days)
            summary.update(article_stats)

            return summary
        except Exception as e:
            print(f"Failed to get stats summary: {e}")
            return {}

    def get_best_articles(self, days: int = 7, limit: int = 3) -> list:
        """
        Get the best performing articles from the past N days.

        Args:
            days: Number of days to look back
            limit: Maximum number of articles to return

        Returns:
            List of best articles with title, score, url, category
        """
        try:
            from datetime import datetime, timedelta

            # Get approved articles sorted by quality score
            articles_ref = self.db.collection(self.collection_name) \
                .where('status', '==', 'approved') \
                .order_by('quality_score', direction='DESCENDING') \
                .limit(limit * 2)  # Get more to filter

            best_articles = []
            for doc in articles_ref.stream():
                article = doc.to_dict()
                title = article.get('cms_content', {}).get('title', '無題')
                score = article.get('quality_score', 0)
                url = article.get('wordpress_url', '')
                category = article.get('trend_source', {}).get('category', 'other')

                if score >= 60:  # Only include articles with decent quality
                    best_articles.append({
                        'title': title[:35] + ('...' if len(title) > 35 else ''),
                        'score': score,
                        'url': url,
                        'category': category
                    })

                if len(best_articles) >= limit:
                    break

            return best_articles

        except Exception as e:
            print(f"Failed to get best articles: {e}")
            return []

    def get_article_performance(self, days: int = 7) -> dict:
        """
        Get article performance statistics.

        Args:
            days: Number of days to look back

        Returns:
            Dictionary with performance stats
        """
        try:
            from datetime import datetime, timedelta

            cutoff = datetime.now() - timedelta(days=days)

            # Get recent approved articles
            articles_ref = self.db.collection(self.collection_name) \
                .where('status', '==', 'approved') \
                .limit(100)

            articles = list(articles_ref.stream())

            total_published = 0
            total_quality_score = 0
            rewritten_count = 0
            scheduled_count = 0
            quality_scores = []

            for doc in articles:
                article = doc.to_dict()
                total_published += 1

                # Quality score
                score = article.get('quality_score', 0)
                if score > 0:
                    quality_scores.append(score)
                    total_quality_score += score

                # Rewritten articles
                if article.get('was_rewritten'):
                    rewritten_count += 1

            # Also check scheduled articles
            scheduled_ref = self.db.collection(self.collection_name) \
                .where('status', '==', 'scheduled') \
                .limit(50)

            for doc in scheduled_ref.stream():
                scheduled_count += 1

            # Calculate averages
            avg_quality = total_quality_score / len(quality_scores) if quality_scores else 0

            return {
                'total_published': total_published,
                'avg_quality_score': round(avg_quality, 1),
                'rewritten_count': rewritten_count,
                'scheduled_count': scheduled_count,
                'rewrite_rate': round(rewritten_count / total_published * 100, 1) if total_published > 0 else 0
            }

        except Exception as e:
            print(f"Failed to get article performance: {e}")
            return {
                'total_published': 0,
                'avg_quality_score': 0,
                'rewritten_count': 0,
                'scheduled_count': 0,
                'rewrite_rate': 0
            }

    def save_trend_title(self, title: str, trend_data: dict = None) -> bool:
        """
        Save a trend title to track for duplicate detection.

        Args:
            title: The trend title to save
            trend_data: Optional additional trend data

        Returns:
            True if saved successfully
        """
        try:
            from datetime import datetime
            import hashlib

            # Create a hash of the title for the document ID
            title_hash = hashlib.md5(title.encode()).hexdigest()[:12]

            doc_data = {
                'title': title,
                'created_at': datetime.now().isoformat(),
                'trend_data': trend_data or {}
            }

            self.db.collection('trend_titles').document(title_hash).set(doc_data)
            return True
        except Exception as e:
            print(f"Failed to save trend title: {e}")
            return False

    def is_duplicate_trend(self, title: str, hours: int = 24) -> bool:
        """
        Check if a similar trend title exists within the specified hours.

        Args:
            title: The trend title to check
            hours: Number of hours to look back (default 24)

        Returns:
            True if a similar trend exists
        """
        try:
            from datetime import datetime, timedelta

            # Calculate cutoff time
            cutoff = datetime.now() - timedelta(hours=hours)
            cutoff_str = cutoff.isoformat()

            # Get recent trend titles
            docs = self.db.collection('trend_titles') \
                .where('created_at', '>=', cutoff_str) \
                .stream()

            # Check for similarity
            for doc in docs:
                data = doc.to_dict()
                existing_title = data.get('title', '')

                # Calculate similarity
                similarity = self._calculate_title_similarity(title, existing_title)
                if similarity >= 0.6:  # 60% similarity threshold
                    print(f"🔄 Duplicate found: '{title[:30]}...' ≈ '{existing_title[:30]}...' ({similarity:.0%})")
                    return True

            return False
        except Exception as e:
            print(f"Failed to check duplicate: {e}")
            return False

    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Calculate word overlap similarity between two titles."""
        if not title1 or not title2:
            return 0.0

        # Normalize titles
        t1 = title1.lower().strip()
        t2 = title2.lower().strip()

        if t1 == t2:
            return 1.0

        # Word overlap similarity
        words1 = set(t1.split())
        words2 = set(t2.split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0

    def cleanup_old_trend_titles(self, days: int = 7) -> int:
        """
        Remove trend titles older than specified days.

        Args:
            days: Number of days to keep (default 7)

        Returns:
            Number of deleted documents
        """
        try:
            from datetime import datetime, timedelta

            cutoff = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff.isoformat()

            # Get old documents
            docs = self.db.collection('trend_titles') \
                .where('created_at', '<', cutoff_str) \
                .stream()

            deleted = 0
            for doc in docs:
                doc.reference.delete()
                deleted += 1

            if deleted > 0:
                print(f"🗑️ Cleaned up {deleted} old trend titles")

            return deleted
        except Exception as e:
            print(f"Failed to cleanup trend titles: {e}")
            return 0
