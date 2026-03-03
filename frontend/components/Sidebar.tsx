import Link from 'next/link'
import {client} from '@/lib/sanity'
import {articlesQuery, allArtistTagsQuery} from '@/lib/queries'
import ArticleCard from './ArticleCard'
import AdSlot from '@/components/AdSlot'

export default async function Sidebar() {
  const [popularArticles, artistTags] = await Promise.all([
    client.fetch(articlesQuery, {limit: 5}),
    client.fetch(allArtistTagsQuery),
  ])

  return (
    <aside className="space-y-8">
      {/* Popular articles */}
      <div>
        <h3 className="text-base font-bold text-[#292929] mb-4 pb-2 border-b-2 border-[#f84643]">
          人気の記事
        </h3>
        <div className="space-y-4">
          {popularArticles.map((article: any, i: number) => (
            <ArticleCard key={article._id} article={article} variant="sidebar" rank={i + 1} />
          ))}
        </div>
      </div>

      {/* Artist Tags */}
      {artistTags && artistTags.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-5">
          <h3 className="text-lg font-bold text-[#292929] mb-1">アーティストタグ</h3>
          <div className="w-full h-0.5 bg-[#f84643] mb-4" />
          <div className="flex flex-wrap gap-2">
            {(artistTags as string[]).map((tag: string) => (
              <Link
                key={tag}
                href={`/artist/${encodeURIComponent(tag)}`}
                className="inline-flex items-center gap-1.5 border border-[#f84643] text-[#f84643] text-sm font-medium px-3 py-1.5 rounded-full hover:bg-[#f84643] hover:text-white transition-colors"
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="shrink-0">
                  <path d="M20.59 13.41l-7.17 7.17a2 2 0 01-2.83 0L2 12V2h10l8.59 8.59a2 2 0 010 2.82z" />
                  <line x1="7" y1="7" x2="7.01" y2="7" />
                </svg>
                {tag}
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Ad slot */}
      <AdSlot slot="sidebar" style={{minHeight: 600}} />
    </aside>
  )
}
