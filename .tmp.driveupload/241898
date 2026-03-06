type SupportedMethod = 'GET' | 'POST';
export type Endpoint = {
    global: boolean;
    method: SupportedMethod;
    path: `/${string}`;
    searchParams: [param: string, value: string][];
};
export declare const endpoints: {
    data: {
        export: (dataset: string, documentTypes?: string[]) => Endpoint;
        mutate: (dataset: string, options?: {
            autoGenerateArrayKeys?: boolean;
            dryRun?: boolean;
            returnDocuments?: boolean;
            returnIds?: boolean;
            tag?: string;
            visibility?: "async" | "deferred" | "sync";
        }) => Endpoint;
        query: (dataset: string) => Endpoint;
    };
    users: {
        me: () => Endpoint;
    };
};
export {};
//# sourceMappingURL=endpoints.d.ts.map