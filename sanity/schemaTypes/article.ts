import { defineField, defineType } from 'sanity'

export default defineType({
  name: 'article',
  title: '記事',
  type: 'document',
  fields: [
    defineField({
      name: 'title',
      title: 'タイトル',
      type: 'string',
      validation: (Rule) => Rule.required().max(120),
    }),
    defineField({
      name: 'slug',
      title: 'スラッグ',
      type: 'slug',
      options: { source: 'title', maxLength: 200 },
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'publishedAt',
      title: '公開日時',
      type: 'datetime',
    }),
    defineField({
      name: 'body',
      title: '本文',
      type: 'array',
      of: [
        {
          type: 'block',
          styles: [
            { title: '通常', value: 'normal' },
            { title: '見出し2', value: 'h2' },
            { title: '見出し3', value: 'h3' },
            { title: '引用', value: 'blockquote' },
          ],
          marks: {
            decorators: [
              { title: '太字', value: 'strong' },
              { title: '斜体', value: 'em' },
            ],
            annotations: [
              {
                name: 'link',
                type: 'object',
                title: 'リンク',
                fields: [
                  { name: 'href', type: 'url', title: 'URL' },
                ],
              },
            ],
          },
          lists: [
            { title: '箇条書き', value: 'bullet' },
            { title: '番号付き', value: 'number' },
          ],
        },
        {
          type: 'image',
          options: { hotspot: true },
          fields: [
            { name: 'alt', type: 'string', title: '代替テキスト' },
            { name: 'caption', type: 'string', title: 'キャプション' },
          ],
        },
      ],
    }),
    defineField({
      name: 'excerpt',
      title: '抜粋',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'mainImage',
      title: 'アイキャッチ画像',
      type: 'image',
      options: { hotspot: true },
      fields: [
        { name: 'alt', type: 'string', title: '代替テキスト' },
      ],
    }),
    defineField({
      name: 'imageCredit',
      title: '画像クレジット',
      type: 'string',
    }),
    defineField({
      name: 'seo',
      title: 'SEO',
      type: 'object',
      fields: [
        { name: 'metaTitle', type: 'string', title: 'メタタイトル' },
        { name: 'metaDescription', type: 'text', title: 'メタディスクリプション', rows: 3 },
        { name: 'ogImage', type: 'image', title: 'OG画像' },
      ],
    }),
    defineField({
      name: 'author',
      title: '著者 / 編集者',
      type: 'reference',
      to: [{ type: 'author' }],
      description: '記事を作成・監修した担当者（E-E-A-T対応）',
    }),
    defineField({
      name: 'sources',
      title: '参考・引用元 (E-E-A-T SOURCES)',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            {
              name: 'title',
              title: '参照元タイトル',
              type: 'string',
              validation: (Rule) => Rule.required(),
            },
            {
              name: 'url',
              title: '参照元URL',
              type: 'url',
            },
          ],
          preview: {
            select: {
              title: 'title',
              subtitle: 'url',
            },
          },
        },
      ],
      description: 'AIと読者に対し「どこから情報を得たか」を示すためのリスト。',
    }),
    defineField({
      name: 'category',
      title: 'カテゴリ',
      type: 'reference',
      to: [{ type: 'category' }],
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'tags',
      title: 'タグ',
      type: 'array',
      of: [{ type: 'reference', to: [{ type: 'tag' }] }],
    }),
    defineField({
      name: 'artistTags',
      title: 'アーティストタグ',
      type: 'array',
      of: [{ type: 'string' }],
      options: { layout: 'tags' },
    }),
    defineField({
      name: 'highlights',
      title: 'ハイライト（CHECKPOINT）',
      type: 'array',
      of: [{ type: 'string' }],
      description: 'AI生成の記事要点リスト。記事上部にCHECKPOINTとして表示されます。',
    }),
    defineField({
      name: 'qualityScore',
      title: '品質スコア',
      type: 'number',
      validation: (Rule) => Rule.min(0).max(100),
    }),
    defineField({
      name: 'viewCount',
      title: 'PV数',
      type: 'number',
      description: 'GA4アクセスデータから自動更新（手動変更不要）',
      readOnly: true,
      hidden: true,
    }),
    defineField({
      name: 'xPost1',
      title: 'X投稿案1',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'xPost2',
      title: 'X投稿案2',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'newsPost',
      title: 'ニュース投稿',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'lunaPostA',
      title: 'Luna投稿A',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'lunaPostB',
      title: 'Luna投稿B',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'sourceUrl',
      title: 'ソースURL',
      type: 'url',
    }),
    defineField({
      name: 'researchReport',
      title: 'リサーチレポート',
      type: 'text',
      rows: 5,
    }),
  ],
  preview: {
    select: {
      title: 'title',
      media: 'mainImage',
      category: 'category.title',
      authorName: 'author.name',
      publishedAt: 'publishedAt',
    },
    prepare({ title, media, category, authorName, publishedAt }) {
      const date = publishedAt ? new Date(publishedAt).toLocaleDateString('ja-JP') : '下書き'
      const meta = [category || '未分類', authorName, date].filter(Boolean).join(' | ')
      return {
        title,
        subtitle: meta,
        media,
      }
    },
  },
  orderings: [
    {
      title: '公開日（新しい順）',
      name: 'publishedAtDesc',
      by: [{ field: 'publishedAt', direction: 'desc' }],
    },
  ],
})
