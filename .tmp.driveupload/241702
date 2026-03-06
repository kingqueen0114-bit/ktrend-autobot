export async function* tap(it, interceptor) {
    for await (const chunk of it) {
        interceptor(chunk);
        yield chunk;
    }
}
//# sourceMappingURL=tap.js.map