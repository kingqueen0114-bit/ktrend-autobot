export function asyncIterableToStream(it) {
    return new ReadableStream({
        async pull(controller) {
            const { done, value } = await it.next();
            if (done) {
                controller.close();
            }
            else {
                controller.enqueue(value);
            }
        },
    });
}
//# sourceMappingURL=asyncIterableToStream.js.map