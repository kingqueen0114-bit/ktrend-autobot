# K-TREND TIMES プロジェクト進捗記録

> 最終更新: 2026-03-06 01:45 JST
> 作業者: Gemini (Antigravity)
> 次の作業者向け: Claude / Gemini / どのAIでも読めるように記載

---

## 📌 プロジェクト概要

**K-TREND TIMES** は韓国トレンド情報メディアサイト。
WordPress → Sanity CMS + Next.js への移行プロジェクト。

### アーキテクチャ

```
┌──────────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  GCP Cloud Functions │     │  Sanity CMS     │     │  Vercel          │
│  ・記事自動生成       │────▶│  ・記事データ保管 │◀────│  ・Next.js SSR   │
│  ・Gemini 2.0 Flash  │     │  ・画像CDN       │     │  ・ISR (60秒)    │
│  ・X(Twitter)投稿    │     │  ・GROQ API      │     │  ・Git連携済み   │
└──────────────────────┘     └─────────────────┘     └──────────────────┘
  (記事を作る)                (記事を貯める)           (記事を見せる)
```

### 主要URL

| 用途 | URL |
|------|-----|
| **本番サイト (Vercel)** | https://frontend-eight-blond-69.vercel.app/ |
| **旧WordPressサイト** | https://k-trendtimes.com/ |
| **Sanity Studio** | https://www.sanity.io/organizations/oMqyDfV3F/project/3pe6cvt2 |
| **GitHub リポジトリ** | https://github.com/kingqueen0114-bit/ktrend-autobot |
| **Vercel ダッシュボード** | https://vercel.com/kingqueen0114-bits-projects/frontend |

### リポジトリ構成

```
ktrend-autobot/
├── frontend/          ← Next.js フロントエンド (Vercel にデプロイ)
│   ├── app/           ← App Router ページ
│   ├── components/    ← React コンポーネント
│   ├── lib/           ← Sanity client, queries, SEO utilities
│   └── public/        ← 静的アセット (logo.png, favicon.png)
├── src/               ← Python バックエンド (GCP Cloud Functions)
│   ├── content_generator.py
│   ├── content_prompts.py
│   ├── sanity_client.py
│   └── ...
├── scripts/           ← 移行・ユーティリティスクリプト
│   ├── migrate_wp_to_sanity.py
│   └── backfill_artist_tags.py
├── sanity/            ← Sanity Studio 設定
└── .env.yaml          ← 環境変数 (API keys)
```

---

## ✅ 2026-03-05〜06 セッションで完了した作業

### 1. WordPress → Sanity 記事移行の確認

- **全805件**の記事がSanityに移行済みであることを確認
- 画像、カテゴリ、タグも移行済み
- 移行スクリプト: `scripts/migrate_wp_to_sanity.py`

### 2. アーティストタグの一括反映 ✅

**スクリプト**: `scripts/backfill_artist_tags.py`

| 項目 | 結果 |
|------|------|
| Sanity全記事数 | 805件 |
| タグ反映済み | 268件 |
| ユニークタグ数 | 50個 |
| エラー | 0件 |

**手法**: Gemini API がサンドボックス制限でアクセス不可だったため、以下の2段階方式を採用:
1. WordPress REST API からタグ-記事紐づけを取得
2. 80+パターンのマスターキーワードリストでタイトルからアーティスト名を自動抽出

**反映されたタグ例**: BTS, TWICE, BLACKPINK, NewJeans, IVE, aespa, SEVENTEEN, LE SSERAFIM, ENHYPEN, Stray Kids, etc.

**残り537件**はグルメ・旅行・美容などアーティスト関連でない記事のため、タグ未設定が正常。

### 3. ホームページレイアウト変更 ✅

**変更ファイル**: `frontend/app/page.tsx`

| Before | After |
|--------|-------|
| 1大+2小のフィーチャーグリッド + 3列カードグリッド | フルワイドヒーロー + 縦リスト表示 |
| 12件表示 | 30件表示 |
| `ArticleCard` コンポーネント使用 | カテゴリページと同じリスト形式 |

カテゴリページ (`category/[slug]/page.tsx`) と同一のレイアウト:
- 最新記事をフルワイドの16:9ヒーロー画像で表示
- 残りは左サムネイル + 右テキスト (タイトル・抜粋・カテゴリバッジ・日付・アーティストタグ)

### 4. ロゴ・ファビコン・カラー変更 ✅

**変更ファイル**: 22ファイル

#### アセット追加
| ファイル | 取得元 |
|----------|--------|
| `frontend/public/logo.png` | WordPress (`site-logo-scaled.png`) |
| `frontend/public/favicon.png` | WordPress (`favicon.png`) |
| `frontend/app/favicon.ico` | favicon.png から PIL で生成 |

#### カラー変更 (全18ファイル一括)

| 変更対象 | Before | After |
|----------|--------|-------|
| メインカラー (CSS変数) | `#f84643` (赤) | `#292929` (黒) |
| ホバーカラー | `#e03e3b` (暗赤) | `#444` (グレー) |
| ティッカーバー背景 | 赤グラデーション (`from-[#f84643] to-[#ff6b6b]`) | ソリッドダーク (`#292929`) |

**変更されたファイル一覧**:
- `app/globals.css` — CSS変数 `--color-primary`
- `app/layout.tsx` — favicon メタデータ追加
- `app/page.tsx` — ホームページ
- `app/articles/page.tsx`, `app/articles/[slug]/page.tsx`
- `app/category/[slug]/page.tsx`
- `app/artist/[tag]/page.tsx`
- `app/tag/[slug]/page.tsx`
- `app/search/page.tsx`
- `app/drafts/page.tsx`
- `components/Header.tsx` — テキストロゴ → 画像ロゴ, ティッカー色変更
- `components/Footer.tsx`
- `components/Sidebar.tsx`
- `components/ArticleCard.tsx`
- `components/ScrollToTop.tsx`
- `components/SearchForm.tsx`
- `components/PortableText.tsx`
- `components/editor/ArticleEditor.tsx`

### 5. Vercel Git連携の設定 ✅

- Vercelプロジェクト `frontend` にGitHubリポジトリ `kingqueen0114-bit/ktrend-autobot` を接続
- Root Directory: `frontend`
- Framework Preset: Next.js
- Production Branch: `main`
- **今後は `git push` で自動デプロイ**される

---

## 🔑 重要な環境情報

### Sanity
- **Project ID**: `3pe6cvt2`
- **Dataset**: `production`
- **API Token**: `.env.yaml` 内に格納 (macOS サンドボックスでアクセス制限あり)
- **GROQ クエリファイル**: `frontend/lib/queries.ts`

### Vercel
- **デプロイ方式**: Git 連携 (GitHub → Vercel 自動ビルド)
- **環境変数**: Vercel ダッシュボードで設定済み

### GCP
- **記事生成**: Cloud Functions (Python)
- **AI**: Gemini 2.0 Flash
- **検索**: Google Custom Search API

### WordPress (旧サイト)
- **URL**: https://k-trendtimes.com/
- **REST API**: `https://k-trendtimes.com/wp-json/wp/v2/`
- **状態**: まだ稼働中 (移行完了後に停止予定)

---

## ⚠️ 既知の制約・注意点

1. **macOS サンドボックス**: `.env` / `.env.yaml` の直接読み込みが制限される場合がある。API トークンはスクリプト実行時に引数で渡すか、Vercel環境変数を使用。
2. **npm cache 権限**: `~/.npm` に root 所有ファイルが存在。`sudo chown -R $(whoami) ~/.npm` で修正可能。
3. **ISR キャッシュ**: Sanity データ変更後、最大60秒のキャッシュ遅延あり (`revalidate = 60`)。
4. **カテゴリカラー**: 各カテゴリには個別の色が設定されており (`Header.tsx` の `categories` 配列)、メインカラーの黒変更とは独立。

---

## 📋 未着手のタスク

- [ ] SEO・SNSエンゲージメント向上チューニング
- [ ] X(Twitter)用プロンプトの見直し
- [ ] アナリティクス・レポート機能の強化
- [ ] 記事内リッチコンテンツ対応 (PortableText 拡張)
- [ ] レガシーコード (WordPress関連) の整理・削除
- [ ] カスタムドメインの設定 (k-trendtimes.com → Vercel)
- [ ] GCPのCloud Functions の安定稼働監視

---

## 📂 Git コミット履歴 (このセッション)

```
342f72b - ロゴ・ファビコン追加 & メインカラーを白黒ベースに変更
3eb6839 - trigger vercel deploy
059269d - ホームページをカテゴリページと同じリスト形式に変更
9830cf5 - (前回セッションまでのコミット)
```
