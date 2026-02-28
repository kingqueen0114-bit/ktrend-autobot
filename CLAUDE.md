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
* **ステータス:** 現在、開発はひと段落している状態。
* **再開時の挙動:** まずは前回の変更点や現状のステータスを確認し、次にやるべきタスクを整理してから作業に入ること。

## 5. ⚠️ 重要な技術的注意事項

### 依存関係（requirements.txt）
* **`google-generativeai`** パッケージを使用中。コード内のimportは `import google.generativeai as genai`。
* ❌ `google-genai`（新SDK）に変更すると **AI機能が全停止する**。importとパッケージ名が一致しないため。
* 将来的に `google-genai` に移行する場合は、import文も全て `from google import genai` に書き換える必要がある。
* **Geminiモデル:** `gemini-2.0-flash` を使用（`gemini-1.5-flash` は廃止済み）

### Google Custom Search API
* 403エラーが断続的に発生する既知の問題あり。
* `fetch_trends.py` の `_search_google` にGemini AIフォールバックを実装済み。
* API失敗時は `_search_with_gemini` でトレンドデータを生成する。

### view_draft 編集画面の構造
* `cloud_entry.py` 内の `view_draft` 関数にHTMLテンプレートが直接埋め込まれている（f-string）。
* **f-string内のJavaScript注意点:**
  * `{}` → `{{}}` にエスケープが必要
  * JS template literal の `${var}` → 使用不可。文字列連結で代替すること。
  * HTML属性値内の `>` → `&gt;` にエスケープすること（HTMLパーサーが壊れる）
* 編集画面の機能一覧:
  - 📷 アイキャッチ画像（URLまたはファイルアップロード、GCSに保存）
  - 📝 画像クレジット・出典欄
  - 🏷️ カテゴリ選択 + アーティストタグ（カンマ区切り）
  - ✏️ 記事本文（Markdown、ツールバー付き: H2/H3/太字/引用/リスト/画像挿入）
  - 🐦 X投稿案 2件（AI自動生成）
  - 📱 SNS投稿バリエーション（ニュース、Luna A/B）
  - 👁️ プレビュータブ（Markdown→HTML変換）

### デプロイ
* `./deploy.sh` でCloud Functionsにデプロイ（asia-northeast1）
* 関数URL: `https://ktrend-autobot-nnfhuwwfiq-an.a.run.app`
* エンドポイント: `/webhook`, `/draft/{id}`, `/approve`, `/reject`

### WordPress連携
* **認証方式:** REST API + Application Password（`WORDPRESS_APP_PASSWORD`環境変数）
* ❌ `_wp_admin_login` 方式は使わない（過去に未完成で放棄された実装）
* `save_draft_to_wordpress`: 下書き保存（status: draft）
* `publish_to_wordpress`: 公開（status: publish）。既存のWP投稿IDがあればステータス更新
* 画像アップロード: `upload_image_to_wordpress` → REST Media API

### LINE Bot
* SDK v1（`linebot`）を使用。v3（`linebot.v3`）ではない。
* リッチメニュー: 3行縦レイアウト（記事作成 / 未公開記事 / 統計）
* カテゴリ選択: FlexMessage + message actionで実装（PostbackActionではない）

### Firestore
* コレクション: `article_drafts`
* フィルタはFieldFilter構文を使用: `.where(filter=FieldFilter(...))`
* `order_by` と `where` の組み合わせにはFirestoreインデックスが必要

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
- **品質チェック:** `checks/quality_check.py` → 7項目スコアリング (score ≥ 90)
- **ファクトチェック:** `checks/fact_checker.py` → Gemini検証 (fact ≥ 80)
- **自動リライト:** スコア不足時、最大3回リライト
- **WordPress下書き保存:** `src/storage_manager.py` → REST API

### Phase 4: 公開管理 (Publication Management)
- **LINE承認リクエスト:** Flex Message（承認/予約/編集/却下/再生成）
- **承認 → WordPress公開:** status: draft → publish
- **編集:** Web UI (`/draft/{id}`) → Markdown編集 + プレビュー
- **予約公開:** WordPress status: future
- **却下 → 再生成:** 新しいトレンドで再試行

### 統計・レポート
- **実行ログ:** Firestore `execution_logs`
- **日次統計:** Firestore `daily_stats`
- **GA4レポート:** 週次LINE送信
