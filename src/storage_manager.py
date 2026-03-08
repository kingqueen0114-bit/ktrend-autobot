"""Sanity CMS ストレージマネージャー

WordPress REST APIの代わりにSanity Mutations API / GROQ / Assets APIを使用。
ドラフト管理: drafts.{id} プレフィックスでSanityネイティブDraftを活用。
"""

import os
import re
import logging
import requests
import hmac
import hashlib
from io import BytesIO
from datetime import datetime

from google.cloud import firestore
from src import sanity_client
from src.portable_text_builder import markdown_to_portable_text
from utils.logging_config import log_event, log_error

logger = logging.getLogger(__name__)


def _sanitize_highlights(highlights) -> list:
    """highlights フィールドの型安全なサニタイズ"""
    if not isinstance(highlights, list):
        return []
    return [h for h in highlights if isinstance(h, str) and h.strip()]


# カテゴリマッピング（トレンドカテゴリ → Sanityカテゴリslug）
TREND_TO_CATEGORY = {
    "artist": "artist",
    "beauty": "beauty",
    "fashion": "fashion",
    "food": "gourmet",
    "travel": "koreantrip",
    "event": "event",
    "drama": "trend",
    "other": "trend",
}

# Sanityカテゴリslug一覧（旧CATEGORY_IDS互換）
CATEGORY_SLUGS = {
    "artist": "artist",
    "beauty": "beauty",
    "fashion": "fashion",
    "gourmet": "gourmet",
    "koreantrip": "koreantrip",
    "event": "event",
    "trend": "trend",
    "lifestyle": "lifestyle",
    "news": "trend",
    "interview": "lifestyle",
    "column": "lifestyle",
}

# 旧互換: get_wp_category_id → get_category_slug
def get_wp_category_id(trend_category: str) -> str:
    """トレンドカテゴリからSanityカテゴリslugを取得（旧互換関数名）"""
    wp_cat = TREND_TO_CATEGORY.get(trend_category, "trend")
    return CATEGORY_SLUGS.get(wp_cat, "trend")


# カテゴリ参照キャッシュ
_category_ref_cache = {}


class StorageManager:
    """Sanity CMS ストレージマネージャー"""

    def __init__(self):
        self.next_app_url = os.environ.get("NEXT_APP_URL", "https://k-trendtimes.com")
        self.edit_secret = os.environ.get("EDIT_SECRET", "")
        self.preview_secret = os.environ.get("PREVIEW_SECRET", "")

        # GCS (画像一時保存用、LINE画像アップロード用)
        self.gcs_bucket = os.environ.get("GCS_BUCKET", "ktrend-autobot-images")

        # Firestore
        self.collection_name = "article_drafts"
        self.logs_collection = "execution_logs"
        self.stats_collection = "daily_stats"
        self.sessions_collection = "edit_sessions"
        self.db = firestore.Client()

    def _get_category_ref(self, category_slug: str) -> str:
        """カテゴリslugからSanity参照IDを取得"""
        if category_slug in _category_ref_cache:
            return _category_ref_cache[category_slug]

        result = sanity_client.query_one(
            '*[_type == "category" && slug.current == $slug]{_id}',
            {"slug": category_slug}
        )

        if result:
            _category_ref_cache[category_slug] = result["_id"]
            return result["_id"]

        logger.warning(f"カテゴリが見つかりません: {category_slug}")
        return ""

    def _generate_edit_token(self, draft_id: str) -> str:
        """編集URL用のHMACトークンを生成"""
        if not self.edit_secret:
            return ""
        return hmac.new(
            self.edit_secret.encode(),
            draft_id.encode(),
            hashlib.sha256
        ).hexdigest()

    def get_or_create_tag(self, tag_name: str) -> str:
        """タグを検索し、なければ作成してSanity _idを返す"""
        tag_name = tag_name.strip()
        if not tag_name:
            return ""

        # slugを生成（小文字、スペースをハイフンに）
        slug = re.sub(r'[^\w\s-]', '', tag_name.lower())
        slug = re.sub(r'[\s]+', '-', slug).strip('-')

        # 既存タグを検索
        existing = sanity_client.query_one(
            '*[_type == "tag" && (title == $name || slug.current == $slug)]{_id}',
            {"name": tag_name, "slug": slug}
        )

        if existing:
            return existing["_id"]

        # 新規作成
        tag_id = sanity_client.generate_id()
        result = sanity_client.create({
            "_id": tag_id,
            "_type": "tag",
            "title": tag_name,
            "slug": {"_type": "slug", "current": slug},
        })

        logger.info(f"タグ作成: {tag_name} (id: {tag_id})")
        return tag_id

    def get_tag_refs(self, tag_names: list) -> list:
        """タグ名リストからSanity参照配列を返す"""
        refs = []
        for name in tag_names:
            if not name or not name.strip():
                continue
            tag_id = self.get_or_create_tag(name)
            if tag_id:
                refs.append({
                    "_type": "reference",
                    "_ref": tag_id,
                    "_key": sanity_client.generate_id()[:12],
                })
        return refs

    # 旧互換
    def get_tag_ids(self, tag_names: list) -> list:
        """旧互換: get_tag_refs のエイリアス"""
        return self.get_tag_refs(tag_names)

    def upload_image_to_sanity(self, image_url: str, title: str = "",
                               max_retries: int = 3) -> dict:
        """URLから画像をダウンロードしてSanity Assetsにアップロード

        Returns:
            {"id": asset_id, "url": asset_url, "ref": image_ref_object}
        """
        if not image_url:
            return {}

        result = sanity_client.upload_image_from_url(image_url, max_retries)
        if not result.get("_id"):
            # フォールバック画像
            fallback_urls = [
                "https://images.unsplash.com/photo-1617575521317-d2974f3b56d2?w=800",
                "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800",
            ]
            for fb_url in fallback_urls:
                result = sanity_client.upload_image_from_url(fb_url, 1)
                if result.get("_id"):
                    logger.info(f"フォールバック画像を使用: {fb_url}")
                    break

        if result.get("_id"):
            return {
                "id": result["_id"],
                "url": result.get("url", ""),
                "ref": sanity_client.image_ref(result["_id"]),
            }
        return {}

    # 旧互換
    def upload_image_to_wordpress(self, image_url: str, title: str = "",
                                  max_retries: int = 3) -> dict:
        """旧互換: upload_image_to_sanity のエイリアス"""
        result = self.upload_image_to_sanity(image_url, title, max_retries)
        return {"id": result.get("id", ""), "url": result.get("url", ""),
                "used_fallback": False}

    def save_draft_to_sanity(self, draft_data: dict, image_url: str = None,
                             additional_images: list = None, category: str = None,
                             artist_tags: list = None, doc_id: str = None) -> dict:
        """記事下書きをSanityに保存

        Args:
            draft_data: {"title": str, "body": str (Markdown/HTML), "meta_description": str, ...}
            image_url: アイキャッチ画像URL
            additional_images: 追加画像URL配列
            category: トレンドカテゴリ (artist/beauty/fashion/food/travel/event/drama/other)
            artist_tags: アーティストタグ名配列
            doc_id: 既存のIDを上書きする場合に指定

        Returns:
            {"id": draft_id, "preview_url": str, "edit_url": str, "slug": str}
        """
        if not doc_id:
            doc_id = sanity_client.generate_id()
        draft_id = f"drafts.{doc_id}"

        title = draft_data.get("title", "")
        body_text = draft_data.get("body", "")
        meta_description = draft_data.get("meta_description", "")

        # タイトルからslugを生成
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[\s]+', '-', slug).strip('-')[:200]
        if not slug:
            slug = doc_id[:20]

        # Markdown → Portable Text 変換
        body_pt = markdown_to_portable_text(body_text)

        # アイキャッチ画像アップロード
        main_image = None
        if image_url:
            img_result = self.upload_image_to_sanity(image_url, title)
            if img_result.get("ref"):
                main_image = img_result["ref"]
                main_image["alt"] = title

        # カテゴリ参照
        category_ref = None
        if category:
            cat_slug = TREND_TO_CATEGORY.get(category, category)
            cat_id = self._get_category_ref(cat_slug)
            if cat_id:
                category_ref = {"_type": "reference", "_ref": cat_id}

        # タグ参照
        tag_refs = []
        if artist_tags:
            tag_refs = self.get_tag_refs(artist_tags)

        # Sanityドキュメント構築
        doc = {
            "_id": draft_id,
            "_type": "article",
            "title": title,
            "slug": {"_type": "slug", "current": slug},
            "body": body_pt,
            "excerpt": meta_description,
            "seo": {
                "metaTitle": title,
                "metaDescription": meta_description,
            },
            "artistTags": artist_tags or [],
            "highlights": _sanitize_highlights(draft_data.get("highlights", [])),
            "qualityScore": draft_data.get("quality_score"),
            "xPost1": draft_data.get("x_post_1", ""),
            "xPost2": draft_data.get("x_post_2", ""),
            "newsPost": draft_data.get("news_post", ""),
            "lunaPostA": draft_data.get("luna_post_a", ""),
            "lunaPostB": draft_data.get("luna_post_b", ""),
            "sourceUrl": draft_data.get("source_url", ""),
            "researchReport": draft_data.get("research_report", ""),
        }

        if main_image:
            doc["mainImage"] = main_image
        if category_ref:
            doc["category"] = category_ref
        if tag_refs:
            doc["tags"] = tag_refs

        # None値を除去
        doc = {k: v for k, v in doc.items() if v is not None}

        # 既存のドキュメントがあればフェッチしてマージ (author, sources等の消失を防ぐ)
        existing_doc = sanity_client.query_one('*[_id == $id]{...}', {"id": draft_id})
        if not existing_doc:
            existing_doc = sanity_client.query_one('*[_id == $id]{...}', {"id": doc_id})
            
        if existing_doc:
            for key, value in existing_doc.items():
                if key not in doc and not key.startswith("_"):
                    doc[key] = value

        # Sanityに保存
        sanity_client.create_or_replace(doc)
        logger.info(f"Sanity下書き保存完了: {draft_id} - {title}")

        # URL生成
        edit_token = self._generate_edit_token(doc_id)
        edit_url = f"{self.next_app_url}/edit/{doc_id}?token={edit_token}"
        preview_url = f"{self.next_app_url}/api/preview?slug={slug}&secret={self.preview_secret}"

        return {
            "id": doc_id,
            "draft_id": draft_id,
            "preview_url": preview_url,
            "edit_url": edit_url,
            "slug": slug,
            "doc": doc
        }

    # 旧互換
    def save_draft_to_wordpress(self, draft_data: dict, image_url: str = None,
                                additional_images: list = None, category: str = None,
                                artist_tags: list = None) -> dict:
        """旧互換: save_draft_to_sanity のエイリアス"""
        return self.save_draft_to_sanity(
            draft_data, image_url, additional_images, category, artist_tags
        )

    def publish_to_sanity(self, draft_data: dict, image_url: str = None,
                          category: str = None, artist_tags: list = None,
                          wp_post_id: int = None, draft_id: str = None) -> dict:
        """記事をSanityで公開

        drafts.{id} → {id} にMutateして公開状態にする。

        Args:
            draft_data: CMS content dict
            image_url: アイキャッチ画像URL
            category: トレンドカテゴリ
            artist_tags: アーティストタグ
            wp_post_id: 旧互換パラメータ（使用しない）
            draft_id: SanityドラフトID（drafts.xxx or xxx）

        Returns:
            {"id": published_id, "url": public_url, "slug": slug}
        """
        import datetime
        
        target_doc_id = None
        if draft_id:
            target_doc_id = draft_id.replace("drafts.", "")
            
        # ドラフトまたは公開記事としてSanityに最新の編集内容を保存（ID指定）
        result = self.save_draft_to_sanity(
            draft_data, image_url, None, category, artist_tags, doc_id=target_doc_id
        )
        doc_id = result["id"]
        draft_id_full = f"drafts.{doc_id}"

        # save_draft_to_sanityで構築された完全なドキュメントを利用（クエリ遅延による空振りを防止）
        draft = result.get("doc")

        if draft:
            draft.pop("_rev", None)
            draft.pop("_updatedAt", None)
            draft.pop("_createdAt", None)
            
            # 既存の公開記事がある場合はその公開日時を維持する
            published_doc = sanity_client.query_one('*[_id == $id]{publishedAt}', {"id": doc_id})
            if published_doc and published_doc.get("publishedAt"):
                draft["publishedAt"] = published_doc["publishedAt"]
            else:
                draft["publishedAt"] = datetime.datetime.utcnow().isoformat() + "Z"

            mutations = [
                {"createOrReplace": {**draft, "_id": doc_id}},
                {"delete": {"id": draft_id_full}},
            ]
            sanity_client.transaction(mutations)

        slug = result.get("slug", doc_id)
        url = f"{self.next_app_url}/articles/{slug}"

        logger.info(f"Sanity公開完了（最新内容反映）: {doc_id}")
        return {"id": doc_id, "url": url, "slug": slug}

    # 旧互換
    def publish_to_wordpress(self, draft_data: dict, image_url: str = None,
                             category: str = None, artist_tags: list = None,
                             wp_post_id: int = None, draft_id: str = None) -> dict:
        """旧互換: publish_to_sanity のエイリアス"""
        return self.publish_to_sanity(
            draft_data, image_url, category, artist_tags, wp_post_id,
            draft_id=draft_id
        )

    def delete_sanity_draft(self, draft_id: str) -> bool:
        """Sanityドラフトを削除"""
        try:
            sanity_draft_id = draft_id if draft_id.startswith("drafts.") else f"drafts.{draft_id}"
            sanity_client.delete(sanity_draft_id)
            logger.info(f"Sanityドラフト削除: {sanity_draft_id}")
            return True
        except Exception as e:
            logger.error(f"Sanityドラフト削除失敗: {e}")
            return False

    # 旧互換
    def delete_wordpress_draft(self, wp_post_id: int) -> bool:
        """旧互換: Firestoreのdraft_idでSanityドラフトを削除"""
        # 旧呼び出しではwp_post_idが渡されるが、
        # Sanityでは直接使えないのでログだけ出す
        logger.warning(f"delete_wordpress_draft called with wp_post_id={wp_post_id}. "
                      f"Sanity移行後はdraft_idを使用してください。")
        return True

    def upload_bytes_to_gcs(self, image_data: bytes, content_type: str = "image/jpeg") -> str:
        """画像バイトをGCSにアップロード（LINE画像アップロード用、変更なし）"""
        try:
            from google.cloud import storage as gcs_storage
            client = gcs_storage.Client()
            bucket = client.bucket(self.gcs_bucket)
            import uuid as _uuid
            blob_name = f"uploads/{_uuid.uuid4().hex}.jpg"
            blob = bucket.blob(blob_name)
            blob.upload_from_string(image_data, content_type=content_type)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            logger.error(f"GCSアップロード失敗: {e}")
            return ""

    # ================================================================
    # Firestore メソッド群
    # ================================================================

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
            log_error("FIRESTORE_SAVE_ERROR", "Failed to save draft to Firestore", error=e)
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
            log_error("FIRESTORE_GET_ERROR", "Failed to get draft from Firestore", error=e)
            return None

    def create_blank_draft(self, user_id):
        """Creates a blank draft in Firestore for manual article creation."""
        try:
            doc_ref = self.db.collection(self.collection_name).document()
            article_data = {
                'created_at': firestore.SERVER_TIMESTAMP,
                'status': 'pending',
                'user_id': user_id,
                'cms_content': {
                    'title': '', 'body': '', 'meta_description': '',
                    'x_post_1': '', 'x_post_2': ''
                },
                'sns_content': {
                    'news_post': '', 'luna_post_a': '', 'luna_post_b': ''
                },
                'trend_source': {
                    'category': 'trend', 'image_url': '', 'artist_tags': []
                }
            }
            doc_ref.set(article_data)
            return doc_ref.id
        except Exception as e:
            log_error("FIRESTORE_CREATE_BLANK_ERROR", "Failed to create blank draft", error=e)
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
            log_event("FIRESTORE_SESSION_STORED", f"Edit session stored for user", edit_type=edit_type, draft_id=draft_id)
            return True
        except Exception as e:
            log_error("FIRESTORE_SESSION_STORE_ERROR", "Failed to store edit session", error=e)
            return False

    def get_edit_session(self, user_id: str) -> dict:
        """Get and clear an edit session for a user from Firestore."""
        try:
            doc_ref = self.db.collection(self.sessions_collection).document(user_id)

            @firestore.transactional
            def read_and_delete_session(transaction, ref):
                snapshot = ref.get(transaction=transaction)
                if snapshot.exists:
                    data = snapshot.to_dict()
                    transaction.delete(ref)
                    return data
                return None

            transaction = self.db.transaction()
            session = read_and_delete_session(transaction, doc_ref)

            if session:
                from datetime import datetime, timezone, timedelta
                session_time = session.get('timestamp')
                if session_time:
                    now = datetime.now(timezone.utc)
                    if now - session_time > timedelta(minutes=5):
                        log_event("FIRESTORE_SESSION_EXPIRED", "Edit session expired for user")
                        return None
                return session
            return None
        except Exception as e:
            log_error("FIRESTORE_SESSION_GET_ERROR", "Failed to get edit session", error=e)
            return None

    def log_execution(self, execution_data: dict) -> str:
        """Save execution log to Firestore."""
        try:
            execution_data['created_at'] = firestore.SERVER_TIMESTAMP
            doc_ref = self.db.collection(self.logs_collection).document()
            doc_ref.set(execution_data)
            log_event("FIRESTORE_LOG_SAVED", "Execution log saved", log_id=doc_ref.id)
            return doc_ref.id
        except Exception as e:
            log_error("FIRESTORE_LOG_SAVE_ERROR", "Failed to save execution log", error=e)
            return None

    def update_daily_stats(self, date_str: str, stats: dict) -> bool:
        """Update daily statistics in Firestore."""
        try:
            doc_ref = self.db.collection(self.stats_collection).document(date_str)
            doc = doc_ref.get()
            if doc.exists:
                existing = doc.to_dict()
                stats['total_trends'] = existing.get('total_trends', 0) + stats.get('total_trends', 0)
                stats['total_drafts'] = existing.get('total_drafts', 0) + stats.get('total_drafts', 0)
                stats['official_images'] = existing.get('official_images', 0) + stats.get('official_images', 0)
                stats['fallback_images'] = existing.get('fallback_images', 0) + stats.get('fallback_images', 0)
                existing_categories = existing.get('categories', {})
                new_categories = stats.get('categories', {})
                merged_categories = existing_categories.copy()
                for cat, count in new_categories.items():
                    merged_categories[cat] = merged_categories.get(cat, 0) + count
                stats['categories'] = merged_categories
            stats['updated_at'] = firestore.SERVER_TIMESTAMP
            doc_ref.set(stats, merge=True)
            log_event("FIRESTORE_STATS_UPDATED", f"Daily stats updated for {date_str}")
            return True
        except Exception as e:
            log_error("FIRESTORE_STATS_UPDATE_ERROR", "Failed to update daily stats", error=e)
            return False

    def increment_approval_stat(self, approved: bool = True) -> bool:
        """Increment approval or rejection count in daily stats."""
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            doc_ref = self.db.collection(self.stats_collection).document(date_str)
            field = 'approved_count' if approved else 'rejected_count'
            doc_ref.set({field: firestore.Increment(1)}, merge=True)
            log_event("FIRESTORE_APPROVAL_STAT", f"{'Approved' if approved else 'Rejected'} count incremented for {date_str}")
            return True
        except Exception as e:
            log_error("FIRESTORE_APPROVAL_STAT_ERROR", "Failed to increment approval stat", error=e)
            return False

    def get_stats_summary(self, days: int = 7) -> dict:
        """Get aggregated statistics summary for the given number of days."""
        try:
            from datetime import timedelta
            summary = {
                'total_trends': 0, 'total_drafts': 0, 'official_images': 0,
                'fallback_images': 0, 'days_collected': 0, 'categories': {},
                'approved_count': 0, 'rejected_count': 0
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
                    for cat, count in data.get('categories', {}).items():
                        summary['categories'][cat] = summary['categories'].get(cat, 0) + count
            total_images = summary['official_images'] + summary['fallback_images']
            summary['official_image_rate'] = (summary['official_images'] / total_images * 100) if total_images > 0 else 0
            total_decisions = summary['approved_count'] + summary['rejected_count']
            summary['approval_rate'] = (summary['approved_count'] / total_decisions * 100) if total_decisions > 0 else 0
            article_stats = self.get_article_performance(days)
            summary.update(article_stats)
            return summary
        except Exception as e:
            log_error("FIRESTORE_STATS_SUMMARY_ERROR", "Failed to get stats summary", error=e)
            return {}

    def get_best_articles(self, days: int = 7, limit: int = 3) -> list:
        """Get top-scoring approved articles."""
        try:
            articles_ref = self.db.collection(self.collection_name) \
                .where('status', '==', 'approved') \
                .order_by('quality_score', direction='DESCENDING') \
                .limit(limit * 2)
            best_articles = []
            for doc in articles_ref.stream():
                article = doc.to_dict()
                title = article.get('cms_content', {}).get('title', '無題')
                score = article.get('quality_score', 0)
                url = article.get('wordpress_url', '')
                category = article.get('trend_source', {}).get('category', 'other')
                if score >= 60:
                    best_articles.append({
                        'title': title[:35] + ('...' if len(title) > 35 else ''),
                        'score': score, 'url': url, 'category': category
                    })
                if len(best_articles) >= limit:
                    break
            return best_articles
        except Exception as e:
            log_error("FIRESTORE_BEST_ARTICLES_ERROR", "Failed to get best articles", error=e)
            return []

    def get_article_performance(self, days: int = 7) -> dict:
        """Get article performance metrics."""
        try:
            articles_ref = self.db.collection(self.collection_name) \
                .where('status', '==', 'approved') \
                .limit(100)
            total_published = 0
            total_quality_score = 0
            rewritten_count = 0
            scheduled_count = 0
            quality_scores = []
            for doc in articles_ref.stream():
                article = doc.to_dict()
                total_published += 1
                score = article.get('quality_score', 0)
                if score > 0:
                    quality_scores.append(score)
                    total_quality_score += score
                if article.get('was_rewritten'):
                    rewritten_count += 1
            scheduled_ref = self.db.collection(self.collection_name) \
                .where('status', '==', 'scheduled') \
                .limit(50)
            for doc in scheduled_ref.stream():
                scheduled_count += 1
            avg_quality = total_quality_score / len(quality_scores) if quality_scores else 0
            return {
                'total_published': total_published,
                'avg_quality_score': round(avg_quality, 1),
                'rewritten_count': rewritten_count,
                'scheduled_count': scheduled_count,
                'rewrite_rate': round(rewritten_count / total_published * 100, 1) if total_published > 0 else 0
            }
        except Exception as e:
            log_error("FIRESTORE_PERFORMANCE_ERROR", "Failed to get article performance", error=e)
            return {'total_published': 0, 'avg_quality_score': 0, 'rewritten_count': 0, 'scheduled_count': 0, 'rewrite_rate': 0}

    def save_trend_title(self, title: str, trend_data: dict = None) -> bool:
        """Save a trend title to Firestore for duplicate detection."""
        try:
            import hashlib as _hashlib
            title_hash = _hashlib.md5(title.encode()).hexdigest()[:12]
            doc_data = {
                'title': title,
                'created_at': datetime.now().isoformat(),
                'trend_data': trend_data or {}
            }
            self.db.collection('trend_titles').document(title_hash).set(doc_data)
            return True
        except Exception as e:
            log_error("FIRESTORE_TREND_SAVE_ERROR", "Failed to save trend title", error=e)
            return False

    def is_duplicate_trend(self, title: str, hours: int = 24) -> bool:
        """Check if a trend title is a duplicate within the given hours."""
        try:
            from datetime import timedelta
            cutoff = datetime.now() - timedelta(hours=hours)
            cutoff_str = cutoff.isoformat()
            docs = self.db.collection('trend_titles') \
                .where('created_at', '>=', cutoff_str) \
                .stream()
            for doc in docs:
                data = doc.to_dict()
                existing_title = data.get('title', '')
                similarity = self._calculate_title_similarity(title, existing_title)
                if similarity >= 0.6:
                    log_event("TREND_DUPLICATE_FOUND", f"Duplicate trend detected (similarity: {similarity:.0%})")
                    return True
            return False
        except Exception as e:
            log_error("TREND_DUPLICATE_CHECK_ERROR", "Failed to check duplicate trend", error=e)
            return False

    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Calculate Jaccard similarity between two titles."""
        if not title1 or not title2:
            return 0.0
        t1 = title1.lower().strip()
        t2 = title2.lower().strip()
        if t1 == t2:
            return 1.0
        words1 = set(t1.split())
        words2 = set(t2.split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0

    def cleanup_old_trend_titles(self, days: int = 7) -> int:
        """Clean up trend titles older than the specified number of days."""
        try:
            from datetime import timedelta
            cutoff = datetime.now() - timedelta(days=days)
            cutoff_str = cutoff.isoformat()
            docs = self.db.collection('trend_titles') \
                .where('created_at', '<', cutoff_str) \
                .stream()
            deleted = 0
            for doc in docs:
                doc.reference.delete()
                deleted += 1
            if deleted > 0:
                log_event("TREND_CLEANUP", f"Cleaned up {deleted} old trend titles")
            return deleted
        except Exception as e:
            log_error("TREND_CLEANUP_ERROR", "Failed to cleanup trend titles", error=e)
            return 0
