import { extractWithPath } from '@sanity/mutator';
import debug from 'debug';
import { get } from 'lodash-es';
import pMap from 'p-map';
import { serializePath } from './serializePath.js';
import { progressStepper } from './util/progressStepper.js';
import { retryOnFailure } from './util/retryOnFailure.js';
import { suffixTag } from './util/suffixTag.js';
const logger = debug('sanity:import');
const STRENGTHEN_CONCURRENCY = 30;
const STRENGTHEN_BATCH_SIZE = 30;
export function getStrongRefs(doc) {
    const refs = findStrongRefs(doc).map(serializePath);
    if (refs.length) {
        return {
            documentId: doc._id,
            references: refs
        };
    }
    return null;
}
// Note: mutates in-place
export function weakenStrongRefs(doc) {
    const refs = findStrongRefs(doc);
    refs.forEach((item)=>{
        item.ref._weak = true;
    });
    return doc;
}
// Note: mutates in-place
export function cleanupReferences(doc, options) {
    const { targetProjectId, skipCrossDatasetReferences } = options;
    extractWithPath('..[_ref]', doc).map((match)=>match.path.slice(0, -1)).map((path)=>({
            path,
            ref: get(doc, path)
        })).forEach((item)=>{
        // We may want to skip cross-dataset references, eg when importing to other projects
        if (skipCrossDatasetReferences && '_dataset' in item.ref) {
            const leaf = item.path[item.path.length - 1];
            const parent = item.path.length > 1 ? get(doc, item.path.slice(0, -1)) : doc;
            if (typeof leaf === 'string' || typeof leaf === 'number') {
                delete parent[leaf];
            }
            return;
        }
        // Apply missing _type on references
        if (typeof item.ref._type === 'undefined') {
            ;
            item.ref._type = 'reference';
        }
        // Ensure cross-dataset references point to the same project ID as being imported to
        const refWithProjectId = item.ref;
        if (typeof refWithProjectId._projectId !== 'undefined') {
            refWithProjectId._projectId = targetProjectId;
        }
    });
    return doc;
}
function findStrongRefs(doc) {
    return extractWithPath('..[_ref]', doc).map((match)=>match.path.slice(0, -1)).map((path)=>({
            path,
            ref: get(doc, path)
        })).filter((item)=>item.ref._weak !== true);
}
export function strengthenReferences(strongRefs, options) {
    const { client, tag } = options;
    const batches = [];
    for(let i = 0; i < strongRefs.length; i += STRENGTHEN_BATCH_SIZE){
        batches.push(strongRefs.slice(i, i + STRENGTHEN_BATCH_SIZE));
    }
    if (batches.length === 0) {
        return Promise.resolve([
            0
        ]);
    }
    const progress = progressStepper(options.onProgress, {
        step: 'Strengthening references',
        total: batches.length
    });
    const mapOptions = {
        concurrency: STRENGTHEN_CONCURRENCY
    };
    return pMap(batches, unsetWeakBatch.bind(null, client, progress, tag), mapOptions);
}
function unsetWeakBatch(client, progress, tag, batch) {
    logger('Strengthening batch of %d documents', batch.length);
    return retryOnFailure(()=>batch.reduce(reducePatch, client.transaction()).commit({
            visibility: 'async',
            tag: suffixTag(tag, 'ref.strengthen')
        }).then((res)=>{
            progress();
            return res.results.length;
        }).catch((err)=>{
            const apiError = err;
            apiError.step = 'strengthen-references';
            throw apiError;
        }), {
        isRetriable: (err)=>!err.statusCode || err.statusCode !== 409
    });
}
function reducePatch(trx, task) {
    return trx.patch(task.documentId, (patch)=>patch.unset(task.references.map((path)=>`${path}._weak`)));
}

//# sourceMappingURL=references.js.map