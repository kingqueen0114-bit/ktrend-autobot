'use client'

import { useEffect } from 'react'

type Props = {
  slot: string
  format?: 'auto' | 'rectangle' | 'vertical' | 'horizontal' | 'fluid'
  style?: React.CSSProperties
  className?: string
  'data-ad-layout-key'?: string
}

export default function AdSlot({ slot, format = 'auto', style, className, 'data-ad-layout-key': dataAdLayoutKey }: Props) {
  useEffect(() => {
    try {
      if (typeof window !== 'undefined' && process.env.NODE_ENV === 'production' && process.env.NEXT_PUBLIC_ADSENSE_ID) {
        const adsbygoogle = (window as any).adsbygoogle || []
        adsbygoogle.push({})
      }
    } catch (err) {
      console.error('AdSense Error:', err)
    }
  }, [])

  // Show placeholder in development or if ad client ID is missing
  if (process.env.NODE_ENV === 'development' || !process.env.NEXT_PUBLIC_ADSENSE_ID) {
    return (
      <div className={`ad-container w-full overflow-hidden flex justify-center py-2 px-4 md:px-0 ${className || ''}`} style={style}>
        <div className="w-full h-full min-h-[50px] bg-gray-50 flex flex-col items-center justify-center border border-gray-200 rounded text-[#9ca3af] relative">
          <span className="text-[10px] absolute top-1 left-2">Sponsor</span>
          <span className="text-sm font-medium">Ad Space</span>
        </div>
      </div>
    )
  }

  return (
    <div className={`ad-container w-full overflow-hidden flex justify-center py-2 px-4 md:px-0 ${className || ''}`} style={style}>
      <ins
        className={`adsbygoogle ${className || ''}`}
        style={style}
        data-ad-client={process.env.NEXT_PUBLIC_ADSENSE_ID}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive="true"
        {...(dataAdLayoutKey ? { 'data-ad-layout-key': dataAdLayoutKey } : {})}
      />
    </div>
  )
}
