import { decodeText, parse } from '../../it-utils/index.js';
import { safeJsonParser } from '../../sources/fromExportEndpoint.js';
import { streamToAsyncIterator } from '../../utils/streamToAsyncIterator.js';
export function createFilteredDocumentsClient(getFilteredDocumentsReadableStream) {
    function getAllDocumentsFromBuffer() {
        return parse(decodeText(streamToAsyncIterator(getFilteredDocumentsReadableStream())), {
            parse: safeJsonParser,
        });
    }
    async function getDocumentsFromBuffer(ids) {
        const found = {};
        let remaining = ids.length;
        for await (const doc of getAllDocumentsFromBuffer()) {
            if (ids.includes(doc._id)) {
                remaining--;
                found[doc._id] = doc;
            }
            if (remaining === 0)
                break;
        }
        return ids.map((id) => found[id]).filter((item) => item !== undefined);
    }
    async function getDocumentFromBuffer(id) {
        return (await getDocumentsFromBuffer([id]))[0];
    }
    return {
        getDocument: getDocumentFromBuffer,
        getDocuments: getDocumentsFromBuffer,
    };
}
//# sourceMappingURL=createFilteredDocumentsClient.js.map