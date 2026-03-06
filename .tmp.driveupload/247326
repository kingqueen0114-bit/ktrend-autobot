import { Flags } from '@oclif/core';
import { LocalBlueprintCommand } from '../../baseCommands.js';
import { blueprintStacksCore } from '../../cores/blueprints/stacks.js';
import { Logger } from '../../utils/logger.js';
export default class StacksCommand extends LocalBlueprintCommand {
    static summary = "List all remote Stack deployments (defaults to the current Blueprint's project scope)";
    static description = `Shows all Stacks associated with a project or organization. By default, lists Stacks scoped to the local Blueprint.

Use this to discover existing Stacks you can scope a local Blueprint to (using 'blueprints config --edit'), or to audit what's deployed across your project.`;
    static examples = [
        '<%= config.bin %> <%= command.id %>',
        '<%= config.bin %> <%= command.id %> --project-id <projectId>',
        '<%= config.bin %> <%= command.id %> --organization-id <organizationId>',
    ];
    static flags = {
        'project-id': Flags.string({
            description: 'Project ID to show Stack deployments for',
            aliases: ['projectId', 'project'],
            exclusive: ['organization-id'],
        }),
        'organization-id': Flags.string({
            description: 'Organization ID to show Stack deployments for',
            aliases: ['organizationId', 'organization', 'org'],
            exclusive: ['project-id'],
            hidden: true,
        }),
    };
    async run() {
        const { success, error } = await blueprintStacksCore({
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
