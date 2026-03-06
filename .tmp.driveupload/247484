import { setTimeout as sleep } from 'node:timers/promises';
import { stashAsset } from '../../actions/blueprints/assets.js';
import { setupLogStreaming } from '../../actions/blueprints/logs-streaming.js';
import { getStack, updateStack } from '../../actions/blueprints/stacks.js';
import { niceId } from '../../utils/display/presenters.js';
import { styleText } from '../../utils/style-text.js';
import { isLocalFunctionCollection, isLocalFunctionResource } from '../../utils/types.js';
const DEFAULT_ASSET_TIMEOUT = 60;
const assetTimeoutS = Number(process.env.SANITY_ASSET_TIMEOUT) || DEFAULT_ASSET_TIMEOUT;
const assetTimeoutMs = assetTimeoutS * 1000;
const warnTimeoutMs = assetTimeoutMs / 2;
export async function blueprintDeployCore(options) {
    const { bin = 'sanity', log, auth, stackId, scopeType, scopeId, deployedStack, blueprint, flags, } = options;
    const { verbose } = flags;
    const noWait = flags['no-wait'] || false;
    const stackName = flags['new-stack-name'] ?? deployedStack.name;
    log(`Deploying "${stackName}" ${niceId(deployedStack.id)}...`);
    try {
        const { ok: checkOk, stack: currentStack } = await getStack({ stackId, auth, logger: log });
        if (!checkOk) {
            return { success: false, error: 'Failed to check current Stack status' };
        }
        const operationStatus = currentStack.recentOperation?.status;
        if (operationStatus === 'QUEUED' || operationStatus === 'IN_PROGRESS') {
            return {
                success: false,
                error: 'A Stack operation is already in progress. Please wait for it to complete before deploying.',
            };
        }
        const { resources } = blueprint.parsedBlueprint;
        const validResources = resources?.filter((r) => r.type) || [];
        const functionResources = validResources.filter(isLocalFunctionResource);
        const functionCollections = validResources.filter(isLocalFunctionCollection);
        const allFunctionResources = [...functionResources, ...functionCollections];
        // First stash all function assets
        if (allFunctionResources.length > 0) {
            log('Processing function assets...');
            for (const resource of allFunctionResources) {
                const fnSpinner = log.ora({ text: `Processing ${resource.name}...`, prefixText: ' ' }).start();
                const warnTimer = setTimeout(() => {
                    fnSpinner.text = `Still processing ${resource.name}, this can take a moment...`;
                }, warnTimeoutMs);
                let assetTimeoutTimer;
                let result;
                try {
                    result = await Promise.race([
                        stashAsset({ resource, auth, logger: log }),
                        new Promise((_, reject) => {
                            assetTimeoutTimer = setTimeout(() => {
                                reject(new Error(`Processing ${resource.name} timed out after ${assetTimeoutS}s`));
                            }, assetTimeoutMs);
                        }),
                    ]);
                }
                catch (err) {
                    const msg = err instanceof Error ? err.message : String(err);
                    fnSpinner.fail(msg);
                    return { success: false, error: msg };
                }
                finally {
                    clearTimeout(warnTimer);
                    clearTimeout(assetTimeoutTimer);
                }
                if (result.success && result.assetId) {
                    resource.src = result.assetId;
                    if (isLocalFunctionCollection(resource)) {
                        try {
                            for (const func of resource.functions) {
                                func.src = func.name;
                            }
                            fnSpinner.succeed(`${resource.name} collection ${niceId(result.assetId)} (${resource.functions.length} functions)`);
                            log(`   Functions: ${resource.functions.map((f) => f.name).join(', ')}`);
                        }
                        catch (err) {
                            fnSpinner.fail(`Failed to update function collection ${resource.name}`);
                            return {
                                success: false,
                                error: `Error updating function collection '${resource.name}': ${err instanceof Error ? err.message : String(err)}`,
                            };
                        }
                    }
                    else {
                        fnSpinner.succeed(`${resource.name} ${niceId(result.assetId)}`);
                        log(`   Source: ${resource.src}`);
                    }
                    if (result.hash) {
                        if (result.hash.length > 24) {
                            log.verbose(`   Hash: ${result.hash.slice(0, 8)}...${result.hash.slice(-12)}`);
                        }
                        else {
                            log.verbose(`   Hash: ${result.hash}`);
                        }
                    }
                    if (result.exists)
                        log.verbose('   Asset unchanged');
                }
                else {
                    const errorMsg = isLocalFunctionCollection(resource)
                        ? `Failed uploading function collection ${resource.name} (${resource.functions?.length || 0} functions), deploy has stopped`
                        : `Failed uploading ${resource.name} asset, deploy has stopped`;
                    fnSpinner.fail(errorMsg);
                    return { success: false, error: result.error || 'Failed to process function resource' };
                }
            }
        }
        const spinner = log.ora('Deploying...').start();
        const isoNow = new Date().toISOString();
        const { ok: deployOk, stack, error: deployError, } = await updateStack({
            stackId,
            stackMutation: {
                scopeType,
                scopeId,
                name: stackName,
                document: { resources: validResources },
            },
            auth,
            logger: log,
        });
        if (!deployOk) {
            spinner.fail(`${styleText('red', 'Failed')} to update Stack deployment`);
            return { success: false, error: deployError || 'Failed to update Stack deployment' };
        }
        spinner.stop().clear();
        if (noWait) {
            log(styleText(['bold', 'green'], 'Stack deployment started!'));
            log(`Use \`${bin} blueprints info\` to check status`);
            return { success: true, data: { resources } };
        }
        log(styleText('dim', 'Stack deployment progress:'));
        let logStreamCleanup = null;
        try {
            let lastLogAt = Date.now();
            let idleMessageShown = false;
            logStreamCleanup = await setupLogStreaming({
                stackId: stack.id,
                after: isoNow,
                auth,
                log,
                verbose,
                onActivity: () => {
                    lastLogAt = Date.now();
                },
            });
            while (true) {
                const { ok, stack: currentStack } = await getStack({ stackId: stack.id, auth, logger: log });
                if (!ok) {
                    if (logStreamCleanup)
                        logStreamCleanup();
                    return { success: false, error: 'Failed to check Stack deployment status' };
                }
                const operation = currentStack.recentOperation;
                if (!operation) {
                    if (logStreamCleanup)
                        logStreamCleanup();
                    return { success: false, error: 'No Stack deployment operation found' };
                }
                if (operation.status === 'FAILED') {
                    if (logStreamCleanup)
                        logStreamCleanup();
                    return { success: false, error: 'Stack deployment failed' };
                }
                if (operation.status === 'COMPLETED') {
                    if (logStreamCleanup)
                        logStreamCleanup();
                    log(styleText(['bold', 'green'], 'Stack deployment completed!'));
                    return { success: true, data: { resources } };
                }
                if (!idleMessageShown && Date.now() - lastLogAt > 60_000) {
                    log(`No new activity for 60 seconds. The deployment is still running on Sanity servers.`);
                    log(`You can safely exit and check status later with \`${bin} blueprints info\`.`);
                    idleMessageShown = true;
                }
                await sleep(1500);
            }
        }
        catch (error) {
            if (logStreamCleanup)
                logStreamCleanup();
            throw error;
        }
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return { success: false, error: errorMessage };
    }
}
