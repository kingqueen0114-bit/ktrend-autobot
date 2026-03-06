import { telemetryStoreDebug } from './telemetryStoreDebug.js';
import { createTrace } from './trace.js';
// Sample rate tracking for log events
const logSampleTracker = new Map();
/**
 * Creates a telemetry logger that emits events via the provided emit function
 * @internal
 */ export function createLogger(sessionId, emit) {
    telemetryStoreDebug('Creating logger for session: %s', sessionId);
    const log = (event, data)=>{
        telemetryStoreDebug('Logging event: %s', event.name);
        // Handle sampling if maxSampleRate is specified
        if (event.maxSampleRate && event.maxSampleRate > 0) {
            const now = Date.now();
            const lastEmit = logSampleTracker.get(event.name) || 0;
            if (now - lastEmit < event.maxSampleRate) {
                telemetryStoreDebug('Skipping event %s due to sampling (maxSampleRate: %d)', event.name, event.maxSampleRate);
                return; // Skip due to sampling
            }
            logSampleTracker.set(event.name, now);
            telemetryStoreDebug('Event %s passed sampling check', event.name);
        }
        const logEvent = {
            createdAt: new Date().toISOString(),
            data: data ?? null,
            name: event.name,
            sessionId,
            type: 'log',
            version: event.version
        };
        emit(logEvent);
    };
    const trace = (event, context)=>{
        telemetryStoreDebug('Creating trace: %s', event.name);
        return createTrace(event, context, sessionId, emit, createLogger);
    };
    const updateUserProperties = (properties)=>{
        telemetryStoreDebug('Updating user properties: %o', properties);
        const userPropsEvent = {
            createdAt: new Date().toISOString(),
            properties,
            sessionId,
            type: 'userProperties'
        };
        emit(userPropsEvent);
    };
    return {
        log,
        trace,
        updateUserProperties
    };
}

//# sourceMappingURL=logger.js.map