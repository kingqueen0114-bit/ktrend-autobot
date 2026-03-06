import type { BlueprintResource } from '@sanity/blueprints';
import { type Blueprint } from '@sanity/blueprints-parser';
import type { Logger } from '../../utils/logger.js';
import { type BlueprintParserError, type ScopeType } from '../../utils/types.js';
import { type LocatedBlueprintsConfig } from './config.js';
declare const SUPPORTED_FILE_EXTENSIONS: readonly [".json", ".js", ".mjs", ".ts"];
type BlueprintFileExtension = (typeof SUPPORTED_FILE_EXTENSIONS)[number];
export declare const JSON_BLUEPRINT_CONTENT: {
    blueprintVersion: string;
    resources: never[];
};
export declare const TS_BLUEPRINT_CONTENT: string;
/** Function type with attached attributes */
export type BlueprintModule = ((args?: unknown) => Record<string, unknown>) & {
    organizationId?: string;
    projectId?: string;
    stackId?: string;
};
type FileInfo = {
    blueprintFilePath: string;
    fileName: string;
    extension: BlueprintFileExtension;
};
/**
 * Finds the blueprint file in the given path or current working directory
 * @param blueprintPath - The path of the blueprint file or directory
 * @returns The path, file name, and extension of the blueprint file
 */
export declare function findBlueprintFile(blueprintPath?: string): FileInfo | null;
/**
 * Source of the config value.
 * - config: from the config file - .sanity.blueprint.config.json most common
 * - env: from the environment - usually CLI var like `SANITY_ORGANIZATION_ID`
 * - module: from the blueprint module - undocumented escape hatch
 * - inferred: legacy `ST-<projectId>` stacks from launch
 */
export type ConfigSource = 'config' | 'env' | 'module' | 'inferred';
/** Result of the blueprint read operation */
export interface ReadBlueprintResult {
    fileInfo: FileInfo;
    blueprintConfig: LocatedBlueprintsConfig | null;
    rawBlueprint: Record<string, unknown>;
    parsedBlueprint: Blueprint;
    errors: BlueprintParserError[];
    /** @deprecated - use blueprintConfig.configPath instead */
    configPath?: string;
    scopeType?: ScopeType;
    scopeId?: string;
    organizationId?: string;
    projectId?: string;
    stackId?: string;
    sources?: {
        organizationId?: ConfigSource;
        projectId?: ConfigSource;
        stackId?: ConfigSource;
    };
}
/**
 * Reads the blueprint file from disk and parses it.
 * Overrides config file values with shell environment variables.
 * Can infer stackId from projectId if no stackId is provided and legacy ST-<projectId> stacks from launch are used.
 *
 * @param logger The logger instance
 * @param validate Validation options
 * @param blueprintPath - The path of the blueprint file or directory- will search up the directory tree!
 * @returns Known information about the Blueprint, config, and Stack
 */
export declare function readLocalBlueprint(logger: ReturnType<typeof Logger>, validate: {
    resources: boolean;
}, blueprintPath?: string): Promise<ReadBlueprintResult>;
export declare function writeBlueprintToDisk({ blueprintFilePath, jsonContent, }: {
    blueprintFilePath: string;
    jsonContent?: Blueprint;
}): string;
export declare function addResourceToBlueprint<T extends BlueprintResource>({ blueprintFilePath, resource, }: {
    blueprintFilePath?: string;
    resource: T;
}): T | undefined;
export {};
