import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { cwd } from 'node:process';
import AdmZip from 'adm-zip';
import getFolderSize from 'get-folder-size';
import config from '../../config.js';
import { detectNativeModules } from '../../utils/functions/detect-native-modules.js';
import { resolveResourceDependencies } from '../../utils/functions/resolve-dependencies.js';
import { shouldAutoResolveDependencies } from '../../utils/functions/should-auto-resolve-deps.js';
import { shouldTranspileFunction } from '../../utils/functions/should-transpile.js';
import getHeaders from '../../utils/get-headers.js';
import { createTracedFetch } from '../../utils/traced-fetch.js';
import { transpileFunction } from '../../utils/transpile/transpile-function.js';
import { isLocalFunctionCollection } from '../../utils/types.js';
const { apiUrl } = config;
const ASSETS_URL = `${apiUrl}vX/blueprints/assets`;
export const ASSET_CHECK_URL = `${ASSETS_URL}/check`;
export const ASSET_STASH_URL = `${ASSETS_URL}/stash`;
const MAX_ASSET_SIZE = 209_715_200; // 200 MB in bytes
export async function stashAsset({ resource, auth, logger, }) {
    const isCollection = isLocalFunctionCollection(resource);
    const functions = isCollection ? resource.functions : [resource];
    const combinedAsset = [];
    const prepareErrors = [];
    try {
        for (const func of functions) {
            const prepResult = await prepareAsset({ resource: func, auth });
            if (prepResult.success && prepResult.outputPath && prepResult.cleanup) {
                combinedAsset.push({
                    name: func.name,
                    partAsset: { outputPath: prepResult.outputPath, cleanup: prepResult.cleanup },
                });
            }
            else if (prepResult.error) {
                prepareErrors.push({ name: func.name, error: prepResult.error });
            }
        }
        if (combinedAsset.length !== functions.length) {
            const processedNames = new Set(combinedAsset.map((asset) => asset.name));
            const failedFunctions = functions.filter((func) => !processedNames.has(func.name));
            const failedNames = failedFunctions.map((f) => f.name).join(', ');
            const errorDetails = prepareErrors.map((e) => `${e.name}: ${e.error}`).join('; ');
            return {
                success: false,
                error: `Failed to prepare ${failedFunctions.length} function(s) in blueprint: ${failedNames}${errorDetails ? `. Details: ${errorDetails}` : ''}`,
            };
        }
        let result = { success: false };
        if (isCollection) {
            const combinedResult = await combineAssets(combinedAsset);
            if (combinedResult.combinedPath && combinedResult.cleanup) {
                result = await stashSingleAsset({
                    outputPath: combinedResult.combinedPath,
                    cleanup: combinedResult.cleanup,
                    resource: resource,
                    auth,
                    logger,
                    collectionInfo: {
                        name: resource.name,
                        functionCount: resource.functions.length,
                    },
                });
            }
            else if (combinedResult.error) {
                result = { success: false, error: combinedResult.error };
            }
        }
        else {
            result = await stashSingleAsset({
                outputPath: combinedAsset[0].partAsset.outputPath,
                cleanup: combinedAsset[0].partAsset.cleanup,
                resource: resource,
                auth,
                logger,
            });
        }
        return result;
    }
    catch (err) {
        return { success: false, error: err instanceof Error ? err.message : `${err}` };
    }
}
async function prepareAsset({ resource, }) {
    if (!resource.src)
        throw new Error('Resource src is required');
    let functionPath = path.join(cwd(), resource.src);
    let cleanup = async () => { };
    const shouldTranspile = await shouldTranspileFunction(resource);
    if (shouldTranspile) {
        try {
            const result = await transpileFunction(resource);
            functionPath = result.outputDir;
            cleanup = result.cleanup;
        }
        catch (err) {
            return { success: false, error: err instanceof Error ? err.message : `${err}` };
        }
    }
    const shouldResolveDependencies = await shouldAutoResolveDependencies(resource);
    if (shouldResolveDependencies) {
        await resolveResourceDependencies(resource, shouldTranspile);
    }
    try {
        // This works for files and folders
        const size = await getFolderSize.loose(functionPath);
        if (size > MAX_ASSET_SIZE) {
            throw new Error('Resource is larger than max asset size of 200 MB.');
        }
        return { success: true, outputPath: functionPath, cleanup };
    }
    catch (err) {
        return { success: false, error: err instanceof Error ? err.message : `${err}` };
    }
}
async function combineAssets(allAssets) {
    const combinedPath = path.join(os.tmpdir(), `assets-${Date.now()}`);
    await fs.promises.mkdir(combinedPath, { recursive: true });
    try {
        for (const asset of allAssets) {
            try {
                await fs.promises.mkdir(path.join(combinedPath, asset.name), { recursive: true });
                await fs.promises.cp(asset.partAsset.outputPath, path.join(combinedPath, asset.name), {
                    recursive: true,
                });
                await asset.partAsset.cleanup();
            }
            catch (err) {
                // Clean up any partial work
                try {
                    await fs.promises.rm(combinedPath, { recursive: true, force: true });
                }
                catch {
                    // Ignore cleanup errors
                }
                // Clean up remaining individual assets
                await Promise.allSettled(allAssets.map((a) => a.partAsset.cleanup()));
                return {
                    error: `Failed to combine asset for function '${asset.name}': ${err instanceof Error ? err.message : String(err)}`,
                };
            }
        }
        const cleanupCombined = async () => {
            await fs.promises.rm(combinedPath, { recursive: true, force: true });
        };
        return { combinedPath, cleanup: cleanupCombined };
    }
    catch (err) {
        // Clean up any partial work
        try {
            await fs.promises.rm(combinedPath, { recursive: true, force: true });
        }
        catch {
            // Ignore cleanup errors
        }
        // Clean up individual assets that were successfully prepared
        await Promise.allSettled(allAssets.map((asset) => asset.partAsset.cleanup()));
        return { error: err instanceof Error ? err.message : `${err}` };
    }
}
async function stashSingleAsset({ outputPath, cleanup, resource, auth, logger, collectionInfo, }) {
    const fetchFn = createTracedFetch(logger);
    try {
        const { b64, hash } = await pathToB64ZipHash(outputPath);
        try {
            const checkResponse = await fetchFn(`${ASSET_CHECK_URL}/${hash}`, {
                method: 'GET',
                headers: getHeaders(auth),
            });
            const checkJson = await checkResponse.json();
            if (checkResponse.ok && checkJson.exists && checkJson.id) {
                return { success: true, assetId: checkJson.id, exists: true, hash };
            }
        }
        catch { } // Continue to stash the Asset
        // Asset doesn't exist, so stash it
        const assetResponse = await fetchFn(ASSET_STASH_URL, {
            method: 'POST',
            headers: getHeaders(auth),
            body: JSON.stringify({
                file: b64,
                filename: `${resource.name}.zip`,
            }),
        });
        const assetJson = await assetResponse.json();
        if (assetResponse.ok) {
            return { success: true, assetId: assetJson.id, exists: false, hash };
        }
        const contextMsg = collectionInfo
            ? ` (part of collection '${collectionInfo.name}' with ${collectionInfo.functionCount} functions)`
            : '';
        return {
            success: false,
            error: `Failed to stash asset for ${resource.name}${contextMsg}: ${assetJson.message || 'Unknown error'}`,
        };
    }
    catch (err) {
        let error = '';
        if (err instanceof Error)
            error = err.message;
        return { success: false, error };
    }
    finally {
        await cleanup();
    }
}
export function hashBuffer(buffer) {
    const hash = crypto.createHash('sha256');
    hash.update(buffer);
    return hash.digest('hex');
}
export async function pathToZip(path) {
    const stats = await fs.promises.stat(path);
    const zip = new AdmZip();
    if (stats.isDirectory())
        zip.addLocalFolder(path);
    else
        zip.addLocalFile(path, '', 'index.js');
    return zip;
}
export async function pathToB64ZipHash(path) {
    const zip = await pathToZip(path);
    const hasNativeModules = detectNativeModules(zip);
    if (hasNativeModules?.length > 0) {
        const errorMsg = `Native modules detected in Function:\n${hasNativeModules.join('\n')}\n\n` +
            `Please replace with JavaScript alternatives.`;
        throw new Error(errorMsg);
    }
    const buffer = zip.toBuffer();
    const b64 = buffer.toString('base64');
    const hash = hashBuffer(buffer);
    return { b64, buffer, hash, zip };
}
