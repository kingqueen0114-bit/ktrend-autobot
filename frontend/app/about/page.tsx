import type { Metadata } from 'next'
import Link from 'next/link'
import JsonLd from '@/components/JsonLd'

const SITE_NAME = 'K-TREND TIMES'
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.k-trendtimes.com'

export const metadata: Metadata = {
    title: `運営者情報（About Us） | ${SITE_NAME}`,
    description: `${SITE_NAME}の運営目的、編集方針、および運営者に関する情報です。`,
    openGraph: {
        title: `運営者情報（About Us） | ${SITE_NAME}`,
        type: 'website',
        url: `${SITE_URL}/about`,
        siteName: SITE_NAME,
    },
}

export default function AboutPage() {
    const breadcrumb = {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: [
            {
                '@type': 'ListItem',
                position: 1,
                name: 'ホーム',
                item: SITE_URL,
            },
            {
                '@type': 'ListItem',
                position: 2,
                name: '運営者情報',
                item: `${SITE_URL}/about`,
            },
        ],
    }

    const aboutJsonLd = {
        '@context': 'https://schema.org',
        '@type': 'AboutPage',
        mainEntity: {
            '@type': 'Organization',
            name: SITE_NAME,
            url: SITE_URL,
            description: '韓国エンタメ・K-POP・ビューティー・ファッションの最新トレンドをお届けするニュースメディア',
        },
    }

    return (
        <>
            <JsonLd data={breadcrumb} />
            <JsonLd data={aboutJsonLd} />

            <main className="max-w-4xl mx-auto px-4 py-12 md:py-20">
                <nav aria-label="パンくずリスト" className="mb-8">
                    <ol className="flex items-center gap-2 text-sm text-[#67737e]">
                        <li>
                            <Link href="/" className="hover:text-[#292929] transition-colors">
                                ホーム
                            </Link>
                        </li>
                        <li aria-hidden="true">&gt;</li>
                        <li className="font-bold text-[#292929]">運営者情報</li>
                    </ol>
                </nav>

                <h1 className="text-3xl md:text-4xl font-bold text-[#292929] mb-10 pb-4 border-b-2 border-[#292929]">
                    運営者情報 (About Us)
                </h1>

                <div className="prose-custom max-w-none space-y-12 text-[#292929] leading-relaxed">
                    <section>
                        <h2 className="text-2xl font-bold mb-6 pb-2 border-b border-gray-200">
                            K-TREND TIMESについて
                        </h2>
                        <p className="mb-4">
                            K-TREND TIMESは、刻一刻と変化する韓国のカルチャー・エンターテインメント・ビューティー・ファッションに関する「今いちばん知りたい最新トレンド」を、日本の皆様へいち早く、そして正確にお届けするニュースメディアです。
                        </p>
                        <p>
                            SNSの最新バイラル情報から、現地発の確かなプレスリリースまで、編集部独自の視点でキュレーションした質の高いコンテンツを提供し、韓国カルチャーを愛するすべての人々の情報プラットフォームとなることを目指しています。
                        </p>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold mb-6 pb-2 border-b border-gray-200">
                            コンテンツ編集方針 (Editorial Policy)
                        </h2>
                        <ul className="list-disc pl-6 space-y-4">
                            <li>
                                <strong>情報の正確性と一次ソースの重視</strong>
                                <br />
                                単なる噂や不確実な情報ではなく、公式発表や信頼できる一次ソース（参照元）に基づいた記事執筆を徹底し、記事内にて出典を明示します。
                            </li>
                            <li>
                                <strong>多様な視点と専門性</strong>
                                <br />
                                K-POP、韓国コスメ、ソウル現地情報など、それぞれの分野に精通した専門ライターおよび編集者がコンテンツの制作・監修を行っています。
                            </li>
                            <li>
                                <strong>読者ファーストのUI/UX</strong>
                                <br />
                                スマートフォンからでも読みやすく、知りたい結論（Q&A）に素早くアクセスできるよう、AI技術も活用した分かりやすい要約と見出し構成を心がけています。
                            </li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold mb-6 pb-2 border-b border-gray-200">
                            運営基本情報
                        </h2>
                        <div className="bg-gray-50 rounded-lg p-6 md:p-8">
                            <dl className="grid grid-cols-1 md:grid-cols-[200px_1fr] gap-4 md:gap-6">
                                <dt className="font-bold text-[#67737e] md:text-right">メディア名</dt>
                                <dd className="font-medium text-[#292929]">K-TREND TIMES</dd>

                                <dt className="font-bold text-[#67737e] md:text-right">URL</dt>
                                <dd>
                                    <a href="https://www.k-trendtimes.com" className="text-[#1E88E5] hover:underline hover:opacity-80 transition-opacity">
                                        https://www.k-trendtimes.com
                                    </a>
                                </dd>

                                <dt className="font-bold text-[#67737e] md:text-right">お問い合わせ</dt>
                                <dd>
                                    <Link href="/contact" className="text-[#1E88E5] hover:underline hover:opacity-80 transition-opacity">
                                        お問い合わせフォームはこちら
                                    </Link>
                                </dd>
                            </dl>
                        </div>
                    </section>
                </div>
            </main>
        </>
    )
}
