"""
Generation action handlers for K-Trend AutoBot.
Handles creating new articles via text, image, and category requests.
"""
import os
from datetime import datetime
from utils.logging_config import log_event, log_error

def process_ondemand_text(topic, line_bot_api, user_id):
    """Handles text-based triggered generation"""
    from src.fetch_trends import TrendFetcher
    from src.content_generator import ContentGenerator, check_article_quality
    from src.notifier import Notifier
    from src.storage_manager import StorageManager

    try:
        fetcher = TrendFetcher(os.environ.get("GEMINI_API_KEY"))
        generator = ContentGenerator(os.environ.get("GEMINI_API_KEY"))
        notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
        storage = StorageManager()

        clean_topic = topic
        for prefix in ["記事: ", "記事:", "記事：", "記事 "]:
            if clean_topic.startswith(prefix):
                clean_topic = clean_topic[len(prefix):].strip()
                break

        trends = fetcher.fetch_trends(topic=clean_topic)
        if not trends:
            log_event("ONDEMAND_TEXT_NO_TRENDS", "No trends found for topic", topic=clean_topic)
            return

        target = trends[0]
        sns_content = generator.generate_content(target)
        cms_content = generator.generate_cms_article(target)

        quality = check_article_quality(cms_content, target)
        log_event("QUALITY_CHECK", f"Quality score: {quality['score']}/100", score=quality['score'])
        rewritten = False
        if not quality['passed'] and quality['warnings']:
            log_event("ARTICLE_REWRITE", "Auto-rewriting article", warnings=quality['warnings'])
            cms_content = generator.rewrite_article(cms_content, quality['warnings'], target)
            quality = check_article_quality(cms_content, target)
            rewritten = True

        img_url = target.get('image_url')
        trend_category = target.get('category', 'other')
        artist_tags = cms_content.get('artist_tags', [])
        if artist_tags:
            target['artist_tags'] = artist_tags
            log_event("ARTIST_TAGS_EXTRACTED", "Artist tags extracted", tags=artist_tags)
        wp_result = storage.save_draft_to_wordpress(cms_content, img_url, None, trend_category, artist_tags)

        draft_data = {
            "status": "draft",
            "trend_source": target,
            "sns_content": sns_content,
            "cms_content": cms_content,
            "quality_score": quality['score'],
            "quality_passed": quality['passed'],
            "quality_warnings": quality['warnings'],
            "was_rewritten": rewritten,
            "wordpress_post_id": wp_result["id"] if wp_result else None,
            "wordpress_preview_url": wp_result.get("preview_url") if wp_result else None,
        }
        draft_id = storage.save_draft(draft_data)

        notifier.send_approval_request(
             content={**sns_content, **cms_content},
             image_url=img_url,
             draft_id=draft_id,
             wp_post_id=wp_result["id"] if wp_result else None,
             wp_preview_url=wp_result.get("preview_url") if wp_result else None,
             quality_data={
                 'score': quality['score'],
                 'passed': quality['passed'],
                 'warnings': quality['warnings'],
                 'was_rewritten': rewritten
             },
             slug=wp_result.get("slug") if wp_result else None
        )
        log_event("ONDEMAND_TEXT_COMPLETE", "On-demand text process complete", draft_id=draft_id)

    except Exception as e:
        log_error("ONDEMAND_TEXT_ERROR", "On-demand text generation failed", error=e)
        try:
            notifier.send_error_notification(
                error_type="ONDEMAND_TEXT_ERROR",
                error_message=str(e),
                context=f"トピック: {topic[:50]}"
            )
        except:
            pass

def process_ondemand_image(image_bytes, line_bot_api, user_id):
    """Handles image-based triggered generation - not yet migrated to Sanity architecture."""
    from src.notifier import Notifier

    try:
        log_event("ONDEMAND_IMAGE_UNSUPPORTED", "Image-based generation not yet migrated to Sanity architecture")
        notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
        notifier.send_error_notification(
            error_type="IMAGE_GENERATION_UNSUPPORTED",
            error_message="画像からの記事生成はSanity移行後、まだ未対応です。テキストで記事トピックを送信してください。",
            context="画像メッセージ受信"
        )
    except Exception as e:
        log_error("ONDEMAND_IMAGE_ERROR", "Failed to send unsupported notification", error=e)

def process_category_generate(category, line_bot_api, reply_token, user_id):
    """Generate article for a specific category selected by user."""
    from src.fetch_trends import TrendFetcher
    from src.content_generator import ContentGenerator, check_article_quality
    from src.notifier import Notifier
    from src.storage_manager import StorageManager
    from linebot.models import TextMessage

    category_topics = {
        'artist': 'K-pop アイドル 最新ニュース カムバック',
        'beauty': '韓国コスメ 新作 スキンケア',
        'fashion': '韓国ファッション トレンド',
        'food': '韓国グルメ カフェ おすすめ',
        'travel': '韓国旅行 ソウル おすすめスポット',
        'event': 'K-pop コンサート イベント',
        'other': '韓国エンタメ トレンド'
    }
    category_names = {
        'artist': 'K-pop', 'beauty': 'コスメ', 'fashion': 'ファッション',
        'food': 'グルメ', 'travel': '旅行', 'event': 'イベント', 'other': 'トレンド'
    }

    try:
        line_bot_api.reply_message(
            reply_token,
            TextMessage(text=f"🔍 {category_names.get(category, category)}の最新記事を生成中...")
        )

        fetcher = TrendFetcher(os.environ.get("GEMINI_API_KEY"))
        generator = ContentGenerator(os.environ.get("GEMINI_API_KEY"))
        notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
        storage = StorageManager()

        year = datetime.now().strftime("%Y")
        topic = f"{category_topics.get(category, category_topics['other'])} {year}"

        trends = fetcher.fetch_trends(topic=topic)
        if not trends:
            notifier.send_error_notification("CATEGORY_NO_TRENDS", f"{category}のトレンドが見つかりませんでした", "")
            return

        trends = [t for t in trends if not storage.is_duplicate_trend(t.get('title', ''))]
        if not trends:
            notifier.send_error_notification("CATEGORY_ALL_DUPLICATES", f"{category}のトレンドがすべて既出でした", "")
            return

        target = trends[0]
        target['category'] = category

        sns_content = generator.generate_content(target)
        cms_content = generator.generate_cms_article(target)

        quality = check_article_quality(cms_content, target)
        rewritten = False
        if not quality['passed'] and quality['warnings']:
            cms_content = generator.rewrite_article(cms_content, quality['warnings'], target)
            quality = check_article_quality(cms_content, target)
            rewritten = True

        img_url = target.get('image_url')
        additional_images = target.get('additional_images', [])
        artist_tags = cms_content.get('artist_tags', [])
        if artist_tags:
            target['artist_tags'] = artist_tags
            log_event("ARTIST_TAGS_EXTRACTED", "Artist tags extracted", tags=artist_tags, category=category)
        wp_result = storage.save_draft_to_wordpress(cms_content, img_url, additional_images, category, artist_tags)

        draft_data = {
            "status": "draft",
            "trend_source": target,
            "sns_content": sns_content,
            "cms_content": cms_content,
            "quality_score": quality['score'],
            "quality_passed": quality['passed'],
            "quality_warnings": quality['warnings'],
            "was_rewritten": rewritten,
            "category": category,
            "wordpress_post_id": wp_result["id"] if wp_result else None,
            "wordpress_preview_url": wp_result.get("preview_url") if wp_result else None,
        }
        draft_id = storage.save_draft(draft_data)
        storage.save_trend_title(target.get('title', ''), {'draft_id': draft_id, 'category': category})

        notifier.send_approval_request(
            content={**sns_content, **cms_content},
            image_url=img_url,
            draft_id=draft_id,
            wp_post_id=wp_result["id"] if wp_result else None,
            wp_preview_url=wp_result.get("preview_url") if wp_result else None,
            quality_data={
                'score': quality['score'],
                'passed': quality['passed'],
                'warnings': quality['warnings'],
                'was_rewritten': rewritten
            },
            additional_images=additional_images,
            slug=wp_result.get("slug") if wp_result else None
        )
        log_event("CATEGORY_GENERATE_SUCCESS", f"Generated article for {category}", draft_id=draft_id)

    except Exception as e:
        log_error("CATEGORY_GENERATE_ERROR", str(e), error=e)
        try:
            notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
            notifier.send_error_notification("CATEGORY_GENERATE_ERROR", str(e), f"カテゴリ: {category}")
        except:
            pass


def process_generate_from_preview(preview_id: str, index: int, line_bot_api, user_id: str):
    """プレビューで選択された1件のトレンドから記事を生成"""
    from src.content_generator import ContentGenerator, check_article_quality
    from src.notifier import Notifier
    from src.storage_manager import StorageManager

    notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))

    try:
        storage = StorageManager()
        generator = ContentGenerator(os.environ.get("GEMINI_API_KEY"))

        # プレビューからトレンドデータ取得
        target = storage.get_trend_from_preview(preview_id, index)

        if not target:
            log_event("PREVIEW_TREND_NOT_FOUND", "Trend not found in preview", preview_id=preview_id, index=index)
            notifier.send_error_notification("PREVIEW_NOT_FOUND", "プレビューデータが見つかりませんでした。", "")
            return

        if target.get("expired"):
            log_event("PREVIEW_EXPIRED", "Preview data expired", preview_id=preview_id)
            notifier.send_error_notification("PREVIEW_EXPIRED", "プレビューの有効期限（30分）が切れました。「トレンド」と入力して再取得してください。", "")
            return

        # 重複チェック
        title = target.get('title', '')
        if storage.is_duplicate_trend(title):
            log_event("PREVIEW_DUPLICATE", "Trend already generated", title=title[:50])
            notifier.send_error_notification("DUPLICATE_TREND", f"「{title[:30]}」は既に記事生成済みです。", "")
            return

        # 記事生成パイプライン（process_ondemand_textと同じフロー）
        sns_content = generator.generate_content(target)
        cms_content = generator.generate_cms_article(target)

        quality = check_article_quality(cms_content, target)
        log_event("QUALITY_CHECK", f"Quality score: {quality['score']}/100", score=quality['score'])
        rewritten = False
        if not quality['passed'] and quality['warnings']:
            log_event("ARTICLE_REWRITE", "Auto-rewriting article", warnings=quality['warnings'])
            cms_content = generator.rewrite_article(cms_content, quality['warnings'], target)
            quality = check_article_quality(cms_content, target)
            rewritten = True

        img_url = target.get('image_url')
        trend_category = target.get('category', 'other')
        artist_tags = cms_content.get('artist_tags', [])
        if artist_tags:
            target['artist_tags'] = artist_tags

        wp_result = storage.save_draft_to_wordpress(cms_content, img_url, None, trend_category, artist_tags)

        draft_data = {
            "status": "draft",
            "trend_source": target,
            "sns_content": sns_content,
            "cms_content": cms_content,
            "quality_score": quality['score'],
            "quality_passed": quality['passed'],
            "quality_warnings": quality['warnings'],
            "was_rewritten": rewritten,
            "wordpress_post_id": wp_result["id"] if wp_result else None,
            "wordpress_preview_url": wp_result.get("preview_url") if wp_result else None,
        }
        draft_id = storage.save_draft(draft_data)
        storage.save_trend_title(title, {'draft_id': draft_id, 'category': trend_category})

        notifier.send_approval_request(
            content={**sns_content, **cms_content},
            image_url=img_url,
            draft_id=draft_id,
            wp_post_id=wp_result["id"] if wp_result else None,
            wp_preview_url=wp_result.get("preview_url") if wp_result else None,
            quality_data={
                'score': quality['score'],
                'passed': quality['passed'],
                'warnings': quality['warnings'],
                'was_rewritten': rewritten
            },
            slug=wp_result.get("slug") if wp_result else None
        )
        log_event("PREVIEW_GENERATE_COMPLETE", "Article generated from preview", draft_id=draft_id, title=title[:50])

    except Exception as e:
        log_error("PREVIEW_GENERATE_ERROR", "Failed to generate article from preview", error=e)
        try:
            notifier.send_error_notification(
                error_type="PREVIEW_GENERATE_ERROR",
                error_message=str(e)[:200],
                context=f"Preview ID: {preview_id}, Index: {index}"
            )
        except:
            pass


def process_generate_all_from_preview(preview_id: str, line_bot_api, user_id: str):
    """全トレンドから一括生成（最大4件制限 — タイムアウト対策）"""
    from src.storage_manager import StorageManager
    from src.notifier import Notifier

    notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))

    try:
        storage = StorageManager()
        trends = storage.get_all_trends_from_preview(preview_id)

        if not trends:
            notifier.send_error_notification("PREVIEW_NOT_FOUND", "プレビューデータが見つかりませんでした。", "")
            return

        if trends and trends[0].get("expired"):
            notifier.send_error_notification("PREVIEW_EXPIRED", "プレビューの有効期限（30分）が切れました。「トレンド」と入力して再取得してください。", "")
            return

        # 最大4件に制限（タイムアウト対策）
        trends_to_process = trends[:4]
        generated = 0
        skipped = 0

        for idx, trend in enumerate(trends_to_process):
            title = trend.get('title', '')
            if storage.is_duplicate_trend(title):
                log_event("PREVIEW_ALL_SKIP_DUPLICATE", "Skipping duplicate", title=title[:50])
                skipped += 1
                continue

            try:
                process_generate_from_preview(preview_id, idx, line_bot_api, user_id)
                generated += 1
            except Exception as e:
                log_error("PREVIEW_ALL_ITEM_ERROR", f"Failed to generate item {idx}", error=e)

        log_event("PREVIEW_ALL_COMPLETE", f"Batch generation complete: {generated} generated, {skipped} skipped")

    except Exception as e:
        log_error("PREVIEW_ALL_ERROR", "Failed to batch generate from preview", error=e)
        try:
            notifier.send_error_notification(
                error_type="PREVIEW_ALL_ERROR",
                error_message=str(e)[:200],
                context=f"Preview ID: {preview_id}"
            )
        except:
            pass
