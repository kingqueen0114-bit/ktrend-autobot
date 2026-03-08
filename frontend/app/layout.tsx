import type { Metadata } from 'next'
import { Noto_Sans_JP, Encode_Sans_Condensed } from 'next/font/google'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import ScrollToTop from '@/components/ScrollToTop'
import SwipeNavigator from '@/components/SwipeNavigator'
import GoogleAnalytics from '@/components/GoogleAnalytics'
import Script from 'next/script'
import './globals.css'

const notoSansJP = Noto_Sans_JP({
  subsets: ['latin'],
  variable: '--font-noto-sans-jp',
  display: 'swap',
})

const encodeSans = Encode_Sans_Condensed({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-encode-sans',
  display: 'swap',
})

export const metadata: Metadata = {
  title: {
    default: 'K-TREND TIMES | 韓国トレンド情報メディア',
    template: '%s | K-TREND TIMES',
  },
  description: '韓国エンタメ・K-POP・ビューティー・ファッションの最新トレンドをお届けするニュースメディア',
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL || 'https://k-trendtimes.com'),
  icons: {
    icon: '/favicon.png',
    apple: '/favicon.png',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja" className={`${notoSansJP.variable} ${encodeSans.variable}`}>
      <body className="font-sans bg-white text-[#292929] antialiased">
        <GoogleAnalytics />
        {process.env.NEXT_PUBLIC_ADSENSE_ID && (
          <Script
            async
            src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
            crossOrigin="anonymous"
            strategy="afterInteractive"
          />
        )}
        <Header />
        <main className="min-h-screen pagead-ignore">
          <SwipeNavigator>{children}</SwipeNavigator>
        </main>
        <Footer />
        <ScrollToTop />
      </body>
    </html>
  )
}
