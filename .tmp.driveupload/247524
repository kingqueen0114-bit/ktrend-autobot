// * https://oclif.io/docs/base_class
import { Command, CommandHelp, Flags as OclifFlags } from '@oclif/core';
import { initBlueprintConfig, initDeployedBlueprintConfig } from './cores/index.js';
import { Logger } from './utils/logger.js';
const hidden = true;
export const baseFlags = {
    json: OclifFlags.boolean({
        // override defaults from oclif's built-in --json flag
        description: 'Format output as json.',
        hidden,
    }),
    path: OclifFlags.string({
        description: 'Path to a Blueprint file or directory containing one',
        env: 'SANITY_BLUEPRINT_PATH',
        aliases: ['blueprint-path'],
        char: 'p',
        hidden,
    }),
    trace: OclifFlags.boolean({
        description: 'Trace output',
        default: false,
        hidden,
    }),
    'validate-resources': OclifFlags.boolean({
        description: 'Validate resources',
        default: false,
        allowNo: true,
        hidden, // TODO: reveal this once support is added in main CLI
    }),
    verbose: OclifFlags.boolean({
        description: 'Verbose output',
        default: false,
        hidden,
    }),
};
export const stackFlag = OclifFlags.string({
    description: 'Stack name or ID to use instead of the locally configured Stack',
    hidden: true,
});
/**
 * @description Unhides a flag by setting its hidden property to false
 * Also makes oclif's types happy when destructuring the flag
 */
export function unhide(flag) {
    return { ...flag, hidden: false };
}
/**
 * @description Guarantees flags and args.
 * Also centralizes baseFlags and enables oclif's built-in --json for all subclasses.
 * @extends Command
 */
export class RuntimeCommand extends Command {
    flags;
    args;
    static baseFlags = baseFlags;
    static enableJsonFlag = true; // oclif's built-in --json flag
    /**
     * Generates help text for this command class
     * @param bin - The bin name to use for the help text; e.g. 'sanity', defaults to 'sanity-run'
     * @param commandId - The sub-command to use for the help text; optional but recommended for better help text
     * @returns The oclif-styled help text for the command
     * @example const helpText = InfoCommand.getHelpText('sanity', 'blueprints info')
     */
    static getHelpText(bin = 'sanity-run', commandId) {
        // biome-ignore lint/complexity/noThisInStatic: this is this command class - not confusing
        const thisClass = this;
        const rawArgs = thisClass.args || {};
        const args = Object.entries(rawArgs).reduce((acc, [name, arg]) => {
            acc[name] = { ...arg, name };
            return acc;
        }, {});
        const commandLoadable = {
            //! required properties
            id: commandId || thisClass.id || '',
            flags: thisClass.flags || {},
            args,
            aliases: thisClass.aliases || [],
            hidden: thisClass.hidden || false,
            hiddenAliases: thisClass.hiddenAliases || [],
            load: async () => thisClass,
            //* optional properties
            // bin, // seems to not be used in the CommandHelp class
            // thisClass, // doesn't change the help text
            help: thisClass.help,
            usage: thisClass.usage,
            examples: thisClass.examples,
            description: thisClass.description,
            summary: thisClass.summary,
            state: thisClass.state,
            deprecateAliases: thisClass.deprecateAliases,
            deprecationOptions: thisClass.deprecationOptions,
            strict: thisClass.strict,
            hasDynamicHelp: thisClass.hasDynamicHelp,
        };
        const commandHelp = new CommandHelp(commandLoadable, { bin }, {
            maxWidth: 120,
        });
        return commandHelp.generate();
    }
    async init() {
        const { args, flags } = await this.parse({
            flags: this.ctor.flags,
            baseFlags: super.ctor.baseFlags,
            enableJsonFlag: this.ctor.enableJsonFlag,
            args: this.ctor.args,
            strict: this.ctor.strict,
        });
        this.flags = flags;
        this.args = args;
        await super.init();
    }
}
/**
 * @description Guarantees flags, args, sanityToken, and blueprint.
 * Blueprint parser errors are logged and the command exits with an error
 * @extends RuntimeCommand
 */
export class LocalBlueprintCommand extends RuntimeCommand {
    sanityToken;
    blueprint;
    static baseFlags = baseFlags;
    async init() {
        await super.init();
        const result = await initBlueprintConfig({
            bin: this.config.bin,
            log: Logger(this.log.bind(this), this.flags),
            validateResources: this.flags['validate-resources'],
            blueprintPath: this.flags.path,
        });
        if (!result.ok) {
            this.error(result.error);
        }
        this.sanityToken = result.value.token;
        this.blueprint = result.value.blueprint;
    }
    async catch(err) {
        // add any custom logic to handle errors from the command
        // or simply return the parent class error handling
        return super.catch(err);
    }
    async finally(_) {
        // called after run and catch regardless of whether or not the command errored
        return super.finally(_);
    }
}
/**
 * @description Guarantees flags, args, sanityToken, blueprint, scopeType, scopeId, stackId, auth, and deployedStack.
 * If scope or stack is missing, the command exits with an error
 * @extends LocalBlueprintCommand
 */
export class DeployedStackCommand extends LocalBlueprintCommand {
    auth;
    deployedStack;
    scopeType;
    scopeId;
    stackId;
    static baseFlags = { ...baseFlags, stack: stackFlag };
    async init() {
        await super.init();
        const result = await initDeployedBlueprintConfig({
            bin: this.config.bin,
            blueprint: this.blueprint,
            log: Logger(this.log.bind(this), this.flags),
            token: this.sanityToken,
            validateToken: false,
            validateResources: this.flags['validate-resources'],
            stackOverride: this.flags.stack,
        });
        if (!result.ok) {
            this.error(result.error);
        }
        this.scopeType = result.value.scopeType;
        this.scopeId = result.value.scopeId;
        this.stackId = result.value.stackId;
        this.auth = result.value.auth;
        this.deployedStack = result.value.deployedStack;
    }
}
