import { groq } from 'next-sanity'

// 記事一覧（トップページ・カテゴリページ用）
export const articlesQuery = groq`
  *[_type == "article" && defined(publishedAt)] | order(publishedAt desc) [0...$limit] {
    _id,
    title,
    slug,
    publishedAt,
    excerpt,
    mainImage,
    "category": category->{title, slug, color},
    artistTags,
    qualityScore
  }
`

// カテゴリ別記事一覧
export const articlesByCategoryQuery = groq`
  *[_type == "article" && defined(publishedAt) && category->slug.current == $categorySlug] | order(publishedAt desc) [0...$limit] {
    _id,
    title,
    slug,
    publishedAt,
    excerpt,
    mainImage,
    "category": category->{title, slug, color},
    artistTags
  }
`

// 記事詳細
export const articleBySlugQuery = groq`
  *[_type == "article" && slug.current == $slug][0] {
    _id,
    title,
    slug,
    body,
    excerpt,
    mainImage,
    imageCredit,
    publishedAt,
    seo,
    category->{
      title,
      slug,
      color
    },
    author->{
      name,
      slug,
      role,
      image,
      bio
    },
    sources,
    tags[]->{
      title,
      slug
    },
    artistTags,
    highlights,
    qualityScore,
    sourceUrl,
    xPost1,
    xPost2,
    newsPost,
    lunaPostA,
    lunaPostB,
    researchReport
  }
`

// 記事のカテゴリスラッグのみ取得（ヘッダーのアクティブタブ判定用）
export const articleCategorySlugQuery = groq`
  *[_type == "article" && slug.current == $slug][0] {
    "categorySlug": category->slug.current
  }
`

// Draft記事（プレビュー用）
export const draftArticleQuery = groq`
  *[_type == "article" && _id == $id][0] {
    _id,
    title,
    slug,
    publishedAt,
    body,
    excerpt,
    mainImage,
    imageCredit,
    seo,
    "category": category->{_id, title, slug, color},
    "tags": tags[]->{_id, title, slug},
    artistTags,
    highlights,
    qualityScore,
    sourceUrl,
    xPost1,
    xPost2,
    newsPost,
    lunaPostA,
    lunaPostB,
    researchReport
  }
`

// 関連記事（同カテゴリ）
export const relatedArticlesQuery = groq`
  *[_type == "article" && defined(publishedAt) && category->slug.current == $categorySlug && _id != $currentId] | order(publishedAt desc) [0...4] {
    _id,
    title,
    slug,
    publishedAt,
    mainImage,
    "category": category->{title, slug, color}
  }
`

// 全カテゴリ
export const categoriesQuery = groq`
  *[_type == "category"] | order(title asc) {
    _id,
    title,
    slug,
    color,
    description
  }
`

// 全カテゴリ（記事数付き）
export const categoriesWithCountQuery = groq`
  *[_type == "category"] | order(title asc) {
    _id,
    title,
    slug,
    color,
    description,
    "articleCount": count(*[_type == "article" && references(^._id) && defined(publishedAt)])
  }
`

// サイトマップ用
export const sitemapQuery = groq`
  *[_type == "article" && defined(publishedAt)] | order(publishedAt desc) {
    slug,
    publishedAt,
    _updatedAt
  }
`

// 前後の記事（記事詳細ページ用）
export const adjacentArticlesQuery = groq`{
  "prev": *[_type == "article" && defined(publishedAt) && publishedAt < $publishedAt] | order(publishedAt desc) [0] {
    _id, title, slug, mainImage
  },
  "next": *[_type == "article" && defined(publishedAt) && publishedAt > $publishedAt] | order(publishedAt asc) [0] {
    _id, title, slug, mainImage
  }
}`

// 下書き一覧（編集画面用）
export const draftsListQuery = groq`
  *[_type == "article" && _id in path("drafts.**")] | order(_updatedAt desc) {
    _id,
    title,
    slug,
    _updatedAt,
    mainImage,
    "category": category->{title, slug, color},
    qualityScore
  }
`

// おすすめ記事（ランダム風に最新記事から取得）
export const recommendedArticlesQuery = groq`
  *[_type == "article" && defined(publishedAt) && _id != $currentId] | order(publishedAt desc) [0...8] {
    _id,
    title,
    slug,
    publishedAt,
    excerpt,
    mainImage,
    "category": category->{title, slug, color}
  }
`

// 検索クエリ
export const searchQuery = groq`
  *[_type == "article" && defined(publishedAt) && (
    title match $q + "*" ||
    excerpt match $q + "*" ||
    pt::text(body) match $q + "*"
  )] | order(publishedAt desc) [0...$limit] {
    _id,
    title,
    slug,
    publishedAt,
    excerpt,
    mainImage,
    "category": category->{title, slug, color},
    artistTags
  }
`

// 検索結果カウント
export const searchCountQuery = groq`
  count(*[_type == "article" && defined(publishedAt) && (
    title match $q + "*" ||
    excerpt match $q + "*" ||
    pt::text(body) match $q + "*"
  )])
`

// タグ別記事一覧
export const articlesByTagQuery = groq`
  *[_type == "article" && defined(publishedAt) && references(*[_type == "tag" && slug.current == $tagSlug]._id)] | order(publishedAt desc) [0...$limit] {
    _id,
    title,
    slug,
    publishedAt,
    excerpt,
    mainImage,
    "category": category->{title, slug, color},
    artistTags
  }
`

// タグ情報取得
export const tagBySlugQuery = groq`
  *[_type == "tag" && slug.current == $tagSlug][0] {
    _id,
    title,
    slug
  }
`

// タグ別記事数
export const tagArticlesCountQuery = groq`
  count(*[_type == "article" && defined(publishedAt) && references(*[_type == "tag" && slug.current == $tagSlug]._id)])
`

// 全記事数
export const articlesCountQuery = groq`
  count(*[_type == "article" && defined(publishedAt)])
`

// ページネーション付き記事一覧
export const articlesPaginatedQuery = groq`
  *[_type == "article" && defined(publishedAt)] | order(publishedAt desc) [$start...$end] {
    _id,
    title,
    slug,
    publishedAt,
    excerpt,
    mainImage,
    "category": category->{title, slug, color},
    artistTags
  }
`

// アーティストタグ別記事一覧
export const articlesByArtistTagQuery = groq`
  *[_type == "article" && defined(publishedAt) && $artistTag in artistTags] | order(publishedAt desc) [0...$limit] {
    _id,
    title,
    slug,
    publishedAt,
    excerpt,
    mainImage,
    "category": category->{title, slug, color},
    artistTags
  }
`

// アーティストタグ別記事カウント
export const artistTagArticlesCountQuery = groq`
  count(*[_type == "article" && defined(publishedAt) && $artistTag in artistTags])
`

// All unique artist tags with article counts
export const allArtistTagsQuery = groq`
  array::unique(*[_type == "article" && defined(publishedAt) && defined(artistTags)].artistTags[])
`
