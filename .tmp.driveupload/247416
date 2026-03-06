import AdmZip from 'adm-zip';
import type { Logger } from '../../utils/logger.js';
import type { AuthParams, CollectionFunction, FunctionResource } from '../../utils/types.js';
export declare const ASSET_CHECK_URL: string;
export declare const ASSET_STASH_URL: string;
export declare function stashAsset({ resource, auth, logger, }: {
    resource: FunctionResource | CollectionFunction;
    auth: AuthParams;
    logger: ReturnType<typeof Logger>;
}): Promise<{
    success: boolean;
    assetId?: string;
    exists?: boolean;
    hash?: string;
    error?: string;
}>;
export declare function hashBuffer(buffer: Buffer): string;
export declare function pathToZip(path: string): Promise<AdmZip>;
export declare function pathToB64ZipHash(path: string): Promise<{
    b64: string;
    buffer: Buffer;
    hash: string;
    zip: AdmZip;
}>;
