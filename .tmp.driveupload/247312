import { LocalBlueprintCommand, stackFlag, unhide } from '../../baseCommands.js';
import { blueprintPlanCore } from '../../cores/blueprints/plan.js';
import { Logger } from '../../utils/logger.js';
export default class PlanCommand extends LocalBlueprintCommand {
    static summary = 'Enumerate resources to be deployed to the remote Stack - will not modify any resources';
    static description = `Use this command to preview what changes will be applied to your remote Stack before deploying. This is a safe, read-only operation—no resources are created, modified, or deleted.

Run 'blueprints plan' after making local changes to your Blueprint manifest to verify the expected diff. When ready, run 'blueprints deploy' to apply changes.`;
    static examples = ['<%= config.bin %> <%= command.id %>'];
    static flags = {
        stack: unhide(stackFlag),
    };
    async run() {
        const { success, error } = await blueprintPlanCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            token: this.sanityToken,
            blueprint: this.blueprint,
            validateResources: this.flags['validate-resources'],
            flags: this.flags,
        });
        if (!success)
            this.error(error);
    }
}
