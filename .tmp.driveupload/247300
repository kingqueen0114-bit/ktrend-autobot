import { LocalBlueprintCommand } from '../../baseCommands.js';
export default class DestroyCommand extends LocalBlueprintCommand<typeof DestroyCommand> {
    static summary: string;
    static description: string;
    static examples: string[];
    static flags: {
        force: import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'project-id': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        'organization-id': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        stack: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        'no-wait': import("@oclif/core/interfaces").BooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
