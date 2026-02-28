"""utils/helpers.py のユニットテスト"""
import pytest
from unittest.mock import MagicMock, patch, call
import time


class TestGenerateHashtags:
    """generate_hashtags関数のテスト

    注意: シグネチャは generate_hashtags(category, title) の順序。
    戻り値は '#' プレフィックス付きの文字列リスト。
    """

    def test_basic_hashtag_generation(self):
        """基本的なハッシュタグ生成: artistカテゴリ"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("artist", "BTS 新曲リリース")
        assert isinstance(result, list)
        assert len(result) > 0
        assert len(result) <= 5
        # 全てのタグが # で始まること
        for tag in result:
            assert tag.startswith("#"), f"タグ '{tag}' が # で始まっていない"

    def test_empty_title(self):
        """空タイトルの場合でもリストが返される"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("artist", "")
        assert isinstance(result, list)
        assert len(result) > 0  # カテゴリタグ + 共通タグは入る

    def test_empty_category_falls_back_to_other(self):
        """未知のカテゴリの場合、'other' カテゴリのタグが使われる"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("unknown_category", "テストタイトル")
        assert isinstance(result, list)
        assert len(result) > 0
        # 'other' カテゴリの共通タグが含まれることを確認
        assert "#韓国トレンド" in result or "#韓国" in result

    def test_known_categories(self):
        """全ての既知カテゴリでリストが返される"""
        from utils.helpers import generate_hashtags

        known_categories = ["artist", "beauty", "fashion", "food", "travel", "event", "drama", "other"]
        for category in known_categories:
            result = generate_hashtags(category, "テスト")
            assert isinstance(result, list), f"カテゴリ '{category}' でリストが返されない"
            assert len(result) > 0, f"カテゴリ '{category}' で空リスト"
            assert len(result) <= 5, f"カテゴリ '{category}' でタグが5個を超えている"

    def test_artist_keyword_detection_bts(self):
        """タイトルにBTSを含む場合、#BTSタグが先頭に挿入される"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("artist", "BTS 新アルバム発売決定")
        assert "#BTS" in result
        # アーティストタグは先頭に挿入される
        assert result[0] == "#BTS"

    def test_artist_keyword_detection_blackpink(self):
        """タイトルにBLACKPINKを含む場合、#BLACKPINKタグが追加される"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("artist", "blackpink ワールドツアー")
        assert "#BLACKPINK" in result
        assert result[0] == "#BLACKPINK"

    def test_artist_keyword_detection_newjeans(self):
        """タイトルにNewJeansを含む場合、#NewJeansタグが追加される"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("artist", "NewJeans 日本デビュー")
        assert "#NewJeans" in result

    def test_artist_keyword_case_insensitive(self):
        """アーティスト名の大文字小文字を区別しない"""
        from utils.helpers import generate_hashtags

        result_lower = generate_hashtags("artist", "bts コンサート")
        result_upper = generate_hashtags("artist", "BTS コンサート")
        # どちらも #BTS が含まれる
        assert "#BTS" in result_lower
        assert "#BTS" in result_upper

    def test_max_five_hashtags(self):
        """ハッシュタグは最大5個まで"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("artist", "BTS 新曲リリース 特別イベント")
        assert len(result) <= 5

    def test_no_duplicate_hashtags(self):
        """重複するハッシュタグがないこと"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("artist", "韓国アイドル 最新情報")
        assert len(result) == len(set(result)), "重複するハッシュタグが存在する"

    def test_common_tags_included(self):
        """共通タグ #韓国 と #KTrendTimes が含まれること"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("other", "テスト")
        # 共通タグが5個制限内に収まれば含まれる
        all_tags_str = " ".join(result)
        assert "#韓国" in all_tags_str or "#KTrendTimes" in all_tags_str

    def test_category_specific_tags_for_beauty(self):
        """beautyカテゴリでコスメ系タグが含まれる"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("beauty", "韓国コスメ新作")
        assert "#韓国コスメ" in result

    def test_category_specific_tags_for_food(self):
        """foodカテゴリでグルメ系タグが含まれる"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("food", "ソウルの人気カフェ")
        assert "#韓国グルメ" in result

    def test_no_artist_match_in_title(self):
        """タイトルにアーティスト名がない場合、アーティストタグは追加されない"""
        from utils.helpers import generate_hashtags

        result = generate_hashtags("artist", "韓国音楽業界の動向")
        # 定義済みアーティストタグが先頭に来ないこと
        artist_tags = [
            "#BTS", "#BLACKPINK", "#TWICE", "#aespa", "#IVE", "#NewJeans",
            "#StrayKids", "#SEVENTEEN", "#NCT", "#EXO", "#RedVelvet",
            "#ITZY", "#TXT", "#ENHYPEN", "#LESSERAFIM", "#ATEEZ", "#GIDLE",
        ]
        assert result[0] not in artist_tags


class TestRetryWithBackoff:
    """retry_with_backoff デコレータのテスト"""

    @patch("utils.helpers.time.sleep")
    @patch("utils.helpers.log_error")
    def test_success_on_first_attempt(self, mock_log_error, mock_sleep):
        """初回成功時はリトライしない"""
        from utils.helpers import retry_with_backoff

        @retry_with_backoff(max_retries=3)
        def success_func():
            return "ok"

        result = success_func()
        assert result == "ok"
        mock_sleep.assert_not_called()

    @patch("utils.helpers.time.sleep")
    @patch("utils.helpers.log_error")
    def test_success_on_second_attempt(self, mock_log_error, mock_sleep):
        """2回目で成功する場合"""
        from utils.helpers import retry_with_backoff

        call_count = {"n": 0}

        @retry_with_backoff(max_retries=3, initial_delay=1.0, backoff_factor=2.0)
        def flaky_func():
            call_count["n"] += 1
            if call_count["n"] < 2:
                raise ValueError("一時的エラー")
            return "recovered"

        result = flaky_func()
        assert result == "recovered"
        assert call_count["n"] == 2
        mock_sleep.assert_called_once_with(1.0)

    @patch("utils.helpers.time.sleep")
    @patch("utils.helpers.log_error")
    def test_all_retries_exhausted(self, mock_log_error, mock_sleep):
        """全リトライが失敗した場合に例外が発生する"""
        from utils.helpers import retry_with_backoff

        @retry_with_backoff(max_retries=2, initial_delay=0.5, backoff_factor=2.0)
        def always_fail():
            raise RuntimeError("永続的エラー")

        with pytest.raises(RuntimeError, match="永続的エラー"):
            always_fail()

        # max_retries=2 なので、sleep は 2回呼ばれる (attempt 0失敗, 1失敗の後)
        assert mock_sleep.call_count == 2

    @patch("utils.helpers.time.sleep")
    @patch("utils.helpers.log_error")
    def test_exponential_backoff_delays(self, mock_log_error, mock_sleep):
        """指数バックオフで遅延が増加すること"""
        from utils.helpers import retry_with_backoff

        @retry_with_backoff(max_retries=3, initial_delay=1.0, backoff_factor=2.0)
        def always_fail():
            raise RuntimeError("error")

        with pytest.raises(RuntimeError):
            always_fail()

        # 遅延: 1.0, 2.0, 4.0
        expected_calls = [call(1.0), call(2.0), call(4.0)]
        assert mock_sleep.call_args_list == expected_calls

    @patch("utils.helpers.time.sleep")
    @patch("utils.helpers.log_error")
    def test_preserves_function_name(self, mock_log_error, mock_sleep):
        """functools.wraps により元の関数名が保持される"""
        from utils.helpers import retry_with_backoff

        @retry_with_backoff()
        def my_special_func():
            return True

        assert my_special_func.__name__ == "my_special_func"


class TestSafeApiCall:
    """safe_api_call関数のテスト"""

    @patch("utils.helpers.log_error")
    def test_successful_call(self, mock_log_error):
        """正常に関数が実行される場合"""
        from utils.helpers import safe_api_call

        def add(a, b):
            return a + b

        result = safe_api_call(add, 2, 3)
        assert result == 5
        mock_log_error.assert_not_called()

    @patch("utils.helpers.log_error")
    def test_returns_default_on_exception(self, mock_log_error):
        """例外時にデフォルト値が返される"""
        from utils.helpers import safe_api_call

        def failing():
            raise ValueError("API error")

        result = safe_api_call(failing, default="fallback", error_context="テスト呼び出し")
        assert result == "fallback"
        mock_log_error.assert_called_once()

    @patch("utils.helpers.log_error")
    def test_default_is_none(self, mock_log_error):
        """デフォルト値を指定しない場合はNoneが返される"""
        from utils.helpers import safe_api_call

        def failing():
            raise RuntimeError("err")

        result = safe_api_call(failing)
        assert result is None

    @patch("utils.helpers.log_error")
    def test_passes_kwargs(self, mock_log_error):
        """キーワード引数が正しく渡される"""
        from utils.helpers import safe_api_call

        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}"

        result = safe_api_call(greet, "World", greeting="Hi")
        assert result == "Hi, World"


class TestFuncInit:
    """func_init関数のテスト"""

    @patch("utils.helpers.log_event")
    @patch("utils.helpers.log_config_status")
    def test_successful_init(self, mock_log_config, mock_log_event):
        """全ての必須環境変数が設定されている場合、正常に初期化される"""
        from utils.helpers import func_init

        # conftest.py の autouse フィクスチャで環境変数は設定済み
        func_init()
        mock_log_event.assert_called_once_with("INIT", "Cloud Function initialized successfully")

    @patch("utils.helpers.log_error")
    @patch("utils.helpers.log_config_status")
    @patch("utils.helpers.validate_env_vars", return_value=["GEMINI_API_KEY"])
    def test_missing_env_vars_raises_error(self, mock_validate, mock_log_config, mock_log_error):
        """必須環境変数が欠如している場合、ConfigurationErrorが発生する"""
        from utils.helpers import func_init
        from src.exceptions import ConfigurationError

        with pytest.raises(ConfigurationError):
            func_init()

        mock_log_error.assert_called_once()
