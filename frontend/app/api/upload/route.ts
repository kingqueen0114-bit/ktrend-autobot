import crypto from 'crypto'
import {NextRequest, NextResponse} from 'next/server'
import {createClient} from '@sanity/client'

function verifyUploadToken(token: string): boolean {
  const secret = process.env.EDIT_SECRET
  if (!secret) return false
  const expected = crypto
    .createHmac('sha256', secret)
    .update('upload')
    .digest('hex')
  return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(token))
}

const sanityClient = createClient({
  projectId: '3pe6cvt2',
  dataset: 'production',
  apiVersion: '2024-01-01',
  token: process.env.SANITY_API_TOKEN,
  useCdn: false,
})

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File | null
    const token = formData.get('token') as string | null

    if (!file || !token) {
      return NextResponse.json({error: 'Missing file or token'}, {status: 400})
    }

    // Verify token using HMAC against EDIT_SECRET
    if (!verifyUploadToken(token)) {
      return NextResponse.json({error: 'Unauthorized'}, {status: 401})
    }

    const buffer = Buffer.from(await file.arrayBuffer())
    const asset = await sanityClient.assets.upload('image', buffer, {
      filename: file.name,
      contentType: file.type,
    })

    return NextResponse.json({
      asset: {
        _id: asset._id,
        _type: 'sanity.imageAsset',
        url: asset.url,
      },
    })
  } catch (err: any) {
    return NextResponse.json({error: err.message}, {status: 500})
  }
}
