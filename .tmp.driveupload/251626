import { CLIError } from '@oclif/core/errors';
import { isTrueish } from './isTrueish.js';
/**
 * @public
 * Symbol used to store the CLI telemetry store on globalThis.
 * Use `getCliTelemetry()` to access the store instead of accessing this directly.
 */ export const CLI_TELEMETRY_SYMBOL = Symbol.for('sanity.cli.telemetry');
/**
 * @public
 */ export function getCliTelemetry() {
    const global = globalThis;
    // This should never happen, but just in case.
    // Ignore this error in tests to avoid failing tests as tests don't run to
    if (!global[CLI_TELEMETRY_SYMBOL] && !isTrueish(process.env.TEST)) {
        throw new CLIError('CLI telemetry not initialized', {
            exit: 1
        });
    }
    return global[CLI_TELEMETRY_SYMBOL];
}
/**
 * Sets the global CLI telemetry store.
 * @internal
 */ export function setCliTelemetry(telemetry) {
    const global = globalThis;
    global[CLI_TELEMETRY_SYMBOL] = telemetry;
}
/**
 * Clears the global CLI telemetry store.
 * @internal
 */ export function clearCliTelemetry() {
    const global = globalThis;
    delete global[CLI_TELEMETRY_SYMBOL];
}

//# sourceMappingURL=getCliTelemetry.js.map