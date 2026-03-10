'use client'

import { trackEvent } from '@/lib/analytics'

interface ShareButtonsProps {
  url: string
  title: string
}

export default function ShareButtons({ url, title }: ShareButtonsProps) {
  const encodedUrl = encodeURIComponent(url)
  const encodedTitle = encodeURIComponent(title)

  const handleShare = (platform: string, shareUrl: string) => {
    trackEvent('share_click', { platform, slug: url })
    window.open(shareUrl, '_blank', 'noopener,noreferrer,width=600,height=400')
  }

  return (
    <div className="flex items-center gap-2 mb-6">
      {/* X (Twitter) */}
      <button
        onClick={() => handleShare('x', `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}`)}
        className="inline-flex items-center gap-1.5 px-4 py-2 rounded text-white text-sm font-medium transition-opacity hover:opacity-80"
        style={{ backgroundColor: '#000' }}
        aria-label="Xでシェア"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
        </svg>
        <span>X</span>
      </button>

      {/* LINE */}
      <button
        onClick={() => handleShare('line', `https://social-plugins.line.me/lineit/share?url=${encodedUrl}`)}
        className="inline-flex items-center gap-1.5 px-4 py-2 rounded text-white text-sm font-medium transition-opacity hover:opacity-80"
        style={{ backgroundColor: '#06C755' }}
        aria-label="LINEでシェア"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .348-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .349-.281.63-.63.63h-2.386c-.345 0-.627-.281-.627-.63V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.63-.631.63-.346 0-.626-.286-.626-.63V8.108c0-.271.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.63-.631.63-.345 0-.627-.286-.627-.63V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.63H4.917c-.345 0-.63-.286-.63-.63V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .349-.281.63-.629.63M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314" />
        </svg>
        <span>LINE</span>
      </button>

      {/* Hatena Bookmark */}
      <button
        onClick={() => handleShare('hatena', `https://b.hatena.ne.jp/entry/${url}`)}
        className="inline-flex items-center gap-1.5 px-4 py-2 rounded text-white text-sm font-medium transition-opacity hover:opacity-80"
        style={{ backgroundColor: '#00A4DE' }}
        aria-label="はてなブックマークに追加"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M20.47 0C22.42 0 24 1.58 24 3.53v16.94c0 1.95-1.58 3.53-3.53 3.53H3.53C1.58 24 0 22.42 0 20.47V3.53C0 1.58 1.58 0 3.53 0h16.94zm-3.705 14.47c-.78 0-1.41.63-1.41 1.41s.63 1.414 1.41 1.414 1.41-.634 1.41-1.414-.63-1.41-1.41-1.41zm.255-9.09h-2.1v8.82h2.1V5.38zm-5.016 5.67c-.72-.36-1.21-.96-1.21-1.89 0-1.8 1.41-2.55 3.03-2.55h3.45v8.82h-3.63c-1.74 0-3.18-.78-3.18-2.67 0-1.17.63-1.98 1.54-2.31v-.03zm1.83.63c-1.02 0-1.59.51-1.59 1.32 0 .78.51 1.26 1.53 1.26h1.38v-2.58h-1.32zm-.15-3.93c-.84 0-1.38.45-1.38 1.17 0 .69.48 1.17 1.38 1.17h1.17V7.75h-1.17z" />
        </svg>
        <span>はてブ</span>
      </button>
    </div>
  )
}
