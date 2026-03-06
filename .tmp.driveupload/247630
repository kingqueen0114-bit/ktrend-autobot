import { confirm, input, Separator, select } from '@inquirer/prompts';
import { createEmptyStack, listStacks } from '../../actions/blueprints/stacks.js';
import { groupProjectsByOrganization } from '../../actions/sanity/projects.js';
import { styleText } from '../style-text.js';
import { niceId } from './presenters.js';
export async function promptForBlueprintType() {
    return await select({
        message: 'Choose a Blueprint file type:',
        choices: [
            { name: 'TypeScript', value: 'ts' },
            { name: 'JavaScript', value: 'js' },
            { name: 'JSON', value: 'json' },
        ],
        default: 'ts',
    });
}
/**
 * Prompt the user for a Project after selecting an Organization.
 * @param token - The Sanity API token
 * @returns The selected project, with the projectId and displayName
 * @throws {Error} If the user does not have any projects or if the API call fails
 */
export async function promptForProject({ token, knownOrganizationId, knownProjectId, logger, }) {
    const { ok, error, organizations } = await groupProjectsByOrganization({ token, logger });
    if (!ok) {
        throw new Error(error ?? 'Unknown error listing projects');
    }
    if (organizations.length === 0) {
        throw new Error('No Sanity projects found. Use `npx sanity init` to create one.');
    }
    let projects;
    if (organizations.length > 1) {
        const orgChoices = organizations.map(({ organization, projects }) => ({
            name: `"${organization.name}" ${niceId(organization.id)}`,
            value: organization.id,
            disabled: !projects || projects.length === 0 ? '(0 Projects)' : false,
        }));
        const pickedOrgId = await select({
            message: 'Which Organization would you like to use?',
            choices: orgChoices,
            default: knownOrganizationId,
        });
        const pickedOrg = organizations.find((o) => o.organization.id === pickedOrgId);
        projects = pickedOrg?.projects;
    }
    else {
        projects = organizations[0].projects;
    }
    const projectChoices = projects.map(({ displayName, id: projectId }) => ({
        name: `"${displayName}" ${niceId(projectId)}`,
        value: projectId,
    }));
    let pickedProjectId;
    if (projectChoices.length === 1) {
        const onlyProject = projectChoices[0];
        const confirmed = await confirm({
            message: `Found 1 project. Use ${onlyProject.name}?`,
            default: true,
        });
        if (confirmed)
            pickedProjectId = onlyProject.value;
        else
            throw new Error('No project selected');
    }
    else {
        pickedProjectId = await select({
            message: 'Choose a Sanity Project:',
            choices: projectChoices,
            default: knownProjectId,
        });
    }
    const pickedProject = projects.find((p) => p.id === pickedProjectId);
    if (!pickedProject)
        throw new Error('Project not found');
    return { projectId: pickedProject.id, displayName: pickedProject.displayName };
}
/**
 * Prompt the user for a Stack ID after selecting a Project.
 * Can be used to create a new Stack or select an existing one.
 * @param projectId - The ID of the Project
 * @param token - The Sanity API token
 * @returns The selected Stack ID
 * @throws {Error} If the user does not have any Stacks or if the API call fails
 */
export async function promptForStack({ projectId, token, logger, }) {
    const { ok: stacksOk, error: stacksErr, stacks, } = await listStacks({ token, scopeType: 'project', scopeId: projectId }, logger);
    if (!stacksOk) {
        throw new Error(stacksErr || 'Failed to list Stacks');
    }
    const NEW_STACK_ID = 'new';
    let pickedStackId = NEW_STACK_ID;
    if (stacks.length > 0) {
        const stackChoices = [];
        stackChoices.push(new Separator(styleText('underline', 'Create a new Stack:')));
        stackChoices.push({ name: styleText('bold', 'New Stack ✨'), value: NEW_STACK_ID });
        stackChoices.push(new Separator(styleText('underline', 'Use an existing Stack:')));
        stackChoices.push(...stacks.map((s) => ({
            name: `"${s.name}" ${niceId(s.id)} ${styleText('dim', `(${s.resources.length} res)`)}`,
            value: s.id,
        })));
        pickedStackId = await select({
            message: 'Select a deployment Stack:',
            choices: stackChoices,
            default: NEW_STACK_ID,
        });
    }
    if (pickedStackId === NEW_STACK_ID) {
        const stackName = await input({
            message: 'Enter a name for your new Stack:',
            validate: (input) => input.length > 0 || 'Stack name is required',
        });
        const stack = await createEmptyStack({
            token,
            scopeType: 'project',
            scopeId: projectId,
            name: stackName,
            logger,
        });
        return { stackId: stack.id, name: stackName };
    }
    const pickedStack = stacks.find((s) => s.id === pickedStackId);
    if (!pickedStack)
        throw new Error('Stack not found');
    return { stackId: pickedStack.id, name: pickedStack.name };
}
