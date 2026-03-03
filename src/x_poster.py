"""X (Twitter) 自動投稿モジュール

記事承認時にX投稿案 + アイキャッチ画像 + 記事URLを自動投稿。
X API v1.1 (画像アップロード) + v2 (ツイート投稿) を使用。
"""

import os
import logging
import requests
import tweepy

logger = logging.getLogger(__name__)


def _get_credentials():
    """X API認証情報を取得"""
    return {
        "api_key": os.environ.get("X_API_KEY", ""),
        "api_key_secret": os.environ.get("X_API_KEY_SECRET", ""),
        "access_token": os.environ.get("X_ACCESS_TOKEN", ""),
        "access_token_secret": os.environ.get("X_ACCESS_TOKEN_SECRET", ""),
        "bearer_token": os.environ.get("X_BEARER_TOKEN", ""),
    }


def _get_v1_api():
    """tweepy API v1.1 クライアント（画像アップロード用）"""
    creds = _get_credentials()
    auth = tweepy.OAuth1UserHandler(
        creds["api_key"],
        creds["api_key_secret"],
        creds["access_token"],
        creds["access_token_secret"],
    )
    return tweepy.API(auth)


def _get_v2_client():
    """tweepy Client v2（ツイート投稿用）"""
    creds = _get_credentials()
    return tweepy.Client(
        bearer_token=creds["bearer_token"],
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_key_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_token_secret"],
    )


def post_tweet(text: str, url: str = "", image_url: str = "") -> dict:
    """画像付きツイートを投稿

    Args:
        text: ツイート本文（x_post_1 or x_post_2）
        url: 記事URL
        image_url: アイキャッチ画像URL

    Returns:
        {"success": bool, "tweet_id": str, "tweet_url": str, "error": str}
    """
    creds = _get_credentials()
    required_fields = ["api_key", "api_key_secret", "access_token", "access_token_secret"]
    missing = [f for f in required_fields if not creds.get(f)]
    if missing:
        logger.warning(f"X API認証情報が不足: {', '.join(missing)}。投稿をスキップします。")
        return {"success": False, "error": "X API credentials not configured"}

    try:
        # ツイートテキストを構築（URL付加）
        tweet_text = text
        if url:
            # URLが既にテキストに含まれていなければ追加
            if url not in tweet_text:
                tweet_text = f"{tweet_text}\n\n{url}"

        # 280文字制限チェック（URLは23文字でカウント）
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."

        media_id = None

        # 画像アップロード（v1.1 API）
        if image_url:
            try:
                api_v1 = _get_v1_api()

                # 画像をダウンロード
                img_resp = requests.get(
                    image_url,
                    timeout=30,
                    headers={"User-Agent": "K-TREND-TIMES/1.0"},
                )
                img_resp.raise_for_status()

                content_type = img_resp.headers.get("Content-Type", "image/jpeg")
                if "html" in content_type.lower():
                    logger.warning(f"X投稿: 画像URLがHTMLを返しました。画像なしで投稿します。")
                else:
                    # 一時ファイルとしてアップロード
                    import tempfile
                    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
                    try:
                        tmp.write(img_resp.content)
                        tmp.flush()
                        tmp.close()  # Close before media_upload reads it
                        media = api_v1.media_upload(filename=tmp.name)
                        media_id = media.media_id
                        logger.info(f"X投稿: 画像アップロード成功 (media_id: {media_id})")
                    finally:
                        import os as _os
                        try:
                            _os.unlink(tmp.name)
                        except OSError:
                            pass

            except Exception as e:
                logger.warning(f"X投稿: 画像アップロード失敗（画像なしで続行）: {e}")

        # ツイート投稿（v2 API）
        client_v2 = _get_v2_client()
        kwargs = {"text": tweet_text}
        if media_id:
            kwargs["media_ids"] = [media_id]

        response = client_v2.create_tweet(**kwargs)

        tweet_id = response.data.get("id", "")
        # X APIのユーザー名を取得してURL構築
        tweet_url = f"https://x.com/i/web/status/{tweet_id}" if tweet_id else ""

        logger.info(f"X投稿成功: {tweet_url}")
        return {
            "success": True,
            "tweet_id": tweet_id,
            "tweet_url": tweet_url,
        }

    except tweepy.TweepyException as e:
        logger.error(f"X投稿失敗 (TweepyError): {e}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"X投稿失敗: {e}")
        return {"success": False, "error": str(e)}
