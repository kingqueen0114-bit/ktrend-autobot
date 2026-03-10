import type { Metadata } from 'next'
import { optimizedUrl } from './sanity'

const SITE_NAME = 'K-TREND TIMES'
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.k-trendtimes.com'
const DEFAULT_OG_IMAGE = `${SITE_URL}/og-default.png`

export function generateArticleMetadata(article: {
  title: string
  seo?: { metaTitle?: string; metaDescription?: string; ogImage?: any }
  excerpt?: string
  mainImage?: any
  slug: { current: string }
  publishedAt?: string
  _updatedAt?: string
  category?: { title: string }
}): Metadata {
  const title = article.seo?.metaTitle || article.title
  const description = article.seo?.metaDescription || article.excerpt || ''
  const ogImage = article.seo?.ogImage || article.mainImage
  const imageUrl = ogImage
    ? optimizedUrl(ogImage).width(1200).height(630).url()
    : null

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
      modifiedTime: article._updatedAt || article.publishedAt,
      url: articleUrl,
      siteName: SITE_NAME,
      ...(imageUrl ? { images: [{ url: imageUrl, width: 1200, height: 630 }] } : {}),
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      ...(imageUrl ? { images: [imageUrl] } : {}),
    },
    robots: {
      index: true,
      follow: true,
      'max-image-preview': 'large' as const,
      'max-snippet': -1,
      'max-video-preview': -1,
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
  _updatedAt?: string
  mainImage?: any
  slug: { current: string }
  category?: { title: string }
  author?: { name: string, slug?: { current: string } }
}) {
  const imageUrl = article.mainImage
    ? optimizedUrl(article.mainImage).width(1200).height(630).url()
    : undefined

  const articleUrl = `${SITE_URL}/articles/${article.slug.current}`

  return {
    '@context': 'https://schema.org',
    '@type': 'NewsArticle',
    headline: article.title,
    description: article.excerpt || '',
    image: imageUrl ? [imageUrl] : [],
    datePublished: article.publishedAt,
    dateModified: article._updatedAt || article.publishedAt,
    url: articleUrl,
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': articleUrl,
    },
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
      '@type': 'NewsMediaOrganization',
      name: SITE_NAME,
      url: SITE_URL,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/og-default.png`,
        width: 600,
        height: 60,
      }
    },
    articleSection: article.category?.title,
  }
}

