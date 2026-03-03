import {cache} from 'react'
import {notFound} from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'
import {draftMode} from 'next/headers'
import {client, getPreviewClient, urlFor} from '@/lib/sanity'
import {articleBySlugQuery, relatedArticlesQuery, adjacentArticlesQuery, recommendedArticlesQuery} from '@/lib/queries'
import {generateArticleMetadata, articleJsonLd} from '@/lib/seo'
import CategoryBadge from '@/components/CategoryBadge'
import ArticleCard from '@/components/ArticleCard'
import JsonLd from '@/components/JsonLd'
import Sidebar from '@/components/Sidebar'
import ArticleBody from '@/components/ArticleBody'

export const revalidate = 60

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://k-trendtimes.com'

type Props = {
  params: Promise<{slug: string}>
}

const getArticle = cache(async (slug: string, isPreview: boolean) => {
  const sanityClient = isPreview ? getPreviewClient() : client
  return sanityClient.fetch(articleBySlugQuery, {slug})
})

export async function generateMetadata({params}: Props) {
  const {slug} = await params
  const decodedSlug = decodeURIComponent(slug)
  const article = await getArticle(decodedSlug, false)
  if (!article) return {}
  return generateArticleMetadata(article)
}

function breadcrumbJsonLd(article: {title: string; slug: {current: string}; category?: {title: string; slug?: {current: string}}}) {
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

export default async function ArticlePage({params}: Props) {
  const {slug} = await params
  const decodedSlug = decodeURIComponent(slug)
  const {isEnabled: isPreview} = await draftMode()

  const article = await getArticle(decodedSlug, isPreview)

  if (!article) notFound()

  const relatedArticles = article.category?.slug?.current
    ? await client.fetch(relatedArticlesQuery, {
        categorySlug: article.category.slug.current,
        currentId: article._id,
      })
    : []

  const adjacentArticles = article.publishedAt
    ? await client.fetch(adjacentArticlesQuery, {
        publishedAt: article.publishedAt,
      })
    : {prev: null, next: null}

  const recommendedArticles = await client.fetch(recommendedArticlesQuery, {
    currentId: article._id,
  })

  const imageUrl = article.mainImage
    ? urlFor(article.mainImage).width(1200).height(630).url()
    : null

  const date = article.publishedAt
    ? new Date(article.publishedAt).toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : ''

  const articleUrl = `${SITE_URL}/articles/${article.slug.current}`
  const encodedUrl = encodeURIComponent(articleUrl)
  const encodedTitle = encodeURIComponent(article.title)

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
                  <Link href="/" className="hover:text-[#f84643] transition-colors">
                    ホーム
                  </Link>
                </li>
                {article.category?.slug?.current && (
                  <>
                    <li aria-hidden="true" className="mx-1">&gt;</li>
                    <li>
                      <Link
                        href={`/category/${article.category.slug.current}`}
                        className="hover:text-[#f84643] transition-colors"
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
            <div className="flex items-center gap-2 mb-6">
              {/* X (Twitter) */}
              <a
                href={`https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded text-white text-sm font-medium transition-opacity hover:opacity-80"
                style={{backgroundColor: '#000'}}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                </svg>
                <span>X</span>
              </a>

              {/* LINE */}
              <a
                href={`https://social-plugins.line.me/lineit/share?url=${encodedUrl}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded text-white text-sm font-medium transition-opacity hover:opacity-80"
                style={{backgroundColor: '#06C755'}}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .348-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .349-.281.63-.63.63h-2.386c-.345 0-.627-.281-.627-.63V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.63-.631.63-.346 0-.626-.286-.626-.63V8.108c0-.271.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.63-.631.63-.345 0-.627-.286-.627-.63V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.63H4.917c-.345 0-.63-.286-.63-.63V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .349-.281.63-.629.63M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314" />
                </svg>
                <span>LINE</span>
              </a>

              {/* Hatena Bookmark */}
              <a
                href={`https://b.hatena.ne.jp/entry/${articleUrl}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded text-white text-sm font-medium transition-opacity hover:opacity-80"
                style={{backgroundColor: '#00A4DE'}}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M20.47 0C22.42 0 24 1.58 24 3.53v16.94c0 1.95-1.58 3.53-3.53 3.53H3.53C1.58 24 0 22.42 0 20.47V3.53C0 1.58 1.58 0 3.53 0h16.94zm-3.705 14.47c-.78 0-1.41.63-1.41 1.41s.63 1.414 1.41 1.414 1.41-.634 1.41-1.414-.63-1.41-1.41-1.41zm.255-9.09h-2.1v8.82h2.1V5.38zm-5.016 5.67c-.72-.36-1.21-.96-1.21-1.89 0-1.8 1.41-2.55 3.03-2.55h3.45v8.82h-3.63c-1.74 0-3.18-.78-3.18-2.67 0-1.17.63-1.98 1.54-2.31v-.03zm1.83.63c-1.02 0-1.59.51-1.59 1.32 0 .78.51 1.26 1.53 1.26h1.38v-2.58h-1.32zm-.15-3.93c-.84 0-1.38.45-1.38 1.17 0 .69.48 1.17 1.38 1.17h1.17V7.75h-1.17z" />
                </svg>
                <span>はてブ</span>
              </a>
            </div>

            {/* Main image */}
            {imageUrl && (
              <figure className="mb-6">
                <div className="relative aspect-video overflow-hidden rounded-lg">
                  <Image
                    src={imageUrl}
                    alt={article.mainImage?.alt || article.title}
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 100vw, 70vw"
                    priority
                  />
                </div>
                {article.imageCredit && (
                  <figcaption className="text-xs text-[#67737e] mt-2">
                    出典: {article.imageCredit}
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

            {/* Artist Tags */}
            {article.artistTags && article.artistTags.length > 0 && (
              <div className="mt-6 flex items-center gap-2 flex-wrap">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f84643" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" className="shrink-0">
                  <path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z" />
                  <line x1="7" y1="7" x2="7.01" y2="7" />
                </svg>
                {article.artistTags.map((tag: string) => (
                  <Link
                    key={tag}
                    href={`/artist/${encodeURIComponent(tag)}`}
                    className="border border-[#f84643] text-[#f84643] text-xs font-medium px-3 py-1 rounded-full hover:bg-[#f84643] hover:text-white transition-colors"
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
                    className="group flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:border-[#f84643] transition-colors"
                  >
                    {adjacentArticles.prev.mainImage && (
                      <div className="relative w-16 h-16 shrink-0 rounded overflow-hidden">
                        <Image
                          src={urlFor(adjacentArticles.prev.mainImage).width(128).height(128).url()}
                          alt={adjacentArticles.prev.title}
                          fill
                          className="object-cover"
                          sizes="64px"
                        />
                      </div>
                    )}
                    <div className="min-w-0">
                      <span className="text-xs text-[#67737e] block mb-1">前の記事</span>
                      <span className="text-sm font-medium text-[#292929] group-hover:text-[#f84643] transition-colors line-clamp-2">
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
                    className="group flex items-center gap-3 p-4 border border-gray-200 rounded-lg hover:border-[#f84643] transition-colors md:flex-row-reverse md:text-right"
                  >
                    {adjacentArticles.next.mainImage && (
                      <div className="relative w-16 h-16 shrink-0 rounded overflow-hidden">
                        <Image
                          src={urlFor(adjacentArticles.next.mainImage).width(128).height(128).url()}
                          alt={adjacentArticles.next.title}
                          fill
                          className="object-cover"
                          sizes="64px"
                        />
                      </div>
                    )}
                    <div className="min-w-0">
                      <span className="text-xs text-[#67737e] block mb-1">次の記事</span>
                      <span className="text-sm font-medium text-[#292929] group-hover:text-[#f84643] transition-colors line-clamp-2">
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
                <h2 className="text-lg font-bold text-[#292929] mb-4 pb-2 border-b-2 border-[#f84643]">
                  関連記事
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {relatedArticles.map((related: any) => (
                    <ArticleCard key={related._id} article={related} />
                  ))}
                </div>
              </section>
            )}

            {/* Recommended articles */}
            {recommendedArticles.length > 0 && (
              <section className="mt-10">
                <h2 className="text-lg font-bold text-[#292929] mb-4 pb-2 border-b-2 border-[#f84643]">
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
      </article>
    </>
  )
}
