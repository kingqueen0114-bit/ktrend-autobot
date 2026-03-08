import { NextResponse } from 'next/server'
import { client } from '@/lib/sanity'
import { articleCategorySlugQuery } from '@/lib/queries'

export async function GET(
    request: Request,
    { params }: { params: { slug: string } }
) {
    try {
        const slug = params.slug
        if (!slug) {
            return NextResponse.json({ categorySlug: null }, { status: 400 })
        }

        const res = await client.fetch(articleCategorySlugQuery, { slug })
        return NextResponse.json({ categorySlug: res?.categorySlug || null })
    } catch (error) {
        console.error('Error fetching article category by slug API:', error)
        return NextResponse.json({ categorySlug: null }, { status: 500 })
    }
}
