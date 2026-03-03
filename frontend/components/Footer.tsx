import Link from 'next/link'

const categories = [
  {title: 'アーティスト', slug: 'artist'},
  {title: 'ビューティー', slug: 'beauty'},
  {title: 'ファッション', slug: 'fashion'},
  {title: 'グルメ', slug: 'gourmet'},
  {title: '韓国旅行', slug: 'koreantrip'},
  {title: 'イベント', slug: 'event'},
  {title: 'トレンド', slug: 'trend'},
  {title: 'ライフスタイル', slug: 'lifestyle'},
]

export default function Footer() {
  return (
    <footer className="bg-[#191919] text-gray-400">
      {/* SNS follow section */}
      <div className="bg-[#222222]">
        <div className="max-w-6xl mx-auto px-4 py-6 flex items-center justify-center gap-4">
          <span className="text-white text-sm font-bold uppercase tracking-wider">
            フォローする
          </span>
          <a
            href="https://x.com/ktrendtimes"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-[#f84643] transition-colors"
            aria-label="X (Twitter)"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
          </a>
        </div>
      </div>

      {/* Main footer */}
      <div className="max-w-6xl mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* About */}
          <div>
            <h3
              className="text-white text-xl font-bold mb-3"
              style={{fontFamily: "'Encode Sans Condensed', sans-serif"}}
            >
              K-TREND TIMES
            </h3>
            <p className="text-sm leading-relaxed">
              韓国エンタメ・K-POP・ビューティー・ファッションの最新トレンドをお届けするニュースメディアです。
            </p>
          </div>

          {/* Categories */}
          <div>
            <h4 className="text-white text-sm font-bold mb-3 uppercase tracking-wider">カテゴリ</h4>
            <ul className="space-y-1.5">
              {categories.map((cat) => (
                <li key={cat.slug}>
                  <Link
                    href={`/category/${cat.slug}`}
                    className="text-sm hover:text-[#f84643] transition-colors"
                  >
                    {cat.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-white text-sm font-bold mb-3 uppercase tracking-wider">リンク</h4>
            <ul className="space-y-1.5">
              <li>
                <Link href="/sitemap.xml" className="text-sm hover:text-[#f84643] transition-colors">
                  サイトマップ
                </Link>
              </li>
              <li>
                <Link href="/privacy-policy" className="text-sm hover:text-[#f84643] transition-colors">
                  プライバシーポリシー
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-sm hover:text-[#f84643] transition-colors">
                  お問い合わせ
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* Copyright */}
      <div className="border-t border-gray-800">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <p className="text-xs text-center text-gray-500">
            &copy; {new Date().getFullYear()} K-TREND TIMES. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
