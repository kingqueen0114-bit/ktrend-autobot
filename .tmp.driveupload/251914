import type { AssetFailure, ImportOptions } from './types.js';
export interface AssetRef {
    documentId: string;
    path: string;
    url: string;
    type: string;
}
export interface AssetRefMapItem {
    documentId: string;
    path: string;
}
export interface UploadAssetsResult {
    batches: number;
    failures: AssetFailure[];
}
export declare function uploadAssets(assets: AssetRef[], options: ImportOptions): Promise<UploadAssetsResult>;
//# sourceMappingURL=uploadAssets.d.ts.map