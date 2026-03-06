import { Flags } from '@oclif/core';
import { baseFlags, RuntimeCommand, unhide } from '../../baseCommands.js';
import config from '../../config.js';
import { blueprintDoctorCore } from '../../cores/blueprints/doctor.js';
import { Logger } from '../../utils/logger.js';
export default class DoctorCommand extends RuntimeCommand {
    static summary = 'Diagnose potential issues with local Blueprint and remote Stack configuration';
    static description = `Analyzes your local Blueprint and remote Stack configuration for common issues, such as missing authentication, invalid project references, or misconfigured resources.

Run this command when encountering errors with other Blueprint commands. Use --fix to interactively resolve detected issues.`;
    // TODO: add "Supports --json for programmatic consumption of diagnostic results." to help text
    static examples = [];
    static flags = {
        path: unhide(baseFlags.path),
        fix: Flags.boolean({
            description: 'Interactively fix configuration issues',
            default: false,
        }),
        json: unhide(baseFlags.json),
        verbose: Flags.boolean({
            description: 'Verbose output; defaults to true',
            default: true,
            allowNo: true,
        }),
    };
    async run() {
        const { token } = config;
        const result = await blueprintDoctorCore({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            token,
            validateResources: this.flags['validate-resources'],
            flags: this.flags,
        });
        const { success, error } = result;
        if (!success)
            this.error(error);
        return result.data;
    }
}
