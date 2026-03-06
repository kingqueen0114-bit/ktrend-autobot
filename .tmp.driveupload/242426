import { type Path } from '@sanity/types';
import { type JsonValue } from '../../json.js';
type MapFn<T> = (value: JsonValue, path: Path) => T | T[];
/**
 * Iterating depth first over the JSON tree, calling the mapFn for parents before children
 * @param value - the value to map deeply over
 * @param mapFn - the mapFn to call for each value
 */
export declare function flatMapDeep<T>(value: JsonValue, mapFn: MapFn<T>): T[];
export {};
//# sourceMappingURL=flatMapDeep.d.ts.map