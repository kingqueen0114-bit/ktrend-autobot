import { normalizeMigrateDefinition } from './normalizeMigrateDefinition.js';
function wrapDocumentsIteratorProducer(factory) {
    function documents() {
        return factory();
    }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any -- Need to dynamically add Symbol property to function
    ;
    documents[Symbol.asyncIterator] = () => {
        throw new Error(`The migration is attempting to iterate over the "documents" function, please call the function instead:

      // BAD:
      for await (const document of documents) {
        // ...
      }

      // GOOD:                        👇 This is a function and has to be called
      for await (const document of documents()) {
        // ...
      }
      `);
    };
    return documents;
}
/**
 * @public
 */
export function collectMigrationMutations(migration, documents, context) {
    const migrate = normalizeMigrateDefinition(migration);
    return migrate(wrapDocumentsIteratorProducer(documents), context);
}
//# sourceMappingURL=collectMigrationMutations.js.map