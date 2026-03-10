import { client, urlFor } from '@/lib/sanity'
import { sitemapWithImagesQuery, categoriesQuery, allArtistTagsQuery } from '@/lib/queries'
import type { MetadataRoute } from 'next'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.k-trendtimes.com'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [articles, categories, artistTags] = await Promise.all([
    client.fetch(sitemapWithImagesQuery),
    client.fetch(categoriesQuery),
    client.fetch(allArtistTagsQuery),
  ])

  const articleUrls = articles.map((article: any) => ({
    url: `${SITE_URL}/articles/${article.slug.current}`,
    lastModified: article._updatedAt || article.publishedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
    ...(article.mainImage ? {
      images: [urlFor(article.mainImage).width(1200).url()],
    } : {}),
  }))

  const categoryUrls = categories.map((cat: any) => ({
    url: `${SITE_URL}/category/${cat.slug.current}`,
    changeFrequency: 'daily' as const,
    priority: 0.6,
  }))

  const validArtistTags = (artistTags || []).filter((tag: string) => {
    return !/^admin$/i.test(tag) && !/^\d+$/.test(tag)
  })

  const artistTagUrls = validArtistTags.map((tag: string) => ({
    url: `${SITE_URL}/artist/${encodeURIComponent(tag)}`,
    changeFrequency: 'weekly' as const,
    priority: 0.5,
  }))

  return [
    {
      url: SITE_URL,
      changeFrequency: 'daily',
      priority: 1.0,
    },
    {
      url: `${SITE_URL}/privacy-policy`,
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${SITE_URL}/contact`,
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...categoryUrls,
    ...artistTagUrls,
    ...articleUrls,
  ]
}
