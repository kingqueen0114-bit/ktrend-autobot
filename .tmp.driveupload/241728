function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
/**
 * @public
 */
export async function* delay(it, ms) {
    for await (const chunk of it) {
        await sleep(ms);
        yield chunk;
    }
}
//# sourceMappingURL=delay.js.map