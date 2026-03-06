import { DeployedStackCommand } from '../../baseCommands.js';
export default class DeployCommand extends DeployedStackCommand<typeof DeployCommand> {
    static summary: string;
    static description: string;
    static examples: string[];
    static flags: {
        stack: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        'no-wait': import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'new-stack-name': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
    };
    run(): Promise<void>;
}
