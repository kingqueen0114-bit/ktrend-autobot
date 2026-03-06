import { dirname } from 'node:path';
import { z } from 'zod';
import { studioWorkerTask } from '../../loaders/studio/studioWorkerTask.js';
const schemaSchema = z.object({
    name: z.string().optional(),
    types: z.array(z.object({}).passthrough())
});
const sourceSchema = z.object({
    dataset: z.string(),
    projectId: z.string(),
    schema: z.object({
        _original: schemaSchema
    })
});
const singleStudioWorkspaceSchema = z.object({
    ...sourceSchema.shape,
    basePath: z.string().optional(),
    name: z.string().optional(),
    plugins: z.array(z.unknown()).optional(),
    schema: schemaSchema.optional(),
    title: z.string().optional(),
    unstable_sources: z.array(sourceSchema)
}).passthrough();
const studioWorkspaceSchema = z.object({
    ...sourceSchema.shape,
    basePath: z.string(),
    name: z.string(),
    plugins: z.array(z.unknown()).optional(),
    title: z.string(),
    unstable_sources: z.array(sourceSchema)
});
const rawConfigSchema = z.union([
    z.array(studioWorkspaceSchema),
    singleStudioWorkspaceSchema
]);
const resolvedConfigSchema = z.array(studioWorkspaceSchema);
export async function readStudioConfig(configPath, options) {
    const result = await studioWorkerTask(new URL('readStudioConfig.worker.js', import.meta.url), {
        name: 'studioConfig',
        studioRootPath: dirname(configPath),
        workerData: {
            configPath,
            resolvePlugins: options.resolvePlugins
        }
    });
    return options.resolvePlugins ? resolvedConfigSchema.parse(result) : rawConfigSchema.parse(result);
}

//# sourceMappingURL=readStudioConfig.js.map