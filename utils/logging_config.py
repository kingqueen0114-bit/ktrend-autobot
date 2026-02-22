"""
Structured logging configuration for K-Trend AutoBot.
Provides Cloud Logging compatible JSON output.
"""
import json
import logging
import sys
from datetime import datetime


class StructuredLogFormatter(logging.Formatter):
    """Custom formatter that outputs JSON for Cloud Logging."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "function": record.funcName,
        }

        # Add extra fields if present
        if hasattr(record, 'trend_title'):
            log_entry['trend_title'] = record.trend_title
        if hasattr(record, 'draft_id'):
            log_entry['draft_id'] = record.draft_id
        if hasattr(record, 'error_type'):
            log_entry['error_type'] = record.error_type
        if hasattr(record, 'duration_ms'):
            log_entry['duration_ms'] = record.duration_ms
        if hasattr(record, 'stats'):
            log_entry['stats'] = record.stats

        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging():
    """Setup structured logging for Cloud Functions."""
    _logger = logging.getLogger('ktrend')
    _logger.setLevel(logging.INFO)

    # Remove existing handlers
    _logger.handlers = []

    # Add structured handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredLogFormatter())
    _logger.addHandler(handler)

    return _logger


# Module-level logger singleton
logger = setup_logging()


def log_event(event_type: str, message: str, **extra):
    """Helper function for structured logging."""
    record = logging.LogRecord(
        name='ktrend',
        level=logging.INFO,
        pathname='',
        lineno=0,
        msg=f"[{event_type}] {message}",
        args=(),
        exc_info=None
    )
    for key, value in extra.items():
        setattr(record, key, value)
    logger.handle(record)


def log_error(event_type: str, message: str, error: Exception = None, **extra):
    """Helper function for error logging."""
    record = logging.LogRecord(
        name='ktrend',
        level=logging.ERROR,
        pathname='',
        lineno=0,
        msg=f"[{event_type}] {message}",
        args=(),
        exc_info=(type(error), error, error.__traceback__) if error else None
    )
    record.error_type = event_type
    for key, value in extra.items():
        setattr(record, key, value)
    logger.handle(record)
