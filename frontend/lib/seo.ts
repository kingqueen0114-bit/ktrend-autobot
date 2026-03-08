import type { Metadata } from 'next'
import { urlFor } from './sanity'

const SITE_NAME = 'K-TREND TIMES'
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://k-trendtimes.com'
const DEFAULT_OG_IMAGE = `${SITE_URL}/og-default.png`

export function generateArticleMetadata(article: {
  title: string
  seo?: { metaTitle?: string; metaDescription?: string; ogImage?: any }
  excerpt?: string
  mainImage?: any
  slug: { current: string }
  publishedAt?: string
  category?: { title: string }
}): Metadata {
  const title = article.seo?.metaTitle || article.title
  const description = article.seo?.metaDescription || article.excerpt || ''
  const ogImage = article.seo?.ogImage || article.mainImage
  const imageUrl = ogImage
    ? urlFor(ogImage).width(1200).height(630).url()
    : DEFAULT_OG_IMAGE

  const articleUrl = `${SITE_URL}/articles/${article.slug.current}`

  return {
    title,
    description,
    alternates: {
      canonical: articleUrl,
    },
    openGraph: {
      title,
      description,
      type: 'article',
      publishedTime: article.publishedAt,
      url: articleUrl,
      siteName: SITE_NAME,
      images: [{ url: imageUrl, width: 1200, height: 630 }],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: [imageUrl],
    },
  }
}

export function generateCategoryMetadata(category: {
  title: string
  description?: string
  slug: { current: string }
}): Metadata {
  return {
    title: category.title,
    description: category.description || `${category.title}の最新ニュース・トレンド情報`,
    openGraph: {
      title: `${category.title} | ${SITE_NAME}`,
      type: 'website',
      url: `${SITE_URL}/category/${category.slug.current}`,
      siteName: SITE_NAME,
    },
  }
}

export function articleJsonLd(article: {
  title: string
  excerpt?: string
  publishedAt?: string
  mainImage?: any
  slug: { current: string }
  category?: { title: string }
  author?: { name: string, slug?: { current: string } }
}) {
  const imageUrl = article.mainImage
    ? urlFor(article.mainImage).width(1200).height(630).url()
    : undefined

  const articleUrl = `${SITE_URL}/articles/${article.slug.current}`

  return {
    '@context': 'https://schema.org',
    '@type': 'NewsArticle',
    headline: article.title,
    description: article.excerpt || '',
    image: imageUrl ? [imageUrl] : [],
    datePublished: article.publishedAt,
    dateModified: article.publishedAt,
    url: articleUrl,
    author: article.author ? {
      '@type': 'Person',
      name: article.author.name,
      url: article.author.slug ? `${SITE_URL}/author/${article.author.slug.current}` : undefined
    } : {
      '@type': 'Organization',
      name: SITE_NAME,
      url: SITE_URL
    },
    publisher: {
      '@type': 'Organization',
      name: SITE_NAME,
      url: SITE_URL,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/favicon.png`
      }
    },
    articleSection: article.category?.title,
  }
}

