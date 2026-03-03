'use client'

import {useState} from 'react'
import Checkpoint from './Checkpoint'
import PortableText from './PortableText'
import AdSlot from './AdSlot'

type Props = {
  highlights: string[] | null
  body: any
  sourceUrl?: string
}

export default function ArticleBody({highlights, body, sourceUrl}: Props) {
  const hasHighlights = highlights && highlights.length > 0
  const [expanded, setExpanded] = useState(!hasHighlights)

  return (
    <>
      {/* AI Checkpoint + もっと見るボタン一体型 */}
      {hasHighlights && (
        <div className="mb-6">
          <Checkpoint highlights={highlights} />
          {!expanded && (
            <button
              onClick={() => setExpanded(true)}
              className="w-full py-3 bg-gray-50 border border-t-0 border-gray-200 rounded-b-xl text-sm font-bold text-[#1E88E5] hover:text-[#1565C0] hover:bg-gray-100 transition-all flex items-center justify-center gap-1"
            >
              <span>もっと見る</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </button>
          )}
        </div>
      )}

      {/* Article body */}
      {expanded && (
        <>
          <AdSlot slot="article-top" style={{minHeight: 250}} />

          <div className="prose-custom">
            {body && <PortableText value={body} />}
          </div>

          <AdSlot slot="article-bottom" style={{minHeight: 280}} />

          {/* Source */}
          {sourceUrl && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-[#67737e]">
                ソース:{' '}
                <a
                  href={sourceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[#1E88E5] hover:underline"
                >
                  {sourceUrl}
                </a>
              </p>
            </div>
          )}
        </>
      )}
    </>
  )
}
