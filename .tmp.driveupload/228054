# K-Trend Times 記事生成パイプライン ― 品質フロー全体図

## パイプライン概要（`handlers/schedulers.py: trigger_daily_fetch()`）

```mermaid
flowchart TD
    A[Cloud Scheduler / LINE] -->|fetch_trends| B[1. トレンド取得]
    B --> C[2. 記事生成]
    C --> D[3. auto_fix]
    D --> E[4. quality_check]
    E -->|reject| F[5. リライト ≤3回]
    F --> D
    E -->|pass| G[6. ファクトチェック]
    G --> H[7. WordPress保存]
    H --> I{品質ゲート}
    I -->|score=100 & fact≥80| J[✅ LINE通知]
    I -->|score<100 or fact<80| K[⚠️ 通知なし<br/>WordPress/Firestoreのみ]
```

---

## 各ステップの詳細

### Step 1: トレンド取得 (`src/fetch_trends.py`)
- **モデル**: gemini-2.5-flash → gemini-2.5-flash-lite (フォールバック)
- **Grounding**: Google Search 有効
- **日付注入**: `本日は{today}です` でJST日付をプロンプトに動的注入
- **鮮度制約**: 「直近1週間以内の最新情報のみ」を明記
- **リトライ**: 503/429/ReadTimeout → 最大3回リトライ + モデルフォールバック
- **重複チェック**: Firestore の trend_titles で過去24時間の類似タイトルを排除

### Step 2: 記事生成 (`src/content_generator.py: generate_cms_article()`)
- **モデル**: gemini-2.5-flash → gemini-2.5-flash-lite (フォールバック)
- **System Instruction**: `prompts/system_instruction.txt`（外部ファイル分離）
  - 捏造禁止ルール強化済み（人物×ブランド明記必須）
- **構造化出力**: `responseSchema` でJSON構造を強制 (`schemas/article_schema.py`)
- **Grounding**: Google Search 有効
- **日付注入**: `本日は{today}です` をプロンプト先頭に注入
- **ソース注入**: ソース記事の原文テキスト（最大3000字）をプロンプトに含める
- **戻り値**: `(article_dict, grounding_metadata)` タプル

### Step 3: 自動修正 (`checks/auto_fix.py: auto_fix_article()`)
- `**text**` → テキストのみ（マークダウン除去）
- `*text*` → テキストのみ（クレジット行は保護）
- 装飾記号（■●▶▷◆◇）除去
- 過剰な「!」を最大2個まで削減

### Step 4: 品質チェック (`checks/quality_check.py: quality_check()`)

| # | チェック項目 | 重要度 | 減点 |
|---|---|---|---|
| 1 | URL実在チェック（HEAD リクエスト） | CRITICAL | -25 |
| 2 | 文字数チェック（1000字以上） | HIGH | -10 |
| 3 | 必須フィールド充実度 | HIGH | -10 |
| 4 | ハッシュタグ数（3個以上） | LOW | -2 |
| 5 | Grounding信頼度（≥0.5） | HIGH | -10 |
| 6 | ソース照合（日付の検証） | MEDIUM | -5 |
| 7 | 禁止パターン（**、■等） | MEDIUM | -5 |

**スコア判定:**
- 100点: `auto_publish`
- 90-99: `auto_publish`（現在は100のみ通知）
- 70-89: `review_needed`
- 0-69: `reject` → リライトループへ

### Step 5: リライトループ
- `quality_check` が `reject` → `rewrite_article()` で再生成
- 最大3回リトライ
- 毎回 `auto_fix` → `quality_check` を再実行

### Step 6: ファクトチェック (`checks/fact_checker.py: verify_article_facts()`)
- **目的**: 生成記事の固有名詞の主張を Gemini + Grounding で事実検証
- **重点チェック対象**:
  1. 人物名×ブランド名（アンバサダー就任、コラボ）
  2. 日付×イベント（発売日、公演日）
  3. 数値データ（売上、ランキング）
  4. 固有名詞の組み合せ
- **モデル**: gemini-2.5-flash（temperature=0.1 低温度）
- **結果**:
  - `fact_score` 0-100（検証OK率）
  - `action`: pass / fix_needed / reject
  - UNVERIFIED主張 → `remove_unverified_claims()` で除去 or 編集部注追加

### Step 7: WordPress保存 (`src/storage_manager.py`)
- **`build_wp_content()`**: highlights を ✔️ CHECKPOINT HTML として本文上部に挿入
- **Markdown→HTML変換**: `##` → `<h2>`, `**` → `<strong>` 等
- アイキャッチ画像＋追加画像を WordPressメディアにアップロード
- Yoast SEO メタデータ自動設定

### Step 8: 品質ゲート（LINE通知フィルター）
```python
should_notify = (quality_score == 100) and (fact_score >= 80 or fact_score == -1)
```
- **通過**: LINE に承認リクエスト送信（✅/❌/🔄ボタン付き）
- **不通過**: WordPress/Firestoreには保存されるが、LINE通知なし。ログに記録。

---

## Firestoreに保存されるデータ

| フィールド | 内容 |
|---|---|
| `quality_score` | 品質スコア (0-100) |
| `quality_passed` | auto_publish判定 |
| `quality_warnings` | 品質警告リスト |
| `fact_score` | ファクトスコア (0-100, -1=skipped) |
| `fact_warnings` | 検証NG主張リスト |
| `was_rewritten` | リライト済みか |
| `grounding_sources` | Groundingで取得した実URL一覧 |

---

## 既知の制約・懸念

1. **ファクトチェックの精度**: Gemini自身がチェッカーなので、同じハルシネーションを「正しい」と判定するリスクあり
2. **処理時間**: ファクトチェック追加で1記事あたり+10-30秒。Cloud Functions URL timeout (540s) に注意
3. **score=100 が厳しすぎる可能性**: URL が1つでも 404 → score=75 → 通知されない。サイト側のリンク切れで記事が全滅するリスク
4. **auto_fix と wp_content_builder の二重変換**: auto_fix が `**` を除去した後、wp_content_builder も変換しようとする（ただし既に除去済みなので実害なし）
