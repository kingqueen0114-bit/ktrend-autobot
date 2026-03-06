import { list } from '../../../actions/functions/env/list.js';
import { findFunctionInStack } from '../../../utils/find-function.js';
export async function functionEnvListCore(options) {
    const { args, log } = options;
    const spinner = log.ora(`Listing environment variables for "${args.name}"`).start();
    const { externalId } = findFunctionInStack(options.deployedStack, args.name);
    const result = await list(externalId, options.auth, options.log);
    if (!result.ok) {
        spinner.stop();
        return { success: false, error: result.error || 'Unknown error' };
    }
    spinner.succeed(`Environment variables for "${args.name}"`);
    for (const key of result.envvars) {
        options.log(key);
    }
    return { success: true };
}
