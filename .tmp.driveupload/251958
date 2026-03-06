import type { ImportOptions, ImportResult, SanityDocument } from './types.js';
interface ImportersContext {
    fromStream: (stream: NodeJS.ReadableStream, options: ImportOptions, importers: ImportersContext) => Promise<ImportResult>;
    fromArray: (documents: SanityDocument[], options: ImportOptions) => Promise<ImportResult>;
    fromFolder: (fromDir: string, options: ImportOptions & {
        deleteOnComplete?: boolean;
    }, importers: ImportersContext) => Promise<ImportResult>;
}
export declare function importFromStream(stream: NodeJS.ReadableStream, options: ImportOptions, importers: ImportersContext): Promise<ImportResult>;
export {};
//# sourceMappingURL=importFromStream.d.ts.map