import { Args } from '@oclif/core';
import { DeployedStackCommand } from '../../../baseCommands.js';
import { functionEnvListCore } from '../../../cores/functions/env/list.js';
import { Logger } from '../../../utils/logger.js';
export default class EnvListCommand extends DeployedStackCommand {
    static summary = 'List environment variables for a deployed function';
    static description = `Displays all environment variables (keys only) configured in a deployed Sanity Function.

Use 'functions env add' to set variables or 'functions env remove' to delete them.`;
    static args = {
        name: Args.string({ description: 'The name of the Sanity Function', required: true }),
    };
    static examples = ['<%= config.bin %> <%= command.id %> MyFunction'];
    async run() {
        const { success, error } = await functionEnvListCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            args: this.args,
            auth: this.auth,
            blueprint: this.blueprint,
            deployedStack: this.deployedStack,
            scopeType: this.scopeType,
            scopeId: this.scopeId,
            token: this.sanityToken,
            stackId: this.stackId,
            validateResources: this.flags['validate-resources'],
        });
        if (!success)
            this.error(error);
    }
}
