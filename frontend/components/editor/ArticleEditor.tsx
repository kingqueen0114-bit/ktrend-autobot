'use client'

import {useState, useEffect, useCallback, useRef} from 'react'

type Article = {
  _id: string
  title: string
  slug?: {current: string}
  body?: any[]
  excerpt?: string
  mainImage?: any
  imageCredit?: string
  seo?: {metaTitle?: string; metaDescription?: string}
  category?: {_id: string; title: string; slug: {current: string}; color: string}
  tags?: {_id: string; title: string}[]
  artistTags?: string[]
  qualityScore?: number
  xPost1?: string
  xPost2?: string
  newsPost?: string
  lunaPostA?: string
  lunaPostB?: string
  sourceUrl?: string
  researchReport?: string
}

type Category = {
  _id: string
  title: string
  slug: {current: string}
  color: string
}

type Props = {
  id: string
  token: string
}

export default function ArticleEditor({id, token}: Props) {
  const [article, setArticle] = useState<Article | null>(null)
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [publishing, setPublishing] = useState(false)
  const [message, setMessage] = useState<{type: 'success' | 'error'; text: string} | null>(null)
  const [activeTab, setActiveTab] = useState<'edit' | 'sns' | 'preview'>('edit')

  // Form state
  const [title, setTitle] = useState('')
  const [bodyMarkdown, setBodyMarkdown] = useState('')
  const [excerpt, setExcerpt] = useState('')
  const [imageCredit, setImageCredit] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [artistTagsStr, setArtistTagsStr] = useState('')
  const [xPost1, setXPost1] = useState('')
  const [xPost2, setXPost2] = useState('')
  const [newsPost, setNewsPost] = useState('')
  const [lunaPostA, setLunaPostA] = useState('')
  const [lunaPostB, setLunaPostB] = useState('')

  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  // Ref to track latest form data (avoids stale closure in auto-save)
  const formDataRef = useRef({
    title: '', bodyMarkdown: '', excerpt: '', xPost1: '', xPost2: '',
    newsPost: '', lunaPostA: '', lunaPostB: '', imageCredit: '',
    categoryId: '', artistTagsStr: '',
  })

  // Update ref whenever state changes
  useEffect(() => {
    formDataRef.current = {
      title, bodyMarkdown, excerpt, xPost1, xPost2,
      newsPost, lunaPostA, lunaPostB, imageCredit,
      categoryId, artistTagsStr,
    }
  }, [title, bodyMarkdown, excerpt, xPost1, xPost2, newsPost, lunaPostA, lunaPostB, imageCredit, categoryId, artistTagsStr])

  // Load article data
  useEffect(() => {
    async function loadArticle() {
      try {
        const res = await fetch(`/api/edit?id=${encodeURIComponent(id)}&token=${encodeURIComponent(token)}`)
        if (!res.ok) {
          const err = await res.json()
          throw new Error(err.error || 'Failed to load')
        }
        const data = await res.json()
        setArticle(data.article)
        setCategories(data.categories || [])

        // Initialize form
        const a = data.article
        setTitle(a.title || '')
        setBodyMarkdown(a.bodyMarkdown || a.body || '')
        setExcerpt(a.excerpt || '')
        setImageCredit(a.imageCredit || '')
        setCategoryId(a.category?._id || '')
        setArtistTagsStr((a.artistTags || []).join(', '))
        setXPost1(a.xPost1 || '')
        setXPost2(a.xPost2 || '')
        setNewsPost(a.newsPost || '')
        setLunaPostA(a.lunaPostA || '')
        setLunaPostB(a.lunaPostB || '')
      } catch (err: any) {
        setMessage({type: 'error', text: err.message})
      } finally {
        setLoading(false)
      }
    }
    loadArticle()
  }, [id, token])

  // Auto-save (debounce 3 seconds) - reads from ref to avoid stale closure
  const triggerAutoSave = useCallback(() => {
    if (saveTimeoutRef.current) clearTimeout(saveTimeoutRef.current)
    saveTimeoutRef.current = setTimeout(() => {
      handleSave(true)
    }, 3000)
  }, [])

  const handleSave = async (isAutoSave = false) => {
    if (saving) return
    setSaving(true)
    setMessage(null)

    // Read from ref to get the latest values (avoids stale closure)
    const current = formDataRef.current

    try {
      const res = await fetch('/api/edit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          id,
          token,
          action: 'save',
          data: {
            title: current.title,
            bodyMarkdown: current.bodyMarkdown,
            excerpt: current.excerpt,
            imageCredit: current.imageCredit,
            categoryId: current.categoryId || undefined,
            artistTags: current.artistTagsStr.split(',').map(s => s.trim()).filter(Boolean),
            xPost1: current.xPost1,
            xPost2: current.xPost2,
            newsPost: current.newsPost,
            lunaPostA: current.lunaPostA,
            lunaPostB: current.lunaPostB,
          },
        }),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error || 'Save failed')
      }

      if (!isAutoSave) {
        setMessage({type: 'success', text: '保存しました'})
        setTimeout(() => setMessage(null), 3000)
      }
    } catch (err: any) {
      setMessage({type: 'error', text: err.message})
    } finally {
      setSaving(false)
    }
  }

  const handlePublish = async () => {
    if (publishing) return
    if (!confirm('この記事を公開しますか？')) return

    setPublishing(true)
    setMessage(null)

    try {
      const res = await fetch('/api/edit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id, token, action: 'publish'}),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error || 'Publish failed')
      }

      const data = await res.json()
      setMessage({
        type: 'success',
        text: `公開しました！ ${data.slug ? `/articles/${data.slug}` : ''}`,
      })
    } catch (err: any) {
      setMessage({type: 'error', text: err.message})
    } finally {
      setPublishing(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#292929]" />
      </div>
    )
  }

  if (!article) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-red-500">記事が見つかりません</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {/* Tab navigation */}
      <div className="sticky top-0 z-40 bg-white border-b">
        <div className="max-w-3xl mx-auto flex">
          {(['edit', 'sns', 'preview'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`flex-1 py-3 text-sm font-medium text-center border-b-2 transition-colors ${
                activeTab === tab
                  ? 'text-[#292929] border-[#292929]'
                  : 'text-[#67737e] border-transparent hover:text-[#292929]'
              }`}
            >
              {tab === 'edit' ? '✏️ 編集' : tab === 'sns' ? '📱 SNS' : '👁️ プレビュー'}
            </button>
          ))}
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-4">
        {/* Status message */}
        {message && (
          <div
            className={`mb-4 p-3 rounded text-sm ${
              message.type === 'success'
                ? 'bg-green-50 text-green-700 border border-green-200'
                : 'bg-red-50 text-red-700 border border-red-200'
            }`}
          >
            {message.text}
          </div>
        )}

        {/* Edit tab */}
        {activeTab === 'edit' && (
          <div className="space-y-4">
            {/* Title */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">タイトル</label>
              <input
                type="text"
                value={title}
                onChange={(e) => {
                  setTitle(e.target.value)
                  triggerAutoSave()
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none"
              />
            </div>

            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">カテゴリ</label>
              <select
                value={categoryId}
                onChange={(e) => {
                  setCategoryId(e.target.value)
                  triggerAutoSave()
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none"
              >
                <option value="">選択してください</option>
                {categories.map((cat) => (
                  <option key={cat._id} value={cat._id}>
                    {cat.title}
                  </option>
                ))}
              </select>
            </div>

            {/* Artist tags */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">
                アーティストタグ（カンマ区切り）
              </label>
              <input
                type="text"
                value={artistTagsStr}
                onChange={(e) => {
                  setArtistTagsStr(e.target.value)
                  triggerAutoSave()
                }}
                placeholder="BTS, BLACKPINK, NewJeans"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none"
              />
              {artistTagsStr && (
                <div className="flex flex-wrap gap-1 mt-2">
                  {artistTagsStr.split(',').map((tag, i) => {
                    const trimmed = tag.trim()
                    if (!trimmed) return null
                    return (
                      <span key={i} className="bg-gray-100 text-gray-700 px-2 py-0.5 rounded text-xs">
                        {trimmed}
                      </span>
                    )
                  })}
                </div>
              )}
            </div>

            {/* Image credit */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">画像クレジット</label>
              <input
                type="text"
                value={imageCredit}
                onChange={(e) => {
                  setImageCredit(e.target.value)
                  triggerAutoSave()
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none"
              />
            </div>

            {/* Excerpt */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">抜粋</label>
              <textarea
                value={excerpt}
                onChange={(e) => {
                  setExcerpt(e.target.value)
                  triggerAutoSave()
                }}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none resize-y"
              />
            </div>

            {/* 記事本文 */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">
                記事本文 (Markdown)
              </label>
              <textarea
                value={bodyMarkdown}
                onChange={(e) => {
                  setBodyMarkdown(e.target.value)
                  triggerAutoSave()
                }}
                rows={15}
                className="w-full border border-gray-300 rounded-md p-3 font-mono text-sm focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none resize-y"
                placeholder="Markdown形式で記事本文を入力..."
              />
            </div>
          </div>
        )}

        {/* SNS tab */}
        {activeTab === 'sns' && (
          <div className="space-y-4">
            {/* X Post 1 */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">
                X投稿案 1
                <span className="ml-2 text-xs text-[#67737e]">{xPost1.length}/280</span>
              </label>
              <textarea
                value={xPost1}
                onChange={(e) => {
                  setXPost1(e.target.value)
                  triggerAutoSave()
                }}
                rows={4}
                className={`w-full px-3 py-2 border rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none resize-y ${
                  xPost1.length > 280 ? 'border-red-400' : 'border-gray-300'
                }`}
              />
            </div>

            {/* X Post 2 */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">
                X投稿案 2
                <span className="ml-2 text-xs text-[#67737e]">{xPost2.length}/280</span>
              </label>
              <textarea
                value={xPost2}
                onChange={(e) => {
                  setXPost2(e.target.value)
                  triggerAutoSave()
                }}
                rows={4}
                className={`w-full px-3 py-2 border rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none resize-y ${
                  xPost2.length > 280 ? 'border-red-400' : 'border-gray-300'
                }`}
              />
            </div>

            <hr className="my-4" />

            {/* News Post */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">ニュース投稿</label>
              <textarea
                value={newsPost}
                onChange={(e) => {
                  setNewsPost(e.target.value)
                  triggerAutoSave()
                }}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none resize-y"
              />
            </div>

            {/* Luna Post A */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">Luna投稿A</label>
              <textarea
                value={lunaPostA}
                onChange={(e) => {
                  setLunaPostA(e.target.value)
                  triggerAutoSave()
                }}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none resize-y"
              />
            </div>

            {/* Luna Post B */}
            <div>
              <label className="block text-sm font-medium text-[#292929] mb-1">Luna投稿B</label>
              <textarea
                value={lunaPostB}
                onChange={(e) => {
                  setLunaPostB(e.target.value)
                  triggerAutoSave()
                }}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-base focus:ring-2 focus:ring-[#292929] focus:border-transparent outline-none resize-y"
              />
            </div>
          </div>
        )}

        {/* Preview tab */}
        {activeTab === 'preview' && (
          <div className="bg-white rounded-lg p-4">
            <h1 className="text-2xl font-bold text-[#292929] mb-4">{title}</h1>
            {excerpt && <p className="text-[#67737e] mb-4">{excerpt}</p>}
            <p className="text-sm text-[#67737e]">
              品質スコア: {article.qualityScore ?? '-'} / 100
            </p>
            {article.sourceUrl && (
              <p className="text-sm text-[#67737e] mt-2">
                ソース: <a href={article.sourceUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">{article.sourceUrl}</a>
              </p>
            )}
            {article.researchReport && (
              <div className="mt-4 p-3 bg-gray-50 rounded text-sm text-[#292929] whitespace-pre-wrap">
                <strong>リサーチレポート:</strong>
                <p className="mt-1">{article.researchReport}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Fixed bottom bar (PublishBar) */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg z-50">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="text-xs text-[#67737e]">
            <span className="mr-3">品質: {article.qualityScore ?? '-'}</span>
            {saving && <span className="text-yellow-600">保存中...</span>}
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => handleSave(false)}
              disabled={saving}
              className="px-4 py-2 text-sm font-medium text-[#292929] bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors disabled:opacity-50"
            >
              {saving ? '保存中...' : '💾 下書き保存'}
            </button>
            <button
              onClick={handlePublish}
              disabled={publishing}
              className="px-4 py-2 text-sm font-medium text-white bg-[#292929] hover:bg-[#444] rounded-lg transition-colors disabled:opacity-50"
            >
              {publishing ? '公開中...' : '🚀 公開する'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
