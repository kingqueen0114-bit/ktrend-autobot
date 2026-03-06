import split from 'split2';
import { validateDocument } from '../documentHasErrors.js';
import { ReplacementCharError, validateLineForReplacementChar } from './validateReplacementCharacters.js';
export function getJsonStreamer(options = {}) {
    let lineNumber = 0;
    const { allowReplacementCharacters } = options;
    const getErrorMessage = (err)=>{
        const suffix = lineNumber === 1 ? '\n\nMake sure this is valid ndjson (one JSON-document *per line*)' : '';
        return `Failed to parse line #${lineNumber}: ${err.message}${suffix}`;
    };
    return split(parseRow);
    function parseRow(row) {
        lineNumber++;
        if (!row) {
            return undefined;
        }
        try {
            // Check for replacement characters before parsing JSON
            if (allowReplacementCharacters !== true) {
                const replacementError = validateLineForReplacementChar(row, lineNumber);
                if (replacementError) {
                    throw new ReplacementCharError(replacementError);
                }
            }
            const doc = JSON.parse(row);
            const error = validateDocument(doc);
            if (error) {
                throw new Error(error);
            }
            return doc;
        } catch (err) {
            if (err instanceof ReplacementCharError) {
                this.emit('error', err);
            } else if (err instanceof Error) {
                this.emit('error', new Error(getErrorMessage(err)));
            } else {
                this.emit('error', new Error(`Unknown error occurred at line #${lineNumber}: ${String(err)}`));
            }
        }
        return undefined;
    }
}

//# sourceMappingURL=getJsonStreamer.js.map