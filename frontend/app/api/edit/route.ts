import {NextRequest, NextResponse} from 'next/server'
import {createClient} from '@sanity/client'
import crypto from 'crypto'

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
      const patch = sanityClient.patch(draftId)

      if (data.title !== undefined) patch.set({title: data.title})
      if (data.body !== undefined) patch.set({body: data.body})
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
