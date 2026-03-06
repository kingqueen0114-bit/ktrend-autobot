import config from '../../config.js';
import { createTracedFetch } from '../../utils/traced-fetch.js';
const { apiUrl } = config;
export const projectsApiPath = `${apiUrl}v2021-06-07/projects`;
export const orgsApiPath = `${apiUrl}v2021-06-07/organizations`;
export async function listProjects({ token, logger, }) {
    const fetchFn = createTracedFetch(logger);
    const projectsFetch = await fetchFn(projectsApiPath, {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });
    const projects = await projectsFetch.json();
    return {
        ok: projectsFetch.ok,
        error: projectsFetch.ok ? null : projects.error?.message,
        projects,
    };
}
export async function groupProjectsByOrganization({ token, logger, }) {
    const fetchFn = createTracedFetch(logger);
    const projectsResponse = await listProjects({ token, logger });
    if (!projectsResponse.ok) {
        return {
            ok: false,
            error: projectsResponse.error,
            organizations: [],
        };
    }
    const orgsFetch = await fetchFn(orgsApiPath, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    });
    if (!orgsFetch.ok) {
        return {
            ok: false,
            error: orgsFetch.statusText,
            organizations: [],
        };
    }
    const organizations = await orgsFetch.json();
    const orgsWithProjects = organizations.map(({ name, id }) => {
        const projects = projectsResponse.projects.filter((project) => project.organizationId === id);
        return { organization: { name, id }, projects };
    });
    return {
        ok: true,
        error: null,
        organizations: orgsWithProjects,
    };
}
export async function getProject({ token, scopeId, scopeType, logger, }) {
    if (scopeType !== 'project') {
        throw new Error('Scope type must be project');
    }
    const fetchFn = createTracedFetch(logger);
    const response = await fetchFn(`${projectsApiPath}/${scopeId}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    });
    const project = await response.json();
    return {
        ok: response.ok,
        error: response.ok ? null : project.error?.message,
        project,
    };
}
