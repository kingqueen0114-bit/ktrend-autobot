import { Args, Flags } from '@oclif/core';
import { baseFlags, RuntimeCommand, unhide } from '../../baseCommands.js';
import { blueprintInitCore } from '../../cores/blueprints/init.js';
import { Logger } from '../../utils/logger.js';
import { validTokenOrErrorMessage } from '../../utils/validated-token.js';
export default class InitCommand extends RuntimeCommand {
    static summary = 'Initialize a local Blueprint and optionally provision a remote Stack deployment';
    static description = `A Blueprint is your local infrastructure-as-code configuration that defines Sanity resources (datasets, functions, etc.). A Stack is the remote deployment target where your Blueprint is applied.
[NOTE: Currently, accounts are limited to three (3) Stacks per project scope.]

This is typically the first command you run in a new project. It creates a local Blueprint manifest file (sanity.blueprint.ts, .js, or .json) and provisions a new remote Stack.
Additionally, a Blueprint configuration file is created in .sanity/ containing the scope and Stack IDs. This is .gitignored by default.

After initialization, use 'blueprints plan' to preview changes, then 'blueprints deploy' to apply them.`;
    static examples = [
        '<%= config.bin %> <%= command.id %>',
        '<%= config.bin %> <%= command.id %> [directory]',
        '<%= config.bin %> <%= command.id %> --blueprint-type <json|js|ts>',
        '<%= config.bin %> <%= command.id %> --blueprint-type <json|js|ts> --project-id <projectId> --stack-id <stackId>',
        '<%= config.bin %> <%= command.id %> --blueprint-type <json|js|ts> --stack-name <stackName>',
    ];
    static args = {
        dir: Args.string({
            description: 'Directory to create the local Blueprint in',
        }),
    };
    static flags = {
        dir: Flags.string({
            description: 'Directory to create the local Blueprint in',
        }),
        example: Flags.string({
            description: 'Example to use for the local Blueprint',
            aliases: ['recipe'],
            exclusive: ['blueprint-type', 'stack-id', 'stack-name'], // set automatically
        }),
        'blueprint-type': Flags.string({
            description: 'Blueprint manifest type to use for the local Blueprint',
            options: ['json', 'js', 'ts'],
            aliases: ['type'],
        }),
        'project-id': Flags.string({
            description: 'Sanity project ID used to scope local Blueprint and remote Stack',
            aliases: ['project', 'projectId'],
        }),
        'organization-id': Flags.string({
            description: 'Sanity organization ID used to scope local Blueprint and remote Stack',
            aliases: ['organization', 'organizationId', 'org'],
            hidden: true,
        }),
        'stack-id': Flags.string({
            description: 'Existing Stack ID used to scope local Blueprint',
            aliases: ['stackId'],
            dependsOn: ['project-id'],
            exclusive: ['stack-name'],
        }),
        'stack-name': Flags.string({
            description: 'Name to use for a new Stack provisioned during initialization',
            aliases: ['name'],
            exclusive: ['stack-id'],
        }),
        verbose: unhide(baseFlags.verbose),
    };
    async run() {
        const log = Logger(this.log.bind(this), this.flags);
        const result = await validTokenOrErrorMessage(log);
        if (!result.ok)
            this.error(result.error.message);
        const { success, error } = await blueprintInitCore({
            bin: this.config.bin,
            log,
            token: result.value,
            validateResources: this.flags['validate-resources'],
            args: this.args,
            flags: this.flags,
        });
        if (!success)
            this.error(error);
    }
}
