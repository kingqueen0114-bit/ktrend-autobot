import { setTimeout as sleep } from 'node:timers/promises';
import { confirm } from '@inquirer/prompts';
import { setupLogStreaming } from '../../actions/blueprints/logs-streaming.js';
import { destroyStack, getStack, resolveStackIdByNameOrId } from '../../actions/blueprints/stacks.js';
import { niceId } from '../../utils/display/presenters.js';
import { styleText } from '../../utils/style-text.js';
export async function blueprintDestroyCore(options) {
    const { bin = 'sanity', log, token, blueprint, flags } = options;
    const { force = false, 'project-id': flagProjectId, 'organization-id': flagOrganizationId, stack: flagStack, 'no-wait': noWait = false, verbose: _verbose = false, } = flags;
    // 3-flag combo: just destroy it
    if ((flagProjectId || flagOrganizationId) && flagStack && force) {
        let scopeType;
        let scopeId;
        if (flagOrganizationId) {
            scopeType = 'organization';
            scopeId = flagOrganizationId;
        }
        else if (flagProjectId) {
            scopeType = 'project';
            scopeId = flagProjectId;
        }
        else {
            return { success: false, error: 'Unable to determine scope for Blueprint Destroy' };
        }
        const auth = { token, scopeType, scopeId };
        const resolvedId = await resolveStackIdByNameOrId(flagStack, auth, log);
        const { ok, error, stack } = await destroyStack({
            stackId: resolvedId,
            auth,
            logger: log,
        });
        if (!ok)
            return { success: false, error: error || 'Failed to destroy Stack deployment' };
        log(`Stack deployment "${stack.name}" ${niceId(stack.id)} destroyed`);
        return { success: true };
    }
    const { scopeType, scopeId, stackId } = blueprint;
    if (!scopeType || !scopeId)
        return { success: false, error: 'Scope is required' };
    const auth = { token, scopeType, scopeId };
    const resolvedStackId = flagStack
        ? await resolveStackIdByNameOrId(flagStack, auth, log)
        : undefined;
    let stack;
    try {
        if (resolvedStackId) {
            const overrideStack = await getStack({ stackId: resolvedStackId, auth, logger: log });
            if (!overrideStack.ok)
                return { success: false, error: overrideStack.error || 'Failed to get Stack' };
            stack = overrideStack.stack;
        }
        else if (stackId) {
            const blueprintStack = await getStack({ stackId, auth, logger: log });
            if (!blueprintStack.ok)
                return { success: false, error: blueprintStack.error || 'Failed to get Stack' };
            stack = blueprintStack.stack;
        }
        if (!stack)
            return { success: false, error: 'Stack deployment not found' };
        const destroySpinner = log.ora({
            text: `Destroying Stack deployment "${styleText('bold', stack.name)}" ${niceId(stack.id)}...`,
            color: 'red',
        });
        if (!force) {
            const confirmed = await confirm({
                message: `Are you sure you want to destroy stack "${stack.name}" ${niceId(stack.id)}?`,
                default: false,
            });
            if (!confirmed) {
                log('Stack deployment destruction cancelled');
                return { success: true };
            }
            destroySpinner.start();
            // 5 second countdown
            let i = 5;
            while (i >= 0) {
                destroySpinner.text = `Destroying Stack deployment in ${styleText('bold', (i--).toString())} seconds...`;
                await sleep(1000);
            }
            destroySpinner.text = 'Destroying Stack deployment 💥';
            await sleep(500);
        }
        else {
            destroySpinner.start();
        }
        const isoNow = new Date().toISOString();
        const { ok, error } = await destroyStack({ stackId: stack.id, auth, logger: log });
        if (!ok) {
            destroySpinner.fail('Failed to destroy Stack deployment');
            return { success: false, error: error || 'Failed to destroy Stack deployment' };
        }
        destroySpinner.stop().clear();
        if (noWait) {
            log(styleText(['bold', 'magenta'], 'Stack destruction started!'));
            return { success: true };
        }
        log(styleText('dim', 'Stack destruction progress:'));
        let logStreamCleanup = null;
        try {
            let lastLogAt = Date.now();
            let idleMessageShown = false;
            logStreamCleanup = await setupLogStreaming({
                stackId: stack.id,
                after: isoNow,
                auth,
                log,
                onActivity: () => {
                    lastLogAt = Date.now();
                },
            });
            while (true) {
                const { ok, stack: currentStack } = await getStack({ stackId: stack.id, auth, logger: log });
                const operation = currentStack?.recentOperation;
                if (!ok || !operation || operation?.status === 'COMPLETED') {
                    // Operation is also marked destroyed when stack is deleted;
                    // it's possible that the operation is "gone" or available and "COMPLETED"
                    if (logStreamCleanup)
                        logStreamCleanup();
                    log(styleText(['bold', 'magenta'], 'Stack destruction completed!'));
                    return { success: true };
                }
                if (operation.status === 'FAILED') {
                    if (logStreamCleanup)
                        logStreamCleanup();
                    return { success: false, error: 'Stack destruction failed' };
                }
                if (!idleMessageShown && Date.now() - lastLogAt > 60_000) {
                    log(`No new activity for 60 seconds. The destruction is still running on Sanity servers.`);
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
