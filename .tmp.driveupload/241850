/**
 * @public
 */
export async function* filter(it, predicate) {
    for await (const chunk of it) {
        if (await predicate(chunk)) {
            yield chunk;
        }
    }
}
//# sourceMappingURL=filter.js.map