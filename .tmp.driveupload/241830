export async function lastValueFrom(it, options) {
    const defaultGiven = 'defaultValue' in (options ?? {});
    let latestValue;
    let didYield = false;
    for await (const value of it) {
        didYield = true;
        latestValue = value;
    }
    if (!didYield) {
        if (defaultGiven) {
            return options.defaultValue;
        }
        throw new Error('No value yielded from async iterable. If this iterable is empty, provide a default value.');
    }
    return latestValue;
}
//# sourceMappingURL=lastValueFrom.js.map