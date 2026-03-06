import { DeployedStackCommand } from '../../baseCommands.js';
export default class LogsCommand extends DeployedStackCommand<typeof LogsCommand> {
    static summary: string;
    static description: string;
    static examples: string[];
    static flags: {
        stack: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        watch: import("@oclif/core/interfaces").BooleanFlag<boolean>;
    };
    run(): Promise<void>;
}
