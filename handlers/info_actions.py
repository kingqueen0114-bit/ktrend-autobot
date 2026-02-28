"""
Info action handlers for K-Trend AutoBot.
Handles showing pending drafts, trend summaries, and searching articles.
"""
import os
from utils.logging_config import log_event, log_error

def show_pending_drafts(line_bot_api, reply_token):
    """Show pending drafts with approval options."""
    from src.storage_manager import StorageManager
    from linebot.models import FlexSendMessage, TextMessage

    storage = StorageManager()

    try:
        from google.cloud.firestore_v1.base_query import FieldFilter
        drafts_ref = storage.db.collection(storage.collection_name) \
            .where(filter=FieldFilter('status', 'in', ['draft', 'pending'])) \
            .order_by('created_at', direction='DESCENDING') \
            .limit(5)

        drafts = list(drafts_ref.stream())

        if not drafts:
            # 返信をFlex Messageにして、Web管理画面へのボタンを提示
            flex_message = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "📭 未承認の下書きはありません。", "weight": "bold", "size": "md", "wrap": True},
                        {"type": "text", "text": "公開済み記事の編集や、過去の記事はWeb管理画面から確認できます。", "size": "sm", "color": "#666666", "wrap": True, "margin": "md"}
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "📰 記事一覧・管理を開く",
                                "uri": "https://ktrend-autobot-nnfhuwwfiq-an.a.run.app/drafts"
                            }
                        }
                    ]
                }
            }
            line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text="未承認の下書きはありません", contents=flex_message))
            return

        bubbles = []
        for doc in drafts:
            draft = doc.to_dict()
            draft_id = doc.id
            title = draft.get('cms_content', {}).get('title', '無題')[:30]
            quality_score = draft.get('quality_score', 0)
            category = draft.get('trend_source', {}).get('category', 'other')

            if quality_score >= 80:
                score_color = "#1DB446"
            elif quality_score >= 60:
                score_color = "#FFA000"
            else:
                score_color = "#F44336"

            bubble = {
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": title, "weight": "bold", "size": "sm", "wrap": True, "maxLines": 2},
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "contents": [
                                {"type": "text", "text": f"📊 {quality_score}", "size": "xs", "color": score_color},
                                {"type": "text", "text": f"📂 {category}", "size": "xs", "color": "#666666", "align": "end"}
                            ]
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
                            "height": "sm",
                            "action": {
                                "type": "uri",
                                "label": "📖 開く",
                                "uri": f"https://ktrend-autobot-nnfhuwwfiq-an.a.run.app/draft/{draft_id}"
                            }
                        },
                        {
                            "type": "button",
                            "style": "secondary",
                            "height": "sm",
                            "action": {
                                "type": "postback",
                                "label": "❌ 却下",
                                "data": f"action=reject&draft_id={draft_id}"
                            }
                        }
                    ]
                }
            }
            bubbles.append(bubble)

        if len(bubbles) > 1:
            approve_all_bubble = {
                "type": "bubble",
                "size": "micro",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "justifyContent": "center",
                    "contents": [
                        {"type": "text", "text": "🚀", "size": "3xl", "align": "center"},
                        {"type": "text", "text": "一括承認", "weight": "bold", "size": "sm", "align": "center", "margin": "md"}
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {
                                "type": "postback",
                                "label": "全て承認",
                                "data": "action=approve_all"
                            }
                        }
                    ]
                }
            }
            bubbles.append(approve_all_bubble)

        # 常に最後尾に「Web管理画面」へのリンクバブルを追加する
        web_manage_bubble = {
            "type": "bubble",
            "size": "micro",
            "body": {
                "type": "box",
                "layout": "vertical",
                "justifyContent": "center",
                "contents": [
                    {"type": "text", "text": "🌐", "size": "3xl", "align": "center"},
                    {"type": "text", "text": "すべての記事", "weight": "bold", "size": "sm", "align": "center", "margin": "md"},
                    {"type": "text", "text": "公開済みの編集も", "size": "xs", "color": "#888888", "align": "center"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#0277bd",
                        "action": {
                            "type": "uri",
                            "label": "管理画面へ",
                            "uri": "https://ktrend-autobot-nnfhuwwfiq-an.a.run.app/drafts"
                        }
                    }
                ]
            }
        }
        bubbles.append(web_manage_bubble)

        flex_message = {"type": "carousel", "contents": bubbles}
        line_bot_api.reply_message(
            reply_token,
            FlexSendMessage(alt_text=f"未承認の下書き {len(drafts)}件", contents=flex_message)
        )

    except Exception as e:
        log_error("PENDING_DRAFTS_ERROR", f"Error showing pending drafts: {e}", error=e)
        line_bot_api.reply_message(reply_token, TextMessage(text=f"エラーが発生しました: {str(e)[:50]}"))

def show_trend_summary(line_bot_api, user_id):
    """Show current trends without generating articles."""
    from src.fetch_trends import TrendFetcher
    from linebot.models import FlexSendMessage, TextMessage
    from linebot import LineBotApi

    try:
        fetcher = TrendFetcher(os.environ.get("GEMINI_API_KEY"))
        trends = fetcher.fetch_trends(include_kpop=True)

        if not trends:
            line_bot_api_push = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
            line_bot_api_push.push_message(user_id, TextMessage(text="📭 現在トレンドが見つかりませんでした。"))
            return

        trends = trends[:6]
        category_emojis = {
            'artist': '🎤', 'beauty': '💄', 'fashion': '👗',
            'food': '🍜', 'travel': '✈️', 'event': '🎉',
            'drama': '📺', 'other': '📰', 'trend': '🔥'
        }

        trend_items = []
        for i, trend in enumerate(trends, 1):
            title = trend.get('title', '不明')[:40]
            snippet = trend.get('snippet', '')[:60]
            category = trend.get('category', 'other')
            emoji = category_emojis.get(category, '📰')
            trend_items.append({
                "type": "box", "layout": "horizontal", "margin": "lg",
                "contents": [
                    {"type": "text", "text": f"{emoji}", "size": "xl", "flex": 0},
                    {"type": "box", "layout": "vertical", "flex": 5, "margin": "md", "contents": [
                        {"type": "text", "text": title, "weight": "bold", "size": "sm", "wrap": True, "maxLines": 2},
                        {"type": "text", "text": snippet + "..." if snippet else "", "size": "xs", "color": "#888888", "wrap": True, "maxLines": 2, "margin": "sm"}
                    ]}
                ]
            })
            if i < len(trends):
                trend_items.append({"type": "separator", "margin": "md"})

        flex_message = {
            "type": "bubble", "size": "mega",
            "header": {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": "🔥 今日のトレンド", "weight": "bold", "size": "xl", "color": "#ffffff"}
            ], "backgroundColor": "#1DB446", "paddingAll": "15px"},
            "body": {"type": "box", "layout": "vertical", "contents": trend_items},
            "footer": {"type": "box", "layout": "vertical", "contents": [
                {"type": "button", "style": "primary", "action": {"type": "message", "label": "📝 記事を生成", "text": "カテゴリ"}}
            ]}
        }

        line_bot_api_push = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
        line_bot_api_push.push_message(user_id, FlexSendMessage(alt_text=f"今日のトレンド {len(trends)}件", contents=flex_message))
        log_event("TREND_SUMMARY_SENT", f"Showed {len(trends)} trends")

    except Exception as e:
        log_error("TREND_SUMMARY_ERROR", f"Trend summary error: {e}", error=e)
        try:
            line_bot_api_push = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
            line_bot_api_push.push_message(user_id, TextMessage(text=f"エラー: {str(e)[:50]}"))
        except:
            pass

def search_articles(keyword: str, line_bot_api, user_id: str):
    """Search published articles by keyword."""
    from src.storage_manager import StorageManager
    from linebot.models import FlexSendMessage, TextMessage
    from linebot import LineBotApi

    try:
        storage = StorageManager()
        articles_ref = storage.db.collection(storage.collection_name) \
            .where('status', '==', 'approved') \
            .order_by('created_at', direction='DESCENDING') \
            .limit(50)

        articles = list(articles_ref.stream())
        keyword_lower = keyword.lower()
        matching_articles = []

        for doc in articles:
            article = doc.to_dict()
            title = article.get('cms_content', {}).get('title', '').lower()
            body = article.get('cms_content', {}).get('body', '').lower()
            category = article.get('trend_source', {}).get('category', '').lower()

            if keyword_lower in title or keyword_lower in body or keyword_lower in category:
                matching_articles.append({
                    'id': doc.id,
                    'title': article.get('cms_content', {}).get('title', '無題')[:35],
                    'url': article.get('wordpress_url', ''),
                    'category': article.get('trend_source', {}).get('category', 'other')
                })
            if len(matching_articles) >= 5:
                break

        line_bot_api_push = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))

        if not matching_articles:
            line_bot_api_push.push_message(user_id, TextMessage(text=f"🔍 「{keyword}」に一致する記事が見つかりませんでした。"))
            return

        category_emojis = {
            'artist': '🎤', 'beauty': '💄', 'fashion': '👗',
            'food': '🍜', 'travel': '✈️', 'event': '🎉',
            'drama': '📺', 'other': '📰', 'trend': '🔥'
        }

        result_items = []
        for article in matching_articles:
            emoji = category_emojis.get(article['category'], '📰')
            result_items.append({
                "type": "box", "layout": "horizontal", "margin": "lg",
                "contents": [
                    {"type": "text", "text": emoji, "size": "xl", "flex": 0},
                    {"type": "box", "layout": "vertical", "flex": 5, "margin": "md", "contents": [
                        {"type": "text", "text": article['title'], "weight": "bold", "size": "sm", "wrap": True, "maxLines": 2},
                        {"type": "button", "style": "link", "height": "sm", "action": {
                            "type": "uri", "label": "記事を見る",
                            "uri": article['url'] if article['url'] else "https://k-trendtimes.com"
                        }} if article['url'] else {"type": "filler"}
                    ]}
                ]
            })

        flex_message = {
            "type": "bubble",
            "header": {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": f"🔍 「{keyword}」の検索結果", "weight": "bold", "size": "md", "color": "#ffffff", "wrap": True}
            ], "backgroundColor": "#0277BD", "paddingAll": "15px"},
            "body": {"type": "box", "layout": "vertical", "contents": result_items},
            "footer": {"type": "box", "layout": "vertical", "contents": [
                {"type": "text", "text": f"{len(matching_articles)}件の記事が見つかりました", "size": "xs", "color": "#888888", "align": "center"}
            ]}
        }

        line_bot_api_push.push_message(user_id, FlexSendMessage(alt_text=f"検索結果: {len(matching_articles)}件", contents=flex_message))
        log_event("SEARCH_COMPLETE", f"Found {len(matching_articles)} articles for '{keyword}'")

    except Exception as e:
        log_error("SEARCH_ERROR", f"Search error: {e}", error=e)
        try:
            line_bot_api_push = LineBotApi(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
            line_bot_api_push.push_message(user_id, TextMessage(text=f"検索エラー: {str(e)[:50]}"))
        except:
            pass
