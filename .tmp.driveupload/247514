import { planStack, resolveStackIdByNameOrId } from '../../actions/blueprints/stacks.js';
import { formatDeploymentPlan, formatResourceTree, hasActionableChanges, } from '../../utils/display/blueprints-formatting.js';
import { styleText } from '../../utils/style-text.js';
export async function blueprintPlanCore(options) {
    const { bin = 'sanity', log, blueprint, token, flags } = options;
    const { verbose: _verbose = false } = flags;
    const { scopeType, scopeId, stackId: blueprintStackId, parsedBlueprint, fileInfo } = blueprint;
    log(`${styleText(['bold', 'blueBright'], 'Local Blueprint')} ${styleText('dim', `(${fileInfo.fileName})`)}`);
    log(formatResourceTree(parsedBlueprint.resources));
    if (!token || !scopeType || !scopeId) {
        log(styleText('dim', 'Unable to retrieve live Stack deployment for comparison'));
        const errorMessage = !token
            ? `Missing authentication token. Run \`${bin} login\` to authenticate.`
            : `Missing Blueprint configuration. Run \`${bin} blueprints doctor --fix\` to repair.`;
        return {
            success: false,
            error: errorMessage,
        };
    }
    const stackId = flags.stack
        ? await resolveStackIdByNameOrId(flags.stack, { token, scopeType, scopeId }, log)
        : blueprintStackId;
    if (!stackId) {
        log(styleText('dim', 'Unable to retrieve live Stack deployment for comparison'));
        return {
            success: false,
            error: `Missing Stack deployment configuration. Run \`${bin} blueprints doctor --fix\` to repair.`,
        };
    }
    const auth = { token, scopeType, scopeId };
    const spinner = log.ora('Generating deployment plan...').start();
    const planResponse = await planStack({
        stackId,
        document: parsedBlueprint,
        auth,
        logger: log,
    });
    spinner.stop().clear();
    if (!planResponse.ok) {
        if (planResponse.problems) {
            log('');
            for (const problem of planResponse.problems) {
                const messages = problem.message
                    .split('\n')
                    .map((s) => s.trim())
                    .filter(Boolean);
                for (const msg of messages) {
                    log(`  ${styleText(['bold', 'red'], '✘')} ${msg}`);
                }
            }
            log(`\n  Fix the issues above before running "${styleText(['bold', 'magenta'], `${bin} blueprints deploy`)}"`);
        }
        else {
            log(styleText('dim', '\nUnable to retrieve deployment plan from server'));
        }
        return { success: false, error: 'Deployment plan has problems' };
    }
    log('');
    log(formatDeploymentPlan(planResponse.deploymentPlan));
    if (hasActionableChanges(planResponse.deploymentPlan)) {
        log(`\n  Run "${styleText(['bold', 'magenta'], `${bin} blueprints deploy`)}" to apply these Stack changes`);
    }
    else {
        log(`\n  ${styleText('dim', `No significant changes to deploy. Run \`${bin} blueprints deploy\` to apply.`)}`);
    }
    return { success: true };
}
