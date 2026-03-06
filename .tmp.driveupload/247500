import { getLogs, getRecentLogs } from '../../actions/blueprints/logs.js';
import { setupLogStreaming } from '../../actions/blueprints/logs-streaming.js';
import { formatTitle } from '../../utils/display/blueprints-formatting.js';
import { formatLogEntry, formatLogs } from '../../utils/display/logs-formatting.js';
import { niceId } from '../../utils/display/presenters.js';
import { styleText } from '../../utils/style-text.js';
export async function blueprintLogsCore(options) {
    const { log, auth, stackId, deployedStack, flags } = options;
    const { watch = false, verbose = false } = flags;
    const spinner = log.ora(`Fetching recent logs for Stack deployment ${niceId(stackId)}`).start();
    try {
        if (watch) {
            const { ok, logs, error } = await getLogs(stackId, auth, log);
            if (!ok) {
                spinner.fail(`${styleText('red', 'Failed')} to retrieve logs`);
                log.error(`Error: ${error || 'Unknown error'}`);
                return { success: false, error: error || 'Failed to retrieve logs' };
            }
            spinner.stop();
            log(`${formatTitle('Blueprint', deployedStack.name)} ${niceId(stackId)} logs`);
            if (logs.length > 0) {
                log('\nMost recent logs:');
                const recentLogs = getRecentLogs(logs);
                let previousLog;
                for (const logEntry of recentLogs) {
                    log(formatLogEntry(logEntry, verbose, previousLog));
                    previousLog = logEntry;
                }
            }
            else {
                log(`No recent logs found for Stack deployment ${niceId(stackId)}`);
            }
            // Set up streaming log display
            await setupLogStreaming({
                stackId,
                auth,
                log,
                showBanner: true,
                verbose,
            });
            // Return a special key for streaming mode
            return {
                success: true,
                streaming: new Promise(() => { }),
            };
        }
        // Regular non-streaming logs
        const { ok, logs, error } = await getLogs(stackId, auth, log);
        if (!ok) {
            spinner.fail(`${styleText('red', 'Failed')} to retrieve Stack deployment logs`);
            log.error(`Error: ${error || 'Unknown error'}`);
            return { success: false, error: error || 'Failed to retrieve logs' };
        }
        if (logs.length === 0) {
            spinner.info(`No logs found for Stack deployment ${stackId}`);
            return { success: true };
        }
        spinner.succeed(`${formatTitle('Blueprint', deployedStack.name)} Logs`);
        log(`Found ${styleText('bold', logs.length.toString())} log entries for Stack deployment ${niceId(stackId)}\n`);
        log(formatLogs(logs, verbose));
        return { success: true };
    }
    catch (err) {
        spinner.fail('Failed to retrieve Stack deployment logs');
        const errorMessage = err instanceof Error ? err.message : String(err);
        log.error(`Error: ${errorMessage}`);
        return { success: false, error: errorMessage };
    }
}
