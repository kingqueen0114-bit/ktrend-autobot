import { SanityEncoder } from '@sanity/mutate';
import arrify from 'arrify';
import { isMutation, isNodePatch, isOperation, isTransaction } from '../mutations/asserters.js';
import { at, patch, } from '../mutations/index.js';
import { flatMapDeep } from './utils/flatMapDeep.js';
import { getValueType } from './utils/getValueType.js';
export function normalizeMigrateDefinition(migration) {
    if (typeof migration.migrate == 'function') {
        // assume AsyncIterableMigration
        return normalizeIteratorValues(migration.migrate);
    }
    return createAsyncIterableMutation(migration.migrate, {
        ...(migration.filter !== undefined && { filter: migration.filter }),
        ...(migration.documentTypes !== undefined && { documentTypes: migration.documentTypes }),
    });
}
function normalizeIteratorValues(asyncIterable) {
    return async function* run(docs, context) {
        for await (const documentMutations of asyncIterable(docs, context)) {
            yield normalizeMutation(documentMutations);
        }
    };
}
/**
 * Normalize a mutation or a NodePatch to a document mutation
 * @param documentId - The document id
 * @param change - The Mutation or NodePatch
 */
function normalizeMutation(change) {
    if (Array.isArray(change)) {
        return change.flatMap((ch) => normalizeMutation(ch));
    }
    if (isRawMutation(change)) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any -- SanityEncoder.decodeAll requires specific mutation format
        return SanityEncoder.decodeAll([change]);
    }
    return [change];
}
function isRawMutation(mutation) {
    return ('createIfNotExists' in mutation ||
        'createOrReplace' in mutation ||
        'create' in mutation ||
        'patch' in mutation ||
        'delete' in mutation);
}
export function createAsyncIterableMutation(migration, opts) {
    const documentTypesSet = new Set(opts.documentTypes);
    return async function* run(docs, context) {
        for await (const doc of docs()) {
            if (opts.documentTypes && !documentTypesSet.has(doc._type))
                continue;
            const documentMutations = await collectDocumentMutations(migration, doc, context);
            if (documentMutations.length > 0) {
                yield documentMutations;
            }
        }
    };
}
async function collectDocumentMutations(migration, doc, context) {
    const documentMutations = Promise.resolve(migration.document?.(doc, context));
    const nodeMigrations = flatMapDeep(doc, async (value, path) => {
        const [nodeReturnValues, nodeTypeReturnValues] = await Promise.all([
            Promise.resolve(migration.node?.(value, path, context)),
            Promise.resolve(migrateNodeType(migration, value, path, context)),
        ]);
        return [...arrify(nodeReturnValues), ...arrify(nodeTypeReturnValues)].map((change) => change && normalizeNodeMutation(path, change));
    });
    const resolvedDocumentMutations = arrify(await documentMutations);
    const resolvedNodeMigrations = await Promise.all(nodeMigrations);
    return [...resolvedDocumentMutations, ...resolvedNodeMigrations]
        .flat()
        .flatMap((change) => (change ? normalizeDocumentMutation(doc._id, change) : []));
}
/**
 * Normalize a mutation or a NodePatch to a document mutation
 * @param documentId - The document id
 * @param change - The Mutation or NodePatch
 */
function normalizeDocumentMutation(documentId, change) {
    if (Array.isArray(change)) {
        return change.flatMap((ch) => normalizeDocumentMutation(documentId, ch));
    }
    if (isRawMutation(change)) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any -- SanityEncoder.decodeAll requires specific mutation format
        return SanityEncoder.decodeAll([change])[0];
    }
    if (isTransaction(change)) {
        return change;
    }
    return isMutation(change) ? change : patch(documentId, change);
}
/**
 * Normalize a mutation or a NodePatch to a document mutation
 * @param path - The path the operation should be applied at
 * @param change - The Mutation or NodePatch
 */
function normalizeNodeMutation(path, change) {
    if (Array.isArray(change)) {
        return change.flatMap((ch) => normalizeNodeMutation(path, ch));
    }
    if (isRawMutation(change)) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any -- SanityEncoder.decodeAll requires specific mutation format
        return SanityEncoder.decodeAll([change])[0];
    }
    if (isNodePatch(change)) {
        return at([...path, ...change.path], change.op);
    }
    return isOperation(change) ? at(path, change) : change;
}
function migrateNodeType(migration, value, path, context) {
    switch (getValueType(value)) {
        case 'array': {
            return migration.array?.(value, path, context);
        }
        case 'boolean': {
            return migration.boolean?.(value, path, context);
        }
        case 'null': {
            return migration.null?.(value, path, context);
        }
        case 'number': {
            return migration.number?.(value, path, context);
        }
        case 'object': {
            return migration.object?.(value, path, context);
        }
        case 'string': {
            return migration.string?.(value, path, context);
        }
        default: {
            throw new Error('Unknown value type');
        }
    }
}
//# sourceMappingURL=normalizeMigrateDefinition.js.map