import { existsSync } from 'node:fs';
import { join } from 'node:path';
import hydrate from '@architect/hydrate';
import inventory from '@architect/inventory';
import { convertResourceToArcFormat } from './resource-to-arc.js';
export async function resolveResourceDependencies(resource, transpiled) {
    const rawArc = await convertResourceToArcFormat(resource, transpiled);
    const inv = await inventory({ rawArc });
    const cwd = inv.inv._project.cwd;
    const installOptions = {
        inventory: inv,
        hydrateShared: false,
        quiet: true,
        pnpm: false,
        yarn: false,
    };
    if (existsSync(join(cwd, 'pnpm-lock.yaml'))) {
        installOptions.pnpm = true;
    }
    else if (existsSync(join(cwd, 'yarn.lock'))) {
        installOptions.yarn = true;
    }
    try {
        await hydrate.install(installOptions);
    }
    catch (err) {
        // This is a temporary fix.
        const regex = /ENOTDIR: not a directory, unlink ['"].*[/\\]node_modules['"]/;
        const errorMessage = err instanceof Error ? err.message : String(err);
        if (!regex.test(errorMessage)) {
            throw err;
        }
    }
}
