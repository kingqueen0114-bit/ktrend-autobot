"""
K-Trend AutoBot Custom Exceptions
"""


class KTrendError(Exception):
    """Base exception for K-Trend AutoBot."""
    pass


class ConfigurationError(KTrendError):
    """Raised when there's a configuration error."""
    pass


class GeminiAPIError(KTrendError):
    """Raised when Gemini API call fails."""
    pass


class WordPressAPIError(KTrendError):
    """Raised when WordPress API call fails."""
    pass


class LINEAPIError(KTrendError):
    """Raised when LINE API call fails."""
    pass


class ContentGenerationError(KTrendError):
    """Raised when content generation fails."""
    pass


class DraftNotFoundError(KTrendError):
    """Raised when a draft is not found."""
    pass
