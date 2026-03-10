import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import Link from 'next/link'
import { client } from '@/lib/sanity'
import { articlesByTagQuery, tagBySlugQuery, tagArticlesCountQuery } from '@/lib/queries'
import ArticleCard from '@/components/ArticleCard'
import Sidebar from '@/components/Sidebar'

const SITE_NAME = 'K-TREND TIMES'
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.k-trendtimes.com'

export const revalidate = 60

type Props = {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const decodedSlug = decodeURIComponent(slug)
  const [tag, count] = await Promise.all([
    client.fetch(tagBySlugQuery, { tagSlug: decodedSlug }),
    client.fetch(tagArticlesCountQuery, { tagSlug: decodedSlug }),
  ])
  if (!tag) return {}
  const description = `「${tag.title}」タグの最新記事${count > 0 ? `${count}件` : ''}一覧。${tag.title}に関する韓国トレンド・エンタメニュースをお届けします。`
  const isJunkTag = /^admin$/i.test(decodedSlug) || /^\d+$/.test(decodedSlug)

  return {
    title: `${tag.title} | ${SITE_NAME}`,
    description,
    robots: isJunkTag ? { index: false, follow: false } : undefined,
    openGraph: {
      title: `${tag.title} | ${SITE_NAME}`,
      description,
      type: 'website',
      url: `${SITE_URL}/tag/${tag.slug.current}`,
      siteName: SITE_NAME,
    },
  }
}

export default async function TagPage({ params }: Props) {
  const { slug } = await params
  const decodedSlug = decodeURIComponent(slug)

  const [tag, articles] = await Promise.all([
    client.fetch(tagBySlugQuery, { tagSlug: decodedSlug }),
    client.fetch(articlesByTagQuery, { tagSlug: decodedSlug, limit: 20 }),
  ])

  if (!tag) notFound()

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Tag header */}
      <div className="mb-8">
        {/* Breadcrumb */}
        <nav aria-label="パンくずリスト" className="mb-4">
          <ol className="flex items-center gap-1 text-sm text-[#67737e]">
            <li>
              <Link href="/" className="hover:text-[#292929] transition-colors">
                ホーム
              </Link>
            </li>
            <li aria-hidden="true" className="mx-1">&gt;</li>
            <li className="font-bold text-[#292929]">{tag.title}</li>
          </ol>
        </nav>

        <div className="flex items-center gap-3 mb-2">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#292929" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z" />
            <line x1="7" y1="7" x2="7.01" y2="7" />
          </svg>
          <h1 className="text-2xl font-bold text-[#292929]">{tag.title}</h1>
        </div>
        <p className="text-sm text-[#67737e]">
          {articles.length}件の記事
        </p>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main content */}
        <div className="w-full lg:w-[70%]">
          {articles.length === 0 ? (
            <div className="text-center py-16">
              <p className="text-lg text-[#292929] font-medium mb-2">
                まだ記事がありません
              </p>
              <Link
                href="/"
                className="inline-block border border-[#292929] text-[#292929] hover:bg-[#292929] hover:text-white px-6 py-2 rounded transition-colors text-sm font-medium mt-4"
              >
                トップページに戻る
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {articles.map((article: any) => (
                <ArticleCard key={article._id} article={article} />
              ))}
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="w-full lg:w-[30%]">
          <Sidebar />
        </div>
      </div>
    </div>
  )
}
