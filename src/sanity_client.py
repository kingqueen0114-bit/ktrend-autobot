"""Sanity CMS HTTP APIクライアント

Sanity Mutations API / GROQ Query API / Assets API の薄いラッパー。
"""

import os
import uuid
import logging
import requests

logger = logging.getLogger(__name__)

# Sanity configuration
SANITY_PROJECT_ID = os.environ.get("SANITY_PROJECT_ID", "3pe6cvt2")
SANITY_DATASET = os.environ.get("SANITY_DATASET", "production")
SANITY_API_VERSION = "2024-01-01"


_cached_token = None


def _get_token():
    """Sanity APIトークンを取得（Secret Manager or 環境変数）- キャッシュあり"""
    global _cached_token
    if _cached_token:
        return _cached_token

    token = os.environ.get("SANITY_API_TOKEN", "")
    if not token:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            project_id = os.environ.get("GCP_PROJECT", "ktrend-autobot")
            name = f"projects/{project_id}/secrets/SANITY_API_TOKEN/versions/latest"
            response = client.access_secret_version(request={"name": name})
            token = response.payload.data.decode("UTF-8")
        except Exception as e:
            logger.warning(f"Secret Manager からトークンを取得できません: {e}")

    _cached_token = token
    return token


def _headers():
    """Sanity API リクエストヘッダー"""
    return {
        "Authorization": f"Bearer {_get_token()}",
        "Content-Type": "application/json",
    }


def _mutations_url():
    return f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/mutate/{SANITY_DATASET}"


def _query_url():
    return f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/data/query/{SANITY_DATASET}"


def _assets_url():
    return f"https://{SANITY_PROJECT_ID}.api.sanity.io/v{SANITY_API_VERSION}/assets/images/{SANITY_DATASET}"


def generate_id():
    """Sanity用のユニークIDを生成"""
    return str(uuid.uuid4()).replace("-", "")


def query(groq_query: str, params: dict = None) -> list:
    """GROQクエリを実行して結果を返す"""
    payload = {"query": groq_query}
    if params:
        for k, v in params.items():
            payload[f"${k}"] = v

    resp = requests.get(
        _query_url(),
        params=payload,
        headers=_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", [])


def query_one(groq_query: str, params: dict = None):
    """GROQクエリを実行して最初の結果を返す（[0]相当）"""
    result = query(groq_query, params)
    if isinstance(result, list):
        return result[0] if result else None
    return result


def create(doc: dict) -> dict:
    """ドキュメントを作成"""
    mutations = [{"create": doc}]
    resp = requests.post(
        _mutations_url(),
        json={"mutations": mutations},
        headers=_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    result = resp.json()
    return result.get("results", [{}])[0]


def create_or_replace(doc: dict) -> dict:
    """ドキュメントを作成または置換"""
    mutations = [{"createOrReplace": doc}]
    resp = requests.post(
        _mutations_url(),
        json={"mutations": mutations},
        headers=_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    result = resp.json()
    return result.get("results", [{}])[0]


def patch(doc_id: str, set_fields: dict = None, unset_fields: list = None) -> dict:
    """ドキュメントをパッチ更新"""
    patch_ops = {"id": doc_id}
    if set_fields:
        patch_ops["set"] = set_fields
    if unset_fields:
        patch_ops["unset"] = unset_fields

    mutations = [{"patch": patch_ops}]
    resp = requests.post(
        _mutations_url(),
        json={"mutations": mutations},
        headers=_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def delete(doc_id: str) -> dict:
    """ドキュメントを削除"""
    mutations = [{"delete": {"id": doc_id}}]
    resp = requests.post(
        _mutations_url(),
        json={"mutations": mutations},
        headers=_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def transaction(mutations: list) -> dict:
    """複数のミューテーションをトランザクションで実行"""
    resp = requests.post(
        _mutations_url(),
        json={"mutations": mutations},
        headers=_headers(),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def upload_image(image_bytes: bytes, filename: str = "image.jpg",
                 content_type: str = "image/jpeg") -> dict:
    """画像をSanity Assetsにアップロード"""
    headers = {
        "Authorization": f"Bearer {_get_token()}",
        "Content-Type": content_type,
    }

    resp = requests.post(
        _assets_url(),
        data=image_bytes,
        headers=headers,
        params={"filename": filename},
        timeout=60,
    )
    resp.raise_for_status()
    result = resp.json()
    doc = result.get("document", {})
    return {
        "_id": doc.get("_id", ""),
        "_type": "sanity.imageAsset",
        "url": doc.get("url", ""),
        "assetId": doc.get("assetId", ""),
    }


def _validate_image_url(url: str) -> bool:
    """画像URLのバリデーション（SSRF対策）"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    hostname = parsed.hostname or ""
    # Block internal/private network access
    blocked_patterns = [
        "localhost", "127.0.0.1", "0.0.0.0",
        "169.254.", "10.",
        "172.16.", "172.17.", "172.18.", "172.19.",
        "172.20.", "172.21.", "172.22.", "172.23.",
        "172.24.", "172.25.", "172.26.", "172.27.",
        "172.28.", "172.29.", "172.30.", "172.31.",
        "192.168.",
        "metadata.google", "metadata.internal",
    ]
    for pattern in blocked_patterns:
        if hostname.startswith(pattern) or hostname == pattern:
            logger.warning(f"ブロックされたURL: {url}")
            return False
    return True


def upload_image_from_url(image_url: str, max_retries: int = 3) -> dict:
    """URLから画像をダウンロードしてSanity Assetsにアップロード"""
    if not _validate_image_url(image_url):
        logger.warning(f"無効な画像URL（SSRF防止）: {image_url}")
        return {}

    for attempt in range(max_retries):
        try:
            img_resp = requests.get(
                image_url,
                timeout=30,
                headers={"User-Agent": "K-TREND-TIMES/1.0"},
            )
            img_resp.raise_for_status()

            content_type = img_resp.headers.get("Content-Type", "image/jpeg")
            if "html" in content_type.lower():
                logger.warning(f"画像URLがHTMLを返しました: {image_url}")
                return {}

            if len(img_resp.content) < 1000:
                logger.warning(f"画像サイズが小さすぎます: {len(img_resp.content)} bytes")
                return {}

            # Extract filename from URL
            filename = image_url.split("/")[-1].split("?")[0] or "image.jpg"

            result = upload_image(img_resp.content, filename, content_type)
            if result.get("_id"):
                logger.info(f"画像アップロード成功: {result['_id']}")
                return result

        except Exception as e:
            logger.warning(f"画像アップロード失敗 (attempt {attempt + 1}): {e}")

    logger.error(f"画像アップロード最終失敗: {image_url}")
    return {}


def image_ref(asset_id: str) -> dict:
    """Sanity画像参照オブジェクトを構築"""
    return {
        "_type": "image",
        "asset": {
            "_type": "reference",
            "_ref": asset_id,
        },
    }
