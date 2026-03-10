"""
Draft action handlers for K-Trend AutoBot.
Handles approval, rejection, scheduling, and regeneration of drafts.
"""
import os
import logging
from datetime import datetime
from utils.logging_config import log_event, log_error
from utils.helpers import generate_hashtags, mark_draft_error, recover_failed_draft
from src.x_poster import post_tweet as post_to_x

logger = logging.getLogger(__name__)

def process_approval(draft_id, line_bot_api, reply_token):
    """Handle approval - publish WordPress draft"""
    from src.storage_manager import StorageManager
    from linebot.models import TextMessage

    log_event("APPROVAL_START", f"Processing approval for draft", draft_id=draft_id)
    storage = StorageManager()

    draft = storage.get_draft(draft_id)
    if not draft:
        line_bot_api.reply_message(reply_token, TextMessage(text="⚠️ ドラフトが見つかりませんでした。"))
        return

    if draft.get('status') == 'approved':
         line_bot_api.reply_message(reply_token, TextMessage(text="ℹ️ この記事はすでに公開されています。"))
         return

    # Sanity移行: draft_idを優先的に使用（wp_post_idは旧互換）
    sanity_draft_id = draft.get('sanity_draft_id') or draft_id
    wp_post_id = draft.get('wordpress_post_id') or draft.get('wordpress_id')
    img_url = draft.get('trend_source', {}).get('image_url')
    cms_content = draft.get('cms_content', {})
    category = draft.get('trend_source', {}).get('category')
    artist_tags = draft.get('trend_source', {}).get('artist_tags', [])
    result = storage.publish_to_wordpress(cms_content, img_url, category=category, artist_tags=artist_tags, wp_post_id=wp_post_id, draft_id=sanity_draft_id)

    if result:
        draft['status'] = 'approved'
        draft['wordpress_url'] = result['url']
        draft['wordpress_id'] = result['id']
        storage.save_draft(draft, draft_id)
        storage.increment_approval_stat(approved=True)

        # X自動投稿
        x_result = {"success": False}
        try:
            x_text = cms_content.get("x_post_1", "")
            published_url = result.get("url", "")
            img_url_for_x = draft.get("trend_source", {}).get("image_url", "")
            if x_text and published_url:
                x_result = post_to_x(x_text, published_url, img_url_for_x)
        except Exception as e:
            logger.warning(f"X投稿でエラー（記事公開は正常完了）: {e}")

        article_title = draft.get('cms_content', {}).get('title', '記事')[:40]
        quality_score = draft.get('quality_score', 0)

        from linebot.models import FlexSendMessage
        flex_body_contents = [
            {"type": "text", "text": "✅ 公開完了!", "weight": "bold", "size": "xl", "color": "#1DB446"},
            {"type": "text", "text": article_title, "wrap": True, "size": "md", "margin": "md"},
            {"type": "separator", "margin": "lg"},
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "md",
                "contents": [
                    {"type": "text", "text": "品質スコア", "size": "sm", "color": "#666666", "flex": 1},
                    {"type": "text", "text": f"{quality_score}/100", "size": "sm", "weight": "bold", "align": "end", "flex": 1}
                ]
            }
        ]

        # X投稿成功時はステータスを表示
        if x_result.get("success"):
            flex_body_contents.append({
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                    {"type": "text", "text": "X投稿", "size": "sm", "color": "#666666", "flex": 1},
                    {"type": "text", "text": "投稿済み", "size": "sm", "weight": "bold", "color": "#1DA1F2", "align": "end", "flex": 1}
                ]
            })

        footer_buttons = [
            {
                "type": "button",
                "style": "primary",
                "action": {
                    "type": "uri",
                    "label": "📖 記事を見る",
                    "uri": result['url']
                }
            }
        ]

        # X投稿成功時はツイートURLボタンも追加
        if x_result.get("success") and x_result.get("tweet_url"):
            footer_buttons.append({
                "type": "button",
                "style": "secondary",
                "action": {
                    "type": "uri",
                    "label": "🐦 Xの投稿を見る",
                    "uri": x_result["tweet_url"]
                }
            })

        flex_contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": flex_body_contents
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": footer_buttons
            }
        }

        log_event("APPROVAL_SUCCESS", f"Article published: {article_title[:40]}", draft_id=draft_id, wordpress_url=result['url'])
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text=f"公開完了: {article_title}", contents=flex_contents))

        cms_content = draft.get('cms_content', {})
        x_post_1 = cms_content.get('x_post_1', '')
        x_post_2 = cms_content.get('x_post_2', '')
        category = draft.get('trend_source', {}).get('category', 'other')
        hashtags = generate_hashtags(category, article_title)

        if x_post_1 or x_post_2:
            from linebot import LineBotApi
            line_bot_api_push = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
            x_message = f"📱 X投稿用テキスト\n\n"
            hashtag_str = " ".join(hashtags)
            if x_post_1:
                if "#" not in x_post_1:
                    x_post_1 = f"{x_post_1}\n{hashtag_str}"
                x_message += f"【案1】\n{x_post_1}\n\n"
            if x_post_2:
                if "#" not in x_post_2:
                    x_post_2 = f"{x_post_2}\n{hashtag_str}"
                x_message += f"【案2】\n{x_post_2}\n\n"
            x_message += f"📎 {result['url']}\n\n"
            x_message += f"🏷️ おすすめタグ: {hashtag_str}"
            if x_result.get("success") and x_result.get("tweet_url"):
                x_message += f"\n\n✅ X自動投稿済み: {x_result['tweet_url']}"
            user_id = (os.environ.get("LINE_USER_ID") or "").split(",")[0]
            if user_id:
                line_bot_api_push.push_message(user_id, TextMessage(text=x_message))
    else:
        log_error("APPROVAL_FAILED", f"Failed to publish draft", draft_id=draft_id)
        mark_draft_error(draft_id, "wordpress_publish", "Failed to publish article", "publish")

        from linebot.models import FlexSendMessage
        retry_flex = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "❌ 公開失敗", "weight": "bold", "size": "lg", "color": "#F44336"},
                    {"type": "text", "text": "記事の公開に失敗しました。", "wrap": True, "size": "sm", "margin": "md"},
                    {"type": "text", "text": "ネットワーク状態を確認後、再試行してください。", "wrap": True, "size": "xs", "color": "#666666", "margin": "sm"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "spacing": "sm",
                "contents": [
                    {"type": "button", "style": "primary", "height": "sm", "action": {"type": "postback", "label": "🔄 再試行", "data": f"action=approve&draft_id={draft_id}", "displayText": "公開を再試行"}},
                    {"type": "button", "style": "secondary", "height": "sm", "action": {"type": "postback", "label": "❌ 中止", "data": f"action=reject&draft_id={draft_id}", "displayText": "公開を中止"}}
                ]
            }
        }
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text="公開失敗 - 再試行可能", contents=retry_flex))

def process_rejection(draft_id, line_bot_api, reply_token):
    """Handle rejection - delete WordPress draft and offer regenerate option"""
    from src.storage_manager import StorageManager
    from linebot.models import TextMessage, FlexSendMessage

    storage = StorageManager()
    draft = storage.get_draft(draft_id)
    category = 'other'

    if draft:
        wp_post_id = draft.get('wordpress_post_id')
        if wp_post_id:
            storage.delete_wordpress_draft(wp_post_id)
            log_event("WP_DRAFT_DELETED", f"Deleted WordPress draft: {wp_post_id}", draft_id=draft_id)

        # Sanity下書きも削除
        sanity_draft_id = draft.get('sanity_draft_id') or draft_id
        if sanity_draft_id:
            try:
                from src.sanity_client import delete as sanity_delete
                plain_id = sanity_draft_id.replace("drafts.", "")
                sanity_delete(f"drafts.{plain_id}")
                log_event("SANITY_DRAFT_DELETED", f"Deleted Sanity draft: drafts.{plain_id}", draft_id=draft_id)
            except Exception as e:
                logger.warning(f"Sanity下書き削除失敗: {e}")

        category = draft.get('trend_source', {}).get('category', 'other')
        draft['status'] = 'rejected'
        storage.save_draft(draft, draft_id)
        storage.increment_approval_stat(approved=False)

    log_event("DRAFT_REJECTED", f"Draft {draft_id} was rejected by user", draft_id=draft_id)

    flex_contents = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "❌ 却下しました", "weight": "bold", "size": "lg", "color": "#999999"},
                {"type": "text", "text": "このドラフトは破棄されました。", "size": "sm", "color": "#666666", "margin": "md"},
                {"type": "separator", "margin": "lg"},
                {"type": "text", "text": "別のトレンドで記事を生成しますか？", "size": "sm", "color": "#666666", "margin": "lg", "wrap": True}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {"type": "button", "style": "primary", "action": {"type": "postback", "label": "🔄 再生成", "data": f"action=regenerate&category={category}", "displayText": "新しい記事を生成します..."}},
                {"type": "button", "style": "secondary", "action": {"type": "postback", "label": "終了", "data": "action=done", "displayText": "了解しました"}}
            ]
        }
    }
    line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text="却下しました", contents=flex_contents))

def process_regenerate(category, line_bot_api, reply_token, user_id):
    """Handle regenerate request - generate a new article with a different topic"""
    from src.fetch_trends import TrendFetcher
    from src.content_generator import ContentGenerator, check_article_quality
    from src.notifier import Notifier
    from src.storage_manager import StorageManager
    from linebot.models import TextMessage

    try:
        line_bot_api.reply_message(reply_token, TextMessage(text=f"🔄 新しい記事を生成中...カテゴリ: {category}"))

        fetcher = TrendFetcher(os.environ.get("GEMINI_API_KEY"))
        generator = ContentGenerator(os.environ.get("GEMINI_API_KEY"))
        notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
        storage = StorageManager()

        category_topics = {
            'artist': 'K-pop アイドル 最新ニュース',
            'beauty': '韓国コスメ 新作',
            'fashion': '韓国ファッション トレンド',
            'food': '韓国グルメ カフェ',
            'travel': '韓国旅行 おすすめ',
            'event': 'K-pop コンサート イベント',
            'other': '韓国エンタメ トレンド'
        }

        topic = category_topics.get(category, category_topics['other'])
        year = datetime.now().strftime("%Y")
        topic = f"{topic} {year}"

        trends = fetcher.fetch_trends(topic=topic)
        if not trends:
            notifier.send_error_notification("REGENERATE_NO_TRENDS", "再生成用のトレンドが見つかりませんでした", f"カテゴリ: {category}")
            return

        trends = [t for t in trends if not storage.is_duplicate_trend(t.get('title', ''))]
        if not trends:
            notifier.send_error_notification("REGENERATE_ALL_DUPLICATES", "すべてのトレンドが既出でした", f"カテゴリ: {category}")
            return

        target = trends[0]
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
        trend_category = target.get('category', 'other')
        artist_tags = cms_content.get('artist_tags', [])
        if artist_tags:
            target['artist_tags'] = artist_tags
        wp_result = storage.save_draft_to_wordpress(cms_content, img_url, additional_images, trend_category, artist_tags)

        draft_data = {
            "status": "draft",
            "trend_source": target,
            "sns_content": sns_content,
            "cms_content": cms_content,
            "quality_score": quality['score'],
            "quality_passed": quality['passed'],
            "quality_warnings": quality['warnings'],
            "was_rewritten": rewritten,
            "regenerated": True,
            "wordpress_post_id": wp_result["id"] if wp_result else None,
            "wordpress_preview_url": wp_result.get("preview_url") if wp_result else None,
        }
        draft_id = storage.save_draft(draft_data)
        storage.save_trend_title(target.get('title', ''), {'draft_id': draft_id, 'category': trend_category})

        notifier.send_approval_request(
            content={**sns_content, **cms_content},
            image_url=img_url,
            draft_id=draft_id,
            wp_post_id=wp_result["id"] if wp_result else None,
            wp_preview_url=wp_result.get("preview_url") if wp_result else None,
            quality_data={'score': quality['score'], 'passed': quality['passed'], 'warnings': quality['warnings'], 'was_rewritten': rewritten},
            additional_images=additional_images,
            slug=wp_result.get("slug") if wp_result else None
        )
        log_event("REGENERATE_SUCCESS", f"Regenerated article for category {category}", draft_id=draft_id, category=category)

    except Exception as e:
        log_error("REGENERATE_ERROR", f"Regenerate failed for category {category}", error=e)
        try:
            notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
            notifier.send_error_notification("REGENERATE_ERROR", str(e), f"カテゴリ: {category}")
        except:
            pass

def process_regenerate_article(draft_id: str, line_bot_api, reply_token):
    """Regenerate article content for a draft."""
    from src.storage_manager import StorageManager
    from src.content_generator import ContentGenerator, check_article_quality
    from linebot.models import TextMessage

    storage = StorageManager()

    try:
        draft_ref = storage.db.collection(storage.collection_name).document(draft_id)
        draft = draft_ref.get()

        if not draft.exists:
            line_bot_api.reply_message(reply_token, TextMessage(text="❌ 下書きが見つかりません。"))
            return

        draft_data = draft.to_dict()
        trend_source = draft_data.get('trend_source', {})

        if not trend_source:
            line_bot_api.reply_message(reply_token, TextMessage(text="❌ 元のトピック情報がありません。"))
            return

        article_title = trend_source.get('title', '')[:30]
        line_bot_api.reply_message(reply_token, TextMessage(text=f"🔄 記事を再生成中...\nトピック: {article_title}..."))

        generator = ContentGenerator(os.environ.get("GEMINI_API_KEY"))
        new_cms_content = generator.generate_cms_article(trend_source)

        if new_cms_content:
            quality = check_article_quality(new_cms_content, trend_source)
            rewritten = False
            if not quality['passed'] and quality['warnings']:
                new_cms_content = generator.rewrite_article(new_cms_content, quality['warnings'], trend_source)
                quality = check_article_quality(new_cms_content, trend_source)
                rewritten = True

            draft_ref.update({
                'cms_content': new_cms_content,
                'quality_score': quality['score'],
                'quality_passed': quality['passed'],
                'quality_warnings': quality['warnings'],
                'was_rewritten': rewritten,
                'regenerated_at': datetime.now().isoformat(),
                'regeneration_count': draft_data.get('regeneration_count', 0) + 1
            })
            log_event("ARTICLE_REGENERATED", f"Draft {draft_id} regenerated successfully")

            from src.notifier import Notifier
            notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
            sns_content = draft_data.get('sns_content', {})
            notifier.send_approval_request(
                content={**sns_content, **new_cms_content},
                image_url=draft_data.get('trend_source', {}).get('image_url', ''),
                draft_id=draft_id,
                wp_post_id=draft_data.get('wordpress_post_id'),
                wp_preview_url=draft_data.get('wordpress_preview_url'),
                quality_data={'score': quality['score'], 'passed': quality['passed'], 'warnings': quality['warnings'], 'was_rewritten': rewritten},
                slug=draft_data.get('slug')
            )
        else:
            import requests
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')}"}
            user_id = (os.environ.get("LINE_USER_ID") or "").split(",")[0]
            if user_id:
                payload = {"to": user_id, "messages": [{"type": "text", "text": "❌ 記事の再生成に失敗しました。"}]}
                requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)

    except Exception as e:
        log_error("REGENERATE_FAILED", str(e), f"draft_id={draft_id}")
        import requests
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')}"}
        user_id = (os.environ.get("LINE_USER_ID") or "").split(",")[0]
        if user_id:
            payload = {"to": user_id, "messages": [{"type": "text", "text": f"❌ エラー: {str(e)[:50]}"}]}
            requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)

def process_approve_all(line_bot_api, reply_token):
    """Approve all pending drafts."""
    from src.storage_manager import StorageManager
    from linebot.models import TextMessage

    storage = StorageManager()

    try:
        drafts_ref = storage.db.collection(storage.collection_name) \
            .where('status', '==', 'draft') \
            .limit(10)
        drafts = list(drafts_ref.stream())

        if not drafts:
            line_bot_api.reply_message(reply_token, TextMessage(text="📭 承認する下書きがありません。"))
            return

        line_bot_api.reply_message(reply_token, TextMessage(text=f"🚀 {len(drafts)}件の記事を一括承認中..."))

        success_count = 0
        fail_count = 0

        for doc in drafts:
            draft = doc.to_dict()
            draft_id = doc.id
            try:
                sanity_draft_id = draft.get('sanity_draft_id') or draft_id
                wp_post_id = draft.get('wordpress_post_id') or draft.get('wordpress_id')
                cms_content = draft.get('cms_content', {})
                img_url = draft.get('trend_source', {}).get('image_url')
                category = draft.get('trend_source', {}).get('category')
                artist_tags = draft.get('trend_source', {}).get('artist_tags', [])
                result = storage.publish_to_wordpress(cms_content, img_url, category=category, artist_tags=artist_tags, wp_post_id=wp_post_id, draft_id=sanity_draft_id)
                if result:
                    draft['status'] = 'approved'
                    draft['wordpress_url'] = result['url']
                    draft['wordpress_id'] = result['id']
                    storage.save_draft(draft, draft_id)
                    storage.increment_approval_stat(approved=True)
                    success_count += 1

                    # X自動投稿
                    try:
                        x_text = cms_content.get("x_post_1", "")
                        published_url = result.get("url", "")
                        img_url_for_x = draft.get("trend_source", {}).get("image_url", "")
                        if x_text and published_url:
                            x_result = post_to_x(x_text, published_url, img_url_for_x)
                            if x_result.get("success"):
                                log_event("X_POST_SUCCESS", f"X auto-post for draft {draft_id}", tweet_url=x_result.get("tweet_url", ""))
                    except Exception as xe:
                        logger.warning(f"X投稿でエラー（記事公開は正常完了）: {xe}")
                else:
                    fail_count += 1
            except Exception as e:
                log_error("BULK_APPROVE_ITEM_FAILED", f"Error approving draft {draft_id}", error=e)
                fail_count += 1

        from src.notifier import Notifier
        if fail_count > 0:
            notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
            notifier.send_error_notification("BULK_APPROVE_COMPLETE", f"一括承認完了: {success_count}件成功 / {fail_count}件失敗", "")

        from linebot import LineBotApi
        line_bot_api_push = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
        bulk_user_id = (os.environ.get("LINE_USER_ID") or "").split(",")[0]
        if bulk_user_id:
            line_bot_api_push.push_message(
                bulk_user_id,
                TextMessage(text=f"✅ 一括承認完了！\n成功: {success_count}件\n失敗: {fail_count}件")
            )
        log_event("BULK_APPROVE_COMPLETE", f"Approved {success_count} drafts", success_count=success_count, fail_count=fail_count)

    except Exception as e:
        log_error("BULK_APPROVE_ERROR", str(e), error=e)

def process_schedule(draft_id, hours, line_bot_api, reply_token):
    """Schedule a draft for future publication via Sanity publishedAt."""
    from src.storage_manager import StorageManager
    from src import sanity_client
    from linebot.models import TextMessage, FlexSendMessage
    from datetime import timedelta

    storage = StorageManager()

    try:
        draft = storage.get_draft(draft_id)
        if not draft:
            line_bot_api.reply_message(reply_token, TextMessage(text="⚠️ ドラフトが見つかりませんでした。"))
            return

        scheduled_time = datetime.utcnow() + timedelta(hours=hours)
        scheduled_time_jst = scheduled_time + timedelta(hours=9)

        # SanityドラフトにpublishedAtを設定して予約公開
        sanity_draft_id = draft.get('sanity_draft_id') or draft_id
        plain_id = sanity_draft_id.replace("drafts.", "")
        sanity_doc_id = f"drafts.{plain_id}"

        sanity_client.patch(sanity_doc_id, set_fields={
            "publishedAt": scheduled_time.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        })

        draft['status'] = 'scheduled'
        draft['scheduled_time'] = scheduled_time.isoformat()
        storage.save_draft(draft, draft_id)

        article_title = draft.get('cms_content', {}).get('title', '記事')[:30]
        time_display = scheduled_time_jst.strftime("%m/%d %H:%M")

        flex_contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "⏰ 予約公開設定完了", "weight": "bold", "size": "lg", "color": "#0277BD"},
                    {"type": "text", "text": article_title, "wrap": True, "size": "md", "margin": "md"},
                    {"type": "separator", "margin": "lg"},
                    {
                        "type": "box", "layout": "horizontal", "margin": "lg",
                        "contents": [
                            {"type": "text", "text": "公開予定", "size": "sm", "color": "#666666", "flex": 1},
                            {"type": "text", "text": f"{time_display} JST", "size": "sm", "weight": "bold", "align": "end", "flex": 2}
                        ]
                    }
                ]
            }
        }
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text=f"予約公開設定: {time_display}", contents=flex_contents))
        log_event("SCHEDULE_SUCCESS", f"Scheduled article for {scheduled_time.isoformat()}", draft_id=draft_id)

    except Exception as e:
        log_error("SCHEDULE_ERROR", str(e), error=e)
        line_bot_api.reply_message(reply_token, TextMessage(text=f"❌ 予約設定に失敗: {str(e)[:30]}"))

def recover_failed_drafts(line_bot_api, user_id: str):
    """Attempt to recover all failed drafts."""
    from src.storage_manager import StorageManager
    import requests

    storage = StorageManager()

    try:
        error_drafts = storage.db.collection(storage.collection_name) \
            .where('status', '==', 'error') \
            .limit(10) \
            .stream()

        error_list = list(error_drafts)
        recovered_count = 0
        failed_count = 0

        if not error_list:
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')}"}
            payload = {"to": user_id, "messages": [{"type": "text", "text": "✅ 失敗した記事はありません。"}]}
            requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
            return

        for doc in error_list:
            draft_id = doc.id
            if recover_failed_draft(draft_id):
                recovered_count += 1
            else:
                failed_count += 1

        result_text = f"🔄 復旧結果\n\n✅ 復旧成功: {recovered_count}件\n❌ 復旧失敗: {failed_count}件"
        if failed_count > 0:
            result_text += "\n\n失敗した記事は「下書き」コマンドで確認してください。"

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')}"}
        payload = {"to": user_id, "messages": [{"type": "text", "text": result_text}]}
        requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
        log_event("RECOVERY_BATCH", f"Recovered {recovered_count}/{recovered_count + failed_count} drafts")

    except Exception as e:
        log_error("RECOVERY_BATCH_FAILED", str(e), error=e)
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')}"}
        payload = {"to": user_id, "messages": [{"type": "text", "text": f"❌ 復旧処理でエラーが発生しました: {str(e)[:50]}"}]}
        requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
