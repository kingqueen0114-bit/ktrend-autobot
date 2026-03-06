import { type Path } from '@sanity/types';
import { type Operation } from './operations/types.js';
import { type CreateIfNotExistsMutation, type CreateMutation, type CreateOrReplaceMutation, type DeleteMutation, type NodePatch, type NodePatchList, type PatchMutation, type PatchOptions, type SanityDocument } from './types.js';
import { type NormalizeReadOnlyArray, type Optional, type Tuplify } from './typeUtils.js';
/**
 * Creates a new document.
 * @public
 * @param document - The document to be created.
 * @returns The mutation to create the document.
 */
export declare function create<Doc extends Optional<SanityDocument, '_id'>>(document: Doc): CreateMutation<Doc>;
/**
 * Applies a patch to a document.
 * @public
 * @param id - The ID of the document to be patched.
 * @param patches - The patches to be applied.
 * @param options - Optional patch options.
 * @returns The mutation to patch the document.
 */
export declare function patch<P extends NodePatch | NodePatchList>(id: string, patches: P, options?: PatchOptions): PatchMutation<NormalizeReadOnlyArray<Tuplify<P>>>;
/**
 * Creates a {@link NodePatch} at a specific path.
 * @public
 * @param path - The path where the operation should be applied.
 * @param operation - The operation to be applied.
 * @returns The node patch.
 */
export declare function at<O extends Operation>(path: Path | string, operation: O): NodePatch<Path, O>;
/**
 * Creates a document if it does not exist.
 * @public
 * @param document - The document to be created.
 * @returns The mutation operation to create the document if it does not exist.
 */
export declare function createIfNotExists<Doc extends SanityDocument>(document: Doc): CreateIfNotExistsMutation<Doc>;
/**
 * Creates or replaces a document.
 * @public
 * @param document - The document to be created or replaced.
 * @returns The mutation operation to create or replace the document.
 */
export declare function createOrReplace<Doc extends SanityDocument>(document: Doc): CreateOrReplaceMutation<Doc>;
/**
 * Deletes a document.
 * @public
 * @param id - The id of the document to be deleted.
 * @returns The mutation operation to delete the document.
 */
export declare function delete_(id: string): DeleteMutation;
/**
 * Alias for delete
 * @public
 * @alias
 */
export declare const del: typeof delete_;
//# sourceMappingURL=creators.d.ts.map