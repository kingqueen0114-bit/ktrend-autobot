import type { Logger } from '../logger.js';
export declare function promptForBlueprintType(): Promise<string>;
/**
 * Prompt the user for a Project after selecting an Organization.
 * @param token - The Sanity API token
 * @returns The selected project, with the projectId and displayName
 * @throws {Error} If the user does not have any projects or if the API call fails
 */
export declare function promptForProject({ token, knownOrganizationId, knownProjectId, logger, }: {
    token: string;
    knownOrganizationId?: string;
    knownProjectId?: string;
    logger: ReturnType<typeof Logger>;
}): Promise<{
    projectId: string;
    displayName: string;
}>;
/**
 * Prompt the user for a Stack ID after selecting a Project.
 * Can be used to create a new Stack or select an existing one.
 * @param projectId - The ID of the Project
 * @param token - The Sanity API token
 * @returns The selected Stack ID
 * @throws {Error} If the user does not have any Stacks or if the API call fails
 */
export declare function promptForStack({ projectId, token, logger, }: {
    projectId: string;
    token: string;
    logger: ReturnType<typeof Logger>;
}): Promise<{
    stackId: string;
    name: string;
}>;
