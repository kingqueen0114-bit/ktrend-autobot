export const endpoints = {
    data: {
        export: (dataset, documentTypes) => ({
            global: false,
            method: 'GET',
            path: `/data/export/${dataset}`,
            searchParams: documentTypes && documentTypes?.length > 0 ? [['types', documentTypes.join(',')]] : [],
        }),
        mutate: (dataset, options) => {
            const params = [
                options?.tag && ['tag', options.tag],
                options?.returnIds && ['returnIds', 'true'],
                options?.returnDocuments && ['returnDocuments', 'true'],
                options?.autoGenerateArrayKeys && ['autoGenerateArrayKeys', 'true'],
                options?.visibility && ['visibility', options.visibility],
                options?.dryRun && ['dryRun', 'true'],
            ].filter(Boolean);
            return {
                global: false,
                method: 'POST',
                path: `/data/mutate/${dataset}`,
                searchParams: params,
            };
        },
        query: (dataset) => ({
            global: false,
            method: 'GET',
            path: `/query/${dataset}`,
            searchParams: [['perspective', 'raw']],
        }),
    },
    users: {
        me: () => ({
            global: true,
            method: 'GET',
            path: '/users/me',
            searchParams: [],
        }),
    },
};
//# sourceMappingURL=endpoints.js.map