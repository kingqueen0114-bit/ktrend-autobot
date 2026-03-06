import { readFileSync } from 'node:fs';
import { arch, cwd, version as nodeVersion, platform } from 'node:process';
import * as resolve from 'empathic/resolve';
import ora from 'ora';
import { readLocalBlueprint, } from '../../actions/blueprints/blueprint.js';
import { getStack } from '../../actions/blueprints/stacks.js';
import config, { RUNTIME_CLI_VERSION } from '../../config.js';
import { check, filePathRelativeToCwd, niceId, severe, unsure, } from '../../utils/display/presenters.js';
import { styleText } from '../../utils/style-text.js';
import { createTracedFetch } from '../../utils/traced-fetch.js';
import { validTokenOrErrorMessage } from '../../utils/validated-token.js';
import { blueprintConfigCore } from './config.js';
const diagLookup = {
    online: 'Host online',
    tokenValid: 'Authenticated',
    blueprintValid: 'Blueprint valid',
    stackReady: 'Stack ready',
    userHasAccess: 'User has access',
};
function sourceLabel(source) {
    switch (source) {
        case 'env':
            return 'environment';
        case 'module':
            return 'blueprint module';
        case 'config':
            return 'config file';
        case 'inferred':
            return 'inferred';
        default:
            return 'unknown';
    }
}
function renderSection(emit, title, rows) {
    const pad = Math.max(...rows.map(([l]) => l.length)) + 3;
    emit(styleText('bold', title));
    for (const [label, value] of rows) {
        emit(`  ${styleText('dim', label.padEnd(pad))}${value}`);
    }
}
export async function blueprintDoctorCore(options) {
    const { bin, log, token, validateResources, flags: { verbose: v, path: p, fix }, } = options;
    const path = p || cwd();
    let tokenOrError;
    const diagnostics = {};
    for (const key in diagLookup) {
        diagnostics[key] = { status: null };
    }
    const envRows = [['Directory', p ? filePathRelativeToCwd(path) : path]];
    const configRows = [];
    const stackRows = [];
    const spinner = ora('Running diagnostics...').start();
    // --- ONLINE ---
    const fetchFn = createTracedFetch(log);
    try {
        const res = await fetchFn(config.apiUrl);
        if (res.ok) {
            diagnostics.online = { status: true };
        }
        else {
            diagnostics.online = { status: false, detail: `${res.status} ${res.statusText}` };
        }
    }
    catch (err) {
        const reason = err instanceof Error ? err.message : 'unknown error';
        diagnostics.online = { status: false, detail: reason };
    }
    // --- TOKEN ---
    if (token) {
        tokenOrError = await validTokenOrErrorMessage(log, token);
        if (tokenOrError.ok) {
            diagnostics.tokenValid = { status: true };
        }
        else {
            diagnostics.tokenValid = { status: false, detail: tokenOrError.error.message };
        }
    }
    else {
        diagnostics.tokenValid = { status: false, detail: 'no token found' };
    }
    // --- BLUEPRINT ---
    let localBlueprint;
    try {
        localBlueprint = await readLocalBlueprint(log, { resources: options.validateResources || false }, path);
        envRows.push(['Blueprint', filePathRelativeToCwd(localBlueprint.fileInfo.blueprintFilePath)]);
        if (localBlueprint.errors.length === 0) {
            diagnostics.blueprintValid = { status: true };
        }
        else {
            diagnostics.blueprintValid = {
                status: false,
                detail: `${localBlueprint.errors.length} error(s)`,
            };
        }
    }
    catch {
        diagnostics.blueprintValid = { status: false, detail: 'unable to read file' };
    }
    envRows.push(['API URL', config.apiUrl]);
    envRows.push(['Runtime', `Node.js ${nodeVersion} (${platform}-${arch})`]);
    if (RUNTIME_CLI_VERSION) {
        envRows.push(['Internals', `v${RUNTIME_CLI_VERSION}`]);
    }
    const sanityCliPkgPath = resolve.from(path, '@sanity/cli/package.json', true);
    if (sanityCliPkgPath) {
        try {
            const sanityCliPkg = JSON.parse(readFileSync(sanityCliPkgPath, 'utf8'));
            envRows.push(['Sanity CLI', sanityCliPkg.version]);
        }
        catch { }
    }
    // --- CONFIGURATION ---
    if (localBlueprint) {
        const { scopeType, scopeId, stackId, sources, blueprintConfig } = localBlueprint;
        if (blueprintConfig && 'configPath' in blueprintConfig && blueprintConfig.configPath) {
            configRows.push(['Source', filePathRelativeToCwd(blueprintConfig.configPath)]);
        }
        else if (!blueprintConfig) {
            configRows.push(['Source', styleText('dim', 'no config file')]);
        }
        if (blueprintConfig?.updatedAt) {
            configRows.push(['Updated', new Date(blueprintConfig.updatedAt).toLocaleString('sv-SE')]);
        }
        if (scopeType && scopeId) {
            const scopeSourceKey = scopeType === 'project' ? 'projectId' : 'organizationId';
            const label = scopeType === 'project' ? 'Project' : 'Organization';
            configRows.push([
                label,
                `${niceId(scopeId)}  ${styleText('dim', sourceLabel(sources?.[scopeSourceKey]))}`,
            ]);
        }
        if (stackId) {
            configRows.push([
                'Stack',
                `${niceId(stackId)}  ${styleText('dim', sourceLabel(sources?.stackId))}`,
            ]);
        }
        // --- STACK + ACCESS ---
        if (diagnostics.online.status &&
            diagnostics.tokenValid.status &&
            token &&
            stackId &&
            scopeType &&
            scopeId) {
            const stackResponse = await getStack({
                auth: { token, scopeType, scopeId },
                stackId,
                logger: log,
            });
            if (stackResponse.ok) {
                diagnostics.stackReady = { status: true };
                diagnostics.userHasAccess = { status: true };
                const stack = stackResponse.stack;
                if (stack) {
                    const label = stack.name ? `"${stack.name}" ${niceId(stackId)}` : niceId(stackId);
                    stackRows.push(['Stack', label]);
                    if (stack.recentOperation) {
                        const op = stack.recentOperation;
                        const time = op.completedAt || op.createdAt;
                        const timestamp = time
                            ? `  ${styleText('dim', new Date(time).toLocaleString('sv-SE'))}`
                            : '';
                        stackRows.push(['Operation', `${op.status}${timestamp}`]);
                    }
                }
            }
            else if (stackResponse.response?.status === 404) {
                diagnostics.stackReady = {
                    status: false,
                    detail: `Stack ${niceId(stackId)} not found (404)`,
                };
            }
            else if (stackResponse.response?.status === 403 || stackResponse.response?.status === 401) {
                diagnostics.userHasAccess = {
                    status: false,
                    detail: `no access to Stack ${niceId(stackId)} (${stackResponse.response.status})`,
                };
            }
            else {
                const statusSuffix = stackResponse.response?.status
                    ? ` (${stackResponse.response.status})`
                    : '';
                diagnostics.stackReady = {
                    status: null,
                    detail: (stackResponse.error || 'unknown error') + statusSuffix,
                };
                diagnostics.userHasAccess = { status: null, detail: `unknown error${statusSuffix}` };
            }
        }
        else if (stackId && scopeType && scopeId) {
            diagnostics.stackReady = { status: null, detail: 'requires online + authenticated' };
            diagnostics.userHasAccess = { status: null, detail: 'requires online + authenticated' };
        }
        else if (!stackId && !scopeType && !scopeId) {
            diagnostics.stackReady = { status: null, detail: 'missing configuration' };
            diagnostics.userHasAccess = { status: null, detail: 'missing configuration' };
        }
        else {
            const missing = [];
            if (!stackId)
                missing.push('Stack ID');
            if (!scopeType)
                missing.push('Scope Type');
            if (!scopeId) {
                const scopeLabel = scopeType === 'project'
                    ? 'Project ID'
                    : scopeType === 'organization'
                        ? 'Organization ID'
                        : 'Scope ID';
                missing.push(scopeLabel);
            }
            const detail = `missing ${missing.join(', ')}`;
            diagnostics.stackReady = { status: null, detail };
            diagnostics.userHasAccess = { status: null, detail };
        }
    }
    // --- RENDER REPORT ---
    spinner.stop();
    // Environment (verbose)
    renderSection((msg) => log.verbose(msg), 'Environment', envRows);
    log.verbose('');
    // Configuration (verbose)
    if (configRows.length > 0) {
        renderSection((msg) => log.verbose(msg), 'Configuration', configRows);
        log.verbose('');
    }
    // Deployment (verbose)
    if (stackRows.length > 0) {
        renderSection((msg) => log.verbose(msg), 'Deployment', stackRows);
        log.verbose('');
    }
    // Checks (always visible)
    const maxLabel = Math.max(...Object.values(diagLookup).map((l) => l.length));
    log(styleText('bold', 'Checks'));
    let allGood = true;
    for (const [key, entry] of Object.entries(diagnostics)) {
        const label = diagLookup[key].padEnd(maxLabel);
        const detail = entry.detail ? `  ${styleText('dim', entry.detail)}` : '';
        switch (entry.status) {
            case true:
                log(`  ${check(label)}${detail}`);
                break;
            case false:
                allGood = false;
                log(`  ${severe(label)}${detail}`);
                break;
            case null:
                allGood = false;
                log(`  ${unsure(label)}${detail}`);
                break;
        }
    }
    // Result
    const flatDiagnostics = {};
    for (const [key, entry] of Object.entries(diagnostics)) {
        flatDiagnostics[key] = entry.status;
    }
    log('');
    const errorMessage = 'One or more checks failed';
    if (allGood) {
        log(styleText(['bold', 'green'], 'All checks passed'));
        if (fix)
            log(styleText(['bold', 'yellow'], 'Nothing to fix; --fix flag is ignored'));
        return { success: true, data: { diagnostics: flatDiagnostics } };
    }
    if (fix) {
        if (p) {
            return {
                success: false,
                error: `${errorMessage}. --fix cannot be used with --path`,
                data: { diagnostics: flatDiagnostics },
            };
        }
        if (!tokenOrError) {
            return {
                success: false,
                error: `${errorMessage}. Unable to fix: Missing authentication token`,
                data: { diagnostics: flatDiagnostics },
            };
        }
        if (tokenOrError?.ok === false) {
            return {
                success: false,
                error: `${errorMessage}. Unable to fix: ${tokenOrError.error.message}`,
                data: { diagnostics: flatDiagnostics },
            };
        }
        if (!localBlueprint) {
            return {
                success: false,
                error: `${errorMessage}. Unable to fix: Blueprint is missing or invalid`,
                data: { diagnostics: flatDiagnostics },
            };
        }
        return blueprintConfigCore({
            bin,
            log,
            token: tokenOrError.value,
            blueprint: localBlueprint,
            validateResources,
            flags: { edit: true, verbose: v },
        });
    }
    log(styleText('dim', `  Run \`${bin} blueprints doctor --fix\` to resolve configuration issues.`));
    return { success: false, error: errorMessage, data: { diagnostics: flatDiagnostics } };
}
