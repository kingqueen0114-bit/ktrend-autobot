import Link from 'next/link'
import Image from 'next/image'
import {urlFor} from '@/lib/sanity'
import CategoryBadge from './CategoryBadge'

type Props = {
  article: {
    _id: string
    title: string
    slug: {current: string}
    publishedAt?: string
    excerpt?: string
    mainImage?: any
    category?: {title: string; slug: {current: string}; color: string}
    artistTags?: string[]
  }
  variant?: 'default' | 'featured' | 'sidebar'
  rank?: number
}

function getRankStyle(rank: number): string {
  if (rank === 1) return 'bg-[#FFD700]'
  if (rank === 2) return 'bg-[#C0C0C0]'
  if (rank === 3) return 'bg-[#CD7F32]'
  return 'bg-gray-400'
}

export default function ArticleCard({article, variant = 'default', rank}: Props) {
  const imageUrl = article.mainImage
    ? urlFor(article.mainImage).width(variant === 'sidebar' ? 120 : 640).height(variant === 'sidebar' ? 80 : 360).url()
    : null

  const date = article.publishedAt
    ? new Date(article.publishedAt).toLocaleDateString('ja-JP', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : ''

  if (variant === 'sidebar') {
    return (
      <Link href={`/articles/${article.slug.current}`} className="flex gap-3 group">
        {rank && (
          <span
            className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-white text-xs font-bold ${getRankStyle(rank)}`}
          >
            {rank}
          </span>
        )}
        <div className="relative w-[100px] h-[66px] flex-shrink-0 overflow-hidden rounded">
          {imageUrl ? (
            <Image
              src={imageUrl}
              alt={article.title}
              fill
              className="object-cover group-hover:scale-105 transition-transform"
              sizes="100px"
            />
          ) : (
            <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
              <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z" /></svg>
            </div>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="text-sm font-medium text-[#292929] line-clamp-2 group-hover:text-[#f84643] transition-colors">
            {article.title}
          </h4>
          <time className="text-xs text-[#67737e] mt-1 block">{date}</time>
        </div>
      </Link>
    )
  }

  if (variant === 'featured') {
    return (
      <Link href={`/articles/${article.slug.current}`} className="block group">
        <div className="relative aspect-video overflow-hidden rounded-lg">
          {imageUrl ? (
            <Image
              src={imageUrl}
              alt={article.title}
              fill
              className="object-cover group-hover:scale-105 transition-transform duration-300"
              sizes="(max-width: 768px) 100vw, 70vw"
              priority
            />
          ) : (
            <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
              <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z" /></svg>
            </div>
          )}
          {article.category && (
            <div className="absolute top-3 left-3">
              <CategoryBadge category={article.category} asLink={false} />
            </div>
          )}
        </div>
        <h2 className="mt-3 text-xl md:text-2xl font-bold text-[#292929] line-clamp-2 group-hover:text-[#f84643] transition-colors">
          {article.title}
        </h2>
        {article.excerpt && (
          <p className="mt-2 text-sm text-[#67737e] line-clamp-2">{article.excerpt}</p>
        )}
        <time className="text-xs text-[#67737e] mt-2 block">{date}</time>
      </Link>
    )
  }

  return (
    <Link href={`/articles/${article.slug.current}`} className="block group">
      <div className="relative aspect-video overflow-hidden rounded">
        {imageUrl ? (
          <Image
            src={imageUrl}
            alt={article.title}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            sizes="(max-width: 768px) 100vw, 33vw"
          />
        ) : (
          <div className="absolute inset-0 bg-gray-200 flex items-center justify-center">
            <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z" /></svg>
          </div>
        )}
        {article.category && (
          <div className="absolute top-2 left-2">
            <CategoryBadge category={article.category} asLink={false} />
          </div>
        )}
      </div>
      <h3 className="mt-2 text-base font-bold text-[#292929] line-clamp-2 group-hover:text-[#f84643] transition-colors">
        {article.title}
      </h3>
      {article.excerpt && (
        <p className="mt-1 text-sm text-[#67737e] line-clamp-2">{article.excerpt}</p>
      )}
      {article.artistTags && article.artistTags.length > 0 && (
        <div className="flex gap-1 flex-wrap mt-1.5">
          {article.artistTags.slice(0, 3).map((tag: string) => (
            <span key={tag} className="border border-[#f84643]/50 text-[#f84643] text-[10px] px-2 py-0.5 rounded-full">
              {tag}
            </span>
          ))}
        </div>
      )}
      <span className="text-[#f84643] text-xs font-medium mt-1 inline-block">
        続きを読む &raquo;
      </span>
      <time className="text-xs text-[#67737e] mt-1 block">{date}</time>
    </Link>
  )
}
