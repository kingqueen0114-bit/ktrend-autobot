import type {MetadataRoute} from 'next'

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.k-trendtimes.com'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/studio/', '/edit/', '/drafts/'],
      },
      {
        userAgent: 'Googlebot-News',
        allow: '/articles/',
        disallow: ['/api/', '/studio/', '/edit/', '/drafts/', '/artist/', '/search/'],
      },
    ],
    sitemap: [`${SITE_URL}/sitemap.xml`, `${SITE_URL}/news-sitemap.xml`],
  }
}
