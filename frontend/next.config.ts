import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.sanity.io',
      },
    ],
  },
  async redirects() {
    return [
      {
        // WordPress old URL pattern: /YYYY/MM/DD/slug/
        source: '/:year(\\d{4})/:month(\\d{2})/:day(\\d{2})/:slug',
        destination: '/articles/:slug',
        permanent: true,
      },
      {
        // WordPress old URL pattern: /notes/slug
        source: '/notes/:slug',
        destination: '/articles/:slug',
        permanent: true,
      },
    ]
  },
}

export default nextConfig
