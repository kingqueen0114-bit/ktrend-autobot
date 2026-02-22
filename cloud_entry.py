"""
K-Trend AutoBot - Cloud Entry Point (Router)
=============================================
Thin routing layer that delegates to handler modules.

Modules:
  - handlers/schedulers.py   : trigger_daily_fetch, trigger_stats_report, trigger_progress_report
  - handlers/webhook.py      : handle_line_webhook
  - handlers/line_actions.py  : LINE postback/message action handlers
  - handlers/draft_editor.py  : view_draft (HTML editor form)
  - utils/logging_config.py   : Structured logging
  - utils/helpers.py           : Utility functions (retry, recovery, hashtags)
"""
import functions_framework
import json

# Re-export all handler functions so main.py and Cloud Functions can import them
from handlers.schedulers import trigger_daily_fetch, trigger_stats_report, trigger_progress_report
from handlers.webhook import handle_line_webhook
from handlers.draft_editor import view_draft
from handlers.generation_actions import (
    process_ondemand_text,
    process_ondemand_image,
    process_category_generate,
)
from handlers.draft_actions import (
    process_approval,
    process_rejection,
    process_regenerate,
    process_regenerate_article,
    process_approve_all,
    process_schedule,
    recover_failed_drafts,
)
from handlers.edit_actions import (
    store_edit_session,
    get_edit_session,
    show_quick_edit_options,
    process_edit_text,
)
from handlers.info_actions import (
    show_pending_drafts,
    show_trend_summary,
    search_articles,
)

# Re-export utilities for backward compatibility
from utils.logging_config import setup_logging, log_event, log_error, StructuredLogFormatter
from utils.helpers import (
    func_init,
    retry_with_backoff,
    safe_api_call,
    recover_failed_draft,
    mark_draft_error,
    generate_hashtags,
)


@functions_framework.http
def main(request):
    """
    Main entry point that routes requests to appropriate handlers.
    """
    # Check for action in JSON body (handle both JSON and octet-stream from Cloud Scheduler)
    data = {}
    if request.is_json:
        data = request.get_json(silent=True) or {}
    elif request.method == 'POST' and request.data:
        try:
            data = json.loads(request.data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    action = data.get('action', '')

    if action == 'fetch_trends':
        return trigger_daily_fetch(request)
    if action == 'stats_report':
        return trigger_stats_report(request)
    if action == 'progress_report':
        return trigger_progress_report(request)

    # Check for view_draft request (has 'id' parameter)
    if 'id' in request.args and not request.path == '/drafts':
        return view_draft(request)

    # Route /drafts path to the new article list handler
    if request.path == '/drafts':
        from handlers.draft_editor import view_article_list
        return view_article_list(request)

    # Check for LINE signature header (webhook)
    if request.headers.get('X-Line-Signature'):
        return handle_line_webhook(request)

    # Default: health check
    if request.method == 'GET':
        return "K-Trend AutoBot is running", 200

    # Try webhook for POST without specific action
    return handle_line_webhook(request)
