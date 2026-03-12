import {NextRequest, NextResponse} from 'next/server'
import {createClient} from '@sanity/client'
import crypto from 'crypto'

// ---------------------------------------------------------------------------
// Markdown → Portable Text converter (mirrors Python portable_text_builder.py)
// ---------------------------------------------------------------------------

function generateKey(): string {
  return crypto.randomBytes(6).toString('hex')
}

interface Span {
  _type: 'span'
  _key: string
  text: string
  marks: string[]
}

interface MarkDef {
  _key: string
  _type: string
  href?: string
}

function parseInlineMarks(text: string): {spans: Span[]; markDefs: MarkDef[]} {
  const spans: Span[] = []
  const markDefs: MarkDef[] = []

  // Combined regex: links, bold, italic, plain text
  const pattern = /\[([^\]]+)\]\(([^)]+)\)|\*\*(.+?)\*\*|\*(.+?)\*|([^*\[]+)/g
  let match: RegExpExecArray | null

  while ((match = pattern.exec(text)) !== null) {
    const [, linkText, linkUrl, boldText, italicText, plainText] = match
    if (linkText && linkUrl) {
      const key = generateKey()
      markDefs.push({_key: key, _type: 'link', href: linkUrl})
      spans.push({_type: 'span', _key: generateKey(), text: linkText, marks: [key]})
    } else if (boldText) {
      spans.push({_type: 'span', _key: generateKey(), text: boldText, marks: ['strong']})
    } else if (italicText) {
      spans.push({_type: 'span', _key: generateKey(), text: italicText, marks: ['em']})
    } else if (plainText) {
      spans.push({_type: 'span', _key: generateKey(), text: plainText, marks: []})
    }
  }

  if (spans.length === 0) {
    spans.push({_type: 'span', _key: generateKey(), text, marks: []})
  }

  return {spans, markDefs}
}

function makeBlock(
  text: string,
  style: string = 'normal',
  listItem?: string,
  level?: number,
): Record<string, unknown> {
  const {spans, markDefs} = parseInlineMarks(text)
  const block: Record<string, unknown> = {
    _type: 'block',
    _key: generateKey(),
    style,
    children: spans,
    markDefs,
  }
  if (listItem) {
    block.listItem = listItem
    block.level = level ?? 1
  }
  return block
}

function markdownToPortableText(markdown: string): Record<string, unknown>[] {
  if (!markdown) return []

  const blocks: Record<string, unknown>[] = []
  const lines = markdown.split('\n')
  let i = 0

  while (i < lines.length) {
    const stripped = lines[i].trim()

    // empty line
    if (!stripped) {
      i++
      continue
    }

    // h3
    if (stripped.startsWith('### ')) {
      blocks.push(makeBlock(stripped.slice(4).trim(), 'h3'))
      i++
      continue
    }
    // h2
    if (stripped.startsWith('## ')) {
      blocks.push(makeBlock(stripped.slice(3).trim(), 'h2'))
      i++
      continue
    }
    // h1 → h2
    if (stripped.startsWith('# ')) {
      blocks.push(makeBlock(stripped.slice(2).trim(), 'h2'))
      i++
      continue
    }

    // blockquote
    if (stripped.startsWith('> ')) {
      blocks.push(makeBlock(stripped.slice(2).trim(), 'blockquote'))
      i++
      continue
    }

    // unordered list
    if (/^[-*+]\s+/.test(stripped)) {
      blocks.push(makeBlock(stripped.replace(/^[-*+]\s+/, ''), 'normal', 'bullet'))
      i++
      continue
    }

    // ordered list
    if (/^\d+\.\s+/.test(stripped)) {
      blocks.push(makeBlock(stripped.replace(/^\d+\.\s+/, ''), 'normal', 'number'))
      i++
      continue
    }

    // horizontal rule — skip
    if (/^---+$/.test(stripped) || /^\*\*\*+$/.test(stripped)) {
      i++
      continue
    }

    // normal paragraph — collect consecutive non-empty lines
    const paragraphLines = [stripped]
    i++
    while (
      i < lines.length &&
      lines[i].trim() &&
      !lines[i].trim().startsWith('#') &&
      !lines[i].trim().startsWith('> ') &&
      !/^[-*+]\s+/.test(lines[i].trim()) &&
      !/^\d+\.\s+/.test(lines[i].trim()) &&
      !/^---+$/.test(lines[i].trim())
    ) {
      paragraphLines.push(lines[i].trim())
      i++
    }
    blocks.push(makeBlock(paragraphLines.join('\n')))
  }

  return blocks
}

// ---------------------------------------------------------------------------
// Portable Text → Markdown converter (for editor display)
// ---------------------------------------------------------------------------

function portableTextToMarkdown(blocks: unknown[]): string {
  if (!Array.isArray(blocks)) return ''

  const lines: string[] = []

  for (const block of blocks) {
    const b = block as Record<string, unknown>
    if (b._type === 'image') {
      const alt = (b.alt as string) || ''
      // Try to reconstruct image URL from asset ref
      const asset = b.asset as Record<string, unknown> | undefined
      if (asset?._ref) {
        const ref = asset._ref as string
        // image-<id>-<w>x<h>-<ext> → https://cdn.sanity.io/images/3pe6cvt2/production/<id>-<w>x<h>.<ext>
        const parts = ref.replace(/^image-/, '').replace(/-([^-]+)$/, '.$1')
        lines.push(`![${alt}](https://cdn.sanity.io/images/3pe6cvt2/production/${parts})`)
      } else {
        lines.push(`![${alt}]()`)
      }
      lines.push('')
      continue
    }

    if (b._type !== 'block') continue

    const style = (b.style as string) || 'normal'
    const children = (b.children as Array<Record<string, unknown>>) || []
    const markDefs = (b.markDefs as Array<Record<string, unknown>>) || []
    const listItem = b.listItem as string | undefined

    // Reconstruct text with inline marks
    let text = ''
    for (const child of children) {
      if (child._type !== 'span') continue
      let t = child.text as string
      const marks = (child.marks as string[]) || []
      for (const mark of marks) {
        if (mark === 'strong') {
          t = `**${t}**`
        } else if (mark === 'em') {
          t = `*${t}*`
        } else {
          // annotation (link etc.)
          const def = markDefs.find((d) => d._key === mark)
          if (def && def._type === 'link' && def.href) {
            t = `[${t}](${def.href})`
          }
        }
      }
      text += t
    }

    if (style === 'h2') {
      lines.push(`## ${text}`)
    } else if (style === 'h3') {
      lines.push(`### ${text}`)
    } else if (style === 'blockquote') {
      lines.push(`> ${text}`)
    } else if (listItem === 'bullet') {
      lines.push(`- ${text}`)
    } else if (listItem === 'number') {
      lines.push(`1. ${text}`)
    } else {
      lines.push(text)
    }
    lines.push('')
  }

  return lines.join('\n').replace(/\n{3,}/g, '\n\n').trim()
}

const sanityClient = createClient({
  projectId: '3pe6cvt2',
  dataset: 'production',
  apiVersion: '2024-01-01',
  token: process.env.SANITY_API_TOKEN,
  useCdn: false,
})

function verifyToken(draftId: string, token: string): boolean {
  const secret = process.env.EDIT_SECRET
  if (!secret) return false
  const expected = crypto
    .createHmac('sha256', secret)
    .update(draftId)
    .digest('hex')
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(token))
}

// GET: Fetch draft data for editing
export async function GET(request: NextRequest) {
  const {searchParams} = request.nextUrl
  const id = searchParams.get('id')
  const token = searchParams.get('token')

  if (!id || !token) {
    return NextResponse.json({error: 'Missing id or token'}, {status: 400})
  }

  if (!verifyToken(id, token)) {
    return NextResponse.json({error: 'Invalid token'}, {status: 401})
  }

  try {
    // Try drafts.{id} first, then {id}
    const draftId = id.startsWith('drafts.') ? id : `drafts.${id}`
    let article = await sanityClient.fetch(
      `*[_id == $draftId][0]{
        _id, title, slug, body, excerpt, mainImage, imageCredit,
        seo, "category": category->{_id, title, slug, color},
        "tags": tags[]->{_id, title, slug},
        artistTags, qualityScore, xPost1, xPost2,
        newsPost, lunaPostA, lunaPostB, sourceUrl, researchReport
      }`,
      {draftId}
    )

    if (!article) {
      // Try without drafts. prefix
      const plainId = id.replace(/^drafts\./, '')
      article = await sanityClient.fetch(
        `*[_id == $plainId][0]{
          _id, title, slug, body, excerpt, mainImage, imageCredit,
          seo, "category": category->{_id, title, slug, color},
          "tags": tags[]->{_id, title, slug},
          artistTags, qualityScore, xPost1, xPost2,
          newsPost, lunaPostA, lunaPostB, sourceUrl, researchReport
        }`,
        {plainId}
      )
    }

    if (!article) {
      return NextResponse.json({error: 'Article not found'}, {status: 404})
    }

    // Convert body (Portable Text) → bodyMarkdown for the editor textarea
    if (Array.isArray(article.body)) {
      article.bodyMarkdown = portableTextToMarkdown(article.body)
    }

    // Also fetch categories for the dropdown
    const categories = await sanityClient.fetch(
      `*[_type == "category"]{_id, title, slug, color}`
    )

    return NextResponse.json({article, categories})
  } catch (err: any) {
    return NextResponse.json({error: err.message}, {status: 500})
  }
}

// POST: Save or publish draft
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const {id, token, action, data} = body

    if (!id || !token) {
      return NextResponse.json({error: 'Missing id or token'}, {status: 400})
    }

    if (!verifyToken(id, token)) {
      return NextResponse.json({error: 'Invalid token'}, {status: 401})
    }

    const draftId = id.startsWith('drafts.') ? id : `drafts.${id}`
    const publishId = id.replace(/^drafts\./, '')

    if (action === 'publish') {
      // Get the current draft
      const draft = await sanityClient.fetch(`*[_id == $draftId][0]`, {draftId})
      if (!draft) {
        return NextResponse.json({error: 'Draft not found'}, {status: 404})
      }

      // Create or replace published version
      const {_id, _rev, _updatedAt, _createdAt, ...docData} = draft
      await sanityClient
        .transaction()
        .createOrReplace({
          ...docData,
          _id: publishId,
          publishedAt: docData.publishedAt || new Date().toISOString(),
        })
        .delete(draftId)
        .commit()

      return NextResponse.json({
        success: true,
        action: 'published',
        slug: draft.slug?.current,
      })
    }

    // Save (update draft)
    if (data) {
      // Ensure draft exists before patching (published articles have no draft)
      const existingDraft = await sanityClient.fetch(`*[_id == $draftId][0]{_id}`, {draftId})
      if (!existingDraft) {
        // Copy published document to create a draft
        const published = await sanityClient.fetch(`*[_id == $publishId][0]`, {publishId})
        if (published) {
          const {_id, _rev, _updatedAt, _createdAt, ...docData} = published
          await sanityClient.createIfNotExists({...docData, _id: draftId})
        }
      }

      const patch = sanityClient.patch(draftId)

      if (data.title !== undefined) patch.set({title: data.title})
      if (data.bodyMarkdown !== undefined) {
        // Convert Markdown → Portable Text before saving to body field
        const portableTextBody = markdownToPortableText(data.bodyMarkdown)
        patch.set({body: portableTextBody})
      } else if (data.body !== undefined) {
        patch.set({body: data.body})
      }
      if (data.excerpt !== undefined) patch.set({excerpt: data.excerpt})
      if (data.imageCredit !== undefined) patch.set({imageCredit: data.imageCredit})
      if (data.xPost1 !== undefined) patch.set({xPost1: data.xPost1})
      if (data.xPost2 !== undefined) patch.set({xPost2: data.xPost2})
      if (data.newsPost !== undefined) patch.set({newsPost: data.newsPost})
      if (data.lunaPostA !== undefined) patch.set({lunaPostA: data.lunaPostA})
      if (data.lunaPostB !== undefined) patch.set({lunaPostB: data.lunaPostB})
      if (data.artistTags !== undefined) patch.set({artistTags: data.artistTags})
      if (data.categoryId !== undefined) {
        patch.set({category: {_type: 'reference', _ref: data.categoryId}})
      }
      if (data.seo !== undefined) patch.set({seo: data.seo})

      await patch.commit()
    }

    return NextResponse.json({success: true, action: 'saved'})
  } catch (err: any) {
    return NextResponse.json({error: err.message}, {status: 500})
  }
}
