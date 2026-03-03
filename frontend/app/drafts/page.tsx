import Link from 'next/link'
import {createClient} from '@sanity/client'
import {urlFor} from '@/lib/sanity'
import Image from 'next/image'

const sanityClient = createClient({
  projectId: '3pe6cvt2',
  dataset: 'production',
  apiVersion: '2024-01-01',
  token: process.env.SANITY_API_TOKEN,
  useCdn: false,
  perspective: 'raw',
})

export const dynamic = 'force-dynamic'

export default async function DraftsPage() {
  const drafts = await sanityClient.fetch(
    `*[_type == "article" && _id in path("drafts.**")] | order(_updatedAt desc) {
      _id,
      title,
      slug,
      _updatedAt,
      mainImage,
      "category": category->{title, slug, color},
      qualityScore
    }`
  )

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-[#292929] mb-6">下書き一覧</h1>

      {drafts.length === 0 ? (
        <p className="text-[#67737e] text-center py-12">下書きはありません</p>
      ) : (
        <div className="space-y-3">
          {drafts.map((draft: any) => {
            const draftId = draft._id.replace(/^drafts\./, '')
            const imageUrl = draft.mainImage
              ? urlFor(draft.mainImage).width(120).height(80).url()
              : null
            const updatedAt = new Date(draft._updatedAt).toLocaleDateString('ja-JP', {
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            })

            return (
              <div
                key={draft._id}
                className="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 hover:border-[#f84643] transition-colors"
              >
                {imageUrl && (
                  <div className="relative w-[80px] h-[53px] flex-shrink-0 overflow-hidden rounded">
                    <Image src={imageUrl} alt="" fill className="object-cover" sizes="80px" />
                  </div>
                )}
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium text-[#292929] line-clamp-1">
                    {draft.title || '無題'}
                  </h3>
                  <div className="flex items-center gap-2 mt-1">
                    {draft.category && (
                      <span
                        className="text-xs text-white px-1.5 py-0.5 rounded"
                        style={{backgroundColor: draft.category.color}}
                      >
                        {draft.category.title}
                      </span>
                    )}
                    <span className="text-xs text-[#67737e]">{updatedAt}</span>
                    {draft.qualityScore != null && (
                      <span className="text-xs text-[#67737e]">
                        Score: {draft.qualityScore}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
