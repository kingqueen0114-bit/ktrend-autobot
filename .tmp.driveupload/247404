import config from '../../config.js';
import getHeaders from '../../utils/get-headers.js';
import { createTracedFetch } from '../../utils/traced-fetch.js';
const { apiUrl } = config;
export const stacksUrl = `${apiUrl}vX/blueprints/stacks`;
export async function listStacks(auth, logger) {
    const fetchFn = createTracedFetch(logger);
    const response = await fetchFn(stacksUrl, {
        method: 'GET',
        headers: getHeaders(auth),
    });
    const data = await response.json();
    return {
        ok: response.ok,
        error: response.ok ? null : data.message,
        stacks: data,
    };
}
export async function getStack({ stackId, auth, logger, }) {
    const fetchFn = createTracedFetch(logger);
    const response = await fetchFn(`${stacksUrl}/${stackId}`, {
        method: 'GET',
        headers: getHeaders(auth),
    });
    const data = await response.json();
    return {
        ok: response.ok,
        error: response.ok ? null : data.message,
        stack: data,
        response,
    };
}
export async function createStack({ stackMutation, auth, logger, }) {
    const fetchFn = createTracedFetch(logger);
    const response = await fetchFn(stacksUrl, {
        method: 'POST',
        headers: getHeaders(auth),
        body: JSON.stringify({ ...stackMutation, useProjectBasedId: false }), // API defaults to true as of 2025-11-26
    });
    const data = await response.json();
    return {
        ok: response.ok,
        error: response.ok ? null : data.message,
        stack: data,
    };
}
export async function createEmptyStack({ token, scopeType, scopeId, name, logger, }) {
    const stackMutation = {
        name,
        scopeType,
        scopeId,
        document: { resources: [] },
    };
    const response = await createStack({
        stackMutation,
        auth: { token, scopeType, scopeId },
        logger,
    });
    if (!response.ok) {
        throw new Error(response.error || 'Failed to create new Stack');
    }
    return response.stack;
}
export async function updateStack({ stackId, stackMutation, auth, logger, }) {
    const fetchFn = createTracedFetch(logger);
    const response = await fetchFn(`${stacksUrl}/${stackId}`, {
        method: 'PUT',
        headers: getHeaders(auth),
        body: JSON.stringify(stackMutation),
    });
    const data = await response.json();
    return {
        ok: response.ok,
        error: response.ok ? null : data.message,
        stack: data,
    };
}
export async function planStack({ stackId, document, auth, logger, }) {
    const fetchFn = createTracedFetch(logger);
    const response = await fetchFn(`${stacksUrl}/${stackId}/plan`, {
        method: 'POST',
        headers: getHeaders(auth),
        body: JSON.stringify({ document }),
    });
    const data = await response.json();
    if (!response.ok) {
        return {
            ok: false,
            error: data.message || 'Failed to retrieve deployment plan',
            problems: response.status === 400 && Array.isArray(data.problems) ? data.problems : null,
            deploymentPlan: null,
        };
    }
    return { ok: true, error: null, problems: null, deploymentPlan: data };
}
export async function resolveStackIdByNameOrId(value, auth, logger) {
    if (value.startsWith('ST-') && value.length === 13)
        return value;
    const result = await listStacks(auth, logger);
    if (!result.ok)
        throw new Error(result.error || 'Failed to list stacks');
    const match = result.stacks.find((s) => s.name === value);
    if (!match)
        throw new Error(`No stack found with name "${value}"`);
    return match.id;
}
export async function destroyStack({ stackId, auth, logger, }) {
    const fetchFn = createTracedFetch(logger);
    const response = await fetchFn(`${stacksUrl}/${stackId}`, {
        method: 'DELETE',
        headers: getHeaders(auth),
    });
    const data = await response.json();
    return {
        ok: response.ok,
        error: response.ok ? null : data.message,
        stack: data,
    };
}
