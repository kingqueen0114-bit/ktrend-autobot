/**
 * WordPress → Sanity データ移行スクリプト
 *
 * Usage:
 *   cd migration && npm install
 *   SANITY_API_TOKEN=xxx WP_URL=https://k-trendtimes.com npm run migrate
 */

import {createClient} from '@sanity/client'
import {JSDOM} from 'jsdom'

const WP_URL = process.env.WP_URL || 'https://k-trendtimes.com'
const SANITY_PROJECT_ID = process.env.SANITY_PROJECT_ID || '3pe6cvt2'
const SANITY_DATASET = process.env.SANITY_DATASET || 'production'
const LIMIT = parseInt(process.env.LIMIT || '0')

const sanityClient = createClient({
  projectId: SANITY_PROJECT_ID,
  dataset: SANITY_DATASET,
  apiVersion: '2024-01-01',
  token: process.env.SANITY_API_TOKEN,
  useCdn: false,
})

// WordPress category ID → Sanity category slug mapping
const WP_CAT_MAP: Record<number, string> = {
  11: 'artist',
  7: 'beauty',
  10: 'fashion',
  6: 'gourmet',
  4: 'koreantrip',
  5: 'event',
  3: 'trend',
  2: 'trend',
  8: 'trend',
  9: 'lifestyle',
}

function decodeHtmlEntities(text: string): string {
  return text
    .replace(/&#8211;/g, '\u2013')
    .replace(/&#8212;/g, '\u2014')
    .replace(/&#8216;/g, '\u2018')
    .replace(/&#8217;/g, '\u2019')
    .replace(/&#8220;/g, '\u201C')
    .replace(/&#8221;/g, '\u201D')
    .replace(/&#038;/g, '&')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&nbsp;/g, ' ')
}

// Cache for category refs
const categoryRefCache: Record<string, string> = {}

async function getCategoryRef(slug: string): Promise<string> {
  if (categoryRefCache[slug]) return categoryRefCache[slug]

  const result = await sanityClient.fetch(
    `*[_type == "category" && slug.current == $slug][0]{_id}`,
    {slug}
  )
  if (result?._id) {
    categoryRefCache[slug] = result._id
    return result._id
  }
  return ''
}

async function getOrCreateTag(name: string): Promise<string> {
  const slug = name.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-').slice(0, 96)

  const existing = await sanityClient.fetch(
    `*[_type == "tag" && slug.current == $slug][0]{_id}`,
    {slug}
  )
  if (existing?._id) return existing._id

  const tagId = crypto.randomUUID().replace(/-/g, '')
  await sanityClient.create({
    _id: tagId,
    _type: 'tag',
    title: name,
    slug: {_type: 'slug', current: slug},
  })
  return tagId
}

async function uploadImage(imageUrl: string): Promise<{_id: string; url: string} | null> {
  try {
    const resp = await fetch(imageUrl, {
      headers: {'User-Agent': 'K-TREND-TIMES-Migration/1.0'},
    })
    if (!resp.ok) return null

    const contentType = resp.headers.get('Content-Type') || 'image/jpeg'
    if (contentType.includes('html')) return null

    const buffer = Buffer.from(await resp.arrayBuffer())
    if (buffer.length < 1000) return null

    const filename = imageUrl.split('/').pop()?.split('?')[0] || 'image.jpg'
    const asset = await sanityClient.assets.upload('image', buffer, {
      filename,
      contentType,
    })

    return {_id: asset._id, url: asset.url}
  } catch (e) {
    console.warn(`  画像アップロード失敗: ${imageUrl}`, e)
    return null
  }
}

async function fetchAllWpPosts(): Promise<any[]> {
  const allPosts: any[] = []
  let page = 1
  const perPage = 50

  while (true) {
    console.log(`  WP REST API: page ${page}...`)
    const url = `${WP_URL}/wp-json/wp/v2/posts?per_page=${perPage}&page=${page}&status=publish&_embed`

    try {
      const resp = await fetch(url)
      if (!resp.ok) break

      const posts = await resp.json()
      if (!Array.isArray(posts) || posts.length === 0) break

      allPosts.push(...posts)
      const totalPages = parseInt(resp.headers.get('X-WP-TotalPages') || '1')
      if (page >= totalPages) break
      page++
    } catch (e) {
      console.error(`  Fetch error at page ${page}:`, e)
      break
    }
  }

  return allPosts
}

function convertHtmlToPortableText(html: string): any[] {
  if (!html || !html.trim()) return []

  try {
    const dom = new JSDOM(html)
    const doc = dom.window.document
    const blocks: any[] = []

    function makeKey(): string {
      return crypto.randomUUID().slice(0, 12)
    }

    function extractInlineContent(el: Element): {children: any[], markDefs: any[]} {
      const children: any[] = []
      const markDefs: any[] = []

      function walk(node: Node, marks: string[]) {
        if (node.nodeType === 3) { // Text
          const text = node.textContent || ''
          if (text) {
            children.push({
              _type: 'span',
              _key: makeKey(),
              text,
              marks: [...marks],
            })
          }
        } else if (node.nodeType === 1) { // Element
          const tag = (node as Element).tagName.toLowerCase()
          let newMarks = [...marks]

          if (tag === 'strong' || tag === 'b') {
            newMarks.push('strong')
          } else if (tag === 'em' || tag === 'i') {
            newMarks.push('em')
          } else if (tag === 'a') {
            const href = (node as Element).getAttribute('href')
            if (href) {
              const markKey = makeKey()
              markDefs.push({_type: 'link', _key: markKey, href})
              newMarks.push(markKey)
            }
          } else if (tag === 'br') {
            children.push({_type: 'span', _key: makeKey(), text: '\n', marks: []})
            return
          }

          for (const child of Array.from(node.childNodes)) {
            walk(child, newMarks)
          }
        }
      }

      for (const child of Array.from(el.childNodes)) {
        walk(child, [])
      }

      if (children.length === 0) {
        children.push({_type: 'span', _key: makeKey(), text: '', marks: []})
      }
      return {children, markDefs}
    }

    function processElement(el: Element) {
      const tag = el.tagName.toLowerCase()

      if (tag === 'h2' || tag === 'h3' || tag === 'h4') {
        const {children, markDefs} = extractInlineContent(el)
        blocks.push({_type: 'block', _key: makeKey(), style: tag, children, markDefs})
      } else if (tag === 'p') {
        const {children, markDefs} = extractInlineContent(el)
        blocks.push({_type: 'block', _key: makeKey(), style: 'normal', children, markDefs})
      } else if (tag === 'blockquote') {
        const {children, markDefs} = extractInlineContent(el)
        blocks.push({_type: 'block', _key: makeKey(), style: 'blockquote', children, markDefs})
      } else if (tag === 'ul' || tag === 'ol') {
        const listStyle = tag === 'ul' ? 'bullet' : 'number'
        for (const li of Array.from(el.querySelectorAll(':scope > li'))) {
          const {children, markDefs} = extractInlineContent(li)
          blocks.push({
            _type: 'block', _key: makeKey(), style: 'normal',
            listItem: listStyle, level: 1,
            children, markDefs,
          })
        }
      } else if (tag === 'div' || tag === 'section' || tag === 'article') {
        for (const child of Array.from(el.children)) {
          processElement(child)
        }
      } else if (tag === 'figure' || tag === 'img') {
        // Skip images - they'll be handled separately if needed
      } else {
        // Fallback: treat as paragraph
        const text = el.textContent?.trim()
        if (text) {
          blocks.push({
            _type: 'block', _key: makeKey(), style: 'normal',
            children: [{_type: 'span', _key: makeKey(), text, marks: []}],
            markDefs: [],
          })
        }
      }
    }

    for (const child of Array.from(doc.body.children)) {
      processElement(child)
    }

    return blocks.length > 0 ? blocks : [{
      _type: 'block', _key: makeKey(), style: 'normal',
      children: [{_type: 'span', _key: makeKey(), text: html.replace(/<[^>]+>/g, '').trim(), marks: []}],
      markDefs: [],
    }]
  } catch (e) {
    console.warn('  HTML→PT変換失敗、プレーンテキスト化')
    const text = html.replace(/<[^>]+>/g, '').trim()
    return text ? [{
      _type: 'block', _key: crypto.randomUUID().slice(0, 12), style: 'normal',
      children: [{_type: 'span', _key: crypto.randomUUID().slice(0, 12), text, marks: []}],
      markDefs: [],
    }] : []
  }
}

async function migratePost(wpPost: any): Promise<boolean> {
  const slug = decodeURIComponent(wpPost.slug || '')

  // Check if already migrated
  const existing = await sanityClient.fetch(
    `*[_type == "article" && slug.current == $slug][0]{_id}`,
    {slug}
  )
  if (existing) {
    console.log(`  ✓ ${slug} は既に移行済み`)
    return false
  }

  // Convert HTML to Portable Text
  const htmlBody = wpPost.content?.rendered || ''
  let body: any[] = []
  body = convertHtmlToPortableText(htmlBody)

  // Upload featured image
  let mainImage: any = undefined
  const featuredUrl = wpPost._embedded?.['wp:featuredmedia']?.[0]?.source_url
  if (featuredUrl) {
    const asset = await uploadImage(featuredUrl)
    if (asset) {
      mainImage = {
        _type: 'image',
        asset: {_type: 'reference', _ref: asset._id},
        alt: wpPost.title?.rendered || '',
      }
    }
  }

  // Resolve category
  let categoryRef: any = undefined
  const wpCatIds: number[] = wpPost.categories || []
  for (const catId of wpCatIds) {
    const catSlug = WP_CAT_MAP[catId]
    if (catSlug) {
      const refId = await getCategoryRef(catSlug)
      if (refId) {
        categoryRef = {_type: 'reference', _ref: refId}
        break
      }
    }
  }

  // Resolve tags
  const tagRefs: any[] = []
  const wpTags = wpPost._embedded?.['wp:term']?.[1] || []
  for (const tag of wpTags) {
    if (tag.name) {
      const tagId = await getOrCreateTag(tag.name)
      if (tagId) {
        tagRefs.push({
          _type: 'reference',
          _ref: tagId,
          _key: crypto.randomUUID().slice(0, 12),
        })
      }
    }
  }

  // Build Sanity document
  const docId = crypto.randomUUID().replace(/-/g, '')
  const doc: any = {
    _id: docId,
    _type: 'article',
    title: decodeHtmlEntities(wpPost.title?.rendered || 'Untitled'),
    slug: {_type: 'slug', current: slug},
    publishedAt: wpPost.date || new Date().toISOString(),
    body,
    excerpt: decodeHtmlEntities(wpPost.excerpt?.rendered?.replace(/<[^>]+>/g, '').trim() || ''),
    seo: {
      metaTitle: decodeHtmlEntities(wpPost.title?.rendered || ''),
      metaDescription: decodeHtmlEntities(wpPost.excerpt?.rendered?.replace(/<[^>]+>/g, '').trim() || ''),
    },
  }

  if (mainImage) doc.mainImage = mainImage
  if (categoryRef) doc.category = categoryRef
  if (tagRefs.length > 0) doc.tags = tagRefs

  // Create in Sanity (as published, not draft)
  await sanityClient.createOrReplace(doc)
  console.log(`  ✅ ${slug} を移行しました`)
  return true
}

async function main() {
  console.log('=== WordPress → Sanity データ移行 ===\n')
  console.log(`WP URL: ${WP_URL}`)
  console.log(`Sanity: ${SANITY_PROJECT_ID} / ${SANITY_DATASET}\n`)

  // Fetch all posts from WordPress
  console.log('1. WordPress記事を取得中...')
  const posts = await fetchAllWpPosts()
  console.log(`   ${posts.length} 件の記事を取得\n`)

  const postsToMigrate = LIMIT > 0 ? posts.slice(0, LIMIT) : posts
  if (LIMIT > 0) console.log(`   テストモード: ${LIMIT} 件に制限\n`)

  // Migrate each post
  console.log('2. Sanityに移行中...')
  let migrated = 0
  let skipped = 0

  for (const post of postsToMigrate) {
    const success = await migratePost(post)
    if (success) migrated++
    else skipped++
  }

  console.log(`\n=== 移行完了 ===`)
  console.log(`移行: ${migrated} 件`)
  console.log(`スキップ: ${skipped} 件`)
  console.log(`合計: ${postsToMigrate.length} 件`)
}

main().catch((err) => {
  console.error('移行エラー:', err)
  process.exit(1)
})
