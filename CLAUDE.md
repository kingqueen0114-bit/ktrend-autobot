# Claude Code Project Guidelines

このプロジェクトでは、以下のガイドラインを **最優先ルール** として常時遵守してください。

## 1. 🔐 セキュリティと機密情報の扱い (最重要)
* **環境変数管理方針:**
    * **ローカル開発:** `.env` または `.env.yaml` ファイルを使用すること。
    * **本番環境:** Google Cloud Secret Manager を使用すること。
    * **禁止事項:** 1Password CLI (`op` コマンド) の使用は **一切禁止**。
    * APIキー、DBパスワード、トークン等はコードや設定ファイルに **絶対に直書きしない** こと。
* **ログ出力の禁止:**
    * 取得した機密情報（Secret）そのものをターミナルやログ（stdout/stderr）に表示しないこと。
* **詳細:** [.claudecode_context.md](./.claudecode_context.md) および [DEVELOPMENT.md](./DEVELOPMENT.md) を参照。

## 2. 🤖 自動化モード (Agentic Workflow) の行動指針
* **状況把握 (Context First):**
    * タスク開始時は、まず `ls -R` や主要な設定ファイル（package.json, requirements.txt等）を読み、プロジェクト構造と依存関係を把握してから計画を立てること。
* **計画と実行 (Plan & Execute):**
    * いきなりコードを書き換えず、「1. 現状分析」「2. 修正案」「3. 実装」「4. 検証」のステップで思考すること。
    * 既存のコードスタイル（命名規則、ディレクトリ構成）を尊重し、逸脱しないこと。
* **検証 (Verification):**
    * コード修正後は、必ず関連するテストやLintを実行し、エラーがないことを確認してから完了報告をすること。

## 3. 🛠 環境固有のルール
* **言語:** ユーザーへの応答は **日本語** で行うこと。
* **役割:** あなたは「セキュリティ意識の高いシニアDevOpsエンジニア」として振る舞うこと。
* **コマンド実行:**
    * 読み取り専用コマンド（`cat`, `ls`, `grep`）は確認なしで実行してよい。
    * ファイルの削除や破壊的な変更を行う場合は、事前に簡潔に許可を求めること。

## 4. プロジェクトの状態 (User Context)
* **ステータス:** WordPress → Sanity + Next.js 移行完了（Phase 1-5）。Phase 6（PV growth）は進行中。
* **再開時の挙動:** まずは前回の変更点や現状のステータスを確認し、次にやるべきタスクを整理してから作業に入ること。

## 5. ⚠️ 重要な技術的注意事項

### アーキテクチャ概要（移行後）

```
[LINE Bot / Cloud Scheduler]
    ↓
[Cloud Functions (Python)] ← バックエンド（記事生成・品質保証・承認管理）
    ↓
[Sanity CMS] ← コンテンツ管理（記事・カテゴリ・タグ）
    ↓
[Next.js (Vercel)] ← フロントエンド（SSG/ISR・Draft Mode・編集UI）
    ↓
[X (Twitter) 自動投稿] ← 承認時に自動ポスト
```

### CMS: Sanity
* **Project ID:** `3pe6cvt2` / **Dataset:** `production`
* **API:** Sanity HTTP Mutations API + GROQ クエリ
* **Python クライアント:** `src/sanity_client.py`（Secret Manager or 環境変数 `SANITY_API_TOKEN` でトークン取得）
* **Portable Text:** `src/portable_text_builder.py`（Markdown → Portable Text 変換）
* **スキーマ:** `sanity/` ディレクトリ（article, category, tag, siteSettings）
* **カテゴリ:** 8種 seeded（artist, beauty, fashion, gourmet, koreantrip, event, trend, lifestyle）
* **Studio:** `sanity/` ディレクトリで `sanity dev` で起動

### フロントエンド: Next.js
* **ディレクトリ:** `frontend/` (App Router)
* **デプロイ先:** Vercel
* **カスタムドメイン:** `https://k-trendtimes.com` (= `www.k-trendtimes.com`)
* **Vercel URL（内部）:** `https://frontend-eight-blond-69.vercel.app`
* **機能:**
  - Draft Mode（プレビュー: `/api/preview`）
  - ISR（Incremental Static Regeneration）
  - Sanity Webhook → `/api/revalidate` でキャッシュ再検証
  - 編集UI: `/edit/[id]` ページ
  - GA4 トラッキング: `G-462773259`
* **主要コンポーネント:**
  - `SwipeNavigator.tsx` — SmartNews風ページフリップ（スワイプナビゲーション）
  - `Header.tsx` — モバイルタブ横スクロール、カラーインジケーター
  - `Sidebar.tsx` — アーティストタグ表示（ピルボタン）
* **Vercel環境変数:** `SANITY_API_TOKEN`, `PREVIEW_SECRET`, `EDIT_SECRET`, `SANITY_WEBHOOK_SECRET`

### 依存関係（requirements.txt）
* **`google-generativeai`** パッケージを使用中。コード内のimportは `import google.generativeai as genai`。
* ❌ `google-genai`（新SDK）に変更すると **AI機能が全停止する**。importとパッケージ名が一致しないため。
* 将来的に `google-genai` に移行する場合は、import文も全て `from google import genai` に書き換える必要がある。
* **Geminiモデル:** `gemini-2.0-flash` を使用（`gemini-1.5-flash` は廃止済み）
* **tweepy:** `>=4.14.0`（X自動投稿用）

### Google Custom Search API
* 403エラーが断続的に発生する既知の問題あり。
* `fetch_trends.py` の `_search_google` にGemini AIフォールバックを実装済み。
* API失敗時は `_search_with_gemini` でトレンドデータを生成する。

### 編集画面
* **現行:** Next.js `/edit/[id]` ページに移行済み（`frontend/app/edit/[id]/page.tsx`）
* **リダイレクト:** `cloud_entry.py` 内の `view_draft` は Next.js 編集ページにリダイレクトする
* **レガシー（参考用）:** 旧 `view_draft` 関数のf-string HTML テンプレートは `handlers/draft_editor.py` に残存
  * f-string内のJavaScript注意点:
    * `{}` → `{{}}` にエスケープが必要
    * JS template literal の `${var}` → 使用不可。文字列連結で代替すること。
    * HTML属性値内の `>` → `&gt;` にエスケープすること（HTMLパーサーが壊れる）

### デプロイ
* **Cloud Functions:** `./deploy.sh` でデプロイ（asia-northeast1）
  * 関数URL: `https://ktrend-autobot-nnfhuwwfiq-an.a.run.app`
  * エンドポイント: `/webhook`, `/draft/{id}`, `/approve`, `/reject`
  * Secret Manager追加: `SANITY_API_TOKEN`, `EDIT_SECRET`, `PREVIEW_SECRET`, `X_API_KEY`, `X_API_KEY_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`
* **Next.js (Vercel):** `cd frontend && npx vercel --prod`
* **Sanity Studio:** `cd sanity && sanity deploy`
* **DNS:** k-trendtimes.com → Vercel（A: `216.198.79.1`, CNAME www: `09c5d989656e13ac.vercel-dns-017.com.`）

### X (Twitter) 自動投稿
* **実装:** `src/x_poster.py`（tweepy v1.1 画像アップロード + v2 ツイート投稿）
* **トリガー:** 記事承認時に自動投稿（`handlers/draft_actions.py`）
* **API クレデンシャル（環境変数）:**
  * `X_API_KEY`, `X_API_KEY_SECRET`
  * `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`

### WordPress連携（⚠️ Sanityに移行済み・レガシー）
> **注意:** 新規記事は全て Sanity API を使用。以下は移行前の参考情報。
> `storage_manager.py` は Sanity API 対応に全面書き換え済み（後方互換エイリアスあり）。

* **認証方式:** REST API + Application Password（`WORDPRESS_APP_PASSWORD`環境変数）
* ❌ `_wp_admin_login` 方式は使わない（過去に未完成で放棄された実装）
* `save_draft_to_wordpress`: 下書き保存（status: draft）→ **現在は `save_draft` が Sanity API を呼び出す**
* `publish_to_wordpress`: 公開（status: publish）→ **現在は `publish_article` が Sanity API を呼び出す**
* 画像アップロード: `upload_image_to_wordpress` → REST Media API → **現在は Sanity Assets API を使用**

### LINE Bot
* SDK v1（`linebot`）を使用。v3（`linebot.v3`）ではない。
* Webhook URL: `https://ktrend-autobot-nnfhuwwfiq-an.a.run.app`
* リッチメニュー: 3行縦レイアウト（記事作成 / 未公開記事 / 統計）
* カテゴリ選択: FlexMessage + message actionで実装（PostbackActionではない）
* 承認リクエスト: Flex Message（承認/予約/編集/却下/再生成）
  * 編集ボタン → Next.js 編集ページ URL (`k-trendtimes.com/edit/{id}`)
  * プレビューボタン → Next.js プレビューページ URL
* LINE編集 → Firestore + **Sanity同期** (`edit_actions.py` の `process_edit_text` で `sanity_client.patch` 呼び出し)

### Firestore
* コレクション: `article_drafts`
* フィルタはFieldFilter構文を使用: `.where(filter=FieldFilter(...))`
* `order_by` と `where` の組み合わせにはFirestoreインデックスが必要

### 主要ファイル変更一覧（移行による）

| ファイル | 変更内容 |
|---------|---------|
| `src/sanity_client.py` | **新規** Sanity HTTP API ラッパー（Mutations/GROQ/Assets） |
| `src/portable_text_builder.py` | **新規** Markdown → Portable Text 変換 |
| `src/x_poster.py` | **新規** X (Twitter) 自動投稿（v1.1 media + v2 tweet） |
| `src/storage_manager.py` | **全面書き換え** WP API → Sanity API（後方互換エイリアスあり） |
| `src/notifier.py` | URL変更（Cloud Functions → Next.js）、プレビューボタン追加 |
| `handlers/draft_actions.py` | X自動投稿追加、draft_id passing、Sanity経由スケジュール |
| `handlers/draft_editor.py` | Next.js 編集ページへリダイレクト |
| `handlers/generation_actions.py` | slug パラメータ追加 |
| `handlers/schedulers.py` | slug パラメータ追加 |
| `utils/helpers.py` | draft_id を publish 呼び出しに追加 |

## 6. 🎯 オーケストレーターモード (Manager Mode)

### 基本原則
* **Claudeはマネージャー/オーケストレーターとして振る舞う。自分では一切実装しない。**
* 全てのコード変更・調査・テストは **Task agent（subagent）** に委任すること。
* タスクは可能な限り **細分化**（1 subagent = 1 明確なアウトプット）して並列実行すること。
* subagentの結果を **レビュー・統合・判断** するのがマネージャーの役割。

### PDCAサイクルの構築

すべてのタスクは以下のPDCAサイクルで管理すること：

#### Plan（計画）
1. TodoWriteでタスクを細分化して一覧化
2. 依存関係の特定（並列実行可能なタスクを識別）
3. 各タスクの完了条件（Definition of Done）を明確化
4. Explore agentで現状調査 → 計画の精度向上

#### Do（実行）
1. 独立したタスクは **並列でsubagentに委任**（Task tool）
2. 各subagentには以下を明示的に指示：
   - 目的（何を達成するか）
   - スコープ（どのファイルを変更するか）
   - 制約（変更してはいけないもの）
   - 完了条件（どうなったら完了か）
3. subagentの結果を逐次確認し、TodoWriteを更新

#### Check（検証）
1. subagentの出力結果をレビュー
2. 別のsubagent（テスト担当）で検証を実行
3. 品質基準に満たない場合は再実行を指示
4. 全タスク完了後、統合テストをsubagentに委任

#### Act（改善）
1. 問題があれば原因分析をsubagentに委任
2. 修正タスクを新たに生成してPDCAを再回転
3. 学んだ教訓をメモリに記録

### subagent委任のルール

| 状況 | 使用するsubagent |
|------|----------------|
| コードベース調査・ファイル検索 | `Explore` agent |
| 実装計画の設計 | `Plan` agent |
| コード実装・ファイル編集 | `Bash` agent または `general-purpose` agent |
| テスト実行・検証 | `Bash` agent |
| 複雑な調査・マルチステップ | `general-purpose` agent |

### 禁止事項
* マネージャー自身が Edit/Write ツールで直接コードを書くこと
* subagentの結果を確認せずに次のステップに進むこと
* TodoWriteを使わずにタスクを開始すること

## 7. 📰 記事制作パイプライン（Article Production Pipeline）

### フロー概要

```
[Phase 1: トレンド収集] → [Phase 2: コンテンツ生成] → [Phase 3: 品質保証] → [Phase 4: 公開管理]
```

### Phase 1: トレンド収集 (Trend Discovery)
- **トリガー:** Cloud Scheduler (毎日09:00 JST) / LINE テキスト / LINE カテゴリ選択
- **実行:** `src/fetch_trends.py` → Google Custom Search + Gemini Grounding
- **出力:** トレンドデータ（title, snippet, image_url, source_url, original_text）
- **品質ゲート:** 重複排除、24時間以内フィルタ、最大4件制限

### Phase 2: コンテンツ生成 (Content Generation)
- **SNS生成:** `src/content_generator.py` → news_post, luna_post_a, luna_post_b
- **CMS記事生成:** Gemini REST API + Grounding → title, lead, body, meta_description
- **X投稿案:** 2件自動生成（タメ語＋絵文字）
- **ソース注入:** source_articles → プロンプトに注入

### Phase 3: 品質保証 (Quality Assurance)
- **自動修正:** `checks/auto_fix.py` → JSON修正、フィールド補完
- **品質チェック:** `checks/quality_check.py` → 7項目スコアリング (score >= 90)
- **ファクトチェック:** `checks/fact_checker.py` → Gemini検証 (fact >= 80)
- **自動リライト:** スコア不足時、最大3回リライト
- **Sanity下書き保存:** `src/storage_manager.py` → Sanity HTTP Mutations API
  - Markdown → Portable Text 変換（`src/portable_text_builder.py`）
  - 画像: Sanity Assets API にアップロード

### Phase 4: 公開管理 (Publication Management)
- **LINE承認リクエスト:** Flex Message（承認/予約/編集/却下/再生成）
- **承認 → Sanity公開:** ドラフト → 公開ドキュメントに昇格
- **X自動投稿:** 承認時に `src/x_poster.py` で自動ツイート（画像付き）
- **編集:** Next.js `/edit/[id]` ページ → Sanity API で保存
- **予約公開:** Sanity スケジュール公開
- **却下 → 再生成:** 新しいトレンドで再試行

### 統計・レポート
- **実行ログ:** Firestore `execution_logs`
- **日次統計:** Firestore `daily_stats`
- **GA4レポート:** 週次LINE送信
