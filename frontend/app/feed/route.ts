import { client, optimizedUrl } from '@/lib/sanity'
import { rssFeedQuery } from '@/lib/queries'

export const revalidate = 3600

function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}

export async function GET() {
  const articles = await client.fetch(rssFeedQuery)
  const siteUrl = 'https://www.k-trendtimes.com'
  const now = new Date().toUTCString()

  const items = articles.map((article: any) => {
    const url = `${siteUrl}/articles/${article.slug?.current || article.slug}`
    const imageUrl = article.mainImage
      ? optimizedUrl(article.mainImage).width(1200).url()
      : null
    const pubDate = article.publishedAt
      ? new Date(article.publishedAt).toUTCString()
      : now

    return `    <item>
      <title><![CDATA[${article.title}]]></title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <pubDate>${pubDate}</pubDate>
      <description><![CDATA[${article.metaDescription || ''}]]></description>${article.categorySlug ? `
      <category>${escapeXml(article.categorySlug)}</category>` : ''}${imageUrl ? `
      <enclosure url="${escapeXml(imageUrl)}" type="image/webp" length="0" />` : ''}
    </item>`
  }).join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>K-TREND TIMES</title>
    <link>${siteUrl}</link>
    <description>韓国トレンド情報をお届けするニュースメディア</description>
    <language>ja</language>
    <lastBuildDate>${now}</lastBuildDate>
    <atom:link href="${siteUrl}/feed" rel="self" type="application/rss+xml" />
${items}
  </channel>
</rss>`

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600',
    },
  })
}
