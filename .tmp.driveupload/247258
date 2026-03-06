import type { Logger } from '../utils/logger.js';
import { type InvokeExecutionOptions } from '../utils/types.js';
declare const app: (host: string, port: number, logger: ReturnType<typeof Logger>, validateResources: boolean, executionOptions?: Partial<InvokeExecutionOptions>) => void;
declare function parseDocumentUrl(url: string): {
    projectId: string;
    dataset: string;
    docId: string;
} | null;
declare function buildApiUrl(projectId: string, dataset: string, docId: string, apiUrl: string): string;
export { app, buildApiUrl, parseDocumentUrl };
