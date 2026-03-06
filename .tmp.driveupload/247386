import type { Logger } from '../../utils/logger.js';
import type { FunctionResourceBase } from '../../utils/types.js';
interface FunctionResourceOptions {
    name: string;
    type: string[];
    lang: string;
    blueprintFilePath?: string;
    addHelpers?: boolean;
    installCommand?: string | null;
}
/**
 * Creates a new function resource file and adds it to the blueprint
 */
export declare function createFunctionResource(options: FunctionResourceOptions, logger: ReturnType<typeof Logger>): Promise<{
    filePath: string;
    resourceAdded: boolean;
    resource: FunctionResourceBase;
}>;
export {};
