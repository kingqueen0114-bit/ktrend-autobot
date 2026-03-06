import { LocalBlueprintCommand } from '../../baseCommands.js';
export default class StacksCommand extends LocalBlueprintCommand<typeof StacksCommand> {
    static summary: string;
    static description: string;
    static examples: string[];
    static flags: {
        'project-id': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        'organization-id': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
    };
    run(): Promise<void>;
}
