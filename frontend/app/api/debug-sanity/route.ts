import { NextResponse } from 'next/server'
import { client } from '@/lib/sanity'
import { articlesQuery } from '@/lib/queries'

// Bypass standard caching for this debug endpoint
export const dynamic = 'force-dynamic'

export async function GET() {
    try {
        const start = Date.now()
        const articles = await client.fetch(articlesQuery, { limit: 30 })
        const durationMs = Date.now() - start

        return NextResponse.json({
            success: true,
            durationMs,
            articlesCount: articles?.length || 0,
            projectId: client.config().projectId,
            dataset: client.config().dataset,
            useCdn: client.config().useCdn,
            articles: articles,
        })
    } catch (error: any) {
        return NextResponse.json({
            success: false,
            error: error.message,
        }, { status: 500 })
    }
}
