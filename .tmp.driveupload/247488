import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { confirm } from '@inquirer/prompts';
import { findBlueprintFile, readLocalBlueprint, writeBlueprintToDisk, } from '../../actions/blueprints/blueprint.js';
import { writeConfigFile } from '../../actions/blueprints/config.js';
import { createEmptyStack } from '../../actions/blueprints/stacks.js';
import { writeGitignoreFile } from '../../actions/git.js';
import { writeOrUpdateNodeDependency } from '../../actions/node.js';
import { verifyExampleExists, writeExample } from '../../actions/sanity/examples.js';
import { getProject } from '../../actions/sanity/projects.js';
import { BLUEPRINT_CONFIG_DIR, BLUEPRINT_CONFIG_FILE } from '../../config.js';
import { check, filePathRelativeToCwd, labeledId, warn } from '../../utils/display/presenters.js';
import { promptForBlueprintType, promptForProject, promptForStack, } from '../../utils/display/prompt.js';
import { styleText } from '../../utils/style-text.js';
import { blueprintConfigCore } from './config.js';
const SCOPE_PROJECT = 'project';
const SCOPE_ORGANIZATION = 'organization';
export async function blueprintInitCore(options) {
    const { bin = 'sanity', log, token, knownProjectId, args, flags, validateResources } = options;
    const { dir: flagDir, example: flagExample, 'blueprint-type': flagBlueprintType, 'project-id': flagProjectId, 'organization-id': flagOrganizationId, 'stack-id': flagStackId, 'stack-name': flagStackName, verbose: v = false, } = flags;
    const { dir: argDir } = args;
    const userProvidedDirName = argDir || flagDir;
    const blueprintDir = userProvidedDirName || '.';
    const validationError = validateFlags({
        stackId: flagStackId,
        stackName: flagStackName,
        organizationId: flagOrganizationId,
        projectId: flagProjectId,
    });
    if (validationError)
        return validationError;
    try {
        const existingBlueprintFile = findBlueprintFile(blueprintDir);
        // existing blueprint file on disk → configure it for deployment
        if (existingBlueprintFile) {
            return handleExistingBlueprint({
                existingBlueprintFile,
                bin,
                log,
                token,
                validateResources,
                flagExample,
                flagProjectId,
                flagOrganizationId,
                flagStackId,
                flagStackName,
                verbose: v,
            });
        }
        // --example flag → scaffold from an example template
        if (flagExample) {
            return handleExampleInitialization({
                exampleName: flagExample,
                projectId: flagProjectId,
                blueprintDir,
                userProvidedDirName,
                token,
                log,
            });
        }
        // no blueprint on disk → create new blueprint files from scratch
        return handleFreshInitialization({
            blueprintDir,
            userProvidedDirName,
            bin,
            log,
            token,
            knownProjectId,
            flagProjectId,
            flagOrganizationId,
            flagStackId,
            flagStackName,
            flagBlueprintType,
        });
    }
    catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        return { success: false, error: errorMessage };
    }
}
async function handleExistingBlueprint(options) {
    const { existingBlueprintFile, bin, log, token, validateResources, flagExample, flagProjectId, flagOrganizationId, flagStackId, flagStackName, verbose, } = options;
    log.warn(warn(`Existing Blueprint found: ${filePathRelativeToCwd(existingBlueprintFile.blueprintFilePath)}`));
    if (flagExample) {
        return {
            success: false,
            error: 'Flag --example cannot be used with an existing Blueprint.',
        };
    }
    // existing blueprint file, user wants to configure a stack
    // --stack-name means they want a new stack created
    let resolvedStackId = flagStackId;
    if (!resolvedStackId && flagStackName) {
        const scopeId = flagProjectId || flagOrganizationId;
        let scopeType;
        if (flagProjectId)
            scopeType = SCOPE_PROJECT;
        else if (flagOrganizationId)
            scopeType = SCOPE_ORGANIZATION;
        if (scopeType && scopeId) {
            // have what we need to create a new stack
            log(`\nCreating new Stack "${flagStackName}" scoped to ${labeledId(scopeType, scopeId)}`);
            const stack = await createEmptyStack({
                token,
                scopeType,
                scopeId,
                name: flagStackName,
                logger: log,
            });
            resolvedStackId = stack.id;
        }
    }
    // unknown intent, prompt for confirmation
    const flagProvidedConfig = [flagProjectId, flagOrganizationId, flagStackId].some(Boolean);
    if (!flagProvidedConfig && !flagStackName) {
        const overwrite = await confirm({
            message: "This Blueprint doesn't have a deployment Stack yet. Configure one now?",
            default: true,
        });
        if (!overwrite)
            return { success: false, error: 'Initialization cancelled.' };
    }
    const existingBlueprint = await readLocalBlueprint(log, { resources: validateResources || false }, existingBlueprintFile.blueprintFilePath);
    return blueprintConfigCore({
        blueprint: existingBlueprint,
        bin,
        log,
        token,
        validateResources,
        flags: {
            edit: true,
            'project-id': flagProjectId,
            'organization-id': flagOrganizationId,
            stack: resolvedStackId,
            verbose,
        },
    });
}
async function handleFreshInitialization(options) {
    const { blueprintDir, userProvidedDirName, bin, log, token, knownProjectId, flagProjectId, flagOrganizationId, flagStackId, flagStackName, flagBlueprintType, } = options;
    const { scopeType, scopeId, stackId } = await resolveScopeAndStack({
        projectId: flagProjectId,
        organizationId: flagOrganizationId,
        stackId: flagStackId,
        stackName: flagStackName,
        knownProjectId,
        log,
        token,
    });
    const blueprintExtension = await determineBlueprintExtension({
        requestedType: flagBlueprintType,
        blueprintDir,
        log,
    });
    return createBlueprintFiles({
        blueprintDir,
        userProvidedDirName,
        blueprintExtension,
        scopeType,
        scopeId,
        stackId,
        bin,
        log,
    });
}
export function validateFlags(flags) {
    const { stackId, stackName, organizationId, projectId } = flags;
    if (stackId && stackName) {
        return { success: false, error: 'Cannot specify both --stack-id and --stack-name' };
    }
    if (organizationId && projectId) {
        return { success: false, error: 'Cannot specify both --organization-id and --project-id' };
    }
    return null;
}
async function handleExampleInitialization(options) {
    const { exampleName, blueprintDir, userProvidedDirName, projectId, token, log } = options;
    log(warn(`Example feature is experimental. Setting up "${exampleName}"...`));
    const exampleExists = await verifyExampleExists({
        type: 'blueprint',
        name: exampleName,
        logger: log,
    });
    if (!exampleExists) {
        return { success: false, error: `Blueprint example "${exampleName}" does not exist.` };
    }
    const resolvedProjectId = projectId || (await promptForProject({ token, logger: log })).projectId;
    const stack = await createEmptyStack({
        token,
        scopeType: SCOPE_PROJECT,
        scopeId: resolvedProjectId,
        name: `example-${exampleName}`,
        logger: log,
    });
    const exampleDir = userProvidedDirName || join(blueprintDir, exampleName);
    if (existsSync(exampleDir)) {
        return { success: false, error: `Example directory "${exampleDir}" already exists.` };
    }
    const addedExample = await writeExample({
        exampleType: 'blueprint',
        exampleName,
        dir: exampleDir,
        logger: log,
    });
    if (!addedExample) {
        return { success: false, error: `Unable to download example "${exampleName}"` };
    }
    const { files, dir: newDir, instructions } = addedExample;
    for (const filePath of Object.keys(files)) {
        log(check(`${styleText('bold', 'Created:')}    ${newDir}/${filePath}`));
    }
    const discoveredBlueprint = findBlueprintFile(exampleDir);
    if (!discoveredBlueprint) {
        return { success: false, error: 'Failed to find blueprint file.' };
    }
    const { blueprintFilePath } = discoveredBlueprint;
    writeConfigFile(blueprintFilePath, { projectId: resolvedProjectId, stackId: stack.id });
    log(check(`${styleText('bold', 'Configured:')} ${exampleDir}/${BLUEPRINT_CONFIG_DIR}/${BLUEPRINT_CONFIG_FILE}`));
    log(`\n  Run "${styleText(['bold', 'magenta'], `cd ${exampleDir} && npm i`)}" and check out the README`);
    if (instructions) {
        log('');
        log(instructions);
    }
    return { success: true };
}
export async function resolveScopeAndStack(params) {
    const { projectId, organizationId, stackId, stackName, knownProjectId, log, token } = params;
    let scopeType = SCOPE_PROJECT;
    let scopeId;
    if (projectId) {
        scopeType = SCOPE_PROJECT;
        scopeId = projectId;
    }
    else if (organizationId) {
        scopeType = SCOPE_ORGANIZATION;
        scopeId = organizationId;
    }
    let resolvedStackId = stackId;
    if (!resolvedStackId && stackName && scopeType && scopeId) {
        // sending stackName will assume you want to create a new stack
        // essentially the only way to create an org-scoped stack
        log(`\nCreating new Stack "${stackName}" scoped to ${labeledId(scopeType, scopeId)}`);
        const stack = await createEmptyStack({
            token,
            scopeType,
            scopeId,
            name: stackName,
            logger: log,
        });
        resolvedStackId = stack.id;
    }
    if (!scopeId) {
        log('\nBlueprints are associated with a Sanity project.');
        // If we have a CLI project ID, offer it as a suggestion
        if (knownProjectId) {
            const { ok, project } = await getProject({
                token,
                scopeId: knownProjectId,
                scopeType: 'project',
                logger: log,
            });
            if (ok && project) {
                const useCliProject = await confirm({
                    message: `The CLI is configured to use "${project.displayName}" (${knownProjectId}). Use this for the blueprint?`,
                    default: true,
                });
                if (useCliProject) {
                    scopeType = SCOPE_PROJECT;
                    scopeId = knownProjectId;
                }
            }
        }
        // If still no scope (no knownProjectId, lookup failed, or user declined), prompt for selection
        if (!scopeId) {
            log('Select a project:');
            const pickedProject = await promptForProject({ token, logger: log });
            scopeType = SCOPE_PROJECT;
            scopeId = pickedProject.projectId;
        }
    }
    if (!resolvedStackId) {
        log('\nBlueprints are deployed to a "Stack".');
        const { stackId } = await promptForStack({ projectId: scopeId, token, logger: log });
        resolvedStackId = stackId;
    }
    return {
        scopeType,
        scopeId,
        stackId: resolvedStackId,
    };
}
export async function determineBlueprintExtension(params) {
    const { requestedType, blueprintDir, log } = params;
    let extension = requestedType;
    if (!extension) {
        log('\nBlueprint files are authored locally to create resources in your Stack.');
        extension = await promptForBlueprintType();
    }
    if (extension === 'js') {
        // do we need to use .mjs or .js?
        const packageJsonPath = join(blueprintDir, 'package.json');
        const packageExists = existsSync(packageJsonPath);
        if (packageExists) {
            try {
                const packageJson = readFileSync(packageJsonPath, 'utf8');
                const packageJsonObject = JSON.parse(packageJson);
                if (packageJsonObject.type !== 'module') {
                    return 'mjs';
                }
            }
            catch { }
        }
    }
    return extension;
}
export async function createBlueprintFiles(params) {
    const { blueprintDir, userProvidedDirName, blueprintExtension, scopeType, scopeId, stackId, bin, log, } = params;
    if (!blueprintExtension) {
        return { success: false, error: 'Blueprint type is required.' };
    }
    log(`\nCreating local Blueprint setup...`);
    const blueprintFileName = `sanity.blueprint.${blueprintExtension}`;
    const blueprintFilePath = join(blueprintDir, blueprintFileName);
    writeBlueprintToDisk({ blueprintFilePath });
    if (userProvidedDirName) {
        log(check(`${styleText('bold', 'New folder created:')}  ${userProvidedDirName}/`));
    }
    const displayPath = userProvidedDirName || '.';
    log(check(`${styleText('bold', 'Created Blueprint:')}   ${displayPath}/${blueprintFileName}`));
    writeConfigFile(blueprintFilePath, {
        stackId,
        ...(scopeType === SCOPE_ORGANIZATION ? { organizationId: scopeId } : { projectId: scopeId }),
    });
    log(check(`${styleText('bold', 'Added configuration:')} ${displayPath}/${BLUEPRINT_CONFIG_DIR}/${BLUEPRINT_CONFIG_FILE}`));
    const gitignoreResult = writeGitignoreFile(blueprintFilePath);
    if (gitignoreResult.action === 'created') {
        log(check(`${styleText('bold', 'Added .gitignore:')}    ${displayPath}/.gitignore`));
    }
    else if (gitignoreResult.action === 'updated') {
        log(check(`${styleText('bold', 'Updated .gitignore:')}  ${displayPath}/.gitignore`));
    }
    if (blueprintExtension !== 'json') {
        const blueprintsPackage = '@sanity/blueprints';
        try {
            await writeOrUpdateNodeDependency(blueprintFilePath, blueprintsPackage, log);
            log(check(`${styleText('bold', 'Added dependency:')}    ${blueprintsPackage}`));
        }
        catch {
            log.warn(warn(`Unable to add ${blueprintsPackage} to your project.`));
        }
    }
    const nextStepParts = [];
    if (userProvidedDirName)
        nextStepParts.push(`cd ${userProvidedDirName}`);
    if (blueprintExtension !== 'json')
        nextStepParts.push('npm install');
    nextStepParts.push(`${bin} blueprints --help`);
    log(`\n  Run "${styleText(['bold', 'magenta'], nextStepParts.join(' && '))}" to get started`);
    return { success: true };
}
