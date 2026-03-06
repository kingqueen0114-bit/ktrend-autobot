import { type SanityDocument } from '@sanity/types';
import { type ExportAPIConfig } from '../types.js';
/**
 * @public
 */
export declare function fromExportEndpoint(options: ExportAPIConfig): Promise<import("node:stream/web").ReadableStream<any>>;
/**
 * Safe JSON parser that is able to handle lines interrupted by an error object.
 *
 * This may occur when streaming NDJSON from the Export HTTP API.
 *
 * @public
 * @see {@link https://github.com/sanity-io/sanity/pull/1787 | Initial pull request}
 */
export declare const safeJsonParser: (line: string) => SanityDocument;
//# sourceMappingURL=fromExportEndpoint.d.ts.map