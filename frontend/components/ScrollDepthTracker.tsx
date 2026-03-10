'use client'

import { useEffect, useRef } from 'react'
import { trackEvent } from '@/lib/analytics'

const THRESHOLDS = [25, 50, 75, 100]

export default function ScrollDepthTracker({ slug }: { slug: string }) {
  const fired = useRef<Set<number>>(new Set())

  useEffect(() => {
    fired.current = new Set()

    const handleScroll = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight
      if (scrollHeight <= 0) return
      const percent = Math.round((window.scrollY / scrollHeight) * 100)

      for (const threshold of THRESHOLDS) {
        if (percent >= threshold && !fired.current.has(threshold)) {
          fired.current.add(threshold)
          trackEvent('scroll_depth', {
            depth: threshold,
            slug,
          })
        }
      }
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [slug])

  return null
}
