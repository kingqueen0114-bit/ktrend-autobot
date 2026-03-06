export function isMutation(mutation) {
    return (mutation !== null &&
        typeof mutation === 'object' &&
        'type' in mutation &&
        (mutation.type === 'create' ||
            mutation.type === 'createIfNotExists' ||
            mutation.type === 'createOrReplace' ||
            mutation.type === 'patch' ||
            mutation.type === 'delete'));
}
export function isTransaction(mutation) {
    return (mutation !== null &&
        typeof mutation === 'object' &&
        'type' in mutation &&
        mutation.type === 'transaction');
}
export function isOperation(value) {
    return (value !== null &&
        typeof value === 'object' &&
        'type' in value &&
        (value.type === 'set' ||
            value.type === 'unset' ||
            value.type === 'insert' ||
            value.type === 'diffMatchPatch' ||
            value.type === 'dec' ||
            value.type === 'inc' ||
            value.type === 'upsert' ||
            value.type === 'unassign' ||
            value.type === 'truncate' ||
            value.type === 'setIfMissing'));
}
export function isNodePatch(change) {
    return (change !== null &&
        typeof change === 'object' &&
        'path' in change &&
        Array.isArray(change.path) &&
        'op' in change &&
        isOperation(change.op));
}
//# sourceMappingURL=asserters.js.map