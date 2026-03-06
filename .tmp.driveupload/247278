import { Args, Flags } from '@oclif/core';
import { DeployedStackCommand, stackFlag, unhide } from '../../baseCommands.js';
import { functionLogsCore } from '../../cores/functions/logs.js';
import { Logger } from '../../utils/logger.js';
export default class LogsCommand extends DeployedStackCommand {
    static summary = 'Retrieve or delete logs for a Sanity Function';
    static description = `Fetches execution logs from a deployed function, useful for debugging production issues or monitoring activity.

Use --watch (-w) to stream logs in real-time. Use --delete to clear all logs for a function (requires confirmation unless --force is specified).`;
    static args = {
        name: Args.string({ description: 'The name of the Sanity Function', required: false }),
    };
    static examples = [
        '<%= config.bin %> <%= command.id %> <name>',
        '<%= config.bin %> <%= command.id %> <name> --json',
        '<%= config.bin %> <%= command.id %> <name> --limit 100',
        '<%= config.bin %> <%= command.id %> <name> --delete',
    ];
    static flags = {
        stack: unhide(stackFlag),
        limit: Flags.integer({
            char: 'l',
            description: 'Total number of log entries to retrieve',
            required: false,
            default: 50,
        }),
        json: Flags.boolean({
            char: 'j',
            description: 'Return logs in JSON format',
            required: false,
        }),
        utc: Flags.boolean({
            char: 'u',
            description: 'Show dates in UTC time zone',
            required: false,
        }),
        delete: Flags.boolean({
            char: 'd',
            exclusive: ['limit', 'json'],
            description: 'Delete all logs for the function',
            required: false,
        }),
        force: Flags.boolean({
            char: 'f',
            dependsOn: ['delete'],
            description: 'Skip confirmation for deleting logs',
            required: false,
        }),
        watch: Flags.boolean({
            char: 'w',
            description: 'Watch for new logs (streaming mode)',
            aliases: ['follow'],
        }),
    };
    async run() {
        const { success, error } = await functionLogsCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            error: (msg, options) => this.error(msg, options),
            args: this.args,
            flags: this.flags,
            auth: this.auth,
            blueprint: this.blueprint,
            deployedStack: this.deployedStack,
            scopeType: this.scopeType,
            scopeId: this.scopeId,
            token: this.sanityToken,
            stackId: this.stackId,
            helpText: LogsCommand.getHelpText(this.config.bin, 'functions logs'),
            validateResources: this.flags['validate-resources'],
        });
        if (!success)
            this.error(error);
    }
}
