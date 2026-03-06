/**
 * @public
 */
export async function* split(it, delimiter) {
    let buf = '';
    for await (const chunk of it) {
        buf += chunk;
        if (buf.includes(delimiter)) {
            const lastIndex = buf.lastIndexOf(delimiter);
            const parts = buf.slice(0, Math.max(0, lastIndex)).split(delimiter);
            for (const part of parts) {
                yield part;
            }
            buf = buf.slice(Math.max(0, lastIndex + delimiter.length));
        }
    }
    yield buf;
}
//# sourceMappingURL=split.js.map