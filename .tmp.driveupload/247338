import { Flags } from '@oclif/core';
import { LocalBlueprintCommand } from '../../baseCommands.js';
import { blueprintDestroyCore } from '../../cores/blueprints/destroy.js';
import { Logger } from '../../utils/logger.js';
export default class DestroyCommand extends LocalBlueprintCommand {
    static summary = 'Destroy the remote Stack deployment and its resources (will not delete local files)';
    static description = `Permanently removes the remote Stack and all its provisioned resources. Your local Blueprint files remain untouched, allowing you to redeploy later with 'blueprints init' + 'blueprints deploy'.

This is a destructive operation. You will be prompted to confirm unless --force is specified.

Use this to clean up test environments or decommission a Stack you no longer need.`;
    static examples = [
        '<%= config.bin %> <%= command.id %>',
        '<%= config.bin %> <%= command.id %> --stack <name-or-id> --project-id <projectId> --force --no-wait',
    ];
    static flags = {
        force: Flags.boolean({
            description: 'Force Stack destruction (skip confirmation)',
            aliases: ['f'],
            default: false,
        }),
        'project-id': Flags.string({
            description: 'Project associated with the Stack',
            aliases: ['projectId', 'project'],
            dependsOn: ['stack', 'force'],
            exclusive: ['organization-id'],
        }),
        'organization-id': Flags.string({
            description: 'Organization associated with the Stack',
            aliases: ['organizationId', 'organization', 'org'],
            dependsOn: ['stack', 'force'],
            exclusive: ['project-id'],
            hidden: true,
        }),
        stack: Flags.string({
            description: 'Stack name or ID to destroy (defaults to the locally configured Stack)',
            aliases: ['stack-id', 'stackId'],
        }),
        'no-wait': Flags.boolean({
            description: 'Do not wait for Stack destruction to complete',
            default: false,
        }),
    };
    async run() {
        const { success, error } = await blueprintDestroyCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            token: this.sanityToken,
            blueprint: this.blueprint,
            validateResources: this.flags['validate-resources'],
            flags: this.flags,
        });
        if (!success)
            this.error(error);
    }
}
