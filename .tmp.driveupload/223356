'use client'

import Link from 'next/link'
import Image from 'next/image'
import { usePathname, useRouter } from 'next/navigation'
import { useState, useEffect, useRef, useCallback } from 'react'

const categories = [
  { title: 'アーティスト', slug: 'artist', color: '#FFA726' },
  { title: 'ビューティー', slug: 'beauty', color: '#29B6F6' },
  { title: 'ファッション', slug: 'fashion', color: '#EC407A' },
  { title: 'グルメ', slug: 'gourmet', color: '#FF7043' },
  { title: '韓国旅行', slug: 'koreantrip', color: '#78909C' },
  { title: 'イベント', slug: 'event', color: '#26A69A' },
  { title: 'トレンド', slug: 'trend', color: '#7CB342' },
  { title: 'ライフスタイル', slug: 'lifestyle', color: '#B0BEC5' },
]

interface HeaderProps {
  tickerItems?: string[]
}

export default function Header({ tickerItems }: HeaderProps) {
  const pathname = usePathname()
  const router = useRouter()
  const [searchOpen, setSearchOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [mobileSearchQuery, setMobileSearchQuery] = useState('')
  const searchInputRef = useRef<HTMLInputElement>(null)
  const mobileSearchInputRef = useRef<HTMLInputElement>(null)
  const mobileTabsRef = useRef<HTMLDivElement>(null)
  const navTouchStart = useRef<{ x: number; y: number } | null>(null)
  const navSwipeActive = useRef(false)

  const tickerTexts = tickerItems && tickerItems.length > 0
    ? tickerItems
    : ['最新ニュースをチェック']

  const tickerContent = tickerTexts.join('\u3000\u3000\u3000')

  // Focus search input when opened
  useEffect(() => {
    if (searchOpen && searchInputRef.current) {
      searchInputRef.current.focus()
    }
  }, [searchOpen])

  // Lock body scroll when mobile menu is open
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [mobileMenuOpen])

  // Auto-scroll active mobile tab into view
  useEffect(() => {
    const container = mobileTabsRef.current
    if (!container) return
    const activeTab = container.querySelector('[data-active="true"]') as HTMLElement | null
    if (activeTab) {
      const containerRect = container.getBoundingClientRect()
      const tabRect = activeTab.getBoundingClientRect()
      const scrollLeft = activeTab.offsetLeft - containerRect.width / 2 + tabRect.width / 2
      container.scrollTo({ left: scrollLeft, behavior: 'smooth' })
    }
  }, [pathname])

  const handleSearch = useCallback((query: string) => {
    const trimmed = query.trim()
    if (trimmed) {
      router.push('/search?q=' + encodeURIComponent(trimmed))
      setSearchOpen(false)
      setSearchQuery('')
      setMobileMenuOpen(false)
      setMobileSearchQuery('')
    }
  }, [router])

  // Swipe navigation on mobile tabs
  const ALL_PATHS = [
    '/',
    '/category/artist',
    '/category/beauty',
    '/category/fashion',
    '/category/gourmet',
    '/category/koreantrip',
    '/category/event',
    '/category/trend',
    '/category/lifestyle',
  ]

  const getCurrentPathIndex = useCallback(() => {
    return ALL_PATHS.indexOf(pathname)
  }, [pathname])

  const handleNavTouchStart = useCallback((e: React.TouchEvent) => {
    const touch = e.touches[0]
    // Ignore touches in edge zones (< 20px from screen edge)
    if (touch.clientX < 20 || touch.clientX > window.innerWidth - 20) {
      navTouchStart.current = null
      return
    }
    navTouchStart.current = { x: touch.clientX, y: touch.clientY }
    navSwipeActive.current = false
  }, [])

  const handleNavTouchEnd = useCallback((e: React.TouchEvent) => {
    if (!navTouchStart.current) return
    const touch = e.changedTouches[0]
    const dx = touch.clientX - navTouchStart.current.x
    const dy = touch.clientY - navTouchStart.current.y
    navTouchStart.current = null
    navSwipeActive.current = false

    // Only trigger for decisive horizontal swipes
    if (Math.abs(dx) > 50 && Math.abs(dy) < 30) {
      const currentIndex = getCurrentPathIndex()
      if (currentIndex === -1) return

      if (dx < 0 && currentIndex < ALL_PATHS.length - 1) {
        // Swipe left → next category
        router.push(ALL_PATHS[currentIndex + 1])
      } else if (dx > 0 && currentIndex > 0) {
        // Swipe right → previous category
        router.push(ALL_PATHS[currentIndex - 1])
      }
    }
  }, [getCurrentPathIndex, router])

  // Attach passive:false touchmove listener to prevent tab scroll during swipe
  useEffect(() => {
    const container = mobileTabsRef.current
    if (!container) return

    const handleTouchMove = (e: TouchEvent) => {
      if (!navTouchStart.current) return
      const touch = e.touches[0]
      const dx = Math.abs(touch.clientX - navTouchStart.current.x)
      const dy = Math.abs(touch.clientY - navTouchStart.current.y)

      // Once we detect a decisive horizontal swipe, prevent default to stop tab scrolling
      if (dx > 10 && dy < 30) {
        navSwipeActive.current = true
      }
      if (navSwipeActive.current) {
        e.preventDefault()
      }
    }

    container.addEventListener('touchmove', handleTouchMove, { passive: false })
    return () => {
      container.removeEventListener('touchmove', handleTouchMove)
    }
  }, [])

  const isActiveCategory = (slug: string) => {
    return pathname === '/category/' + slug
  }

  const isHome = pathname === '/'

  // Compute the active tab color for the indicator line
  const activeTabColor = (() => {
    if (isHome) return '#333333'
    const activeCat = categories.find((c) => pathname === '/category/' + c.slug)
    return activeCat ? activeCat.color : '#333333'
  })()

  return (
    <>
      {/* Ticker animation keyframes */}
      <style>{`
        @keyframes ticker-scroll {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .ticker-animate {
          animation: ticker-scroll 20s linear infinite;
        }
        .ticker-animate:hover {
          animation-play-state: paused;
        }
        @keyframes search-slide-down {
          from { max-height: 0; opacity: 0; }
          to { max-height: 80px; opacity: 1; }
        }
        @keyframes search-slide-up {
          from { max-height: 80px; opacity: 1; }
          to { max-height: 0; opacity: 0; }
        }
      `}</style>

      <header className="w-full">
        {/* Top bar with ticker */}
        <div className="bg-[#292929] text-white text-xs py-1.5">
          <div className="max-w-6xl mx-auto px-4 flex items-center">
            {/* Hot News label */}
            <div className="flex-shrink-0 flex items-center gap-1.5 mr-3">
              <span className="font-bold text-white text-xs whitespace-nowrap">Hot News</span>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" className="flex-shrink-0">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-1.41-1.41L12.17 12 8.59 8.41 10 7l5 5-5 5z" fill="none" />
                <path d="M13.5 0.67s.74 2.65.74 4.8c0 2.06-1.35 3.73-3.41 3.73-2.07 0-3.63-1.67-3.63-3.73l.03-.36C5.21 7.51 4 10.62 4 14c0 4.42 3.58 8 8 8s8-3.58 8-8C20 8.61 17.41 3.8 13.5.67zM11.71 19c-1.78 0-3.22-1.4-3.22-3.14 0-1.62 1.05-2.76 2.81-3.12 1.77-.36 3.6-1.21 4.62-2.58.39 1.29.59 2.65.59 4.04 0 2.65-2.15 4.8-4.8 4.8z" fill="currentColor" />
              </svg>
            </div>
            {/* News ticker */}
            <div className="flex-1 overflow-hidden relative">
              <div className="flex whitespace-nowrap ticker-animate">
                <span className="text-white/90 px-2">{tickerContent}</span>
                <span className="text-white/90 px-2">{tickerContent}</span>
              </div>
            </div>
            <div className="hidden md:flex gap-3 flex-shrink-0 ml-3">
              <a
                href="https://x.com"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:text-white/70 transition-colors text-white"
              >
                X
              </a>
            </div>
          </div>
        </div>

        {/* Logo + Search icon */}
        <div className="bg-white border-b border-gray-200">
          <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <Link href="/" className="inline-block">
              <Image
                src="/logo.png"
                alt="K-TREND TIMES"
                width={280}
                height={40}
                className="h-[32px] md:h-[40px] w-auto"
                priority
              />
            </Link>
            {/* Search icon button */}
            <button
              onClick={() => setSearchOpen(!searchOpen)}
              className="p-2 text-[#292929] hover:text-[#555] transition-colors"
              aria-label="検索"
            >
              <svg
                width="22"
                height="22"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </button>
          </div>

          {/* Search form slide-down */}
          <div
            className="overflow-hidden transition-all duration-300 ease-in-out"
            style={{
              maxHeight: searchOpen ? '80px' : '0',
              opacity: searchOpen ? 1 : 0,
            }}
          >
            <div className="max-w-6xl mx-auto px-4 pb-4">
              <div className="flex items-center border border-gray-300 rounded-md overflow-hidden">
                <input
                  ref={searchInputRef}
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      handleSearch(searchQuery)
                    }
                  }}
                  placeholder="キーワードを入力..."
                  className="flex-1 px-4 py-2.5 text-sm text-[#292929] outline-none bg-white"
                />
                <button
                  onClick={() => handleSearch(searchQuery)}
                  className="px-4 py-2.5 bg-[#292929] text-white hover:bg-[#444] transition-colors"
                  aria-label="検索実行"
                >
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Category navigation - outside header so sticky works against viewport */}
      <nav
        className="sticky top-0 z-50 bg-white"
        style={{ borderBottom: `4px solid ${activeTabColor}` }}
      >
        <div className="max-w-6xl mx-auto">
          {/* Mobile: SmartNews-style horizontal scrollable tabs */}
          <div
            ref={mobileTabsRef}
            className="md:hidden flex flex-nowrap gap-0 overflow-x-auto scrollbar-hide snap-x snap-mandatory"
            onTouchStart={handleNavTouchStart}
            onTouchEnd={handleNavTouchEnd}
          >
            <Link
              href="/"
              data-active={isHome ? 'true' : 'false'}
              className={`snap-start flex-shrink-0 rounded-t-lg font-bold text-white whitespace-nowrap transition-all duration-200 active:brightness-110 active:scale-[0.97] ${isHome ? 'px-5 py-3 text-[15px] shadow-md' : 'opacity-85 px-4 py-2.5 text-[13px]'
                }`}
              style={{ backgroundColor: isHome ? '#333333' : '#9E9E9E' }}
            >
              主要
            </Link>
            {categories.map((cat) => {
              const isActive = isActiveCategory(cat.slug)
              return (
                <Link
                  key={cat.slug}
                  href={'/category/' + cat.slug}
                  data-active={isActive ? 'true' : 'false'}
                  className={`snap-start flex-shrink-0 rounded-t-lg font-bold text-white whitespace-nowrap transition-all duration-200 active:brightness-110 active:scale-[0.97] ${isActive ? 'px-5 py-3 text-[15px] shadow-md' : 'opacity-85 px-4 py-2.5 text-[13px]'
                    }`}
                  style={{ backgroundColor: isActive ? cat.color : cat.color + 'CC' }}
                >
                  {cat.title}
                </Link>
              )
            })}
          </div>

          {/* Desktop: horizontal scroll nav */}
          <div className="hidden md:flex items-center px-4 border-b border-gray-100">
            <div className="flex overflow-x-auto scrollbar-hide gap-0 flex-1">
              {/* Home button */}
              <Link
                href="/"
                className="flex-shrink-0 px-3 py-2.5 text-sm font-medium whitespace-nowrap border-b-2 transition-colors"
                style={{
                  color: isHome ? '#292929' : '#292929',
                  borderBottomColor: isHome ? '#292929' : 'transparent',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.backgroundColor = '#292929'
                  e.currentTarget.style.color = '#fff'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.backgroundColor = 'transparent'
                  e.currentTarget.style.color = isHome ? '#292929' : '#292929'
                }}
              >
                ホーム
              </Link>

              {categories.map((cat) => {
                const isActive = isActiveCategory(cat.slug)
                return (
                  <Link
                    key={cat.slug}
                    href={'/category/' + cat.slug}
                    className="flex-shrink-0 px-3 py-2.5 text-sm font-medium transition-colors whitespace-nowrap border-b-2"
                    style={{
                      color: isActive ? cat.color : '#292929',
                      borderBottomColor: isActive ? cat.color : 'transparent',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor = cat.color
                      e.currentTarget.style.color = '#fff'
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = 'transparent'
                      e.currentTarget.style.color = isActive ? cat.color : '#292929'
                    }}
                  >
                    {cat.title}
                  </Link>
                )
              })}
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile menu overlay */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-[100] bg-white flex flex-col md:hidden">
          {/* Mobile menu header */}
          <div className="flex justify-between items-center px-4 py-4 border-b border-gray-200">
            <span
              className="text-xl font-bold text-[#292929]"
              style={{ fontFamily: "'Encode Sans Condensed', sans-serif" }}
            >
              K-TREND TIMES
            </span>
            <button
              onClick={() => setMobileMenuOpen(false)}
              className="p-2 text-[#292929]"
              aria-label="メニューを閉じる"
            >
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          {/* Mobile search */}
          <div className="px-4 py-3 border-b border-gray-100">
            <div className="flex items-center border border-gray-300 rounded-md overflow-hidden">
              <input
                ref={mobileSearchInputRef}
                type="text"
                value={mobileSearchQuery}
                onChange={(e) => setMobileSearchQuery(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSearch(mobileSearchQuery)
                  }
                }}
                placeholder="キーワードを入力..."
                className="flex-1 px-4 py-2.5 text-sm text-[#292929] outline-none"
              />
              <button
                onClick={() => handleSearch(mobileSearchQuery)}
                className="px-4 py-2.5 bg-[#292929] text-white"
                aria-label="検索実行"
              >
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="11" cy="11" r="8" />
                  <line x1="21" y1="21" x2="16.65" y2="16.65" />
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile category links */}
          <div className="flex-1 overflow-y-auto">
            <Link
              href="/"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center px-6 py-4 text-base font-medium border-b border-gray-50 transition-colors"
              style={{
                color: isHome ? '#292929' : '#292929',
                borderLeftWidth: '4px',
                borderLeftColor: isHome ? '#292929' : 'transparent',
              }}
            >
              ホーム
            </Link>
            {categories.map((cat) => {
              const isActive = isActiveCategory(cat.slug)
              return (
                <Link
                  key={cat.slug}
                  href={'/category/' + cat.slug}
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center px-6 py-4 text-base font-medium border-b border-gray-50 transition-colors"
                  style={{
                    color: isActive ? cat.color : '#292929',
                    borderLeftWidth: '4px',
                    borderLeftColor: isActive ? cat.color : 'transparent',
                  }}
                >
                  <span
                    className="w-2.5 h-2.5 rounded-full mr-3 flex-shrink-0"
                    style={{ backgroundColor: cat.color }}
                  />
                  {cat.title}
                </Link>
              )
            })}
          </div>
        </div>
      )}
    </>
  )
}
