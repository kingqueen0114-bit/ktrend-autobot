"""
K-Trend AutoBot Configuration Management
"""

import os
from typing import List, Optional


# Required environment variables
REQUIRED_ENV_VARS = [
    "GEMINI_API_KEY",
    "LINE_CHANNEL_ACCESS_TOKEN",
    "LINE_CHANNEL_SECRET",
    "LINE_USER_ID",
    "GCP_PROJECT_ID",
]

# Optional environment variables
OPTIONAL_ENV_VARS = [
    "GOOGLE_CUSTOM_SEARCH_API_KEY",
    "GOOGLE_CSE_ID",
    "WORDPRESS_URL",
    "WORDPRESS_USER",
    "WORDPRESS_APP_PASSWORD",
    "X_API_KEY",
    "X_API_KEY_SECRET",
    "X_ACCESS_TOKEN",
    "X_ACCESS_TOKEN_SECRET",
    "X_BEARER_TOKEN",
]


def validate_env_vars() -> List[str]:
    """
    Validate that all required environment variables are set.

    Returns:
        List of missing environment variable names
    """
    missing = []
    for var in REQUIRED_ENV_VARS:
        if not os.environ.get(var):
            missing.append(var)
    return missing


def log_config_status(logger) -> None:
    """
    Log the current configuration status.

    Args:
        logger: Logger instance to use for output
    """
    logger.info("=== Configuration Status ===")

    # Check required vars
    for var in REQUIRED_ENV_VARS:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            masked = value[:4] + "..." + value[-4:] if len(value) > 10 else "***"
            logger.info(f"  {var}: {masked}")
        else:
            logger.warning(f"  {var}: NOT SET")

    # Check optional vars
    for var in OPTIONAL_ENV_VARS:
        value = os.environ.get(var)
        if value:
            logger.info(f"  {var}: SET")
        else:
            logger.debug(f"  {var}: not set (optional)")

    logger.info("============================")


def get_config() -> dict:
    """
    Get the current configuration as a dictionary.

    Returns:
        Dictionary of configuration values
    """
    config = {}

    for var in REQUIRED_ENV_VARS + OPTIONAL_ENV_VARS:
        config[var] = os.environ.get(var)

    return config
