"""
Utility helper functions for K-Trend AutoBot.
Includes initialization, retry logic, error recovery, and hashtag generation.
"""
import time
import functools
from datetime import datetime

from src.storage_manager import StorageManager
from src.config import validate_env_vars, log_config_status
from src.exceptions import ConfigurationError
from utils.logging_config import logger, log_event, log_error


def func_init():
    """
    Initialize the Cloud Function.
    Validates required environment variables at startup.
    """
    missing_vars = validate_env_vars()
    if missing_vars:
        log_error(
            "CONFIG_ERROR",
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
        log_config_status(logger)
        raise ConfigurationError(missing_vars)

    log_event("INIT", "Cloud Function initialized successfully")


def retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay on each retry
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        log_error("RETRY", f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {str(e)[:100]}")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        log_error("RETRY_EXHAUSTED", f"All {max_retries + 1} attempts failed for {func.__name__}", error=e)

            raise last_exception
        return wrapper
    return decorator


def safe_api_call(func, *args, default=None, error_context="API call", **kwargs):
    """
    Execute a function safely with error handling.

    Args:
        func: Function to call
        default: Default value to return on failure
        error_context: Context for error logging

    Returns:
        Function result or default value
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_error("SAFE_CALL_FAILED", f"{error_context}: {str(e)[:100]}", error=e)
        return default


def recover_failed_draft(draft_id: str) -> bool:
    """
    Attempt to recover a draft that failed during processing.

    Args:
        draft_id: ID of the draft to recover

    Returns:
        True if recovery was successful
    """
    try:
        storage = StorageManager()
        draft_ref = storage.db.collection(storage.collection_name).document(draft_id)
        draft = draft_ref.get()

        if not draft.exists:
            log_error("RECOVERY_FAILED", f"Draft {draft_id} not found")
            return False

        draft_data = draft.to_dict()
        status = draft_data.get('status', '')
        error_state = draft_data.get('error_state', {})

        # Check if draft is in error state
        if not error_state and status not in ['error', 'failed']:
            log_event("RECOVERY_SKIPPED", f"Draft {draft_id} is not in error state")
            return True

        # Attempt recovery based on error type
        error_type = error_state.get('type', 'unknown')
        last_action = error_state.get('last_action', '')

        if error_type == 'wordpress_publish' or last_action == 'publish':
            # Re-attempt WordPress publish
            log_event("RECOVERY_ATTEMPT", f"Retrying WordPress publish for {draft_id}")
            cms_content = draft_data.get('cms_content', {})
            image_id = draft_data.get('wordpress_image_id')

            result = storage.publish_to_wordpress(cms_content, image_id)
            if result.get('url'):
                draft_ref.update({
                    'status': 'approved',
                    'wordpress_url': result['url'],
                    'wordpress_post_id': result.get('post_id'),
                    'error_state': {},
                    'recovered_at': datetime.now().isoformat()
                })
                log_event("RECOVERY_SUCCESS", f"Draft {draft_id} recovered - published to WordPress")
                return True

        elif error_type == 'image_upload' or last_action == 'image_upload':
            # Re-attempt image upload
            log_event("RECOVERY_ATTEMPT", f"Retrying image upload for {draft_id}")
            image_url = draft_data.get('original_image_url', draft_data.get('image_url', ''))

            if image_url:
                wp_image = storage.upload_image_to_wordpress(image_url)
                if wp_image:
                    draft_ref.update({
                        'wordpress_image_id': wp_image.get('id'),
                        'image_url': wp_image.get('url', image_url),
                        'error_state': {},
                        'recovered_at': datetime.now().isoformat()
                    })
                    log_event("RECOVERY_SUCCESS", f"Draft {draft_id} image recovered")
                    return True

        # Generic recovery: reset to draft status
        draft_ref.update({
            'status': 'draft',
            'error_state': {},
            'recovery_attempted_at': datetime.now().isoformat()
        })
        log_event("RECOVERY_RESET", f"Draft {draft_id} reset to draft status")
        return True

    except Exception as e:
        log_error("RECOVERY_ERROR", f"Failed to recover draft {draft_id}: {str(e)[:100]}", error=e)
        return False


def mark_draft_error(draft_id: str, error_type: str, error_message: str, last_action: str = ""):
    """
    Mark a draft as having an error for later recovery.

    Args:
        draft_id: ID of the draft
        error_type: Type of error
        error_message: Error details
        last_action: Last action attempted before error
    """
    try:
        storage = StorageManager()
        draft_ref = storage.db.collection(storage.collection_name).document(draft_id)

        draft_ref.update({
            'error_state': {
                'type': error_type,
                'message': error_message[:500],
                'last_action': last_action,
                'timestamp': datetime.now().isoformat()
            },
            'status': 'error'
        })
        log_event("DRAFT_ERROR_MARKED", f"Draft {draft_id} marked with error: {error_type}")

    except Exception as e:
        log_error("MARK_ERROR_FAILED", f"Could not mark draft {draft_id} error: {str(e)[:50]}", error=e)


def generate_hashtags(category: str, title: str) -> list:
    """
    Generate relevant hashtags based on category and title.

    Args:
        category: Article category (artist, beauty, fashion, etc.)
        title: Article title

    Returns:
        List of hashtags (without # prefix added here)
    """
    # Category-specific popular hashtags
    category_tags = {
        'artist': ['#Kpop', '#韓国アイドル', '#KPOPFAN', '#推し活'],
        'beauty': ['#韓国コスメ', '#韓国美容', '#スキンケア', '#コスメ好きさんと繋がりたい'],
        'fashion': ['#韓国ファッション', '#韓国通販', '#オルチャン', '#韓国コーデ'],
        'food': ['#韓国グルメ', '#韓国料理', '#韓国カフェ', '#韓国旅行'],
        'travel': ['#韓国旅行', '#ソウル旅行', '#韓国観光', '#渡韓'],
        'event': ['#Kpopコンサート', '#韓国イベント', '#Kpopライブ', '#韓国エンタメ'],
        'drama': ['#韓国ドラマ', '#韓ドラ', '#Netflix韓国', '#韓ドラ好きと繋がりたい'],
        'other': ['#韓国トレンド', '#韓国情報', '#韓国好き', '#韓国カルチャー']
    }

    # Get base tags for category
    tags = category_tags.get(category, category_tags['other'])[:3]

    # Add common trending tags
    common_tags = ['#韓国', '#KTrendTimes']

    # Extract keywords from title for additional tags
    title_lower = title.lower()

    # Artist name detection (common K-pop groups)
    artist_keywords = {
        'bts': '#BTS', 'blackpink': '#BLACKPINK', 'twice': '#TWICE',
        'aespa': '#aespa', 'ive': '#IVE', 'newjeans': '#NewJeans',
        'stray kids': '#StrayKids', 'seventeen': '#SEVENTEEN',
        'nct': '#NCT', 'exo': '#EXO', 'red velvet': '#RedVelvet',
        'itzy': '#ITZY', 'txt': '#TXT', 'enhypen': '#ENHYPEN',
        'le sserafim': '#LESSERAFIM', 'ateez': '#ATEEZ',
        'straykids': '#StrayKids', 'gidle': '#GIDLE'
    }

    for keyword, tag in artist_keywords.items():
        if keyword in title_lower:
            tags.insert(0, tag)
            break

    # Combine and limit to 5 tags
    all_tags = tags + common_tags
    return list(dict.fromkeys(all_tags))[:5]  # Remove duplicates, limit to 5
