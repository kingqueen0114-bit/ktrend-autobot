/**
 * @public
 */
export type JSONParser<Type> = (line: string) => Type;
/**
 * @public
 */
export interface JSONOptions<Type> {
    parse?: JSONParser<Type>;
}
/**
 * @public
 */
export declare function parseJSON<Type>(it: AsyncIterableIterator<string>, { parse }?: JSONOptions<Type>): AsyncIterableIterator<Type>;
/**
 * @public
 */
export declare function stringifyJSON(it: AsyncIterableIterator<unknown>): AsyncGenerator<string, void, unknown>;
//# sourceMappingURL=json.d.ts.map