import { Flags } from '@oclif/core';
import { LocalBlueprintCommand } from '../../baseCommands.js';
import { blueprintConfigCore } from '../../cores/blueprints/config.js';
import { Logger } from '../../utils/logger.js';
export default class ConfigCommand extends LocalBlueprintCommand {
    static summary = 'View or edit the local Blueprint configuration';
    static description = `Manages the local Blueprint configuration, which links your Blueprint to a Sanity project and Stack.

Without flags, displays the current configuration. Use --edit to interactively modify settings, or combine --edit with ID flags to update values directly (useful for scripting and automation).

If you need to switch your Blueprint to a different Stack, use --edit --stack.`;
    static examples = [
        '<%= config.bin %> <%= command.id %>',
        '<%= config.bin %> <%= command.id %> --edit',
        '<%= config.bin %> <%= command.id %> --edit --project-id <projectId>',
        '<%= config.bin %> <%= command.id %> --edit --project-id <projectId> --stack <name-or-id>',
    ];
    static flags = {
        edit: Flags.boolean({
            char: 'e',
            description: 'Modify the configuration interactively, or directly when combined with ID flags.',
            default: false,
        }),
        'project-id': Flags.string({
            description: 'Directly set the project ID in the configuration. Requires --edit flag',
            aliases: ['project', 'projectId'],
            dependsOn: ['edit'],
        }),
        'organization-id': Flags.string({
            description: 'Directly set the organization ID in the configuration. Requires --edit flag',
            aliases: ['organization', 'organizationId', 'org'],
            dependsOn: ['edit'],
            hidden: true,
        }),
        stack: Flags.string({
            description: 'Stack name or ID to set in the configuration. Requires --edit flag',
            aliases: ['stack-id', 'stackId'],
            dependsOn: ['edit'],
        }),
    };
    async run() {
        const { success, error } = await blueprintConfigCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            blueprint: this.blueprint,
            token: this.sanityToken,
            validateResources: this.flags['validate-resources'],
            flags: this.flags,
        });
        if (!success)
            this.error(error);
    }
}
