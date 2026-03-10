'use client'

import { useState } from 'react'
import Checkpoint from './Checkpoint'
import PortableText from './PortableText'
import AdSlot from './AdSlot'

type Props = {
  highlights: string[] | null
  body: any
  sourceUrl?: string
}

export default function ArticleBody({ highlights, body, sourceUrl }: Props) {
  const hasHighlights = highlights && highlights.length > 0
  const [expanded, setExpanded] = useState(!hasHighlights)

  const isArrayBody = body && Array.isArray(body)
  let splitIndex = -1

  if (isArrayBody && body.length >= 3) {
    const mid = Math.floor(body.length / 2)

    // Helper to check if it's safe to insert an ad between prevBlock and currBlock
    const isSafeToSplit = (prevBlock: any, currBlock: any) => {
      const isSplittingList = prevBlock?.listItem && currBlock?.listItem
      const isAfterHeading = prevBlock?._type === 'block' && typeof prevBlock?.style === 'string' && prevBlock.style.startsWith('h')
      return !isSplittingList && !isAfterHeading
    }

    // Forward search
    for (let i = mid; i < body.length; i++) {
      if (isSafeToSplit(body[i - 1], body[i])) {
        splitIndex = i
        break
      }
    }

    // Backward search if forward failed
    if (splitIndex === -1) {
      for (let i = mid; i > 0; i--) {
        if (isSafeToSplit(body[i - 1], body[i])) {
          splitIndex = i
          break
        }
      }
    }

    // Fallback if absolutely no safe spot is found
    if (splitIndex === -1) {
      splitIndex = mid
    }
  } else if (isArrayBody && body.length === 2) {
    splitIndex = 1
  }

  const bodyTop = isArrayBody && splitIndex > 0 ? body.slice(0, splitIndex) : body
  const bodyBottom = isArrayBody && splitIndex > 0 ? body.slice(splitIndex) : null

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

      {/* Ad after highlights — always visible */}
      {hasHighlights && (
        <div className="my-8 w-full flex justify-center">
          <AdSlot slot="9279135629" />
        </div>
      )}

      {/* Article body */}
      {expanded && (
        <>
          <div className="prose-custom">
            {bodyTop && <PortableText value={bodyTop} />}

            {bodyBottom && bodyBottom.length > 0 && (
              <>
                <div className="my-10 w-full flex justify-center">
                  <AdSlot slot="9279135629" />
                </div>
                <PortableText value={bodyBottom} />
              </>
            )}
          </div>

          <div className="mt-12 w-full flex justify-center">
            <AdSlot slot="5544234317" />
          </div>

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
