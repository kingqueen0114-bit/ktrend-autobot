'use client'

import { useEffect } from 'react'

type Props = {
  slot: string
  format?: 'auto' | 'rectangle' | 'vertical' | 'horizontal'
  style?: React.CSSProperties
  className?: string
}

export default function AdSlot({ slot, format = 'auto', style, className }: Props) {
  useEffect(() => {
    try {
      if (typeof window !== 'undefined') {
        const adsbygoogle = (window as any).adsbygoogle || []
        adsbygoogle.push({})
      }
    } catch (err) {
      console.error('AdSense Error:', err)
    }
  }, [])

  return (
    <div className={`ad-container w-full overflow-hidden flex justify-center py-6 px-4 md:px-0 ${className || 'my-6'}`} style={style}>
      <ins
        className="adsbygoogle"
        style={{ display: 'block' }}
        data-ad-client={process.env.NEXT_PUBLIC_ADSENSE_ID || ''}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  )
}
