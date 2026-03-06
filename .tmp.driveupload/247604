import { validateCorsOrigin, validateDataset, validateDocumentWebhook, validateRobot, validateRole, } from '@sanity/blueprints';
import { SANITY_FUNCTION_DOCUMENT, SANITY_FUNCTION_MEDIA_LIBRARY_ASSET, SANITY_FUNCTION_SCHEDULE, } from '../constants.js';
// type narrowing with predicate functions
export function isLocalFunctionResource(r) {
    return r.type.startsWith('sanity.function.');
}
export function isDocumentFunctionResource(r) {
    return r.type === SANITY_FUNCTION_DOCUMENT;
}
export function isMediaLibraryAssetFunctionResource(r) {
    return r.type === SANITY_FUNCTION_MEDIA_LIBRARY_ASSET;
}
export function isScheduleFunctionResource(r) {
    return r.type === SANITY_FUNCTION_SCHEDULE;
}
export function isLocalFunctionCollection(r) {
    return r.type === 'sanity.experimental.functions-collection';
}
export function isScheduleEvent(e) {
    return e !== null && typeof e === 'object' && ('hour' in e || 'expression' in e);
}
export function isCorsOriginResource(r) {
    return validateCorsOrigin(r).length === 0;
}
export function isRobotResource(r) {
    return validateRobot(r).length === 0;
}
export function isRoleResource(r) {
    return validateRole(r).length === 0;
}
export function isDatasetResource(r) {
    return validateDataset(r).length === 0;
}
export function isWebhookResource(r) {
    return validateDocumentWebhook(r).length === 0;
}
export function isEventType(arg) {
    return ['create', 'update', 'delete'].includes(arg);
}
export function isGroqContextOptions(context) {
    return 'clientOptions' in context;
}
/** @internal */
export var BlueprintParserErrorType;
(function (BlueprintParserErrorType) {
    BlueprintParserErrorType["InvalidProperty"] = "invalid_property";
    BlueprintParserErrorType["InvalidVersion"] = "invalid_version";
    BlueprintParserErrorType["InvalidType"] = "invalid_type";
    BlueprintParserErrorType["MissingRequiredProperty"] = "missing_required_property";
    BlueprintParserErrorType["DuplicateName"] = "duplicate_name";
    BlueprintParserErrorType["InvalidFormat"] = "invalid_format";
    BlueprintParserErrorType["InvalidValue"] = "invalid_value";
    BlueprintParserErrorType["JsonValidationError"] = "json_validation_error";
    BlueprintParserErrorType["InvalidInput"] = "invalid_input";
    BlueprintParserErrorType["MissingParameter"] = "missing_parameter";
})(BlueprintParserErrorType || (BlueprintParserErrorType = {}));
