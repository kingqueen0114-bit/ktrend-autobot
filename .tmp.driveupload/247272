import { Flags } from '@oclif/core';
import { LocalBlueprintCommand } from '../../baseCommands.js';
import { functionAddCore } from '../../cores/functions/index.js';
import { Logger } from '../../utils/logger.js';
export default class AddCommand extends LocalBlueprintCommand {
    static summary = 'Add a Function to your Blueprint';
    static description = `Scaffolds a new Function in the functions/ folder and templates a resource for your Blueprint manifest.

Functions are serverless handlers triggered by document events (create, update, delete, publish) or media library events.

After adding, use 'functions dev' to test locally, then 'blueprints deploy' to publish.`;
    static examples = [
        '<%= config.bin %> <%= command.id %>',
        '<%= config.bin %> <%= command.id %> --helpers',
        '<%= config.bin %> <%= command.id %> --name my-function',
        '<%= config.bin %> <%= command.id %> --name my-function --type document-create',
        '<%= config.bin %> <%= command.id %> --name my-function --type document-create --type document-update --lang js',
    ];
    static flags = {
        example: Flags.string({
            description: 'Example to use for the Function',
            aliases: ['recipe'],
            exclusive: ['name', 'fn-type', 'language', 'javascript', 'fn-helpers', 'fn-installer'],
        }),
        name: Flags.string({
            description: 'Name of the Function to add',
            char: 'n',
        }),
        type: Flags.string({
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
            multiple: true,
            multipleNonGreedy: true,
            dependsOn: ['name'],
        }),
        language: Flags.string({
            description: 'Language of the new Function',
            aliases: ['lang'],
            options: ['ts', 'js'],
            default: 'ts',
        }),
        javascript: Flags.boolean({
            description: 'Use JavaScript instead of TypeScript',
            aliases: ['js'],
            exclusive: ['language'],
        }),
        helpers: Flags.boolean({
            description: 'Add helpers to the new Function',
            allowNo: true,
        }),
        installer: Flags.string({
            description: 'How to install the @sanity/functions helpers',
            options: ['skip', 'npm', 'pnpm', 'yarn'],
        }),
        install: Flags.boolean({
            description: 'Shortcut for --fn-installer npm',
            char: 'i',
            exclusive: ['fn-installer'],
        }),
    };
    async run() {
        const { success, error } = await functionAddCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            blueprint: this.blueprint,
            validateResources: this.flags['validate-resources'],
            flags: this.flags,
        });
        if (!success)
            this.error(error);
    }
}
