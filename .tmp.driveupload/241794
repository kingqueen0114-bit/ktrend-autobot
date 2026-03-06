import { filter } from './filter.js';
import { parseJSON } from './json.js';
import { split } from './split.js';
/**
 * @public
 */
export function parse(it, options) {
    return parseJSON(filter(split(it, '\n'), (line) => Boolean(line && line.trim())), options);
}
/**
 * @public
 */
export async function* stringify(iterable) {
    for await (const doc of iterable) {
        yield `${JSON.stringify(doc)}\n`;
    }
}
//# sourceMappingURL=ndjson.js.map