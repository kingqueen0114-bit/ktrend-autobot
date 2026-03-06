/**
 * @public
 */
export type ArrayElement<A> = A extends readonly (infer T)[] ? T : never;
/**
 * @public
 */
export type NormalizeReadOnlyArray<T> = T extends readonly [infer NP, ...infer Rest] ? [NP, ...Rest] : T extends readonly (infer NP)[] ? NP[] : T;
/**
 * @public
 */
export type AnyArray<T = any> = readonly T[] | T[];
/**
 * @public
 */
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;
/**
 * @public
 */
export type Tuplify<T> = T extends readonly [infer NP, ...infer Rest] ? [NP, ...Rest] : T extends readonly (infer NP)[] ? NP[] : [T];
//# sourceMappingURL=typeUtils.d.ts.map