import { getConfig } from './cliUserConfig.js';
let cachedToken;
/**
 * Get the CLI authentication token from the environment or the config file
 *
 * @returns A promise that resolves to a CLI token, or undefined if no token is found
 * @internal
 */ export async function getCliToken() {
    if (cachedToken !== undefined) {
        return cachedToken;
    }
    const token = process.env.SANITY_AUTH_TOKEN;
    if (token) {
        cachedToken = token.trim();
        return cachedToken;
    }
    cachedToken = await getConfig('authToken');
    return cachedToken;
}

//# sourceMappingURL=getCliToken.js.map