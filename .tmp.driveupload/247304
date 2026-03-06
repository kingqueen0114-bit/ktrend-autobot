import { Flags } from '@oclif/core';
import { DeployedStackCommand } from '../../baseCommands.js';
import { blueprintInfoCore } from '../../cores/blueprints/info.js';
import { Logger } from '../../utils/logger.js';
export default class InfoCommand extends DeployedStackCommand {
    static summary = "Show information about the local Blueprint's remote Stack deployment";
    static description = `Displays the current state and metadata of your remote Stack deployment, including deployed resources, status, and configuration.

Use this command to verify a deployment succeeded, check what resources are live, or confirm which Stack your local Blueprint is connected to.

Run 'blueprints stacks' to see all available Stacks in your project or organization.`;
    static examples = [
        '<%= config.bin %> <%= command.id %>',
        '<%= config.bin %> <%= command.id %> --stack <name-or-id>',
    ];
    static flags = {
        stack: Flags.string({
            description: 'Stack name or ID to use instead of the locally configured Stack',
            aliases: ['id'],
        }),
    };
    async run() {
        const { success, error } = await blueprintInfoCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            stackId: this.stackId,
            deployedStack: this.deployedStack,
            validateResources: this.flags['validate-resources'],
            flags: this.flags,
        });
        if (!success)
            this.error(error);
    }
}
