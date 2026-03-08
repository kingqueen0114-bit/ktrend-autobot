import { notFound } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import { client, urlFor } from '@/lib/sanity'
import { articlesByCategoryQuery, categoriesQuery } from '@/lib/queries'
import ArticleCard from '@/components/ArticleCard'
import AdSlot from '@/components/AdSlot'
import { generateCategoryMetadata } from '@/lib/seo'
import Sidebar from '@/components/Sidebar'

export const revalidate = 60

type Props = {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params
  const decodedSlug = decodeURIComponent(slug)
  const categories = await client.fetch(categoriesQuery)
  const category = categories.find((c: any) => c.slug.current === decodedSlug)
  if (!category) return {}
  return generateCategoryMetadata(category)
}

export default async function CategoryPage({ params }: Props) {
  const { slug } = await params
  const decodedSlug = decodeURIComponent(slug)
  const [articles, categories] = await Promise.all([
    client.fetch(articlesByCategoryQuery, { categorySlug: decodedSlug, limit: 20 }),
    client.fetch(categoriesQuery),
  ])

  const category = categories.find((c: any) => c.slug.current === decodedSlug)
  if (!category) notFound()

  return (
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
                {articles.slice(1).map((article: any, index: number) => (
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
        </div>

        {/* Sidebar */}
        <div className="w-full lg:w-[30%]">
          <Sidebar />
        </div>
      </div>
    </div>
  )
}
