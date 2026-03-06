import { confirm } from '@inquirer/prompts';
import { deleteLogs as deleteLogsAction, logs as getLogsAction, streamLogs as streamLogsAction, } from '../../actions/functions/logs.js';
import { formatTitle } from '../../utils/display/blueprints-formatting.js';
import { niceId } from '../../utils/display/presenters.js';
import { findFunctionInStack, getFunctionNames } from '../../utils/find-function.js';
import { styleText } from '../../utils/style-text.js';
export async function functionLogsCore(options) {
    const { args, flags, log, error, auth, deployedStack, blueprint, helpText } = options;
    const { name } = args;
    const { delete: shouldDelete, watch: shouldWatch, force, limit, json, utc } = flags;
    if (!name) {
        const functionNames = getFunctionNames(blueprint.parsedBlueprint.resources);
        const validNames = functionNames.length > 0
            ? `Valid names are: ${functionNames.join(', ')}`
            : 'No functions are defined in the blueprint.';
        error(`Missing required argument: name\n${validNames}\n`, { exit: false });
        log(helpText);
        return { success: true };
    }
    const { externalId } = findFunctionInStack(deployedStack, name); // throws if not found
    if (shouldDelete)
        return deleteLogs({ name, externalId, auth, force, log });
    if (shouldWatch)
        return streamLogs({ name, externalId, auth, json, utc, log });
    return getLogs({ name, externalId, auth, limit, json, utc, log });
}
async function deleteLogs({ name, externalId, auth, force, log, }) {
    if (!force) {
        const certain = await confirm({
            message: `Are you sure you want to delete ${styleText('bold', 'all')} logs for function ${styleText('yellow', name)}?`,
            default: false,
        });
        if (!certain)
            return { success: true };
    }
    const spinner = log.ora(`Deleting logs for function ${styleText('yellow', name)}`).start();
    const { ok, error } = await deleteLogsAction(externalId, auth, log);
    if (!ok) {
        spinner.fail(`${styleText('red', 'Failed')} to delete logs`);
        return { success: false, error: error || 'Unknown error' };
    }
    spinner.succeed('Logs deleted');
    return { success: true };
}
async function streamLogs({ name, externalId, auth, log, }) {
    const spinner = log.ora(`Setting up streaming logs session for function ${niceId(name)}`).start();
    try {
        spinner.stop();
        log(`Streaming log session for function ${niceId(name)}`);
        log(`Watching for new logs... ${styleText('bold', 'ctrl+c')} to stop`);
        let alreadyOpened = false;
        const onOpen = () => {
            if (alreadyOpened)
                log(`${styleText('green', 'Reconnected')}`);
            alreadyOpened = true;
        };
        const renderLog = (logEntry) => {
            const { time, level, message } = logEntry;
            log(formatLog(time, level, message, true));
        };
        streamLogsAction(externalId, auth, renderLog, onOpen, (error) => log.error(`${styleText('red', 'Error:')} ${error}`), log);
        // Return a special key for streaming mode
        return {
            success: true,
            streaming: new Promise(() => { }),
        };
    }
    catch (err) {
        spinner.fail('Failed to retrieve logs');
        const errorMessage = err instanceof Error ? err.message : String(err);
        log.error(`Error: ${errorMessage}`);
        return { success: false, error: errorMessage };
    }
}
async function getLogs({ name, externalId, auth, limit, json, utc, log, }) {
    const spinner = log.ora(`Finding logs for function "${name}"`).start();
    const { ok, error, logs, total } = await getLogsAction(externalId, { limit }, auth, log);
    if (!ok) {
        spinner.fail(`${styleText('red', 'Failed')} to retrieve logs`);
        return { success: false, error: error || 'Unknown error' };
    }
    const filteredLogs = logs.filter((entry) => entry.level && entry.message);
    if (filteredLogs.length === 0) {
        spinner.info(`No logs found for function ${name}`);
        return { success: true };
    }
    spinner.succeed(`${formatTitle('Function', name)} Logs`);
    if (!json) {
        log(`Found ${styleText('bold', String(total))} log entries for function ${styleText('yellow', name)}`);
        if (logs.length < total) {
            log(`Here are the last ${styleText('bold', filteredLogs.length.toString())} entries`);
        }
        log('\n');
        for (const { time, level, message } of filteredLogs) {
            log(formatLog(time, level, message, utc));
        }
    }
    else {
        log(JSON.stringify(filteredLogs, null, 2));
    }
    return { success: true };
}
function formatLog(time, level, message, utc) {
    const date = new Date(time);
    const [dateString, timeString] = utc
        ? date.toISOString().slice(0, 19).split('T')
        : [date.toLocaleDateString(), date.toLocaleTimeString()];
    return [
        styleText('bold', dateString),
        styleText(['bold', 'blue'], timeString),
        logLevel(level.toUpperCase()),
        message,
    ].join(' ');
}
function logLevel(level) {
    if (level === 'ERROR')
        return styleText('red', level);
    if (level === 'WARN')
        return styleText('yellow', level);
    return styleText('green', level);
}
