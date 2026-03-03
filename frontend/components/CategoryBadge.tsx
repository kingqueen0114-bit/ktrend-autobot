'use client'

import Link from 'next/link'

type Props = {
  category: {
    title: string
    slug?: {current: string}
    color: string
  }
  size?: 'sm' | 'md'
  asLink?: boolean
}

export default function CategoryBadge({category, size = 'sm', asLink = true}: Props) {
  const className = `inline-block text-white font-medium rounded ${
    size === 'sm' ? 'text-xs px-2 py-0.5' : 'text-sm px-3 py-1'
  }`

  if (asLink && category.slug?.current) {
    return (
      <Link
        href={`/category/${category.slug.current}`}
        className={className}
        style={{backgroundColor: category.color}}
        onClick={(e) => e.stopPropagation()}
      >
        {category.title}
      </Link>
    )
  }

  return (
    <span
      className={className}
      style={{backgroundColor: category.color}}
    >
      {category.title}
    </span>
  )
}
