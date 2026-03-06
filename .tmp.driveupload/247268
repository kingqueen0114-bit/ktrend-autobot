import { LocalBlueprintCommand } from '../../baseCommands.js';
export default class DevCommand extends LocalBlueprintCommand<typeof DevCommand> {
    static summary: string;
    static description: string;
    static examples: string[];
    static flags: {
        host: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        port: import("@oclif/core/interfaces").OptionFlag<number | undefined, import("@oclif/core/interfaces").CustomOptions>;
        timeout: import("@oclif/core/interfaces").OptionFlag<number | undefined, import("@oclif/core/interfaces").CustomOptions>;
    };
    run(): Promise<void>;
}
