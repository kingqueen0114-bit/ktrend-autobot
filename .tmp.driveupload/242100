import { concatUint8Arrays } from '../uint8arrays/index.js';
export function peekInto(readable, options) {
    const { size } = options;
    return new Promise((resolve, reject) => {
        let totalBytesRead = 0;
        let streamCompleted = false;
        const chunks = [];
        const reader = readable.getReader();
        function settled() {
            const head = concatUint8Arrays(chunks);
            resolve([
                head,
                new ReadableStream({
                    async pull(controller) {
                        const { done, value } = await reader.read();
                        if (done) {
                            controller.close();
                        }
                        else {
                            controller.enqueue(value);
                        }
                    },
                    start(controller) {
                        controller.enqueue(head);
                        if (streamCompleted) {
                            controller.close();
                        }
                    },
                }),
            ]);
        }
        ;
        (async () => {
            while (true) {
                const { done, value: chunk } = await reader.read();
                if (done) {
                    streamCompleted = true;
                    break;
                }
                else {
                    totalBytesRead += chunk.byteLength;
                    chunks.push(chunk);
                    if (totalBytesRead >= size) {
                        break;
                    }
                }
            }
        })().then(settled, reject);
    });
}
//# sourceMappingURL=peekInto.js.map