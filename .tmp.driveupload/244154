import { type BlueprintBaseFunctionConfig, type BlueprintBaseFunctionResource, type BlueprintDocumentFunctionConfig, type BlueprintDocumentFunctionResource, type BlueprintDocumentFunctionResourceEvent, type BlueprintMediaLibraryAssetFunctionConfig, type BlueprintMediaLibraryAssetFunctionResource, type BlueprintScheduleFunctionConfig, type BlueprintScheduleFunctionResource } from '../index.js';
/**
 * Defines a function that is triggered by document events in Sanity datasets.
 *
 * ```ts
 * defineDocumentFunction({
 *   name: 'my-document-function',
 *   event: {
 *     on: ['create', 'update'],
 *     filter: "_type == 'post'",
 *     projection: "{_id, title, slug}",
 *   },
 * })
 * ```
 * @param functionConfig The configuration for the document function
 * @public
 * @category Definers
 * @expandType BlueprintDocumentFunctionConfig
 * @returns The validated document function resource
 */
export declare function defineDocumentFunction(functionConfig: BlueprintDocumentFunctionConfig): BlueprintDocumentFunctionResource;
/**
 * @deprecated Define event properties under the 'event' key instead of specifying them at the top level
 * @hidden
 */
export declare function defineDocumentFunction(functionConfig: BlueprintDocumentFunctionConfig & Partial<BlueprintDocumentFunctionResourceEvent>): BlueprintDocumentFunctionResource;
/**
 * Defines a function that is triggered by media library events.
 *
 * ```ts
 * defineMediaLibraryAssetFunction({
 *   name: 'my-media-library-function',
 *   event: {
 *     on: ['create'],
 *     resource: {
 *       type: 'media-library',
 *       id: 'my-media-library-id',
 *     },
 *   },
 * })
 * ```
 * @param functionConfig The configuration for the media library asset function
 * @public
 * @category Definers
 * @expandType BlueprintMediaLibraryAssetFunctionConfig
 * @returns The validated media library asset function resource
 */
export declare function defineMediaLibraryAssetFunction(functionConfig: BlueprintMediaLibraryAssetFunctionConfig): BlueprintMediaLibraryAssetFunctionResource;
/**
 * Defines a function that is triggered on a schedule.
 * Supports cron expressions or natural language schedules.
 *
 * @remarks
 * Using a cron expression:
 * ```ts
 * defineScheduleFunction({
 *   name: 'daily-cleanup',
 *   event: {expression: '0 9 * * *'},
 * })
 * ```
 *
 * Using explicit cron fields:
 * ```ts
 * defineScheduleFunction({
 *   name: 'daily-cleanup',
 *   event: {minute: '0', hour: '9', dayOfMonth: '*', month: '*', dayOfWeek: '*'},
 * })
 * ```
 *
 * The `event.expression` field accepts standard cron expressions or natural language:
 * `'every 15 minutes'`, `'weekdays at 8am'`, `'fridays in the evening'`,
 * `'mon, wed, fri at 9am'`, `'first of the month at noon'`
 *
 * ```ts
 * defineScheduleFunction({
 *   name: 'daily-cleanup',
 *   event: {expression: 'every day at 9am'},
 * })
 * ```
 * @public
 * @alpha Deploying Schedule Functions via Blueprints is experimental. This feature is not available publicly yet.
 * @hidden
 * @category Definers
 * @expandType BlueprintScheduleFunctionConfig
 * @param functionConfig The configuration for the schedule function
 * @returns The validated schedule function resource
 */
export declare function defineScheduleFunction(functionConfig: BlueprintScheduleFunctionConfig): BlueprintScheduleFunctionResource;
/**
 * Defines a base function resource with common properties.
 *
 * @param functionConfig The configuration for the function
 * @param options Optional configuration including validation options
 * @category Definers
 * @internal
 * @expandType BlueprintBaseFunctionConfig
 * @returns The validated function resource
 */
export declare function defineFunction(functionConfig: BlueprintBaseFunctionConfig, options?: {
    skipValidation?: boolean;
}): BlueprintBaseFunctionResource;
