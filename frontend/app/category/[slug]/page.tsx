import {notFound} from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'
import {client, urlFor} from '@/lib/sanity'
import {articlesByCategoryQuery, categoriesQuery} from '@/lib/queries'
import {generateCategoryMetadata} from '@/lib/seo'
import Sidebar from '@/components/Sidebar'

export const revalidate = 60

type Props = {
  params: Promise<{slug: string}>
}

export async function generateMetadata({params}: Props) {
  const {slug} = await params
  const decodedSlug = decodeURIComponent(slug)
  const categories = await client.fetch(categoriesQuery)
  const category = categories.find((c: any) => c.slug.current === decodedSlug)
  if (!category) return {}
  return generateCategoryMetadata(category)
}

export default async function CategoryPage({params}: Props) {
  const {slug} = await params
  const decodedSlug = decodeURIComponent(slug)
  const [articles, categories] = await Promise.all([
    client.fetch(articlesByCategoryQuery, {categorySlug: decodedSlug, limit: 20}),
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
                  <div className="relative aspect-[16/9] overflow-hidden rounded-lg">
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
                          ? new Date(articles[0].publishedAt).toLocaleDateString('ja-JP', {year: 'numeric', month: 'long', day: 'numeric'})
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
                    <div className="relative w-[120px] h-[80px] md:w-[160px] md:h-[100px] flex-shrink-0 overflow-hidden rounded-lg">
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
                      <h3 className="text-base font-bold text-[#292929] line-clamp-2 group-hover:text-[#f84643] transition-colors">
                        {article.title}
                      </h3>
                      {article.excerpt && (
                        <p className="text-sm text-[#67737e] mt-1 line-clamp-2 hidden md:block">{article.excerpt}</p>
                      )}
                      <div className="flex items-center gap-2 mt-2 flex-wrap">
                        {article.category && (
                          <span
                            className="text-xs text-white font-medium px-2 py-0.5 rounded-full"
                            style={{backgroundColor: article.category.color}}
                          >
                            {article.category.title}
                          </span>
                        )}
                        <time className="text-xs text-[#67737e]">
                          {article.publishedAt
                            ? new Date(article.publishedAt).toLocaleDateString('ja-JP', {year: 'numeric', month: 'long', day: 'numeric'})
                            : ''}
                        </time>
                        {article.artistTags && article.artistTags.length > 0 && article.artistTags.slice(0, 3).map((tag: string) => (
                          <span key={tag} className="border border-[#f84643]/50 text-[#f84643] text-[10px] px-2 py-0.5 rounded-full">
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </Link>
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
