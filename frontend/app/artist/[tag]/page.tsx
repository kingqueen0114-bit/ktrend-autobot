import { notFound } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { client, urlFor } from '@/lib/sanity'
import { articlesByArtistTagQuery, artistTagArticlesCountQuery } from '@/lib/queries'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://k-trendtimes.com'
import Sidebar from '@/components/Sidebar'
import type { Metadata } from 'next'

export const revalidate = 60

const SITE_NAME = 'K-TREND TIMES'

type Props = {
  params: Promise<{ tag: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { tag } = await params
  const decodedTag = decodeURIComponent(tag)
  const count = await client.fetch(artistTagArticlesCountQuery, { artistTag: decodedTag })
  const description = `「${decodedTag}」の最新ニュース${count > 0 ? `・記事${count}件` : ''}。${decodedTag}に関する韓国エンタメ・K-POPトレンド情報をお届けします。`
  return {
    title: `${decodedTag}の記事一覧 | ${SITE_NAME}`,
    description,
    openGraph: {
      title: `${decodedTag}の記事一覧 | ${SITE_NAME}`,
      description,
      type: 'website',
      url: `${SITE_URL}/artist/${encodeURIComponent(decodedTag)}`,
      siteName: SITE_NAME,
    },
  }
}

export default async function ArtistTagPage({ params }: Props) {
  const { tag } = await params
  const decodedTag = decodeURIComponent(tag)

  const [articles, totalCount] = await Promise.all([
    client.fetch(articlesByArtistTagQuery, { artistTag: decodedTag, limit: 30 }),
    client.fetch(artistTagArticlesCountQuery, { artistTag: decodedTag }),
  ])

  if (totalCount === 0) notFound()

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <nav aria-label="パンくずリスト" className="mb-6">
        <ol className="flex items-center gap-1 text-sm text-[#67737e]">
          <li>
            <Link href="/" className="hover:text-[#292929] transition-colors">
              ホーム
            </Link>
          </li>
          <li aria-hidden="true" className="mx-1">&gt;</li>
          <li className="font-bold text-[#292929]">{decodedTag}</li>
        </ol>
      </nav>

      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#292929" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z" />
            <line x1="7" y1="7" x2="7.01" y2="7" />
          </svg>
          <h1 className="text-2xl font-bold text-[#292929]">{decodedTag}</h1>
          <span className="text-sm text-[#67737e]">({totalCount}件)</span>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main content */}
        <div className="w-full lg:w-[70%]">
          {/* Hero: Latest article */}
          {articles[0] && (
            <Link href={`/articles/${articles[0].slug.current}`} className="block group mb-6">
              <div className="relative aspect-square md:aspect-[16/9] overflow-hidden rounded-lg">
                {articles[0].mainImage ? (
                  <Image
                    src={urlFor(articles[0].mainImage).width(800).height(450).url()}
                    alt={articles[0].title}
                    fill
                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                    sizes="(max-width: 768px) 100vw, 70vw"
                    priority
                  />
                ) : (
                  <div className="absolute inset-0 bg-gray-200" />
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                <div className="absolute bottom-0 left-0 right-0 p-5">
                  <h2 className="text-white text-xl md:text-2xl font-bold leading-tight line-clamp-3 group-hover:underline">
                    {articles[0].title}
                  </h2>
                  {articles[0].excerpt && (
                    <p className="text-white/80 text-sm mt-2 line-clamp-2">{articles[0].excerpt}</p>
                  )}
                  <time className="text-white/60 text-xs mt-2 block">
                    {articles[0].publishedAt
                      ? new Date(articles[0].publishedAt).toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' })
                      : ''}
                  </time>
                </div>
              </div>
            </Link>
          )}

          {/* Remaining articles: list style */}
          <div className="divide-y divide-gray-100">
            {articles.slice(1).map((article: any) => (
              <Link
                key={article._id}
                href={`/articles/${article.slug.current}`}
                className="flex gap-4 py-4 group"
              >
                <div className="relative w-[100px] md:w-[120px] aspect-square flex-shrink-0 overflow-hidden rounded-lg">
                  {article.mainImage ? (
                    <Image
                      src={urlFor(article.mainImage).width(320).height(200).url()}
                      alt={article.title}
                      fill
                      className="object-cover group-hover:scale-105 transition-transform duration-300"
                      sizes="160px"
                    />
                  ) : (
                    <div className="absolute inset-0 bg-gray-200 rounded-lg" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-bold text-[#292929] line-clamp-2 group-hover:text-[#292929] transition-colors">
                    {article.title}
                  </h3>
                  {article.excerpt && (
                    <p className="text-sm text-[#67737e] mt-1 line-clamp-2 hidden md:block">{article.excerpt}</p>
                  )}
                  <div className="flex items-center gap-2 mt-2 flex-wrap">
                    {article.category && (
                      <span
                        className="text-xs text-white font-medium px-2 py-0.5 rounded-full"
                        style={{ backgroundColor: article.category.color }}
                      >
                        {article.category.title}
                      </span>
                    )}
                    <time className="text-xs text-[#67737e]">
                      {article.publishedAt
                        ? new Date(article.publishedAt).toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' })
                        : ''}
                    </time>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-full lg:w-[30%]">
          <Sidebar />
        </div>
      </div>
    </div>
  )
}
