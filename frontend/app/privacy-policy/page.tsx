import { Metadata } from 'next'

export const metadata: Metadata = {
    title: 'プライバシーポリシー | K-TREND TIMES',
    description: 'K-TREND TIMESのプライバシーポリシー（個人情報保護方針）について記載しています。',
}

export default function PrivacyPolicyPage() {
    return (
        <div className="max-w-4xl mx-auto px-4 py-12 md:py-20">
            <h1 className="text-3xl md:text-4xl font-bold mb-10 text-center text-gray-900 shadow-sm pb-4 border-b">
                プライバシーポリシー
            </h1>

            <div className="prose prose-lg max-w-none text-gray-700 space-y-8">
                <section>
                    <h2 className="text-2xl font-semibold mb-4 text-[#1DB446] border-l-4 border-[#1DB446] pl-3">
                        1. 個人情報の収集について
                    </h2>
                    <p>
                        当サイト（K-TREND TIMES）では、お問い合わせやコメントの投稿、メールマガジンの登録などの際に、名前（ハンドルネーム）、メールアドレスなどの個人情報をご登録いただく場合がございます。これらの個人情報は、質問に対する回答や必要な情報を電子メールなどでご連絡する場合に利用させていただくものであり、個人情報をご提供いただく際の目的以外では利用いたしません。
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-4 text-[#1DB446] border-l-4 border-[#1DB446] pl-3">
                        2. 個人情報の第三者への開示
                    </h2>
                    <p>当サイトでは、個人情報は適切に管理し、以下に該当する場合を除いて第三者に開示することはありません。</p>
                    <ul className="list-disc pl-6 mt-2 space-y-2">
                        <li>本人のご了解がある場合</li>
                        <li>法令等への協力のため、開示が必要となる場合</li>
                    </ul>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-4 text-[#1DB446] border-l-4 border-[#1DB446] pl-3">
                        3. 個人情報の開示、訂正、追加、削除、利用停止
                    </h2>
                    <p>
                        ご本人からの個人データの開示、訂正、追加、削除、利用停止のご希望の場合には、ご本人であることを確認させていただいた上、速やかに対応させていただきます。
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-4 text-[#1DB446] border-l-4 border-[#1DB446] pl-3">
                        4. アクセス解析ツールについて
                    </h2>
                    <p>
                        当サイトでは、Googleによるアクセス解析ツール「Googleアナリティクス」を利用しています。このGoogleアナリティクスはトラフィックデータの収集のためにCookieを使用しています。このトラフィックデータは匿名で収集されており、個人を特定するものではありません。この機能はCookieを無効にすることで収集を拒否することが出来ますので、お使いのブラウザの設定をご確認ください。
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-4 text-[#1DB446] border-l-4 border-[#1DB446] pl-3">
                        5. 広告の配信について
                    </h2>
                    <p>
                        当サイトは、第三者配信の広告サービス（Googleアドセンス等）を利用しています。広告配信事業者は、ユーザーの興味に応じた広告を表示するためにCookie（クッキー）を使用することがあります。Cookieを無効にする設定およびGoogleアドセンスに関する詳細は「広告 – ポリシーと規約 – Google」をご覧ください。
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-4 text-[#1DB446] border-l-4 border-[#1DB446] pl-3">
                        6. 免責事項
                    </h2>
                    <p>
                        当サイトからリンクやバナーなどによって他のサイトに移動された場合、移動先サイトで提供される情報、サービス等について一切の責任を負いません。<br /><br />
                        当サイトのコンテンツ・情報につきまして、可能な限り正確な情報を掲載するよう努めておりますが、誤情報が入り込んだり、情報が古くなっていることもございます。<br /><br />
                        当サイトに掲載された内容によって生じた損害等の一切の責任を負いかねますのでご了承ください。
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-4 text-[#1DB446] border-l-4 border-[#1DB446] pl-3">
                        7. プライバシーポリシーの変更について
                    </h2>
                    <p>
                        当サイトは、個人情報に関して適用される日本の法令を遵守するとともに、本ポリシーの内容を適宜見直しその改善に努めます。<br />
                        修正された最新のプライバシーポリシーは常に本ページにて開示されます。
                    </p>
                </section>
            </div>

            <div className="mt-12 pt-8 border-t border-gray-200 text-right text-sm text-gray-500">
                <p>制定日：2023年4月1日</p>
                <p>最終改定日：2026年3月8日</p>
            </div>
        </div>
    )
}
