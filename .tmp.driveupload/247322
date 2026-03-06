import { Flags } from '@oclif/core';
import { DeployedStackCommand, stackFlag, unhide } from '../../baseCommands.js';
import { blueprintLogsCore } from '../../cores/blueprints/logs.js';
import { Logger } from '../../utils/logger.js';
export default class LogsCommand extends DeployedStackCommand {
    static summary = "Display logs for the current Blueprint's Stack deployment";
    static description = `Retrieves Stack deployment logs, useful for debugging and monitoring deployment activity.

Use --watch (-w) to stream logs in real-time.

If you're not seeing expected logs, verify your Stack is deployed with 'blueprints info'.`;
    static examples = [
        '<%= config.bin %> <%= command.id %>',
        '<%= config.bin %> <%= command.id %> --watch',
    ];
    static flags = {
        stack: unhide(stackFlag),
        watch: Flags.boolean({
            char: 'w',
            description: 'Watch for new Stack logs (streaming mode)',
            aliases: ['follow'],
        }),
    };
    async run() {
        const { success, streaming, error } = await blueprintLogsCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            auth: this.auth,
            stackId: this.stackId,
            deployedStack: this.deployedStack,
            validateResources: this.flags['validate-resources'],
            flags: this.flags,
        });
        if (streaming)
            return streaming;
        if (!success)
            this.error(error);
    }
}
