import { getRandomValues } from 'node:crypto';
import { isPlainObject } from 'lodash-es';
// Note: Mutates in-place
function assignArrayKeys(obj) {
    if (Array.isArray(obj)) {
        obj.forEach((item)=>{
            if (isPlainObject(item) && !('_key' in item)) {
                ;
                item._key = generateKey();
            }
            assignArrayKeys(item);
        });
        return obj;
    }
    if (isPlainObject(obj)) {
        const plainObj = obj;
        Object.keys(plainObj).forEach((key)=>{
            assignArrayKeys(plainObj[key]);
        });
        return obj;
    }
    return obj;
}
function generateKey(length = 8) {
    const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    const bytes = new Uint8Array(length);
    getRandomValues(bytes);
    return Array.from(bytes, (b)=>chars[b % chars.length]).join('');
}
export { assignArrayKeys };

//# sourceMappingURL=assignArrayKeys.js.map