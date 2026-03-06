import { remove } from '../../../actions/functions/env/remove.js';
import { findFunctionInStack } from '../../../utils/find-function.js';
import { styleText } from '../../../utils/style-text.js';
export async function functionEnvRemoveCore(options) {
    const { args, log } = options;
    const spinner = log.ora(`Removing "${args.key}" environment variable in "${args.name}"`).start();
    const { externalId } = findFunctionInStack(options.deployedStack, args.name);
    const result = await remove(externalId, args.key, options.auth, options.log);
    if (!result.ok) {
        spinner.fail(`${styleText('red', 'Failed')} to remove ${args.key}`);
        return { success: false, error: result.error || 'Unknown error' };
    }
    spinner.succeed(`Removal of ${args.key} succeeded`);
    return { success: true };
}
