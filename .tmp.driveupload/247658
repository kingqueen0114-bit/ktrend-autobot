import { treeify } from 'array-treeify';
import { SANITY_ACCESS_ROBOT, SANITY_ACCESS_ROLE, SANITY_FUNCTION_DOCUMENT, SANITY_FUNCTION_MEDIA_LIBRARY_ASSET, SANITY_FUNCTION_SCHEDULE, SANITY_PROJECT_CORS, SANITY_PROJECT_DATASET, SANITY_PROJECT_WEBHOOK, } from '../../constants.js';
import { styleText } from '../style-text.js';
import { isCorsOriginResource, isDatasetResource, isRobotResource, isRoleResource, isWebhookResource, } from '../types.js';
import { formatDate, formatDuration } from './dates.js';
import { niceId } from './presenters.js';
import { arrayifyCors, arrayifyDataset, arrayifyFunction, arrayifyRobot, arrayifyRole, arrayifyWebhook, } from './resources-formatting.js';
const functionCategory = {
    label: 'Functions',
    displayNameAttribute: 'displayName',
    formatDetails: arrayifyFunction,
};
const RESOURCE_CATEGORIES = {
    [SANITY_ACCESS_ROLE]: {
        label: 'Roles',
        displayNameAttribute: 'title',
        formatDetails(res) {
            return isRoleResource(res) ? arrayifyRole(res) : [];
        },
    },
    [SANITY_ACCESS_ROBOT]: {
        label: 'Robots',
        displayNameAttribute: 'label',
        formatDetails(res) {
            return isRobotResource(res) ? arrayifyRobot(res) : [];
        },
    },
    [SANITY_FUNCTION_DOCUMENT]: functionCategory,
    [SANITY_FUNCTION_MEDIA_LIBRARY_ASSET]: functionCategory,
    [SANITY_FUNCTION_SCHEDULE]: functionCategory,
    [SANITY_PROJECT_CORS]: {
        label: 'CORS Origins',
        formatDetails(res) {
            return isCorsOriginResource(res) ? arrayifyCors(res) : [];
        },
    },
    [SANITY_PROJECT_DATASET]: {
        label: 'Datasets',
        displayNameAttribute: 'datasetName',
        formatDetails(res) {
            return isDatasetResource(res) ? arrayifyDataset(res) : [];
        },
    },
    [SANITY_PROJECT_WEBHOOK]: {
        label: 'Webhooks',
        displayNameAttribute: 'displayName',
        formatDetails(res) {
            return isWebhookResource(res) ? arrayifyWebhook(res) : [];
        },
    },
};
const categoryByLabel = Object.values(RESOURCE_CATEGORIES).reduce((acc, curr) => {
    acc[curr.label] = curr;
    return acc;
}, {});
function resourceName(res, displayNameAttribute) {
    const nameParts = [styleText(['bold', 'green'], res.name)];
    const displayName = displayNameAttribute &&
        displayNameAttribute in res &&
        typeof res[displayNameAttribute] === 'string' &&
        res[displayNameAttribute];
    if (displayName && displayName !== res.name)
        nameParts.push(styleText('green', `"${displayName}"`));
    return nameParts.join(' ');
}
function deployedResourceName(res, displayNameAttribute, _verbose = false) {
    const nameParts = [styleText(['bold', 'green'], res.name)];
    const displayName = displayNameAttribute &&
        typeof res.parameters[displayNameAttribute] === 'string' &&
        res.parameters[displayNameAttribute];
    if (displayName && displayName !== res.name)
        nameParts.push(styleText('green', `"${displayName}"`));
    // if (verbose)
    nameParts.push(idList(res));
    return nameParts.join(' ');
}
function idList(res) {
    const ids = [];
    if ('id' in res && typeof res.id === 'string' && res.id) {
        ids.push(niceId(res.id));
    }
    if ('externalId' in res && typeof res.externalId === 'string' && res.externalId) {
        ids.push(`<${niceId(res.externalId)}>`);
    }
    return ids.length > 0 ? ids.join(' ') : '';
}
export function formatTitle(title, name) {
    return `${styleText(['bold', 'blue'], title)} ${styleText('bold', `"${name}"`)}`;
}
function categorizeResources(resources) {
    const categorized = {};
    const otherResources = [];
    for (const resource of resources) {
        const cat = RESOURCE_CATEGORIES[resource.type];
        if (cat) {
            if (!categorized[cat.label])
                categorized[cat.label] = [];
            categorized[cat.label].push(resource);
        }
        else {
            otherResources.push(resource);
        }
    }
    // unmatched resources are 'Other Resources'
    if (otherResources.length > 0) {
        categorized['Other Resources'] = otherResources;
    }
    return categorized;
}
function buildOutputTree(resources, createName, mapToResource, verbose = false) {
    const output = [
        `${styleText(['bold', 'underline'], 'Resources')} [${resources.length}]`,
    ];
    const children = [];
    const categorized = categorizeResources(resources);
    for (const category of Object.values(categoryByLabel)) {
        const catResources = categorized[category.label];
        if (catResources && catResources.length > 0) {
            children.push(`${styleText('bold', category.label)} [${catResources.length}]`);
            const details = [];
            for (const res of catResources) {
                details.push(createName(category, res, verbose));
                if (category.formatDetails) {
                    details.push(category.formatDetails(mapToResource(res)));
                }
            }
            children.push(details);
        }
    }
    if (categorized['Other Resources'] && categorized['Other Resources'].length > 0) {
        children.push(`${styleText('bold', 'Other Resources')} [${categorized['Other Resources'].length}]`);
        const otherResourcesOutput = categorized['Other Resources'].map((other) => {
            return `${styleText('yellow', other.name ?? 'unnamed')} ${styleText('dim', other.type)}`;
        });
        children.push(otherResourcesOutput);
    }
    output.push(children);
    return output;
}
export function formatDeployedResourceTree(resources, verbose = false) {
    if (!resources || resources.length === 0)
        return '  Zero deployed resources';
    const output = buildOutputTree(resources, (category, res, v) => deployedResourceName(res, category.displayNameAttribute, v), (res) => ({ name: res.name, type: res.type, ...res.parameters }), verbose);
    return `${treeify(output)}\n`;
}
export function formatResourceTree(resources, verbose = false) {
    if (!resources || resources.length === 0)
        return '  Zero resources';
    const output = buildOutputTree(resources, (category, res) => resourceName(res, category.displayNameAttribute), (res) => res, verbose);
    return `${treeify(output)}\n`;
}
export function formatStackInfo(stack, isCurrentStack = false) {
    const isStack = 'id' in stack; // type narrowing
    const isProjectBasedStack = isStack && stack.id === `ST-${stack.scopeId}`;
    const output = [];
    if (isStack) {
        let stackName = styleText('bold', `"${stack.name}"`);
        if (isCurrentStack)
            stackName = `${styleText('blue', stackName)} (current)`;
        if (isProjectBasedStack)
            stackName += ' (project-based)';
        output.push(`${stackName} ${niceId(stack.id)}`);
    }
    else {
        output.push('Local Blueprint');
    }
    const infoOutput = [];
    if (stack.resources) {
        infoOutput.push(`${stack.resources.length} resource${stack.resources.length === 1 ? '' : 's'}`);
    }
    else {
        infoOutput.push('No resources');
    }
    if (isStack) {
        if (stack.createdAt)
            infoOutput.push(`Created: ${formatDate(stack.createdAt)}`);
        if (stack.updatedAt)
            infoOutput.push(`Updated: ${formatDate(stack.updatedAt)}`);
        if (stack.recentOperation) {
            const operation = stack.recentOperation;
            const operationOutput = [];
            if (operation.id)
                operationOutput.push(`Recent Operation ${niceId(operation.id)}:`);
            if (operation.status) {
                const operationColor = operation.status === 'COMPLETED' ? 'green' : 'red';
                const status = operation.status || 'UNKNOWN';
                operationOutput.push(`Status: ${styleText(operationColor, status)}`);
            }
            if (operation.createdAt)
                operationOutput.push(`Started: ${formatDate(operation.createdAt)}`);
            if (operation.status === 'COMPLETED' && operation.completedAt && operation.createdAt) {
                operationOutput.push(`Completed: ${formatDate(operation.completedAt)}`);
                operationOutput.push(`Duration: ${styleText('yellow', formatDuration(operation.createdAt, operation.completedAt))}`);
            }
            infoOutput.push(operationOutput);
        }
    }
    output.push(infoOutput);
    return treeify(output, { plain: true });
}
export function formatStacksListing(stacks, currentStackId) {
    if (!stacks || stacks.length === 0)
        return 'No stacks found';
    const output = [];
    for (const stack of stacks) {
        const isCurrentStack = currentStackId === stack.id;
        output.push(formatStackInfo(stack, isCurrentStack));
    }
    return output.join('\n');
}
const IGNORED_PARAMS = {
    [SANITY_FUNCTION_DOCUMENT]: new Set(['src']),
    [SANITY_FUNCTION_MEDIA_LIBRARY_ASSET]: new Set(['src']),
    [SANITY_FUNCTION_SCHEDULE]: new Set(['src']),
};
const ASSET_RESOURCE_TYPES = new Set([
    SANITY_FUNCTION_DOCUMENT,
    SANITY_FUNCTION_MEDIA_LIBRARY_ASSET,
    SANITY_FUNCTION_SCHEDULE,
]);
function stringifyUnknown(val) {
    if (val === null || val === undefined)
        return JSON.stringify(val);
    if (Array.isArray(val))
        return `[${val.map(stringifyUnknown).join(',')}]`;
    if (typeof val === 'object') {
        const obj = val;
        const sorted = Object.keys(obj)
            .sort()
            .map((k) => `${JSON.stringify(k)}:${stringifyUnknown(obj[k])}`);
        return `{${sorted.join(',')}}`;
    }
    return JSON.stringify(val);
}
function detectChangedParams(details) {
    const existing = details.existingResource?.parameters;
    const updated = details.updatedResource?.parameters;
    if (!existing || !updated)
        return [];
    const ignored = IGNORED_PARAMS[details.type];
    const keys = new Set([...Object.keys(existing), ...Object.keys(updated)]);
    const changed = [];
    for (const key of keys) {
        if (ignored?.has(key))
            continue;
        if (stringifyUnknown(existing[key]) !== stringifyUnknown(updated[key])) {
            changed.push(key);
        }
    }
    return changed;
}
function getAssetSrc(details) {
    const src = details.updatedResource?.parameters?.src ?? details.parameters?.src;
    return typeof src === 'string' && !src.startsWith('AS-') ? src : undefined;
}
function actionStyle(type, isUnchanged = false) {
    if (isUnchanged)
        return { icon: '=', color: 'dim' };
    switch (type) {
        case 'create':
            return { icon: '+', color: 'green' };
        case 'update':
            return { icon: '~', color: 'yellow' };
        case 'destroy':
            return { icon: '-', color: 'red' };
        case 'attach':
            return { icon: '←', color: 'blue' };
        case 'detach':
            return { icon: '→', color: 'gray' };
        // case 'skip':
        default:
            return { icon: '=', color: 'dim' };
    }
}
export function hasActionableChanges(deploymentPlan) {
    const { summary } = deploymentPlan;
    if (summary.createCount || summary.destroyCount || summary.attachCount || summary.detachCount) {
        return true;
    }
    return deploymentPlan.plan.some((action) => action.type === 'update' &&
        action.details &&
        (detectChangedParams(action.details).length > 0 ||
            (ASSET_RESOURCE_TYPES.has(action.resourceType) &&
                getAssetSrc(action.details) !== undefined)));
}
export function formatDeploymentPlan(deploymentPlan) {
    const lines = [];
    lines.push(styleText('bold', 'Deployment Plan'));
    if (deploymentPlan.plan.length === 0) {
        lines.push(styleText('dim', '  No changes'));
        return lines.join('\n');
    }
    const typePad = Math.max(...deploymentPlan.plan.map((a) => a.type.length));
    const names = deploymentPlan.plan.map((a) => a.details?.name ?? '');
    const namePad = Math.max(...names.map((n) => n.length));
    const enrichedPlan = deploymentPlan.plan.map((action) => {
        const changedParams = action.type === 'update' && action.details ? detectChangedParams(action.details) : [];
        // always represent asset updates as a change; hard to know if the asset has changed
        const assetSrc = action.details && ASSET_RESOURCE_TYPES.has(action.resourceType)
            ? getAssetSrc(action.details)
            : undefined;
        const isUnchanged = action.type === 'update' && changedParams.length === 0 && !assetSrc;
        return { action, changedParams, isUnchanged };
    });
    let unchangedCount = 0;
    for (const { action, changedParams, isUnchanged } of enrichedPlan) {
        const name = action.details?.name ?? '';
        if (isUnchanged)
            unchangedCount++;
        const style = actionStyle(action.type, isUnchanged);
        const icon = styleText(['bold', style.color], style.icon);
        const typeLabel = styleText(style.color, action.type.padEnd(typePad));
        const nameLabel = isUnchanged
            ? styleText('dim', name.padEnd(namePad))
            : styleText('bold', name.padEnd(namePad));
        const resourceType = styleText('dim', action.resourceType);
        let suffix = '';
        if (changedParams.length > 0) {
            suffix = `  ${styleText('yellow', changedParams.join(', '))}`;
        }
        lines.push(`  ${icon} ${typeLabel}  ${nameLabel}  ${resourceType}${suffix}`);
    }
    const { summary } = deploymentPlan;
    const parts = [];
    if (summary.createCount)
        parts.push(styleText('green', `${summary.createCount} create`));
    if (summary.updateCount) {
        let label = `${summary.updateCount} update`;
        if (unchangedCount > 0 && unchangedCount < summary.updateCount) {
            label += ` (${styleText('yellow', `${summary.updateCount - unchangedCount} changed`)})`;
        }
        else if (unchangedCount === summary.updateCount) {
            label += ` ${styleText('dim', '(no changes)')}`;
        }
        parts.push(label);
    }
    if (summary.destroyCount)
        parts.push(styleText('red', `${summary.destroyCount} destroy`));
    if (summary.skipCount)
        parts.push(styleText('dim', `${summary.skipCount} skip`));
    if (summary.attachCount)
        parts.push(styleText('blue', `${summary.attachCount} attach`));
    if (summary.detachCount)
        parts.push(styleText('dim', `${summary.detachCount} detach`));
    if (parts.length > 0) {
        lines.push('');
        lines.push(`  ${parts.join(', ')}`);
    }
    return lines.join('\n');
}
