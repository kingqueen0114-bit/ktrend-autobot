import Link from 'next/link'
import Image from 'next/image'
import { client, urlFor } from '@/lib/sanity'
import { articlesQuery } from '@/lib/queries'
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
                          {article.artistTags && article.artistTags.length > 0 && article.artistTags.slice(0, 3).map((tag: string) => (
                            <span key={tag} className="border border-[#292929]/50 text-[#292929] text-[10px] px-2 py-0.5 rounded-full">
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                    </Link>
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
