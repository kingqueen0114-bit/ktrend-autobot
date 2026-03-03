'use client'

import {useRouter} from 'next/navigation'
import {useState} from 'react'

type Props = {
  defaultQuery?: string
}

export default function SearchForm({defaultQuery = ''}: Props) {
  const router = useRouter()
  const [query, setQuery] = useState(defaultQuery)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const trimmed = query.trim()
    if (trimmed) {
      router.push('/search?q=' + encodeURIComponent(trimmed))
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mb-8">
      <div className="flex items-center border border-gray-300 rounded-md overflow-hidden">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="キーワードを入力..."
          className="flex-1 px-4 py-3 text-sm text-[#292929] outline-none bg-white"
          autoFocus={!defaultQuery}
        />
        <button
          type="submit"
          className="px-5 py-3 bg-[#f84643] text-white hover:bg-[#e03e3b] transition-colors"
          aria-label="検索"
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
    </form>
  )
}
