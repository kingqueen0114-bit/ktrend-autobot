"""
LINE Webhook handler for K-Trend AutoBot.
Handles incoming LINE events (text messages, images, postback actions).
"""
import os
import functions_framework

from utils.logging_config import log_event, log_error


@functions_framework.http
def handle_line_webhook(request):
    """
    LINE Webhook Entry Point.
    Handles 'Postback' events from the Approve button.
    """
    # Health Check (GET Request)
    if request.method == 'GET':
        return "OK", 200

    log_event("WEBHOOK_TRIGGERED", "Webhook request received")

    # Lazy Import LineBotApi to prevent top-level import errors
    from linebot import LineBotApi, WebhookHandler
    from linebot.models import PostbackEvent, TextMessage
    from linebot.exceptions import InvalidSignatureError
    
    # 1. Signature Validation (Security)
    channel_secret = os.environ.get("LINE_CHANNEL_SECRET")
    channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    
    if not channel_secret:
        return "Config Error", 500

    line_bot_api = LineBotApi(channel_access_token)
    handler = WebhookHandler(channel_secret)

    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    log_event("WEBHOOK_DEBUG", "Signature received", signature_length=len(signature) if signature else 0)
    
    try:
        # Custom handler for Postback
        events = handler.parser.parse(body, signature)
        log_event("WEBHOOK_EVENTS_PARSED", f"Parsed {len(events)} events")
        
        for event in events:
            log_event("WEBHOOK_EVENT_TYPE", f"Event type: {type(event).__name__}")
            # Handle text messages
            # Note: SDK v1 events are MessageEvent, containing .message which is TextMessage
            from linebot.models import MessageEvent, TextMessage, ImageMessage
            
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    text = event.message.text.strip()
                    log_event("TEXT_MESSAGE_RECEIVED", f"Received text message: {text}")

                    # Import line_actions functions
                    from handlers.edit_actions import process_edit_text
                    from handlers.generation_actions import process_ondemand_text, process_category_generate
                    from handlers.info_actions import show_pending_drafts, show_trend_summary, search_articles
                    from handlers.draft_actions import recover_failed_drafts

                    # Check for active edit session first
                    if process_edit_text(event.source.user_id, text, line_bot_api):
                        log_event("EDIT_SESSION_PROCESSED", "Processed edit session for user")
                        continue

                    if text in ["ID", "id", "Id", "ミナト"]:
                       log_event("ID_REQUEST_MATCHED", "User requested their ID")
                       user_id = event.source.user_id
                       line_bot_api.reply_message(
                           event.reply_token,
                           TextMessage(text=f"Your User ID:\n{user_id}")
                       )
                       log_event("ID_REQUEST_REPLIED", "Replied with user ID")
                    elif text in ["ヘルプ", "help", "Help", "HELP"]:
                       help_text = """📰 K-Trend AutoBot ヘルプ

【コマンド一覧】
・「トレンド」→ 今日のトレンド一覧
・「カテゴリ」→ カテゴリ選択メニュー
・「下書き」→ 未承認記事一覧
・「検索 キーワード」→ 記事検索
・「統計」→ 週間レポート
・「復旧」→ 失敗記事の復旧
・トピック送信 → 記事を自動生成

【承認フロー】
✅ 今すぐ公開 → 即時公開+Xテキスト
⏰ 予約公開 → 3時間後/翌日9時
✏️ 編集 → タイトル/メタ編集
❌ 却下 → 破棄（再生成可）

【自動実行】
毎日9時に記事自動生成"""
                       line_bot_api.reply_message(
                           event.reply_token,
                           TextMessage(text=help_text)
                       )
                    elif text in ["統計", "stats", "統計レポート", "レポート", "アナリティクス", "GA4", "analytics", "アナリティクスレポート"]:
                       line_bot_api.reply_message(
                           event.reply_token,
                           TextMessage(text="📊 GA4 アクセス統計レポートを分析中...")
                       )
                       try:
                           import subprocess
                           import sys
                           # Execute the analytics reporter directly to avoid refactoring the singleton/env initialization
                           subprocess.run([sys.executable, "-m", "src.analytics_reporter", "daily"], check=True, env=os.environ.copy())
                       except Exception as e:
                           log_error("ANALYTICS_FETCH_ERROR", "Failed to fetch analytics report", error=e)
                           line_bot_api.push_message(
                               event.source.user_id,
                               TextMessage(text=f"❌ レポートの取得に失敗しました: {e}")
                           )
                    elif text in ["カテゴリ", "新規記事", "記事作成", "カテゴリー"]:
                       # Show choice: AI vs Manual
                       from linebot.models import FlexSendMessage
                       flex_msg = {
                           "type": "bubble",
                           "body": {
                               "type": "box",
                               "layout": "vertical",
                               "contents": [
                                   {"type": "text", "text": "✍️ 記事作成メニュー", "weight": "bold", "size": "lg", "color": "#333333"},
                                   {"type": "text", "text": "作成方法を選んでください", "size": "xs", "color": "#999999", "margin": "sm"},
                                   {"type": "separator", "margin": "lg"},
                                   {
                                       "type": "button",
                                       "style": "primary",
                                       "color": "#1DB446",
                                       "height": "sm",
                                       "margin": "sm",
                                       "action": {
                                           "type": "postback",
                                           "label": "🤖 AIで自動生成",
                                           "data": "action=show_categories"
                                       }
                                   },
                                   {
                                       "type": "button",
                                       "style": "secondary",
                                       "height": "sm",
                                       "margin": "sm",
                                       "action": {
                                           "type": "postback",
                                           "label": "✍️ 自分で記事作成",
                                           "data": "action=create_blank_draft"
                                       }
                                   }
                               ]
                           }
                       }
                       line_bot_api.reply_message(
                           event.reply_token,
                           FlexSendMessage(alt_text="記事作成メニュー", contents=flex_msg)
                       )
                    elif text in ["下書き", "未承認", "pending", "ドラフト"]:
                       # Show pending drafts
                       show_pending_drafts(line_bot_api, event.reply_token)
                    elif text in ["復旧", "recover", "リカバリー", "再試行"]:
                       # Attempt to recover failed drafts
                       line_bot_api.reply_message(
                           event.reply_token,
                           TextMessage(text="🔄 失敗した記事の復旧を試みています...")
                       )
                       recover_failed_drafts(line_bot_api, event.source.user_id)
                    elif text in ["トレンド", "trend", "今日のトレンド", "最新トレンド"]:
                       # Show current trends without generating articles
                       line_bot_api.reply_message(
                           event.reply_token,
                           TextMessage(text="🔍 最新トレンドを取得中...")
                       )
                       show_trend_summary(line_bot_api, event.source.user_id)
                    elif text.startswith("検索 ") or text.startswith("検索　"):
                       # Search published articles
                       keyword = text.split(" ", 1)[1] if " " in text else text.split("　", 1)[1]
                       line_bot_api.reply_message(
                           event.reply_token,
                           TextMessage(text=f"🔍 「{keyword}」を検索中...")
                       )
                       search_articles(keyword, line_bot_api, event.source.user_id)
                    else:
                        # Trigger On-Demand Generation (Text Topic)
                        log_event("ONDEMAND_TEXT_TRIGGERED", f"Triggering on-demand generation: {text}")
                        # Immediately reply to user to acknowledge receipt
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextMessage(text=f"「{text}」について検索して記事を作成します...少々お待ちを！🤖📝")
                        )
                        # Process (This might timeout if simple function, ideally should be pub/sub for long tasks)
                        process_ondemand_text(text, line_bot_api, event.source.user_id)

                elif isinstance(event.message, ImageMessage):
                    from handlers.generation_actions import process_ondemand_image
                    log_event("IMAGE_MESSAGE_RECEIVED", "Received image message")
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextMessage(text="画像を受け取りました！解析して記事を作成します...📸🤖")
                    )
                    
                    # Get Image Content
                    message_content = line_bot_api.get_message_content(event.message.id)
                    image_data = message_content.content
                    
                    process_ondemand_image(image_data, line_bot_api, event.source.user_id)

            if isinstance(event, PostbackEvent):
                data = event.postback.data
                log_event("POSTBACK_RECEIVED", f"Postback data: {data}")

                # data format: "action=approve&draft_id=xyz" or "action=reject&draft_id=xyz"
                try:
                    params = dict(x.split('=') for x in data.split('&') if '=' in x)
                except Exception as parse_error:
                    log_error("POSTBACK_PARSE_ERROR", f"Failed to parse postback: {data}", error=parse_error)
                    params = {}

                action = params.get('action')
                draft_id = params.get('draft_id')
                log_event("POSTBACK_ACTION", f"Action: {action}, Draft ID: {draft_id}")

                # Import line_actions functions
                from handlers.draft_actions import (
                    process_approval, process_rejection, process_regenerate,
                    process_approve_all, process_schedule, process_regenerate_article,
                )
                from handlers.generation_actions import process_category_generate
                from handlers.info_actions import show_pending_drafts
                from handlers.edit_actions import show_quick_edit_options, store_edit_session

                if action == 'approve':
                    process_approval(draft_id, line_bot_api, event.reply_token)
                elif action == 'reject':
                    process_rejection(draft_id, line_bot_api, event.reply_token)
                elif action == 'regenerate':
                    category = params.get('category', 'other')
                    process_regenerate(category, line_bot_api, event.reply_token, event.source.user_id)
                elif action == 'done':
                    from linebot.models import TextMessage
                    line_bot_api.reply_message(event.reply_token, TextMessage(text="👋 了解しました！"))
                elif action == 'stats_request':
                    from src.notifier import Notifier
                    from src.storage_manager import StorageManager
                    from linebot.models import TextMessage
                    line_bot_api.reply_message(event.reply_token, TextMessage(text="📊 統計レポートを生成中..."))
                    notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))
                    storage = StorageManager()
                    stats = storage.get_stats_summary(days=7)
                    best_articles = storage.get_best_articles(days=7, limit=3)
                    notifier.send_stats_summary(stats, period_days=7, best_articles=best_articles)
                elif action == 'category_generate':
                    category = params.get('category', 'other')
                    process_category_generate(category, line_bot_api, event.reply_token, event.source.user_id)
                elif action == 'approve_all':
                    process_approve_all(line_bot_api, event.reply_token)
                elif action == 'view_drafts':
                    show_pending_drafts(line_bot_api, event.reply_token)
                elif action == 'schedule':
                    hours = int(params.get('hours', 3))
                    process_schedule(draft_id, hours, line_bot_api, event.reply_token)
                elif action == 'quick_edit':
                    show_quick_edit_options(draft_id, line_bot_api, event.reply_token)
                elif action == 'edit_title':
                    # Store edit session and prompt for new title
                    store_edit_session(event.source.user_id, draft_id, 'title')
                    from linebot.models import TextMessage
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextMessage(text="📝 新しいタイトルを入力してください：")
                    )
                elif action == 'edit_meta':
                    # Store edit session and prompt for new meta description
                    store_edit_session(event.source.user_id, draft_id, 'meta')
                    from linebot.models import TextMessage
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextMessage(text="📝 新しいメタ説明を入力してください（160文字以内推奨）：")
                    )
                elif action == 'regenerate_article':
                    process_regenerate_article(draft_id, line_bot_api, event.reply_token)
                elif action == 'show_categories':
                    from linebot.models import FlexSendMessage
                    categories = [
                        ("🎤", "K-pop", "#6C5CE7", "K-pop アイドル"),
                        ("💄", "コスメ", "#E84393", "韓国コスメ"),
                        ("👗", "ファッション", "#00B894", "韓国ファッション"),
                        ("🍜", "グルメ", "#FDCB6E", "韓国グルメ"),
                        ("✈️", "旅行", "#0984E3", "韓国旅行"),
                        ("🎉", "イベント", "#FF7675", "K-pop イベント"),
                    ]
                    buttons = []
                    for emoji, name, color, topic in categories:
                        buttons.append({
                            "type": "button",
                            "style": "primary",
                            "color": color,
                            "height": "sm",
                            "margin": "sm",
                            "action": {
                                "type": "message",
                                "label": f"{emoji} {name}",
                                "text": f"記事: {topic}"
                            }
                        })
                    flex_msg = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "📂 カテゴリを選択", "weight": "bold", "size": "lg", "color": "#333333"},
                                {"type": "text", "text": "AIが生成するカテゴリを選んでください", "size": "xs", "color": "#999999", "margin": "sm"},
                                {"type": "separator", "margin": "lg"}
                            ] + buttons
                        }
                    }
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(alt_text="カテゴリ選択", contents=flex_msg)
                    )
                elif action == 'create_blank_draft':
                    from src.storage_manager import StorageManager
                    from linebot.models import FlexSendMessage, TextMessage
                    storage = StorageManager()
                    new_draft_id = storage.create_blank_draft(event.source.user_id)
                    if not new_draft_id:
                        line_bot_api.reply_message(event.reply_token, TextMessage(text="❌ エラー: 下書きの作成に失敗しました。"))
                        return
                    
                    app_url = os.environ.get('APP_URL', 'https://asia-northeast1-k-trend-autobot.cloudfunctions.net/ktrend-autobot')
                    view_url = f"{app_url}?action=view_draft&id={new_draft_id}"
                    
                    flex_msg = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "✍️ 新規記事の作成",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#333333"
                                },
                                {
                                    "type": "text",
                                    "text": "以下のボタンからエディタを開いて記事を作成・公開できます。",
                                    "wrap": True,
                                    "size": "sm",
                                    "color": "#666666",
                                    "margin": "md"
                                }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "color": "#1DB446",
                                    "action": {
                                        "type": "uri",
                                        "label": "📝 エディタを開く",
                                        "uri": view_url
                                    }
                                }
                            ]
                        }
                    }
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(alt_text="記事エディタ", contents=flex_msg)
                    )
                else:
                    log_event("POSTBACK_UNHANDLED", f"Unhandled action: {action}")

    except InvalidSignatureError:
        return "Invalid Signature", 400
    except Exception as e:
        log_error("WEBHOOK_ERROR", "Unhandled webhook exception", error=e)
        return "Error", 500

    return "OK", 200
