import type { BlueprintError } from '../types/errors';
/**
 * Executes the given validator function and throws a formatted error if any are returned.
 * @param validator A function that returns a list of validation errors.
 * @internal
 */
export declare function runValidation(validator: () => BlueprintError[]): void;
/**
 * Checks whether a value is a blueprint reference expression.
 *
 * Recognized prefixes: `$.resources.*`, `$.values.*`, `$.parameters.*`, `$.params.*`.
 * @param value The value to check
 * @returns `true` if the value matches a known reference prefix
 * @internal
 */
export declare function isReference(value: unknown): boolean;
