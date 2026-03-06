import { readFile } from 'node:fs/promises';
import { z } from 'zod';
/**
 * Comprehensive package.json schema including all common properties.
 * Feel free to add properties to this,
 * 🟠ℹ️   BUT ENSURE OPTIONAL STUFF IS ACTUALLY OPTIONAL  ℹ️🟠
 * 🟠ℹ️ SINCE THIS IS USED IN A NUMBER OF LOCATIONS WHERE ℹ️🟠
 * 🟠ℹ️ WE CANNOT ENFORCE/GUARANTEE ANY PARTICULAR PROPS  ℹ️🟠
 */ const packageJsonSchema = z.looseObject({
    // Required fields
    name: z.string(),
    version: z.string(),
    // Dependencies (optional)
    dependencies: z.record(z.string(), z.string()).optional(),
    devDependencies: z.record(z.string(), z.string()).optional(),
    peerDependencies: z.record(z.string(), z.string()).optional(),
    // Module structure (optional)
    exports: z.record(z.string(), z.any()).optional(),
    main: z.string().optional(),
    types: z.string().optional(),
    // Metadata (optional)
    author: z.string().optional(),
    description: z.string().optional(),
    engines: z.record(z.string(), z.string()).optional(),
    license: z.string().optional(),
    private: z.boolean().optional(),
    repository: z.object({
        type: z.string(),
        url: z.string()
    }).optional(),
    scripts: z.record(z.string(), z.string()).optional()
});
/**
 * Read the `package.json` file at the given path
 *
 * @param filePath - Path to package.json to read
 * @param options - Options object for controlling read behavior
 * @returns The parsed package.json
 * @public
 */ export async function readPackageJson(filePath, options = {}) {
    const { defaults = {}, skipSchemaValidation = false } = options;
    // Read and parse the file
    let pkg;
    try {
        pkg = JSON.parse(await readFile(filePath, 'utf8'));
    } catch (err) {
        throw new Error(`Failed to read "${filePath}"`, {
            cause: err
        });
    }
    // Merge with defaults (parsed values take precedence)
    const merged = {
        ...defaults,
        ...pkg
    };
    // Validate with schema unless skipped
    let validated;
    if (skipSchemaValidation) {
        validated = merged;
    } else {
        const { data, error, success } = packageJsonSchema.safeParse(merged);
        if (!success) {
            throw new Error(`Invalid package.json at "${filePath}": ${error.issues.map((err)=>err.message).join('\n')}`);
        }
        validated = data;
    }
    return validated;
}

//# sourceMappingURL=readPackageJson.js.map