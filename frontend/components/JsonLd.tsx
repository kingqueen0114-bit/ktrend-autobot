type Props = {
  data: Record<string, any>
}

export default function JsonLd({data}: Props) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{__html: JSON.stringify(data).replace(/</g, '\\u003c')}}
    />
  )
}
