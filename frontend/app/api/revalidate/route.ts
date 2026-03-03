import {revalidatePath} from 'next/cache'
import {NextRequest, NextResponse} from 'next/server'
import {parseBody} from 'next-sanity/webhook'

export async function POST(request: NextRequest) {
  try {
    const {isValidSignature, body} = await parseBody<{
      _type: string
      slug?: {current?: string}
    }>(request, process.env.SANITY_WEBHOOK_SECRET)

    if (!isValidSignature) {
      return NextResponse.json({message: 'Invalid signature'}, {status: 401})
    }

    if (!body?._type) {
      return NextResponse.json({message: 'Missing body type'}, {status: 400})
    }

    // Revalidate specific article if slug is provided
    if (body._type === 'article' && body.slug?.current) {
      revalidatePath(`/articles/${body.slug.current}`)
    }

    // Also revalidate the homepage and category pages
    revalidatePath('/')
    revalidatePath('/category/[slug]', 'page')

    return NextResponse.json({revalidated: true, now: Date.now()})
  } catch (err) {
    return NextResponse.json({message: 'Error revalidating'}, {status: 500})
  }
}
