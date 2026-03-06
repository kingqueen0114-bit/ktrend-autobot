import { createClient, type SanityClient } from '@sanity/client';
export declare function createContextClient(config: Parameters<typeof createClient>[0]): RestrictedClient;
/**
 * @public
 */
export declare const ALLOWED_PROPERTIES: readonly ["fetch", "clone", "config", "withConfig", "getDocument", "getDocuments", "users", "projects"];
/**
 * @public
 */
export type AllowedMethods = (typeof ALLOWED_PROPERTIES)[number];
/**
 * @public
 */
export type RestrictedClient = Pick<SanityClient, AllowedMethods>;
//# sourceMappingURL=createContextClient.d.ts.map