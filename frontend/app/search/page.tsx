import {Metadata} from 'next'
import Link from 'next/link'
import {client} from '@/lib/sanity'
import {searchQuery, searchCountQuery} from '@/lib/queries'
import ArticleCard from '@/components/ArticleCard'
import Sidebar from '@/components/Sidebar'
import SearchForm from '@/components/SearchForm'

const SITE_NAME = 'K-TREND TIMES'

type Props = {
  searchParams: Promise<{q?: string}>
}

export async function generateMetadata({searchParams}: Props): Promise<Metadata> {
  const {q} = await searchParams
  const query = q || ''
  return {
    title: query ? `「${query}」の検索結果 | ${SITE_NAME}` : `検索 | ${SITE_NAME}`,
    robots: {index: false},
  }
}

export default async function SearchPage({searchParams}: Props) {
  const {q} = await searchParams
  const query = q?.trim() || ''

  let articles: any[] = []
  let totalCount = 0

  if (query) {
    [articles, totalCount] = await Promise.all([
      client.fetch(searchQuery, {q: query, limit: 20}),
      client.fetch(searchCountQuery, {q: query}),
    ])
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main content */}
        <div className="w-full lg:w-[70%]">
          {/* Search heading */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-[#292929] mb-2">
              {query ? (
                <>「<span className="text-[#292929]">{query}</span>」の検索結果</>
              ) : (
                '記事を検索'
              )}
            </h1>
            {query && (
              <p className="text-sm text-[#67737e]">
                {totalCount}件の記事が見つかりました
              </p>
            )}
          </div>

          {/* Search form */}
          <SearchForm defaultQuery={query} />

          {/* Results */}
          {query && articles.length === 0 ? (
            <div className="text-center py-16">
              <div className="text-6xl mb-4">🔍</div>
              <p className="text-lg text-[#292929] font-medium mb-2">
                記事が見つかりませんでした
              </p>
              <p className="text-sm text-[#67737e] mb-6">
                別のキーワードで検索してみてください
              </p>
              <Link
                href="/"
                className="inline-block border border-[#292929] text-[#292929] hover:bg-[#292929] hover:text-white px-6 py-2 rounded transition-colors text-sm font-medium"
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

          {!query && (
            <div className="text-center py-16">
              <div className="text-6xl mb-4">🔍</div>
              <p className="text-lg text-[#292929] font-medium">
                キーワードを入力して記事を検索
              </p>
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
