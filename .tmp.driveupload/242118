/**
 * Takes a source stream that will be drained and written to the provided file name as fast as possible.
 * and returns a function that can be called to create multiple readable stream on top of the buffer file.
 * It will start pulling data from the source stream once the first readableStream is created, writing to the buffer file in the background.
 * The readable streams and can be read at any rate (but will not receive data faster than the buffer file is written to).
 * Note: by default, buffering will run to completion, and this may prevent the process from exiting after done reading from the
 * buffered streams. To stop writing to the buffer file, an AbortSignal can be provided and once it's controller aborts, the buffer file will
 * stop. After the signal is aborted, no new buffered readers can be created.
 *
 * @param source - The source readable stream. Will be drained as fast as possible.
 * @param filename - The filename to write to.
 * @param options - Optional AbortSignal to stop writing to the buffer file.
 * @returns A function that can be called multiple times to create a readable stream on top of the buffer file.
 */
export declare function bufferThroughFile(source: globalThis.ReadableStream<Uint8Array>, filename: string, options?: {
    keepFile?: boolean;
    signal: AbortSignal;
}): () => import("node:stream/web").ReadableStream<Uint8Array<ArrayBufferLike>>;
//# sourceMappingURL=bufferThroughFile.d.ts.map