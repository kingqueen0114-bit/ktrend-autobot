import { getValueType } from './getValueType.js';
function callMap(mapFn, value, path) {
    const res = mapFn(value, path);
    return Array.isArray(res) ? res : [res];
}
function getPathWithKey(item, index, container) {
    if (item &&
        Array.isArray(container) &&
        typeof item === 'object' &&
        '_key' in item &&
        typeof item._key === 'string') {
        return { _key: item._key };
    }
    return index;
}
// Reduce depth first
function mapObject(reducerFn, object, path) {
    return [
        ...callMap(reducerFn, object, path),
        ...Object.keys(object).flatMap((key) => {
            const value = object[key];
            if (value === undefined)
                return [];
            return flatMapAny(reducerFn, value, [...path, getPathWithKey(value, key, object)]);
        }),
    ];
}
// Reduce depth first
function mapArray(mapFn, array, path) {
    return [
        ...callMap(mapFn, array, path),
        ...array.flatMap((item, index) => flatMapAny(mapFn, item, [...path, getPathWithKey(item, index, array)])),
    ];
}
function flatMapAny(mapFn, val, path) {
    const type = getValueType(val);
    if (type === 'object') {
        return mapObject(mapFn, val, path);
    }
    if (type === 'array') {
        return mapArray(mapFn, val, path);
    }
    return callMap(mapFn, val, path);
}
/**
 * Iterating depth first over the JSON tree, calling the mapFn for parents before children
 * @param value - the value to map deeply over
 * @param mapFn - the mapFn to call for each value
 */
export function flatMapDeep(value, mapFn) {
    return flatMapAny(mapFn, value, []);
}
//# sourceMappingURL=flatMapDeep.js.map