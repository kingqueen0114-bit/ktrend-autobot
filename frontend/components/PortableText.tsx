import { PortableText as PortableTextReact } from '@portabletext/react'
import Image from 'next/image'
import { optimizedUrl } from '@/lib/sanity'

const components = {
  types: {
    image: ({ value }: { value: any }) => {
      const imageUrl = optimizedUrl(value).width(800).url()

      // Calculate aspect ratio from Sanity reference
      let aspectRatio = '16/9' // fallback
      if (value?.asset?._ref) {
        // _ref format: image-Tb9Ew8CXIwaY6R1kjMvI0uRR-2000x3000-jpg
        const match = value.asset._ref.match(/-(\d+)x(\d+)-/)
        if (match) {
          const width = parseInt(match[1], 10)
          const height = parseInt(match[2], 10)
          aspectRatio = `${width}/${height}`
        }
      }

      return (
        <figure className="my-6">
          <div className="relative w-full" style={{ aspectRatio }}>
            <Image
              src={imageUrl}
              alt={value.alt || ''}
              fill
              className="object-contain rounded"
              sizes="(max-width: 768px) 100vw, 800px"
            />
          </div>
          {value.caption && (
            <figcaption className="text-sm text-[#67737e] mt-2 text-center">
              {value.caption}
            </figcaption>
          )}
        </figure>
      )
    },

    youtube: ({ value }: { value: { url: string } }) => {
      // Extract video ID from various YouTube URL formats
      const url = value?.url || ''
      let videoId = ''
      const match = url.match(
        /(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/))([a-zA-Z0-9_-]{11})/
      )
      if (match) videoId = match[1]

      if (!videoId) return null

      return (
        <div className="my-6">
          <div className="relative w-full" style={{ aspectRatio: '16/9' }}>
            <iframe
              src={`https://www.youtube.com/embed/${videoId}`}
              title="YouTube video"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="absolute inset-0 w-full h-full rounded"
            />
          </div>
        </div>
      )
    },

    instagram: ({ value }: { value: { url: string } }) => {
      const url = value?.url || ''
      // Extract Instagram post URL for embed
      const match = url.match(/instagram\.com\/(p|reel)\/([a-zA-Z0-9_-]+)/)
      if (!match) return null

      return (
        <div className="my-6 flex justify-center">
          <iframe
            src={`https://www.instagram.com/${match[1]}/${match[2]}/embed`}
            title="Instagram post"
            className="border-0 rounded"
            width={400}
            height={480}
            allowFullScreen
          />
        </div>
      )
    },

    table: ({ value }: { value: { rows: { cells: string[] }[] } }) => {
      if (!value?.rows?.length) return null
      const [header, ...body] = value.rows

      return (
        <div className="my-6 overflow-x-auto">
          <table className="w-full border-collapse text-sm">
            <thead>
              <tr className="bg-gray-100">
                {header.cells.map((cell: string, i: number) => (
                  <th
                    key={i}
                    className="border border-gray-200 px-4 py-2.5 font-bold text-left text-[#292929]"
                  >
                    {cell}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {body.map((row: { cells: string[] }, rowIdx: number) => (
                <tr key={rowIdx} className={rowIdx % 2 === 1 ? 'bg-gray-50' : ''}>
                  {row.cells.map((cell: string, cellIdx: number) => (
                    <td
                      key={cellIdx}
                      className="border border-gray-200 px-4 py-2 text-[#292929]"
                    >
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )
    },
  },

  marks: {
    link: ({ children, value }: { children: React.ReactNode; value?: { href: string } }) => (
      <a
        href={value?.href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-[#1E88E5] hover:underline"
      >
        {children}
      </a>
    ),

    code: ({ children }: { children: React.ReactNode }) => (
      <code className="bg-gray-100 text-[#d63384] px-1.5 py-0.5 rounded text-sm font-mono">
        {children}
      </code>
    ),

    highlight: ({ children }: { children: React.ReactNode }) => (
      <span className="bg-yellow-100 px-0.5">{children}</span>
    ),
  },

  block: {
    h2: ({ children }: { children?: React.ReactNode }) => (
      <h2 className="text-xl md:text-2xl font-bold text-[#292929] mt-10 mb-5 pb-3 border-b-2 border-[#292929]">
        {children}
      </h2>
    ),
    h3: ({ children }: { children?: React.ReactNode }) => (
      <h3 className="text-lg md:text-xl font-bold text-[#292929] mt-8 mb-4 pl-3 border-l-4 border-[#1E88E5]">
        {children}
      </h3>
    ),
    h4: ({ children }: { children?: React.ReactNode }) => (
      <h4 className="text-lg font-bold text-[#292929] mt-6 mb-3 flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-[#1E88E5]"></span>
        {children}
      </h4>
    ),
    blockquote: ({ children }: { children?: React.ReactNode }) => (
      <blockquote className="border-l-4 border-[#292929] pl-4 my-4 text-[#67737e] italic">
        {children}
      </blockquote>
    ),
    normal: ({ children }: { children?: React.ReactNode }) => (
      <p className="text-base whitespace-pre-line leading-relaxed text-[#292929] mb-4">{children}</p>
    ),
  },

  list: {
    bullet: ({ children }: { children?: React.ReactNode }) => (
      <ul className="list-disc pl-6 mb-4 space-y-1">{children}</ul>
    ),
    number: ({ children }: { children?: React.ReactNode }) => (
      <ol className="list-decimal pl-6 mb-4 space-y-1">{children}</ol>
    ),
  },
}

type Props = {
  value: any[]
}

export default function PortableText({ value }: Props) {
  return <PortableTextReact value={value} components={components} />
}
