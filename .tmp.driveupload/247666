import type { Logger } from './logger.js';
import type { Result } from './types.js';
export declare function validToken(logger: ReturnType<typeof Logger>, maybeToken?: string): Promise<string>;
export declare function validTokenOrErrorMessage(logger: ReturnType<typeof Logger>, maybeToken?: string): Promise<Result<string, {
    e: Error | unknown;
    message: string;
}>>;
