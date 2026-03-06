import { listStacks } from '../../actions/blueprints/stacks.js';
import { formatStacksListing } from '../../utils/display/blueprints-formatting.js';
import { capitalize, niceId } from '../../utils/display/presenters.js';
import { styleText } from '../../utils/style-text.js';
export async function blueprintStacksCore(options) {
    const { log, token, blueprint, flags } = options;
    const { scopeType: blueprintScopeType, scopeId: blueprintScopeId, stackId: blueprintStackId, } = blueprint;
    const { 'project-id': flagProjectId, 'organization-id': flagOrganizationId, verbose: _verbose = false, } = flags;
    if (flagOrganizationId && flagProjectId) {
        log.error('Cannot specify both --organization-id and --project-id');
        return { success: false, error: 'Cannot specify both --organization-id and --project-id' };
    }
    let scopeType = blueprintScopeType;
    let scopeId = blueprintScopeId;
    if (flagOrganizationId) {
        scopeType = 'organization';
        scopeId = flagOrganizationId;
    }
    if (flagProjectId) {
        scopeType = 'project';
        scopeId = flagProjectId;
    }
    if (!scopeType || !scopeId) {
        log.error('Run in a Blueprint directory or provide a Project with --project-id');
        return { success: false, error: 'Unable to determine scope for Blueprint Stacks' };
    }
    try {
        const { ok, stacks, error } = await listStacks({ token, scopeType, scopeId }, log);
        if (!ok)
            return { success: false, error: error || 'Failed to list stacks' };
        if (!stacks || stacks.length === 0) {
            log('No stacks found');
            return { success: true };
        }
        log(`${styleText('bold', capitalize(scopeType))} ${niceId(scopeId)} ${styleText('bold', 'Stacks')}:\n`);
        log(formatStacksListing(stacks, blueprintStackId));
        return { success: true };
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        log.error(`Error: ${errorMessage}`);
        return { success: false, error: errorMessage };
    }
}
