import { readLocalBlueprint } from '../../actions/blueprints/blueprint.js';
import { findFunctionInBlueprint } from '../../utils/find-function.js';
import invoke from '../../utils/invoke-local.js';
export async function handleInvokeRequest(functionName, event, metadata, context, logger, validateResources, executionOptions) {
    const start = performance.now();
    const { parsedBlueprint } = await readLocalBlueprint(logger, { resources: validateResources });
    const resource = findFunctionInBlueprint(parsedBlueprint, functionName);
    const readBlueprintTime = performance.now() - start;
    const payload = {
        payload: event,
        ...metadata,
    };
    const response = await invoke(resource, payload, context, {
        forceColor: executionOptions?.forceColor ?? false,
        timeout: executionOptions?.timeout ?? resource.timeout,
    });
    const timings = { ...response.timings, 'blueprint:read': readBlueprintTime };
    return { ...response, timings };
}
