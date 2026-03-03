import {client} from '@/lib/sanity'
import {sitemapQuery, categoriesQuery} from '@/lib/queries'
import type {MetadataRoute} from 'next'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://k-trendtimes.com'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [articles, categories] = await Promise.all([
    client.fetch(sitemapQuery),
    client.fetch(categoriesQuery),
  ])

  const articleUrls = articles.map((article: any) => ({
    url: `${SITE_URL}/articles/${article.slug.current}`,
    lastModified: article._updatedAt || article.publishedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))

  const categoryUrls = categories.map((cat: any) => ({
    url: `${SITE_URL}/category/${cat.slug.current}`,
    changeFrequency: 'daily' as const,
    priority: 0.6,
  }))

  return [
    {
      url: SITE_URL,
      changeFrequency: 'daily',
      priority: 1.0,
    },
    ...categoryUrls,
    ...articleUrls,
  ]
}
