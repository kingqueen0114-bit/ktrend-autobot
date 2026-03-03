import {timingSafeEqual} from 'crypto'
import {draftMode} from 'next/headers'
import {redirect} from 'next/navigation'
import {NextRequest} from 'next/server'

export async function GET(request: NextRequest) {
  const {searchParams} = request.nextUrl
  const secret = searchParams.get('secret')
  const slug = searchParams.get('slug')

  const expected = process.env.PREVIEW_SECRET || ''
  const received = secret || ''
  const maxLen = Math.max(expected.length, received.length)
  const expectedBuf = Buffer.from(expected.padEnd(maxLen))
  const receivedBuf = Buffer.from(received.padEnd(maxLen))
  if (!timingSafeEqual(expectedBuf, receivedBuf)) {
    return new Response('Invalid secret', {status: 401})
  }

  if (!slug) {
    return new Response('Missing slug', {status: 400})
  }

  const draft = await draftMode()
  draft.enable()
  redirect(`/articles/${slug}`)
}
