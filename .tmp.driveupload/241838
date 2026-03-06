export async function firstValueFrom(it, options) {
    const defaultGiven = 'defaultValue' in (options ?? {});
    let firstValue;
    let didYield = false;
    for await (const value of it) {
        didYield = true;
        firstValue = value;
        break;
    }
    if (!didYield) {
        if (defaultGiven) {
            return options.defaultValue;
        }
        throw new Error('No value yielded from async iterable. If this iterable is empty, provide a default value.');
    }
    return firstValue;
}
//# sourceMappingURL=firstValueFrom.js.map