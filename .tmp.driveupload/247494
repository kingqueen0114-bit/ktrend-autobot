import { patchConfigFile, writeConfigFile, } from '../../actions/blueprints/config.js';
import { resolveStackIdByNameOrId } from '../../actions/blueprints/stacks.js';
import { filePathRelativeToCwd, labeledId, warn } from '../../utils/display/presenters.js';
import { promptForProject, promptForStack } from '../../utils/display/prompt.js';
import { styleText } from '../../utils/style-text.js';
export async function blueprintConfigCore(options) {
    const { bin = 'sanity', blueprint, log, token, flags } = options;
    const { edit: editConfig = false, 'project-id': flagProjectId, 'organization-id': flagOrganizationId, stack: flagStack, verbose: _v = false, } = flags;
    const providedConfigFlag = [flagProjectId, flagStack, flagOrganizationId].some(Boolean);
    const { stackId: configStackId, scopeType: configScopeType, scopeId: configScopeId, blueprintConfig, fileInfo, } = blueprint;
    const blueprintFilePath = fileInfo.blueprintFilePath;
    if (!configStackId && !configScopeType && !configScopeId) {
        log(warn('Incomplete configuration.'));
        if (!editConfig) {
            // blueprint.json exists but no config JSON
            log(`Run \`${bin} blueprints doctor\` for diagnostics.`);
            return { success: true }; // not necessarily fatal
        }
    }
    if (blueprintConfig)
        printConfig({ configLabel: 'Current', log, config: blueprintConfig });
    // passing new config without --edit flag is not allowed
    if (providedConfigFlag && !editConfig) {
        log('To update the configuration, use the --edit flag.');
        return { success: true };
    }
    if (!editConfig) {
        // no edit; return success early
        return { success: true };
    }
    else {
        if (providedConfigFlag) {
            // if a config property flag was passed, set the value and return success
            // do not try to validate correctness of combined flags; this should not be interactive
            const configUpdate = {};
            if (flagProjectId)
                configUpdate.projectId = flagProjectId;
            if (flagStack) {
                const scopeType = flagProjectId ? 'project' : configScopeType;
                const scopeId = flagProjectId || configScopeId;
                if (scopeType && scopeId) {
                    configUpdate.stackId = await resolveStackIdByNameOrId(flagStack, { token, scopeType, scopeId }, log);
                }
                else {
                    configUpdate.stackId = flagStack;
                }
            }
            if (flagOrganizationId)
                configUpdate.organizationId = flagOrganizationId;
            try {
                const newConfig = patchConfigFile(blueprintFilePath, configUpdate);
                printConfig({ configLabel: 'Updated', log, config: newConfig });
                return { success: true };
            }
            catch {
                // fallback to writeConfigFile if patchConfigFile fails
                // creates a new config file with the given properties
                try {
                    const newConfig = writeConfigFile(blueprintFilePath, configUpdate);
                    printConfig({ configLabel: 'Updated', log, config: newConfig });
                    return { success: true };
                }
                catch {
                    return { success: false, error: 'Unable to update configuration.' };
                }
            }
        }
        // prompt for values interactively
        // do not yet offer organization as scope option
        let updatedProjectId = flagProjectId;
        if (!updatedProjectId) {
            const pickedProject = await promptForProject({
                token,
                knownProjectId: configScopeId,
                logger: log,
            });
            updatedProjectId = pickedProject.projectId;
        }
        if (!updatedProjectId)
            return { success: false, error: 'Project ID is required.' };
        let updatedStackId;
        if (flagStack) {
            updatedStackId = await resolveStackIdByNameOrId(flagStack, { token, scopeType: 'project', scopeId: updatedProjectId }, log);
        }
        if (!updatedStackId) {
            const pickedStack = await promptForStack({ projectId: updatedProjectId, token, logger: log });
            updatedStackId = pickedStack.stackId;
        }
        if (!updatedStackId)
            return { success: false, error: 'Stack is required.' };
        try {
            // update or create config JSON
            const newConfig = writeConfigFile(blueprintFilePath, {
                projectId: updatedProjectId,
                stackId: updatedStackId,
            });
            printConfig({ configLabel: 'Updated', log, config: newConfig });
            return { success: true };
        }
        catch {
            return { success: false, error: 'Unable to update configuration!' };
        }
    }
}
function printConfig(options) {
    const { configLabel, log, config } = options;
    const { projectId, organizationId, stackId, updatedAt } = config;
    const scopeType = projectId ? 'project' : 'organization';
    const scopeId = projectId ? projectId : organizationId;
    log.verbose(JSON.stringify(config));
    log(`${styleText('bold', `${configLabel} configuration:`)}`);
    log(`  Deployment: ${labeledId('stack', stackId)}`);
    log(`   Scoped to: ${labeledId(scopeType, scopeId)}`);
    if (updatedAt)
        log(`     Updated: ${new Date(updatedAt).toLocaleString()}`);
    if ('configPath' in config) {
        const { configPath } = config;
        if (configPath)
            log(`        File: ${filePathRelativeToCwd(configPath)}`);
    }
}
