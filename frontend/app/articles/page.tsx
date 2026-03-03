import type {Metadata} from 'next'
import Link from 'next/link'
import {client} from '@/lib/sanity'
import {articlesPaginatedQuery, articlesCountQuery} from '@/lib/queries'
import ArticleCard from '@/components/ArticleCard'
import Sidebar from '@/components/Sidebar'

const SITE_NAME = 'K-TREND TIMES'
const PER_PAGE = 12

export const revalidate = 60

type Props = {
  searchParams: Promise<{page?: string}>
}

export async function generateMetadata({searchParams}: Props): Promise<Metadata> {
  const {page} = await searchParams
  const pageNum = parseInt(page || '1', 10)
  const title = pageNum > 1
    ? `記事一覧 (${pageNum}ページ目) | ${SITE_NAME}`
    : `記事一覧 | ${SITE_NAME}`
  return {
    title,
    description: '韓国トレンド・K-POP・ビューティー・ファッションの最新記事一覧',
  }
}

export default async function ArticlesPage({searchParams}: Props) {
  const {page} = await searchParams
  const currentPage = Math.max(1, parseInt(page || '1', 10))
  const start = (currentPage - 1) * PER_PAGE
  const end = start + PER_PAGE

  const [articles, totalCount] = await Promise.all([
    client.fetch(articlesPaginatedQuery, {start, end}),
    client.fetch(articlesCountQuery),
  ])

  const totalPages = Math.ceil(totalCount / PER_PAGE)

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <nav aria-label="パンくずリスト" className="mb-4">
        <ol className="flex items-center gap-1 text-sm text-[#67737e]">
          <li>
            <Link href="/" className="hover:text-[#f84643] transition-colors">
              ホーム
            </Link>
          </li>
          <li aria-hidden="true" className="mx-1">&gt;</li>
          <li className="font-bold text-[#292929]">記事一覧</li>
        </ol>
      </nav>

      {/* Page heading */}
      <h1 className="border-l-4 border-[#f84643] pl-3 text-2xl font-bold text-[#292929] mb-2">
        記事一覧
      </h1>
      <p className="text-sm text-[#67737e] mb-8">
        全{totalCount}件の記事
        {totalPages > 1 && ` (${currentPage} / ${totalPages}ページ)`}
      </p>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main content */}
        <div className="w-full lg:w-[70%]">
          {articles.length === 0 ? (
            <p className="text-[#67737e] text-center py-12">記事がありません</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {articles.map((article: any) => (
                <ArticleCard key={article._id} article={article} />
              ))}
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <nav className="flex justify-center items-center gap-2 mt-10" aria-label="ページネーション">
              {/* Previous button */}
              {currentPage > 1 ? (
                <Link
                  href={`/articles?page=${currentPage - 1}`}
                  className="px-4 py-2 border border-gray-300 rounded text-sm text-[#292929] hover:border-[#f84643] hover:text-[#f84643] transition-colors"
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
                    href={`/articles?page=${num}`}
                    className={`w-10 h-10 flex items-center justify-center rounded text-sm font-medium transition-colors ${
                      num === currentPage
                        ? 'bg-[#f84643] text-white'
                        : 'border border-gray-300 text-[#292929] hover:border-[#f84643] hover:text-[#f84643]'
                    }`}
                  >
                    {num}
                  </Link>
                )
              })}

              {/* Next button */}
              {currentPage < totalPages ? (
                <Link
                  href={`/articles?page=${currentPage + 1}`}
                  className="px-4 py-2 border border-gray-300 rounded text-sm text-[#292929] hover:border-[#f84643] hover:text-[#f84643] transition-colors"
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
  )
}

// Helper function to generate page numbers with ellipsis
function generatePageNumbers(current: number, total: number): (number | '...')[] {
  if (total <= 7) {
    return Array.from({length: total}, (_, i) => i + 1)
  }

  const pages: (number | '...')[] = []

  // Always show first page
  pages.push(1)

  if (current > 3) {
    pages.push('...')
  }

  // Pages around current
  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)
  for (let i = start; i <= end; i++) {
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
