import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { basename, dirname, extname } from 'node:path';
import { cwd, env } from 'node:process';
import { pathToFileURL } from 'node:url';
import blueprintParserValidator from '@sanity/blueprints-parser';
import * as find from 'empathic/find';
import { createJiti } from 'jiti';
import { SANITY_FUNCTION_DOCUMENT, SANITY_FUNCTION_MEDIA_LIBRARY_ASSET, SANITY_FUNCTION_SCHEDULE, } from '../../constants.js';
import { isLocalFunctionResource, } from '../../utils/types.js';
import { validateResources } from '../../utils/validate/index.js';
import { validateFunctionResource } from '../../utils/validate/resource.js';
import { backfillOrganizationId, backfillProjectBasedStackId, readConfigFile, } from './config.js';
const SUPPORTED_FILE_EXTENSIONS = ['.json', '.js', '.mjs', '.ts'];
let SUPPORTED_FILE_NAMES = SUPPORTED_FILE_EXTENSIONS.map((ext) => `blueprint${ext}`);
SUPPORTED_FILE_NAMES = [
    ...SUPPORTED_FILE_NAMES,
    ...SUPPORTED_FILE_NAMES.map((name) => `sanity.${name}`),
];
export const JSON_BLUEPRINT_CONTENT = {
    blueprintVersion: '2024-10-01',
    resources: [],
};
export const TS_BLUEPRINT_CONTENT = `
import {defineBlueprint, defineDocumentFunction} from '@sanity/blueprints'

export default defineBlueprint({
  resources: [
    // defineDocumentFunction({name: 'my-function'}),
  ],
})
`.trim();
/**
 * Finds the blueprint file in the given path or current working directory
 * @param blueprintPath - The path of the blueprint file or directory
 * @returns The path, file name, and extension of the blueprint file
 */
export function findBlueprintFile(blueprintPath) {
    let dirToSearch = cwd();
    if (blueprintPath) {
        const pathExists = existsSync(blueprintPath);
        if (!pathExists)
            return null;
        const stat = statSync(blueprintPath);
        if (stat.isFile()) {
            return {
                blueprintFilePath: blueprintPath,
                fileName: basename(blueprintPath),
                extension: extname(blueprintPath),
            };
        }
        if (stat.isDirectory()) {
            dirToSearch = blueprintPath;
        }
    }
    const blueprintFile = find.any(SUPPORTED_FILE_NAMES, { cwd: dirToSearch });
    if (!blueprintFile)
        return null;
    return {
        blueprintFilePath: blueprintFile,
        fileName: basename(blueprintFile),
        extension: extname(blueprintFile),
    };
}
/**
 * Reads the blueprint file from disk and parses it.
 * Overrides config file values with shell environment variables.
 * Can infer stackId from projectId if no stackId is provided and legacy ST-<projectId> stacks from launch are used.
 *
 * @param logger The logger instance
 * @param validate Validation options
 * @param blueprintPath - The path of the blueprint file or directory- will search up the directory tree!
 * @returns Known information about the Blueprint, config, and Stack
 */
export async function readLocalBlueprint(logger, validate, blueprintPath) {
    const blueprintFile = findBlueprintFile(blueprintPath);
    if (!blueprintFile)
        throw Error('Could not find Blueprint file! Use the `blueprints init` command.');
    const { blueprintFilePath: foundFilePath, fileName, extension } = blueprintFile;
    let rawBlueprint;
    let blueprintModule;
    try {
        switch (extension) {
            case '.json': {
                const blueprintString = readFileSync(foundFilePath, 'utf8').toString();
                rawBlueprint = JSON.parse(blueprintString);
                break;
            }
            case '.js':
            case '.mjs': {
                const module = await import(foundFilePath);
                blueprintModule = module.default;
                break;
            }
            case '.ts': {
                const jiti = createJiti(dirname(foundFilePath));
                const modDefault = await jiti.import(pathToFileURL(foundFilePath).href, { default: true });
                blueprintModule = modDefault;
                break;
            }
            default:
                throw Error(`Unsupported blueprint file extension: ${extension}`);
        }
    }
    catch (err) {
        throw Error(`Unable to parse Blueprint file: ${fileName}\n${err}`);
    }
    /**
     * Org, Project, Stack IDs can be set...
     * - in the environment,
     * - on the blueprint module,
     * - and in the config file.
     * The precedence is: environment > blueprint module > config file
     */
    let moduleOrganizationId;
    let moduleProjectId;
    let moduleStackId;
    if (blueprintModule) {
        if (typeof blueprintModule === 'function') {
            try {
                moduleOrganizationId = blueprintModule.organizationId;
                moduleProjectId = blueprintModule.projectId;
                moduleStackId = blueprintModule.stackId;
                rawBlueprint = blueprintModule();
            }
            catch {
                throw Error(`Error executing Blueprint file: ${fileName}`);
            }
        }
        else {
            throw Error(`Blueprint ${fileName} must export a default function`);
        }
    }
    if (typeof rawBlueprint === 'undefined') {
        throw Error('Unable to read Blueprint');
    }
    const { SANITY_ORGANIZATION_ID: envOrganizationId, SANITY_PROJECT_ID: envProjectId, SANITY_BLUEPRINT_STACK_ID: envStackId, } = env;
    const blueprintConfig = readConfigFile(foundFilePath);
    // passively heal config on disk by getting organizationId from projectId
    if (blueprintConfig?.projectId && !blueprintConfig.organizationId) {
        try {
            await backfillOrganizationId({
                projectId: blueprintConfig.projectId,
                blueprintFilePath: foundFilePath,
                logger,
            });
        }
        catch { }
    }
    const sources = {};
    let organizationId;
    if (envOrganizationId) {
        organizationId = envOrganizationId;
        sources.organizationId = 'env';
    }
    else if (moduleOrganizationId) {
        organizationId = moduleOrganizationId;
        sources.organizationId = 'module';
    }
    else if (blueprintConfig?.organizationId) {
        organizationId = blueprintConfig.organizationId;
        sources.organizationId = 'config';
    }
    let projectId;
    if (envProjectId) {
        projectId = envProjectId;
        sources.projectId = 'env';
    }
    else if (moduleProjectId) {
        projectId = moduleProjectId;
        sources.projectId = 'module';
    }
    else if (blueprintConfig?.projectId) {
        projectId = blueprintConfig.projectId;
        sources.projectId = 'config';
    }
    let stackId;
    if (envStackId) {
        stackId = envStackId;
        sources.stackId = 'env';
    }
    else if (moduleStackId) {
        stackId = moduleStackId;
        sources.stackId = 'module';
    }
    else if (blueprintConfig?.stackId) {
        stackId = blueprintConfig.stackId;
        sources.stackId = 'config';
    }
    // LAUNCH LIMIT: 1 Stack per Project - infer stackId from projectId
    // this code path exists to handle project-based stacks from initial Blueprints/Functions launch
    if (!stackId && projectId) {
        try {
            // try to assume project-based stack if no stackId is provided
            stackId = await backfillProjectBasedStackId({
                blueprintFilePath: foundFilePath,
                projectId,
                logger,
            });
            if (stackId)
                sources.stackId = 'inferred';
        }
        catch {
            // our assumption was wrong, so we'll leave stackId undefined
        }
    }
    let scopeType;
    let scopeId;
    // Scope is as specific as possible; project > organization
    if (projectId) {
        scopeType = 'project';
        scopeId = projectId;
    }
    else if (organizationId) {
        scopeType = 'organization';
        scopeId = organizationId;
    }
    const parserResult = blueprintParserValidator(rawBlueprint, {
        invalidReferenceTypes: [
            SANITY_FUNCTION_DOCUMENT,
            SANITY_FUNCTION_MEDIA_LIBRARY_ASSET,
            SANITY_FUNCTION_SCHEDULE,
        ],
    });
    const parsedBlueprint = parserResult.result === 'valid' ? parserResult.blueprint : undefined;
    const errors = parserResult.result !== 'valid' ? parserResult.errors : [];
    // resource validation
    if (parsedBlueprint?.resources) {
        if (validate?.resources) {
            // validate function resources
            errors.push(...validateResources(parsedBlueprint.resources));
        }
        else {
            // backwards compat: fallback to the previous validation if validation was not explicitly enabled
            const functionResources = parsedBlueprint.resources.filter(isLocalFunctionResource);
            const fnErrors = functionResources.map((r) => validateFunctionResource(r));
            errors.push(...fnErrors.flat());
        }
    }
    return {
        fileInfo: { blueprintFilePath: foundFilePath, fileName, extension },
        blueprintConfig,
        rawBlueprint,
        errors,
        scopeType,
        scopeId,
        organizationId,
        projectId,
        stackId,
        sources,
        /** @deprecated */
        configPath: blueprintConfig?.configPath,
        // fallback to the raw blueprint if the parser found errors
        parsedBlueprint: parsedBlueprint || rawBlueprint,
    };
}
export function writeBlueprintToDisk({ blueprintFilePath, jsonContent = JSON_BLUEPRINT_CONTENT, }) {
    const dir = dirname(blueprintFilePath);
    const extension = extname(blueprintFilePath);
    let blueprintContent;
    switch (extension) {
        case '.json': {
            blueprintContent = JSON.stringify(jsonContent, null, 2);
            break;
        }
        case '.js':
        case '.mjs':
        case '.ts': {
            blueprintContent = TS_BLUEPRINT_CONTENT;
            break;
        }
        default: {
            throw Error(`Unsupported blueprint file extension: ${extension}`);
        }
    }
    mkdirSync(dir, { recursive: true });
    writeFileSync(blueprintFilePath, blueprintContent);
    return blueprintContent;
}
export function addResourceToBlueprint({ blueprintFilePath, resource, }) {
    const blueprintFile = findBlueprintFile(blueprintFilePath);
    if (!blueprintFile)
        throw Error('Could not find Blueprint file');
    const { blueprintFilePath: foundPath, extension } = blueprintFile;
    // modify .json files directly
    if (extension === '.json') {
        const blueprintString = readFileSync(foundPath, 'utf8').toString();
        const blueprint = JSON.parse(blueprintString);
        blueprint.resources = blueprint.resources || [];
        blueprint.resources.push(resource);
        writeFileSync(foundPath, JSON.stringify(blueprint, null, 2));
        return;
    }
    return resource;
}
