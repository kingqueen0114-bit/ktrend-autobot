import { cache } from 'react'
import { notFound } from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'
import { draftMode } from 'next/headers'
import { client, getPreviewClient, optimizedUrl } from '@/lib/sanity'
import { articleBySlugQuery, relatedArticlesQuery, adjacentArticlesQuery, recommendedArticlesQuery } from '@/lib/queries'
import { generateArticleMetadata, articleJsonLd } from '@/lib/seo'
import CategoryBadge from '@/components/CategoryBadge'
import ArticleCard from '@/components/ArticleCard'
import JsonLd from '@/components/JsonLd'
import Sidebar from '@/components/Sidebar'
import ArticleBody from '@/components/ArticleBody'
import ScrollDepthTracker from '@/components/ScrollDepthTracker'
import ShareButtons from '@/components/ShareButtons'
import AdSlot from '@/components/AdSlot'

export const revalidate = 60

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.k-trendtimes.com'

type Props = {
  params: Promise<{ slug: string }>
}

const getArticle = cache(async (slug: string, isPreview: boolean) => {
  const sanityClient = isPreview ? getPreviewClient() : client
  return sanityClient.fetch(articleBySlugQuery, { slug })
})

export async function generateMetadata({ params }: Props) {
  const { slug } = await params
  const decodedSlug = decodeURIComponent(slug)
  const article = await getArticle(decodedSlug, false)
  if (!article) return {}
  return generateArticleMetadata(article)
}

function breadcrumbJsonLd(article: { title: string; slug: { current: string }; category?: { title: string; slug?: { current: string } } }) {
  const items: Array<{
    '@type': string
    position: number
    name: string
    item?: string
  }> = [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'ホーム',
        item: SITE_URL,
      },
    ]

  if (article.category?.slug?.current) {
    items.push({
      '@type': 'ListItem',
      position: 2,
      name: article.category.title,
      item: `${SITE_URL}/category/${article.category.slug.current}`,
    })
  }

  items.push({
    '@type': 'ListItem',
    position: items.length + 1,
    name: article.title,
  })

  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items,
  }
}

export default async function ArticlePage({ params }: Props) {
  const { slug } = await params
  const decodedSlug = decodeURIComponent(slug)
  const { isEnabled: isPreview } = await draftMode()

  const article = await getArticle(decodedSlug, isPreview)

  if (!article) notFound()

  const relatedResult = await client.fetch(relatedArticlesQuery, {
    categorySlug: article.category?.slug?.current || '',
    currentId: article._id,
    artistTags: article.artistTags || [],
  })

  // アーティストタグ優先、カテゴリフォールバック、重複排除で最大4件
  const seenIds = new Set<string>()
  const relatedArticles: any[] = []
  for (const a of [...(relatedResult.byArtistTag || []), ...(relatedResult.byCategory || [])]) {
    if (!seenIds.has(a._id) && relatedArticles.length < 4) {
      seenIds.add(a._id)
      relatedArticles.push(a)
    }
  }

  const adjacentArticles = article.publishedAt
    ? await client.fetch(adjacentArticlesQuery, {
      publishedAt: article.publishedAt,
    })
    : { prev: null, next: null }

  const recommendedResult = await client.fetch(recommendedArticlesQuery, {
    currentId: article._id,
    artistTags: article.artistTags || [],
    categorySlug: article.category?.slug?.current || '',
  })

  // アーティストタグ人気 → 同カテゴリ人気 → 全体人気、重複排除
  const recSeenIds = new Set<string>(relatedArticles.map((a: any) => a._id))
  const recommendedArticles: any[] = []
  for (const a of [
    ...(recommendedResult.byArtistTag || []),
    ...(recommendedResult.byCategoryPopular || []),
    ...(recommendedResult.popular || []),
  ]) {
    if (!recSeenIds.has(a._id) && recommendedArticles.length < 8) {
      recSeenIds.add(a._id)
      recommendedArticles.push(a)
    }
  }

  const imageDimensions = article.mainImage?.asset?.metadata?.dimensions
  const imageUrl = article.mainImage
    ? optimizedUrl(article.mainImage).width(1200).url()
    : null
  const imageWidth = 1200
  const imageHeight = imageDimensions
    ? Math.round(1200 / imageDimensions.aspectRatio)
    : 630

  const date = article.publishedAt
    ? new Date(article.publishedAt).toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
    : ''

  const articleUrl = `${SITE_URL}/articles/${article.slug.current}`

  return (
    <>
      <JsonLd data={articleJsonLd(article)} />
      <JsonLd data={breadcrumbJsonLd(article)} />

      {isPreview && (
        <div className="bg-yellow-400 text-black text-center py-2 text-sm font-medium">
          プレビューモード —{' '}
          <a href="/api/exit-preview" className="underline">
            終了する
          </a>
        </div>
      )}

      <article className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Main content */}
          <div className="w-full lg:w-[70%]">
            {/* Breadcrumb */}
            <nav aria-label="パンくずリスト" className="mb-4">
              <ol className="flex items-center flex-wrap gap-1 text-sm text-[#67737e]">
                <li>
                  <Link href="/" className="hover:text-[#292929] transition-colors">
                    ホーム
                  </Link>
                </li>
                {article.category?.slug?.current && (
                  <>
                    <li aria-hidden="true" className="mx-1">&gt;</li>
                    <li>
                      <Link
                        href={`/category/${article.category.slug.current}`}
                        className="hover:text-[#292929] transition-colors"
                      >
                        {article.category.title}
                      </Link>
                    </li>
                  </>
                )}
                <li aria-hidden="true" className="mx-1">&gt;</li>
                <li className="font-bold text-[#292929] truncate max-w-[200px] md:max-w-[400px]">
                  {article.title}
                </li>
              </ol>
            </nav>

            {/* Category badge */}
            {article.category && (
              <div className="mb-3">
                <CategoryBadge category={article.category} size="md" />
              </div>
            )}

            {/* Title */}
            <h1 className="text-2xl md:text-3xl font-bold text-[#292929] leading-tight mb-4">
              {article.title}
            </h1>

            {/* Meta */}
            <div className="flex items-center gap-3 text-sm text-[#67737e] mb-4">
              <time>{date}</time>
            </div>

            {/* SNS Share Buttons */}
            <ShareButtons url={articleUrl} title={article.title} />

            {/* Main image */}
            {imageUrl && (
              <figure className="mb-6">
                <div className="overflow-hidden rounded-lg">
                  <Image
                    src={imageUrl}
                    alt={article.mainImage?.alt || article.title}
                    width={imageWidth}
                    height={imageHeight}
                    className="w-full h-auto"
                    sizes="(max-width: 768px) 100vw, 70vw"
                    priority
                  />
                </div>
                {(article.mainImage?.credit || article.imageCredit) && (
                  <figcaption className="text-xs text-[#67737e] mt-2">
                    出典: {article.mainImage?.credit || article.imageCredit}
                  </figcaption>
                )}
              </figure>
            )}

            {/* Checkpoint + Article body with read more */}
            <ArticleBody
              highlights={article.highlights}
              body={article.body}
              sourceUrl={article.sourceUrl}
            />

            {/* Sources / References (E-E-A-T) */}
            {article.sources && article.sources.length > 0 && (
              <div className="mt-8 pt-6 border-t border-gray-100">
                <h3 className="text-sm font-bold text-[#67737e] mb-3 flex items-center gap-2">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"></path>
                    <path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"></path>
                  </svg>
                  参考・引用元
                </h3>
                <ul className="space-y-2">
                  {article.sources.map((source: any, idx: number) => (
                    <li key={idx} className="text-sm">
                      {source.url ? (
                        <a
                          href={source.url}
                          target="_blank"
                          rel="noopener noreferrer nofollow"
                          className="text-[#00A4DE] hover:underline break-words"
                        >
                          {source.title}
                        </a>
                      ) : (
                        <span className="text-[#292929]">{source.title}</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Author Card (E-E-A-T) */}
            {article.author && (
              <div className="mt-8 p-6 bg-gray-50 rounded-xl flex flex-col sm:flex-row gap-4 items-start border border-gray-100">
                {article.author.image && (
                  <div className="shrink-0 relative w-16 h-16 rounded-full overflow-hidden shadow-sm">
                    <Image
                      src={optimizedUrl(article.author.image).width(128).height(128).url()}
                      alt={article.author.name}
                      fill
                      className="object-cover"
                      sizes="64px"
                    />
                  </div>
                )}
                <div className="flex-1">
                  <div className="mb-1">
                    <span className="text-xs font-bold px-2 py-0.5 bg-[#292929] text-white rounded mr-2 align-middle">
                      {article.author.role || 'Writer'}
                    </span>
                    <span className="text-lg font-bold text-[#292929] align-middle">
                      {article.author.name}
                    </span>
                  </div>
                  {article.author.bio && (
                    <p className="text-sm text-[#67737e] mt-2 leading-relaxed">
                      {article.author.bio}
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* Artist Tags */}
            {article.artistTags && article.artistTags.length > 0 && (
              <div className="mt-6 flex items-center gap-2 flex-wrap">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#292929" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="shrink-0">
                  <path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z" />
                  <line x1="7" y1="7" x2="7.01" y2="7" />
                </svg>
                {article.artistTags.map((tag: string) => (
                  <Link
                    key={tag}
                    href={`/artist/${encodeURIComponent(tag)}`}
                    className="border border-[#292929] text-[#292929] text-xs font-medium px-3 py-1 rounded-full hover:bg-[#292929] hover:text-white transition-colors"
                  >
                    {tag}
                  </Link>
                ))}
              </div>
            )}

            {/* Previous/Next article navigation */}
            {(adjacentArticles.prev || adjacentArticles.next) && (
              <nav className="mt-10 grid grid-cols-1 md:grid-cols-2 gap-4" aria-label="前後の記事">
                {/* Previous article */}
                {adjacentArticles.prev ? (
                  <Link
                    href={`/articles/${adjacentArticles.prev.slug.current}`}
                    className="group flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:border-[#292929] transition-colors"
                  >
                    {adjacentArticles.prev.mainImage && (
                      <div className="relative w-16 h-16 shrink-0 rounded overflow-hidden">
                        <Image
                          src={optimizedUrl(adjacentArticles.prev.mainImage).width(128).height(128).url()}
                          alt={adjacentArticles.prev.title}
                          fill
                          className="object-cover"
                          sizes="64px"
                        />
                      </div>
                    )}
                    <div className="min-w-0">
                      <span className="text-xs text-[#67737e] block mb-1">前の記事</span>
                      <span className="text-sm font-medium text-[#292929] group-hover:text-[#292929] transition-colors line-clamp-2">
                        {adjacentArticles.prev.title}
                      </span>
                    </div>
                  </Link>
                ) : (
                  <div />
                )}

                {/* Next article */}
                {adjacentArticles.next ? (
                  <Link
                    href={`/articles/${adjacentArticles.next.slug.current}`}
                    className="group flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:border-[#292929] transition-colors md:flex-row-reverse md:text-right"
                  >
                    {adjacentArticles.next.mainImage && (
                      <div className="relative w-16 h-16 shrink-0 rounded overflow-hidden">
                        <Image
                          src={optimizedUrl(adjacentArticles.next.mainImage).width(128).height(128).url()}
                          alt={adjacentArticles.next.title}
                          fill
                          className="object-cover"
                          sizes="64px"
                        />
                      </div>
                    )}
                    <div className="min-w-0">
                      <span className="text-xs text-[#67737e] block mb-1">次の記事</span>
                      <span className="text-sm font-medium text-[#292929] group-hover:text-[#292929] transition-colors line-clamp-2">
                        {adjacentArticles.next.title}
                      </span>
                    </div>
                  </Link>
                ) : (
                  <div />
                )}
              </nav>
            )}

            {/* Related articles */}
            {relatedArticles.length > 0 && (
              <section className="mt-10">
                <h2 className="text-lg font-bold text-[#292929] mb-4 pb-2 border-b-2 border-[#292929]">
                  関連記事
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {relatedArticles.map((related: any) => (
                    <ArticleCard key={related._id} article={related} />
                  ))}
                </div>
              </section>
            )}

            {/* Ad between sections */}
            <div className="mt-8 w-full flex justify-center">
              <AdSlot slot="5544234317" />
            </div>

            {/* Recommended articles */}
            {recommendedArticles.length > 0 && (
              <section className="mt-10">
                <h2 className="text-lg font-bold text-[#292929] mb-4 pb-2 border-b-2 border-[#292929]">
                  あなたへのおすすめ記事
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {recommendedArticles.slice(0, 4).map((rec: any) => (
                    <ArticleCard key={rec._id} article={rec} />
                  ))}
                </div>
              </section>
            )}
          </div>

          {/* Sidebar */}
          <div className="w-full lg:w-[30%]">
            <Sidebar />
          </div>
        </div>
        <ScrollDepthTracker slug={article.slug.current} />
      </article>
    </>
  )
}
