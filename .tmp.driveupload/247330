import { Flags } from '@oclif/core';
import { DeployedStackCommand, stackFlag, unhide } from '../../baseCommands.js';
import { blueprintDeployCore } from '../../cores/blueprints/deploy.js';
import { Logger } from '../../utils/logger.js';
export default class DeployCommand extends DeployedStackCommand {
    static summary = 'Deploy the local Blueprint to the remote Stack';
    static description = `Pushes your local Blueprint configuration to the remote Stack; provisioning, updating, or destroying resources as needed. This is the primary command for applying infrastructure changes.

Before deploying, run 'blueprints plan' to preview changes. After deployment, use 'blueprints info' to verify Stack status or 'blueprints logs' to monitor activity.

Use --no-wait to queue the deployment and return immediately without waiting for completion.

Set SANITY_ASSET_TIMEOUT (seconds) to override the 60-second timeout for processing resource assets.`;
    static examples = [
        '<%= config.bin %> <%= command.id %>',
        '<%= config.bin %> <%= command.id %> --no-wait',
    ];
    static flags = {
        stack: unhide(stackFlag),
        'no-wait': Flags.boolean({
            description: 'Do not wait for Stack deployment to complete',
            default: false,
        }),
        'new-stack-name': Flags.string({
            description: 'Set a new name for the Stack',
            hidden: true,
        }),
    };
    async run() {
        const { success, error } = await blueprintDeployCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            auth: this.auth,
            stackId: this.stackId,
            scopeType: this.scopeType,
            scopeId: this.scopeId,
            deployedStack: this.deployedStack,
            blueprint: this.blueprint,
            validateResources: this.flags['validate-resources'],
            flags: this.flags,
        });
        if (!success)
            this.error(error);
    }
}
