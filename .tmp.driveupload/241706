/**
 * Concatenates each chunk of a string iterator to a buffer and yields the buffer when the input iterator is done
 * @param it - The input iterator
 */
export async function* concatStr(it) {
    let buf = '';
    for await (const chunk of it) {
        buf += chunk;
    }
    yield buf;
}
//# sourceMappingURL=concatStr.js.map