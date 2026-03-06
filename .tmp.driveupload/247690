import type { Interfaces } from '@oclif/core';
import { Command } from '@oclif/core';
import type { ReadBlueprintResult } from './actions/blueprints/blueprint.js';
import type { AuthParams, ScopeType, Stack } from './utils/types.js';
export type Flags<T extends typeof Command> = Interfaces.InferredFlags<(typeof RuntimeCommand)['baseFlags'] & T['flags']>;
export type Args<T extends typeof Command> = Interfaces.InferredArgs<T['args']>;
export declare const baseFlags: {
    json: Interfaces.BooleanFlag<boolean>;
    path: Interfaces.OptionFlag<string | undefined, Interfaces.CustomOptions>;
    trace: Interfaces.BooleanFlag<boolean>;
    'validate-resources': Interfaces.BooleanFlag<boolean>;
    verbose: Interfaces.BooleanFlag<boolean>;
};
export declare const stackFlag: Interfaces.OptionFlag<string | undefined, Interfaces.CustomOptions>;
/**
 * @description Unhides a flag by setting its hidden property to false
 * Also makes oclif's types happy when destructuring the flag
 */
export declare function unhide<T>(flag: T): T;
/**
 * @description Guarantees flags and args.
 * Also centralizes baseFlags and enables oclif's built-in --json for all subclasses.
 * @extends Command
 */
export declare abstract class RuntimeCommand<T extends typeof Command> extends Command {
    protected flags: Flags<T>;
    protected args: Args<T>;
    static baseFlags: {
        json: Interfaces.BooleanFlag<boolean>;
        path: Interfaces.OptionFlag<string | undefined, Interfaces.CustomOptions>;
        trace: Interfaces.BooleanFlag<boolean>;
        'validate-resources': Interfaces.BooleanFlag<boolean>;
        verbose: Interfaces.BooleanFlag<boolean>;
    };
    static enableJsonFlag: boolean;
    /**
     * Generates help text for this command class
     * @param bin - The bin name to use for the help text; e.g. 'sanity', defaults to 'sanity-run'
     * @param commandId - The sub-command to use for the help text; optional but recommended for better help text
     * @returns The oclif-styled help text for the command
     * @example const helpText = InfoCommand.getHelpText('sanity', 'blueprints info')
     */
    static getHelpText(bin?: string, commandId?: string): string;
    init(): Promise<void>;
}
/**
 * @description Guarantees flags, args, sanityToken, and blueprint.
 * Blueprint parser errors are logged and the command exits with an error
 * @extends RuntimeCommand
 */
export declare abstract class LocalBlueprintCommand<T extends typeof Command> extends RuntimeCommand<T> {
    protected sanityToken: string;
    protected blueprint: ReadBlueprintResult;
    static baseFlags: {
        json: Interfaces.BooleanFlag<boolean>;
        path: Interfaces.OptionFlag<string | undefined, Interfaces.CustomOptions>;
        trace: Interfaces.BooleanFlag<boolean>;
        'validate-resources': Interfaces.BooleanFlag<boolean>;
        verbose: Interfaces.BooleanFlag<boolean>;
    };
    init(): Promise<void>;
    protected catch(err: Error & {
        exitCode?: number;
    }): Promise<unknown>;
    protected finally(_: Error | undefined): Promise<unknown>;
}
/**
 * @description Guarantees flags, args, sanityToken, blueprint, scopeType, scopeId, stackId, auth, and deployedStack.
 * If scope or stack is missing, the command exits with an error
 * @extends LocalBlueprintCommand
 */
export declare abstract class DeployedStackCommand<T extends typeof Command> extends LocalBlueprintCommand<T> {
    protected auth: AuthParams;
    protected deployedStack: Stack;
    protected scopeType: ScopeType;
    protected scopeId: string;
    protected stackId: string;
    static baseFlags: {
        stack: Interfaces.OptionFlag<string | undefined, Interfaces.CustomOptions>;
        json: Interfaces.BooleanFlag<boolean>;
        path: Interfaces.OptionFlag<string | undefined, Interfaces.CustomOptions>;
        trace: Interfaces.BooleanFlag<boolean>;
        'validate-resources': Interfaces.BooleanFlag<boolean>;
        verbose: Interfaces.BooleanFlag<boolean>;
    };
    init(): Promise<void>;
}
