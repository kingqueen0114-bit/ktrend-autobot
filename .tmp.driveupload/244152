import { validateDocumentFunction, validateFunction, validateMediaLibraryAssetFunction, validateScheduleFunction, } from '../index.js';
import { parseScheduleExpression } from '../utils/schedule-parser.js';
import { runValidation } from '../utils/validation.js';
const BASE_EVENT_KEYS = new Set(['on', 'filter', 'projection', 'includeDrafts']);
const DOCUMENT_EVENT_KEYS = new Set(['includeAllVersions', 'resource', ...BASE_EVENT_KEYS.values()]);
const MEDIA_LIBRARY_EVENT_KEYS = new Set(['resource', ...BASE_EVENT_KEYS.values()]);
const SCHEDULE_EVENT_KEYS = new Set(['minute', 'hour', 'dayOfWeek', 'month', 'dayOfMonth', 'expression']);
export function defineDocumentFunction(functionConfig) {
    let { name, src, event, timeout, memory, env, robotToken, project, runtime, ...maybeEvent } = functionConfig;
    // event validation and normalization
    if (event) {
        // `event` was specified, but event keys (aggregated in `maybeEvent`) were also specified at the top level. ambiguous and deprecated usage.
        const duplicateKeys = Array.from(DOCUMENT_EVENT_KEYS).filter((key) => key in maybeEvent);
        if (duplicateKeys.length > 0) {
            throw new Error(`\`event\` properties should be specified under the \`event\` key - specifying them at the top level is deprecated. The following keys were specified at the top level: ${duplicateKeys.map((k) => `\`${k}\``).join(', ')}`);
        }
        event = buildDocumentFunctionEvent(event);
    }
    else {
        event = buildDocumentFunctionEvent(maybeEvent);
        // deprecated usage of putting event properties at the top level, warn about this.
        console.warn('⚠️ Deprecated usage of `defineDocumentFunction`: prefer to put `event` properties under the `event` key rather than at the top level.');
    }
    const functionResource = {
        ...defineFunction(functionConfig, { skipValidation: true }),
        type: 'sanity.function.document',
        event,
    };
    runValidation(() => validateDocumentFunction(functionResource));
    return functionResource;
}
/*
 * FUTURE example (move below @example when ready)
 * @example With robot token reference
 * ```ts
 * defineRobotToken({
 *   name: 'media-robot',
 *   memberships: [{
 *     resourceType: 'project',
 *     resourceId: projectId,
 *     roleNames: ['editor'],
 *   }],
 * })
 *
 * defineMediaLibraryAssetFunction({
 *   name: 'process-uploads',
 *   src: 'functions/process-uploads-v2',
 *   robotToken: '$.resources.media-robot',
 *   event: {
 *     on: ['create', 'update'],
 *     resource: {
 *       type: 'media-library',
 *       id: 'my-media-library-id',
 *     },
 *     filter: "type == 'image'",
 *     projection: "{_id}",
 *   },
 *   env: {
 *     CDN_BUCKET: 'my-cdn-bucket',
 *   },
 * })
 * ```
 */
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
export function defineMediaLibraryAssetFunction(functionConfig) {
    const { event } = functionConfig;
    const functionResource = {
        ...defineFunction(functionConfig, { skipValidation: true }),
        type: 'sanity.function.media-library.asset',
        event: buildMediaLibraryFunctionEvent(event),
    };
    runValidation(() => validateMediaLibraryAssetFunction(functionResource));
    return functionResource;
}
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
export function defineScheduleFunction(functionConfig) {
    const { event, timezone } = functionConfig;
    const functionResource = {
        ...defineFunction(functionConfig, { skipValidation: true }),
        type: 'sanity.function.cron',
        event: buildScheduleFunctionEvent(event),
    };
    if (timezone)
        functionResource.timezone = timezone;
    runValidation(() => validateScheduleFunction(functionResource));
    // Parse expression after validation (validation ensures it's valid)
    if ('expression' in functionResource.event && functionResource.event.expression) {
        functionResource.event.expression = parseScheduleExpression(functionResource.event.expression);
    }
    return functionResource;
}
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
export function defineFunction(functionConfig, options) {
    const { name, displayName, src, timeout, memory, env, robotToken, project, runtime, lifecycle } = functionConfig;
    const functionResource = {
        type: 'sanity.function.document',
        name,
        src: src ?? `functions/${name}`,
        displayName,
        timeout,
        memory,
        env,
        robotToken,
        project,
        runtime,
    };
    if (lifecycle)
        functionResource.lifecycle = lifecycle;
    if (options?.skipValidation !== true)
        runValidation(() => validateFunction(functionResource));
    return functionResource;
}
/**
 * Builds a document function event configuration from partial event properties.
 * Filters out non-event properties and applies defaults.
 * @param event Partial document function event configuration
 * @returns Complete document function event configuration
 */
function buildDocumentFunctionEvent(event) {
    const cleanEvent = Object.fromEntries(Object.entries(event).filter(([key]) => DOCUMENT_EVENT_KEYS.has(key)));
    return {
        on: cleanEvent.on || ['publish'],
        ...cleanEvent,
    };
}
/**
 * Builds a media library function event configuration.
 * Filters out non-event properties and applies defaults.
 * @param event Media library function event configuration
 * @returns Complete media library function event configuration
 */
function buildMediaLibraryFunctionEvent(event) {
    const cleanEvent = Object.fromEntries(Object.entries(event).filter(([key]) => MEDIA_LIBRARY_EVENT_KEYS.has(key)));
    const fullEvent = {
        on: cleanEvent.on || ['publish'],
        ...cleanEvent,
    };
    return fullEvent;
}
/**
 * Builds a schedule function event configuration.
 * Filters out non-event properties. Does not parse expressions.
 * @param event Schedule function event configuration
 * @returns Cleaned schedule function event configuration
 */
function buildScheduleFunctionEvent(event) {
    return Object.fromEntries(Object.entries(event).filter(([key]) => SCHEDULE_EVENT_KEYS.has(key)));
}
//# sourceMappingURL=functions.js.map