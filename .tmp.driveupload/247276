import { LocalBlueprintCommand } from '../../baseCommands.js';
export default class AddCommand extends LocalBlueprintCommand<typeof AddCommand> {
    static summary: string;
    static description: string;
    static examples: string[];
    static flags: {
        example: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        name: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        type: import("@oclif/core/interfaces").OptionFlag<string[] | undefined, import("@oclif/core/interfaces").CustomOptions>;
        language: import("@oclif/core/interfaces").OptionFlag<string, import("@oclif/core/interfaces").CustomOptions>;
        javascript: import("@oclif/core/interfaces").BooleanFlag<boolean>;
        helpers: import("@oclif/core/interfaces").BooleanFlag<boolean>;
        installer: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        install: import("@oclif/core/interfaces").BooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
