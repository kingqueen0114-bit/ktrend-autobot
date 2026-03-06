import { type BlueprintCorsOriginResource, type BlueprintDatasetResource, type BlueprintDocumentWebhookResource, type BlueprintResource, type BlueprintRobotResource, type BlueprintRoleResource } from '@sanity/blueprints';
import type { Blueprint } from '@sanity/blueprints-parser';
import { SANITY_FUNCTION_DOCUMENT, SANITY_FUNCTION_MEDIA_LIBRARY_ASSET, SANITY_FUNCTION_SCHEDULE } from '../constants.js';
export type ScopeType = 'organization' | 'project';
/** Result utility type */
export type Result<T, E = string> = {
    ok: true;
    value: T;
} | {
    ok: false;
    error: E;
};
/** @internal */
export interface AuthParams {
    token: string;
    scopeType: ScopeType;
    scopeId: string;
}
/** @internal */
export type GroqRule = GroqRuleDocumentFunction | GroqRuleMediaLibraryFunction;
export interface GroqRuleBase {
    on: Array<string>;
    filter?: string;
    projection?: string;
}
interface GroqRuleDocumentFunction extends GroqRuleBase {
    includeDrafts?: boolean;
    includeAllVersions?: boolean;
    resource?: {
        type: 'dataset';
        id: string;
    };
}
interface GroqRuleMediaLibraryFunction extends GroqRuleBase {
    resource: {
        type: 'media-library';
        id: string;
    };
}
export interface FunctionResourceScheduleExplicitEvent {
    minute: string;
    hour: string;
    dayOfMonth: string;
    month: string;
    dayOfWeek: string;
}
interface FunctionResourceScheduleExpressionEvent {
    expression: string;
}
type FunctionResourceScheduleEvent = FunctionResourceScheduleExplicitEvent | FunctionResourceScheduleExpressionEvent;
/** The Blueprint resource as represented in the Blueprints API database */
export interface BlueprintResourceRecord extends BlueprintResource {
    id: string;
    externalId?: string | null;
    parameters: Record<string, unknown>;
}
/** The deployed resource; complete with external ID */
export interface DeployedResource extends BlueprintResourceRecord {
    externalId: string;
}
export declare function isLocalFunctionResource(r: BlueprintResource): r is FunctionResourceBase;
export declare function isDocumentFunctionResource<T extends BlueprintResource>(r: T): r is T & FunctionResourceDocument;
export declare function isMediaLibraryAssetFunctionResource<T extends BlueprintResource>(r: T): r is T & FunctionResourceMediaLibraryAsset;
export declare function isScheduleFunctionResource<T extends BlueprintResource>(r: T): r is T & FunctionResourceSchedule;
export declare function isLocalFunctionCollection<T extends BlueprintResource>(r: T): r is T & FunctionsCollection;
export declare function isScheduleEvent(e: unknown): e is FunctionResourceScheduleEvent;
export declare function isCorsOriginResource(r: unknown): r is BlueprintCorsOriginResource;
export declare function isRobotResource(r: unknown): r is BlueprintRobotResource;
export declare function isRoleResource(r: unknown): r is BlueprintRoleResource;
export declare function isDatasetResource(r: unknown): r is BlueprintDatasetResource;
export declare function isWebhookResource(r: unknown): r is BlueprintDocumentWebhookResource;
/** @internal */
export type FunctionResource = FunctionResourceDocument | FunctionResourceMediaLibraryAsset | FunctionResourceSchedule | FunctionResourceBase;
export type FunctionGroqResource = FunctionResourceDocument | FunctionResourceMediaLibraryAsset;
export interface FunctionResourceBase extends BlueprintResource {
    displayName?: string;
    src?: string;
    autoResolveDeps?: boolean;
    transpile?: boolean;
    memory?: number;
    timeout?: number;
    env?: Record<string, string>;
    event?: GroqRuleBase | FunctionResourceScheduleEvent;
}
interface FunctionResourceDocument extends FunctionResourceBase {
    type: typeof SANITY_FUNCTION_DOCUMENT;
    event?: GroqRuleDocumentFunction;
}
interface FunctionResourceMediaLibraryAsset extends FunctionResourceBase {
    type: typeof SANITY_FUNCTION_MEDIA_LIBRARY_ASSET;
    event: GroqRuleMediaLibraryFunction;
}
interface FunctionResourceSchedule extends FunctionResourceBase {
    type: typeof SANITY_FUNCTION_SCHEDULE;
    event: FunctionResourceScheduleEvent;
}
export interface CollectionFunction {
    type: typeof SANITY_FUNCTION_DOCUMENT | typeof SANITY_FUNCTION_SCHEDULE | typeof SANITY_FUNCTION_MEDIA_LIBRARY_ASSET;
    src: string;
    name: string;
    displayName?: string;
    event?: GroqRuleBase | FunctionResourceScheduleEvent;
    memory?: number;
    timeout?: number;
    env?: Record<string, string>;
}
/** @internal */
export interface FunctionsCollection extends BlueprintResource {
    type: 'sanity.experimental.functions-collection';
    name: string;
    src?: string;
    functions: Array<FunctionResourceBase>;
}
export interface CorsResource extends BlueprintResource {
    origin?: string;
}
export interface Stack {
    id: string;
    name: string;
    displayName: string;
    scopeType: ScopeType;
    scopeId: string;
    resources: Array<BlueprintResourceRecord>;
    createdAt?: string;
    updatedAt?: string;
    recentOperation?: StackOperation;
}
/** @internal */
export interface StackOperation {
    id: string;
    status: string;
    createdAt?: string;
    completedAt?: string;
}
/** @internal */
export interface StackMutation {
    name: string;
    scopeType: ScopeType;
    scopeId: string;
    document: Blueprint;
}
/** @internal */
export interface BuildPayloadOptions {
    data?: string;
    file?: string;
    timeout?: number;
}
/** @internal */
export interface InvokeGroqPayloadOptions {
    payload?: Record<string, unknown>;
    event: EventType;
    before: Record<string, unknown> | null;
    after: Record<string, unknown> | null;
}
export interface InvokeSchedulePayloadOptions {
    payload?: Record<string, unknown>;
    event: 'schedule';
}
export type InvokePayloadOptions = InvokeGroqPayloadOptions | InvokeSchedulePayloadOptions;
export type InvokePayloadMetadata = Pick<InvokeGroqPayloadOptions, 'event' | 'before' | 'after'> | Pick<InvokeSchedulePayloadOptions, 'event'>;
export type EventType = 'create' | 'update' | 'delete';
export declare function isEventType(arg: string): arg is EventType;
/** @internal */
export interface InvokeGroqContextOptions {
    clientOptions: {
        apiVersion?: string;
        dataset?: string;
        projectId?: string;
        organizationId?: string;
        token?: string;
    };
    /** The resource type of the event source; resource type that invoked the function. */
    eventResourceType: string;
    /** The resource ID of the event source; resource ID that invoked the function. */
    eventResourceId: string;
    /** The resource type of the function container; resource type that houses the function. */
    functionResourceType: string;
    /** The resource ID of the function container; resource ID that houses the function. */
    functionResourceId: string;
}
export type InvokeScheduleContextOptions = Record<string, never>;
export type InvokeContextOptions = InvokeGroqContextOptions | InvokeScheduleContextOptions;
export declare function isGroqContextOptions(context: InvokeContextOptions): context is InvokeGroqContextOptions;
/** @internal */
export interface InvokeExecutionOptions {
    forceColor?: boolean;
    timeout?: number;
}
/** @internal */
export interface InvocationResponse {
    error: InvocationError | undefined;
    json: JsonInvocationResponse | undefined;
    logs: string | undefined;
    timings?: Record<string, number>;
}
/** @internal */
export interface InvocationError {
    stack: string;
    message: string;
    name: string;
}
/** @internal */
export interface JsonInvocationResponse {
    data: Record<string, unknown> | undefined;
}
/** @internal */
export interface BlueprintLog {
    id: string;
    timestamp: string;
    level: string;
    message: string;
    duration: number | null;
    metadata: Record<string, unknown> | null;
    blueprintId: string;
    stackId: string;
    operationId: string;
    resourceId: string | null;
    requestId: string | null;
}
/** @internal */
export interface FunctionLog {
    time: string;
    requestId: string;
    level: string;
    message: string;
}
/** @internal */
export declare enum BlueprintParserErrorType {
    InvalidProperty = "invalid_property",
    InvalidVersion = "invalid_version",
    InvalidType = "invalid_type",
    MissingRequiredProperty = "missing_required_property",
    DuplicateName = "duplicate_name",
    InvalidFormat = "invalid_format",
    InvalidValue = "invalid_value",
    JsonValidationError = "json_validation_error",
    InvalidInput = "invalid_input",
    MissingParameter = "missing_parameter"
}
/** @internal */
export interface BlueprintParserError {
    message: string;
    type: string;
}
/** @internal */
export declare interface FetchConfig {
    mediaLibraryId?: string;
    token?: string;
    apiHost?: string;
    apiVersion?: string;
}
export {};
