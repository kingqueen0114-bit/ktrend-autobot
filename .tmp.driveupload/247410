import type { Blueprint } from '@sanity/blueprints-parser';
import type { Logger } from '../../utils/logger.js';
import type { AuthParams, ScopeType, Stack, StackMutation } from '../../utils/types.js';
export declare const stacksUrl: string;
type ListStacksResponse = {
    ok: true;
    error: null;
    stacks: Stack[];
} | {
    ok: false;
    error: string;
    stacks: unknown;
};
export declare function listStacks(auth: AuthParams, logger: ReturnType<typeof Logger>): Promise<ListStacksResponse>;
interface GetStackResponse {
    ok: boolean;
    error: string | null;
    stack: Stack;
    response?: Response;
}
export declare function getStack({ stackId, auth, logger, }: {
    stackId: string;
    auth: AuthParams;
    logger: ReturnType<typeof Logger>;
}): Promise<GetStackResponse>;
interface CreateStackResponse {
    ok: boolean;
    error: string | null;
    stack: Stack;
}
export declare function createStack({ stackMutation, auth, logger, }: {
    stackMutation: StackMutation;
    auth: AuthParams;
    logger: ReturnType<typeof Logger>;
}): Promise<CreateStackResponse>;
export declare function createEmptyStack({ token, scopeType, scopeId, name, logger, }: {
    token: string;
    scopeType: ScopeType;
    scopeId: string;
    name: string;
    logger: ReturnType<typeof Logger>;
}): Promise<Stack>;
interface UpdateStackResponse {
    ok: boolean;
    error: string | null;
    stack: Stack;
}
export declare function updateStack({ stackId, stackMutation, auth, logger, }: {
    stackId: string;
    stackMutation: StackMutation;
    auth: AuthParams;
    logger: ReturnType<typeof Logger>;
}): Promise<UpdateStackResponse>;
interface PlanResourceSnapshot {
    name: string;
    type: string;
    parameters: Record<string, unknown>;
}
export interface PlanActionDetails {
    name: string;
    type: string;
    parameters?: Record<string, unknown>;
    existingResource?: PlanResourceSnapshot & {
        id: string;
        externalId?: string;
    };
    updatedResource?: PlanResourceSnapshot;
}
export interface DeploymentPlanAction {
    type: 'create' | 'update' | 'destroy' | 'skip' | 'attach' | 'detach';
    resourceType: string;
    details: PlanActionDetails | null;
}
export interface DeploymentPlan {
    plan: DeploymentPlanAction[];
    summary: {
        createCount: number;
        updateCount: number;
        destroyCount: number;
        skipCount: number;
        attachCount: number;
        detachCount: number;
    };
}
type PlanStackResponse = {
    ok: true;
    error: null;
    problems: null;
    deploymentPlan: DeploymentPlan;
} | {
    ok: false;
    error: string;
    problems: {
        message: string;
    }[] | null;
    deploymentPlan: null;
};
export declare function planStack({ stackId, document, auth, logger, }: {
    stackId: string;
    document: Blueprint;
    auth: AuthParams;
    logger: ReturnType<typeof Logger>;
}): Promise<PlanStackResponse>;
interface DestroyStackResponse {
    ok: boolean;
    error: string | null;
    stack: Stack;
}
export declare function resolveStackIdByNameOrId(value: string, auth: AuthParams, logger: ReturnType<typeof Logger>): Promise<string>;
export declare function destroyStack({ stackId, auth, logger, }: {
    stackId: string;
    auth: AuthParams;
    logger: ReturnType<typeof Logger>;
}): Promise<DestroyStackResponse>;
export {};
