import { ImageResponse } from 'next/og'
import { client } from '@/lib/sanity'

export const runtime = 'edge'
export const alt = 'K-TREND TIMES'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

export default async function Image({ params }: { params: { slug: string } }) {
  const slug = decodeURIComponent(params.slug)
  const article = await client.fetch(
    `*[_type == "article" && slug.current == $slug][0]{ title, "categoryTitle": category->title, "categoryColor": category->color }`,
    { slug }
  )

  if (!article) {
    return new ImageResponse(
      (
        <div
          style={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#292929',
            color: '#ffffff',
            fontSize: 48,
            fontWeight: 700,
          }}
        >
          K-TREND TIMES
        </div>
      ),
      { ...size }
    )
  }

  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'flex-end',
          padding: '60px',
          background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
          color: '#ffffff',
        }}
      >
        {article.categoryTitle && (
          <div
            style={{
              display: 'flex',
              marginBottom: '20px',
            }}
          >
            <span
              style={{
                backgroundColor: article.categoryColor || '#e94560',
                color: '#ffffff',
                fontSize: 24,
                fontWeight: 600,
                padding: '8px 20px',
                borderRadius: '20px',
              }}
            >
              {article.categoryTitle}
            </span>
          </div>
        )}
        <div
          style={{
            fontSize: article.title.length > 40 ? 40 : 52,
            fontWeight: 700,
            lineHeight: 1.3,
            marginBottom: '40px',
            display: '-webkit-box',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
          }}
        >
          {article.title}
        </div>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderTop: '2px solid rgba(255,255,255,0.2)',
            paddingTop: '20px',
          }}
        >
          <span style={{ fontSize: 28, fontWeight: 700, letterSpacing: '2px' }}>
            K-TREND TIMES
          </span>
          <span style={{ fontSize: 20, opacity: 0.7 }}>
            k-trendtimes.com
          </span>
        </div>
      </div>
    ),
    { ...size }
  )
}
