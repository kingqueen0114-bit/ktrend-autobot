import { SanityCommand } from '@sanity/cli-core';
export type RunMigrationFlags = RunMigrationCommand['flags'];
export declare class RunMigrationCommand extends SanityCommand<typeof RunMigrationCommand> {
    static args: {
        id: import("@oclif/core/interfaces").Arg<string | undefined, Record<string, unknown>>;
    };
    static description: string;
    static examples: {
        command: string;
        description: string;
    }[];
    static flags: {
        'api-version': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        concurrency: import("@oclif/core/interfaces").OptionFlag<number, import("@oclif/core/interfaces").CustomOptions>;
        confirm: import("@oclif/core/interfaces").BooleanFlag<boolean>;
        dataset: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        'dry-run': import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'from-export': import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        progress: import("@oclif/core/interfaces").BooleanFlag<boolean>;
        project: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
    };
    run(): Promise<void>;
    private createProgress;
    private dryRunHandler;
    private promptConfirmMigrate;
}
//# sourceMappingURL=run.d.ts.map