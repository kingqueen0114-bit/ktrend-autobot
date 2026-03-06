import type { Logger } from '../../utils/logger.js';
import type { InvocationResponse, InvokeContextOptions, InvokeExecutionOptions, InvokePayloadMetadata } from '../../utils/types.js';
export declare function handleInvokeRequest(functionName: string, event: Record<string, unknown>, metadata: InvokePayloadMetadata, context: InvokeContextOptions, logger: ReturnType<typeof Logger>, validateResources: boolean, executionOptions?: Partial<InvokeExecutionOptions>): Promise<InvocationResponse & {
    timings: Record<string, number>;
}>;
