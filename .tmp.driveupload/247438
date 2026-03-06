import { readLocalBlueprint } from '../actions/blueprints/blueprint.js';
import { getStack, resolveStackIdByNameOrId } from '../actions/blueprints/stacks.js';
import { presentBlueprintParserErrors } from '../utils/display/errors.js';
import { niceId } from '../utils/display/presenters.js';
import { validTokenOrErrorMessage } from '../utils/validated-token.js';
export * as blueprintsCores from './blueprints/index.js';
export * as functionsCores from './functions/index.js';
export async function initBlueprintConfig({ bin, log, token, validateResources = false, validateToken = true, blueprintPath, }) {
    let checkedToken = token;
    if (!token || (token && validateToken)) {
        const tokenCheck = await validTokenOrErrorMessage(log, token);
        if (!tokenCheck.ok) {
            return { ok: false, error: tokenCheck.error.message };
        }
        checkedToken = tokenCheck.value;
    }
    if (!checkedToken) {
        return { ok: false, error: 'A valid token is required but was not provided.' };
    }
    const blueprint = await readLocalBlueprint(log, { resources: validateResources }, blueprintPath);
    if (blueprint.errors.length > 0) {
        log(presentBlueprintParserErrors(blueprint.errors));
        return { ok: false, error: 'Blueprint file contains errors.' };
    }
    return {
        ok: true,
        value: {
            bin,
            blueprint,
            log,
            token: checkedToken,
            validateResources,
        },
    };
}
export async function initDeployedBlueprintConfig(config) {
    if (!config.blueprint) {
        const blueprintResult = await initBlueprintConfig(config);
        if (!blueprintResult.ok)
            return blueprintResult;
        config.blueprint = blueprintResult.value.blueprint;
        config.token = blueprintResult.value.token;
    }
    const { scopeType, scopeId, stackId: blueprintStackId } = config.blueprint;
    if (!scopeType || !scopeId) {
        config.log(`Incomplete configuration. Run \`${config.bin} blueprints doctor\` for diagnostics.`);
        return { ok: false, error: 'Missing scope configuration for Blueprint' };
    }
    const auth = { token: config.token, scopeType, scopeId };
    let stackId = blueprintStackId;
    if (config.stackOverride) {
        stackId = await resolveStackIdByNameOrId(config.stackOverride, auth, config.log);
    }
    if (!stackId) {
        config.log(`Incomplete configuration. Run \`${config.bin} blueprints doctor\` for diagnostics.`);
        return { ok: false, error: 'Missing Stack deployment configuration for Blueprint' };
    }
    const stackResponse = await getStack({ stackId, auth, logger: config.log });
    if (!stackResponse.ok) {
        config.log(`Could not retrieve Stack deployment info for ${niceId(stackId)}.`);
        config.log(`Run \`${config.bin} blueprints doctor\` for diagnostics.`);
        return { ok: false, error: 'Missing Stack deployment' };
    }
    return {
        ok: true,
        value: {
            bin: config.bin,
            log: config.log,
            blueprint: config.blueprint,
            token: config.token,
            scopeType,
            scopeId,
            stackId,
            auth,
            deployedStack: stackResponse.stack,
            validateResources: config.validateResources,
        },
    };
}
