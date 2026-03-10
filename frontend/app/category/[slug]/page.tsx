import { notFound } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { client, optimizedUrl } from '@/lib/sanity'
import { articlesByCategoryPaginatedQuery, articlesByCategoryCountQuery, categoriesQuery } from '@/lib/queries'
import ArticleCard from '@/components/ArticleCard'
import AdSlot from '@/components/AdSlot'
import { generateCategoryMetadata } from '@/lib/seo'
import Sidebar from '@/components/Sidebar'
import JsonLd from '@/components/JsonLd'

const PER_PAGE = 12
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://k-trendtimes.com'

export const revalidate = 60

type Props = {
  params: Promise<{ slug: string }>
  searchParams: Promise<{ page?: string }>
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params
  const decodedSlug = decodeURIComponent(slug)
  const categories = await client.fetch(categoriesQuery)
  const category = categories.find((c: any) => c.slug.current === decodedSlug)
  if (!category) return {}
  return generateCategoryMetadata(category)
}

export default async function CategoryPage({ params, searchParams }: Props) {
  const { slug } = await params
  const { page } = await searchParams
  const decodedSlug = decodeURIComponent(slug)
  const currentPage = Math.max(1, parseInt(page || '1', 10))
  const start = (currentPage - 1) * PER_PAGE
  const end = start + PER_PAGE

  const [articles, totalCount, categories] = await Promise.all([
    client.fetch(articlesByCategoryPaginatedQuery, { categorySlug: decodedSlug, start, end }),
    client.fetch(articlesByCategoryCountQuery, { categorySlug: decodedSlug }),
    client.fetch(categoriesQuery),
  ])

  const category = categories.find((c: any) => c.slug.current === decodedSlug)
  if (!category) notFound()

  const totalPages = Math.ceil(totalCount / PER_PAGE)
  const isFirstPage = currentPage === 1

  return (
    <>
      <JsonLd data={{
        '@context': 'https://schema.org',
        '@type': 'CollectionPage',
        name: `${category.title} | K-TREND TIMES`,
        url: `${SITE_URL}/category/${decodedSlug}`,
        description: category.description || `${category.title}の最新ニュース・トレンド情報`,
        isPartOf: { '@type': 'WebSite', name: 'K-TREND TIMES', url: SITE_URL },
        mainEntity: {
          '@type': 'ItemList',
          numberOfItems: totalCount,
          itemListElement: articles.map((a: any, i: number) => ({
            '@type': 'ListItem',
            position: (currentPage - 1) * PER_PAGE + i + 1,
            url: `${SITE_URL}/articles/${a.slug.current}`,
            name: a.title,
          })),
        },
      }} />
      <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Page heading with article count */}
      <p className="text-sm text-[#67737e] mb-6">
        全{totalCount}件の記事
        {totalPages > 1 && ` (${currentPage} / ${totalPages}ページ)`}
      </p>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main content */}
        <div className="w-full lg:w-[70%]">
          {articles.length === 0 ? (
            <p className="text-[#67737e] text-center py-12">まだ記事がありません</p>
          ) : (
            <>
              {/* Hero: Latest article (1ページ目のみ) */}
              {isFirstPage && articles[0] && (
                <Link href={`/articles/${articles[0].slug.current}`} className="block group mb-6">
                  <div className="relative aspect-square md:aspect-[16/9] overflow-hidden rounded-lg">
                    {articles[0].mainImage ? (
                      <Image
                        src={optimizedUrl(articles[0].mainImage).width(800).height(450).url()}
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

              {/* Article list */}
              <div className="divide-y divide-gray-100">
                {(isFirstPage ? articles.slice(1) : articles).map((article: any, index: number) => (
                  <div key={article._id}>
                    <div>
                      <ArticleCard article={article} variant="list" />
                    </div>

                    {/* Inject In-Feed Ad Every 5 Articles */}
                    {(index + 1) % 5 === 0 && (
                      <div className="border-b border-[#292929]/10 w-full flex justify-center items-center">
                        <AdSlot slot="5161090936" format="fluid" data-ad-layout-key="-fb+5w+4e-db+86" className="!py-0" />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <nav className="flex justify-center items-center gap-2 mt-10" aria-label="ページネーション">
              {/* Previous button */}
              {currentPage > 1 ? (
                <Link
                  href={`/category/${slug}?page=${currentPage - 1}`}
                  className="px-4 py-2 border border-gray-300 rounded text-sm text-[#292929] hover:border-[#292929] hover:text-[#292929] transition-colors"
                >
                  ← 前へ
                </Link>
              ) : (
                <span className="px-4 py-2 border border-gray-200 rounded text-sm text-gray-400 cursor-not-allowed">
                  ← 前へ
                </span>
              )}

              {/* Page numbers */}
              {generatePageNumbers(currentPage, totalPages).map((pageNum, i) => {
                if (pageNum === '...') {
                  return (
                    <span key={`ellipsis-${i}`} className="px-2 py-2 text-sm text-[#67737e]">
                      ...
                    </span>
                  )
                }
                const num = pageNum as number
                return (
                  <Link
                    key={num}
                    href={`/category/${slug}?page=${num}`}
                    className={`w-10 h-10 flex items-center justify-center rounded text-sm font-medium transition-colors ${num === currentPage
                      ? 'bg-[#292929] text-white'
                      : 'border border-gray-300 text-[#292929] hover:border-[#292929] hover:text-[#292929]'
                      }`}
                  >
                    {num}
                  </Link>
                )
              })}

              {/* Next button */}
              {currentPage < totalPages ? (
                <Link
                  href={`/category/${slug}?page=${currentPage + 1}`}
                  className="px-4 py-2 border border-gray-300 rounded text-sm text-[#292929] hover:border-[#292929] hover:text-[#292929] transition-colors"
                >
                  次へ →
                </Link>
              ) : (
                <span className="px-4 py-2 border border-gray-200 rounded text-sm text-gray-400 cursor-not-allowed">
                  次へ →
                </span>
              )}
            </nav>
          )}
        </div>

        {/* Sidebar */}
        <div className="w-full lg:w-[30%]">
          <Sidebar />
        </div>
      </div>
    </div>
    </>
  )
}

// Helper function to generate page numbers with ellipsis
function generatePageNumbers(current: number, total: number): (number | '...')[] {
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  const pages: (number | '...')[] = []

  // Always show first page
  pages.push(1)

  if (current > 3) {
    pages.push('...')
  }

  // Pages around current
  const rangeStart = Math.max(2, current - 1)
  const rangeEnd = Math.min(total - 1, current + 1)
  for (let i = rangeStart; i <= rangeEnd; i++) {
    pages.push(i)
  }

  if (current < total - 2) {
    pages.push('...')
  }

  // Always show last page
  if (total > 1) {
    pages.push(total)
  }

  return pages
}
