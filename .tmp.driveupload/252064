import { Readable, Writable } from 'node:stream';
/**
 * Type guard to check if an unknown value is a readable stream
 */ export function isReadableStream(stream) {
    return stream instanceof Readable || stream !== null && typeof stream === 'object' && 'readable' in stream && typeof stream.readable === 'boolean';
}
/**
 * Type guard to check if an unknown value is a writable stream
 */ export function isWritableStream(stream) {
    return stream instanceof Writable || stream !== null && typeof stream === 'object' && 'writable' in stream && typeof stream.writable === 'boolean';
}

//# sourceMappingURL=streamTypeGuards.js.map