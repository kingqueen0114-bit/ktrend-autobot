import {defineField, defineType} from 'sanity'

export default defineType({
  name: 'siteSettings',
  title: 'サイト設定',
  type: 'document',
  fields: [
    defineField({
      name: 'siteName',
      title: 'サイト名',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'description',
      title: 'サイト説明',
      type: 'text',
      rows: 3,
    }),
    defineField({
      name: 'ogImage',
      title: 'デフォルトOG画像',
      type: 'image',
    }),
    defineField({
      name: 'socialLinks',
      title: 'SNSリンク',
      type: 'object',
      fields: [
        {name: 'x', type: 'url', title: 'X (Twitter)'},
        {name: 'instagram', type: 'url', title: 'Instagram'},
        {name: 'line', type: 'url', title: 'LINE'},
      ],
    }),
  ],
  preview: {
    prepare() {
      return {title: 'サイト設定'}
    },
  },
})
