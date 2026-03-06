# K-TREND TIMES (k-trendtimes.com) 修正記録

## 日付: 2026-02-13

---

## インフラ整備・セキュリティ強化

### 1. line-claude-bridge のシークレット移行

**問題**: `server.js` に機密情報（LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN, WORDPRESS_APP_PASSWORD）がハードコードされていた

**解決策**:
- `server.js` を修正し、`process.env` から環境変数を読み込むように変更
- `.env.example` テンプレートを作成

**変更ファイル**: `line-claude-bridge/server.js`, `line-claude-bridge/.env.example`

---

### 2. 重複スケジューラの整理

**問題**: Cloud Scheduler に重複・不要なジョブが5件存在

**削除したジョブ**:
| ジョブ名 | 理由 |
|---------|------|
| ktrend-fetch-09 | 深夜0時実行（不要） |
| ktrend-fetch-12 | 深夜3時実行（不要） |
| ktrend-fetch-18 | 9時実行（ktrend-daily-fetch-schedulerと重複） |
| ktrend-daily-trigger | UTC設定で混乱の原因 |
| ktrend-weekly-stats | ktrend-weekly-stats-schedulerと重複 |

**残存ジョブ（5件）**:
- ktrend-daily-fetch-scheduler: 毎日 9:00 JST
- ktrend-analytics-daily-schedule: 毎日 9:00 JST
- ktrend-analytics-weekly-schedule: 毎週月曜 10:00 JST
- ktrend-analytics-monthly-schedule: 毎月1日 11:00 JST
- ktrend-weekly-stats-scheduler: 毎週月曜 9:00 JST

---

### 3. Secret Manager への移行

**実施内容**:
- Google Cloud Secret Manager に機密情報を登録
- Cloud Functions がSecret Managerから自動的に読み込むように設定

**登録したシークレット**:
- `GEMINI_API_KEY`
- `GOOGLE_CUSTOM_SEARCH_API_KEY`
- `LINE_CHANNEL_ACCESS_TOKEN`
- `LINE_CHANNEL_SECRET`
- `WORDPRESS_APP_PASSWORD`

**IAM権限**: `647168456227-compute@developer.gserviceaccount.com` に `secretmanager.secretAccessor` ロールを付与

---

### 4. 欠落モジュールの復元

**問題**: ローカルソースに以下のモジュールが欠落しており、新規デプロイが失敗

**作成したモジュール**:
| ファイル | 内容 |
|---------|------|
| `src/exceptions.py` | カスタム例外クラス (KTrendError, ConfigurationError等) |
| `src/config.py` | 環境変数検証・設定管理 (validate_env_vars, log_config_status) |
| `src/fetch_trends.py` | TrendFetcher - Google Search API + Gemini AI連携 |
| `src/content_generator.py` | ContentGenerator + check_article_quality |

**デプロイ結果**:
| 関数 | リビジョン | 状態 |
|------|-----------|------|
| ktrend-main | 00020-yep | ACTIVE |
| ktrend-daily-fetch | 00064-wix | ACTIVE |
| ktrend-line-webhook | 00070-hil | ACTIVE |
| view-draft | 00055-fid | ACTIVE |

---

### 5. LINE-Claude Bridge のCloud Runデプロイ

**実施内容**: Node.js サーバーをCloud Runにデプロイ

**サービス情報**:
- **URL**: https://line-claude-bridge-647168456227.asia-northeast1.run.app
- **リビジョン**: line-claude-bridge-00002-ljc
- **メモリ**: 512Mi
- **ポート**: 8080

**エンドポイント**:
- `/drafts` - 未公開記事一覧
- `/edit/{draft_id}` - 記事編集
- `/draft/{draft_id}` - プレビュー
- `/webhook` - LINE Webhook

**環境変数**: Secret Managerから読み込み + 通常環境変数を設定

---

## 新規作成ファイル

| ファイル | 説明 |
|---------|------|
| `src/exceptions.py` | カスタム例外クラス |
| `src/config.py` | 環境変数検証 |
| `src/fetch_trends.py` | トレンド取得 |
| `src/content_generator.py` | コンテンツ生成 |
| `.env.deploy.yaml` | デプロイ用環境変数（シークレット除外） |
| `line-claude-bridge/.env.example` | 環境変数テンプレート |

---

## WordPress公開エラーの修正（同日追加）

### 問題1: SSL証明書エラー

**症状**: LINEの「今すぐ公開」ボタンを押しても公開されない

**エラーログ**:
```
SSL: CERTIFICATE_VERIFY_FAILED - certificate is not valid for '34.84.132.199'
```

**原因**: `storage_manager.py` でWordPress URLのデフォルト値がIPアドレス `http://34.84.132.199` にハードコードされていた

**解決策**:
```python
# 修正前
self.wp_url = os.getenv("WORDPRESS_URL", "http://34.84.132.199")

# 修正後
self.wp_url = os.getenv("WORDPRESS_URL", "https://k-trendtimes.com")
```

---

### 問題2: エントリポイント名の不一致

**症状**: ktrend-line-webhook のデプロイが失敗

**エラーログ**:
```
MissingTargetException: File /workspace/main.py is expected to contain
a function named 'line_webhook'. Found: 'handle_line_webhook' instead
```

**解決策**: デプロイ時のエントリポイントを `handle_line_webhook` に修正

---

### 問題3: WordPress認証エラー (401 Unauthorized)

**症状**: 公開ボタンを押すと「公開エラー」が表示される

**エラーログ**:
```
401 Client Error: Unauthorized for url: https://k-trendtimes.com/wp-json/wp/v2/media
```

**原因**: `_get_wp_auth_header()` メソッドが `WORDPRESS_ADMIN_PASSWORD` を使用していたが、これはSecret Managerに登録されていない。`WORDPRESS_APP_PASSWORD` を使用すべきだった。

**解決策**:
```python
# 修正前
credentials = f"{self.wp_user}:{self.wp_password}"

# 修正後
password = self.wp_app_password or self.wp_password
credentials = f"{self.wp_user}:{password}"
```

---

### 最終デプロイ結果

| 関数 | リビジョン | 状態 |
|------|-----------|------|
| ktrend-main | 00022-mef | ✅ ACTIVE |
| ktrend-line-webhook | 00073-qis | ✅ ACTIVE |
| view-draft | 00057-lab | ✅ ACTIVE |

---

## 現在のシステム構成

### Cloud Functions（全7件 ACTIVE）
- ktrend-main (00022-mef)
- ktrend-daily-fetch
- ktrend-line-webhook (00073-qis)
- view-draft (00057-lab)
- ktrend-analytics-daily
- ktrend-analytics-weekly
- ktrend-analytics-monthly

### Cloud Run
- line-claude-bridge

### Cloud Scheduler（全5件 ENABLED）
- 毎日9時: トレンド取得 + 日次Analytics
- 毎週月曜: 週次Analytics + 統計サマリー
- 毎月1日: 月次Analytics

---

## 日付: 2026-02-08

---

## 実装した広告タイプ

| 広告タイプ | 配置場所 | ファイル |
|-----------|---------|---------|
| 記事内広告 | 記事の中間・末尾 | ktrend-ads.php |
| サイドバー広告 | 右サイドバー（PC） | ktrend-ads.php |
| インフィード広告 | 投稿リスト（5件ごと） | category-tabs.php |

---

## 発生した問題と解決策

### 問題1: 上部スライド広告（アンカー広告）が邪魔

**症状**: 画面上部からスライドしてくる広告が表示される

**解決策**: WordPressヘッダーコードで自動広告のオーバーレイを無効化

```javascript
(adsbygoogle = window.adsbygoogle || []).push({
  google_ad_client: "ca-pub-6657168802277658",
  enable_page_level_ads: true,
  overlays: {bottom: false, top: false}
});
```

**最終的な解決**: 自動広告を完全に無効化し、手動配置のみに変更

---

### 問題2: 広告がcheckpoint（要約セクション）に重なる

**症状**: Google自動広告が`article-highlights`セクションに重なって表示される

**解決策**:

1. **Google自動広告（page-level ads）を完全に無効化**
   - ヘッダーから `enable_page_level_ads` の設定を削除

2. **checkpoint直後の広告配置を削除**
   - 記事内広告は中間と末尾のみに変更
   - 最初の段落後の広告を削除

3. **CSSでcheckpointセクションを保護**
```css
/* checkpointセクションを保護 */
.article-highlights {
    position: relative;
    z-index: 100 !important;
    overflow: visible !important;
    isolation: isolate;
}

/* checkpoint内部の広告を完全に非表示 */
.article-highlights ins,
.article-highlights .adsbygoogle,
.article-highlights iframe[id^="google_ads"],
.article-highlights iframe[id^="aswift"] {
    display: none !important;
}

/* checkpoint周辺のGoogle自動挿入広告を非表示 */
.article-highlights + ins.adsbygoogle,
.article-highlights + div > ins.adsbygoogle {
    display: none !important;
}
```

---

### 問題3: 投稿日付が全て同じ（2026-02-04 12:27:27）

**症状**: 142件の投稿が全く同じ日時に集中している

**原因**: 一括インポート時に元の日付が保持されなかった

**解決策**: スラッグに含まれる日付情報を抽出してSQLで更新

**スラッグパターン**:
- `YYMMDD + category` 例: `241018artist` → 2024-10-18
- `category + YYMMDD` 例: `news2410132` → 2024-10-13

**実行したSQL**:
```sql
UPDATE wp_posts SET
  post_date='2024-10-18 09:00:00',
  post_date_gmt='2024-10-18 09:00:00',
  post_modified='2024-10-18 09:00:00',
  post_modified_gmt='2024-10-18 09:00:00'
WHERE ID=796;
-- ... 791件更新
```

---

### 問題4: カテゴリタブのフィーチャー画像が表示されない

**症状**: タブの下のフィーチャー画像が空白

**原因**: 最新投稿（BTS記事 ID:2652）にサムネイルが設定されていなかった

**解決策**: `category-tabs.php`を修正
- サムネイルがある投稿の中から最新のものをフィーチャー表示するように変更
- フィーチャー投稿を最初に出力してからリストを表示するように順序を修正

---

### 問題5: 画像の表示が不安定（ぼやけ・欠落）

**症状**:
- 画像がぼやけて表示される
- 一部の記事で画像が表示されない

**解決策**: 画像を完全に削除し、タイトルのみ表示に変更（韓国ゴンチャスタイル）

**変更内容**:
1. フィーチャー画像セクションを完全に削除
2. リスト表示のサムネイルを削除
3. タイトルのみのシンプルなリスト表示に変更
4. ページあたりの投稿数を10件→15件に増加（画像なしのため）

**変更ファイル**: `category-tabs.php`

```php
// 変更前（画像付き）
$output .= '<li class="post-item">';
if ($thumb) {
    $output .= '<a href="..." class="item-thumb"><img src="..." alt=""></a>';
}
$output .= '<div class="item-content">...</div></li>';

// 変更後（タイトルのみ）
$output .= '<li class="post-item">';
$output .= '<div class="item-content">';
$output .= '<a href="..."><h4 class="item-title">...</h4></a>';
$output .= '<div class="item-meta">...</div></div></li>';
```

---

## 関連ファイル

| ファイル | 場所 | 説明 |
|---------|------|------|
| ktrend-ads.php | `/var/www/html/wp-content/mu-plugins/` | 広告管理プラグイン |
| category-tabs.php | `/var/www/html/wp-content/mu-plugins/` | カテゴリタブ＋インフィード広告 |
| ihaf_insert_header | WordPress option | Analytics/AdSenseヘッダーコード |

---

## AdSense設定

- **Publisher ID**: `ca-pub-6657168802277658`
- **Analytics ID**: `G-GG97WC82VK`
- **自動広告**: 無効（手動配置のみ）
- **アンカー広告**: 無効

---

## サーバー情報

- **プロジェクト**: k-trend-autobot (GCP)
- **VM**: ktrend-server (asia-northeast1-a)
- **コンテナ**:
  - ktrend-wordpress (WordPress-FPM)
  - ktrend-nginx
  - ktrend-mysql
- **データベース**: ktrend_db
- **MySQL認証**: root / R00tKtr3nd2024!
