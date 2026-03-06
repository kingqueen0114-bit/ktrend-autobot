/**
 * Patterns to identify native modules based on common file types and build configurations.
 */
const KNOWN_MODULE_PATTERNS = [/binding\.gyp$/, /\.node$/];
/**
 * Scan zip entries of dependencies for native modules.
 * Native modules built on one platform may not work on another (e.g., macOS vs Linux)
 */
export const detectNativeModules = (zip) => {
    try {
        const zippedEntries = zip.getEntries();
        const moduleNames = zippedEntries
            // Filter entries that match known native module patterns
            .filter((entry) => KNOWN_MODULE_PATTERNS.some((pattern) => pattern.test(entry.entryName)))
            // Extract package names from the entry paths
            .map((entry) => entry.entryName.match(/node_modules[\\/](.+?)[\\/]/)?.[1])
            // Filter out undefined results (in case the regex didn't match)
            .filter((name) => name !== undefined);
        // return a unique list of module names
        return [...new Set(moduleNames)];
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        throw new Error(`Failed to scan zip for native modules: ${message}`);
    }
};
