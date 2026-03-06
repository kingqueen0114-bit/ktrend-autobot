import { streamToAsyncIterator } from '../utils/streamToAsyncIterator.js';
class HTTPError extends Error {
    statusCode;
    constructor(statusCode, message) {
        super(message);
        this.name = 'HTTPError';
        this.statusCode = statusCode;
    }
}
export async function assert2xx(res) {
    if (res.status < 200 || res.status > 299) {
        const jsonResponse = (await res.json().catch(() => null));
        let message;
        if (jsonResponse?.error) {
            if (typeof jsonResponse.error === 'object') {
                message = jsonResponse.error.description
                    ? `${jsonResponse.error.type || res.status}: ${jsonResponse.error.description}`
                    : `${jsonResponse.error.type || res.status}: ${jsonResponse.message || 'Unknown error'}`;
            }
            else {
                message = `${jsonResponse.error}: ${jsonResponse.message || ''}`;
            }
        }
        else {
            message = `HTTP Error ${res.status}: ${res.statusText}`;
        }
        throw new HTTPError(res.status, message);
    }
}
export async function fetchStream({ init, url }) {
    const response = await fetch(url, init);
    await assert2xx(response);
    if (response.body === null)
        throw new Error('No response received');
    return response.body;
}
export async function fetchAsyncIterator(options) {
    return streamToAsyncIterator(await fetchStream(options));
}
//# sourceMappingURL=fetchStream.js.map