import { pMapIterable } from 'p-map';
export async function mapAsync(it, project, concurrency) {
    return pMapIterable(it, (v) => project(v), {
        concurrency: concurrency,
    });
}
//# sourceMappingURL=mapAsync.js.map