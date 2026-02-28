"""共通テストフィクスチャ"""
import os
import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """テスト用環境変数を設定"""
    env_vars = {
        "GEMINI_API_KEY": "test-gemini-key",
        "GOOGLE_CUSTOM_SEARCH_API_KEY": "test-search-key",
        "GOOGLE_CSE_ID": "test-cse-id",
        "LINE_CHANNEL_ACCESS_TOKEN": "test-line-token",
        "LINE_CHANNEL_SECRET": "test-line-secret",
        "LINE_USER_ID": "test-user-id",
        "GCP_PROJECT_ID": "test-project",
        "WORDPRESS_URL": "https://test.example.com",
        "WORDPRESS_USER": "test-user",
        "WORDPRESS_APP_PASSWORD": "test-password",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def mock_firestore():
    """Firestoreクライアントのモック"""
    with patch("google.cloud.firestore.Client") as mock:
        yield mock


@pytest.fixture
def mock_gcs():
    """GCSクライアントのモック"""
    with patch("google.cloud.storage.Client") as mock:
        yield mock


@pytest.fixture
def mock_requests():
    """requestsモジュールのモック"""
    with patch("requests.post") as mock_post, \
         patch("requests.get") as mock_get, \
         patch("requests.head") as mock_head:
        yield {
            "post": mock_post,
            "get": mock_get,
            "head": mock_head,
        }


@pytest.fixture
def sample_trend():
    """テスト用トレンドデータ"""
    return {
        "title": "テスト韓国トレンド",
        "snippet": "テスト用のスニペットです",
        "image_url": "https://example.com/image.jpg",
        "source_url": "https://example.com/article",
        "original_text": "テスト用の記事本文",
        "fetched_at": "2026-02-28T09:00:00",
        "category": "artist",
    }


@pytest.fixture
def sample_cms_content():
    """テスト用CMS記事データ"""
    return {
        "title": "テスト記事タイトル",
        "lead": "テスト記事のリード文",
        "body": "# テスト見出し\n\nテスト本文です。" * 100,
        "meta_description": "テスト記事のメタ説明",
        "x_post_1": "テストX投稿案1 #韓国",
        "x_post_2": "テストX投稿案2 #KPOP",
        "artist_tags": ["BTS", "BLACKPINK"],
    }


@pytest.fixture
def sample_sns_content():
    """テスト用SNSコンテンツデータ"""
    return {
        "news_post": "テストニュース投稿",
        "luna_post_a": "テストLuna A投稿",
        "luna_post_b": "テストLuna B投稿",
    }
