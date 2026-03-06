import { createClient } from '@sanity/client';
import { limitClientConcurrency } from './limitClientConcurrency.js';
export function createContextClient(config) {
    return restrictClient(limitClientConcurrency(createClient({ ...config, requestTagPrefix: 'sanity.migration', useCdn: false })));
}
/**
 * @public
 */
export const ALLOWED_PROPERTIES = [
    'fetch',
    'clone',
    'config',
    'withConfig',
    'getDocument',
    'getDocuments',
    'users',
    'projects',
];
function restrictClient(client) {
    return new Proxy(client, {
        get: (target, property) => {
            switch (property) {
                case 'clone': {
                    return (...args) => {
                        return restrictClient(target.clone(...args));
                    };
                }
                case 'config': {
                    return (...args) => {
                        const result = target.config(...args);
                        // if there is a config, it returns a client so we need to wrap again
                        if (args[0])
                            return restrictClient(result);
                        return result;
                    };
                }
                case 'withConfig': {
                    return (...args) => {
                        return restrictClient(target.withConfig(...args));
                    };
                }
                default: {
                    if (typeof property === 'string' &&
                        ALLOWED_PROPERTIES.includes(property)) {
                        return target[property];
                    }
                    throw new Error(`Client method "${String(property)}" can not be called during a migration. Only ${ALLOWED_PROPERTIES.join(', ')} are allowed.`);
                }
            }
        },
    });
}
//# sourceMappingURL=createContextClient.js.map