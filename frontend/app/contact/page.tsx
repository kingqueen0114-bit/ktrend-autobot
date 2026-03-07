import { Metadata } from 'next'

export const metadata: Metadata = {
    title: 'お問い合わせ | K-TREND TIMES',
    description: 'K-TREND TIMESへのお問い合わせページです。記事に関するご質問や、広告掲載、プレスリリースなどはこちらからご連絡ください。',
}

export default function ContactPage() {
    return (
        <div className="max-w-4xl mx-auto px-4 py-12 md:py-20">
            <h1 className="text-3xl md:text-4xl font-bold mb-6 text-center text-gray-900 pb-4 border-b">
                お問い合わせ
            </h1>

            <div className="text-center mb-10 text-gray-600">
                <p className="mb-2">K-TREND TIMESをご覧いただきありがとうございます。</p>
                <p>
                    記事に関するご意見・ご質問、広告掲載に関するお問い合わせ、プレスリリース等の送付につきましては、<br className="hidden md:block" />
                    以下のフォームまたはメールアドレスよりご連絡ください。
                </p>
            </div>

            <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
                <form className="space-y-6">
                    <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                            お名前 <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            required
                            placeholder="山田 太郎"
                            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#1DB446] focus:border-[#1DB446] transition-colors"
                        />
                    </div>

                    <div>
                        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                            メールアドレス <span className="text-red-500">*</span>
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            required
                            placeholder="you@example.com"
                            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#1DB446] focus:border-[#1DB446] transition-colors"
                        />
                    </div>

                    <div>
                        <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-1">
                            お問い合わせ種別 <span className="text-red-500">*</span>
                        </label>
                        <select
                            id="subject"
                            name="subject"
                            required
                            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#1DB446] focus:border-[#1DB446] transition-colors bg-white"
                        >
                            <option value="">選択してください</option>
                            <option value="article">記事の内容に関するお問い合わせ</option>
                            <option value="press">プレスリリース・情報提供</option>
                            <option value="ad">広告掲載に関するお問い合わせ</option>
                            <option value="other">その他のお問い合わせ</option>
                        </select>
                    </div>

                    <div>
                        <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
                            お問い合わせ内容 <span className="text-red-500">*</span>
                        </label>
                        <textarea
                            id="message"
                            name="message"
                            rows={6}
                            required
                            placeholder="お問い合わせ内容をご記入ください"
                            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#1DB446] focus:border-[#1DB446] transition-colors resize-y"
                        ></textarea>
                    </div>

                    <div className="pt-2">
                        <p className="text-sm text-red-500 mb-4 pb-2 text-center">
                            ※現在お問い合わせフォームはメンテナンス中です。直接LINEなどでお問い合わせください。
                        </p>
                        <button
                            type="button"
                            className="w-full bg-gray-400 text-white font-bold py-4 rounded-lg transition-colors shadow-sm focus:outline-none cursor-not-allowed"
                            disabled
                        >
                            送信する
                        </button>
                    </div>
                </form>
            </div>

            <div className="mt-12 text-center text-gray-500 text-sm">
                <h3 className="font-semibold text-gray-700 mb-2">その他のお問い合わせ方法</h3>
                <p>公式LINEアカウントからも受け付けております。</p>
            </div>
        </div>
    )
}
