import { Command } from '@oclif/core';
import { getCliConfig } from './config/cli/getCliConfig.js';
import { findProjectRoot } from './config/findProjectRoot.js';
import { subdebug } from './debug.js';
import { getGlobalCliClient, getProjectCliClient } from './services/apiClient.js';
import { getCliTelemetry } from './util/getCliTelemetry.js';
import { isInteractive } from './util/isInteractive.js';
const debug = subdebug('sanityCommand');
export class SanityCommand extends Command {
    args;
    flags;
    /**
   * Get the global API client.
   *
   * @param args - The global API client options.
   * @returns The global API client.
   *
   * @deprecated use `getGlobalCliClient` function directly instead.
   */ getGlobalApiClient = (args)=>getGlobalCliClient(args);
    /**
   * Get the project API client.
   *
   * @param args - The project API client options.
   * @returns The project API client.
   *
   * @deprecated use `getProjectCliClient` function directly instead.
   */ getProjectApiClient = (args)=>getProjectCliClient(args);
    /**
   * Helper for outputting to the console.
   *
   * @example
   * ```ts
   * this.output.log('Hello')
   * this.output.warn('Warning')
   * this.output.error('Error')
   * ```
   */ output = {
        error: this.error.bind(this),
        log: this.log.bind(this),
        warn: this.warn.bind(this)
    };
    /**
   * The telemetry store.
   *
   * @returns The telemetry store.
   */ telemetry;
    /**
   * Get the CLI config.
   *
   * @returns The CLI config.
   */ async getCliConfig() {
        const root = await this.getProjectRoot();
        debug(`Using project root`, root);
        return getCliConfig(root.directory);
    }
    /**
   * Get the project ID from the CLI config.
   *
   * @returns The project ID or `undefined` if it's not set.
   */ async getProjectId() {
        const config = await this.getCliConfig();
        return config.api?.projectId;
    }
    /**
   * Get the project's root directory by resolving the config
   *
   * @returns The project root result.
   */ getProjectRoot() {
        return findProjectRoot(process.cwd());
    }
    async init() {
        const { args, flags } = await this.parse({
            args: this.ctor.args,
            baseFlags: super.ctor.baseFlags,
            enableJsonFlag: this.ctor.enableJsonFlag,
            flags: this.ctor.flags,
            strict: this.ctor.strict
        });
        this.args = args;
        this.flags = flags;
        this.telemetry = getCliTelemetry();
        await super.init();
    }
    /**
   * Check if the command is running in unattended mode.
   *
   * This means the command should not ask for user input, instead using defaults where
   * possible, and if that does not make sense (eg there's missing information), then we
   * should error out (remember to exit with a non-zero code).
   *
   * Most commands should take an explicit `--yes` flag to enable unattended mode, but
   * some commands may also be run in unattended mode if `process.stdin` is not a TTY
   * (eg when running in a CI environment).
   */ isUnattended() {
        return this.flags.yes || !this.resolveIsInteractive();
    }
    /**
   * Resolver for checking if the terminal is interactive. Override in tests to provide mock values.
   *
   * @returns Whether the terminal is interactive.
   */ resolveIsInteractive() {
        return isInteractive();
    }
}

//# sourceMappingURL=SanityCommand.js.map