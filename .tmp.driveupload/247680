import { BlueprintParserErrorType, isDocumentFunctionResource, isMediaLibraryAssetFunctionResource, isScheduleEvent, } from '../types.js';
export function validateFunctionName(name) {
    // must be 3+ characters, no special characters, no spaces, allow _ and -
    return /^[a-zA-Z0-9][a-zA-Z0-9_-]{2,}$/.test(name);
}
const validFunctionEventNames = ['publish', 'create', 'update', 'delete'];
export function validateFunctionResource(resource) {
    const { name: fnName } = resource;
    const msgPrefix = `Function "${fnName}":`;
    const errors = [];
    if (!validateFunctionName(resource.name)) {
        errors.push({
            message: `${msgPrefix} Function name must be at least 3 characters, start with a letter or number, and only contain letters, numbers, _ or -`,
            type: BlueprintParserErrorType.InvalidProperty,
        });
    }
    if (!resource.type.startsWith('sanity.function.')) {
        errors.push({
            message: `${msgPrefix} Resource type must start with "sanity.function."`,
            type: BlueprintParserErrorType.InvalidType,
        });
    }
    if (isScheduleEvent(resource.event)) {
        const event = resource.event;
        const hasExpression = 'expression' in event;
        const hasExplicitFields = 'minute' in event ||
            'hour' in event ||
            'dayOfMonth' in event ||
            'month' in event ||
            'dayOfWeek' in event;
        if (hasExpression && hasExplicitFields) {
            errors.push({
                type: BlueprintParserErrorType.InvalidFormat,
                message: 'Cannot specify both `expression` and explicit cron fields (`minute`, `hour`, `dayOfMonth`, `month`, `dayOfWeek`)',
            });
        }
        else if (!hasExpression && !hasExplicitFields) {
            errors.push({
                type: BlueprintParserErrorType.MissingRequiredProperty,
                message: 'Either `expression` or explicit cron fields (`minute`, `hour`, `dayOfMonth`, `month`, `dayOfWeek`) must be provided',
            });
        }
        else if (hasExpression) {
            const expressionParts = event.expression.split(' ');
            if (expressionParts.length !== 5) {
                errors.push({
                    type: BlueprintParserErrorType.InvalidFormat,
                    message: 'Invalid `expression` format. Cron fields (`minute`, `hour`, `dayOfMonth`, `month`, `dayOfWeek`) must be provided',
                });
            }
            else {
                const [minute, hour, dayOfWeek, month, dayOfMonth] = expressionParts;
                errors.push(...validateScheduleEvent(msgPrefix, { minute, hour, dayOfWeek, month, dayOfMonth }));
            }
        }
        else if (hasExplicitFields) {
            errors.push(...validateScheduleEvent(msgPrefix, event));
        }
    }
    else {
        if (!resource.event || !Array.isArray(resource.event.on) || resource.event.on.length === 0) {
            errors.push({
                message: `${msgPrefix} event.on must be a non-empty array`,
                type: BlueprintParserErrorType.MissingRequiredProperty,
            });
        }
        else if (!resource.event.on.every((evt) => validFunctionEventNames.includes(evt))) {
            errors.push({
                message: `${msgPrefix} event.on values must be one of ${validFunctionEventNames.map((e) => `"${e}"`).join(', ')}`,
                type: BlueprintParserErrorType.InvalidValue,
            });
        }
        if (resource.event?.filter && typeof resource.event.filter !== 'string') {
            errors.push({
                message: `${msgPrefix} event.filter must be a string`,
                type: BlueprintParserErrorType.InvalidType,
            });
        }
        if (resource.event?.projection && typeof resource.event.projection !== 'string') {
            errors.push({
                message: `${msgPrefix} event.projection must be a string`,
                type: BlueprintParserErrorType.InvalidType,
            });
        }
    }
    if (resource.memory !== undefined) {
        if (!Number.isInteger(resource.memory)) {
            errors.push({
                message: `${msgPrefix} memory must be an integer`,
                type: BlueprintParserErrorType.InvalidType,
            });
        }
        else if (resource.memory < 1 || resource.memory > 10) {
            errors.push({
                message: `${msgPrefix} memory must be between 1 and 10 (GB)`,
                type: BlueprintParserErrorType.InvalidValue,
            });
        }
    }
    if (resource.timeout !== undefined) {
        if (!Number.isInteger(resource.timeout)) {
            errors.push({
                message: `${msgPrefix} timeout must be an integer`,
                type: BlueprintParserErrorType.InvalidType,
            });
        }
        else if (resource.timeout < 1 || resource.timeout > 900) {
            errors.push({
                message: `${msgPrefix} timeout must be between 1 and 900 (seconds)`,
                type: BlueprintParserErrorType.InvalidValue,
            });
        }
    }
    if (resource.env !== undefined) {
        if (typeof resource.env !== 'object') {
            errors.push({
                message: `${msgPrefix} env must be an object`,
                type: BlueprintParserErrorType.InvalidType,
            });
        }
        else {
            if (!Object.keys(resource.env).every((key) => typeof key === 'string')) {
                errors.push({
                    message: `${msgPrefix} All env keys must be strings`,
                    type: BlueprintParserErrorType.InvalidFormat,
                });
            }
            if (!Object.values(resource.env).every((value) => typeof value === 'string')) {
                errors.push({
                    message: `${msgPrefix} All env values must be strings`,
                    type: BlueprintParserErrorType.InvalidFormat,
                });
            }
        }
    }
    if (resource.event && 'resource' in resource.event && resource.event.resource) {
        if (!resource.event.resource.type) {
            errors.push({
                message: `${msgPrefix} event.resource.type must be defined`,
                type: BlueprintParserErrorType.MissingRequiredProperty,
            });
        }
        if (!resource.event.resource.id) {
            errors.push({
                message: `${msgPrefix} event.resource.id must be defined`,
                type: BlueprintParserErrorType.MissingRequiredProperty,
            });
        }
    }
    if (isMediaLibraryAssetFunctionResource(resource)) {
        if (resource.event.resource.type !== 'media-library') {
            errors.push({
                message: `${msgPrefix} event.resource.type must be "media-library"`,
                type: BlueprintParserErrorType.InvalidType,
            });
        }
    }
    if (isDocumentFunctionResource(resource) && resource.event) {
        if (resource.event.includeDrafts && typeof resource.event.includeDrafts !== 'boolean') {
            errors.push({
                message: `${msgPrefix} event.includeDrafts must be a boolean`,
                type: BlueprintParserErrorType.InvalidType,
            });
        }
        if (resource.event.includeAllVersions &&
            typeof resource.event.includeAllVersions !== 'boolean') {
            errors.push({
                message: `${msgPrefix} event.includeAllVersions must be a boolean`,
                type: BlueprintParserErrorType.InvalidType,
            });
        }
        if (resource.event.resource) {
            if (!resource.event.resource.type || resource.event.resource.type !== 'dataset') {
                errors.push({
                    message: `${msgPrefix} event.resource.type must be "dataset"`,
                    type: BlueprintParserErrorType.InvalidType,
                });
            }
            // Ensure exactly one period is passed into the ID to conform to the format <projectId>.<datasetName>
            if (!resource.event.resource.id || resource.event.resource.id.split('.').length !== 2) {
                errors.push({
                    message: `${msgPrefix} event.resource.id must be of the form <projectId>.<datasetName>. <datasetName> can be "*" to signify "all datasets in project with ID <projectId>."`,
                    type: BlueprintParserErrorType.InvalidFormat,
                });
            }
            // TODO: validate the project ID and dataset names exist by making an API call?
            // NB: this is done by the functions service
        }
    }
    return errors;
}
function validateScheduleEvent(msgPrefix, event) {
    const errors = [];
    const properties = [
        { name: 'minute', regex: MINUTES },
        { name: 'hour', regex: HOURS },
        { name: 'dayOfMonth', regex: DAY_OF_MONTH },
        { name: 'month', regex: MONTH },
        { name: 'dayOfWeek', regex: DAY_OF_WEEK },
    ];
    properties.forEach((prop) => {
        const { name, regex } = prop;
        if (!(name in event)) {
            errors.push({
                type: BlueprintParserErrorType.MissingRequiredProperty,
                message: `${msgPrefix} '${name}' must be provided`,
            });
            return;
        }
        const value = event[name];
        if (typeof value !== 'string') {
            errors.push({
                type: BlueprintParserErrorType.InvalidType,
                message: `${msgPrefix} '${name}' must be a string`,
            });
            return;
        }
        if (!isValidCronPart(regex, value)) {
            errors.push({
                type: BlueprintParserErrorType.InvalidValue,
                message: `${msgPrefix} ${name} field contains invalid value: ${value}`,
            });
        }
    });
    return errors;
}
/**
 * Validates that each cron part adheres to it's rules
 *
 * @param {RegExp} regex the regular expression that corresponds to the part of the cron expression you are testing
 * @param {string} value the string value of part of the cron expression you are testing
 * @returns {boolean} whether or not the cron part is valid
 */
function isValidCronPart(regex, value) {
    return regex.test(value) && checkAscendingRanges(value) && checkNoZeroStep(value);
}
const MINUTES = /^(\*(\/([1-5]?\d))?|([0-5]?\d)(-[0-5]?\d)?(\/([1-5]?\d))?)(,(\*(\/([1-5]?\d))?|([0-5]?\d)(-[0-5]?\d)?(\/([1-5]?\d))?))*$/;
const HOURS = /^(\*(\/([1-9]|1\d|2[0-3]))?|([01]?\d|2[0-3])(-([01]?\d|2[0-3]))?(\/([1-9]|1\d|2[0-3]))?)(,(\*(\/([1-9]|1\d|2[0-3]))?|([01]?\d|2[0-3])(-([01]?\d|2[0-3]))?(\/([1-9]|1\d|2[0-3]))?))*$/;
const DAY_OF_MONTH = /^(\*(\/([1-9]|[12]\d|3[01]))?|([1-9]|[12]\d|3[01])(-([1-9]|[12]\d|3[01]))?(\/([1-9]|[12]\d|3[01]))?)(,(\*(\/([1-9]|[12]\d|3[01]))?|([1-9]|[12]\d|3[01])(-([1-9]|[12]\d|3[01]))?(\/([1-9]|[12]\d|3[01]))?))*$/;
const MONTH = /^(\*(\/([1-9]|1[0-2]))?|([1-9]|1[0-2]|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(-([1-9]|1[0-2]|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC))?(\/([1-9]|1[0-2]))?)(,(\*(\/([1-9]|1[0-2]))?|([1-9]|1[0-2]|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(-([1-9]|1[0-2]|JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC))?(\/([1-9]|1[0-2]))?))*$/i;
const DAY_OF_WEEK = /^(\*(\/([0-7]))?|([0-7]|SUN|MON|TUE|WED|THU|FRI|SAT)(-([0-7]|SUN|MON|TUE|WED|THU|FRI|SAT))?(\/([0-7]))?)(,(\*(\/([0-7]))?|([0-7]|SUN|MON|TUE|WED|THU|FRI|SAT)(-([0-7]|SUN|MON|TUE|WED|THU|FRI|SAT))?(\/([0-7]))?))*$/i;
/**
 *
 * @param {string} value the string value of part of the cron expression you are testing
 * @returns {boolean} returns true if the range is valid
 */
function checkAscendingRanges(value) {
    for (const part of value.split(',')) {
        if (part.includes('-')) {
            const [start, right] = part.split('-');
            const end = right.split('/')[0]; // remove /step
            const s = Number(start);
            const e = Number(end);
            if (s > e)
                return false;
        }
    }
    return true;
}
/**
 * @param {string} value the string value of part of the cron expression you are testing
 * @returns {boolean} makes sure we are not trying to divide by zero
 */
function checkNoZeroStep(value) {
    for (const part of value.split(',')) {
        if (part.includes('/')) {
            const step = Number(part.split('/')[1]);
            if (step === 0)
                return false;
        }
    }
    return true;
}
