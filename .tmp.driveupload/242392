import { type Mutation as SanityMutation } from '@sanity/client';
import { type Mutation, type Transaction } from '../../mutations/index.js';
/**
 * @public
 */
export interface TransactionPayload {
    mutations: SanityMutation[];
    transactionId?: string;
}
export declare function toSanityMutations(it: AsyncIterableIterator<(Mutation | Transaction)[] | Mutation | Transaction>): AsyncIterableIterator<SanityMutation[] | TransactionPayload>;
//# sourceMappingURL=toSanityMutations.d.ts.map