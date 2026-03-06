/**
 * @public
 */
export async function* take(it, count) {
    let i = 0;
    for await (const chunk of it) {
        if (i++ >= count)
            return;
        yield chunk;
    }
}
//# sourceMappingURL=take.js.map