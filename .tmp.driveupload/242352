import { SanityEncoder } from '@sanity/mutate';
import arrify from 'arrify';
import { isTransaction } from '../../mutations/asserters.js';
export async function* toSanityMutations(it) {
    for await (const mutation of it) {
        for (const mut of arrify(mutation)) {
            if (isTransaction(mut)) {
                yield {
                    ...(mut.id !== undefined && { transactionId: mut.id }),
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any -- SanityEncoder.encodeAll requires array of any
                    mutations: SanityEncoder.encodeAll(mut.mutations),
                };
                continue;
            }
            // eslint-disable-next-line @typescript-eslint/no-explicit-any -- SanityEncoder.encodeAll requires array of any
            yield SanityEncoder.encodeAll(arrify(mut));
        }
    }
}
//# sourceMappingURL=toSanityMutations.js.map