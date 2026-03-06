import { Migration } from '../../types.js';
interface ResolvedMigrationScript {
    /**
     * Absolute path to the migration script
     */
    absolutePath: string;
    /**
     * Relative path from the working directory to the migration script
     */
    relativePath: string;
    /**
     * The migration module, if it could be resolved - otherwise `undefined`
     */
    mod?: {
        default: Migration;
        down?: unknown;
        up?: unknown;
    };
}
/**
 * Resolves the potential paths to a migration script.
 * Considers the following paths (where `<ext>` is 'mjs', 'js', 'ts' or 'cjs'):
 *
 * - `<migrationsDir>/<migrationName>.<ext>`
 * - `<migrationsDir>/<migrationName>/index.<ext>`
 *
 * Note that all possible paths are returned, even if the files do not exist.
 * Check the `mod` property to see if a module could actually be loaded.
 *
 * @param workDir - Working directory of the studio
 * @param migrationName - The name of the migration directory to resolve
 * @returns An array of potential migration scripts
 * @internal
 */
export declare function resolveMigrationScript(workDir: string, migrationName: string): Promise<ResolvedMigrationScript[]>;
/**
 * Checks whether or not the passed resolved migration script is actually loadable (eg has a default export)
 *
 * @param script - The resolved migration script to check
 * @returns `true` if the script is loadable, `false` otherwise
 * @internal
 */
export declare function isLoadableMigrationScript(script: ResolvedMigrationScript): script is Required<ResolvedMigrationScript>;
export {};
//# sourceMappingURL=resolveMigrationScript.d.ts.map