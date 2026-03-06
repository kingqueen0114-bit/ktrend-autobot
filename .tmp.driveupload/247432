import type { Logger } from '../../utils/logger.js';
import type { ScopeType } from '../../utils/types.js';
export declare const projectsApiPath: string;
export declare const orgsApiPath: string;
export interface Project {
    id: string;
    displayName: string;
    studioHost: string | null;
    organizationId: string;
    isBlocked: boolean;
    isDisabled: boolean;
    isDisabledByUser: boolean;
    activityFeedEnabled: boolean;
    createdAt: string;
    updatedAt: string;
}
interface ListProjectsResponse {
    ok: boolean;
    error: string | null;
    projects: Project[];
}
export declare function listProjects({ token, logger, }: {
    token: string;
    logger: ReturnType<typeof Logger>;
}): Promise<ListProjectsResponse>;
interface GroupedProjectsByOrganizationResponse {
    ok: boolean;
    error: string | null;
    organizations: GroupedProjects[];
}
interface GroupedProjects {
    organization: {
        id: string;
        name: string;
    };
    projects?: Project[];
}
export declare function groupProjectsByOrganization({ token, logger, }: {
    token: string;
    logger: ReturnType<typeof Logger>;
}): Promise<GroupedProjectsByOrganizationResponse>;
interface GetProjectResponse {
    ok: boolean;
    error: string | null;
    project: Project;
}
export declare function getProject({ token, scopeId, scopeType, logger, }: {
    token: string;
    scopeId: string;
    scopeType: ScopeType;
    logger: ReturnType<typeof Logger>;
}): Promise<GetProjectResponse>;
export {};
