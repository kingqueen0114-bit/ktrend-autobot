'use client'

import { useEffect, useRef, useState } from 'react'

type Props = {
  slot: string
  format?: 'auto' | 'rectangle' | 'vertical' | 'horizontal' | 'fluid'
  style?: React.CSSProperties
  className?: string
  'data-ad-layout-key'?: string
}

export default function AdSlot({ slot, format = 'auto', style, className, 'data-ad-layout-key': dataAdLayoutKey }: Props) {
  const [isVisible, setIsVisible] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = containerRef.current
    if (!el) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
          observer.disconnect()
        }
      },
      { rootMargin: '200px' }
    )

    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    if (!isVisible) return
    try {
      if (typeof window !== 'undefined' && process.env.NODE_ENV === 'production' && process.env.NEXT_PUBLIC_ADSENSE_ID) {
        const adsbygoogle = (window as any).adsbygoogle || []
        adsbygoogle.push({})
      }
    } catch (err) {
      console.error('AdSense Error:', err)
    }
  }, [isVisible])

  // Show placeholder in development or if ad client ID is missing
  if (process.env.NODE_ENV === 'development' || !process.env.NEXT_PUBLIC_ADSENSE_ID) {
    return (
      <div ref={containerRef} className={`ad-container w-full overflow-hidden flex justify-center py-2 px-4 md:px-0 ${className || ''}`} style={style}>
        <div className="w-full h-full min-h-[50px] bg-gray-50 flex flex-col items-center justify-center border border-gray-200 rounded text-[#9ca3af] relative">
          <span className="text-[10px] absolute top-1 left-2">Sponsor</span>
          <span className="text-sm font-medium">Ad Space</span>
        </div>
      </div>
    )
  }

  return (
    <div ref={containerRef} className={`ad-container w-full overflow-hidden flex justify-center py-2 px-4 md:px-0 ${className || ''}`} style={style}>
      {isVisible && (
        <ins
          className={`adsbygoogle ${className || ''}`}
          style={{ display: 'block', width: '100%', ...style }}
          data-ad-client={process.env.NEXT_PUBLIC_ADSENSE_ID}
          data-ad-slot={slot}
          data-ad-format={format}
          data-full-width-responsive="true"
          {...(dataAdLayoutKey ? { 'data-ad-layout-key': dataAdLayoutKey } : {})}
        />
      )}
    </div>
  )
}
