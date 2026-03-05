import {PortableText as PortableTextReact} from '@portabletext/react'
import Image from 'next/image'
import {urlFor} from '@/lib/sanity'

const components = {
  types: {
    image: ({value}: {value: any}) => {
      const imageUrl = urlFor(value).width(800).url()
      return (
        <figure className="my-6">
          <div className="relative w-full" style={{aspectRatio: '16/9'}}>
            <Image
              src={imageUrl}
              alt={value.alt || ''}
              fill
              className="object-cover rounded"
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
  },
  marks: {
    link: ({children, value}: {children: React.ReactNode; value?: {href: string}}) => (
      <a
        href={value?.href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-[#1E88E5] hover:underline"
      >
        {children}
      </a>
    ),
  },
  block: {
    h2: ({children}: {children?: React.ReactNode}) => (
      <h2 className="text-2xl font-bold text-[#292929] mt-8 mb-4 pb-2 border-b border-gray-200">
        {children}
      </h2>
    ),
    h3: ({children}: {children?: React.ReactNode}) => (
      <h3 className="text-xl font-bold text-[#292929] mt-6 mb-3">{children}</h3>
    ),
    blockquote: ({children}: {children?: React.ReactNode}) => (
      <blockquote className="border-l-4 border-[#292929] pl-4 my-4 text-[#67737e] italic">
        {children}
      </blockquote>
    ),
    normal: ({children}: {children?: React.ReactNode}) => (
      <p className="text-base leading-relaxed text-[#292929] mb-4">{children}</p>
    ),
  },
  list: {
    bullet: ({children}: {children?: React.ReactNode}) => (
      <ul className="list-disc pl-6 mb-4 space-y-1">{children}</ul>
    ),
    number: ({children}: {children?: React.ReactNode}) => (
      <ol className="list-decimal pl-6 mb-4 space-y-1">{children}</ol>
    ),
  },
}

type Props = {
  value: any[]
}

export default function PortableText({value}: Props) {
  return <PortableTextReact value={value} components={components} />
}
