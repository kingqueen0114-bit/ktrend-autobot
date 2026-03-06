/**
 * @public
 */
export async function* decodeText(it) {
    const decoder = new TextDecoder();
    for await (const chunk of it) {
        yield decoder.decode(chunk, { stream: true });
    }
}
//# sourceMappingURL=decodeText.js.map