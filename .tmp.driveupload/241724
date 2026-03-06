import { evaluate, parse } from 'groq-js';
export function parseGroqFilter(filter) {
    try {
        return parse(`*[${filter}]`);
    }
    catch (err) {
        if (err instanceof Error) {
            err.message = `Failed to parse GROQ filter "${filter}": ${err.message}`;
            throw err;
        }
        throw new Error(`Failed to parse GROQ filter "${filter}": ${String(err)}`);
    }
}
export async function matchesFilter(parsedFilter, document) {
    const result = await (await evaluate(parsedFilter, { dataset: [document] })).get();
    return result.length === 1;
}
//# sourceMappingURL=groqFilter.js.map