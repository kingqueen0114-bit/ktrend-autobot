/**
 * @file
 * @deprecated Use `functions add` instead.
 * We're in the process of deprecating the `blueprints add` command.
 */
import { Args, Flags } from '@oclif/core';
import { LocalBlueprintCommand } from '../../baseCommands.js';
import { functionAddCore } from '../../cores/functions/index.js';
import { Logger } from '../../utils/logger.js';
// import {warn} from '../../utils/display/presenters.js'
export default class AddCommand extends LocalBlueprintCommand {
    // static state = 'deprecated'
    // static deprecationOptions = {
    //   message: '`blueprints add` is deprecated. Use `functions add` instead.',
    // }
    static summary = 'Add a function resource to a Blueprint';
    static description = `Scaffolds a new Sanity Function in your Blueprint. Functions are serverless handlers triggered by document events (create, update, delete, publish) or media library events.

After adding a function, use 'functions dev' to test locally, then 'blueprints deploy' to publish it.`;
    static examples = [
        '<%= config.bin %> <%= command.id %> function',
        '<%= config.bin %> <%= command.id %> function --helpers',
        '<%= config.bin %> <%= command.id %> function --name my-function',
        '<%= config.bin %> <%= command.id %> function --name my-function --fn-type document-create',
        '<%= config.bin %> <%= command.id %> function --name my-function --fn-type document-create --fn-type document-update --lang js',
    ];
    static args = {
        type: Args.string({
            description: 'Type of resource to add (only "function" is supported)',
            options: ['function'],
            required: true,
        }),
    };
    static flags = {
        example: Flags.string({
            description: 'Example to use for the function resource. Discover examples at https://www.sanity.io/exchange/type=recipes/by=sanity',
            aliases: ['recipe'],
            exclusive: ['name', 'fn-type', 'language', 'javascript', 'fn-helpers', 'fn-installer'],
        }),
        name: Flags.string({
            description: 'Name of the resource to add',
            char: 'n',
        }),
        'fn-type': Flags.string({
            description: 'Document change event(s) that should trigger the function; you can specify multiple events by specifying this flag multiple times',
            options: [
                'document-create',
                'document-delete',
                'document-update',
                'document-publish',
                'media-library-asset-create',
                'media-library-asset-update',
                'media-library-asset-delete',
            ],
            aliases: ['function-type'],
            multiple: true,
            multipleNonGreedy: true,
            dependsOn: ['name'],
        }),
        language: Flags.string({
            description: 'Language of the new function',
            aliases: ['function-language', 'fn-language', 'lang'],
            options: ['ts', 'js'],
            default: 'ts',
        }),
        javascript: Flags.boolean({
            description: 'Use JavaScript instead of TypeScript',
            aliases: ['js'],
            exclusive: ['language'],
        }),
        'fn-helpers': Flags.boolean({
            description: 'Add helpers to the new function',
            aliases: ['function-helpers', 'helpers'],
            allowNo: true,
        }),
        'fn-installer': Flags.string({
            description: 'Which package manager to use when installing the @sanity/functions helpers',
            aliases: ['function-installer', 'installer'],
            options: ['skip', 'npm', 'pnpm', 'yarn'],
        }),
        install: Flags.boolean({
            description: 'Shortcut for --fn-installer npm',
            char: 'i',
            exclusive: ['fn-installer'],
        }),
    };
    async run() {
        const { blueprint, flags, args: { type: resourceType }, config: { bin }, } = this;
        if (resourceType !== 'function') {
            this.error(`Unsupported Resource type: ${resourceType}`);
        }
        // log(
        //   warn(
        //     `\`${bin} blueprints add function\` is deprecated. Use \`${bin} functions add\` instead.`,
        //   ),
        // )
        const { success, error } = await functionAddCore({
            bin,
            log: Logger(this.log.bind(this), this.flags),
            blueprint,
            validateResources: flags['validate-resources'],
            flags: {
                example: flags.example,
                name: flags.name,
                type: flags['fn-type'],
                language: flags.language,
                javascript: flags.javascript,
                helpers: flags['fn-helpers'],
                installer: flags['fn-installer'],
                install: flags.install,
            },
        });
        if (!success)
            this.error(error);
    }
}
