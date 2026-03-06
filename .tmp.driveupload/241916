export function transaction(idOrMutations, _mutations) {
    const [id, mutations] = typeof idOrMutations === 'string'
        ? [idOrMutations, _mutations]
        : [undefined, idOrMutations];
    return { type: 'transaction', ...(id !== undefined && { id }), mutations };
}
//# sourceMappingURL=transaction.js.map