import { SanityCommand } from '@sanity/cli-core';
export declare class DatasetImportCommand extends SanityCommand<typeof DatasetImportCommand> {
    static description: string;
    static examples: {
        description: string;
        command: string;
    }[];
    static flags: {
        project: import("@oclif/core/interfaces").OptionFlag<string, import("@oclif/core/interfaces").CustomOptions>;
        dataset: import("@oclif/core/interfaces").OptionFlag<string, import("@oclif/core/interfaces").CustomOptions>;
        token: import("@oclif/core/interfaces").OptionFlag<string | undefined, import("@oclif/core/interfaces").CustomOptions>;
        replace: import("@oclif/core/interfaces").BooleanFlag<boolean>;
        missing: import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'allow-failing-assets': import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'allow-assets-in-different-dataset': import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'replace-assets': import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'skip-cross-dataset-references': import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'allow-replacement-characters': import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'allow-system-documents': import("@oclif/core/interfaces").BooleanFlag<boolean>;
        'asset-concurrency': import("@oclif/core/interfaces").OptionFlag<number | undefined, import("@oclif/core/interfaces").CustomOptions>;
    };
    static args: {
        source: import("@oclif/core/interfaces").Arg<string, Record<string, unknown>>;
    };
    private currentStep?;
    private currentProgress?;
    private stepStart?;
    private spinInterval?;
    run(): Promise<void>;
    private printWarnings;
    private static getStream;
    private onProgress;
}
//# sourceMappingURL=import.d.ts.map