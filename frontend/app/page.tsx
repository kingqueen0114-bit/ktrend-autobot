import Link from 'next/link'
import Image from 'next/image'
import { client, urlFor } from '@/lib/sanity'
import { articlesQuery } from '@/lib/queries'
import ArticleCard from '@/components/ArticleCard'
import AdSlot from '@/components/AdSlot'
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
  const articles = await client.fetch(articlesQuery, { limit: 30 })

  return (
    <>
      <JsonLd data={organizationJsonLd} />
      <JsonLd data={webSiteJsonLd} />
      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Main content */}
          <div className="w-full lg:w-[70%]">
            {articles.length === 0 ? (
              <p className="text-[#67737e] text-center py-12">まだ記事がありません</p>
            ) : (
              <>
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
                        {articles[0].category && (
                          <span
                            className="text-xs text-white font-medium px-2 py-0.5 rounded-full inline-block mb-2"
                            style={{ backgroundColor: articles[0].category.color }}
                          >
                            {articles[0].category.title}
                          </span>
                        )}
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

                {/* Section heading */}
                <h2 className="border-l-4 border-[#292929] pl-3 text-lg font-bold text-[#292929] mb-4">
                  最新記事
                </h2>

                {/* Remaining articles: list style (same as category page) */}
                <div className="divide-y divide-gray-100">
                  {articles.map((article: any, index: number) => (
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

                {/* Load more button */}
                <div className="flex justify-center mt-10">
                  <Link
                    href="/articles"
                    className="border border-[#292929] text-[#292929] hover:bg-[#292929] hover:text-white px-8 py-2.5 rounded transition-colors text-sm font-medium"
                  >
                    もっと読む
                  </Link>
                </div>
              </>
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
