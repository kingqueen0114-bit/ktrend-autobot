"""src/config.py のユニットテスト"""
import os
import pytest
from unittest.mock import MagicMock, patch, call


class TestValidateEnvVars:
    """validate_env_vars関数のテスト"""

    def test_all_required_vars_set(self):
        """全ての必須環境変数が設定されている場合、空リストが返される"""
        from src.config import validate_env_vars

        # conftest.py の autouse フィクスチャで環境変数は設定済み
        result = validate_env_vars()
        assert result == []

    def test_missing_single_var(self, monkeypatch):
        """1つの必須環境変数が未設定の場合"""
        from src.config import validate_env_vars

        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        result = validate_env_vars()
        assert "GEMINI_API_KEY" in result

    def test_missing_multiple_vars(self, monkeypatch):
        """複数の必須環境変数が未設定の場合"""
        from src.config import validate_env_vars

        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        monkeypatch.delenv("LINE_CHANNEL_ACCESS_TOKEN", raising=False)
        result = validate_env_vars()
        assert "GEMINI_API_KEY" in result
        assert "LINE_CHANNEL_ACCESS_TOKEN" in result

    def test_all_required_vars_missing(self, monkeypatch):
        """全ての必須環境変数が未設定の場合"""
        from src.config import validate_env_vars, REQUIRED_ENV_VARS

        for var in REQUIRED_ENV_VARS:
            monkeypatch.delenv(var, raising=False)
        result = validate_env_vars()
        assert set(result) == set(REQUIRED_ENV_VARS)

    def test_empty_string_treated_as_missing(self, monkeypatch):
        """空文字列は未設定として扱われる"""
        from src.config import validate_env_vars

        monkeypatch.setenv("GEMINI_API_KEY", "")
        result = validate_env_vars()
        assert "GEMINI_API_KEY" in result

    def test_optional_vars_not_checked(self, monkeypatch):
        """オプション環境変数はバリデーション対象外"""
        from src.config import validate_env_vars, OPTIONAL_ENV_VARS

        for var in OPTIONAL_ENV_VARS:
            monkeypatch.delenv(var, raising=False)
        result = validate_env_vars()
        # オプション変数が欠けていてもエラーにならない
        for var in OPTIONAL_ENV_VARS:
            assert var not in result

    def test_returns_list_type(self):
        """戻り値がリスト型であること"""
        from src.config import validate_env_vars

        result = validate_env_vars()
        assert isinstance(result, list)


class TestLogConfigStatus:
    """log_config_status関数のテスト"""

    def test_logs_header_and_footer(self):
        """ヘッダーとフッターのログが出力される"""
        from src.config import log_config_status

        mock_logger = MagicMock()
        log_config_status(mock_logger)

        # info の呼び出しにヘッダーとフッターが含まれること
        info_calls = [c.args[0] for c in mock_logger.info.call_args_list]
        assert "=== Configuration Status ===" in info_calls
        assert "============================" in info_calls

    def test_logs_set_required_vars(self):
        """設定済みの必須環境変数がマスクされてログ出力される"""
        from src.config import log_config_status

        mock_logger = MagicMock()
        log_config_status(mock_logger)

        info_calls = [c.args[0] for c in mock_logger.info.call_args_list]
        # GEMINI_API_KEY は設定済み（conftest.py の test-gemini-key）
        # 長さ10以下なので *** でマスクされる
        gemini_log = [c for c in info_calls if "GEMINI_API_KEY" in c]
        assert len(gemini_log) > 0

    def test_logs_missing_required_vars_as_warning(self, monkeypatch):
        """未設定の必須環境変数がwarningでログ出力される"""
        from src.config import log_config_status

        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        mock_logger = MagicMock()
        log_config_status(mock_logger)

        warning_calls = [c.args[0] for c in mock_logger.warning.call_args_list]
        gemini_warning = [c for c in warning_calls if "GEMINI_API_KEY" in c]
        assert len(gemini_warning) > 0
        assert "NOT SET" in gemini_warning[0]

    def test_logs_set_optional_vars(self):
        """設定済みのオプション環境変数がログ出力される"""
        from src.config import log_config_status

        mock_logger = MagicMock()
        log_config_status(mock_logger)

        info_calls = [c.args[0] for c in mock_logger.info.call_args_list]
        # WORDPRESS_URL は conftest.py で設定済み
        wp_log = [c for c in info_calls if "WORDPRESS_URL" in c]
        assert len(wp_log) > 0
        assert "SET" in wp_log[0]

    def test_logs_missing_optional_vars_as_debug(self, monkeypatch):
        """未設定のオプション環境変数がdebugでログ出力される"""
        from src.config import log_config_status

        monkeypatch.delenv("X_API_KEY", raising=False)
        mock_logger = MagicMock()
        log_config_status(mock_logger)

        debug_calls = [c.args[0] for c in mock_logger.debug.call_args_list]
        x_debug = [c for c in debug_calls if "X_API_KEY" in c and "X_API_KEY_SECRET" not in c]
        assert len(x_debug) > 0

    def test_masks_long_values(self, monkeypatch):
        """10文字以上の値は先頭4文字...末尾4文字にマスクされる"""
        from src.config import log_config_status

        monkeypatch.setenv("GEMINI_API_KEY", "abcdefghijklmnop")
        mock_logger = MagicMock()
        log_config_status(mock_logger)

        info_calls = [c.args[0] for c in mock_logger.info.call_args_list]
        gemini_log = [c for c in info_calls if "GEMINI_API_KEY" in c]
        assert len(gemini_log) > 0
        # "abcd...mnop" のようなマスク形式
        assert "abcd" in gemini_log[0]
        assert "mnop" in gemini_log[0]
        assert "..." in gemini_log[0]

    def test_masks_short_values(self, monkeypatch):
        """10文字以下の値は *** でマスクされる"""
        from src.config import log_config_status

        monkeypatch.setenv("GEMINI_API_KEY", "short")
        mock_logger = MagicMock()
        log_config_status(mock_logger)

        info_calls = [c.args[0] for c in mock_logger.info.call_args_list]
        gemini_log = [c for c in info_calls if "GEMINI_API_KEY" in c]
        assert len(gemini_log) > 0
        assert "***" in gemini_log[0]


class TestGetConfig:
    """get_config関数のテスト"""

    def test_returns_dict(self):
        """戻り値が辞書型であること"""
        from src.config import get_config

        result = get_config()
        assert isinstance(result, dict)

    def test_contains_required_vars(self):
        """必須環境変数が辞書に含まれる"""
        from src.config import get_config, REQUIRED_ENV_VARS

        result = get_config()
        for var in REQUIRED_ENV_VARS:
            assert var in result

    def test_contains_optional_vars(self):
        """オプション環境変数が辞書に含まれる"""
        from src.config import get_config, OPTIONAL_ENV_VARS

        result = get_config()
        for var in OPTIONAL_ENV_VARS:
            assert var in result

    def test_returns_correct_values(self):
        """環境変数の値が正しく返される"""
        from src.config import get_config

        result = get_config()
        # conftest.py で設定された値
        assert result["GEMINI_API_KEY"] == "test-gemini-key"
        assert result["GCP_PROJECT_ID"] == "test-project"

    def test_missing_var_returns_none(self, monkeypatch):
        """未設定の環境変数はNoneになる"""
        from src.config import get_config

        monkeypatch.delenv("X_BEARER_TOKEN", raising=False)
        result = get_config()
        assert result["X_BEARER_TOKEN"] is None


class TestRequiredEnvVars:
    """REQUIRED_ENV_VARS定数のテスト"""

    def test_required_vars_is_list(self):
        """REQUIRED_ENV_VARSがリストであること"""
        from src.config import REQUIRED_ENV_VARS

        assert isinstance(REQUIRED_ENV_VARS, list)

    def test_required_vars_not_empty(self):
        """REQUIRED_ENV_VARSが空でないこと"""
        from src.config import REQUIRED_ENV_VARS

        assert len(REQUIRED_ENV_VARS) > 0

    def test_required_vars_contains_essential_keys(self):
        """最低限必要なキーが含まれていること"""
        from src.config import REQUIRED_ENV_VARS

        assert "GEMINI_API_KEY" in REQUIRED_ENV_VARS
        assert "LINE_CHANNEL_ACCESS_TOKEN" in REQUIRED_ENV_VARS
        assert "GCP_PROJECT_ID" in REQUIRED_ENV_VARS


class TestOptionalEnvVars:
    """OPTIONAL_ENV_VARS定数のテスト"""

    def test_optional_vars_is_list(self):
        """OPTIONAL_ENV_VARSがリストであること"""
        from src.config import OPTIONAL_ENV_VARS

        assert isinstance(OPTIONAL_ENV_VARS, list)

    def test_wordpress_vars_in_optional(self):
        """WordPress関連変数がオプションに含まれること"""
        from src.config import OPTIONAL_ENV_VARS

        assert "WORDPRESS_URL" in OPTIONAL_ENV_VARS
        assert "WORDPRESS_USER" in OPTIONAL_ENV_VARS
        assert "WORDPRESS_APP_PASSWORD" in OPTIONAL_ENV_VARS

    def test_x_api_vars_in_optional(self):
        """X(旧Twitter) API変数がオプションに含まれること"""
        from src.config import OPTIONAL_ENV_VARS

        assert "X_API_KEY" in OPTIONAL_ENV_VARS
        assert "X_ACCESS_TOKEN" in OPTIONAL_ENV_VARS
