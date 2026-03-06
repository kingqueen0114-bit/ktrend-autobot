/**
 * Copied over from uint8array-extras to sort out ESM build issues. Should be replaced with imports from that module eventually
 */
const objectToString = Object.prototype.toString;
const uint8ArrayStringified = '[object Uint8Array]';
function isUint8Array(value) {
    if (!value) {
        return false;
    }
    if (value.constructor === Uint8Array) {
        return true;
    }
    return objectToString.call(value) === uint8ArrayStringified;
}
function assertUint8Array(value) {
    if (!isUint8Array(value)) {
        throw new TypeError(`Expected \`Uint8Array\`, got \`${typeof value}\``);
    }
}
export function concatUint8Arrays(arrays, totalLength) {
    if (arrays.length === 0) {
        return new Uint8Array(0);
    }
    totalLength ??= arrays.reduce((accumulator, currentValue) => accumulator + currentValue.length, 0);
    const returnValue = new Uint8Array(totalLength);
    let offset = 0;
    for (const array of arrays) {
        assertUint8Array(array);
        returnValue.set(array, offset);
        offset += array.length;
    }
    return returnValue;
}
export function areUint8ArraysEqual(a, b) {
    assertUint8Array(a);
    assertUint8Array(b);
    if (a === b) {
        return true;
    }
    if (a.length !== b.length) {
        return false;
    }
    for (const [index, element] of a.entries()) {
        if (element !== b[index]) {
            return false;
        }
    }
    return true;
}
//# sourceMappingURL=index.js.map