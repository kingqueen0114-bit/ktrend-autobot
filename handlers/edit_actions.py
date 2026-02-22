"""
Edit action handlers for K-Trend AutoBot.
Handles editing draft titles, content, and session management.
"""
import os
from utils.logging_config import log_event, log_error

def store_edit_session(user_id: str, draft_id: str, edit_type: str):
    """Store an edit session for a user."""
    from src.storage_manager import StorageManager
    storage = StorageManager()
    storage.store_edit_session(user_id, draft_id, edit_type)
    log_event("EDIT_SESSION_STORED", f"User {user_id[:10]}... editing {edit_type} for {draft_id}")

def get_edit_session(user_id: str) -> dict:
    """Get and clear an edit session for a user."""
    from src.storage_manager import StorageManager
    storage = StorageManager()
    return storage.get_edit_session(user_id)

def show_quick_edit_options(draft_id: str, line_bot_api, reply_token):
    """Show quick edit options for a draft using Flex Message buttons."""
    try:
        from linebot.models import FlexSendMessage
        log_event("QUICK_EDIT", f"Showing edit options for draft: {draft_id}")

        flex_contents = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "📝 編集オプション", "weight": "bold", "size": "lg", "color": "#1DB446"},
                    {"type": "text", "text": "選択してください", "size": "sm", "color": "#999999", "margin": "sm"}
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {"type": "button", "style": "primary", "height": "sm", "action": {"type": "postback", "label": "✏️ タイトル編集", "data": f"action=edit_title&draft_id={draft_id}", "displayText": "タイトルを編集"}},
                    {"type": "button", "style": "primary", "height": "sm", "action": {"type": "postback", "label": "📝 メタ説明編集", "data": f"action=edit_meta&draft_id={draft_id}", "displayText": "メタ説明を編集"}},
                    {"type": "button", "style": "secondary", "height": "sm", "action": {"type": "postback", "label": "🔄 記事再生成", "data": f"action=regenerate_article&draft_id={draft_id}", "displayText": "記事を再生成"}},
                    {"type": "button", "style": "link", "height": "sm", "action": {"type": "uri", "label": "🌐 WPで編集", "uri": f"https://asia-northeast1-k-trend-autobot.cloudfunctions.net/view-draft?id={draft_id}"}},
                    {"type": "button", "style": "link", "height": "sm", "action": {"type": "postback", "label": "❌ キャンセル", "data": "action=done", "displayText": "キャンセル"}}
                ]
            }
        }
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text="編集オプション", contents=flex_contents))
        log_event("QUICK_EDIT", "Edit options sent successfully")

    except Exception as e:
        log_error("QUICK_EDIT_ERROR", f"Failed to show edit options: {str(e)}", error=e)
        try:
            from linebot.models import TextMessage
            line_bot_api.reply_message(reply_token, TextMessage(text=f"❌ 編集オプションの表示に失敗しました。\nview-draft URLから編集してください:\nhttps://asia-northeast1-k-trend-autobot.cloudfunctions.net/view-draft?id={draft_id}"))
        except Exception as fallback_error:
            log_error("QUICK_EDIT_FALLBACK_ERROR", f"Fallback also failed: {str(fallback_error)}")

def process_edit_text(user_id: str, text: str, line_bot_api) -> bool:
    """Process edit text input from user. Returns True if edit was processed."""
    from src.storage_manager import StorageManager
    from src.notifier import Notifier

    session = get_edit_session(user_id)
    if not session:
        return False

    draft_id = session['draft_id']
    edit_type = session['edit_type']
    storage = StorageManager()
    notifier = Notifier(os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"), os.environ.get("LINE_USER_ID"))

    try:
        draft_ref = storage.db.collection(storage.collection_name).document(draft_id)
        draft = draft_ref.get()

        if not draft.exists:
            notifier.send_error_notification("EDIT_ERROR", f"Draft {draft_id} not found")
            return True

        draft_data = draft.to_dict()
        cms_content = draft_data.get('cms_content', {})

        if edit_type == 'title':
            new_title = text.strip()[:100]
            cms_content['title'] = new_title
            draft_ref.update({'cms_content': cms_content})
            log_event("EDIT_TITLE", f"Draft {draft_id} title updated to: {new_title[:30]}...")

            import requests, json
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')}"}
            payload = {"to": user_id, "messages": [{"type": "text", "text": f"✅ タイトルを更新しました:\n「{new_title}」"}]}
            requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)

        elif edit_type == 'meta':
            new_meta = text.strip()[:160]
            cms_content['meta_description'] = new_meta
            draft_ref.update({'cms_content': cms_content})
            log_event("EDIT_META", f"Draft {draft_id} meta updated")

            import requests
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')}"}
            payload = {"to": user_id, "messages": [{"type": "text", "text": f"✅ メタ説明を更新しました:\n「{new_meta}」"}]}
            requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)

        return True

    except Exception as e:
        log_error("EDIT_FAILED", str(e), f"draft_id={draft_id}, edit_type={edit_type}")
        return True
