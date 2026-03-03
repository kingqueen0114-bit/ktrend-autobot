import Link from 'next/link'
import Image from 'next/image'
import {client, urlFor} from '@/lib/sanity'
import {articlesQuery} from '@/lib/queries'
import ArticleCard from '@/components/ArticleCard'
import Sidebar from '@/components/Sidebar'
import JsonLd from '@/components/JsonLd'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://k-trendtimes.com'

const organizationJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'K-TREND TIMES',
  url: SITE_URL,
  logo: `${SITE_URL}/og-default.png`,
}

const webSiteJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'K-TREND TIMES',
  url: SITE_URL,
  potentialAction: {
    '@type': 'SearchAction',
    target: `${SITE_URL}/search?q={search_term_string}`,
    'query-input': 'required name=search_term_string',
  },
}

export const revalidate = 60

export default async function HomePage() {
  const articles = await client.fetch(articlesQuery, {limit: 12})

  const featured = articles[0]
  const sub1 = articles[1]
  const sub2 = articles[2]
  const rest = articles.slice(3)

  return (
    <>
      <JsonLd data={organizationJsonLd} />
      <JsonLd data={webSiteJsonLd} />
      <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main content */}
        <div className="w-full lg:w-[70%]">
          {/* Hero section: featured + sub articles */}
          <div className="flex flex-col lg:flex-row gap-6 mb-8">
            {/* Featured article */}
            {featured && (
              <div className="w-full lg:w-[60%]">
                {/* Mobile: overlay style */}
                <Link href={`/articles/${featured.slug.current}`} className="block lg:hidden relative aspect-[4/3] overflow-hidden rounded-lg">
                  {featured.mainImage ? (
                    <Image
                      src={urlFor(featured.mainImage).width(800).height(600).url()}
                      alt={featured.title}
                      fill
                      className="object-cover"
                      sizes="100vw"
                      priority
                    />
                  ) : (
                    <div className="absolute inset-0 bg-gray-200" />
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                  {featured.category && (
                    <span
                      className="absolute top-3 left-3 text-xs text-white font-medium px-2 py-0.5 rounded"
                      style={{backgroundColor: featured.category.color}}
                    >
                      {featured.category.title}
                    </span>
                  )}
                  <div className="absolute bottom-0 left-0 right-0 p-4">
                    <h2 className="text-white text-lg font-bold leading-tight line-clamp-3">
                      {featured.title}
                    </h2>
                    <time className="text-white/70 text-xs mt-1 block">
                      {featured.publishedAt
                        ? new Date(featured.publishedAt).toLocaleDateString('ja-JP', {month: 'long', day: 'numeric'})
                        : ''}
                    </time>
                  </div>
                </Link>
                {/* Desktop: existing card */}
                <div className="hidden lg:block">
                  <ArticleCard article={featured} variant="featured" />
                </div>
              </div>
            )}

            {/* Sub articles */}
            {(sub1 || sub2) && (
              <div className="w-full lg:w-[40%]">
                {/* Mobile: list style */}
                <div className="lg:hidden space-y-3">
                  {[sub1, sub2].filter(Boolean).map((a: any) => (
                    <Link key={a._id} href={`/articles/${a.slug.current}`} className="flex gap-3 group">
                      <div className="relative w-[120px] h-[80px] shrink-0 overflow-hidden rounded">
                        {a.mainImage ? (
                          <Image
                            src={urlFor(a.mainImage).width(240).height(160).url()}
                            alt={a.title}
                            fill
                            className="object-cover group-hover:scale-105 transition-transform"
                            sizes="120px"
                          />
                        ) : (
                          <div className="absolute inset-0 bg-gray-200 rounded" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className="text-sm font-medium text-[#292929] line-clamp-2 group-hover:text-[#f84643] transition-colors">
                          {a.title}
                        </h3>
                        <time className="text-xs text-[#67737e] mt-1 block">
                          {a.publishedAt
                            ? new Date(a.publishedAt).toLocaleDateString('ja-JP', {month: 'long', day: 'numeric'})
                            : ''}
                        </time>
                      </div>
                    </Link>
                  ))}
                </div>
                {/* Desktop: existing cards */}
                <div className="hidden lg:flex flex-col gap-6">
                  {sub1 && <ArticleCard article={sub1} />}
                  {sub2 && <ArticleCard article={sub2} />}
                </div>
              </div>
            )}
          </div>

          {/* Section heading */}
          <h2 className="border-l-4 border-[#f84643] pl-3 text-lg font-bold text-[#292929] mb-6">
            最新記事
          </h2>

          {/* Article grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {rest.map((article: any) => (
              <ArticleCard key={article._id} article={article} />
            ))}
          </div>

          {/* Load more button */}
          <div className="flex justify-center mt-10">
            <Link
              href="/articles"
              className="border border-[#f84643] text-[#f84643] hover:bg-[#f84643] hover:text-white px-8 py-2.5 rounded transition-colors text-sm font-medium"
            >
              もっと読む
            </Link>
          </div>
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
