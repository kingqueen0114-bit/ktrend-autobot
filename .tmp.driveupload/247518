import { type ReadBlueprintResult } from '../actions/blueprints/blueprint.js';
import type { Logger } from '../utils/logger.js';
import type { AuthParams, Result, ScopeType, Stack } from '../utils/types.js';
export * as blueprintsCores from './blueprints/index.js';
export * as functionsCores from './functions/index.js';
export interface CoreConfig {
    /** The CLI binary name. */
    bin: string;
    /** The log output function. */
    log: ReturnType<typeof Logger>;
    /** Enable resource validation during parsing */
    validateResources?: boolean;
    /** Path to a specific Blueprint file or directory */
    blueprintPath?: string;
}
export interface BlueprintConfig extends CoreConfig {
    token: string;
    blueprint: ReadBlueprintResult;
}
export interface DeployedBlueprintConfig extends BlueprintConfig {
    stackId: string;
    scopeType: ScopeType;
    scopeId: string;
    auth: AuthParams;
    deployedStack: Stack;
}
export type CoreResult = {
    /** Arbitrary data for isolated testing */
    data?: Record<string, unknown>;
} & ({
    /** Something went wrong. */
    success: false;
    /** The error message, if the operation failed. */
    error: string;
    streaming?: never;
} | {
    /** Everything went well. */
    success: true;
    /** The streaming function, if the operation is streaming. */
    streaming?: Promise<void>;
    error?: never;
});
type InitBlueprintConfigParams = CoreConfig & ({
    validateToken: true;
    token: string;
} | {
    validateToken?: false;
    token?: string;
});
export declare function initBlueprintConfig({ bin, log, token, validateResources, validateToken, blueprintPath, }: InitBlueprintConfigParams): Promise<Result<BlueprintConfig>>;
export declare function initDeployedBlueprintConfig(config: Partial<BlueprintConfig> & Pick<BlueprintConfig, 'bin' | 'log' | 'token' | 'validateResources'> & {
    validateToken?: boolean;
    stackOverride?: string;
}): Promise<Result<DeployedBlueprintConfig>>;
