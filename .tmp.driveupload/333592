import {defineField, defineType} from 'sanity'

export default defineType({
  name: 'category',
  title: 'カテゴリ',
  type: 'document',
  fields: [
    defineField({
      name: 'title',
      title: 'タイトル',
      type: 'string',
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'slug',
      title: 'スラッグ',
      type: 'slug',
      options: {source: 'title', maxLength: 96},
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'description',
      title: '説明',
      type: 'text',
      rows: 2,
    }),
    defineField({
      name: 'color',
      title: 'テーマカラー',
      type: 'string',
      description: 'HEXカラーコード（例: #E53935）',
      validation: (Rule) => Rule.regex(/^#[0-9A-Fa-f]{6}$/).error('有効なHEXカラーコードを入力してください'),
    }),
  ],
  preview: {
    select: {
      title: 'title',
      color: 'color',
    },
    prepare({title, color}) {
      return {
        title,
        subtitle: color || 'カラー未設定',
      }
    },
  },
})
