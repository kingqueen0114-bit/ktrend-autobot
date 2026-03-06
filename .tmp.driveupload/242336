import { type FetchOptions } from '../fetch-utils/fetchStream.js';
import { type APIConfig, type Migration, type MigrationProgress } from '../types.js';
import { type TransactionPayload } from './utils/toSanityMutations.js';
/**
 * @public
 */
export interface MigrationRunnerConfig {
    api: APIConfig;
    concurrency?: number;
    onProgress?: (event: MigrationProgress) => void;
}
/**
 * @public
 */
export declare function toFetchOptionsIterable(apiConfig: APIConfig, mutations: AsyncIterableIterator<TransactionPayload>): AsyncGenerator<FetchOptions, void, unknown>;
/**
 * @public
 */
export declare function run(config: MigrationRunnerConfig, migration: Migration): Promise<void>;
//# sourceMappingURL=run.d.ts.map