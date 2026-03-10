import { client } from '@/lib/sanity'
import { newsSitemapQuery } from '@/lib/queries'

export const revalidate = 600

export async function GET() {
  const since = new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString()
  const articles = await client.fetch(newsSitemapQuery, { since })
  const siteUrl = 'https://www.k-trendtimes.com'

  const urls = articles.map((article: any) => {
    const slug = article.slug?.current || article.slug
    const pubDate = article.publishedAt
      ? new Date(article.publishedAt).toISOString()
      : new Date().toISOString()

    return `  <url>
    <loc>${siteUrl}/articles/${slug}</loc>
    <news:news>
      <news:publication>
        <news:name>K-TREND TIMES</news:name>
        <news:language>ja</news:language>
      </news:publication>
      <news:publication_date>${pubDate}</news:publication_date>
      <news:title><![CDATA[${article.title}]]></news:title>
    </news:news>
  </url>`
  }).join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
${urls}
</urlset>`

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=600, s-maxage=600',
    },
  })
}
