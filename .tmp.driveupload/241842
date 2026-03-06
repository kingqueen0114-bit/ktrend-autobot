/**
 * @public
 */
export async function* parseJSON(it, { parse = JSON.parse } = {}) {
    for await (const chunk of it) {
        yield parse(chunk);
    }
}
/**
 * @public
 */
export async function* stringifyJSON(it) {
    for await (const chunk of it) {
        yield JSON.stringify(chunk);
    }
}
//# sourceMappingURL=json.js.map