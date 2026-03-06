import { LocalBlueprintCommand } from '../../baseCommands.js';
export default class ConfigCommand extends LocalBlueprintCommand<typeof ConfigCommand> {
    static summary: string;
    static description: string;
    static examples: string[];
    static flags: {
        edit: import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'project-id': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        'organization-id': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        stack: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
    };
    run(): Promise<void>;
}
