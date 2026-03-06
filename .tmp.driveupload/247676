export function getFunctionNames(resources) {
    return (resources
        ?.filter((r) => r?.type?.startsWith('sanity.function.'))
        .map((r) => r.name)
        .filter((name) => typeof name === 'string') ?? []);
}
export function findFunctionInBlueprint(blueprint, name) {
    const func = blueprint?.resources?.find((r) => r?.type?.startsWith('sanity.function.') && r.name === name);
    if (!func)
        throw Error(`Unable to find function ${name}`);
    return func;
}
export function findFunctionInStack(stack, name) {
    const func = stack?.resources?.find((r) => r?.type?.startsWith('sanity.function.') && r.name === name);
    if (!func)
        throw Error(`Unable to find function: "${name}"`);
    if (!isDeployedResource(func))
        throw Error(`Unable to find deployed function: "${name}"`);
    // return the deployed resource
    return func;
}
function isDeployedResource(r) {
    return 'externalId' in r && typeof r.externalId === 'string';
}
