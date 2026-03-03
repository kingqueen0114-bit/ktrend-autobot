type Props = {
  highlights: string[]
}

export default function Checkpoint({highlights}: Props) {
  if (!highlights || highlights.length === 0) return null

  return (
    <div className="border border-gray-200 rounded-t-xl p-5 bg-white">
      <div className="flex items-center gap-2 mb-4">
        {/* Green checkmark circle */}
        <span className="w-7 h-7 rounded-full bg-[#4CAF50] flex items-center justify-center flex-shrink-0">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </span>
        <span className="text-sm font-bold text-[#4CAF50] uppercase tracking-wider">
          CHECKPOINT
        </span>
      </div>
      <div className="divide-y divide-gray-100">
        {highlights.map((item, i) => (
          <div key={i} className="flex items-start gap-3 py-3 first:pt-0 last:pb-0">
            {/* Blue checkmark circle */}
            <span className="w-6 h-6 rounded-full bg-[#2196F3] flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </span>
            <p className="text-sm text-[#292929] leading-relaxed">{item}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
