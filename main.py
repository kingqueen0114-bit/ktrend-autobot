import os
import functions_framework
from dotenv import load_dotenv
from cloud_entry import trigger_daily_fetch, handle_line_webhook, view_draft, trigger_stats_report, trigger_progress_report

# Load environment variables
load_dotenv()

class MockRequest:
    def __init__(self, data=None, headers=None):
        self.data = data or {}
        self.headers = headers or {}

    def get_data(self, as_text=False):
        return self.data if not as_text else str(self.data)


@functions_framework.http
def main(request):
    """
    Cloud Functions entry point that routes requests.
    """
    import json as json_lib

    # Check for action in JSON body (handle both JSON and octet-stream from Cloud Scheduler)
    data = {}
    if request.is_json:
        data = request.get_json(silent=True) or {}
    elif request.method == 'POST' and request.data:
        # Try to parse body as JSON even if content-type is not application/json
        try:
            data = json_lib.loads(request.data.decode('utf-8'))
        except (json_lib.JSONDecodeError, UnicodeDecodeError):
            pass

    action = data.get('action', '')
    if action == 'fetch_trends':
        return trigger_daily_fetch(request)
    if action == 'stats_report':
        return trigger_stats_report(request)
    if action == 'progress_report':
        return trigger_progress_report(request)

    # Path-based routing
    path = request.path or ''

    # Handle /draft/{id} path
    if path.startswith('/draft/'):
        draft_id = path.split('/draft/')[-1].strip('/')
        if draft_id:
            # Inject draft_id into request args for view_draft
            from werkzeug.datastructures import ImmutableMultiDict
            if not request.args.get('id'):
                request.args = ImmutableMultiDict({**request.args, 'id': draft_id})
            return view_draft(request)

    # Check for view_draft request (has 'id' parameter - legacy support)
    if 'id' in request.args and not path == '/drafts':
        return view_draft(request)

    # Handle /drafts path for article list
    if path == '/drafts':
        from handlers.draft_editor import view_article_list
        return view_article_list(request)

    # Handle /webhook path or LINE signature header
    if path == '/webhook' or request.headers.get('X-Line-Signature'):
        return handle_line_webhook(request)

    # Default: health check
    if request.method == 'GET':
        return "K-Trend AutoBot is running", 200

    # Try webhook for POST without specific action
    return handle_line_webhook(request)


def run_local():
    print("K-Trend AutoBot: Starting Local CMS Integration Test...")
    
    
    # Check for critical env vars
    if not os.getenv("GCP_SA_KEY_PATH"):
        print("\n[!] Warning: 'GCP_SA_KEY_PATH' is not set in .env")
        print("    Firestore/GCS/Sheets operations will fail without service account credentials.")
    
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "webhook":
        # Simulate Webhook
        draft_id = sys.argv[2]
        print(f"\n--- Simulating Webhook for Draft ID: {draft_id} ---")
        
        # Mock Request object expected by cloud_entry
        class MockRequestObj:
            def __init__(self, json_data, headers):
                self._json = json_data
                self.headers = headers
            def get_data(self, as_text=True):
                import json
                return json.dumps(self._json)
        
        # Construct Postback Payload
        # We need to mock the signature verification or bypass it.
        # Since logic handles signature, we might need to bypass it for local test 
        # OR we just invoke process_approval directly if we want to be lazy.
        # But let's try to call the entry point to be sure.
        # Wait, signature relies on Channel Secret. If we use valid secret, we neeed valid signature.
        # Generating signature locally is annoying.
        # Let's import process_approval directly for local test to bypass security checks.
        
        from cloud_entry import process_approval
        # Need line bot api instance
        from linebot import LineBotApi
        from linebot.models import TextMessage
        
        line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
        
        # Mock Reply Token (won't work for real reply, but function might trigger)
        # Actually without real reply token, reply_message will fail.
        # We should mock line_bot_api too?
        
        print(">> Calling process_approval directly (Bypassing Signature & Reply)...")
        
        # Mock LineBotApi to prevent error on reply
        class MockLineBotApi:
            def reply_message(self, token, messages):
                print(f"[Mock Reply] Token: {token}")
                if isinstance(messages, (list, tuple)):
                    for m in messages:
                        print(f"[Mock Reply] Message: {m.text}")
                else:
                    print(f"[Mock Reply] Message: {messages.text}")

        process_approval(draft_id, MockLineBotApi(), "mock_reply_token")
        
    else:
        # Simulate Daily Fetch Logic
        print("\n--- Triggering Daily Fetch (Simulating Cloud Scheduler) ---")
        response, status = trigger_daily_fetch(None)
        print(f"\nResponse: {response}")
        print(f"Status: {status}")

        if status == 200:
            print("\n[Next Steps]")
            print("1. Check your LINE for the 'Approval Request'.")
            print("2. To test publishing locally, run:")
            # Extract Draft ID if possible, or generic msg
            # Response: "OK. Draft: xyz"
            try:
                draft = response.split("Draft: ")[1].strip()
                print(f"   python3 main.py webhook {draft}")
            except:
                print("   python3 main.py webhook <draft_id>")

if __name__ == "__main__":
    run_local()
