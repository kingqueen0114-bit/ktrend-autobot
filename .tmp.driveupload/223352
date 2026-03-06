type Props = {
  slot: string
  format?: 'auto' | 'rectangle' | 'vertical' | 'horizontal'
  style?: React.CSSProperties
}

export default function AdSlot({slot, format = 'auto', style}: Props) {
  return (
    <div className="ad-container my-6" style={{minHeight: 250, ...style}}>
      <ins
        className="adsbygoogle"
        style={{display: 'block'}}
        data-ad-client={process.env.NEXT_PUBLIC_ADSENSE_ID || ''}
        data-ad-slot={slot}
        data-ad-format={format}
        data-full-width-responsive="true"
      />
    </div>
  )
}
