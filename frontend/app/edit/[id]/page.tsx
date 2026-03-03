import ArticleEditor from '@/components/editor/ArticleEditor'

type Props = {
  params: Promise<{id: string}>
  searchParams: Promise<{token?: string}>
}

export default async function EditPage({params, searchParams}: Props) {
  const {id} = await params
  const {token} = await searchParams

  if (!token) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-red-500 text-lg">認証トークンが必要です</p>
      </div>
    )
  }

  return <ArticleEditor id={id} token={token} />
}
