# K-Trend AutoBot 作業履歴

このファイルはClaude Codeセッションの作業履歴を記録しています。

---

## 2026-02-13: インフラ整備・セキュリティ強化

### 作業サマリー

1. **line-claude-bridge シークレット移行完了**
   - server.jsのハードコードを環境変数に変更
   - `.env.example` テンプレート作成

2. **Cloud Scheduler 重複整理**
   - 5件削除、5件残存
   - 削除: ktrend-fetch-09, ktrend-fetch-12, ktrend-fetch-18, ktrend-daily-trigger, ktrend-weekly-stats

3. **Secret Manager 設定完了**
   - 5つのシークレットを登録
   - GEMINI_API_KEY, GOOGLE_CUSTOM_SEARCH_API_KEY, LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET, WORDPRESS_APP_PASSWORD
   - Cloud Functionsから自動参照

4. **欠落モジュール復元**
   - `src/exceptions.py` - カスタム例外クラス
   - `src/config.py` - 環境変数検証
   - `src/fetch_trends.py` - トレンド取得 (TrendFetcher)
   - `src/content_generator.py` - コンテンツ生成 (ContentGenerator, check_article_quality)

5. **LINE-Claude Bridge デプロイ完了**
   - URL: https://line-claude-bridge-647168456227.asia-northeast1.run.app
   - リビジョン: line-claude-bridge-00002-ljc

### システム状態

| コンポーネント | 状態 |
|---------------|------|
| Cloud Functions (7件) | 全て ACTIVE |
| Cloud Run (1件) | ACTIVE |
| Cloud Scheduler (5件) | 全て ENABLED |

### デプロイされた関数

| 関数名 | リビジョン |
|--------|-----------|
| ktrend-main | 00020-yep |
| ktrend-daily-fetch | 00064-wix |
| ktrend-line-webhook | 00070-hil |
| view-draft | 00055-fid |
| ktrend-analytics-daily | - |
| ktrend-analytics-weekly | - |
| ktrend-analytics-monthly | - |

---

## 2026-02-13: WordPress公開エラー修正（同日追加）

### 発生した問題

LINEの「今すぐ公開」ボタンを押しても記事が公開されない問題が発生。

### 修正内容

#### 問題1: SSL証明書エラー
- **エラー**: `SSL: CERTIFICATE_VERIFY_FAILED - certificate is not valid for '34.84.132.199'`
- **原因**: `storage_manager.py`でWordPress URLのデフォルト値がIPアドレスにハードコード
- **修正**: デフォルト値を `https://k-trendtimes.com` に変更

#### 問題2: エントリポイント名の不一致
- **エラー**: `MissingTargetException: expected 'line_webhook', found 'handle_line_webhook'`
- **修正**: デプロイ時のエントリポイントを `handle_line_webhook` に変更

#### 問題3: WordPress認証エラー (401 Unauthorized)
- **エラー**: `401 Client Error: Unauthorized for url: https://k-trendtimes.com/wp-json/wp/v2/media`
- **原因**: `_get_wp_auth_header()` が `WORDPRESS_ADMIN_PASSWORD` を使用していたが、Secret Managerには `WORDPRESS_APP_PASSWORD` のみ登録
- **修正**: `_get_wp_auth_header()` で `wp_app_password` を優先使用するように変更

### 変更ファイル

| ファイル | 変更内容 |
|---------|---------|
| src/storage_manager.py | WordPress URL デフォルト値修正、認証ヘッダー修正 |

### 最終デプロイ結果

| 関数名 | リビジョン | 状態 |
|--------|-----------|------|
| ktrend-main | 00022-mef | ✅ ACTIVE |
| ktrend-line-webhook | 00073-qis | ✅ ACTIVE |
| view-draft | 00057-lab | ✅ ACTIVE |

---

## 2026-02-08: 広告実装・修正記録

### 実装した広告タイプ

1. **記事内広告** - 記事の中間と末尾に配置
2. **サイドバー広告** - 右サイドバー（PC表示時）
3. **インフィード広告** - カテゴリタブの投稿リスト内（5件ごと）

### 発生した問題と解決策

#### 問題1: 上部スライド広告（アンカー広告）
- **症状**: 画面上部からスライドしてくる広告が邪魔
- **解決**: ヘッダーコードで `overlays: {bottom: false, top: false}` を設定

#### 問題2: 広告がcheckpoint（要約セクション）に重なる
- **症状**: Google自動広告がarticle-highlightsセクションに重なって表示
- **解決策**:
  1. Google自動広告（page-level ads）を完全に無効化
  2. checkpoint直後の広告配置を削除（中間と末尾のみに変更）
  3. CSSで保護:
     ```css
     .article-highlights {
         position: relative;
         z-index: 100 !important;
         isolation: isolate;
     }
     .article-highlights ins,
     .article-highlights .adsbygoogle {
         display: none !important;
     }
     ```

#### 問題3: 投稿日付が全て同じ（2026-02-04）
- **症状**: 142件の投稿が同じ日時に集中
- **原因**: 一括インポート時に元の日付が保持されなかった
- **解決**: スラッグから日付を抽出してSQLで更新（791件修正）
  - パターン: `YYMMDD + category` または `category + YYMMDD`

### 関連ファイル

| ファイル | 場所 |
|---------|------|
| ktrend-ads.php | `/var/www/html/wp-content/mu-plugins/` |
| category-tabs.php | `/var/www/html/wp-content/mu-plugins/` |
| ihaf_insert_header | WordPress option |

### AdSense設定

- **Publisher ID**: `ca-pub-6657168802277658`
- **自動広告**: 無効（手動配置のみ）
- **アンカー広告**: 無効

---

## 参照ドキュメント

- [BUGFIX_LOG.md](./BUGFIX_LOG.md) - 詳細な修正記録
- [DEVELOPMENT.md](./DEVELOPMENT.md) - 開発者ガイド
- [CLAUDE.md](./CLAUDE.md) - Claude Code ガイドライン
- [.claudecode_context.md](./.claudecode_context.md) - AIエージェント向けコンテキスト
