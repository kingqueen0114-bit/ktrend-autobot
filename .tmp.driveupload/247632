import { styleText } from '../style-text.js';
import { niceId } from './presenters.js';
const errorStyle = ['bold', 'red'];
const newOperationStyle = ['bold', 'blue'];
const GUTTER_SYMBOL_WIDTH = 2;
const GUTTER_LEVEL_WIDTH = 6;
function isNewOperation(log, previousLog) {
    return !!previousLog && log.operationId !== previousLog.operationId;
}
function logGutter(log, verbose, previousLog) {
    const operationIsNew = isNewOperation(log, previousLog);
    const level = log.level.toUpperCase();
    const isError = level === 'ERROR' || level === 'FATAL';
    if (verbose) {
        const color = isError ? errorStyle : operationIsNew ? newOperationStyle : 'dim';
        return styleText(color, level.padEnd(GUTTER_LEVEL_WIDTH));
    }
    if (isError)
        return `${styleText(errorStyle, '✗')} `;
    if (operationIsNew)
        return `${styleText(newOperationStyle, '◆')} `;
    return ' '.repeat(GUTTER_SYMBOL_WIDTH);
}
function formatMetadataLines(log) {
    const lines = [];
    const ids = [
        log.operationId ? niceId(log.operationId) : null,
        log.stackId ? niceId(log.stackId) : null,
        log.blueprintId ? niceId(log.blueprintId) : null,
        log.resourceId ? niceId(log.resourceId) : null,
        log.duration ? `${String(log.duration)}ms` : null,
    ].filter(Boolean);
    if (ids.length > 0) {
        lines.push(styleText('dim', ids.join(' ')));
    }
    if (log.metadata) {
        for (const [key, value] of Object.entries(log.metadata)) {
            const formatted = typeof value === 'string' ? value : JSON.stringify(value);
            lines.push(styleText('dim', `${key}: ${formatted}`));
        }
    }
    return lines;
}
function singleLine(message) {
    return message.replace(/\n/g, ' ').replace(/\s{2,}/g, ' ');
}
function formatDate(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}
function formatTime(date) {
    const h = String(date.getHours()).padStart(2, '0');
    const m = String(date.getMinutes()).padStart(2, '0');
    const s = String(date.getSeconds()).padStart(2, '0');
    return `${h}:${m}:${s}`;
}
export function formatLogEntry(log, verbose = false, previousLog) {
    const date = new Date(log.timestamp);
    const time = formatTime(date);
    const day = formatDate(date);
    const gutter = logGutter(log, verbose, previousLog);
    let line = `${day} ${time} ${gutter}${singleLine(log.message)}`;
    if (verbose) {
        const timestampWidth = `${day} ${time} `.length;
        const pad = ' '.repeat(timestampWidth + (verbose ? GUTTER_LEVEL_WIDTH : GUTTER_SYMBOL_WIDTH));
        for (const metaLine of formatMetadataLines(log)) {
            line += `\n${pad}${metaLine}`;
        }
    }
    return line;
}
export function formatLogs(logs, verbose = false) {
    const sorted = [...logs].sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());
    return sorted
        .map((log, i) => formatLogEntry(log, verbose, sorted[i - 1]))
        .join('\n');
}
