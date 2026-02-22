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
            print("No trends found for topic")
            return

        target = trends[0]
        sns_content = generator.generate_content(target)
        cms_content = generator.generate_cms_article(target)

        quality = check_article_quality(cms_content, target)
        print(f"📊 Quality score: {quality['score']}/100")
        rewritten = False
        if not quality['passed'] and quality['warnings']:
            print(f"🔄 Auto-rewriting article...")
            cms_content = generator.rewrite_article(cms_content, quality['warnings'], target)
            quality = check_article_quality(cms_content, target)
            rewritten = True

        img_url = target.get('image_url')
        trend_category = target.get('category', 'other')
        artist_tags = cms_content.get('artist_tags', [])
        if artist_tags:
            target['artist_tags'] = artist_tags
            print(f"🏷️ Artist tags extracted: {artist_tags}")
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
             }
        )
        print("On-Demand Text Process Complete")

    except Exception as e:
        print(f"On-Demand Text Error: {e}")
        try:
            notifier.send_error_notification(
                error_type="ONDEMAND_TEXT_ERROR",
                error_message=str(e),
                context=f"トピック: {topic[:50]}"
            )
        except:
            pass

def process_ondemand_image(image_bytes, line_bot_api, user_id):
    """Handles image-based triggered generation"""
    from src.content_generator import ContentGenerator, check_article_quality
    from src.notifier import Notifier
    from src.storage_manager import StorageManager

    try:
        generator = ContentGenerator(os.environ.get("GEMINI_API_KEY"))
        notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
        storage = StorageManager()

        public_img_url = storage.upload_bytes_to_gcs(image_bytes)
        if not public_img_url:
            print("Image Upload Failed")
            return

        trend_data = generator.analyze_image_trend(public_img_url)
        sns_content = generator.generate_content(trend_data)
        cms_content = generator.generate_cms_article(trend_data)

        quality = check_article_quality(cms_content, trend_data)
        print(f"📊 Quality score: {quality['score']}/100")
        rewritten = False
        if not quality['passed'] and quality['warnings']:
            print(f"🔄 Auto-rewriting article...")
            cms_content = generator.rewrite_article(cms_content, quality['warnings'], trend_data)
            quality = check_article_quality(cms_content, trend_data)
            rewritten = True

        trend_category = trend_data.get('category', 'other')
        artist_tags = cms_content.get('artist_tags', [])
        if artist_tags:
            trend_data['artist_tags'] = artist_tags
            print(f"🏷️ Artist tags extracted: {artist_tags}")
        wp_result = storage.save_draft_to_wordpress(cms_content, public_img_url, None, trend_category, artist_tags)

        draft_data = {
            "status": "draft",
            "trend_source": trend_data,
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
             image_url=public_img_url,
             draft_id=draft_id,
             wp_post_id=wp_result["id"] if wp_result else None,
             wp_preview_url=wp_result.get("preview_url") if wp_result else None,
             quality_data={
                 'score': quality['score'],
                 'passed': quality['passed'],
                 'warnings': quality['warnings'],
                 'was_rewritten': rewritten
             }
        )
        print("On-Demand Image Process Complete")

    except Exception as e:
        print(f"On-Demand Image Error: {e}")
        try:
            notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
            notifier.send_error_notification(
                error_type="ONDEMAND_IMAGE_ERROR",
                error_message=str(e),
                context="画像からの記事生成中にエラー"
            )
        except:
            pass

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
            print(f"🏷️ Artist tags extracted: {artist_tags}")
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
            additional_images=additional_images
        )
        log_event("CATEGORY_GENERATE_SUCCESS", f"Generated article for {category}", draft_id=draft_id)

    except Exception as e:
        log_error("CATEGORY_GENERATE_ERROR", str(e), error=e)
        try:
            notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
            notifier.send_error_notification("CATEGORY_GENERATE_ERROR", str(e), f"カテゴリ: {category}")
        except:
            pass
