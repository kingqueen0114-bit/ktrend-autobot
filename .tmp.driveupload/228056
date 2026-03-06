# WordPress サーバー管理ガイド

サーバー内での WordPress 管理方法とトラブルシューティング手順を記録します。

## 📋 目次

1. [サーバー接続](#サーバー接続)
2. [WordPress 管理 (wp-cli)](#wordpress-管理-wp-cli)
3. [Application Password管理](#application-password管理)
4. [画像アップロード](#画像アップロード)
5. [トラブルシューティング](#トラブルシューティング)

---

## サーバー接続

### GCP インスタンスへのSSH接続

```bash
# gcloud SDK を使用した接続
/Users/yuiyane/line-calendar-bot/google-cloud-sdk/bin/gcloud compute ssh ktrend-server \
  --zone=asia-northeast1-a \
  --project=k-trend-autobot
```

### Docker コンテナ情報

| コンテナ名 | 用途 | 接続方法 |
|-----------|------|---------|
| `ktrend-wordpress` | WordPress | `docker exec ktrend-wordpress <command>` |
| `ktrend-mysql` | MySQL データベース | `docker exec ktrend-mysql <command>` |
| `ktrend-nginx` | Nginx ウェブサーバー | `docker exec ktrend-nginx <command>` |

---

## WordPress 管理 (wp-cli)

### 基本コマンド形式

```bash
# SSH経由でwp-cliコマンドを実行
gcloud compute ssh ktrend-server --zone=asia-northeast1-a --project=k-trend-autobot \
  --command="docker exec ktrend-wordpress wp <コマンド> --allow-root"
```

### よく使うコマンド

#### 1. サイト情報の確認

```bash
# WordPressバージョン確認
docker exec ktrend-wordpress wp core version --allow-root

# サイトURL確認
docker exec ktrend-wordpress wp option get siteurl --allow-root
docker exec ktrend-wordpress wp option get home --allow-root

# プラグイン一覧
docker exec ktrend-wordpress wp plugin list --allow-root

# テーマ一覧
docker exec ktrend-wordpress wp theme list --allow-root
```

#### 2. ユーザー管理

```bash
# ユーザー一覧
docker exec ktrend-wordpress wp user list --allow-root

# ユーザー情報取得
docker exec ktrend-wordpress wp user get admin --allow-root

# ユーザーパスワード変更
docker exec ktrend-wordpress wp user update admin --user_pass='NewPassword123!' --allow-root
```

#### 3. 投稿・メディア管理

```bash
# 投稿一覧（最新10件）
docker exec ktrend-wordpress wp post list --posts_per_page=10 --allow-root

# メディア一覧
docker exec ktrend-wordpress wp media list --allow-root

# メディアアップロード
docker exec ktrend-wordpress wp media import /path/to/image.jpg --title="Image Title" --allow-root
```

---

## Application Password管理

### 現在の状況

**問題**: WordPress REST API の Application Password 認証が機能していません。

**原因**:
1. `wp_is_application_passwords_available()` が `false` を返す
2. WordPress が HTTPS 接続として認識されていない可能性
3. mu-plugin でフィルターを追加済みだが効果なし

### Application Password の基本操作

#### 1. Application Password の一覧表示

```bash
docker exec ktrend-wordpress wp user application-password list admin --format=table --allow-root
```

#### 2. 新しい Application Password の生成

```bash
docker exec ktrend-wordpress wp user application-password create admin 'アプリ名' --allow-root
```

出力例：
```
Success: Created application password.
Password: Pe4PF7EbYpnungFx2IB4UmCo
```

#### 3. Application Password の削除

```bash
# 特定のUUIDを削除
docker exec ktrend-wordpress wp user application-password delete admin <UUID> --allow-root

# すべて削除（MySQLから直接）
docker exec ktrend-mysql sh -c "mysql -u root -p\$MYSQL_ROOT_PASSWORD ktrend_db -e \"DELETE FROM wp_usermeta WHERE meta_key='_application_passwords';\""
```

### 認証テスト

```bash
# REST API 認証テスト
curl -s https://k-trendtimes.com/wp-json/wp/v2/users/me \
  -H "Authorization: Basic $(echo -n 'admin:APPLICATION_PASSWORD' | base64)"
```

正常な場合：ユーザー情報のJSONが返る
エラーの場合：`{"code":"rest_not_logged_in","message":"現在ログインしていません。"}`

---

## 画像アップロード

### 方法1: wp-cli を使用（推奨）

```bash
# ホストマシンから画像をアップロード
# 1. 画像をサーバーにコピー
gcloud compute scp /local/path/image.jpg ktrend-server:/tmp/image.jpg \
  --zone=asia-northeast1-a --project=k-trend-autobot

# 2. wp-cli でメディアライブラリに追加
gcloud compute ssh ktrend-server --zone=asia-northeast1-a --project=k-trend-autobot \
  --command="docker cp /tmp/image.jpg ktrend-wordpress:/tmp/image.jpg && \
             docker exec ktrend-wordpress wp media import /tmp/image.jpg \
             --title='Image Title' --allow-root"
```

### 方法2: REST API（現在機能していません）

```python
import requests
import base64

wp_url = "https://k-trendtimes.com"
wp_user = "admin"
wp_password = "APPLICATION_PASSWORD"

credentials = f"{wp_user}:{wp_password}"
encoded = base64.b64encode(credentials.encode()).decode()

headers = {
    "Authorization": f"Basic {encoded}",
    "Content-Disposition": f'attachment; filename="image.jpg"'
}

with open('image.jpg', 'rb') as f:
    response = requests.post(
        f"{wp_url}/wp-json/wp/v2/media",
        headers=headers,
        data=f.read(),
        verify=True
    )

print(response.json())
```

### 方法3: MySQL 直接挿入（非推奨）

画像ファイルを手動でアップロードし、メタデータをデータベースに直接挿入する方法もありますが、WordPressの整合性が保てないため推奨しません。

---

## トラブルシューティング

### 1. Application Password が機能しない

**チェックリスト**:

1. Application Password が生成されているか確認
   ```bash
   docker exec ktrend-wordpress wp user application-password list admin --allow-root
   ```

2. Nginx が Authorization ヘッダーを渡しているか確認
   ```bash
   docker exec ktrend-nginx cat /etc/nginx/conf.d/default.conf | grep HTTP_AUTHORIZATION
   ```

   以下の行があるべき：
   ```
   fastcgi_param HTTP_AUTHORIZATION $http_authorization;
   ```

3. WordPress が Authorization ヘッダーを受け取っているか確認
   ```bash
   curl -s https://k-trendtimes.com/test-auth.php \
     -H "Authorization: Basic $(echo -n 'admin:PASSWORD' | base64)" \
     | grep -i authorization
   ```

   `["HTTP_AUTHORIZATION"]=>` が表示されればOK

4. Application Password 機能が有効か確認
   ```bash
   docker exec ktrend-wordpress sh -c 'cd /var/www/html && php -r "require_once(\"wp-load.php\"); echo wp_is_application_passwords_available() ? \"true\" : \"false\";"'
   ```

**現在の状況**: 上記すべてをチェック済みだが、認証が失敗している

**回避策**: wp-cli を使用して画像アップロードを行う

### 2. Nginx 設定の更新

```bash
# Nginx設定ファイルの編集（ホストマシン上）
sudo vi /opt/ktrend/nginx/conf.d/default.conf

# Nginx再起動
docker restart ktrend-nginx
```

### 3. WordPress wp-config.php の編集

```bash
docker exec ktrend-wordpress vi /var/www/html/wp-config.php

# または、sedで特定の設定を追加
docker exec ktrend-wordpress sh -c 'echo "設定内容" >> /var/www/html/wp-config.php'
```

### 4. MySQL データベース操作

```bash
# MySQL接続
docker exec ktrend-mysql sh -c "mysql -u root -p\$MYSQL_ROOT_PASSWORD ktrend_db"

# クエリ実行例
docker exec ktrend-mysql sh -c "mysql -u root -p\$MYSQL_ROOT_PASSWORD ktrend_db -e \"SELECT * FROM wp_users;\""
```

### 5. ログ確認

```bash
# Nginx ログ
docker logs ktrend-nginx --tail=50

# WordPress ログ（存在する場合）
docker exec ktrend-wordpress tail -50 /var/www/html/wp-content/debug.log

# MySQL ログ
docker logs ktrend-mysql --tail=50
```

---

## 設定ファイルの場所

### ホストマシン上

| ファイル/ディレクトリ | 説明 |
|---------------------|------|
| `/opt/ktrend/nginx/conf.d/` | Nginx 設定ファイル |
| `/opt/ktrend/nginx/ssl/` | SSL証明書（読み取り専用） |
| `/opt/ktrend/certbot/conf/` | Let's Encrypt 証明書 |
| `/var/lib/docker/volumes/ktrend_wordpress_data/_data/` | WordPress ファイル |

### コンテナ内

| ファイル/ディレクトリ | 説明 |
|---------------------|------|
| `/var/www/html/` | WordPress ルートディレクトリ |
| `/var/www/html/wp-config.php` | WordPress 設定ファイル |
| `/var/www/html/wp-content/mu-plugins/` | Must-Use プラグイン |
| `/etc/nginx/conf.d/` | Nginx 設定（読み取り専用マウント） |

---

## 重要な認証情報

### WordPress
- URL: `https://k-trendtimes.com`
- 管理画面: `https://k-trendtimes.com/wp-admin/`
- ユーザー名: `admin`
- パスワード: `KTrend2026Admin!`
- Application Password（最新）: `Pe4PF7EbYpnungFx2IB4UmCo`

### MySQL
- ホスト: `ktrend-mysql`（Docker ネットワーク内）
- データベース名: `ktrend_db`
- Root パスワード: `R00tKtr3nd2024!`

### GCP
- プロジェクトID: `k-trend-autobot`
- リージョン: `asia-northeast1`
- インスタンス名: `ktrend-server`

---

## 今後の対応

### 短期的な解決策

1. **画像アップロード機能の修正**
   - REST API の代わりに wp-cli を使用する方法に変更
   - Cloud Function から gcloud compute ssh 経由で wp-cli を実行

2. **Application Password 問題の継続調査**
   - WordPress のデバッグログを有効化
   - REST API の詳細なエラーログを確認

### 長期的な改善

1. **Application Password 認証の完全な修正**
   - WordPress コア、プラグイン、テーマの競合を調査
   - 必要に応じて WordPress を再インストール

2. **画像ストレージの変更検討**
   - Google Cloud Storage を直接使用
   - CloudFlare R2 などの CDN 統合

---

**最終更新**: 2026-02-09
**メンテナ**: K-Trend Development Team
