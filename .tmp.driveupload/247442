import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { cwd } from 'node:process';
import { checkbox, confirm, input, select } from '@inquirer/prompts';
import { highlight } from 'cardinal';
import { createFunctionResource } from '../../actions/blueprints/resources.js';
import { verifyExampleExists, writeExample } from '../../actions/sanity/examples.js';
import { SANITY_FUNCTION_MEDIA_LIBRARY_ASSET, SANITY_FUNCTION_SCHEDULE } from '../../constants.js';
import { check, indent, warn } from '../../utils/display/presenters.js';
import { styleText } from '../../utils/style-text.js';
import { validateFunctionName } from '../../utils/validate/resource.js';
const generateFunctionBlueprintResourceTemplate = (fnName, eventNames) => {
    const definer = eventNames[0].substring(0, eventNames[0].lastIndexOf('-')) === 'document'
        ? 'Document'
        : 'MediaLibraryAsset';
    const isML = definer.startsWith('Media');
    const eventOns = eventNames.map((e) => `'${e.substring(e.lastIndexOf('-') + 1)}'`);
    return `
  export default defineBlueprint({
    resources: [
      // ...
      define${definer}Function({name: '${fnName}', event: {on: [${eventOns.join(', ')}]${isML ? ", resource: {type: 'media-library', id: 'my-media-library-id'}" : ''}}}), // ← add this line
    ],
  })
`;
};
export async function functionAddCore(options) {
    const root = cwd();
    const { log, blueprint, flags } = options;
    const { blueprintFilePath } = blueprint.fileInfo;
    const { example: flagExample, name: flagResourceName, type: flagType, javascript: flagJs, helpers: flagHelpers, install: flagI, installer: flagInstaller, } = flags;
    let { language: flagLang } = flags;
    flagLang = flagJs ? 'js' : flagLang;
    if (flagExample) {
        // short circuit whole command for example flag
        log(`Setting up "${flagExample}"...`);
        const exampleExists = await verifyExampleExists({
            type: 'function',
            name: flagExample,
            logger: log,
        });
        if (!exampleExists) {
            return { success: false, error: `Function example "${flagExample}" does not exist.` };
        }
        const exampleDir = join(dirname(blueprintFilePath), 'functions', flagExample);
        if (existsSync(exampleDir)) {
            return {
                success: false,
                error: `Directory "${exampleDir.replace(root, '')}" already exists.`,
            };
        }
        const addedExample = await writeExample({
            exampleType: 'function',
            exampleName: flagExample,
            dir: exampleDir,
            logger: log,
        });
        if (!addedExample) {
            return { success: false, error: `Unable to download example "${flagExample}"` };
        }
        const { files, dir, instructions, functionConfig } = addedExample;
        const newDir = dir.replace(root, '').replace(/^[/\\]+/, '');
        for (const filePath of Object.keys(files)) {
            log(check(`${styleText('bold', 'Created:')}  ${newDir}/${filePath}`));
        }
        if (functionConfig) {
            log('');
            log(styleText('bold', `Add the following to ${blueprint.fileInfo.fileName}:`));
            const configString = JSON.stringify(functionConfig, null, 2);
            if (blueprint.fileInfo.extension === '.json') {
                log(indent(highlight(configString)));
            }
            else {
                const objectLiteral = configString.replace(/^(\s*)"([a-zA-Z_$][a-zA-Z0-9_$]*)":/gm, '$1$2:');
                let type = 'Document';
                switch (functionConfig.type) {
                    case SANITY_FUNCTION_MEDIA_LIBRARY_ASSET:
                        type = 'MediaLibraryAsset';
                        break;
                    case SANITY_FUNCTION_SCHEDULE:
                        type = 'Schedule';
                        break;
                    default:
                }
                log(indent(highlight(`define${type}Function(${objectLiteral})`)));
            }
        }
        else {
            log.warn(warn('No Function config found in example.'));
        }
        if (instructions) {
            log('');
            log(instructions);
        }
        return { success: true };
    }
    if (flagI) {
        if (flagInstaller) {
            return {
                success: false,
                error: 'Cannot use --installer flag with the --install flag',
            };
        }
        if (!flagHelpers) {
            return {
                success: false,
                error: 'Cannot use --no-helpers flag with the --install flag',
            };
        }
    }
    if (flagResourceName && !validateFunctionName(flagResourceName)) {
        return {
            success: false,
            error: `Invalid function name: "${styleText('bold', flagResourceName)}"`,
        };
    }
    try {
        const fnName = flagResourceName || (await promptForFunctionName());
        if (blueprint.parsedBlueprint.resources?.some((r) => r.name === fnName)) {
            return {
                success: false,
                error: `Function "${styleText('bold', fnName)}" already exists.`,
            };
        }
        let fnTypes;
        if (flagType) {
            if (Array.isArray(flagType)) {
                fnTypes = flagType;
            }
            else {
                fnTypes = [flagType];
            }
        }
        else {
            fnTypes = await promptForFunctionType();
        }
        const fnLang = flagLang || (await promptForFunctionLang());
        if (fnTypes.length === 0) {
            throw new Error('At least one function type must be provided.');
        }
        if (!fnTypes.every((evt) => [
            'document-publish',
            'document-create',
            'document-delete',
            'document-update',
            'media-library-asset-create',
            'media-library-asset-update',
            'media-library-asset-delete',
        ].includes(evt))) {
            throw new Error('Invalid function type. Must be one of: document-publish, document-create, document-delete, document-update, media-library-asset-create, media-library-asset-update, media-library-asset-delete');
        }
        const eventSources = new Set(fnTypes.map((t) => t.substring(0, t.lastIndexOf('-'))));
        if (eventSources.size > 1) {
            throw new Error('Invalid function type. Cannot mix document-* and media-library-asset-* types.');
        }
        let addHelpers;
        let installCommand;
        if (!['ts', 'js'].includes(fnLang)) {
            addHelpers = false;
            installCommand = null;
        }
        else if (flagHelpers === false) {
            addHelpers = false;
            installCommand = null;
        }
        else if (flagI) {
            addHelpers = true;
            installCommand = 'npm';
        }
        else if (flagInstaller) {
            addHelpers = true;
            installCommand = flagInstaller === 'skip' ? null : flagInstaller;
        }
        else {
            addHelpers = flagHelpers || (await promptForAddHelpers());
            installCommand = addHelpers ? await promptForInstallCommand() : null;
        }
        if (installCommand)
            log(`${styleText('magenta', 'Installing')} with ${installCommand}...`);
        const { filePath, resourceAdded, resource } = await createFunctionResource({
            blueprintFilePath,
            name: fnName,
            type: fnTypes,
            lang: fnLang,
            addHelpers,
            installCommand,
        }, log);
        log(`\nCreated function: ${filePath.replace(root, '')}`);
        if (!resourceAdded) {
            log(`\n${styleText('bold', 'Add the Resource to your Blueprint:')}`);
            switch (blueprint.fileInfo.extension) {
                case '.ts':
                case '.js':
                case '.mjs': {
                    log(highlight(generateFunctionBlueprintResourceTemplate(fnName, fnTypes)));
                    break;
                }
                default:
                    log(highlight(JSON.stringify(resource, null, 2)));
                    break;
            }
        }
        else {
            log(`Function "${styleText('bold', fnName)}" added to Blueprint file.`);
        }
        return { success: true };
    }
    catch (err) {
        const errorMessage = err instanceof Error ? err.message : String(err);
        return {
            success: false,
            error: errorMessage,
        };
    }
}
async function promptForFunctionName() {
    const functionName = await input({
        message: 'Enter function name:',
        validate: (input) => validateFunctionName(input) ||
            'Invalid function name. Must be 6+ characters, no special characters, no spaces',
    });
    return functionName;
}
async function promptForFunctionType() {
    function hasAtLeastOne(arr) {
        // TypeScript believes me when I make a funciton to "guard" the type
        return arr.length > 0;
    }
    const functionTypes = await checkbox({
        message: 'Choose events to trigger your function:',
        choices: [
            { name: 'Document Create', value: 'document-create', checked: true },
            { name: 'Document Update', value: 'document-update', checked: true },
            { name: 'Document Delete', value: 'document-delete' },
            { name: 'Media Library Asset Create', value: 'media-library-asset-create' },
            { name: 'Media Library Asset Update', value: 'media-library-asset-update' },
            { name: 'Media Library Asset Delete', value: 'media-library-asset-delete' },
        ],
        validate(choices) {
            if (choices.length === 0) {
                return 'You must choose at least one function type / document change event';
            }
            if (choices.some((c) => String(c.value).startsWith('media-library')) &&
                choices.some((c) => String(c.value).startsWith('document'))) {
                return 'You cannot mix both Document and Media Library Asset events together in one Function';
            }
            return true;
        },
    });
    // checking functionTypes.length > 0 doesn't narrow the type
    // validate should prevent this from happening, but just in case
    if (!hasAtLeastOne(functionTypes)) {
        throw new Error('You must choose at least one function type / document change event');
    }
    return functionTypes;
}
async function promptForFunctionLang() {
    const functionLang = await select({
        message: 'Choose function language:',
        choices: [
            { name: 'TypeScript', value: 'ts' },
            { name: 'JavaScript', value: 'js' },
        ],
        default: 'ts',
    });
    return functionLang;
}
async function promptForAddHelpers() {
    const addHelpers = await confirm({
        message: 'Add @sanity/functions helpers to the new Function?',
        default: true,
    });
    return addHelpers;
}
async function promptForInstallCommand() {
    const command = await select({
        message: 'How to install the @sanity/functions helpers:',
        choices: [
            { name: 'npm', value: 'npm' },
            { name: 'pnpm', value: 'pnpm' },
            { name: 'yarn', value: 'yarn' },
            { name: 'Skip install', value: null },
        ],
        default: 'npm',
    });
    return command;
}
