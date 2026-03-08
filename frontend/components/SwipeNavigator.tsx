'use client'

import { useRouter, usePathname } from 'next/navigation'
import {
  useRef,
  useCallback,
  useState,
  useEffect,
  type ReactNode,
  type TouchEvent,
} from 'react'

const CATEGORIES = [
  { slug: '', path: '/' },
  { slug: 'trend', path: '/category/trend' },
  { slug: 'event', path: '/category/event' },
  { slug: 'gourmet', path: '/category/gourmet' },
  { slug: 'artist', path: '/category/artist' },
  { slug: 'koreantrip', path: '/category/koreantrip' },
  { slug: 'beauty', path: '/category/beauty' },
  { slug: 'fashion', path: '/category/fashion' },
  { slug: 'lifestyle', path: '/category/lifestyle' },
]

const SWIPE_THRESHOLD = 50
const SWIPE_MAX_Y = 30 // tighter vertical threshold for better gesture detection

export default function SwipeNavigator({ children }: { children: ReactNode }) {
  const router = useRouter()
  const pathname = usePathname()

  const touchStart = useRef<{ x: number; y: number } | null>(null)
  const touchEnd = useRef<{ x: number; y: number } | null>(null)

  const [offsetX, setOffsetX] = useState(0)
  const [useTransition, setUseTransition] = useState(false)
  const [animating, setAnimating] = useState(false)

  const isHorizontalSwipe = useRef(false)
  const isVerticalLock = useRef(false)
  const viewportWidth = useRef(375)
  const contentRef = useRef<HTMLDivElement>(null)

  // Track article category context for accurate swipe math
  const [articleCategoryAlias, setArticleCategoryAlias] = useState<string | null>(null)

  // Resolve category context when viewing an individual article
  useEffect(() => {
    async function resolveArticleCategory() {
      if (pathname.startsWith('/articles/') && pathname !== '/articles') {
        const slugMatch = pathname.match(/\/articles\/([^\/]+)/)
        const slug = slugMatch ? slugMatch[1] : null

        if (!slug) {
          setArticleCategoryAlias(null)
          return
        }

        try {
          const response = await fetch('/api/article-category/' + encodeURIComponent(slug))
          if (!response.ok) throw new Error('Network response was not ok')
          const data = await response.json()

          if (data?.categorySlug) {
            setArticleCategoryAlias(data.categorySlug)
          } else {
            setArticleCategoryAlias(null)
          }
        } catch (e) {
          console.error('Failed to fetch article category from proxy API', e)
          setArticleCategoryAlias(null)
        }
      } else {
        setArticleCategoryAlias(null)
      }
    }
    resolveArticleCategory()
  }, [pathname])

  // Keep refs in sync with state for use in native event listener
  const animatingRef = useRef(false)
  useEffect(() => {
    animatingRef.current = animating
  }, [animating])

  // Get viewport width on mount
  useEffect(() => {
    viewportWidth.current = window.innerWidth
    const handleResize = () => {
      viewportWidth.current = window.innerWidth
    }
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  const getCurrentIndex = useCallback(() => {
    // Exact home or general archive => index 0 (最新)
    if (pathname === '/' || pathname === '/articles') return 0

    // Exact category archive => resolve via pathname chunk
    const match = pathname.match(/^\/category\/(.+)$/)
    if (match) {
      const idx = CATEGORIES.findIndex((c) => c.slug === match[1])
      return idx >= 0 ? idx : 0
    }

    // Inside an individual article => resolve via fetched category alias
    if (pathname.startsWith('/articles/') && articleCategoryAlias) {
      const idx = CATEGORIES.findIndex((c) => c.slug === articleCategoryAlias)
      return idx >= 0 ? idx : 0
    }

    // Default fallback => index 0 (最新)
    if (pathname.startsWith('/articles/')) return 0
    return -1
  }, [pathname, articleCategoryAlias])

  // Keep getCurrentIndex accessible from native event listener via ref
  const getCurrentIndexRef = useRef(getCurrentIndex)
  useEffect(() => {
    getCurrentIndexRef.current = getCurrentIndex
  }, [getCurrentIndex])

  const onTouchStart = useCallback(
    (e: TouchEvent) => {
      if (animating) return
      const idx = getCurrentIndex()
      if (idx < 0) return

      // Allow touches everywhere, including screen edges, so users can swipe
      // in the "safe zones" we created around AdSense iframes.

      touchEnd.current = null
      touchStart.current = {
        x: e.targetTouches[0].clientX,
        y: e.targetTouches[0].clientY,
      }
      isHorizontalSwipe.current = false
      isVerticalLock.current = false
    },
    [animating, getCurrentIndex],
  )

  // Native (non-passive) touchmove handler to enable preventDefault for vertical scroll lock
  useEffect(() => {
    const el = contentRef.current
    if (!el) return

    const handleTouchMove = (e: globalThis.TouchEvent) => {
      if (animatingRef.current || !touchStart.current) return

      const currentIndex = getCurrentIndexRef.current()
      if (currentIndex < 0) return

      touchEnd.current = {
        x: e.touches[0].clientX,
        y: e.touches[0].clientY,
      }

      const distX = touchStart.current.x - touchEnd.current.x
      const distY = Math.abs(touchStart.current.y - touchEnd.current.y)

      if (isVerticalLock.current) return

      // Decide gesture direction early
      if (!isHorizontalSwipe.current) {
        // If vertical movement is more than horizontal, lock to vertical
        if (distY > Math.abs(distX) && distY > 10) {
          isVerticalLock.current = true
          setOffsetX(0)
          return
        }
        if (Math.abs(distX) < 8) return
        isHorizontalSwipe.current = true
      }

      // CRITICAL: Prevent vertical scrolling during horizontal swipe
      if (isHorizontalSwipe.current) {
        e.preventDefault()
      }

      const canGoNext = currentIndex < CATEGORIES.length - 1
      const canGoPrev = currentIndex > 0

      if ((distX > 0 && canGoNext) || (distX < 0 && canGoPrev)) {
        // 1:1 finger tracking - content follows finger exactly
        // No cap - allow full viewport width slide
        setOffsetX(-distX)
      } else {
        // At the boundary - rubber-band resistance (max ~30px)
        const resistance = Math.min(Math.abs(distX) / 300, 1) * 30
        setOffsetX(distX > 0 ? -resistance : resistance)
      }
    }

    el.addEventListener('touchmove', handleTouchMove, { passive: false })
    return () => el.removeEventListener('touchmove', handleTouchMove)
  }, []) // Empty deps - uses refs for all mutable values

  const snapBack = useCallback(() => {
    setUseTransition(true)
    setOffsetX(0)
    setTimeout(() => {
      setUseTransition(false)
    }, 310)
  }, [])

  const onTouchEnd = useCallback(() => {
    if (animating) return

    if (!touchStart.current || !touchEnd.current || isVerticalLock.current) {
      if (offsetX !== 0) snapBack()
      touchStart.current = null
      touchEnd.current = null
      return
    }

    const distX = touchStart.current.x - touchEnd.current.x

    if (!isHorizontalSwipe.current) {
      snapBack()
      touchStart.current = null
      touchEnd.current = null
      return
    }

    const currentIndex = getCurrentIndex()
    if (currentIndex < 0) {
      setOffsetX(0)
      touchStart.current = null
      touchEnd.current = null
      return
    }

    let targetPath: string | null = null
    let direction: 'left' | 'right' | null = null

    if (distX > SWIPE_THRESHOLD) {
      const nextIndex = currentIndex + 1
      if (nextIndex < CATEGORIES.length) {
        targetPath = CATEGORIES[nextIndex].path
        direction = 'left'
      }
    } else if (distX < -SWIPE_THRESHOLD) {
      const prevIndex = currentIndex - 1
      if (prevIndex >= 0) {
        targetPath = CATEGORIES[prevIndex].path
        direction = 'right'
      }
    }

    if (targetPath && direction) {
      const vw = viewportWidth.current
      const dest = targetPath
      const dir = direction

      // PHASE 1: Slide current page completely off-screen
      setAnimating(true)
      setUseTransition(true)
      const slideOutTarget = dir === 'left' ? -vw : vw
      setOffsetX(slideOutTarget)

      // PHASE 2: After slide-out completes, navigate and slide in
      setTimeout(() => {
        router.push(dest)

        // Position new content on the incoming side (no transition)
        setUseTransition(false)
        const slideInStart = dir === 'left' ? vw * 0.4 : -vw * 0.4
        setOffsetX(slideInStart)

        // PHASE 3: Slide in new content
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            setUseTransition(true)
            setOffsetX(0)

            setTimeout(() => {
              setUseTransition(false)
              setAnimating(false)
            }, 320)
          })
        })
      }, 280)
    } else {
      snapBack()
    }

    touchStart.current = null
    touchEnd.current = null
  }, [getCurrentIndex, router, animating, offsetX, snapBack])

  // Compute box-shadow for depth effect on the exposed edge
  const shadowStyle = (() => {
    if (offsetX === 0) return 'none'
    // Shadow on the trailing edge of the sliding content
    if (offsetX < 0) {
      // Moving left - shadow on right edge
      return '8px 0 24px -4px rgba(0,0,0,0.2), 2px 0 6px -2px rgba(0,0,0,0.1)'
    }
    // Moving right - shadow on left edge
    return '-8px 0 24px -4px rgba(0,0,0,0.2), -2px 0 6px -2px rgba(0,0,0,0.1)'
  })()

  const transitionStyle = useTransition
    ? 'transform 300ms cubic-bezier(0.2, 0.9, 0.3, 1)'
    : 'none'

  return (
    <div style={{ overflow: 'hidden', position: 'relative' }}>
      {/* Background layer - visible when content slides away */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: '#f0f0f0',
          zIndex: 0,
          minHeight: '100vh',
        }}
      />
      {/* Sliding content layer */}
      <div
        ref={contentRef}
        onTouchStart={onTouchStart}
        onTouchEnd={onTouchEnd}
        style={{
          position: 'relative',
          zIndex: 1,
          backgroundColor: 'white',
          transform: `translateX(${offsetX}px)`,
          transition: transitionStyle,
          willChange: animating ? 'transform' : 'auto',
          boxShadow: shadowStyle,
          minHeight: '100vh',
          touchAction: 'pan-y',
        }}
      >
        {children}
      </div>
    </div>
  )
}
