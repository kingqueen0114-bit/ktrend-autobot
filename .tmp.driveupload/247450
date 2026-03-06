import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { cwd } from 'node:process';
import { testAction } from '../../actions/functions/test.js';
import config from '../../config.js';
import { SANITY_FUNCTION_DOCUMENT, SANITY_FUNCTION_MEDIA_LIBRARY_ASSET } from '../../constants.js';
import buildPayload from '../../utils/build-payload.js';
import { findFunctionInBlueprint, getFunctionNames } from '../../utils/find-function.js';
import { fetchAsset, fetchDocument } from '../../utils/functions/fetch-document.js';
import { parseJsonObject } from '../../utils/parse-json-object.js';
import { isEventType, isGroqContextOptions, } from '../../utils/types.js';
export async function functionTestCore(options) {
    const { blueprint, log, error, args, flags, helpText } = options;
    const { name: fnName } = args;
    const { data, event, file, timeout, api, dataset, 'document-id': documentId, 'with-user-token': withUserToken, 'data-before': dataBefore, 'data-after': dataAfter, 'file-before': fileBefore, 'file-after': fileAfter, 'document-id-before': documentIdBefore, 'document-id-after': documentIdAfter, 'media-library-id': mediaLibraryId, } = flags;
    const { parsedBlueprint } = blueprint;
    const { 'project-id': projectId = blueprint?.projectId, 'organization-id': organizationId = blueprint?.organizationId, } = flags;
    if (!fnName) {
        const functionNames = getFunctionNames(blueprint.parsedBlueprint.resources);
        const validNames = functionNames.length > 0
            ? `Valid names are: ${functionNames.join(', ')}`
            : 'No functions are defined in the blueprint.';
        error(`Missing required argument: name\n${validNames}\n`, { exit: false });
        log(helpText);
        return { success: true };
    }
    let eventType;
    if (!event) {
        eventType = 'create';
    }
    else if (isEventType(event)) {
        eventType = event;
    }
    else {
        return {
            success: false,
            error: 'The event must be one of `create`, `update` or `delete`.',
        };
    }
    try {
        const resource = findFunctionInBlueprint(parsedBlueprint, fnName); // throws if not found
        const docFunction = resource.type === SANITY_FUNCTION_DOCUMENT;
        const mediaFunction = resource.type === SANITY_FUNCTION_MEDIA_LIBRARY_ASSET;
        const contextOptions = docFunction || mediaFunction
            ? {
                clientOptions: {
                    apiVersion: api,
                    dataset,
                    projectId,
                    organizationId,
                },
                eventResourceType: docFunction ? 'dataset' : 'media-library',
                eventResourceId: (docFunction ? `${projectId}.${dataset}` : mediaLibraryId) || '',
                functionResourceType: 'project',
                functionResourceId: projectId || '',
            }
            : {};
        // If the user sets the flag to use the real token set it in our options
        if (withUserToken && isGroqContextOptions(contextOptions)) {
            contextOptions.clientOptions.token = config.token || undefined;
        }
        let before = null;
        let after = null;
        if (dataBefore && dataAfter) {
            before = parseJsonObject(dataBefore);
            after = parseJsonObject(dataAfter);
        }
        else if (fileBefore && fileAfter) {
            let fileContents = readFileSync(join(cwd(), fileBefore), 'utf8');
            before = parseJsonObject(fileContents);
            fileContents = readFileSync(join(cwd(), fileAfter), 'utf8');
            after = parseJsonObject(fileContents);
        }
        else if (documentIdBefore && documentIdAfter && docFunction) {
            before = await fetchDocument(documentIdBefore, {
                projectId,
                dataset,
                apiVersion: api,
                apiHost: config.apiUrl,
                token: config.token || undefined,
            }, log);
            after = await fetchDocument(documentIdAfter, {
                projectId,
                dataset,
                apiVersion: api,
                apiHost: config.apiUrl,
                token: config.token || undefined,
            }, log);
        }
        else if (documentIdBefore && documentIdAfter) {
            before = await fetchAsset(documentIdBefore, {
                mediaLibraryId,
                apiVersion: api,
                apiHost: config.apiUrl,
                token: config.token || undefined,
            }, log);
            after = await fetchAsset(documentIdAfter, {
                mediaLibraryId,
                apiVersion: api,
                apiHost: config.apiUrl,
                token: config.token || undefined,
            }, log);
        }
        let payload;
        if (after) {
            payload = after;
        }
        else {
            if (documentId && docFunction) {
                payload = await fetchDocument(documentId, {
                    projectId,
                    dataset,
                    apiVersion: api,
                    apiHost: config.apiUrl,
                    token: config.token || undefined,
                }, log);
            }
            else if (documentId) {
                payload = await fetchAsset(documentId, {
                    mediaLibraryId,
                    apiVersion: api,
                    apiHost: config.apiUrl,
                    token: config.token || undefined,
                }, log);
            }
            else {
                payload = buildPayload({ data, file });
            }
        }
        const invokeOptions = docFunction || mediaFunction
            ? {
                event: eventType,
                payload,
                before,
                after,
            }
            : {
                event: 'schedule',
            };
        const spinner = log.ora('Executing function...').start();
        const { json, logs, error } = await testAction(resource, invokeOptions, contextOptions, {
            timeout: timeout ? timeout : resource.timeout,
        });
        if (error) {
            spinner.fail('Function execution failed.');
            return {
                success: false,
                error: error.stack || error.message || error.name,
            };
        }
        spinner.succeed('Function execution succeeded.');
        log('Logs:');
        log(logs || '');
        if (json) {
            log('Response:');
            log(JSON.stringify(json, null, 2));
        }
        return { success: true };
    }
    catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : String(error),
        };
    }
}
