import { defineField, defineType } from 'sanity'

export default defineType({
    name: 'author',
    title: '著者 / 運営者',
    type: 'document',
    fields: [
        defineField({
            name: 'name',
            title: '名前',
            type: 'string',
            validation: (Rule) => Rule.required(),
        }),
        defineField({
            name: 'slug',
            title: 'スラッグ',
            type: 'slug',
            options: {
                source: 'name',
                maxLength: 96,
            },
            validation: (Rule) => Rule.required(),
        }),
        defineField({
            name: 'role',
            title: '役職・肩書き',
            type: 'string',
            description: '例: 編集部、K-POPライター',
        }),
        defineField({
            name: 'image',
            title: 'プロフィール画像',
            type: 'image',
            options: {
                hotspot: true,
            },
        }),
        defineField({
            name: 'bio',
            title: 'プロフィール・自己紹介',
            type: 'text',
            rows: 4,
        }),
    ],
    preview: {
        select: {
            title: 'name',
            subtitle: 'role',
            media: 'image',
        },
    },
})
