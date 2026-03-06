// seed-categories.ts
// Usage: npx tsx seed-categories.ts
// Requires: SANITY_API_TOKEN environment variable

import {createClient} from '@sanity/client'

const client = createClient({
  projectId: '3pe6cvt2',
  dataset: 'production',
  apiVersion: '2024-01-01',
  token: process.env.SANITY_API_TOKEN,
  useCdn: false,
})

const categories = [
  {title: 'アーティスト', slug: 'artist', color: '#E53935', description: 'K-POPアーティストの最新ニュース'},
  {title: 'ビューティー', slug: 'beauty', color: '#8E24AA', description: '韓国コスメ・美容トレンド'},
  {title: 'ファッション', slug: 'fashion', color: '#1E88E5', description: '韓国ファッション最新トレンド'},
  {title: 'グルメ', slug: 'gourmet', color: '#F4511E', description: '韓国グルメ・フード情報'},
  {title: '韓国旅行', slug: 'koreantrip', color: '#00897B', description: '韓国旅行・観光ガイド'},
  {title: 'イベント', slug: 'event', color: '#FDD835', description: 'K-POP・韓国関連イベント'},
  {title: 'トレンド', slug: 'trend', color: '#43A047', description: '韓国エンタメ・ドラマ・トレンド'},
  {title: 'ライフスタイル', slug: 'lifestyle', color: '#546E7A', description: '韓国ライフスタイル・カルチャー'},
]

async function seedCategories() {
  console.log('カテゴリデータを投入中...')

  for (const cat of categories) {
    const existing = await client.fetch(
      `*[_type == "category" && slug.current == $slug][0]`,
      {slug: cat.slug}
    )

    if (existing) {
      console.log(`  ✓ ${cat.title} (${cat.slug}) は既に存在します`)
      continue
    }

    await client.create({
      _type: 'category',
      title: cat.title,
      slug: {_type: 'slug', current: cat.slug},
      color: cat.color,
      description: cat.description,
    })
    console.log(`  ✅ ${cat.title} (${cat.slug}) を作成しました`)
  }

  console.log('カテゴリデータの投入が完了しました')
}

seedCategories().catch((err) => {
  console.error('エラー:', err.message)
  process.exit(1)
})
