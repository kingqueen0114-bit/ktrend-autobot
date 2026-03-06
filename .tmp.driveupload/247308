import { DeployedStackCommand } from '../../baseCommands.js';
export default class InfoCommand extends DeployedStackCommand<typeof InfoCommand> {
    static summary: string;
    static description: string;
    static examples: string[];
    static flags: {
        stack: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
    };
    run(): Promise<void>;
}
