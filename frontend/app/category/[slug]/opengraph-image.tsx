import { ImageResponse } from 'next/og'
import { client } from '@/lib/sanity'

export const runtime = 'edge'
export const alt = 'K-TREND TIMES'
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

const categoryColors: Record<string, string> = {
  artist: '#e94560',
  beauty: '#ff6b9d',
  fashion: '#c44569',
  gourmet: '#f8b500',
  koreantrip: '#38ada9',
  event: '#6c5ce7',
  trend: '#0984e3',
  lifestyle: '#00b894',
}

export default async function Image({ params }: { params: { slug: string } }) {
  const slug = decodeURIComponent(params.slug)
  const category = await client.fetch(
    `*[_type == "category" && slug.current == $slug][0]{ title, slug, color, description }`,
    { slug }
  )

  const title = category?.title || slug
  const color = category?.color || categoryColors[slug] || '#292929'
  const description = category?.description || `${title}の最新ニュース・トレンド情報`

  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          background: `linear-gradient(135deg, ${color} 0%, #292929 100%)`,
          color: '#ffffff',
        }}
      >
        <div
          style={{
            fontSize: 28,
            fontWeight: 600,
            letterSpacing: '4px',
            marginBottom: '24px',
            opacity: 0.8,
          }}
        >
          K-TREND TIMES
        </div>
        <div
          style={{
            fontSize: 64,
            fontWeight: 700,
            marginBottom: '16px',
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontSize: 24,
            opacity: 0.7,
            maxWidth: '800px',
            textAlign: 'center',
          }}
        >
          {description}
        </div>
      </div>
    ),
    { ...size }
  )
}
