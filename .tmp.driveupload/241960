import { fromString } from '@sanity/util/paths';
import arrify from 'arrify';
/**
 * Creates a new document.
 * @public
 * @param document - The document to be created.
 * @returns The mutation to create the document.
 */
export function create(document) {
    return { document, type: 'create' };
}
/**
 * Applies a patch to a document.
 * @public
 * @param id - The ID of the document to be patched.
 * @param patches - The patches to be applied.
 * @param options - Optional patch options.
 * @returns The mutation to patch the document.
 */
export function patch(id, patches, options) {
    return {
        id,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any -- arrify loses type information, cast needed for tuple type preservation
        patches: arrify(patches),
        type: 'patch',
        ...(options ? { options } : {}),
    };
}
/**
 * Creates a {@link NodePatch} at a specific path.
 * @public
 * @param path - The path where the operation should be applied.
 * @param operation - The operation to be applied.
 * @returns The node patch.
 */
export function at(path, operation) {
    return {
        op: operation,
        path: typeof path === 'string' ? fromString(path) : path,
    };
}
/**
 * Creates a document if it does not exist.
 * @public
 * @param document - The document to be created.
 * @returns The mutation operation to create the document if it does not exist.
 */
export function createIfNotExists(document) {
    return { document, type: 'createIfNotExists' };
}
/**
 * Creates or replaces a document.
 * @public
 * @param document - The document to be created or replaced.
 * @returns The mutation operation to create or replace the document.
 */
export function createOrReplace(document) {
    return { document, type: 'createOrReplace' };
}
/**
 * Deletes a document.
 * @public
 * @param id - The id of the document to be deleted.
 * @returns The mutation operation to delete the document.
 */
export function delete_(id) {
    return { id, type: 'delete' };
}
/**
 * Alias for delete
 * @public
 * @alias
 */
export const del = delete_;
//# sourceMappingURL=creators.js.map