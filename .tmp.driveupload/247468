import { update } from '../../../actions/functions/env/update.js';
import { findFunctionInStack } from '../../../utils/find-function.js';
import { styleText } from '../../../utils/style-text.js';
export async function functionEnvAddCore(options) {
    const { args, log } = options;
    const spinner = log.ora(`Updating "${args.key}" environment variable in "${args.name}"`).start();
    const { externalId } = findFunctionInStack(options.deployedStack, args.name);
    const result = await update(externalId, args.key, args.value, options.auth, options.log);
    if (!result.ok) {
        spinner.fail(`${styleText('red', 'Failed')} to update ${args.key}`);
        return {
            success: false,
            error: result.error || 'Unknown error',
        };
    }
    spinner.succeed(`Update of ${args.key} succeeded`);
    return { success: true };
}
