import { jsx, jsxs, Fragment as Fragment$1 } from "react/jsx-runtime";
import { c } from "react/compiler-runtime";
import { useSelector, useActorRef } from "@xstate/react";
import React, { useRef, useEffect, useLayoutEffect, useState, createContext, useContext, Fragment, useReducer, useCallback, useMemo, memo, forwardRef, Component, startTransition } from "react";
import rawDebug from "debug";
import { isHotkey as isHotkey$1 } from "is-hotkey";
import { getBlockEndPoint, getBlockStartPoint, getBlockKeyFromSelectionPoint, isSelectionCollapsed, isKeyedSegment, isEqualSelectionPoints, getChildKeyFromSelectionPoint, blockOffsetToSpanSelectionPoint, defaultKeyGenerator, parseBlocks, parseBlock, isListBlock, isTypedObject, getSelectionStartPoint as getSelectionStartPoint$1, getSelectionEndPoint as getSelectionEndPoint$1, parseAnnotation, parseMarkDefs, parseSpan, parseInlineObject, isEqualPathSegments } from "./_chunks-es/util.slice-blocks.js";
import { isTextBlock, isSpan, compileSchema } from "@portabletext/schema";
import { defineSchema } from "@portabletext/schema";
import scrollIntoView from "scroll-into-view-if-needed";
import { ResizeObserver } from "@juggle/resize-observer";
import { isEmptyTextBlock, sliceTextBlock, getTextBlockText } from "./_chunks-es/util.slice-text-block.js";
import { setup, fromCallback, assign, and, enqueueActions, emit, assertEvent, raise as raise$1, not, createActor } from "xstate";
import { isSelectionCollapsed as isSelectionCollapsed$1, getFocusChild as getFocusChild$1, getSelectedChildren, getSelectionStartPoint, getSelectionEndPoint, getFocusInlineObject, getFocusTextBlock, getFocusSpan as getFocusSpan$1, getSelectedBlocks, isSelectionExpanded, getSelectionStartBlock, getSelectionEndBlock, isOverlappingSelection, getFocusBlock as getFocusBlock$1, isSelectingEntireBlocks, getSelectedValue, isActiveAnnotation, getActiveAnnotationsMarks, getActiveDecorators, getSelectionStartChild, getSelectionEndChild, getPreviousSpan, getNextSpan, getCaretWordSelection, getFocusBlockObject, getPreviousBlock, getNextBlock, getMarkState, isAtTheEndOfBlock, isAtTheStartOfBlock, getFocusListBlock, isActiveDecorator, getActiveAnnotations, getLastBlock as getLastBlock$1, getSelectedTextBlocks, isActiveListItem, isActiveStyle } from "./_chunks-es/selector.is-selecting-entire-blocks.js";
import { defineBehavior, forward, raise, effect } from "./behaviors/index.js";
import { compileSchemaDefinitionToPortableTextMemberSchemaTypes, createPortableTextMemberSchemaTypes, portableTextMemberSchemaTypesToSchema } from "@portabletext/sanity-bridge";
import { htmlToBlocks } from "@portabletext/block-tools";
import { toHTML } from "@portabletext/to-html";
import { markdownToPortableText, portableTextToMarkdown } from "@portabletext/markdown";
import { Schema } from "@sanity/schema";
import { applyAll, unset, insert, setIfMissing, set, diffMatchPatch as diffMatchPatch$1 } from "@portabletext/patches";
import { createKeyboardShortcut, code, underline, italic, bold, undo, redo } from "@portabletext/keyboard-shortcuts";
import { EditorContext as EditorContext$1 } from "./_chunks-es/use-editor.js";
import { useEditor } from "./_chunks-es/use-editor.js";
import { Subject } from "rxjs";
const rootName = "pte:";
function createDebugger(name) {
  const namespace = `${rootName}${name}`;
  return rawDebug && rawDebug.enabled(namespace) ? rawDebug(namespace) : rawDebug(rootName);
}
const debug$1 = {
  behaviors: createDebugger("behaviors"),
  history: createDebugger("history"),
  mutation: createDebugger("mutation"),
  normalization: createDebugger("normalization"),
  operation: createDebugger("operation"),
  selection: createDebugger("selection"),
  setup: createDebugger("setup"),
  state: createDebugger("state"),
  syncValue: createDebugger("sync:value"),
  syncPatch: createDebugger("sync:patch")
}, isElement = (value, {
  deep = !1
} = {}) => !isObject(value) || typeof value.apply == "function" ? !1 : deep ? Node$1.isNodeList(value.children) : Array.isArray(value.children), Element$2 = {
  isAncestor(value, {
    deep = !1
  } = {}) {
    return isObject(value) && Node$1.isNodeList(value.children, {
      deep
    });
  },
  isElement,
  isElementList(value, {
    deep = !1
  } = {}) {
    return Array.isArray(value) && value.every((val) => Element$2.isElement(val, {
      deep
    }));
  },
  isElementProps(props) {
    return props.children !== void 0;
  },
  isElementType: (value, elementVal, elementKey = "type") => isElement(value) && value[elementKey] === elementVal,
  matches(element, props) {
    for (const key in props)
      if (key !== "children" && element[key] !== props[key])
        return !1;
    return !0;
  }
}, Span = {
  isSpan(value) {
    return Array.isArray(value) && value.length === 2 && value.every(Path.isPath);
  }
}, Operation = {
  isNodeOperation(value) {
    return Operation.isOperation(value) && value.type.endsWith("_node");
  },
  isOperation(value) {
    if (!isObject(value))
      return !1;
    switch (value.type) {
      case "insert_node":
        return Path.isPath(value.path) && Node$1.isNode(value.node);
      case "insert_text":
        return typeof value.offset == "number" && typeof value.text == "string" && Path.isPath(value.path);
      case "merge_node":
        return typeof value.position == "number" && Path.isPath(value.path) && isObject(value.properties);
      case "move_node":
        return Path.isPath(value.path) && Path.isPath(value.newPath);
      case "remove_node":
        return Path.isPath(value.path) && Node$1.isNode(value.node);
      case "remove_text":
        return typeof value.offset == "number" && typeof value.text == "string" && Path.isPath(value.path);
      case "set_node":
        return Path.isPath(value.path) && isObject(value.properties) && isObject(value.newProperties);
      case "set_selection":
        return value.properties === null && Range.isRange(value.newProperties) || value.newProperties === null && Range.isRange(value.properties) || isObject(value.properties) && isObject(value.newProperties);
      case "split_node":
        return Path.isPath(value.path) && typeof value.position == "number" && isObject(value.properties);
      default:
        return !1;
    }
  },
  isOperationList(value) {
    return Array.isArray(value) && value.every((val) => Operation.isOperation(val));
  },
  isSelectionOperation(value) {
    return Operation.isOperation(value) && value.type.endsWith("_selection");
  },
  isTextOperation(value) {
    return Operation.isOperation(value) && value.type.endsWith("_text");
  },
  inverse(op) {
    switch (op.type) {
      case "insert_node":
        return {
          ...op,
          type: "remove_node"
        };
      case "insert_text":
        return {
          ...op,
          type: "remove_text"
        };
      case "merge_node":
        return {
          ...op,
          type: "split_node",
          path: Path.previous(op.path)
        };
      case "move_node": {
        const {
          newPath,
          path: path2
        } = op;
        if (Path.equals(newPath, path2))
          return op;
        if (Path.isSibling(path2, newPath))
          return {
            ...op,
            path: newPath,
            newPath: path2
          };
        const inversePath = Path.transform(path2, op), inverseNewPath = Path.transform(Path.next(path2), op);
        return {
          ...op,
          path: inversePath,
          newPath: inverseNewPath
        };
      }
      case "remove_node":
        return {
          ...op,
          type: "insert_node"
        };
      case "remove_text":
        return {
          ...op,
          type: "insert_text"
        };
      case "set_node": {
        const {
          properties,
          newProperties
        } = op;
        return {
          ...op,
          properties: newProperties,
          newProperties: properties
        };
      }
      case "set_selection": {
        const {
          properties,
          newProperties
        } = op;
        return properties == null ? {
          ...op,
          properties: newProperties,
          newProperties: null
        } : newProperties == null ? {
          ...op,
          properties: null,
          newProperties: properties
        } : {
          ...op,
          properties: newProperties,
          newProperties: properties
        };
      }
      case "split_node":
        return {
          ...op,
          type: "merge_node",
          path: Path.next(op.path)
        };
    }
  }
}, PathRef = {
  transform(ref, op) {
    const {
      current,
      affinity
    } = ref;
    if (current == null)
      return;
    const path2 = Path.transform(current, op, {
      affinity
    });
    ref.current = path2, path2 == null && ref.unref();
  }
}, Path = {
  ancestors(path2, options = {}) {
    const {
      reverse = !1
    } = options;
    let paths = Path.levels(path2, options);
    return reverse ? paths = paths.slice(1) : paths = paths.slice(0, -1), paths;
  },
  common(path2, another) {
    const common = [];
    for (let i = 0; i < path2.length && i < another.length; i++) {
      const av = path2[i], bv = another[i];
      if (av !== bv)
        break;
      common.push(av);
    }
    return common;
  },
  compare(path2, another) {
    const min = Math.min(path2.length, another.length);
    for (let i = 0; i < min; i++) {
      if (path2[i] < another[i])
        return -1;
      if (path2[i] > another[i])
        return 1;
    }
    return 0;
  },
  endsAfter(path2, another) {
    const i = path2.length - 1, as = path2.slice(0, i), bs = another.slice(0, i), av = path2[i], bv = another[i];
    return Path.equals(as, bs) && av > bv;
  },
  endsAt(path2, another) {
    const i = path2.length, as = path2.slice(0, i), bs = another.slice(0, i);
    return Path.equals(as, bs);
  },
  endsBefore(path2, another) {
    const i = path2.length - 1, as = path2.slice(0, i), bs = another.slice(0, i), av = path2[i], bv = another[i];
    return Path.equals(as, bs) && av < bv;
  },
  equals(path2, another) {
    return path2.length === another.length && path2.every((n2, i) => n2 === another[i]);
  },
  hasPrevious(path2) {
    return path2[path2.length - 1] > 0;
  },
  isAfter(path2, another) {
    return Path.compare(path2, another) === 1;
  },
  isAncestor(path2, another) {
    return path2.length < another.length && Path.compare(path2, another) === 0;
  },
  isBefore(path2, another) {
    return Path.compare(path2, another) === -1;
  },
  isChild(path2, another) {
    return path2.length === another.length + 1 && Path.compare(path2, another) === 0;
  },
  isCommon(path2, another) {
    return path2.length <= another.length && Path.compare(path2, another) === 0;
  },
  isDescendant(path2, another) {
    return path2.length > another.length && Path.compare(path2, another) === 0;
  },
  isParent(path2, another) {
    return path2.length + 1 === another.length && Path.compare(path2, another) === 0;
  },
  isPath(value) {
    return Array.isArray(value) && (value.length === 0 || typeof value[0] == "number");
  },
  isSibling(path2, another) {
    if (path2.length !== another.length)
      return !1;
    const as = path2.slice(0, -1), bs = another.slice(0, -1), al = path2[path2.length - 1], bl = another[another.length - 1];
    return al !== bl && Path.equals(as, bs);
  },
  levels(path2, options = {}) {
    const {
      reverse = !1
    } = options, list = [];
    for (let i = 0; i <= path2.length; i++)
      list.push(path2.slice(0, i));
    return reverse && list.reverse(), list;
  },
  next(path2) {
    if (path2.length === 0)
      throw new Error(`Cannot get the next path of a root path [${path2}], because it has no next index.`);
    const last2 = path2[path2.length - 1];
    return path2.slice(0, -1).concat(last2 + 1);
  },
  operationCanTransformPath(operation) {
    switch (operation.type) {
      case "insert_node":
      case "remove_node":
      case "merge_node":
      case "split_node":
      case "move_node":
        return !0;
      default:
        return !1;
    }
  },
  parent(path2) {
    if (path2.length === 0)
      throw new Error(`Cannot get the parent path of the root path [${path2}].`);
    return path2.slice(0, -1);
  },
  previous(path2) {
    if (path2.length === 0)
      throw new Error(`Cannot get the previous path of a root path [${path2}], because it has no previous index.`);
    const last2 = path2[path2.length - 1];
    if (last2 <= 0)
      throw new Error(`Cannot get the previous path of a first child path [${path2}] because it would result in a negative index.`);
    return path2.slice(0, -1).concat(last2 - 1);
  },
  relative(path2, ancestor) {
    if (!Path.isAncestor(ancestor, path2) && !Path.equals(path2, ancestor))
      throw new Error(`Cannot get the relative path of [${path2}] inside ancestor [${ancestor}], because it is not above or equal to the path.`);
    return path2.slice(ancestor.length);
  },
  transform(path2, operation, options = {}) {
    if (!path2)
      return null;
    const p = [...path2], {
      affinity = "forward"
    } = options;
    if (path2.length === 0)
      return p;
    switch (operation.type) {
      case "insert_node": {
        const {
          path: op
        } = operation;
        (Path.equals(op, p) || Path.endsBefore(op, p) || Path.isAncestor(op, p)) && (p[op.length - 1] = p[op.length - 1] + 1);
        break;
      }
      case "remove_node": {
        const {
          path: op
        } = operation;
        if (Path.equals(op, p) || Path.isAncestor(op, p))
          return null;
        Path.endsBefore(op, p) && (p[op.length - 1] = p[op.length - 1] - 1);
        break;
      }
      case "merge_node": {
        const {
          path: op,
          position
        } = operation;
        Path.equals(op, p) || Path.endsBefore(op, p) ? p[op.length - 1] = p[op.length - 1] - 1 : Path.isAncestor(op, p) && (p[op.length - 1] = p[op.length - 1] - 1, p[op.length] = p[op.length] + position);
        break;
      }
      case "split_node": {
        const {
          path: op,
          position
        } = operation;
        if (Path.equals(op, p)) {
          if (affinity === "forward")
            p[p.length - 1] = p[p.length - 1] + 1;
          else if (affinity !== "backward")
            return null;
        } else Path.endsBefore(op, p) ? p[op.length - 1] = p[op.length - 1] + 1 : Path.isAncestor(op, p) && path2[op.length] >= position && (p[op.length - 1] = p[op.length - 1] + 1, p[op.length] = p[op.length] - position);
        break;
      }
      case "move_node": {
        const {
          path: op,
          newPath: onp
        } = operation;
        if (Path.equals(op, onp))
          return p;
        if (Path.isAncestor(op, p) || Path.equals(op, p)) {
          const copy = onp.slice();
          return Path.endsBefore(op, onp) && op.length < onp.length && (copy[op.length - 1] = copy[op.length - 1] - 1), copy.concat(p.slice(op.length));
        } else Path.isSibling(op, onp) && (Path.isAncestor(onp, p) || Path.equals(onp, p)) ? Path.endsBefore(op, p) ? p[op.length - 1] = p[op.length - 1] - 1 : p[op.length - 1] = p[op.length - 1] + 1 : Path.endsBefore(onp, p) || Path.equals(onp, p) || Path.isAncestor(onp, p) ? (Path.endsBefore(op, p) && (p[op.length - 1] = p[op.length - 1] - 1), p[onp.length - 1] = p[onp.length - 1] + 1) : Path.endsBefore(op, p) && (Path.equals(onp, p) && (p[onp.length - 1] = p[onp.length - 1] + 1), p[op.length - 1] = p[op.length - 1] - 1);
        break;
      }
    }
    return p;
  }
}, PointRef = {
  transform(ref, op) {
    const {
      current,
      affinity
    } = ref;
    if (current == null)
      return;
    const point2 = Point.transform(current, op, {
      affinity
    });
    ref.current = point2, point2 == null && ref.unref();
  }
}, Point = {
  compare(point2, another) {
    const result = Path.compare(point2.path, another.path);
    return result === 0 ? point2.offset < another.offset ? -1 : point2.offset > another.offset ? 1 : 0 : result;
  },
  isAfter(point2, another) {
    return Point.compare(point2, another) === 1;
  },
  isBefore(point2, another) {
    return Point.compare(point2, another) === -1;
  },
  equals(point2, another) {
    return point2.offset === another.offset && Path.equals(point2.path, another.path);
  },
  isPoint(value) {
    return isObject(value) && typeof value.offset == "number" && Path.isPath(value.path);
  },
  transform(point2, op, options = {}) {
    if (point2 === null)
      return null;
    const {
      affinity = "forward"
    } = options;
    let {
      path: path2,
      offset
    } = point2;
    switch (op.type) {
      case "insert_node":
      case "move_node": {
        path2 = Path.transform(path2, op, options);
        break;
      }
      case "insert_text": {
        Path.equals(op.path, path2) && (op.offset < offset || op.offset === offset && affinity === "forward") && (offset += op.text.length);
        break;
      }
      case "merge_node": {
        Path.equals(op.path, path2) && (offset += op.position), path2 = Path.transform(path2, op, options);
        break;
      }
      case "remove_text": {
        Path.equals(op.path, path2) && op.offset <= offset && (offset -= Math.min(offset - op.offset, op.text.length));
        break;
      }
      case "remove_node": {
        if (Path.equals(op.path, path2) || Path.isAncestor(op.path, path2))
          return null;
        path2 = Path.transform(path2, op, options);
        break;
      }
      case "split_node": {
        if (Path.equals(op.path, path2)) {
          if (op.position === offset && affinity == null)
            return null;
          (op.position < offset || op.position === offset && affinity === "forward") && (offset -= op.position, path2 = Path.transform(path2, op, {
            ...options,
            affinity: "forward"
          }));
        } else
          path2 = Path.transform(path2, op, options);
        break;
      }
      default:
        return point2;
    }
    return {
      path: path2,
      offset
    };
  }
}, RangeRef = {
  transform(ref, op) {
    const {
      current,
      affinity
    } = ref;
    if (current == null)
      return;
    const path2 = Range.transform(current, op, {
      affinity
    });
    ref.current = path2, path2 == null && ref.unref();
  }
}, Range = {
  edges(range2, options = {}) {
    const {
      reverse = !1
    } = options, {
      anchor,
      focus
    } = range2;
    return Range.isBackward(range2) === reverse ? [anchor, focus] : [focus, anchor];
  },
  end(range2) {
    const [, end2] = Range.edges(range2);
    return end2;
  },
  equals(range2, another) {
    return Point.equals(range2.anchor, another.anchor) && Point.equals(range2.focus, another.focus);
  },
  surrounds(range2, target) {
    const intersectionRange = Range.intersection(range2, target);
    return intersectionRange ? Range.equals(intersectionRange, target) : !1;
  },
  includes(range2, target) {
    if (Range.isRange(target)) {
      if (Range.includes(range2, target.anchor) || Range.includes(range2, target.focus))
        return !0;
      const [rs, re] = Range.edges(range2), [ts, te] = Range.edges(target);
      return Point.isBefore(rs, ts) && Point.isAfter(re, te);
    }
    const [start2, end2] = Range.edges(range2);
    let isAfterStart = !1, isBeforeEnd = !1;
    return Point.isPoint(target) ? (isAfterStart = Point.compare(target, start2) >= 0, isBeforeEnd = Point.compare(target, end2) <= 0) : (isAfterStart = Path.compare(target, start2.path) >= 0, isBeforeEnd = Path.compare(target, end2.path) <= 0), isAfterStart && isBeforeEnd;
  },
  intersection(range2, another) {
    const {
      anchor: _anchor,
      focus: _focus,
      ...rest
    } = range2, [s1, e1] = Range.edges(range2), [s2, e2] = Range.edges(another), start2 = Point.isBefore(s1, s2) ? s2 : s1, end2 = Point.isBefore(e1, e2) ? e1 : e2;
    return Point.isBefore(end2, start2) ? null : {
      anchor: start2,
      focus: end2,
      ...rest
    };
  },
  isBackward(range2) {
    const {
      anchor,
      focus
    } = range2;
    return Point.isAfter(anchor, focus);
  },
  isCollapsed(range2) {
    const {
      anchor,
      focus
    } = range2;
    return Point.equals(anchor, focus);
  },
  isExpanded(range2) {
    return !Range.isCollapsed(range2);
  },
  isForward(range2) {
    return !Range.isBackward(range2);
  },
  isRange(value) {
    return isObject(value) && Point.isPoint(value.anchor) && Point.isPoint(value.focus);
  },
  *points(range2) {
    yield [range2.anchor, "anchor"], yield [range2.focus, "focus"];
  },
  start(range2) {
    const [start2] = Range.edges(range2);
    return start2;
  },
  transform(range2, op, options = {}) {
    if (range2 === null)
      return null;
    const {
      affinity = "inward"
    } = options;
    let affinityAnchor, affinityFocus;
    if (affinity === "inward") {
      const isCollapsed = Range.isCollapsed(range2);
      Range.isForward(range2) ? (affinityAnchor = "forward", affinityFocus = isCollapsed ? affinityAnchor : "backward") : (affinityAnchor = "backward", affinityFocus = isCollapsed ? affinityAnchor : "forward");
    } else affinity === "outward" ? Range.isForward(range2) ? (affinityAnchor = "backward", affinityFocus = "forward") : (affinityAnchor = "forward", affinityFocus = "backward") : (affinityAnchor = affinity, affinityFocus = affinity);
    const anchor = Point.transform(range2.anchor, op, {
      affinity: affinityAnchor
    }), focus = Point.transform(range2.focus, op, {
      affinity: affinityFocus
    });
    return !anchor || !focus ? null : {
      anchor,
      focus
    };
  }
};
let _scrubber;
const Scrubber = {
  setScrubber(scrubber) {
    _scrubber = scrubber;
  },
  stringify(value) {
    return JSON.stringify(value, _scrubber);
  }
}, isObject = (value) => typeof value == "object" && value !== null, isDeepEqual$1 = (node2, another) => {
  for (const key in node2) {
    const a = node2[key], b = another[key];
    if (Array.isArray(a) && Array.isArray(b)) {
      if (a.length !== b.length)
        return !1;
      for (let i = 0; i < a.length; i++)
        if (a[i] !== b[i])
          return !1;
    } else if (isObject(a) && isObject(b)) {
      if (!isDeepEqual$1(a, b))
        return !1;
    } else if (a !== b)
      return !1;
  }
  for (const key in another)
    if (node2[key] === void 0 && another[key] !== void 0)
      return !1;
  return !0;
}, Text$1 = {
  equals(text, another, options = {}) {
    const {
      loose = !1
    } = options;
    function omitText(obj) {
      const {
        text: _text,
        ...rest
      } = obj;
      return rest;
    }
    return isDeepEqual$1(loose ? omitText(text) : text, loose ? omitText(another) : another);
  },
  isText(value) {
    return isObject(value) && typeof value.text == "string";
  },
  isTextList(value) {
    return Array.isArray(value) && value.every((val) => Text$1.isText(val));
  },
  isTextProps(props) {
    return props.text !== void 0;
  },
  matches(text, props) {
    for (const key in props)
      if (key !== "text" && (!text.hasOwnProperty(key) || text[key] !== props[key]))
        return !1;
    return !0;
  },
  decorations(node2, decorations) {
    let leaves = [{
      leaf: {
        ...node2
      }
    }];
    for (const dec of decorations) {
      const {
        anchor: _anchor,
        focus: _focus,
        merge: mergeDecoration,
        ...rest
      } = dec, [start2, end2] = Range.edges(dec), next2 = [];
      let leafEnd = 0;
      const decorationStart = start2.offset, decorationEnd = end2.offset, merge = mergeDecoration ?? Object.assign;
      for (const {
        leaf: leaf2
      } of leaves) {
        const {
          length
        } = leaf2.text, leafStart = leafEnd;
        if (leafEnd += length, decorationStart <= leafStart && leafEnd <= decorationEnd) {
          merge(leaf2, rest), next2.push({
            leaf: leaf2
          });
          continue;
        }
        if (decorationStart !== decorationEnd && (decorationStart === leafEnd || decorationEnd === leafStart) || decorationStart > leafEnd || decorationEnd < leafStart || decorationEnd === leafStart && leafStart !== 0) {
          next2.push({
            leaf: leaf2
          });
          continue;
        }
        let middle = leaf2, before2, after2;
        if (decorationEnd < leafEnd) {
          const off = decorationEnd - leafStart;
          after2 = {
            leaf: {
              ...middle,
              text: middle.text.slice(off)
            }
          }, middle = {
            ...middle,
            text: middle.text.slice(0, off)
          };
        }
        if (decorationStart > leafStart) {
          const off = decorationStart - leafStart;
          before2 = {
            leaf: {
              ...middle,
              text: middle.text.slice(0, off)
            }
          }, middle = {
            ...middle,
            text: middle.text.slice(off)
          };
        }
        merge(middle, rest), before2 && next2.push(before2), next2.push({
          leaf: middle
        }), after2 && next2.push(after2);
      }
      leaves = next2;
    }
    if (leaves.length > 1) {
      let currentOffset = 0;
      for (const [index, item] of leaves.entries()) {
        const start2 = currentOffset, end2 = start2 + item.leaf.text.length, position = {
          start: start2,
          end: end2
        };
        index === 0 && (position.isFirst = !0), index === leaves.length - 1 && (position.isLast = !0), item.position = position, currentOffset = end2;
      }
    }
    return leaves;
  }
}, GeneralTransforms = {
  transform(editor, op) {
    let transformSelection = !1;
    switch (op.type) {
      case "insert_node": {
        const {
          path: path2,
          node: node2
        } = op;
        modifyChildren(editor, Path.parent(path2), (children) => {
          const index = path2[path2.length - 1];
          if (index > children.length)
            throw new Error(`Cannot apply an "insert_node" operation at path [${path2}] because the destination is past the end of the node.`);
          return insertChildren$1(children, index, node2);
        }), transformSelection = !0;
        break;
      }
      case "insert_text": {
        const {
          path: path2,
          offset,
          text
        } = op;
        if (text.length === 0)
          break;
        modifyLeaf(editor, path2, (node2) => {
          const before2 = node2.text.slice(0, offset), after2 = node2.text.slice(offset);
          return {
            ...node2,
            text: before2 + text + after2
          };
        }), transformSelection = !0;
        break;
      }
      case "merge_node": {
        const {
          path: path2
        } = op, index = path2[path2.length - 1], prevPath = Path.previous(path2), prevIndex = prevPath[prevPath.length - 1];
        modifyChildren(editor, Path.parent(path2), (children) => {
          const node2 = children[index], prev = children[prevIndex];
          let newNode;
          if (Text$1.isText(node2) && Text$1.isText(prev))
            newNode = {
              ...prev,
              text: prev.text + node2.text
            };
          else if (!Text$1.isText(node2) && !Text$1.isText(prev))
            newNode = {
              ...prev,
              children: prev.children.concat(node2.children)
            };
          else
            throw new Error(`Cannot apply a "merge_node" operation at path [${path2}] to nodes of different interfaces: ${Scrubber.stringify(node2)} ${Scrubber.stringify(prev)}`);
          return replaceChildren(children, prevIndex, 2, newNode);
        }), transformSelection = !0;
        break;
      }
      case "move_node": {
        const {
          path: path2,
          newPath
        } = op, index = path2[path2.length - 1];
        if (Path.isAncestor(path2, newPath))
          throw new Error(`Cannot move a path [${path2}] to new path [${newPath}] because the destination is inside itself.`);
        const node2 = Node$1.get(editor, path2);
        modifyChildren(editor, Path.parent(path2), (children) => removeChildren$1(children, index, 1));
        const truePath = Path.transform(path2, op), newIndex = truePath[truePath.length - 1];
        modifyChildren(editor, Path.parent(truePath), (children) => insertChildren$1(children, newIndex, node2)), transformSelection = !0;
        break;
      }
      case "remove_node": {
        const {
          path: path2
        } = op, index = path2[path2.length - 1];
        if (modifyChildren(editor, Path.parent(path2), (children) => removeChildren$1(children, index, 1)), editor.selection) {
          let selection = {
            ...editor.selection
          };
          for (const [point2, key] of Range.points(selection)) {
            const result = Point.transform(point2, op);
            if (selection != null && result != null)
              selection[key] = result;
            else {
              let prev, next2;
              for (const [n2, p] of Node$1.texts(editor))
                if (Path.compare(p, path2) === -1)
                  prev = [n2, p];
                else {
                  next2 = [n2, p];
                  break;
                }
              let preferNext = !1;
              prev && next2 && (Path.isSibling(prev[1], path2) ? preferNext = !1 : Path.equals(next2[1], path2) ? preferNext = !0 : preferNext = Path.common(prev[1], path2).length < Path.common(next2[1], path2).length), prev && !preferNext ? selection[key] = {
                path: prev[1],
                offset: prev[0].text.length
              } : next2 ? selection[key] = {
                path: next2[1],
                offset: 0
              } : selection = null;
            }
          }
          (!selection || !Range.equals(selection, editor.selection)) && (editor.selection = selection);
        }
        break;
      }
      case "remove_text": {
        const {
          path: path2,
          offset,
          text
        } = op;
        if (text.length === 0)
          break;
        modifyLeaf(editor, path2, (node2) => {
          const before2 = node2.text.slice(0, offset), after2 = node2.text.slice(offset + text.length);
          return {
            ...node2,
            text: before2 + after2
          };
        }), transformSelection = !0;
        break;
      }
      case "set_node": {
        const {
          path: path2,
          properties,
          newProperties
        } = op;
        if (path2.length === 0)
          throw new Error("Cannot set properties on the root node!");
        modifyDescendant(editor, path2, (node2) => {
          const newNode = {
            ...node2
          };
          for (const key in newProperties) {
            if (key === "children" || key === "text")
              throw new Error(`Cannot set the "${key}" property of nodes!`);
            const value = newProperties[key];
            value == null ? delete newNode[key] : newNode[key] = value;
          }
          for (const key in properties)
            newProperties.hasOwnProperty(key) || delete newNode[key];
          return newNode;
        });
        break;
      }
      case "set_selection": {
        const {
          newProperties
        } = op;
        if (newProperties == null) {
          editor.selection = null;
          break;
        }
        if (editor.selection == null) {
          if (!Range.isRange(newProperties))
            throw new Error(`Cannot apply an incomplete "set_selection" operation properties ${Scrubber.stringify(newProperties)} when there is no current selection.`);
          editor.selection = {
            ...newProperties
          };
          break;
        }
        const selection = {
          ...editor.selection
        };
        for (const key in newProperties) {
          const value = newProperties[key];
          if (value == null) {
            if (key === "anchor" || key === "focus")
              throw new Error(`Cannot remove the "${key}" selection property`);
            delete selection[key];
          } else
            selection[key] = value;
        }
        editor.selection = selection;
        break;
      }
      case "split_node": {
        const {
          path: path2,
          position,
          properties
        } = op, index = path2[path2.length - 1];
        if (path2.length === 0)
          throw new Error(`Cannot apply a "split_node" operation at path [${path2}] because the root node cannot be split.`);
        modifyChildren(editor, Path.parent(path2), (children) => {
          const node2 = children[index];
          let newNode, nextNode;
          if (Text$1.isText(node2)) {
            const before2 = node2.text.slice(0, position), after2 = node2.text.slice(position);
            newNode = {
              ...node2,
              text: before2
            }, nextNode = {
              ...properties,
              text: after2
            };
          } else {
            const before2 = node2.children.slice(0, position), after2 = node2.children.slice(position);
            newNode = {
              ...node2,
              children: before2
            }, nextNode = {
              ...properties,
              children: after2
            };
          }
          return replaceChildren(children, index, 1, newNode, nextNode);
        }), transformSelection = !0;
        break;
      }
    }
    if (transformSelection && editor.selection) {
      const selection = {
        ...editor.selection
      };
      for (const [point2, key] of Range.points(selection))
        selection[key] = Point.transform(point2, op);
      Range.equals(selection, editor.selection) || (editor.selection = selection);
    }
  }
}, NodeTransforms = {
  insertNodes(editor, nodes2, options) {
    editor.insertNodes(nodes2, options);
  },
  liftNodes(editor, options) {
    editor.liftNodes(options);
  },
  mergeNodes(editor, options) {
    editor.mergeNodes(options);
  },
  moveNodes(editor, options) {
    editor.moveNodes(options);
  },
  removeNodes(editor, options) {
    editor.removeNodes(options);
  },
  setNodes(editor, props, options) {
    editor.setNodes(props, options);
  },
  splitNodes(editor, options) {
    editor.splitNodes(options);
  },
  unsetNodes(editor, props, options) {
    editor.unsetNodes(props, options);
  },
  unwrapNodes(editor, options) {
    editor.unwrapNodes(options);
  },
  wrapNodes(editor, element, options) {
    editor.wrapNodes(element, options);
  }
}, SelectionTransforms = {
  collapse(editor, options) {
    editor.collapse(options);
  },
  deselect(editor) {
    editor.deselect();
  },
  move(editor, options) {
    editor.move(options);
  },
  select(editor, target) {
    editor.select(target);
  },
  setPoint(editor, props, options) {
    editor.setPoint(props, options);
  },
  setSelection(editor, props) {
    editor.setSelection(props);
  }
}, getDefaultInsertLocation = (editor) => editor.selection ? editor.selection : editor.children.length > 0 ? Editor.end(editor, []) : [0], matchPath = (editor, path2) => {
  const [node2] = Editor.node(editor, path2);
  return (n2) => n2 === node2;
}, getCharacterDistance = (str, isRTL = !1) => {
  const isLTR = !isRTL, codepoints = isRTL ? codepointsIteratorRTL(str) : str;
  let left = CodepointType.None, right = CodepointType.None, distance = 0, gb11 = null, gb12Or13 = null;
  for (const char of codepoints) {
    const code2 = char.codePointAt(0);
    if (!code2)
      break;
    const type = getCodepointType(char, code2);
    if ([left, right] = isLTR ? [right, type] : [type, left], intersects(left, CodepointType.ZWJ) && intersects(right, CodepointType.ExtPict) && (isLTR ? gb11 = endsWithEmojiZWJ(str.substring(0, distance)) : gb11 = endsWithEmojiZWJ(str.substring(0, str.length - distance)), !gb11) || intersects(left, CodepointType.RI) && intersects(right, CodepointType.RI) && (gb12Or13 !== null ? gb12Or13 = !gb12Or13 : isLTR ? gb12Or13 = !0 : gb12Or13 = endsWithOddNumberOfRIs(str.substring(0, str.length - distance)), !gb12Or13) || left !== CodepointType.None && right !== CodepointType.None && isBoundaryPair(left, right))
      break;
    distance += char.length;
  }
  return distance || 1;
}, SPACE = /\s/, PUNCTUATION = /[\u002B\u0021-\u0023\u0025-\u002A\u002C-\u002F\u003A\u003B\u003F\u0040\u005B-\u005D\u005F\u007B\u007D\u00A1\u00A7\u00AB\u00B6\u00B7\u00BB\u00BF\u037E\u0387\u055A-\u055F\u0589\u058A\u05BE\u05C0\u05C3\u05C6\u05F3\u05F4\u0609\u060A\u060C\u060D\u061B\u061E\u061F\u066A-\u066D\u06D4\u0700-\u070D\u07F7-\u07F9\u0830-\u083E\u085E\u0964\u0965\u0970\u0AF0\u0DF4\u0E4F\u0E5A\u0E5B\u0F04-\u0F12\u0F14\u0F3A-\u0F3D\u0F85\u0FD0-\u0FD4\u0FD9\u0FDA\u104A-\u104F\u10FB\u1360-\u1368\u1400\u166D\u166E\u169B\u169C\u16EB-\u16ED\u1735\u1736\u17D4-\u17D6\u17D8-\u17DA\u1800-\u180A\u1944\u1945\u1A1E\u1A1F\u1AA0-\u1AA6\u1AA8-\u1AAD\u1B5A-\u1B60\u1BFC-\u1BFF\u1C3B-\u1C3F\u1C7E\u1C7F\u1CC0-\u1CC7\u1CD3\u2010-\u2027\u2030-\u2043\u2045-\u2051\u2053-\u205E\u207D\u207E\u208D\u208E\u2329\u232A\u2768-\u2775\u27C5\u27C6\u27E6-\u27EF\u2983-\u2998\u29D8-\u29DB\u29FC\u29FD\u2CF9-\u2CFC\u2CFE\u2CFF\u2D70\u2E00-\u2E2E\u2E30-\u2E3B\u3001-\u3003\u3008-\u3011\u3014-\u301F\u3030\u303D\u30A0\u30FB\uA4FE\uA4FF\uA60D-\uA60F\uA673\uA67E\uA6F2-\uA6F7\uA874-\uA877\uA8CE\uA8CF\uA8F8-\uA8FA\uA92E\uA92F\uA95F\uA9C1-\uA9CD\uA9DE\uA9DF\uAA5C-\uAA5F\uAADE\uAADF\uAAF0\uAAF1\uABEB\uFD3E\uFD3F\uFE10-\uFE19\uFE30-\uFE52\uFE54-\uFE61\uFE63\uFE68\uFE6A\uFE6B\uFF01-\uFF03\uFF05-\uFF0A\uFF0C-\uFF0F\uFF1A\uFF1B\uFF1F\uFF20\uFF3B-\uFF3D\uFF3F\uFF5B\uFF5D\uFF5F-\uFF65]/, CHAMELEON = /['\u2018\u2019]/, getWordDistance = (text, isRTL = !1) => {
  let dist = 0, started = !1;
  for (; text.length > 0; ) {
    const charDist = getCharacterDistance(text, isRTL), [char, remaining] = splitByCharacterDistance(text, charDist, isRTL);
    if (isWordCharacter(char, remaining, isRTL))
      started = !0, dist += charDist;
    else if (!started)
      dist += charDist;
    else
      break;
    text = remaining;
  }
  return dist;
}, splitByCharacterDistance = (str, dist, isRTL) => {
  if (isRTL) {
    const at = str.length - dist;
    return [str.slice(at, str.length), str.slice(0, at)];
  }
  return [str.slice(0, dist), str.slice(dist)];
}, isWordCharacter = (char, remaining, isRTL = !1) => {
  if (SPACE.test(char))
    return !1;
  if (CHAMELEON.test(char)) {
    const charDist = getCharacterDistance(remaining, isRTL), [nextChar, nextRemaining] = splitByCharacterDistance(remaining, charDist, isRTL);
    if (isWordCharacter(nextChar, nextRemaining, isRTL))
      return !0;
  }
  return !PUNCTUATION.test(char);
}, codepointsIteratorRTL = function* (str) {
  const end2 = str.length - 1;
  for (let i = 0; i < str.length; i++) {
    const char1 = str.charAt(end2 - i);
    if (isLowSurrogate$1(char1.charCodeAt(0))) {
      const char2 = str.charAt(end2 - i - 1);
      if (isHighSurrogate$1(char2.charCodeAt(0))) {
        yield char2 + char1, i++;
        continue;
      }
    }
    yield char1;
  }
}, isHighSurrogate$1 = (charCode) => charCode >= 55296 && charCode <= 56319, isLowSurrogate$1 = (charCode) => charCode >= 56320 && charCode <= 57343, CodepointType = {
  None: 0,
  Extend: 1,
  ZWJ: 2,
  RI: 4,
  Prepend: 8,
  SpacingMark: 16,
  L: 32,
  V: 64,
  T: 128,
  LV: 256,
  LVT: 512,
  ExtPict: 1024,
  Any: 2048
}, reExtend = /^[\p{Gr_Ext}\p{EMod}]$/u, rePrepend = /^[\u0600-\u0605\u06DD\u070F\u0890-\u0891\u08E2\u0D4E\u{110BD}\u{110CD}\u{111C2}-\u{111C3}\u{1193F}\u{11941}\u{11A3A}\u{11A84}-\u{11A89}\u{11D46}]$/u, reSpacingMark = /^[\u0903\u093B\u093E-\u0940\u0949-\u094C\u094E-\u094F\u0982-\u0983\u09BF-\u09C0\u09C7-\u09C8\u09CB-\u09CC\u0A03\u0A3E-\u0A40\u0A83\u0ABE-\u0AC0\u0AC9\u0ACB-\u0ACC\u0B02-\u0B03\u0B40\u0B47-\u0B48\u0B4B-\u0B4C\u0BBF\u0BC1-\u0BC2\u0BC6-\u0BC8\u0BCA-\u0BCC\u0C01-\u0C03\u0C41-\u0C44\u0C82-\u0C83\u0CBE\u0CC0-\u0CC1\u0CC3-\u0CC4\u0CC7-\u0CC8\u0CCA-\u0CCB\u0D02-\u0D03\u0D3F-\u0D40\u0D46-\u0D48\u0D4A-\u0D4C\u0D82-\u0D83\u0DD0-\u0DD1\u0DD8-\u0DDE\u0DF2-\u0DF3\u0E33\u0EB3\u0F3E-\u0F3F\u0F7F\u1031\u103B-\u103C\u1056-\u1057\u1084\u1715\u1734\u17B6\u17BE-\u17C5\u17C7-\u17C8\u1923-\u1926\u1929-\u192B\u1930-\u1931\u1933-\u1938\u1A19-\u1A1A\u1A55\u1A57\u1A6D-\u1A72\u1B04\u1B3B\u1B3D-\u1B41\u1B43-\u1B44\u1B82\u1BA1\u1BA6-\u1BA7\u1BAA\u1BE7\u1BEA-\u1BEC\u1BEE\u1BF2-\u1BF3\u1C24-\u1C2B\u1C34-\u1C35\u1CE1\u1CF7\uA823-\uA824\uA827\uA880-\uA881\uA8B4-\uA8C3\uA952-\uA953\uA983\uA9B4-\uA9B5\uA9BA-\uA9BB\uA9BE-\uA9C0\uAA2F-\uAA30\uAA33-\uAA34\uAA4D\uAAEB\uAAEE-\uAAEF\uAAF5\uABE3-\uABE4\uABE6-\uABE7\uABE9-\uABEA\uABEC\u{11000}\u{11002}\u{11082}\u{110B0}-\u{110B2}\u{110B7}-\u{110B8}\u{1112C}\u{11145}-\u{11146}\u{11182}\u{111B3}-\u{111B5}\u{111BF}-\u{111C0}\u{111CE}\u{1122C}-\u{1122E}\u{11232}-\u{11233}\u{11235}\u{112E0}-\u{112E2}\u{11302}-\u{11303}\u{1133F}\u{11341}-\u{11344}\u{11347}-\u{11348}\u{1134B}-\u{1134D}\u{11362}-\u{11363}\u{11435}-\u{11437}\u{11440}-\u{11441}\u{11445}\u{114B1}-\u{114B2}\u{114B9}\u{114BB}-\u{114BC}\u{114BE}\u{114C1}\u{115B0}-\u{115B1}\u{115B8}-\u{115BB}\u{115BE}\u{11630}-\u{11632}\u{1163B}-\u{1163C}\u{1163E}\u{116AC}\u{116AE}-\u{116AF}\u{116B6}\u{11726}\u{1182C}-\u{1182E}\u{11838}\u{11931}-\u{11935}\u{11937}-\u{11938}\u{1193D}\u{11940}\u{11942}\u{119D1}-\u{119D3}\u{119DC}-\u{119DF}\u{119E4}\u{11A39}\u{11A57}-\u{11A58}\u{11A97}\u{11C2F}\u{11C3E}\u{11CA9}\u{11CB1}\u{11CB4}\u{11D8A}-\u{11D8E}\u{11D93}-\u{11D94}\u{11D96}\u{11EF5}-\u{11EF6}\u{16F51}-\u{16F87}\u{16FF0}-\u{16FF1}\u{1D166}\u{1D16D}]$/u, reL = /^[\u1100-\u115F\uA960-\uA97C]$/u, reV = /^[\u1160-\u11A7\uD7B0-\uD7C6]$/u, reT = /^[\u11A8-\u11FF\uD7CB-\uD7FB]$/u, reLV = /^[\uAC00\uAC1C\uAC38\uAC54\uAC70\uAC8C\uACA8\uACC4\uACE0\uACFC\uAD18\uAD34\uAD50\uAD6C\uAD88\uADA4\uADC0\uADDC\uADF8\uAE14\uAE30\uAE4C\uAE68\uAE84\uAEA0\uAEBC\uAED8\uAEF4\uAF10\uAF2C\uAF48\uAF64\uAF80\uAF9C\uAFB8\uAFD4\uAFF0\uB00C\uB028\uB044\uB060\uB07C\uB098\uB0B4\uB0D0\uB0EC\uB108\uB124\uB140\uB15C\uB178\uB194\uB1B0\uB1CC\uB1E8\uB204\uB220\uB23C\uB258\uB274\uB290\uB2AC\uB2C8\uB2E4\uB300\uB31C\uB338\uB354\uB370\uB38C\uB3A8\uB3C4\uB3E0\uB3FC\uB418\uB434\uB450\uB46C\uB488\uB4A4\uB4C0\uB4DC\uB4F8\uB514\uB530\uB54C\uB568\uB584\uB5A0\uB5BC\uB5D8\uB5F4\uB610\uB62C\uB648\uB664\uB680\uB69C\uB6B8\uB6D4\uB6F0\uB70C\uB728\uB744\uB760\uB77C\uB798\uB7B4\uB7D0\uB7EC\uB808\uB824\uB840\uB85C\uB878\uB894\uB8B0\uB8CC\uB8E8\uB904\uB920\uB93C\uB958\uB974\uB990\uB9AC\uB9C8\uB9E4\uBA00\uBA1C\uBA38\uBA54\uBA70\uBA8C\uBAA8\uBAC4\uBAE0\uBAFC\uBB18\uBB34\uBB50\uBB6C\uBB88\uBBA4\uBBC0\uBBDC\uBBF8\uBC14\uBC30\uBC4C\uBC68\uBC84\uBCA0\uBCBC\uBCD8\uBCF4\uBD10\uBD2C\uBD48\uBD64\uBD80\uBD9C\uBDB8\uBDD4\uBDF0\uBE0C\uBE28\uBE44\uBE60\uBE7C\uBE98\uBEB4\uBED0\uBEEC\uBF08\uBF24\uBF40\uBF5C\uBF78\uBF94\uBFB0\uBFCC\uBFE8\uC004\uC020\uC03C\uC058\uC074\uC090\uC0AC\uC0C8\uC0E4\uC100\uC11C\uC138\uC154\uC170\uC18C\uC1A8\uC1C4\uC1E0\uC1FC\uC218\uC234\uC250\uC26C\uC288\uC2A4\uC2C0\uC2DC\uC2F8\uC314\uC330\uC34C\uC368\uC384\uC3A0\uC3BC\uC3D8\uC3F4\uC410\uC42C\uC448\uC464\uC480\uC49C\uC4B8\uC4D4\uC4F0\uC50C\uC528\uC544\uC560\uC57C\uC598\uC5B4\uC5D0\uC5EC\uC608\uC624\uC640\uC65C\uC678\uC694\uC6B0\uC6CC\uC6E8\uC704\uC720\uC73C\uC758\uC774\uC790\uC7AC\uC7C8\uC7E4\uC800\uC81C\uC838\uC854\uC870\uC88C\uC8A8\uC8C4\uC8E0\uC8FC\uC918\uC934\uC950\uC96C\uC988\uC9A4\uC9C0\uC9DC\uC9F8\uCA14\uCA30\uCA4C\uCA68\uCA84\uCAA0\uCABC\uCAD8\uCAF4\uCB10\uCB2C\uCB48\uCB64\uCB80\uCB9C\uCBB8\uCBD4\uCBF0\uCC0C\uCC28\uCC44\uCC60\uCC7C\uCC98\uCCB4\uCCD0\uCCEC\uCD08\uCD24\uCD40\uCD5C\uCD78\uCD94\uCDB0\uCDCC\uCDE8\uCE04\uCE20\uCE3C\uCE58\uCE74\uCE90\uCEAC\uCEC8\uCEE4\uCF00\uCF1C\uCF38\uCF54\uCF70\uCF8C\uCFA8\uCFC4\uCFE0\uCFFC\uD018\uD034\uD050\uD06C\uD088\uD0A4\uD0C0\uD0DC\uD0F8\uD114\uD130\uD14C\uD168\uD184\uD1A0\uD1BC\uD1D8\uD1F4\uD210\uD22C\uD248\uD264\uD280\uD29C\uD2B8\uD2D4\uD2F0\uD30C\uD328\uD344\uD360\uD37C\uD398\uD3B4\uD3D0\uD3EC\uD408\uD424\uD440\uD45C\uD478\uD494\uD4B0\uD4CC\uD4E8\uD504\uD520\uD53C\uD558\uD574\uD590\uD5AC\uD5C8\uD5E4\uD600\uD61C\uD638\uD654\uD670\uD68C\uD6A8\uD6C4\uD6E0\uD6FC\uD718\uD734\uD750\uD76C\uD788]$/u, reLVT = /^[\uAC01-\uAC1B\uAC1D-\uAC37\uAC39-\uAC53\uAC55-\uAC6F\uAC71-\uAC8B\uAC8D-\uACA7\uACA9-\uACC3\uACC5-\uACDF\uACE1-\uACFB\uACFD-\uAD17\uAD19-\uAD33\uAD35-\uAD4F\uAD51-\uAD6B\uAD6D-\uAD87\uAD89-\uADA3\uADA5-\uADBF\uADC1-\uADDB\uADDD-\uADF7\uADF9-\uAE13\uAE15-\uAE2F\uAE31-\uAE4B\uAE4D-\uAE67\uAE69-\uAE83\uAE85-\uAE9F\uAEA1-\uAEBB\uAEBD-\uAED7\uAED9-\uAEF3\uAEF5-\uAF0F\uAF11-\uAF2B\uAF2D-\uAF47\uAF49-\uAF63\uAF65-\uAF7F\uAF81-\uAF9B\uAF9D-\uAFB7\uAFB9-\uAFD3\uAFD5-\uAFEF\uAFF1-\uB00B\uB00D-\uB027\uB029-\uB043\uB045-\uB05F\uB061-\uB07B\uB07D-\uB097\uB099-\uB0B3\uB0B5-\uB0CF\uB0D1-\uB0EB\uB0ED-\uB107\uB109-\uB123\uB125-\uB13F\uB141-\uB15B\uB15D-\uB177\uB179-\uB193\uB195-\uB1AF\uB1B1-\uB1CB\uB1CD-\uB1E7\uB1E9-\uB203\uB205-\uB21F\uB221-\uB23B\uB23D-\uB257\uB259-\uB273\uB275-\uB28F\uB291-\uB2AB\uB2AD-\uB2C7\uB2C9-\uB2E3\uB2E5-\uB2FF\uB301-\uB31B\uB31D-\uB337\uB339-\uB353\uB355-\uB36F\uB371-\uB38B\uB38D-\uB3A7\uB3A9-\uB3C3\uB3C5-\uB3DF\uB3E1-\uB3FB\uB3FD-\uB417\uB419-\uB433\uB435-\uB44F\uB451-\uB46B\uB46D-\uB487\uB489-\uB4A3\uB4A5-\uB4BF\uB4C1-\uB4DB\uB4DD-\uB4F7\uB4F9-\uB513\uB515-\uB52F\uB531-\uB54B\uB54D-\uB567\uB569-\uB583\uB585-\uB59F\uB5A1-\uB5BB\uB5BD-\uB5D7\uB5D9-\uB5F3\uB5F5-\uB60F\uB611-\uB62B\uB62D-\uB647\uB649-\uB663\uB665-\uB67F\uB681-\uB69B\uB69D-\uB6B7\uB6B9-\uB6D3\uB6D5-\uB6EF\uB6F1-\uB70B\uB70D-\uB727\uB729-\uB743\uB745-\uB75F\uB761-\uB77B\uB77D-\uB797\uB799-\uB7B3\uB7B5-\uB7CF\uB7D1-\uB7EB\uB7ED-\uB807\uB809-\uB823\uB825-\uB83F\uB841-\uB85B\uB85D-\uB877\uB879-\uB893\uB895-\uB8AF\uB8B1-\uB8CB\uB8CD-\uB8E7\uB8E9-\uB903\uB905-\uB91F\uB921-\uB93B\uB93D-\uB957\uB959-\uB973\uB975-\uB98F\uB991-\uB9AB\uB9AD-\uB9C7\uB9C9-\uB9E3\uB9E5-\uB9FF\uBA01-\uBA1B\uBA1D-\uBA37\uBA39-\uBA53\uBA55-\uBA6F\uBA71-\uBA8B\uBA8D-\uBAA7\uBAA9-\uBAC3\uBAC5-\uBADF\uBAE1-\uBAFB\uBAFD-\uBB17\uBB19-\uBB33\uBB35-\uBB4F\uBB51-\uBB6B\uBB6D-\uBB87\uBB89-\uBBA3\uBBA5-\uBBBF\uBBC1-\uBBDB\uBBDD-\uBBF7\uBBF9-\uBC13\uBC15-\uBC2F\uBC31-\uBC4B\uBC4D-\uBC67\uBC69-\uBC83\uBC85-\uBC9F\uBCA1-\uBCBB\uBCBD-\uBCD7\uBCD9-\uBCF3\uBCF5-\uBD0F\uBD11-\uBD2B\uBD2D-\uBD47\uBD49-\uBD63\uBD65-\uBD7F\uBD81-\uBD9B\uBD9D-\uBDB7\uBDB9-\uBDD3\uBDD5-\uBDEF\uBDF1-\uBE0B\uBE0D-\uBE27\uBE29-\uBE43\uBE45-\uBE5F\uBE61-\uBE7B\uBE7D-\uBE97\uBE99-\uBEB3\uBEB5-\uBECF\uBED1-\uBEEB\uBEED-\uBF07\uBF09-\uBF23\uBF25-\uBF3F\uBF41-\uBF5B\uBF5D-\uBF77\uBF79-\uBF93\uBF95-\uBFAF\uBFB1-\uBFCB\uBFCD-\uBFE7\uBFE9-\uC003\uC005-\uC01F\uC021-\uC03B\uC03D-\uC057\uC059-\uC073\uC075-\uC08F\uC091-\uC0AB\uC0AD-\uC0C7\uC0C9-\uC0E3\uC0E5-\uC0FF\uC101-\uC11B\uC11D-\uC137\uC139-\uC153\uC155-\uC16F\uC171-\uC18B\uC18D-\uC1A7\uC1A9-\uC1C3\uC1C5-\uC1DF\uC1E1-\uC1FB\uC1FD-\uC217\uC219-\uC233\uC235-\uC24F\uC251-\uC26B\uC26D-\uC287\uC289-\uC2A3\uC2A5-\uC2BF\uC2C1-\uC2DB\uC2DD-\uC2F7\uC2F9-\uC313\uC315-\uC32F\uC331-\uC34B\uC34D-\uC367\uC369-\uC383\uC385-\uC39F\uC3A1-\uC3BB\uC3BD-\uC3D7\uC3D9-\uC3F3\uC3F5-\uC40F\uC411-\uC42B\uC42D-\uC447\uC449-\uC463\uC465-\uC47F\uC481-\uC49B\uC49D-\uC4B7\uC4B9-\uC4D3\uC4D5-\uC4EF\uC4F1-\uC50B\uC50D-\uC527\uC529-\uC543\uC545-\uC55F\uC561-\uC57B\uC57D-\uC597\uC599-\uC5B3\uC5B5-\uC5CF\uC5D1-\uC5EB\uC5ED-\uC607\uC609-\uC623\uC625-\uC63F\uC641-\uC65B\uC65D-\uC677\uC679-\uC693\uC695-\uC6AF\uC6B1-\uC6CB\uC6CD-\uC6E7\uC6E9-\uC703\uC705-\uC71F\uC721-\uC73B\uC73D-\uC757\uC759-\uC773\uC775-\uC78F\uC791-\uC7AB\uC7AD-\uC7C7\uC7C9-\uC7E3\uC7E5-\uC7FF\uC801-\uC81B\uC81D-\uC837\uC839-\uC853\uC855-\uC86F\uC871-\uC88B\uC88D-\uC8A7\uC8A9-\uC8C3\uC8C5-\uC8DF\uC8E1-\uC8FB\uC8FD-\uC917\uC919-\uC933\uC935-\uC94F\uC951-\uC96B\uC96D-\uC987\uC989-\uC9A3\uC9A5-\uC9BF\uC9C1-\uC9DB\uC9DD-\uC9F7\uC9F9-\uCA13\uCA15-\uCA2F\uCA31-\uCA4B\uCA4D-\uCA67\uCA69-\uCA83\uCA85-\uCA9F\uCAA1-\uCABB\uCABD-\uCAD7\uCAD9-\uCAF3\uCAF5-\uCB0F\uCB11-\uCB2B\uCB2D-\uCB47\uCB49-\uCB63\uCB65-\uCB7F\uCB81-\uCB9B\uCB9D-\uCBB7\uCBB9-\uCBD3\uCBD5-\uCBEF\uCBF1-\uCC0B\uCC0D-\uCC27\uCC29-\uCC43\uCC45-\uCC5F\uCC61-\uCC7B\uCC7D-\uCC97\uCC99-\uCCB3\uCCB5-\uCCCF\uCCD1-\uCCEB\uCCED-\uCD07\uCD09-\uCD23\uCD25-\uCD3F\uCD41-\uCD5B\uCD5D-\uCD77\uCD79-\uCD93\uCD95-\uCDAF\uCDB1-\uCDCB\uCDCD-\uCDE7\uCDE9-\uCE03\uCE05-\uCE1F\uCE21-\uCE3B\uCE3D-\uCE57\uCE59-\uCE73\uCE75-\uCE8F\uCE91-\uCEAB\uCEAD-\uCEC7\uCEC9-\uCEE3\uCEE5-\uCEFF\uCF01-\uCF1B\uCF1D-\uCF37\uCF39-\uCF53\uCF55-\uCF6F\uCF71-\uCF8B\uCF8D-\uCFA7\uCFA9-\uCFC3\uCFC5-\uCFDF\uCFE1-\uCFFB\uCFFD-\uD017\uD019-\uD033\uD035-\uD04F\uD051-\uD06B\uD06D-\uD087\uD089-\uD0A3\uD0A5-\uD0BF\uD0C1-\uD0DB\uD0DD-\uD0F7\uD0F9-\uD113\uD115-\uD12F\uD131-\uD14B\uD14D-\uD167\uD169-\uD183\uD185-\uD19F\uD1A1-\uD1BB\uD1BD-\uD1D7\uD1D9-\uD1F3\uD1F5-\uD20F\uD211-\uD22B\uD22D-\uD247\uD249-\uD263\uD265-\uD27F\uD281-\uD29B\uD29D-\uD2B7\uD2B9-\uD2D3\uD2D5-\uD2EF\uD2F1-\uD30B\uD30D-\uD327\uD329-\uD343\uD345-\uD35F\uD361-\uD37B\uD37D-\uD397\uD399-\uD3B3\uD3B5-\uD3CF\uD3D1-\uD3EB\uD3ED-\uD407\uD409-\uD423\uD425-\uD43F\uD441-\uD45B\uD45D-\uD477\uD479-\uD493\uD495-\uD4AF\uD4B1-\uD4CB\uD4CD-\uD4E7\uD4E9-\uD503\uD505-\uD51F\uD521-\uD53B\uD53D-\uD557\uD559-\uD573\uD575-\uD58F\uD591-\uD5AB\uD5AD-\uD5C7\uD5C9-\uD5E3\uD5E5-\uD5FF\uD601-\uD61B\uD61D-\uD637\uD639-\uD653\uD655-\uD66F\uD671-\uD68B\uD68D-\uD6A7\uD6A9-\uD6C3\uD6C5-\uD6DF\uD6E1-\uD6FB\uD6FD-\uD717\uD719-\uD733\uD735-\uD74F\uD751-\uD76B\uD76D-\uD787\uD789-\uD7A3]$/u, reExtPict = new RegExp("^\\p{ExtPict}$", "u"), getCodepointType = (char, code2) => {
  let type = CodepointType.Any;
  return char.search(reExtend) !== -1 && (type |= CodepointType.Extend), code2 === 8205 && (type |= CodepointType.ZWJ), code2 >= 127462 && code2 <= 127487 && (type |= CodepointType.RI), char.search(rePrepend) !== -1 && (type |= CodepointType.Prepend), char.search(reSpacingMark) !== -1 && (type |= CodepointType.SpacingMark), char.search(reL) !== -1 && (type |= CodepointType.L), char.search(reV) !== -1 && (type |= CodepointType.V), char.search(reT) !== -1 && (type |= CodepointType.T), char.search(reLV) !== -1 && (type |= CodepointType.LV), char.search(reLVT) !== -1 && (type |= CodepointType.LVT), char.search(reExtPict) !== -1 && (type |= CodepointType.ExtPict), type;
};
function intersects(x, y) {
  return (x & y) !== 0;
}
const NonBoundaryPairs = [
  // GB6
  [CodepointType.L, CodepointType.L | CodepointType.V | CodepointType.LV | CodepointType.LVT],
  // GB7
  [CodepointType.LV | CodepointType.V, CodepointType.V | CodepointType.T],
  // GB8
  [CodepointType.LVT | CodepointType.T, CodepointType.T],
  // GB9
  [CodepointType.Any, CodepointType.Extend | CodepointType.ZWJ],
  // GB9a
  [CodepointType.Any, CodepointType.SpacingMark],
  // GB9b
  [CodepointType.Prepend, CodepointType.Any],
  // GB11
  [CodepointType.ZWJ, CodepointType.ExtPict],
  // GB12 and GB13
  [CodepointType.RI, CodepointType.RI]
];
function isBoundaryPair(left, right) {
  return NonBoundaryPairs.findIndex((r) => intersects(left, r[0]) && intersects(right, r[1])) === -1;
}
const endingEmojiZWJ = new RegExp("\\p{ExtPict}[\\p{Gr_Ext}\\p{EMod}]*\\u200D$", "u"), endsWithEmojiZWJ = (str) => str.search(endingEmojiZWJ) !== -1, endingRIs = new RegExp("\\p{RI}+$", "gu"), endsWithOddNumberOfRIs = (str) => {
  const match2 = str.match(endingRIs);
  return match2 === null ? !1 : match2[0].length / 2 % 2 === 1;
}, DIRTY_PATHS = /* @__PURE__ */ new WeakMap(), DIRTY_PATH_KEYS = /* @__PURE__ */ new WeakMap(), FLUSHING = /* @__PURE__ */ new WeakMap(), NORMALIZING = /* @__PURE__ */ new WeakMap(), PATH_REFS = /* @__PURE__ */ new WeakMap(), POINT_REFS = /* @__PURE__ */ new WeakMap(), RANGE_REFS = /* @__PURE__ */ new WeakMap(), TextTransforms = {
  delete(editor, options) {
    editor.delete(options);
  },
  insertFragment(editor, fragment2, options) {
    editor.insertFragment(fragment2, options);
  },
  insertText(editor, text, options = {}) {
    Editor.withoutNormalizing(editor, () => {
      const {
        voids = !1
      } = options;
      let {
        at = getDefaultInsertLocation(editor)
      } = options;
      if (Path.isPath(at) && (at = Editor.range(editor, at)), Range.isRange(at))
        if (Range.isCollapsed(at))
          at = at.anchor;
        else {
          const end2 = Range.end(at);
          if (!voids && Editor.void(editor, {
            at: end2
          }))
            return;
          const start2 = Range.start(at), startRef = Editor.pointRef(editor, start2), endRef = Editor.pointRef(editor, end2);
          Transforms.delete(editor, {
            at,
            voids
          });
          const startPoint = startRef.unref(), endPoint = endRef.unref();
          at = startPoint || endPoint, Transforms.setSelection(editor, {
            anchor: at,
            focus: at
          });
        }
      if (!voids && Editor.void(editor, {
        at
      }) || Editor.elementReadOnly(editor, {
        at
      }))
        return;
      const {
        path: path2,
        offset
      } = at;
      text.length > 0 && editor.apply({
        type: "insert_text",
        path: path2,
        offset,
        text
      });
    });
  }
}, Transforms = {
  ...GeneralTransforms,
  ...NodeTransforms,
  ...SelectionTransforms,
  ...TextTransforms
}, insertChildren$1 = (xs, index, ...newValues) => [...xs.slice(0, index), ...newValues, ...xs.slice(index)], replaceChildren = (xs, index, removeCount, ...newValues) => [...xs.slice(0, index), ...newValues, ...xs.slice(index + removeCount)], removeChildren$1 = replaceChildren, modifyDescendant = (root, path2, f) => {
  if (path2.length === 0)
    throw new Error("Cannot modify the editor");
  const node2 = Node$1.get(root, path2), slicedPath = path2.slice();
  let modifiedNode = f(node2);
  for (; slicedPath.length > 1; ) {
    const index2 = slicedPath.pop(), ancestorNode = Node$1.get(root, slicedPath);
    modifiedNode = {
      ...ancestorNode,
      children: replaceChildren(ancestorNode.children, index2, 1, modifiedNode)
    };
  }
  const index = slicedPath.pop();
  root.children = replaceChildren(root.children, index, 1, modifiedNode);
}, modifyChildren = (root, path2, f) => {
  path2.length === 0 ? root.children = f(root.children) : modifyDescendant(root, path2, (node2) => {
    if (Text$1.isText(node2))
      throw new Error(`Cannot get the element at path [${path2}] because it refers to a leaf node: ${Scrubber.stringify(node2)}`);
    return {
      ...node2,
      children: f(node2.children)
    };
  });
}, modifyLeaf = (root, path2, f) => modifyDescendant(root, path2, (node2) => {
  if (!Text$1.isText(node2))
    throw new Error(`Cannot get the leaf node at path [${path2}] because it refers to a non-leaf node: ${Scrubber.stringify(node2)}`);
  return f(node2);
}), Node$1 = {
  ancestor(root, path2) {
    const node2 = Node$1.get(root, path2);
    if (Text$1.isText(node2))
      throw new Error(`Cannot get the ancestor node at path [${path2}] because it refers to a text node instead: ${Scrubber.stringify(node2)}`);
    return node2;
  },
  *ancestors(root, path2, options = {}) {
    for (const p of Path.ancestors(path2, options))
      yield [Node$1.ancestor(root, p), p];
  },
  child(root, index) {
    if (Text$1.isText(root))
      throw new Error(`Cannot get the child of a text node: ${Scrubber.stringify(root)}`);
    const c2 = root.children[index];
    if (c2 == null)
      throw new Error(`Cannot get child at index \`${index}\` in node: ${Scrubber.stringify(root)}`);
    return c2;
  },
  *children(root, path2, options = {}) {
    const {
      reverse = !1
    } = options, ancestor = Node$1.ancestor(root, path2), {
      children
    } = ancestor;
    let index = reverse ? children.length - 1 : 0;
    for (; reverse ? index >= 0 : index < children.length; ) {
      const child = Node$1.child(ancestor, index), childPath = path2.concat(index);
      yield [child, childPath], index = reverse ? index - 1 : index + 1;
    }
  },
  common(root, path2, another) {
    const p = Path.common(path2, another);
    return [Node$1.get(root, p), p];
  },
  descendant(root, path2) {
    const node2 = Node$1.get(root, path2);
    if (Editor.isEditor(node2))
      throw new Error(`Cannot get the descendant node at path [${path2}] because it refers to the root editor node instead: ${Scrubber.stringify(node2)}`);
    return node2;
  },
  *descendants(root, options = {}) {
    for (const [node2, path2] of Node$1.nodes(root, options))
      path2.length !== 0 && (yield [node2, path2]);
  },
  *elements(root, options = {}) {
    for (const [node2, path2] of Node$1.nodes(root, options))
      Element$2.isElement(node2) && (yield [node2, path2]);
  },
  extractProps(node2) {
    if (Element$2.isAncestor(node2)) {
      const {
        children: _children,
        ...properties
      } = node2;
      return properties;
    } else {
      const {
        text: _text,
        ...properties
      } = node2;
      return properties;
    }
  },
  first(root, path2) {
    const p = path2.slice();
    let n2 = Node$1.get(root, p);
    for (; n2 && !(Text$1.isText(n2) || n2.children.length === 0); )
      n2 = n2.children[0], p.push(0);
    return [n2, p];
  },
  fragment(root, range2) {
    const newRoot = {
      children: root.children
    }, [start2, end2] = Range.edges(range2), nodeEntries = Node$1.nodes(newRoot, {
      reverse: !0,
      pass: ([, path2]) => !Range.includes(range2, path2)
    });
    for (const [, path2] of nodeEntries) {
      if (!Range.includes(range2, path2)) {
        const index = path2[path2.length - 1];
        modifyChildren(newRoot, Path.parent(path2), (children) => removeChildren$1(children, index, 1));
      }
      Path.equals(path2, end2.path) && modifyLeaf(newRoot, path2, (node2) => {
        const before2 = node2.text.slice(0, end2.offset);
        return {
          ...node2,
          text: before2
        };
      }), Path.equals(path2, start2.path) && modifyLeaf(newRoot, path2, (node2) => {
        const before2 = node2.text.slice(start2.offset);
        return {
          ...node2,
          text: before2
        };
      });
    }
    return newRoot.children;
  },
  get(root, path2) {
    const node2 = Node$1.getIf(root, path2);
    if (node2 === void 0)
      throw new Error(`Cannot find a descendant at path [${path2}] in node: ${Scrubber.stringify(root)}`);
    return node2;
  },
  getIf(root, path2) {
    let node2 = root;
    for (let i = 0; i < path2.length; i++) {
      const p = path2[i];
      if (Text$1.isText(node2) || !node2.children[p])
        return;
      node2 = node2.children[p];
    }
    return node2;
  },
  has(root, path2) {
    let node2 = root;
    for (let i = 0; i < path2.length; i++) {
      const p = path2[i];
      if (Text$1.isText(node2) || !node2.children[p])
        return !1;
      node2 = node2.children[p];
    }
    return !0;
  },
  isNode(value, {
    deep = !1
  } = {}) {
    return Text$1.isText(value) || Element$2.isElement(value, {
      deep
    }) || Editor.isEditor(value, {
      deep
    });
  },
  isNodeList(value, {
    deep = !1
  } = {}) {
    return Array.isArray(value) && value.every((val) => Node$1.isNode(val, {
      deep
    }));
  },
  last(root, path2) {
    const p = path2.slice();
    let n2 = Node$1.get(root, p);
    for (; n2 && !(Text$1.isText(n2) || n2.children.length === 0); ) {
      const i = n2.children.length - 1;
      n2 = n2.children[i], p.push(i);
    }
    return [n2, p];
  },
  leaf(root, path2) {
    const node2 = Node$1.get(root, path2);
    if (!Text$1.isText(node2))
      throw new Error(`Cannot get the leaf node at path [${path2}] because it refers to a non-leaf node: ${Scrubber.stringify(node2)}`);
    return node2;
  },
  *levels(root, path2, options = {}) {
    for (const p of Path.levels(path2, options))
      yield [Node$1.get(root, p), p];
  },
  matches(node2, props) {
    return Element$2.isElement(node2) && Element$2.isElementProps(props) && Element$2.matches(node2, props) || Text$1.isText(node2) && Text$1.isTextProps(props) && Text$1.matches(node2, props);
  },
  *nodes(root, options = {}) {
    const {
      pass,
      reverse = !1
    } = options, {
      from = [],
      to
    } = options, visited = /* @__PURE__ */ new Set();
    let p = [], n2 = root;
    for (; !(to && (reverse ? Path.isBefore(p, to) : Path.isAfter(p, to))); ) {
      if (visited.has(n2) || (yield [n2, p]), !visited.has(n2) && !Text$1.isText(n2) && n2.children.length !== 0 && (pass == null || pass([n2, p]) === !1)) {
        visited.add(n2);
        let nextIndex = reverse ? n2.children.length - 1 : 0;
        Path.isAncestor(p, from) && (nextIndex = from[p.length]), p = p.concat(nextIndex), n2 = Node$1.get(root, p);
        continue;
      }
      if (p.length === 0)
        break;
      if (!reverse) {
        const newPath = Path.next(p);
        if (Node$1.has(root, newPath)) {
          p = newPath, n2 = Node$1.get(root, p);
          continue;
        }
      }
      if (reverse && p[p.length - 1] !== 0) {
        p = Path.previous(p), n2 = Node$1.get(root, p);
        continue;
      }
      p = Path.parent(p), n2 = Node$1.get(root, p), visited.add(n2);
    }
  },
  parent(root, path2) {
    const parentPath = Path.parent(path2), p = Node$1.get(root, parentPath);
    if (Text$1.isText(p))
      throw new Error(`Cannot get the parent of path [${path2}] because it does not exist in the root.`);
    return p;
  },
  string(node2) {
    return Text$1.isText(node2) ? node2.text : node2.children.map(Node$1.string).join("");
  },
  *texts(root, options = {}) {
    for (const [node2, path2] of Node$1.nodes(root, options))
      Text$1.isText(node2) && (yield [node2, path2]);
  }
}, isEditor = (value, {
  deep = !1
} = {}) => isObject(value) ? typeof value.addMark == "function" && typeof value.apply == "function" && typeof value.deleteFragment == "function" && typeof value.insertBreak == "function" && typeof value.insertSoftBreak == "function" && typeof value.insertFragment == "function" && typeof value.insertNode == "function" && typeof value.insertText == "function" && typeof value.isElementReadOnly == "function" && typeof value.isInline == "function" && typeof value.isSelectable == "function" && typeof value.isVoid == "function" && typeof value.normalizeNode == "function" && typeof value.onChange == "function" && typeof value.removeMark == "function" && typeof value.getDirtyPaths == "function" && (value.marks === null || isObject(value.marks)) && (value.selection === null || Range.isRange(value.selection)) && (!deep || Node$1.isNodeList(value.children)) && Operation.isOperationList(value.operations) : !1, Editor = {
  above(editor, options) {
    return editor.above(options);
  },
  addMark(editor, key, value) {
    editor.addMark(key, value);
  },
  after(editor, at, options) {
    return editor.after(at, options);
  },
  before(editor, at, options) {
    return editor.before(at, options);
  },
  deleteBackward(editor, options = {}) {
    const {
      unit = "character"
    } = options;
    editor.deleteBackward(unit);
  },
  deleteForward(editor, options = {}) {
    const {
      unit = "character"
    } = options;
    editor.deleteForward(unit);
  },
  deleteFragment(editor, options) {
    editor.deleteFragment(options);
  },
  edges(editor, at) {
    return editor.edges(at);
  },
  elementReadOnly(editor, options = {}) {
    return editor.elementReadOnly(options);
  },
  end(editor, at) {
    return editor.end(at);
  },
  first(editor, at) {
    return editor.first(at);
  },
  fragment(editor, at) {
    return editor.fragment(at);
  },
  hasBlocks(editor, element) {
    return editor.hasBlocks(element);
  },
  hasInlines(editor, element) {
    return editor.hasInlines(element);
  },
  hasPath(editor, path2) {
    return editor.hasPath(path2);
  },
  hasTexts(editor, element) {
    return editor.hasTexts(element);
  },
  insertBreak(editor) {
    editor.insertBreak();
  },
  insertFragment(editor, fragment2, options) {
    editor.insertFragment(fragment2, options);
  },
  insertNode(editor, node2) {
    editor.insertNode(node2);
  },
  insertSoftBreak(editor) {
    editor.insertSoftBreak();
  },
  insertText(editor, text) {
    editor.insertText(text);
  },
  isBlock(editor, value) {
    return editor.isBlock(value);
  },
  isEdge(editor, point2, at) {
    return editor.isEdge(point2, at);
  },
  isEditor(value) {
    return isEditor(value);
  },
  isElementReadOnly(editor, element) {
    return editor.isElementReadOnly(element);
  },
  isEmpty(editor, element) {
    return editor.isEmpty(element);
  },
  isEnd(editor, point2, at) {
    return editor.isEnd(point2, at);
  },
  isInline(editor, value) {
    return editor.isInline(value);
  },
  isNormalizing(editor) {
    return editor.isNormalizing();
  },
  isSelectable(editor, value) {
    return editor.isSelectable(value);
  },
  isStart(editor, point2, at) {
    return editor.isStart(point2, at);
  },
  isVoid(editor, value) {
    return editor.isVoid(value);
  },
  last(editor, at) {
    return editor.last(at);
  },
  leaf(editor, at, options) {
    return editor.leaf(at, options);
  },
  levels(editor, options) {
    return editor.levels(options);
  },
  marks(editor) {
    return editor.getMarks();
  },
  next(editor, options) {
    return editor.next(options);
  },
  node(editor, at, options) {
    return editor.node(at, options);
  },
  nodes(editor, options) {
    return editor.nodes(options);
  },
  normalize(editor, options) {
    editor.normalize(options);
  },
  parent(editor, at, options) {
    return editor.parent(at, options);
  },
  path(editor, at, options) {
    return editor.path(at, options);
  },
  pathRef(editor, path2, options) {
    return editor.pathRef(path2, options);
  },
  pathRefs(editor) {
    return editor.pathRefs();
  },
  point(editor, at, options) {
    return editor.point(at, options);
  },
  pointRef(editor, point2, options) {
    return editor.pointRef(point2, options);
  },
  pointRefs(editor) {
    return editor.pointRefs();
  },
  positions(editor, options) {
    return editor.positions(options);
  },
  previous(editor, options) {
    return editor.previous(options);
  },
  range(editor, at, to) {
    return editor.range(at, to);
  },
  rangeRef(editor, range2, options) {
    return editor.rangeRef(range2, options);
  },
  rangeRefs(editor) {
    return editor.rangeRefs();
  },
  removeMark(editor, key) {
    editor.removeMark(key);
  },
  setNormalizing(editor, isNormalizing2) {
    editor.setNormalizing(isNormalizing2);
  },
  start(editor, at) {
    return editor.start(at);
  },
  string(editor, at, options) {
    return editor.string(at, options);
  },
  unhangRange(editor, range2, options) {
    return editor.unhangRange(range2, options);
  },
  void(editor, options) {
    return editor.void(options);
  },
  withoutNormalizing(editor, fn) {
    editor.withoutNormalizing(fn);
  },
  shouldMergeNodesRemovePrevNode: (editor, prevNode, curNode) => editor.shouldMergeNodesRemovePrevNode(prevNode, curNode)
}, BATCHING_DIRTY_PATHS = /* @__PURE__ */ new WeakMap(), isBatchingDirtyPaths = (editor) => BATCHING_DIRTY_PATHS.get(editor) || !1, batchDirtyPaths = (editor, fn, update) => {
  const value = BATCHING_DIRTY_PATHS.get(editor) || !1;
  BATCHING_DIRTY_PATHS.set(editor, !0);
  try {
    fn(), update();
  } finally {
    BATCHING_DIRTY_PATHS.set(editor, value);
  }
};
function updateDirtyPaths(editor, newDirtyPaths, transform) {
  const oldDirtyPaths = DIRTY_PATHS.get(editor) || [], oldDirtyPathKeys = DIRTY_PATH_KEYS.get(editor) || /* @__PURE__ */ new Set();
  let dirtyPaths, dirtyPathKeys;
  const add = (path2) => {
    if (path2) {
      const key = path2.join(",");
      dirtyPathKeys.has(key) || (dirtyPathKeys.add(key), dirtyPaths.push(path2));
    }
  };
  if (transform) {
    dirtyPaths = [], dirtyPathKeys = /* @__PURE__ */ new Set();
    for (const path2 of oldDirtyPaths) {
      const newPath = transform(path2);
      add(newPath);
    }
  } else
    dirtyPaths = oldDirtyPaths, dirtyPathKeys = oldDirtyPathKeys;
  for (const path2 of newDirtyPaths)
    add(path2);
  DIRTY_PATHS.set(editor, dirtyPaths), DIRTY_PATH_KEYS.set(editor, dirtyPathKeys);
}
const apply$1 = (editor, op) => {
  for (const ref of Editor.pathRefs(editor))
    PathRef.transform(ref, op);
  for (const ref of Editor.pointRefs(editor))
    PointRef.transform(ref, op);
  for (const ref of Editor.rangeRefs(editor))
    RangeRef.transform(ref, op);
  if (!isBatchingDirtyPaths(editor)) {
    const transform = Path.operationCanTransformPath(op) ? (p) => Path.transform(p, op) : void 0;
    updateDirtyPaths(editor, editor.getDirtyPaths(op), transform);
  }
  Transforms.transform(editor, op), editor.operations.push(op), Editor.normalize(editor, {
    operation: op
  }), op.type === "set_selection" && (editor.marks = null), FLUSHING.get(editor) || (FLUSHING.set(editor, !0), Promise.resolve().then(() => {
    FLUSHING.set(editor, !1), editor.onChange({
      operation: op
    }), editor.operations = [];
  }));
}, getDirtyPaths = (_editor, op) => {
  switch (op.type) {
    case "insert_text":
    case "remove_text":
    case "set_node": {
      const {
        path: path2
      } = op;
      return Path.levels(path2);
    }
    case "insert_node": {
      const {
        node: node2,
        path: path2
      } = op, levels2 = Path.levels(path2), descendants = Text$1.isText(node2) ? [] : Array.from(Node$1.nodes(node2), ([, p]) => path2.concat(p));
      return [...levels2, ...descendants];
    }
    case "merge_node": {
      const {
        path: path2
      } = op, ancestors = Path.ancestors(path2), previousPath = Path.previous(path2);
      return [...ancestors, previousPath];
    }
    case "move_node": {
      const {
        path: path2,
        newPath
      } = op;
      if (Path.equals(path2, newPath))
        return [];
      const oldAncestors = [], newAncestors = [];
      for (const ancestor of Path.ancestors(path2)) {
        const p = Path.transform(ancestor, op);
        oldAncestors.push(p);
      }
      for (const ancestor of Path.ancestors(newPath)) {
        const p = Path.transform(ancestor, op);
        newAncestors.push(p);
      }
      const newParent = newAncestors[newAncestors.length - 1], newIndex = newPath[newPath.length - 1], resultPath = newParent.concat(newIndex);
      return [...oldAncestors, ...newAncestors, resultPath];
    }
    case "remove_node": {
      const {
        path: path2
      } = op;
      return [...Path.ancestors(path2)];
    }
    case "split_node": {
      const {
        path: path2
      } = op, levels2 = Path.levels(path2), nextPath = Path.next(path2);
      return [...levels2, nextPath];
    }
    default:
      return [];
  }
}, getFragment = (editor) => {
  const {
    selection
  } = editor;
  return selection ? Node$1.fragment(editor, selection) : [];
}, normalizeNode = (editor, entry, options) => {
  const [node2, path2] = entry;
  if (Text$1.isText(node2))
    return;
  if (Element$2.isElement(node2) && node2.children.length === 0) {
    const child = editor.createSpan();
    Transforms.insertNodes(editor, child, {
      at: path2.concat(0),
      voids: !0
    });
    return;
  }
  const shouldHaveInlines = Editor.isEditor(node2) ? !1 : Element$2.isElement(node2) && (editor.isInline(node2) || node2.children.length === 0 || Text$1.isText(node2.children[0]) || editor.isInline(node2.children[0]));
  let n2 = 0;
  for (let i = 0; i < node2.children.length; i++, n2++) {
    const currentNode = Node$1.get(editor, path2);
    if (Text$1.isText(currentNode))
      continue;
    const child = currentNode.children[n2], prev = currentNode.children[n2 - 1], isLast = i === node2.children.length - 1, isInlineOrText = Text$1.isText(child) || Element$2.isElement(child) && editor.isInline(child);
    if (isInlineOrText !== shouldHaveInlines)
      isInlineOrText ? options?.fallbackElement ? Transforms.wrapNodes(editor, options.fallbackElement(), {
        at: path2.concat(n2),
        voids: !0
      }) : Transforms.removeNodes(editor, {
        at: path2.concat(n2),
        voids: !0
      }) : Transforms.unwrapNodes(editor, {
        at: path2.concat(n2),
        voids: !0
      }), n2--;
    else if (Element$2.isElement(child)) {
      if (editor.isInline(child)) {
        if (prev == null || !Text$1.isText(prev)) {
          const newChild = editor.createSpan();
          Transforms.insertNodes(editor, newChild, {
            at: path2.concat(n2),
            voids: !0
          }), n2++;
        } else if (isLast) {
          const newChild = editor.createSpan();
          Transforms.insertNodes(editor, newChild, {
            at: path2.concat(n2 + 1),
            voids: !0
          }), n2++;
        }
      }
    } else {
      if (!Text$1.isText(child) && !("children" in child)) {
        const elementChild = child;
        elementChild.children = [];
      }
      prev != null && Text$1.isText(prev) && (Text$1.equals(child, prev, {
        loose: !0
      }) ? (Transforms.mergeNodes(editor, {
        at: path2.concat(n2),
        voids: !0
      }), n2--) : prev.text === "" ? (Transforms.removeNodes(editor, {
        at: path2.concat(n2 - 1),
        voids: !0
      }), n2--) : child.text === "" && (Transforms.removeNodes(editor, {
        at: path2.concat(n2),
        voids: !0
      }), n2--));
    }
  }
}, shouldNormalize = (_editor, {
  iteration,
  initialDirtyPathsLength
}) => {
  const maxIterations = initialDirtyPathsLength * 42;
  if (iteration > maxIterations)
    throw new Error(`Could not completely normalize the editor after ${maxIterations} iterations! This is usually due to incorrect normalization logic that leaves a node in an invalid state.`);
  return !0;
}, above = (editor, options = {}) => {
  const {
    voids = !1,
    mode = "lowest",
    at = editor.selection,
    match: match2
  } = options;
  if (!at)
    return;
  let path2 = Editor.path(editor, at);
  if (!Range.isRange(at) || Path.equals(at.focus.path, at.anchor.path)) {
    if (path2.length === 0)
      return;
    path2 = Path.parent(path2);
  }
  const reverse = mode === "lowest", [firstMatch] = Editor.levels(editor, {
    at: path2,
    voids,
    match: match2,
    reverse
  });
  return firstMatch;
}, addMark = (editor, key, value) => {
  const {
    selection
  } = editor;
  if (selection) {
    const match2 = (node2, path2) => {
      if (!Text$1.isText(node2))
        return !1;
      const [parentNode] = Editor.parent(editor, path2);
      return !editor.isVoid(parentNode) || editor.markableVoid(parentNode);
    }, expandedSelection = Range.isExpanded(selection);
    let markAcceptingVoidSelected = !1;
    if (!expandedSelection) {
      const [selectedNode, selectedPath] = Editor.node(editor, selection);
      if (selectedNode && match2(selectedNode, selectedPath)) {
        const [parentNode] = Editor.parent(editor, selectedPath);
        markAcceptingVoidSelected = parentNode && editor.markableVoid(parentNode);
      }
    }
    if (expandedSelection || markAcceptingVoidSelected)
      Transforms.setNodes(editor, {
        [key]: value
      }, {
        match: match2,
        split: !0,
        voids: !0
      });
    else {
      const marks2 = {
        ...Editor.marks(editor) || {},
        [key]: value
      };
      editor.marks = marks2, FLUSHING.get(editor) || editor.onChange();
    }
  }
}, after = (editor, at, options = {}) => {
  const anchor = Editor.point(editor, at, {
    edge: "end"
  }), focus = Editor.end(editor, []), range2 = {
    anchor,
    focus
  }, {
    distance = 1
  } = options;
  let d = 0, target;
  for (const p of Editor.positions(editor, {
    ...options,
    at: range2
  })) {
    if (d > distance)
      break;
    d !== 0 && (target = p), d++;
  }
  return target;
}, before = (editor, at, options = {}) => {
  const anchor = Editor.start(editor, []), focus = Editor.point(editor, at, {
    edge: "start"
  }), range2 = {
    anchor,
    focus
  }, {
    distance = 1
  } = options;
  let d = 0, target;
  for (const p of Editor.positions(editor, {
    ...options,
    at: range2,
    reverse: !0
  })) {
    if (d > distance)
      break;
    d !== 0 && (target = p), d++;
  }
  return target;
}, deleteBackward = (editor, unit) => {
  const {
    selection
  } = editor;
  selection && Range.isCollapsed(selection) && Transforms.delete(editor, {
    unit,
    reverse: !0
  });
}, deleteForward = (editor, unit) => {
  const {
    selection
  } = editor;
  selection && Range.isCollapsed(selection) && Transforms.delete(editor, {
    unit
  });
}, deleteFragment = (editor, {
  direction = "forward"
} = {}) => {
  const {
    selection
  } = editor;
  selection && Range.isExpanded(selection) && Transforms.delete(editor, {
    reverse: direction === "backward"
  });
}, edges = (editor, at) => [Editor.start(editor, at), Editor.end(editor, at)], elementReadOnly = (editor, options = {}) => Editor.above(editor, {
  ...options,
  match: (n2) => Element$2.isElement(n2) && Editor.isElementReadOnly(editor, n2)
}), end = (editor, at) => Editor.point(editor, at, {
  edge: "end"
}), first = (editor, at) => {
  const path2 = Editor.path(editor, at, {
    edge: "start"
  });
  return Editor.node(editor, path2);
}, fragment = (editor, at) => {
  const range2 = Editor.range(editor, at);
  return Node$1.fragment(editor, range2);
}, getVoid = (editor, options = {}) => Editor.above(editor, {
  ...options,
  match: (n2) => Element$2.isElement(n2) && Editor.isVoid(editor, n2)
}), hasBlocks = (editor, element) => element.children.some((n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)), hasInlines = (editor, element) => element.children.some((n2) => Text$1.isText(n2) || Editor.isInline(editor, n2)), hasPath = (editor, path2) => Node$1.has(editor, path2), hasTexts = (_editor, element) => element.children.every((n2) => Text$1.isText(n2)), insertBreak = (editor) => {
  Transforms.splitNodes(editor, {
    always: !0
  });
}, insertNode = (editor, node2, options) => {
  Transforms.insertNodes(editor, node2, options);
}, insertSoftBreak = (editor) => {
  Transforms.splitNodes(editor, {
    always: !0
  });
}, insertText = (editor, text, options = {}) => {
  const {
    selection,
    marks: marks2
  } = editor;
  if (selection) {
    if (marks2) {
      const node2 = {
        text,
        ...marks2
      };
      Transforms.insertNodes(editor, node2, {
        at: options.at,
        voids: options.voids
      });
    } else
      Transforms.insertText(editor, text, options);
    editor.marks = null;
  }
}, isBlock = (editor, value) => !editor.isInline(value), isEdge = (editor, point2, at) => Editor.isStart(editor, point2, at) || Editor.isEnd(editor, point2, at), isEmpty = (editor, element) => {
  const {
    children
  } = element, [first2] = children;
  return children.length === 0 || children.length === 1 && Text$1.isText(first2) && first2.text === "" && !editor.isVoid(element);
}, isEnd = (editor, point2, at) => {
  const end2 = Editor.end(editor, at);
  return Point.equals(point2, end2);
}, isNormalizing = (editor) => {
  const isNormalizing2 = NORMALIZING.get(editor);
  return isNormalizing2 === void 0 ? !0 : isNormalizing2;
}, isStart = (editor, point2, at) => {
  if (point2.offset !== 0)
    return !1;
  const start2 = Editor.start(editor, at);
  return Point.equals(point2, start2);
}, last = (editor, at) => {
  const path2 = Editor.path(editor, at, {
    edge: "end"
  });
  return Editor.node(editor, path2);
}, leaf = (editor, at, options = {}) => {
  const path2 = Editor.path(editor, at, options);
  return [Node$1.leaf(editor, path2), path2];
};
function* levels(editor, options = {}) {
  const {
    at = editor.selection,
    reverse = !1,
    voids = !1
  } = options;
  let {
    match: match2
  } = options;
  if (match2 == null && (match2 = () => !0), !at)
    return;
  const levels2 = [], path2 = Editor.path(editor, at);
  for (const [n2, p] of Node$1.levels(editor, path2))
    if (match2(n2, p) && (levels2.push([n2, p]), !voids && Element$2.isElement(n2) && Editor.isVoid(editor, n2)))
      break;
  reverse && levels2.reverse(), yield* levels2;
}
const marks = (editor, _options = {}) => {
  const {
    marks: marks2,
    selection
  } = editor;
  if (!selection)
    return null;
  let {
    anchor,
    focus
  } = selection;
  if (marks2)
    return marks2;
  if (Range.isExpanded(selection)) {
    if (Range.isBackward(selection) && ([focus, anchor] = [anchor, focus]), Editor.isEnd(editor, anchor, anchor.path)) {
      const after2 = Editor.after(editor, anchor);
      after2 && (anchor = after2);
    }
    const [match2] = Editor.nodes(editor, {
      match: Text$1.isText,
      at: {
        anchor,
        focus
      }
    });
    if (match2) {
      const [node22] = match2, {
        text: _text,
        ...rest2
      } = node22;
      return rest2;
    } else
      return {};
  }
  const {
    path: path2
  } = anchor;
  let [node2] = Editor.leaf(editor, path2);
  if (anchor.offset === 0) {
    const prev = Editor.previous(editor, {
      at: path2,
      match: Text$1.isText
    });
    if (!Editor.above(editor, {
      match: (n2) => Element$2.isElement(n2) && Editor.isVoid(editor, n2) && editor.markableVoid(n2)
    })) {
      const block = Editor.above(editor, {
        match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)
      });
      if (prev && block) {
        const [prevNode, prevPath] = prev, [, blockPath] = block;
        Path.isAncestor(blockPath, prevPath) && (node2 = prevNode);
      }
    }
  }
  const {
    text: _text2,
    ...rest
  } = node2;
  return rest;
}, next = (editor, options = {}) => {
  const {
    mode = "lowest",
    voids = !1
  } = options;
  let {
    match: match2,
    at = editor.selection
  } = options;
  if (!at)
    return;
  const pointAfterLocation = Editor.after(editor, at, {
    voids
  });
  if (!pointAfterLocation)
    return;
  const [, to] = Editor.last(editor, []), span = [pointAfterLocation.path, to];
  if (Path.isPath(at) && at.length === 0)
    throw new Error("Cannot get the next node from the root node!");
  if (match2 == null)
    if (Path.isPath(at)) {
      const [parent2] = Editor.parent(editor, at);
      match2 = (n2) => parent2.children.includes(n2);
    } else
      match2 = () => !0;
  const [next2] = Editor.nodes(editor, {
    at: span,
    match: match2,
    mode,
    voids
  });
  return next2;
}, node = (editor, at, options = {}) => {
  const path2 = Editor.path(editor, at, options);
  return [Node$1.get(editor, path2), path2];
};
function* nodes(editor, options = {}) {
  const {
    at = editor.selection,
    mode = "all",
    universal = !1,
    reverse = !1,
    voids = !1,
    pass
  } = options;
  let {
    match: match2
  } = options;
  if (match2 || (match2 = () => !0), !at)
    return;
  let from, to;
  if (Span.isSpan(at))
    from = at[0], to = at[1];
  else {
    const first2 = Editor.path(editor, at, {
      edge: "start"
    }), last2 = Editor.path(editor, at, {
      edge: "end"
    });
    from = reverse ? last2 : first2, to = reverse ? first2 : last2;
  }
  const nodeEntries = Node$1.nodes(editor, {
    reverse,
    from,
    to,
    pass: ([node2, path2]) => pass && pass([node2, path2]) ? !0 : Element$2.isElement(node2) ? !!(!voids && (Editor.isVoid(editor, node2) || Editor.isElementReadOnly(editor, node2))) : !1
  }), matches = [];
  let hit;
  for (const [node2, path2] of nodeEntries) {
    const isLower = hit && Path.compare(path2, hit[1]) === 0;
    if (mode === "highest" && isLower)
      continue;
    if (!match2(node2, path2)) {
      if (universal && !isLower && Text$1.isText(node2))
        return;
      continue;
    }
    if (mode === "lowest" && isLower) {
      hit = [node2, path2];
      continue;
    }
    const emit2 = mode === "lowest" ? hit : [node2, path2];
    emit2 && (universal ? matches.push(emit2) : yield emit2), hit = [node2, path2];
  }
  mode === "lowest" && hit && (universal ? matches.push(hit) : yield hit), universal && (yield* matches);
}
const normalize = (editor, options = {}) => {
  const {
    force = !1,
    operation
  } = options, getDirtyPaths2 = (editor2) => DIRTY_PATHS.get(editor2) || [], getDirtyPathKeys = (editor2) => DIRTY_PATH_KEYS.get(editor2) || /* @__PURE__ */ new Set(), popDirtyPath = (editor2) => {
    const path2 = getDirtyPaths2(editor2).pop(), key = path2.join(",");
    return getDirtyPathKeys(editor2).delete(key), path2;
  };
  if (Editor.isNormalizing(editor)) {
    if (force) {
      const allPaths = Array.from(Node$1.nodes(editor), ([, p]) => p), allPathKeys = new Set(allPaths.map((p) => p.join(",")));
      DIRTY_PATHS.set(editor, allPaths), DIRTY_PATH_KEYS.set(editor, allPathKeys);
    }
    getDirtyPaths2(editor).length !== 0 && Editor.withoutNormalizing(editor, () => {
      for (const dirtyPath of getDirtyPaths2(editor))
        if (Node$1.has(editor, dirtyPath)) {
          const entry = Editor.node(editor, dirtyPath), [node2] = entry;
          Element$2.isElement(node2) && node2.children.length === 0 && editor.normalizeNode(entry, {
            operation
          });
        }
      let dirtyPaths = getDirtyPaths2(editor);
      const initialDirtyPathsLength = dirtyPaths.length;
      let iteration = 0;
      for (; dirtyPaths.length !== 0; ) {
        if (!editor.shouldNormalize({
          dirtyPaths,
          iteration,
          initialDirtyPathsLength,
          operation
        }))
          return;
        const dirtyPath = popDirtyPath(editor);
        if (Node$1.has(editor, dirtyPath)) {
          const entry = Editor.node(editor, dirtyPath);
          editor.normalizeNode(entry, {
            operation
          });
        }
        iteration++, dirtyPaths = getDirtyPaths2(editor);
      }
    });
  }
}, parent = (editor, at, options = {}) => {
  const path2 = Editor.path(editor, at, options), parentPath = Path.parent(path2);
  return Editor.node(editor, parentPath);
}, pathRef = (editor, path2, options = {}) => {
  const {
    affinity = "forward"
  } = options, ref = {
    current: path2,
    affinity,
    unref() {
      const {
        current
      } = ref;
      return Editor.pathRefs(editor).delete(ref), ref.current = null, current;
    }
  };
  return Editor.pathRefs(editor).add(ref), ref;
}, pathRefs = (editor) => {
  let refs = PATH_REFS.get(editor);
  return refs || (refs = /* @__PURE__ */ new Set(), PATH_REFS.set(editor, refs)), refs;
}, path = (editor, at, options = {}) => {
  const {
    depth,
    edge
  } = options;
  if (Path.isPath(at)) {
    if (edge === "start") {
      const [, firstPath] = Node$1.first(editor, at);
      at = firstPath;
    } else if (edge === "end") {
      const [, lastPath] = Node$1.last(editor, at);
      at = lastPath;
    }
  }
  return Range.isRange(at) && (edge === "start" ? at = Range.start(at) : edge === "end" ? at = Range.end(at) : at = Path.common(at.anchor.path, at.focus.path)), Point.isPoint(at) && (at = at.path), depth != null && (at = at.slice(0, depth)), at;
}, pointRef = (editor, point2, options = {}) => {
  const {
    affinity = "forward"
  } = options, ref = {
    current: point2,
    affinity,
    unref() {
      const {
        current
      } = ref;
      return Editor.pointRefs(editor).delete(ref), ref.current = null, current;
    }
  };
  return Editor.pointRefs(editor).add(ref), ref;
}, pointRefs = (editor) => {
  let refs = POINT_REFS.get(editor);
  return refs || (refs = /* @__PURE__ */ new Set(), POINT_REFS.set(editor, refs)), refs;
}, point = (editor, at, options = {}) => {
  const {
    edge = "start"
  } = options;
  if (Path.isPath(at)) {
    let path2;
    if (edge === "end") {
      const [, lastPath] = Node$1.last(editor, at);
      path2 = lastPath;
    } else {
      const [, firstPath] = Node$1.first(editor, at);
      path2 = firstPath;
    }
    const node2 = Node$1.get(editor, path2);
    if (!Text$1.isText(node2))
      throw new Error(`Cannot get the ${edge} point in the node at path [${at}] because it has no ${edge} text node.`);
    return {
      path: path2,
      offset: edge === "end" ? node2.text.length : 0
    };
  }
  if (Range.isRange(at)) {
    const [start2, end2] = Range.edges(at);
    return edge === "start" ? start2 : end2;
  }
  return at;
};
function* positions(editor, options = {}) {
  const {
    at = editor.selection,
    unit = "offset",
    reverse = !1,
    voids = !1
  } = options;
  if (!at)
    return;
  const range2 = Editor.range(editor, at), [start2, end2] = Range.edges(range2), first2 = reverse ? end2 : start2;
  let isNewBlock = !1, blockText = "", distance = 0, leafTextRemaining = 0, leafTextOffset = 0;
  const skippedPaths = [];
  for (const [node2, path2] of Editor.nodes(editor, {
    at,
    reverse,
    voids
  })) {
    const hasSkippedAncestor = skippedPaths.some((p) => Path.isAncestor(p, path2));
    function* maybeYield(point2) {
      hasSkippedAncestor || (yield point2);
    }
    if (Element$2.isElement(node2)) {
      if (!editor.isSelectable(node2))
        if (skippedPaths.push(path2), reverse) {
          Path.hasPrevious(path2) && (yield* maybeYield(Editor.end(editor, Path.previous(path2))));
          continue;
        } else {
          const nextPath = Path.next(path2);
          Editor.hasPath(editor, nextPath) && (yield* maybeYield(Editor.start(editor, nextPath)));
          continue;
        }
      if (!voids && (editor.isVoid(node2) || editor.isElementReadOnly(node2))) {
        yield* maybeYield(Editor.start(editor, path2));
        continue;
      }
      if (editor.isInline(node2))
        continue;
      if (Editor.hasInlines(editor, node2)) {
        const e = Path.isAncestor(path2, end2.path) ? end2 : Editor.end(editor, path2), s = Path.isAncestor(path2, start2.path) ? start2 : Editor.start(editor, path2);
        blockText = Editor.string(editor, {
          anchor: s,
          focus: e
        }, {
          voids
        }), isNewBlock = !0;
      }
    }
    if (Text$1.isText(node2)) {
      const isFirst = Path.equals(path2, first2.path);
      for (isFirst ? (leafTextRemaining = reverse ? first2.offset : node2.text.length - first2.offset, leafTextOffset = first2.offset) : (leafTextRemaining = node2.text.length, leafTextOffset = reverse ? leafTextRemaining : 0), (isFirst || isNewBlock || unit === "offset") && (yield* maybeYield({
        path: path2,
        offset: leafTextOffset
      }), isNewBlock = !1); ; ) {
        if (distance === 0) {
          if (blockText === "")
            break;
          distance = calcDistance(blockText, unit, reverse), blockText = splitByCharacterDistance(blockText, distance, reverse)[1];
        }
        if (leafTextOffset = reverse ? leafTextOffset - distance : leafTextOffset + distance, leafTextRemaining = leafTextRemaining - distance, leafTextRemaining < 0) {
          distance = -leafTextRemaining;
          break;
        }
        distance = 0, yield* maybeYield({
          path: path2,
          offset: leafTextOffset
        });
      }
    }
  }
  function calcDistance(text, unit2, reverse2) {
    return unit2 === "character" ? getCharacterDistance(text, reverse2) : unit2 === "word" ? getWordDistance(text, reverse2) : unit2 === "line" || unit2 === "block" ? text.length : 1;
  }
}
const previous = (editor, options = {}) => {
  const {
    mode = "lowest",
    voids = !1
  } = options;
  let {
    match: match2,
    at = editor.selection
  } = options;
  if (!at)
    return;
  const pointBeforeLocation = Editor.before(editor, at, {
    voids
  });
  if (!pointBeforeLocation)
    return;
  const [, to] = Editor.first(editor, []), span = [pointBeforeLocation.path, to];
  if (Path.isPath(at) && at.length === 0)
    throw new Error("Cannot get the previous node from the root node!");
  if (match2 == null)
    if (Path.isPath(at)) {
      const [parent2] = Editor.parent(editor, at);
      match2 = (n2) => parent2.children.includes(n2);
    } else
      match2 = () => !0;
  const [previous2] = Editor.nodes(editor, {
    reverse: !0,
    at: span,
    match: match2,
    mode,
    voids
  });
  return previous2;
}, rangeRef = (editor, range2, options = {}) => {
  const {
    affinity = "forward"
  } = options, ref = {
    current: range2,
    affinity,
    unref() {
      const {
        current
      } = ref;
      return Editor.rangeRefs(editor).delete(ref), ref.current = null, current;
    }
  };
  return Editor.rangeRefs(editor).add(ref), ref;
}, rangeRefs = (editor) => {
  let refs = RANGE_REFS.get(editor);
  return refs || (refs = /* @__PURE__ */ new Set(), RANGE_REFS.set(editor, refs)), refs;
}, range = (editor, at, to) => {
  if (Range.isRange(at) && !to)
    return at;
  const start2 = Editor.start(editor, at), end2 = Editor.end(editor, to || at);
  return {
    anchor: start2,
    focus: end2
  };
}, removeMark = (editor, key) => {
  const {
    selection
  } = editor;
  if (selection) {
    const match2 = (node2, path2) => {
      if (!Text$1.isText(node2))
        return !1;
      const [parentNode] = Editor.parent(editor, path2);
      return !editor.isVoid(parentNode) || editor.markableVoid(parentNode);
    }, expandedSelection = Range.isExpanded(selection);
    let markAcceptingVoidSelected = !1;
    if (!expandedSelection) {
      const [selectedNode, selectedPath] = Editor.node(editor, selection);
      if (selectedNode && match2(selectedNode, selectedPath)) {
        const [parentNode] = Editor.parent(editor, selectedPath);
        markAcceptingVoidSelected = parentNode && editor.markableVoid(parentNode);
      }
    }
    if (expandedSelection || markAcceptingVoidSelected)
      Transforms.unsetNodes(editor, key, {
        match: match2,
        split: !0,
        voids: !0
      });
    else {
      const marks2 = {
        ...Editor.marks(editor) || {}
      };
      delete marks2[key], editor.marks = marks2, FLUSHING.get(editor) || editor.onChange();
    }
  }
}, setNormalizing = (editor, isNormalizing2) => {
  NORMALIZING.set(editor, isNormalizing2);
}, start = (editor, at) => Editor.point(editor, at, {
  edge: "start"
}), string = (editor, at, options = {}) => {
  const {
    voids = !1
  } = options, range2 = Editor.range(editor, at), [start2, end2] = Range.edges(range2);
  let text = "";
  for (const [node2, path2] of Editor.nodes(editor, {
    at: range2,
    match: Text$1.isText,
    voids
  })) {
    let t = node2.text;
    Path.equals(path2, end2.path) && (t = t.slice(0, end2.offset)), Path.equals(path2, start2.path) && (t = t.slice(start2.offset)), text += t;
  }
  return text;
}, unhangRange = (editor, range2, options = {}) => {
  const {
    voids = !1
  } = options;
  let [start2, end2] = Range.edges(range2);
  if (start2.offset !== 0 || end2.offset !== 0 || Range.isCollapsed(range2) || Path.hasPrevious(end2.path))
    return range2;
  const endBlock = Editor.above(editor, {
    at: end2,
    match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2),
    voids
  }), blockPath = endBlock ? endBlock[1] : [], before2 = {
    anchor: Editor.start(editor, start2),
    focus: end2
  };
  let skip = !0;
  for (const [node2, path2] of Editor.nodes(editor, {
    at: before2,
    match: Text$1.isText,
    reverse: !0,
    voids
  })) {
    if (skip) {
      skip = !1;
      continue;
    }
    if (node2.text !== "" || Path.isBefore(path2, blockPath)) {
      end2 = {
        path: path2,
        offset: node2.text.length
      };
      break;
    }
  }
  return {
    anchor: start2,
    focus: end2
  };
}, withoutNormalizing = (editor, fn) => {
  const value = Editor.isNormalizing(editor);
  Editor.setNormalizing(editor, !1);
  try {
    fn();
  } finally {
    Editor.setNormalizing(editor, value);
  }
  Editor.normalize(editor);
}, shouldMergeNodesRemovePrevNode = (editor, [prevNode, prevPath], [_curNode, _curNodePath]) => Element$2.isElement(prevNode) && Editor.isEmpty(editor, prevNode) || Text$1.isText(prevNode) && prevNode.text === "" && prevPath[prevPath.length - 1] !== 0, insertNodes = (editor, nodes2, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      hanging = !1,
      voids = !1,
      mode = "lowest",
      batchDirty = !0
    } = options;
    let {
      at,
      match: match2,
      select: select2
    } = options;
    if (Node$1.isNode(nodes2) && (nodes2 = [nodes2]), nodes2.length === 0)
      return;
    const node2 = nodes2[0];
    if (at || (at = getDefaultInsertLocation(editor), select2 !== !1 && (select2 = !0)), select2 == null && (select2 = !1), Range.isRange(at))
      if (hanging || (at = Editor.unhangRange(editor, at, {
        voids
      })), Range.isCollapsed(at))
        at = at.anchor;
      else {
        const [, end2] = Range.edges(at), pointRef2 = Editor.pointRef(editor, end2);
        Transforms.delete(editor, {
          at
        }), at = pointRef2.unref();
      }
    if (Point.isPoint(at)) {
      match2 == null && (Text$1.isText(node2) ? match2 = (n2) => Text$1.isText(n2) : editor.isInline(node2) ? match2 = (n2) => Text$1.isText(n2) || Editor.isInline(editor, n2) : match2 = (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2));
      const [entry] = Editor.nodes(editor, {
        at: at.path,
        match: match2,
        mode,
        voids
      });
      if (entry) {
        const [, matchPath2] = entry, pathRef2 = Editor.pathRef(editor, matchPath2), isAtEnd = Editor.isEnd(editor, at, matchPath2);
        Transforms.splitNodes(editor, {
          at,
          match: match2,
          mode,
          voids
        });
        const path2 = pathRef2.unref();
        at = isAtEnd ? Path.next(path2) : path2;
      } else
        return;
    }
    const parentPath = Path.parent(at);
    let index = at[at.length - 1];
    if (!(!voids && Editor.void(editor, {
      at: parentPath
    }))) {
      if (batchDirty) {
        const batchedOps = [], newDirtyPaths = Path.levels(parentPath);
        batchDirtyPaths(editor, () => {
          for (const node22 of nodes2) {
            const path2 = parentPath.concat(index);
            index++;
            const op = {
              type: "insert_node",
              path: path2,
              node: node22
            };
            editor.apply(op), at = Path.next(at), batchedOps.push(op), Text$1.isText(node22) ? newDirtyPaths.push(path2) : newDirtyPaths.push(...Array.from(Node$1.nodes(node22), ([, p]) => path2.concat(p)));
          }
        }, () => {
          updateDirtyPaths(editor, newDirtyPaths, (p) => {
            let newPath = p;
            for (const op of batchedOps)
              if (Path.operationCanTransformPath(op) && (newPath = Path.transform(newPath, op), !newPath))
                return null;
            return newPath;
          });
        });
      } else
        for (const node22 of nodes2) {
          const path2 = parentPath.concat(index);
          index++, editor.apply({
            type: "insert_node",
            path: path2,
            node: node22
          }), at = Path.next(at);
        }
      if (at = Path.previous(at), select2) {
        const point2 = Editor.end(editor, at);
        point2 && Transforms.select(editor, point2);
      }
    }
  });
}, liftNodes = (editor, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      at = editor.selection,
      mode = "lowest",
      voids = !1
    } = options;
    let {
      match: match2
    } = options;
    if (match2 == null && (match2 = Path.isPath(at) ? matchPath(editor, at) : (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)), !at)
      return;
    const matches = Editor.nodes(editor, {
      at,
      match: match2,
      mode,
      voids
    }), pathRefs2 = Array.from(matches, ([, p]) => Editor.pathRef(editor, p));
    for (const pathRef2 of pathRefs2) {
      const path2 = pathRef2.unref();
      if (path2.length < 2)
        throw new Error(`Cannot lift node at a path [${path2}] because it has a depth of less than \`2\`.`);
      const parentNodeEntry = Editor.node(editor, Path.parent(path2)), [parent2, parentPath] = parentNodeEntry, index = path2[path2.length - 1], {
        length
      } = parent2.children;
      if (length === 1) {
        const toPath = Path.next(parentPath);
        Transforms.moveNodes(editor, {
          at: path2,
          to: toPath,
          voids
        }), Transforms.removeNodes(editor, {
          at: parentPath,
          voids
        });
      } else if (index === 0)
        Transforms.moveNodes(editor, {
          at: path2,
          to: parentPath,
          voids
        });
      else if (index === length - 1) {
        const toPath = Path.next(parentPath);
        Transforms.moveNodes(editor, {
          at: path2,
          to: toPath,
          voids
        });
      } else {
        const splitPath = Path.next(path2), toPath = Path.next(parentPath);
        Transforms.splitNodes(editor, {
          at: splitPath,
          voids
        }), Transforms.moveNodes(editor, {
          at: path2,
          to: toPath,
          voids
        });
      }
    }
  });
}, hasSingleChildNest = (editor, node2) => {
  if (Element$2.isElement(node2)) {
    const element = node2;
    return Editor.isVoid(editor, node2) ? !0 : element.children.length === 1 ? hasSingleChildNest(editor, element.children[0]) : !1;
  } else return !Editor.isEditor(node2);
}, mergeNodes = (editor, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    let {
      match: match2,
      at = editor.selection
    } = options;
    const {
      hanging = !1,
      voids = !1,
      mode = "lowest"
    } = options;
    if (!at)
      return;
    if (match2 == null)
      if (Path.isPath(at)) {
        const [parent2] = Editor.parent(editor, at);
        match2 = (n2) => parent2.children.includes(n2);
      } else
        match2 = (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2);
    if (!hanging && Range.isRange(at) && (at = Editor.unhangRange(editor, at, {
      voids
    })), Range.isRange(at))
      if (Range.isCollapsed(at))
        at = at.anchor;
      else {
        const [, end2] = Range.edges(at), pointRef2 = Editor.pointRef(editor, end2);
        Transforms.delete(editor, {
          at
        }), at = pointRef2.unref(), options.at == null && Transforms.select(editor, at);
      }
    const [current] = Editor.nodes(editor, {
      at,
      match: match2,
      voids,
      mode
    }), prev = Editor.previous(editor, {
      at,
      match: match2,
      voids,
      mode
    });
    if (!current || !prev)
      return;
    const [node2, path2] = current, [prevNode, prevPath] = prev;
    if (path2.length === 0 || prevPath.length === 0)
      return;
    const newPath = Path.next(prevPath), commonPath = Path.common(path2, prevPath), isPreviousSibling = Path.isSibling(path2, prevPath), levels2 = Array.from(Editor.levels(editor, {
      at: path2
    }), ([n2]) => n2).slice(commonPath.length).slice(0, -1), emptyAncestor = Editor.above(editor, {
      at: path2,
      mode: "highest",
      match: (n2) => levels2.includes(n2) && hasSingleChildNest(editor, n2)
    }), emptyRef = emptyAncestor && Editor.pathRef(editor, emptyAncestor[1]);
    let properties, position;
    if (Text$1.isText(node2) && Text$1.isText(prevNode)) {
      const {
        text: _text,
        ...rest
      } = node2;
      position = prevNode.text.length, properties = rest;
    } else if (Element$2.isElement(node2) && Element$2.isElement(prevNode)) {
      const {
        children: _children,
        ...rest
      } = node2;
      position = prevNode.children.length, properties = rest;
    } else
      throw new Error(`Cannot merge the node at path [${path2}] with the previous sibling because it is not the same kind: ${Scrubber.stringify(node2)} ${Scrubber.stringify(prevNode)}`);
    isPreviousSibling || Transforms.moveNodes(editor, {
      at: path2,
      to: newPath,
      voids
    }), emptyRef && Transforms.removeNodes(editor, {
      at: emptyRef.current,
      voids
    }), Editor.shouldMergeNodesRemovePrevNode(editor, prev, current) ? Transforms.removeNodes(editor, {
      at: prevPath,
      voids
    }) : editor.apply({
      type: "merge_node",
      path: newPath,
      position,
      properties
    }), emptyRef && emptyRef.unref();
  });
}, moveNodes = (editor, options) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      to,
      at = editor.selection,
      mode = "lowest",
      voids = !1
    } = options;
    let {
      match: match2
    } = options;
    if (!at)
      return;
    match2 == null && (match2 = Path.isPath(at) ? matchPath(editor, at) : (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2));
    const toRef = Editor.pathRef(editor, to), targets = Editor.nodes(editor, {
      at,
      match: match2,
      mode,
      voids
    }), pathRefs2 = Array.from(targets, ([, p]) => Editor.pathRef(editor, p));
    for (const pathRef2 of pathRefs2) {
      const path2 = pathRef2.unref(), newPath = toRef.current;
      path2.length !== 0 && editor.apply({
        type: "move_node",
        path: path2,
        newPath
      }), toRef.current && Path.isSibling(newPath, path2) && Path.isAfter(newPath, path2) && (toRef.current = Path.next(toRef.current));
    }
    toRef.unref();
  });
}, removeNodes = (editor, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      hanging = !1,
      voids = !1,
      mode = "lowest"
    } = options;
    let {
      at = editor.selection,
      match: match2
    } = options;
    if (!at)
      return;
    match2 == null && (match2 = Path.isPath(at) ? matchPath(editor, at) : (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)), !hanging && Range.isRange(at) && (at = Editor.unhangRange(editor, at, {
      voids
    }));
    const depths = Editor.nodes(editor, {
      at,
      match: match2,
      mode,
      voids
    }), pathRefs2 = Array.from(depths, ([, p]) => Editor.pathRef(editor, p));
    for (const pathRef2 of pathRefs2) {
      const path2 = pathRef2.unref();
      if (path2) {
        const [node2] = Editor.node(editor, path2);
        editor.apply({
          type: "remove_node",
          path: path2,
          node: node2
        });
      }
    }
  });
}, setNodes = (editor, props, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    let {
      match: match2,
      at = editor.selection,
      compare,
      merge
    } = options;
    const {
      hanging = !1,
      mode = "lowest",
      split = !1,
      voids = !1
    } = options;
    if (at) {
      if (match2 == null && (match2 = Path.isPath(at) ? matchPath(editor, at) : (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)), !hanging && Range.isRange(at) && (at = Editor.unhangRange(editor, at, {
        voids
      })), split && Range.isRange(at)) {
        if (Range.isCollapsed(at) && Editor.leaf(editor, at.anchor)[0].text.length > 0)
          return;
        const rangeRef2 = Editor.rangeRef(editor, at, {
          affinity: "inward"
        }), [start2, end2] = Range.edges(at), splitMode = mode === "lowest" ? "lowest" : "highest", endAtEndOfNode = Editor.isEnd(editor, end2, end2.path);
        Transforms.splitNodes(editor, {
          at: end2,
          match: match2,
          mode: splitMode,
          voids,
          always: !endAtEndOfNode
        });
        const startAtStartOfNode = Editor.isStart(editor, start2, start2.path);
        Transforms.splitNodes(editor, {
          at: start2,
          match: match2,
          mode: splitMode,
          voids,
          always: !startAtStartOfNode
        }), at = rangeRef2.unref(), options.at == null && Transforms.select(editor, at);
      }
      compare || (compare = (prop, nodeProp) => prop !== nodeProp);
      for (const [node2, path2] of Editor.nodes(editor, {
        at,
        match: match2,
        mode,
        voids
      })) {
        const properties = {}, newProperties = {};
        if (path2.length === 0)
          continue;
        let hasChanges = !1;
        for (const k in props)
          k === "children" || k === "text" || compare(props[k], node2[k]) && (hasChanges = !0, node2.hasOwnProperty(k) && (properties[k] = node2[k]), merge ? props[k] != null && (newProperties[k] = merge(node2[k], props[k])) : props[k] != null && (newProperties[k] = props[k]));
        hasChanges && editor.apply({
          type: "set_node",
          path: path2,
          properties,
          newProperties
        });
      }
    }
  });
}, deleteRange = (editor, range2) => {
  if (Range.isCollapsed(range2))
    return range2.anchor;
  {
    const [, end2] = Range.edges(range2), pointRef2 = Editor.pointRef(editor, end2);
    return Transforms.delete(editor, {
      at: range2
    }), pointRef2.unref();
  }
}, splitNodes = (editor, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      mode = "lowest",
      voids = !1
    } = options;
    let {
      match: match2,
      at = editor.selection,
      height = 0,
      always = !1
    } = options;
    if (match2 == null && (match2 = (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)), Range.isRange(at) && (at = deleteRange(editor, at)), Path.isPath(at)) {
      const path2 = at, point2 = Editor.point(editor, path2), [parent2] = Editor.parent(editor, path2);
      match2 = (n2) => n2 === parent2, height = point2.path.length - path2.length + 1, at = point2, always = !0;
    }
    if (!at)
      return;
    const beforeRef = Editor.pointRef(editor, at, {
      affinity: "backward"
    });
    let afterRef;
    try {
      const [highest] = Editor.nodes(editor, {
        at,
        match: match2,
        mode,
        voids
      });
      if (!highest)
        return;
      const voidMatch = Editor.void(editor, {
        at,
        mode: "highest"
      }), nudge = 0;
      if (!voids && voidMatch) {
        const [voidNode, voidPath] = voidMatch;
        if (Element$2.isElement(voidNode) && editor.isInline(voidNode)) {
          let after2 = Editor.after(editor, voidPath);
          if (!after2) {
            const text = editor.createSpan(), afterPath = Path.next(voidPath);
            Transforms.insertNodes(editor, text, {
              at: afterPath,
              voids
            }), after2 = Editor.point(editor, afterPath);
          }
          at = after2, always = !0;
        }
        height = at.path.length - voidPath.length + 1, always = !0;
      }
      afterRef = Editor.pointRef(editor, at);
      const depth = at.path.length - height, [, highestPath] = highest, lowestPath = at.path.slice(0, depth);
      let position = height === 0 ? at.offset : at.path[depth] + nudge;
      for (const [node2, path2] of Editor.levels(editor, {
        at: lowestPath,
        reverse: !0,
        voids
      })) {
        let split = !1;
        if (path2.length < highestPath.length || path2.length === 0 || !voids && Element$2.isElement(node2) && Editor.isVoid(editor, node2))
          break;
        const point2 = beforeRef.current, isEnd2 = Editor.isEnd(editor, point2, path2);
        if (always || !beforeRef || !Editor.isEdge(editor, point2, path2)) {
          split = !0;
          const properties = Node$1.extractProps(node2);
          editor.apply({
            type: "split_node",
            path: path2,
            position,
            properties
          });
        }
        position = path2[path2.length - 1] + (split || isEnd2 ? 1 : 0);
      }
      if (options.at == null) {
        const point2 = afterRef.current || Editor.end(editor, []);
        Transforms.select(editor, point2);
      }
    } finally {
      beforeRef.unref(), afterRef?.unref();
    }
  });
}, unsetNodes = (editor, props, options = {}) => {
  Array.isArray(props) || (props = [props]);
  const obj = {};
  for (const key of props)
    obj[key] = null;
  Transforms.setNodes(editor, obj, options);
}, unwrapNodes = (editor, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      mode = "lowest",
      split = !1,
      voids = !1
    } = options;
    let {
      at = editor.selection,
      match: match2
    } = options;
    if (!at)
      return;
    match2 == null && (match2 = Path.isPath(at) ? matchPath(editor, at) : (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)), Path.isPath(at) && (at = Editor.range(editor, at));
    const rangeRef2 = Range.isRange(at) ? Editor.rangeRef(editor, at) : null, matches = Editor.nodes(editor, {
      at,
      match: match2,
      mode,
      voids
    }), pathRefs2 = Array.from(
      matches,
      ([, p]) => Editor.pathRef(editor, p)
      // unwrapNode will call liftNode which does not support splitting the node when nested.
      // If we do not reverse the order and call it from top to the bottom, it will remove all blocks
      // that wrap target node. So we reverse the order.
    ).reverse();
    for (const pathRef2 of pathRefs2) {
      const path2 = pathRef2.unref(), [node2] = Editor.node(editor, path2);
      let range2 = Editor.range(editor, path2);
      split && rangeRef2 && (range2 = Range.intersection(rangeRef2.current, range2)), Transforms.liftNodes(editor, {
        at: range2,
        match: (n2) => Element$2.isAncestor(node2) && node2.children.includes(n2),
        voids
      });
    }
    rangeRef2 && rangeRef2.unref();
  });
}, wrapNodes = (editor, element, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      mode = "lowest",
      split = !1,
      voids = !1
    } = options;
    let {
      match: match2,
      at = editor.selection
    } = options;
    if (!at)
      return;
    if (match2 == null && (Path.isPath(at) ? match2 = matchPath(editor, at) : editor.isInline(element) ? match2 = (n2) => Element$2.isElement(n2) && Editor.isInline(editor, n2) || Text$1.isText(n2) : match2 = (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)), split && Range.isRange(at)) {
      const [start2, end2] = Range.edges(at), rangeRef2 = Editor.rangeRef(editor, at, {
        affinity: "inward"
      }), isAtBlockEdge = (point2) => {
        const blockAbove = Editor.above(editor, {
          at: point2,
          match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)
        });
        return blockAbove && Editor.isEdge(editor, point2, blockAbove[1]);
      };
      Transforms.splitNodes(editor, {
        at: end2,
        match: match2,
        voids,
        always: !isAtBlockEdge(end2)
      }), Transforms.splitNodes(editor, {
        at: start2,
        match: match2,
        voids,
        always: !isAtBlockEdge(start2)
      }), at = rangeRef2.unref(), options.at == null && Transforms.select(editor, at);
    }
    const roots = Array.from(Editor.nodes(editor, {
      at,
      match: editor.isInline(element) ? (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2) : (n2) => Editor.isEditor(n2),
      mode: "lowest",
      voids
    }));
    for (const [, rootPath] of roots) {
      const a = Range.isRange(at) ? Range.intersection(at, Editor.range(editor, rootPath)) : at;
      if (!a)
        continue;
      const matches = Array.from(Editor.nodes(editor, {
        at: a,
        match: match2,
        mode,
        voids
      }));
      if (matches.length > 0) {
        const first2 = matches[0], last2 = matches[matches.length - 1], [, firstPath] = first2, [, lastPath] = last2;
        if (firstPath.length === 0 && lastPath.length === 0)
          continue;
        const commonPath = Path.equals(firstPath, lastPath) ? Path.parent(firstPath) : Path.common(firstPath, lastPath), range2 = Editor.range(editor, firstPath, lastPath), commonNodeEntry = Editor.node(editor, commonPath), [commonNode] = commonNodeEntry, depth = commonPath.length + 1, wrapperPath = Path.next(lastPath.slice(0, depth)), wrapper = {
          ...element,
          children: []
        };
        Transforms.insertNodes(editor, wrapper, {
          at: wrapperPath,
          voids
        }), Transforms.moveNodes(editor, {
          at: range2,
          match: (n2) => Element$2.isAncestor(commonNode) && commonNode.children.includes(n2),
          to: wrapperPath.concat(0),
          voids
        });
      }
    }
  });
}, collapse = (editor, options = {}) => {
  const {
    edge = "anchor"
  } = options, {
    selection
  } = editor;
  if (selection) {
    if (edge === "anchor")
      Transforms.select(editor, selection.anchor);
    else if (edge === "focus")
      Transforms.select(editor, selection.focus);
    else if (edge === "start") {
      const [start2] = Range.edges(selection);
      Transforms.select(editor, start2);
    } else if (edge === "end") {
      const [, end2] = Range.edges(selection);
      Transforms.select(editor, end2);
    }
  } else return;
}, deselect = (editor) => {
  const {
    selection
  } = editor;
  selection && editor.apply({
    type: "set_selection",
    properties: selection,
    newProperties: null
  });
}, move = (editor, options = {}) => {
  const {
    selection
  } = editor, {
    distance = 1,
    unit = "character",
    reverse = !1
  } = options;
  let {
    edge = null
  } = options;
  if (!selection)
    return;
  edge === "start" && (edge = Range.isBackward(selection) ? "focus" : "anchor"), edge === "end" && (edge = Range.isBackward(selection) ? "anchor" : "focus");
  const {
    anchor,
    focus
  } = selection, opts = {
    distance,
    unit
  }, props = {};
  if (edge == null || edge === "anchor") {
    const point2 = reverse ? Editor.before(editor, anchor, opts) : Editor.after(editor, anchor, opts);
    point2 && (props.anchor = point2);
  }
  if (edge == null || edge === "focus") {
    const point2 = reverse ? Editor.before(editor, focus, opts) : Editor.after(editor, focus, opts);
    point2 && (props.focus = point2);
  }
  Transforms.setSelection(editor, props);
}, select = (editor, target) => {
  const {
    selection
  } = editor;
  if (target = Editor.range(editor, target), selection) {
    Transforms.setSelection(editor, target);
    return;
  }
  if (!Range.isRange(target))
    throw new Error(`When setting the selection and the current selection is \`null\` you must provide at least an \`anchor\` and \`focus\`, but you passed: ${Scrubber.stringify(target)}`);
  editor.apply({
    type: "set_selection",
    properties: selection,
    newProperties: target
  });
}, setPoint = (editor, props, options = {}) => {
  const {
    selection
  } = editor;
  let {
    edge = "both"
  } = options;
  if (!selection)
    return;
  edge === "start" && (edge = Range.isBackward(selection) ? "focus" : "anchor"), edge === "end" && (edge = Range.isBackward(selection) ? "anchor" : "focus");
  const {
    anchor,
    focus
  } = selection, point2 = edge === "anchor" ? anchor : focus;
  Transforms.setSelection(editor, {
    [edge === "anchor" ? "anchor" : "focus"]: {
      ...point2,
      ...props
    }
  });
}, setSelection$1 = (editor, props) => {
  const {
    selection
  } = editor, oldProps = {}, newProps = {};
  if (selection) {
    for (const k in props)
      (k === "anchor" && props.anchor != null && !Point.equals(props.anchor, selection.anchor) || k === "focus" && props.focus != null && !Point.equals(props.focus, selection.focus) || k !== "anchor" && k !== "focus" && props[k] !== selection[k]) && (oldProps[k] = selection[k], newProps[k] = props[k]);
    Object.keys(oldProps).length > 0 && editor.apply({
      type: "set_selection",
      properties: oldProps,
      newProperties: newProps
    });
  }
}, deleteText = (editor, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      reverse = !1,
      unit = "character",
      distance = 1,
      voids = !1
    } = options;
    let {
      at = editor.selection,
      hanging = !1
    } = options;
    if (!at)
      return;
    let isCollapsed = !1;
    if (Range.isRange(at) && Range.isCollapsed(at) && (isCollapsed = !0, at = at.anchor), Point.isPoint(at)) {
      const furthestVoid = Editor.void(editor, {
        at,
        mode: "highest"
      });
      if (!voids && furthestVoid) {
        const [, voidPath] = furthestVoid;
        at = voidPath;
      } else {
        const opts = {
          unit,
          distance
        }, target = reverse ? Editor.before(editor, at, opts) || Editor.start(editor, []) : Editor.after(editor, at, opts) || Editor.end(editor, []);
        at = {
          anchor: at,
          focus: target
        }, hanging = !0;
      }
    }
    if (Path.isPath(at)) {
      Transforms.removeNodes(editor, {
        at,
        voids
      });
      return;
    }
    if (Range.isCollapsed(at))
      return;
    if (!hanging) {
      const [, end22] = Range.edges(at), endOfDoc = Editor.end(editor, []);
      Point.equals(end22, endOfDoc) || (at = Editor.unhangRange(editor, at, {
        voids
      }));
    }
    let [start2, end2] = Range.edges(at);
    const startBlock = Editor.above(editor, {
      match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2),
      at: start2,
      voids
    }), endBlock = Editor.above(editor, {
      match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2),
      at: end2,
      voids
    }), isAcrossBlocks = startBlock && endBlock && !Path.equals(startBlock[1], endBlock[1]), isSingleText = Path.equals(start2.path, end2.path), startNonEditable = voids ? null : Editor.void(editor, {
      at: start2,
      mode: "highest"
    }) ?? Editor.elementReadOnly(editor, {
      at: start2,
      mode: "highest"
    }), endNonEditable = voids ? null : Editor.void(editor, {
      at: end2,
      mode: "highest"
    }) ?? Editor.elementReadOnly(editor, {
      at: end2,
      mode: "highest"
    });
    if (startNonEditable) {
      const before2 = Editor.before(editor, start2);
      before2 && startBlock && Path.isAncestor(startBlock[1], before2.path) && (start2 = before2);
    }
    if (endNonEditable) {
      const after2 = Editor.after(editor, end2);
      after2 && endBlock && Path.isAncestor(endBlock[1], after2.path) && (end2 = after2);
    }
    const matches = [];
    let lastPath;
    for (const entry of Editor.nodes(editor, {
      at,
      voids
    })) {
      const [node2, path2] = entry;
      lastPath && Path.compare(path2, lastPath) === 0 || (!voids && Element$2.isElement(node2) && (Editor.isVoid(editor, node2) || Editor.isElementReadOnly(editor, node2)) || !Path.isCommon(path2, start2.path) && !Path.isCommon(path2, end2.path)) && (matches.push(entry), lastPath = path2);
    }
    const pathRefs2 = Array.from(matches, ([, p]) => Editor.pathRef(editor, p)), startRef = Editor.pointRef(editor, start2), endRef = Editor.pointRef(editor, end2);
    let removedText = "";
    if (!isSingleText && !startNonEditable) {
      const point22 = startRef.current, [node2] = Editor.leaf(editor, point22), {
        path: path2
      } = point22, {
        offset
      } = start2, text = node2.text.slice(offset);
      text.length > 0 && (editor.apply({
        type: "remove_text",
        path: path2,
        offset,
        text
      }), removedText = text);
    }
    if (pathRefs2.reverse().map((r) => r.unref()).filter((r) => r !== null).forEach((p) => {
      Transforms.removeNodes(editor, {
        at: p,
        voids
      });
    }), !endNonEditable) {
      const point22 = endRef.current, [node2] = Editor.leaf(editor, point22), {
        path: path2
      } = point22, offset = isSingleText ? start2.offset : 0, text = node2.text.slice(offset, end2.offset);
      text.length > 0 && (editor.apply({
        type: "remove_text",
        path: path2,
        offset,
        text
      }), removedText = text);
    }
    !isSingleText && isAcrossBlocks && endRef.current && startRef.current && Transforms.mergeNodes(editor, {
      at: endRef.current,
      hanging: !0,
      voids
    }), isCollapsed && reverse && unit === "character" && removedText.length > 1 && removedText.match(/[\u0980-\u09FF\u0E00-\u0E7F\u1000-\u109F\u0900-\u097F\u1780-\u17FF\u0D00-\u0D7F\u0B00-\u0B7F\u0A00-\u0A7F\u0B80-\u0BFF\u0C00-\u0C7F]+/) && Transforms.insertText(editor, removedText.slice(0, removedText.length - distance));
    const startUnref = startRef.unref(), endUnref = endRef.unref(), point2 = reverse ? startUnref || endUnref : endUnref || startUnref;
    options.at == null && point2 && Transforms.select(editor, point2);
  });
}, insertFragment = (editor, fragment2, options = {}) => {
  Editor.withoutNormalizing(editor, () => {
    const {
      hanging = !1,
      voids = !1
    } = options;
    let {
      at = getDefaultInsertLocation(editor),
      batchDirty = !0
    } = options;
    if (!fragment2.length)
      return;
    if (Range.isRange(at))
      if (hanging || (at = Editor.unhangRange(editor, at, {
        voids
      })), Range.isCollapsed(at))
        at = at.anchor;
      else {
        const [, end2] = Range.edges(at);
        if (!voids && Editor.void(editor, {
          at: end2
        }))
          return;
        const pointRef2 = Editor.pointRef(editor, end2);
        Transforms.delete(editor, {
          at
        }), at = pointRef2.unref();
      }
    else Path.isPath(at) && (at = Editor.start(editor, at));
    if (!voids && Editor.void(editor, {
      at
    }))
      return;
    const inlineElementMatch = Editor.above(editor, {
      at,
      match: (n2) => Element$2.isElement(n2) && Editor.isInline(editor, n2),
      mode: "highest",
      voids
    });
    if (inlineElementMatch) {
      const [, inlinePath2] = inlineElementMatch;
      Editor.isEnd(editor, at, inlinePath2) ? at = Editor.after(editor, inlinePath2) : Editor.isStart(editor, at, inlinePath2) && (at = Editor.before(editor, inlinePath2));
    }
    const blockMatch = Editor.above(editor, {
      match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2),
      at,
      voids
    }), [, blockPath] = blockMatch, isBlockStart = Editor.isStart(editor, at, blockPath), isBlockEnd = Editor.isEnd(editor, at, blockPath), isBlockEmpty = isBlockStart && isBlockEnd, [, firstLeafPath] = Node$1.first({
      children: fragment2
    }, []), [, lastLeafPath] = Node$1.last({
      children: fragment2
    }, []), shouldInsert = ([n2, p]) => p.length === 0 ? !1 : isBlockEmpty ? !0 : !(!isBlockStart && Path.isAncestor(p, firstLeafPath) && Element$2.isElement(n2) && !editor.isVoid(n2) && !editor.isInline(n2) || !isBlockEnd && Path.isAncestor(p, lastLeafPath) && Element$2.isElement(n2) && !editor.isVoid(n2) && !editor.isInline(n2));
    let starting = !0;
    const starts = [], middles = [], ends = [];
    for (const entry of Node$1.nodes({
      children: fragment2
    }, {
      pass: shouldInsert
    })) {
      const [node2, path2] = entry;
      starting && Element$2.isElement(node2) && !editor.isInline(node2) && !Path.isAncestor(path2, firstLeafPath) && (starting = !1), shouldInsert(entry) && (Element$2.isElement(node2) && !editor.isInline(node2) ? (starting = !1, middles.push(node2)) : starting ? starts.push(node2) : ends.push(node2));
    }
    const inlineMatch = Array.from(Editor.nodes(editor, {
      at,
      match: (n2) => Text$1.isText(n2) || Editor.isInline(editor, n2),
      mode: "highest",
      voids
    }))[0], [, inlinePath] = inlineMatch, isInlineStart = Editor.isStart(editor, at, inlinePath), isInlineEnd = Editor.isEnd(editor, at, inlinePath), middleRef = Editor.pathRef(editor, isBlockEnd && !ends.length ? Path.next(blockPath) : blockPath), endRef = Editor.pathRef(editor, isInlineEnd ? Path.next(inlinePath) : inlinePath), splitBlock = ends.length > 0;
    Transforms.splitNodes(editor, {
      at,
      match: (n2) => splitBlock ? Element$2.isElement(n2) && Editor.isBlock(editor, n2) : Text$1.isText(n2) || Editor.isInline(editor, n2),
      mode: splitBlock ? "lowest" : "highest",
      always: splitBlock && (!isBlockStart || starts.length > 0) && (!isBlockEnd || ends.length > 0),
      voids
    });
    const startRef = Editor.pathRef(editor, !isInlineStart || isInlineStart && isInlineEnd ? Path.next(inlinePath) : inlinePath);
    if (Transforms.insertNodes(editor, starts, {
      at: startRef.current,
      match: (n2) => Text$1.isText(n2) || Editor.isInline(editor, n2),
      mode: "highest",
      voids,
      batchDirty
    }), isBlockEmpty && !starts.length && middles.length && !ends.length && Transforms.delete(editor, {
      at: blockPath,
      voids
    }), Transforms.insertNodes(editor, middles, {
      at: middleRef.current,
      match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2),
      mode: "lowest",
      voids,
      batchDirty
    }), Transforms.insertNodes(editor, ends, {
      at: endRef.current,
      match: (n2) => Text$1.isText(n2) || Editor.isInline(editor, n2),
      mode: "highest",
      voids,
      batchDirty
    }), !options.at) {
      let path2;
      if (ends.length > 0 && endRef.current ? path2 = Path.previous(endRef.current) : middles.length > 0 && middleRef.current ? path2 = Path.previous(middleRef.current) : startRef.current && (path2 = Path.previous(startRef.current)), path2) {
        const end2 = Editor.end(editor, path2);
        Transforms.select(editor, end2);
      }
    }
    startRef.unref(), middleRef.unref(), endRef.unref();
  });
}, createEditor = (context) => {
  const e = {
    children: [],
    operations: [],
    selection: null,
    marks: null,
    createSpan: () => ({
      _type: context.schema.span.name,
      _key: context.keyGenerator(),
      text: "",
      marks: []
    }),
    isElementReadOnly: () => !1,
    isInline: () => !1,
    isSelectable: () => !0,
    isVoid: () => !1,
    markableVoid: () => !1,
    onChange: () => {
    },
    // Core
    apply: (...args) => apply$1(e, ...args),
    // Editor
    addMark: (...args) => addMark(e, ...args),
    deleteBackward: (...args) => deleteBackward(e, ...args),
    deleteForward: (...args) => deleteForward(e, ...args),
    deleteFragment: (...args) => deleteFragment(e, ...args),
    getFragment: (...args) => getFragment(e, ...args),
    insertBreak: (...args) => insertBreak(e, ...args),
    insertSoftBreak: (...args) => insertSoftBreak(e, ...args),
    insertFragment: (...args) => insertFragment(e, ...args),
    insertNode: (...args) => insertNode(e, ...args),
    insertText: (...args) => insertText(e, ...args),
    normalizeNode: (...args) => normalizeNode(e, ...args),
    removeMark: (...args) => removeMark(e, ...args),
    getDirtyPaths: (...args) => getDirtyPaths(e, ...args),
    shouldNormalize: (...args) => shouldNormalize(e, ...args),
    // Editor interface
    above: (...args) => above(e, ...args),
    after: (...args) => after(e, ...args),
    before: (...args) => before(e, ...args),
    collapse: (...args) => collapse(e, ...args),
    delete: (...args) => deleteText(e, ...args),
    deselect: (...args) => deselect(e, ...args),
    edges: (...args) => edges(e, ...args),
    elementReadOnly: (...args) => elementReadOnly(e, ...args),
    end: (...args) => end(e, ...args),
    first: (...args) => first(e, ...args),
    fragment: (...args) => fragment(e, ...args),
    getMarks: (...args) => marks(e, ...args),
    hasBlocks: (...args) => hasBlocks(e, ...args),
    hasInlines: (...args) => hasInlines(e, ...args),
    hasPath: (...args) => hasPath(e, ...args),
    hasTexts: (...args) => hasTexts(e, ...args),
    insertNodes: (...args) => insertNodes(e, ...args),
    isBlock: (...args) => isBlock(e, ...args),
    isEdge: (...args) => isEdge(e, ...args),
    isEmpty: (...args) => isEmpty(e, ...args),
    isEnd: (...args) => isEnd(e, ...args),
    isNormalizing: (...args) => isNormalizing(e, ...args),
    isStart: (...args) => isStart(e, ...args),
    last: (...args) => last(e, ...args),
    leaf: (...args) => leaf(e, ...args),
    levels: (...args) => levels(e, ...args),
    liftNodes: (...args) => liftNodes(e, ...args),
    mergeNodes: (...args) => mergeNodes(e, ...args),
    move: (...args) => move(e, ...args),
    moveNodes: (...args) => moveNodes(e, ...args),
    next: (...args) => next(e, ...args),
    node: (...args) => node(e, ...args),
    nodes: (...args) => nodes(e, ...args),
    normalize: (...args) => normalize(e, ...args),
    parent: (...args) => parent(e, ...args),
    path: (...args) => path(e, ...args),
    pathRef: (...args) => pathRef(e, ...args),
    pathRefs: (...args) => pathRefs(e, ...args),
    point: (...args) => point(e, ...args),
    pointRef: (...args) => pointRef(e, ...args),
    pointRefs: (...args) => pointRefs(e, ...args),
    positions: (...args) => positions(e, ...args),
    previous: (...args) => previous(e, ...args),
    range: (...args) => range(e, ...args),
    rangeRef: (...args) => rangeRef(e, ...args),
    rangeRefs: (...args) => rangeRefs(e, ...args),
    removeNodes: (...args) => removeNodes(e, ...args),
    select: (...args) => select(e, ...args),
    setNodes: (...args) => setNodes(e, ...args),
    setNormalizing: (...args) => setNormalizing(e, ...args),
    setPoint: (...args) => setPoint(e, ...args),
    setSelection: (...args) => setSelection$1(e, ...args),
    splitNodes: (...args) => splitNodes(e, ...args),
    start: (...args) => start(e, ...args),
    string: (...args) => string(e, ...args),
    unhangRange: (...args) => unhangRange(e, ...args),
    unsetNodes: (...args) => unsetNodes(e, ...args),
    unwrapNodes: (...args) => unwrapNodes(e, ...args),
    void: (...args) => getVoid(e, ...args),
    withoutNormalizing: (...args) => withoutNormalizing(e, ...args),
    wrapNodes: (...args) => wrapNodes(e, ...args),
    shouldMergeNodesRemovePrevNode: (...args) => shouldMergeNodesRemovePrevNode(e, ...args)
  };
  return e;
}, DOMText = globalThis.Text, getDefaultView = (value) => value && value.ownerDocument && value.ownerDocument.defaultView || null, isDOMComment = (value) => isDOMNode(value) && value.nodeType === 8, isDOMElement = (value) => isDOMNode(value) && value.nodeType === 1, isDOMNode = (value) => {
  const window2 = getDefaultView(value);
  return !!window2 && value instanceof window2.Node;
}, isDOMSelection = (value) => {
  const window2 = value && value.anchorNode && getDefaultView(value.anchorNode);
  return !!window2 && value instanceof window2.Selection;
}, isDOMText = (value) => isDOMNode(value) && value.nodeType === 3, isPlainTextOnlyPaste = (event) => event.clipboardData && event.clipboardData.getData("text/plain") !== "" && event.clipboardData.types.length === 1, normalizeDOMPoint = (domPoint) => {
  let [node2, offset] = domPoint;
  if (isDOMElement(node2) && node2.childNodes.length) {
    let isLast = offset === node2.childNodes.length, index = isLast ? offset - 1 : offset;
    for ([node2, index] = getEditableChildAndIndex(node2, index, isLast ? "backward" : "forward"), isLast = index < offset; isDOMElement(node2) && node2.childNodes.length; ) {
      const i = isLast ? node2.childNodes.length - 1 : 0;
      node2 = getEditableChild(node2, i, isLast ? "backward" : "forward");
    }
    offset = isLast && node2.textContent != null ? node2.textContent.length : 0;
  }
  return [node2, offset];
}, hasShadowRoot = (node2) => {
  let parent2 = node2 && node2.parentNode;
  for (; parent2; ) {
    if (parent2.toString() === "[object ShadowRoot]")
      return !0;
    parent2 = parent2.parentNode;
  }
  return !1;
}, getEditableChildAndIndex = (parent2, index, direction) => {
  const {
    childNodes
  } = parent2;
  let child = childNodes[index], i = index, triedForward = !1, triedBackward = !1;
  for (; (isDOMComment(child) || isDOMElement(child) && child.childNodes.length === 0 || isDOMElement(child) && child.getAttribute("contenteditable") === "false") && !(triedForward && triedBackward); ) {
    if (i >= childNodes.length) {
      triedForward = !0, i = index - 1, direction = "backward";
      continue;
    }
    if (i < 0) {
      triedBackward = !0, i = index + 1, direction = "forward";
      continue;
    }
    child = childNodes[i], index = i, i += direction === "forward" ? 1 : -1;
  }
  return [child, index];
}, getEditableChild = (parent2, index, direction) => {
  const [child] = getEditableChildAndIndex(parent2, index, direction);
  return child;
}, getPlainText = (domNode) => {
  let text = "";
  if (isDOMText(domNode) && domNode.nodeValue)
    return domNode.nodeValue;
  if (isDOMElement(domNode)) {
    for (const childNode of Array.from(domNode.childNodes))
      text += getPlainText(childNode);
    const display = getComputedStyle(domNode).getPropertyValue("display");
    (display === "block" || display === "list" || domNode.tagName === "BR") && (text += `
`);
  }
  return text;
}, catchSlateFragment = /data-slate-fragment="(.+?)"/m, getSlateFragmentAttribute = (dataTransfer) => {
  const htmlData = dataTransfer.getData("text/html"), [, fragment2] = htmlData.match(catchSlateFragment) || [];
  return fragment2;
}, getSelection = (root) => "getSelection" in root && typeof root.getSelection == "function" ? root.getSelection() : document.getSelection(), isTrackedMutation = (editor, mutation, batch) => {
  const {
    target
  } = mutation;
  if (isDOMElement(target) && target.matches('[contentEditable="false"]'))
    return !1;
  const {
    document: document2
  } = DOMEditor.getWindow(editor);
  if (containsShadowAware(document2, target))
    return DOMEditor.hasDOMNode(editor, target, {
      editable: !0
    });
  const parentMutation = batch.find(({
    addedNodes,
    removedNodes
  }) => {
    for (const node2 of addedNodes)
      if (node2 === target || containsShadowAware(node2, target))
        return !0;
    for (const node2 of removedNodes)
      if (node2 === target || containsShadowAware(node2, target))
        return !0;
    return !1;
  });
  return !parentMutation || parentMutation === mutation ? !1 : isTrackedMutation(editor, parentMutation, batch);
}, getActiveElement = () => {
  let activeElement = document.activeElement;
  for (; activeElement?.shadowRoot && activeElement.shadowRoot?.activeElement; )
    activeElement = activeElement?.shadowRoot?.activeElement;
  return activeElement;
}, isBefore = (node2, otherNode) => !!(node2.compareDocumentPosition(otherNode) & Node.DOCUMENT_POSITION_PRECEDING), isAfter = (node2, otherNode) => !!(node2.compareDocumentPosition(otherNode) & Node.DOCUMENT_POSITION_FOLLOWING), closestShadowAware = (element, selector) => {
  if (!element)
    return null;
  let current = element;
  for (; current; ) {
    if (current.matches && current.matches(selector))
      return current;
    if (current.parentElement)
      current = current.parentElement;
    else if (current.parentNode && "host" in current.parentNode)
      current = current.parentNode.host;
    else
      return null;
  }
  return null;
}, containsShadowAware = (parent2, child) => {
  if (!parent2 || !child)
    return !1;
  if (parent2.contains(child))
    return !0;
  let current = child;
  for (; current; ) {
    if (current === parent2)
      return !0;
    if (current.parentNode)
      "host" in current.parentNode ? current = current.parentNode.host : current = current.parentNode;
    else
      return !1;
  }
  return !1;
}, IS_IOS = typeof navigator < "u" && typeof window < "u" && /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream, IS_APPLE = typeof navigator < "u" && /Mac OS X/.test(navigator.userAgent), IS_ANDROID = typeof navigator < "u" && /Android/.test(navigator.userAgent), IS_FIREFOX = typeof navigator < "u" && /^(?!.*Seamonkey)(?=.*Firefox).*/i.test(navigator.userAgent), IS_WEBKIT = typeof navigator < "u" && /AppleWebKit(?!.*Chrome)/i.test(navigator.userAgent), IS_EDGE_LEGACY = typeof navigator < "u" && /Edge?\/(?:[0-6][0-9]|[0-7][0-8])(?:\.)/i.test(navigator.userAgent), IS_CHROME = typeof navigator < "u" && /Chrome/i.test(navigator.userAgent), IS_CHROME_LEGACY = typeof navigator < "u" && /Chrome?\/(?:[0-7][0-5]|[0-6][0-9])(?:\.)/i.test(navigator.userAgent), IS_ANDROID_CHROME_LEGACY = IS_ANDROID && typeof navigator < "u" && /Chrome?\/(?:[0-5]?\d)(?:\.)/i.test(navigator.userAgent), IS_FIREFOX_LEGACY = typeof navigator < "u" && /^(?!.*Seamonkey)(?=.*Firefox\/(?:[0-7][0-9]|[0-8][0-6])(?:\.)).*/i.test(navigator.userAgent), IS_UC_MOBILE = typeof navigator < "u" && /.*UCBrowser/.test(navigator.userAgent), IS_WECHATBROWSER = typeof navigator < "u" && /.*Wechat/.test(navigator.userAgent) && !/.*MacWechat/.test(navigator.userAgent) && // avoid lookbehind (buggy in safari < 16.4)
(!IS_CHROME || IS_CHROME_LEGACY), CAN_USE_DOM = typeof window < "u" && typeof window.document < "u" && typeof window.document.createElement < "u";
typeof navigator < "u" && /Safari/.test(navigator.userAgent) && /Version\/(\\d+)/.test(navigator.userAgent) && (navigator.userAgent.match(/Version\/(\\d+)/)?.[1] && // biome-ignore lint/suspicious/noNonNullAssertedOptionalChain: Slate upstream — regex match guaranteed by outer test
parseInt(navigator.userAgent.match(/Version\/(\\d+)/)?.[1], 10) < 17);
const HAS_BEFORE_INPUT_SUPPORT = (!IS_CHROME_LEGACY || !IS_ANDROID_CHROME_LEGACY) && !IS_EDGE_LEGACY && // globalThis is undefined in older browsers
typeof globalThis < "u" && globalThis.InputEvent && typeof globalThis.InputEvent.prototype.getTargetRanges == "function";
let n = 0;
class Key {
  constructor() {
    this.id = `${n++}`;
  }
}
const IS_NODE_MAP_DIRTY = /* @__PURE__ */ new WeakMap(), NODE_TO_INDEX = /* @__PURE__ */ new WeakMap(), NODE_TO_PARENT = /* @__PURE__ */ new WeakMap(), EDITOR_TO_WINDOW = /* @__PURE__ */ new WeakMap(), EDITOR_TO_ELEMENT = /* @__PURE__ */ new WeakMap(), EDITOR_TO_PLACEHOLDER_ELEMENT = /* @__PURE__ */ new WeakMap(), ELEMENT_TO_NODE = /* @__PURE__ */ new WeakMap(), NODE_TO_ELEMENT = /* @__PURE__ */ new WeakMap(), NODE_TO_KEY = /* @__PURE__ */ new WeakMap(), EDITOR_TO_KEY_TO_ELEMENT = /* @__PURE__ */ new WeakMap(), IS_READ_ONLY = /* @__PURE__ */ new WeakMap(), IS_FOCUSED = /* @__PURE__ */ new WeakMap(), IS_COMPOSING = /* @__PURE__ */ new WeakMap(), EDITOR_TO_USER_SELECTION = /* @__PURE__ */ new WeakMap(), EDITOR_TO_ON_CHANGE = /* @__PURE__ */ new WeakMap(), EDITOR_TO_SCHEDULE_FLUSH = /* @__PURE__ */ new WeakMap(), EDITOR_TO_PENDING_INSERTION_MARKS = /* @__PURE__ */ new WeakMap(), EDITOR_TO_USER_MARKS = /* @__PURE__ */ new WeakMap(), EDITOR_TO_PENDING_DIFFS = /* @__PURE__ */ new WeakMap(), EDITOR_TO_PENDING_ACTION = /* @__PURE__ */ new WeakMap(), EDITOR_TO_PENDING_SELECTION = /* @__PURE__ */ new WeakMap(), EDITOR_TO_FORCE_RENDER = /* @__PURE__ */ new WeakMap(), PLACEHOLDER_SYMBOL = /* @__PURE__ */ Symbol("placeholder"), MARK_PLACEHOLDER_SYMBOL = /* @__PURE__ */ Symbol("mark-placeholder"), DOMEditor = {
  androidPendingDiffs: (editor) => EDITOR_TO_PENDING_DIFFS.get(editor),
  androidScheduleFlush: (editor) => {
    EDITOR_TO_SCHEDULE_FLUSH.get(editor)?.();
  },
  blur: (editor) => {
    const el = DOMEditor.toDOMNode(editor, editor), root = DOMEditor.findDocumentOrShadowRoot(editor);
    IS_FOCUSED.set(editor, !1), root.activeElement === el && el.blur();
  },
  deselect: (editor) => {
    const {
      selection
    } = editor, root = DOMEditor.findDocumentOrShadowRoot(editor), domSelection = getSelection(root);
    domSelection && domSelection.rangeCount > 0 && domSelection.removeAllRanges(), selection && Transforms.deselect(editor);
  },
  findDocumentOrShadowRoot: (editor) => {
    const el = DOMEditor.toDOMNode(editor, editor), root = el.getRootNode();
    return root instanceof Document || root instanceof ShadowRoot ? root : el.ownerDocument;
  },
  findEventRange: (editor, event) => {
    "nativeEvent" in event && (event = event.nativeEvent);
    const {
      clientX: x,
      clientY: y,
      target
    } = event;
    if (x == null || y == null)
      throw new Error(`Cannot resolve a Slate range from a DOM event: ${event}`);
    const node2 = DOMEditor.toSlateNode(editor, event.target), path2 = DOMEditor.findPath(editor, node2);
    if (Element$2.isElement(node2) && Editor.isVoid(editor, node2)) {
      const rect = target.getBoundingClientRect(), isPrev = editor.isInline(node2) ? x - rect.left < rect.left + rect.width - x : y - rect.top < rect.top + rect.height - y, edge = Editor.point(editor, path2, {
        edge: isPrev ? "start" : "end"
      }), point2 = isPrev ? Editor.before(editor, edge) : Editor.after(editor, edge);
      if (point2)
        return Editor.range(editor, point2);
    }
    let domRange = null;
    const {
      document: document2
    } = DOMEditor.getWindow(editor);
    if (document2.caretRangeFromPoint)
      domRange = document2.caretRangeFromPoint(x, y);
    else {
      const position = document2.caretPositionFromPoint(x, y);
      position && (domRange = document2.createRange(), domRange.setStart(position.offsetNode, position.offset), domRange.setEnd(position.offsetNode, position.offset));
    }
    if (!domRange)
      throw new Error(`Cannot resolve a Slate range from a DOM event: ${event}`);
    return DOMEditor.toSlateRange(editor, domRange, {
      exactMatch: !1,
      suppressThrow: !1
    });
  },
  findKey: (_editor, node2) => {
    let key = NODE_TO_KEY.get(node2);
    return key || (key = new Key(), NODE_TO_KEY.set(node2, key)), key;
  },
  findPath: (_editor, node2) => {
    const path2 = [];
    let child = node2;
    for (; ; ) {
      const parent2 = NODE_TO_PARENT.get(child);
      if (parent2 == null) {
        if (Editor.isEditor(child))
          return path2;
        break;
      }
      const i = NODE_TO_INDEX.get(child);
      if (i == null)
        break;
      path2.unshift(i), child = parent2;
    }
    throw new Error(`Unable to find the path for Slate node: ${Scrubber.stringify(node2)}`);
  },
  focus: (editor, options = {
    retries: 5
  }) => {
    if (IS_FOCUSED.get(editor) || !EDITOR_TO_ELEMENT.get(editor))
      return;
    if (options.retries <= 0)
      throw new Error("Could not set focus, editor seems stuck with pending operations");
    if (editor.operations.length > 0) {
      setTimeout(() => {
        DOMEditor.focus(editor, {
          retries: options.retries - 1
        });
      }, 10);
      return;
    }
    const el = DOMEditor.toDOMNode(editor, editor), root = DOMEditor.findDocumentOrShadowRoot(editor);
    if (root.activeElement !== el) {
      if (editor.selection && root instanceof Document) {
        const domSelection = getSelection(root), domRange = DOMEditor.toDOMRange(editor, editor.selection);
        domSelection?.removeAllRanges(), domSelection?.addRange(domRange);
      }
      editor.selection || Transforms.select(editor, Editor.start(editor, [])), IS_FOCUSED.set(editor, !0), el.focus({
        preventScroll: !0
      });
    }
  },
  getWindow: (editor) => {
    const window2 = EDITOR_TO_WINDOW.get(editor);
    if (!window2)
      throw new Error("Unable to find a host window element for this editor");
    return window2;
  },
  hasDOMNode: (editor, target, options = {}) => {
    const {
      editable = !1
    } = options, editorEl = DOMEditor.toDOMNode(editor, editor);
    let targetEl = null;
    try {
      targetEl = isDOMElement(target) ? target : target.parentElement;
    } catch (err) {
      if (err instanceof Error && !err.message.includes('Permission denied to access property "nodeType"'))
        throw err;
    }
    return targetEl ? closestShadowAware(targetEl, "[data-slate-editor]") === editorEl && (!editable || targetEl.isContentEditable ? !0 : typeof targetEl.isContentEditable == "boolean" && // isContentEditable exists only on HTMLElement, and on other nodes it will be undefined
    // this is the core logic that lets you know you got the right editor.selection instead of null when editor is contenteditable="false"(readOnly)
    closestShadowAware(targetEl, '[contenteditable="false"]') === editorEl || !!targetEl.getAttribute("data-slate-zero-width")) : !1;
  },
  hasEditableTarget: (editor, target) => isDOMNode(target) && DOMEditor.hasDOMNode(editor, target, {
    editable: !0
  }),
  hasRange: (editor, range2) => {
    const {
      anchor,
      focus
    } = range2;
    return Editor.hasPath(editor, anchor.path) && Editor.hasPath(editor, focus.path);
  },
  hasSelectableTarget: (editor, target) => DOMEditor.hasEditableTarget(editor, target) || DOMEditor.isTargetInsideNonReadonlyVoid(editor, target),
  hasTarget: (editor, target) => isDOMNode(target) && DOMEditor.hasDOMNode(editor, target),
  insertData: (editor, data) => {
    editor.insertData(data);
  },
  insertFragmentData: (editor, data) => editor.insertFragmentData(data),
  insertTextData: (editor, data) => editor.insertTextData(data),
  isComposing: (editor) => !!IS_COMPOSING.get(editor),
  isFocused: (editor) => !!IS_FOCUSED.get(editor),
  isReadOnly: (editor) => !!IS_READ_ONLY.get(editor),
  isTargetInsideNonReadonlyVoid: (editor, target) => {
    if (IS_READ_ONLY.get(editor))
      return !1;
    const slateNode = DOMEditor.hasTarget(editor, target) && DOMEditor.toSlateNode(editor, target);
    return Element$2.isElement(slateNode) && Editor.isVoid(editor, slateNode);
  },
  setFragmentData: (editor, data, originEvent) => editor.setFragmentData(data, originEvent),
  toDOMNode: (editor, node2) => {
    const KEY_TO_ELEMENT = EDITOR_TO_KEY_TO_ELEMENT.get(editor), domNode = Editor.isEditor(node2) ? EDITOR_TO_ELEMENT.get(editor) : KEY_TO_ELEMENT?.get(DOMEditor.findKey(editor, node2));
    if (!domNode)
      throw new Error(`Cannot resolve a DOM node from Slate node: ${Scrubber.stringify(node2)}`);
    return domNode;
  },
  toDOMPoint: (editor, point2) => {
    const [node2] = Editor.node(editor, point2.path), el = DOMEditor.toDOMNode(editor, node2);
    let domPoint;
    Editor.void(editor, {
      at: point2
    }) && (point2 = {
      path: point2.path,
      offset: 0
    });
    const texts = Array.from(el.querySelectorAll("[data-slate-string], [data-slate-zero-width]"));
    let start2 = 0;
    for (let i = 0; i < texts.length; i++) {
      const text = texts[i], domNode = text.childNodes[0];
      if (domNode == null || domNode.textContent == null)
        continue;
      const {
        length
      } = domNode.textContent, attr = text.getAttribute("data-slate-length"), trueLength = attr == null ? length : parseInt(attr, 10), end2 = start2 + trueLength, nextText = texts[i + 1];
      if (point2.offset === end2 && nextText?.hasAttribute("data-slate-mark-placeholder")) {
        const domText = nextText.childNodes[0];
        domPoint = [
          // COMPAT: If we don't explicity set the dom point to be on the actual
          // dom text element, chrome will put the selection behind the actual dom
          // text element, causing domRange.getBoundingClientRect() calls on a collapsed
          // selection to return incorrect zero values (https://bugs.chromium.org/p/chromium/issues/detail?id=435438)
          // which will cause issues when scrolling to it.
          domText instanceof DOMText ? domText : nextText,
          nextText.textContent?.startsWith("\uFEFF") ? 1 : 0
        ];
        break;
      }
      if (point2.offset <= end2) {
        const offset = Math.min(length, Math.max(0, point2.offset - start2));
        domPoint = [domNode, offset];
        break;
      }
      start2 = end2;
    }
    if (!domPoint)
      throw new Error(`Cannot resolve a DOM point from Slate point: ${Scrubber.stringify(point2)}`);
    return domPoint;
  },
  toDOMRange: (editor, range2) => {
    const {
      anchor,
      focus
    } = range2, isBackward = Range.isBackward(range2), domAnchor = DOMEditor.toDOMPoint(editor, anchor), domFocus = Range.isCollapsed(range2) ? domAnchor : DOMEditor.toDOMPoint(editor, focus), domRange = DOMEditor.getWindow(editor).document.createRange(), [startNode, startOffset] = isBackward ? domFocus : domAnchor, [endNode, endOffset] = isBackward ? domAnchor : domFocus, isStartAtZeroWidth = !!(isDOMElement(startNode) ? startNode : startNode.parentElement).getAttribute("data-slate-zero-width"), isEndAtZeroWidth = !!(isDOMElement(endNode) ? endNode : endNode.parentElement).getAttribute("data-slate-zero-width");
    return domRange.setStart(startNode, isStartAtZeroWidth ? 1 : startOffset), domRange.setEnd(endNode, isEndAtZeroWidth ? 1 : endOffset), domRange;
  },
  toSlateNode: (_editor, domNode) => {
    let domEl = isDOMElement(domNode) ? domNode : domNode.parentElement;
    domEl && !domEl.hasAttribute("data-slate-node") && (domEl = domEl.closest("[data-slate-node]"));
    const node2 = domEl ? ELEMENT_TO_NODE.get(domEl) : null;
    if (!node2)
      throw new Error(`Cannot resolve a Slate node from DOM node: ${domEl}`);
    return node2;
  },
  toSlatePoint: (editor, domPoint, options) => {
    const {
      exactMatch,
      suppressThrow,
      searchDirection
    } = options, [nearestNode, nearestOffset] = exactMatch ? domPoint : normalizeDOMPoint(domPoint), parentNode = nearestNode.parentNode;
    let textNode = null, offset = 0;
    if (parentNode) {
      const editorEl = DOMEditor.toDOMNode(editor, editor), potentialVoidNode = parentNode.closest('[data-slate-void="true"]'), voidNode = potentialVoidNode && containsShadowAware(editorEl, potentialVoidNode) ? potentialVoidNode : null, potentialNonEditableNode = parentNode.closest('[contenteditable="false"]'), nonEditableNode = potentialNonEditableNode && containsShadowAware(editorEl, potentialNonEditableNode) ? potentialNonEditableNode : null;
      let leafNode = parentNode.closest("[data-slate-leaf]"), domNode = null;
      if (leafNode) {
        if (textNode = leafNode.closest('[data-slate-node="text"]'), textNode) {
          const range2 = DOMEditor.getWindow(editor).document.createRange();
          range2.setStart(textNode, 0), range2.setEnd(nearestNode, nearestOffset);
          const contents = range2.cloneContents();
          [...Array.prototype.slice.call(contents.querySelectorAll("[data-slate-zero-width]")), ...Array.prototype.slice.call(contents.querySelectorAll("[contenteditable=false]"))].forEach((el) => {
            if (IS_ANDROID && !exactMatch && el.hasAttribute("data-slate-zero-width") && el.textContent.length > 0 && el.textContext !== "\uFEFF") {
              el.textContent.startsWith("\uFEFF") && (el.textContent = el.textContent.slice(1));
              return;
            }
            el.parentNode.removeChild(el);
          }), offset = contents.textContent.length, domNode = textNode;
        }
      } else if (voidNode) {
        const leafNodes = voidNode.querySelectorAll("[data-slate-leaf]");
        for (let index = 0; index < leafNodes.length; index++) {
          const current = leafNodes[index];
          if (DOMEditor.hasDOMNode(editor, current)) {
            leafNode = current;
            break;
          }
        }
        leafNode ? (textNode = leafNode.closest('[data-slate-node="text"]'), domNode = leafNode, offset = domNode.textContent.length, domNode.querySelectorAll("[data-slate-zero-width]").forEach((el) => {
          offset -= el.textContent.length;
        })) : offset = 1;
      } else if (nonEditableNode) {
        const getLeafNodes = (node2) => node2 ? node2.querySelectorAll(
          // Exclude leaf nodes in nested editors
          "[data-slate-leaf]:not(:scope [data-slate-editor] [data-slate-leaf])"
        ) : [], elementNode = nonEditableNode.closest('[data-slate-node="element"]');
        (searchDirection === "backward" || !searchDirection) && (leafNode = [...getLeafNodes(elementNode?.previousElementSibling), ...getLeafNodes(elementNode)].findLast((leaf2) => isBefore(nonEditableNode, leaf2)) ?? null), (searchDirection === "forward" || !searchDirection) && (leafNode = [...getLeafNodes(elementNode), ...getLeafNodes(elementNode?.nextElementSibling)].find((leaf2) => isAfter(nonEditableNode, leaf2)) ?? null), leafNode && (textNode = leafNode.closest('[data-slate-node="text"]'), domNode = leafNode, searchDirection === "forward" ? offset = 0 : (offset = domNode.textContent.length, domNode.querySelectorAll("[data-slate-zero-width]").forEach((el) => {
          offset -= el.textContent.length;
        })));
      }
      domNode && offset === domNode.textContent.length && // COMPAT: Android IMEs might remove the zero width space while composing,
      // and we don't add it for line-breaks.
      IS_ANDROID && domNode.getAttribute("data-slate-zero-width") === "z" && domNode.textContent?.startsWith("\uFEFF") && // COMPAT: If the parent node is a Slate zero-width space, editor is
      // because the text node should have no characters. However, during IME
      // composition the ASCII characters will be prepended to the zero-width
      // space, so subtract 1 from the offset to account for the zero-width
      // space character.
      (parentNode.hasAttribute("data-slate-zero-width") || // COMPAT: In Firefox, `range.cloneContents()` returns an extra trailing '\n'
      // when the document ends with a new-line character. This results in the offset
      // length being off by one, so we need to subtract one to account for this.
      IS_FIREFOX && domNode.textContent?.endsWith(`

`)) && offset--;
    }
    if (IS_ANDROID && !textNode && !exactMatch) {
      const node2 = parentNode.hasAttribute("data-slate-node") ? parentNode : parentNode.closest("[data-slate-node]");
      if (node2 && DOMEditor.hasDOMNode(editor, node2, {
        editable: !0
      })) {
        const slateNode2 = DOMEditor.toSlateNode(editor, node2);
        let {
          path: path2,
          offset: offset2
        } = Editor.start(editor, DOMEditor.findPath(editor, slateNode2));
        return node2.querySelector("[data-slate-leaf]") || (offset2 = nearestOffset), {
          path: path2,
          offset: offset2
        };
      }
    }
    if (!textNode) {
      if (suppressThrow)
        return null;
      throw new Error(`Cannot resolve a Slate point from DOM point: ${domPoint}`);
    }
    const slateNode = DOMEditor.toSlateNode(editor, textNode);
    return {
      path: DOMEditor.findPath(editor, slateNode),
      offset
    };
  },
  toSlateRange: (editor, domRange, options) => {
    const {
      exactMatch,
      suppressThrow
    } = options, el = isDOMSelection(domRange) ? domRange.anchorNode : domRange.startContainer;
    let anchorNode = null, anchorOffset = 0, focusNode = null, focusOffset = 0, isCollapsed = !1;
    if (el)
      if (isDOMSelection(domRange)) {
        if (IS_FIREFOX && domRange.rangeCount > 1) {
          focusNode = domRange.focusNode;
          const firstRange = domRange.getRangeAt(0), lastRange = domRange.getRangeAt(domRange.rangeCount - 1);
          if (focusNode instanceof HTMLTableRowElement && firstRange.startContainer instanceof HTMLTableRowElement && lastRange.startContainer instanceof HTMLTableRowElement) {
            let getLastChildren2 = function(element) {
              return element.childElementCount > 0 ? getLastChildren2(element.children[0]) : element;
            };
            const firstNodeRow = firstRange.startContainer, lastNodeRow = lastRange.startContainer, firstNode = getLastChildren2(firstNodeRow.children[firstRange.startOffset]), lastNode = getLastChildren2(lastNodeRow.children[lastRange.startOffset]);
            focusOffset = 0, lastNode.childNodes.length > 0 ? anchorNode = lastNode.childNodes[0] ?? null : anchorNode = lastNode, firstNode.childNodes.length > 0 ? focusNode = firstNode.childNodes[0] ?? null : focusNode = firstNode, lastNode instanceof HTMLElement ? anchorOffset = lastNode.innerHTML.length : anchorOffset = 0;
          } else
            firstRange.startContainer === focusNode ? (anchorNode = lastRange.endContainer, anchorOffset = lastRange.endOffset, focusOffset = firstRange.startOffset) : (anchorNode = firstRange.startContainer, anchorOffset = firstRange.endOffset, focusOffset = lastRange.startOffset);
        } else
          anchorNode = domRange.anchorNode, anchorOffset = domRange.anchorOffset, focusNode = domRange.focusNode, focusOffset = domRange.focusOffset;
        IS_CHROME && hasShadowRoot(anchorNode) || IS_FIREFOX ? isCollapsed = domRange.anchorNode === domRange.focusNode && domRange.anchorOffset === domRange.focusOffset : isCollapsed = domRange.isCollapsed;
      } else
        anchorNode = domRange.startContainer, anchorOffset = domRange.startOffset, focusNode = domRange.endContainer, focusOffset = domRange.endOffset, isCollapsed = domRange.collapsed;
    if (anchorNode == null || focusNode == null || anchorOffset == null || focusOffset == null)
      throw new Error(`Cannot resolve a Slate range from DOM range: ${domRange}`);
    IS_FIREFOX && focusNode.textContent?.endsWith(`

`) && focusOffset === focusNode.textContent.length && focusOffset--;
    const anchor = DOMEditor.toSlatePoint(editor, [anchorNode, anchorOffset], {
      exactMatch,
      suppressThrow
    });
    if (!anchor)
      return null;
    const focusBeforeAnchor = isBefore(anchorNode, focusNode) || anchorNode === focusNode && focusOffset < anchorOffset, focus = isCollapsed ? anchor : DOMEditor.toSlatePoint(editor, [focusNode, focusOffset], {
      exactMatch,
      suppressThrow,
      searchDirection: focusBeforeAnchor ? "forward" : "backward"
    });
    if (!focus)
      return null;
    let range2 = {
      anchor,
      focus
    };
    return Range.isExpanded(range2) && Range.isForward(range2) && isDOMElement(focusNode) && Editor.void(editor, {
      at: range2.focus,
      mode: "highest"
    }) && (range2 = Editor.unhangRange(editor, range2, {
      voids: !0
    })), range2;
  }
};
function verifyDiffState(editor, textDiff) {
  const {
    path: path2,
    diff: diff2
  } = textDiff;
  if (!Editor.hasPath(editor, path2))
    return !1;
  const node2 = Node$1.get(editor, path2);
  if (!Text$1.isText(node2))
    return !1;
  if (diff2.start !== node2.text.length || diff2.text.length === 0)
    return node2.text.slice(diff2.start, diff2.start + diff2.text.length) === diff2.text;
  const nextPath = Path.next(path2);
  if (!Editor.hasPath(editor, nextPath))
    return !1;
  const nextNode = Node$1.get(editor, nextPath);
  return Text$1.isText(nextNode) && nextNode.text.startsWith(diff2.text);
}
function applyStringDiff(text, ...diffs) {
  return diffs.reduce((text2, diff2) => text2.slice(0, diff2.start) + diff2.text + text2.slice(diff2.end), text);
}
function longestCommonPrefixLength(str, another) {
  const length = Math.min(str.length, another.length);
  for (let i = 0; i < length; i++)
    if (str.charAt(i) !== another.charAt(i))
      return i;
  return length;
}
function longestCommonSuffixLength(str, another, max) {
  const length = Math.min(str.length, another.length, max);
  for (let i = 0; i < length; i++)
    if (str.charAt(str.length - i - 1) !== another.charAt(another.length - i - 1))
      return i;
  return length;
}
function normalizeStringDiff(targetText, diff2) {
  const {
    start: start2,
    end: end2,
    text
  } = diff2, removedText = targetText.slice(start2, end2), prefixLength = longestCommonPrefixLength(removedText, text), max = Math.min(removedText.length - prefixLength, text.length - prefixLength), suffixLength = longestCommonSuffixLength(removedText, text, max), normalized = {
    start: start2 + prefixLength,
    end: end2 - suffixLength,
    text: text.slice(prefixLength, text.length - suffixLength)
  };
  return normalized.start === normalized.end && normalized.text.length === 0 ? null : normalized;
}
function mergeStringDiffs(targetText, a, b) {
  const start2 = Math.min(a.start, b.start), overlap = Math.max(0, Math.min(a.start + a.text.length, b.end) - b.start), applied = applyStringDiff(targetText, a, b), sliceEnd = Math.max(b.start + b.text.length, a.start + a.text.length + (a.start + a.text.length > b.start ? b.text.length : 0) - overlap), text = applied.slice(start2, sliceEnd), end2 = Math.max(a.end, b.end - a.text.length + (a.end - a.start));
  return normalizeStringDiff(targetText, {
    start: start2,
    end: end2,
    text
  });
}
function targetRange(textDiff) {
  const {
    path: path2,
    diff: diff2
  } = textDiff;
  return {
    anchor: {
      path: path2,
      offset: diff2.start
    },
    focus: {
      path: path2,
      offset: diff2.end
    }
  };
}
function normalizePoint$1(editor, point2) {
  let {
    path: path2,
    offset
  } = point2;
  if (!Editor.hasPath(editor, path2))
    return null;
  let leaf2 = Node$1.get(editor, path2);
  if (!Text$1.isText(leaf2))
    return null;
  const parentBlock = Editor.above(editor, {
    match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2),
    at: path2
  });
  if (!parentBlock)
    return null;
  for (; offset > leaf2.text.length; ) {
    const entry = Editor.next(editor, {
      at: path2,
      match: Text$1.isText
    });
    if (!entry || !Path.isDescendant(entry[1], parentBlock[1]))
      return null;
    offset -= leaf2.text.length, leaf2 = entry[0], path2 = entry[1];
  }
  return {
    path: path2,
    offset
  };
}
function normalizeRange(editor, range2) {
  const anchor = normalizePoint$1(editor, range2.anchor);
  if (!anchor)
    return null;
  if (Range.isCollapsed(range2))
    return {
      anchor,
      focus: anchor
    };
  const focus = normalizePoint$1(editor, range2.focus);
  return focus ? {
    anchor,
    focus
  } : null;
}
function transformPendingPoint(editor, point2, op) {
  const textDiff = EDITOR_TO_PENDING_DIFFS.get(editor)?.find(({
    path: path2
  }) => Path.equals(path2, point2.path));
  if (!textDiff || point2.offset <= textDiff.diff.start)
    return Point.transform(point2, op, {
      affinity: "backward"
    });
  const {
    diff: diff2
  } = textDiff;
  if (point2.offset <= diff2.start + diff2.text.length) {
    const anchor2 = {
      path: point2.path,
      offset: diff2.start
    }, transformed2 = Point.transform(anchor2, op, {
      affinity: "backward"
    });
    return transformed2 ? {
      path: transformed2.path,
      offset: transformed2.offset + point2.offset - diff2.start
    } : null;
  }
  const anchor = {
    path: point2.path,
    offset: point2.offset - diff2.text.length + diff2.end - diff2.start
  }, transformed = Point.transform(anchor, op, {
    affinity: "backward"
  });
  return transformed ? op.type === "split_node" && Path.equals(op.path, point2.path) && anchor.offset < op.position && diff2.start < op.position ? transformed : {
    path: transformed.path,
    offset: transformed.offset + diff2.text.length - diff2.end + diff2.start
  } : null;
}
function transformPendingRange(editor, range2, op) {
  const anchor = transformPendingPoint(editor, range2.anchor, op);
  if (!anchor)
    return null;
  if (Range.isCollapsed(range2))
    return {
      anchor,
      focus: anchor
    };
  const focus = transformPendingPoint(editor, range2.focus, op);
  return focus ? {
    anchor,
    focus
  } : null;
}
function transformTextDiff(textDiff, op) {
  const {
    path: path2,
    diff: diff2,
    id
  } = textDiff;
  switch (op.type) {
    case "insert_text":
      return !Path.equals(op.path, path2) || op.offset >= diff2.end ? textDiff : op.offset <= diff2.start ? {
        diff: {
          start: op.text.length + diff2.start,
          end: op.text.length + diff2.end,
          text: diff2.text
        },
        id,
        path: path2
      } : {
        diff: {
          start: diff2.start,
          end: diff2.end + op.text.length,
          text: diff2.text
        },
        id,
        path: path2
      };
    case "remove_text":
      return !Path.equals(op.path, path2) || op.offset >= diff2.end ? textDiff : op.offset + op.text.length <= diff2.start ? {
        diff: {
          start: diff2.start - op.text.length,
          end: diff2.end - op.text.length,
          text: diff2.text
        },
        id,
        path: path2
      } : {
        diff: {
          start: diff2.start,
          end: diff2.end - op.text.length,
          text: diff2.text
        },
        id,
        path: path2
      };
    case "split_node":
      return !Path.equals(op.path, path2) || op.position >= diff2.end ? {
        diff: diff2,
        id,
        path: Path.transform(path2, op, {
          affinity: "backward"
        })
      } : op.position > diff2.start ? {
        diff: {
          start: diff2.start,
          end: Math.min(op.position, diff2.end),
          text: diff2.text
        },
        id,
        path: path2
      } : {
        diff: {
          start: diff2.start - op.position,
          end: diff2.end - op.position,
          text: diff2.text
        },
        id,
        path: Path.transform(path2, op, {
          affinity: "forward"
        })
      };
    case "merge_node":
      return Path.equals(op.path, path2) ? {
        diff: {
          start: diff2.start + op.position,
          end: diff2.end + op.position,
          text: diff2.text
        },
        id,
        path: Path.transform(path2, op)
      } : {
        diff: diff2,
        id,
        path: Path.transform(path2, op)
      };
  }
  const newPath = Path.transform(path2, op);
  return newPath ? {
    diff: diff2,
    path: newPath,
    id
  } : null;
}
const doRectsIntersect = (rect, compareRect) => {
  const middle = (compareRect.top + compareRect.bottom) / 2;
  return rect.top <= middle && rect.bottom >= middle;
}, areRangesSameLine = (editor, range1, range2) => {
  const rect1 = DOMEditor.toDOMRange(editor, range1).getBoundingClientRect(), rect2 = DOMEditor.toDOMRange(editor, range2).getBoundingClientRect();
  return doRectsIntersect(rect1, rect2) && doRectsIntersect(rect2, rect1);
}, findCurrentLineRange$1 = (editor, parentRange) => {
  const parentRangeBoundary = Editor.range(editor, Range.end(parentRange)), positions2 = Array.from(Editor.positions(editor, {
    at: parentRange
  }));
  let left = 0, right = positions2.length, middle = Math.floor(right / 2);
  if (areRangesSameLine(editor, Editor.range(editor, positions2[left]), parentRangeBoundary))
    return Editor.range(editor, positions2[left], parentRangeBoundary);
  if (positions2.length < 2)
    return Editor.range(editor, positions2[positions2.length - 1], parentRangeBoundary);
  for (; middle !== positions2.length && middle !== left; )
    areRangesSameLine(editor, Editor.range(editor, positions2[middle]), parentRangeBoundary) ? right = middle : left = middle, middle = Math.floor((left + right) / 2);
  return Editor.range(editor, positions2[left], parentRangeBoundary);
}, withDOM = (editor, clipboardFormatKey = "x-slate-fragment") => {
  const e = editor, {
    apply: apply2,
    onChange,
    deleteBackward: deleteBackward2,
    addMark: addMark2,
    removeMark: removeMark2
  } = e;
  return EDITOR_TO_KEY_TO_ELEMENT.set(e, /* @__PURE__ */ new WeakMap()), e.addMark = (key, value) => {
    EDITOR_TO_SCHEDULE_FLUSH.get(e)?.(), !EDITOR_TO_PENDING_INSERTION_MARKS.get(e) && EDITOR_TO_PENDING_DIFFS.get(e)?.length && EDITOR_TO_PENDING_INSERTION_MARKS.set(e, null), EDITOR_TO_USER_MARKS.delete(e), addMark2(key, value);
  }, e.removeMark = (key) => {
    !EDITOR_TO_PENDING_INSERTION_MARKS.get(e) && EDITOR_TO_PENDING_DIFFS.get(e)?.length && EDITOR_TO_PENDING_INSERTION_MARKS.set(e, null), EDITOR_TO_USER_MARKS.delete(e), removeMark2(key);
  }, e.deleteBackward = (unit) => {
    if (unit !== "line")
      return deleteBackward2(unit);
    if (e.selection && Range.isCollapsed(e.selection)) {
      const parentBlockEntry = Editor.above(e, {
        match: (n2) => Element$2.isElement(n2) && Editor.isBlock(e, n2),
        at: e.selection
      });
      if (parentBlockEntry) {
        const [, parentBlockPath] = parentBlockEntry, parentElementRange = Editor.range(e, parentBlockPath, e.selection.anchor), currentLineRange = findCurrentLineRange$1(e, parentElementRange);
        Range.isCollapsed(currentLineRange) || Transforms.delete(e, {
          at: currentLineRange
        });
      }
    }
  }, e.apply = (op) => {
    const matches = [], pathRefMatches = [], pendingDiffs = EDITOR_TO_PENDING_DIFFS.get(e);
    if (pendingDiffs?.length) {
      const transformed = pendingDiffs.map((textDiff) => transformTextDiff(textDiff, op)).filter(Boolean);
      EDITOR_TO_PENDING_DIFFS.set(e, transformed);
    }
    const pendingSelection = EDITOR_TO_PENDING_SELECTION.get(e);
    pendingSelection && EDITOR_TO_PENDING_SELECTION.set(e, transformPendingRange(e, pendingSelection, op));
    const pendingAction = EDITOR_TO_PENDING_ACTION.get(e);
    if (pendingAction?.at) {
      const at = Point.isPoint(pendingAction?.at) ? transformPendingPoint(e, pendingAction.at, op) : transformPendingRange(e, pendingAction.at, op);
      EDITOR_TO_PENDING_ACTION.set(e, at ? {
        ...pendingAction,
        at
      } : null);
    }
    switch (op.type) {
      case "insert_text":
      case "remove_text":
      case "set_node":
      case "split_node": {
        matches.push(...getMatches(e, op.path));
        break;
      }
      case "set_selection": {
        EDITOR_TO_USER_SELECTION.get(e)?.unref(), EDITOR_TO_USER_SELECTION.delete(e);
        break;
      }
      case "insert_node":
      case "remove_node": {
        matches.push(...getMatches(e, Path.parent(op.path)));
        break;
      }
      case "merge_node": {
        const prevPath = Path.previous(op.path);
        matches.push(...getMatches(e, prevPath));
        break;
      }
      case "move_node": {
        const commonPath = Path.common(Path.parent(op.path), Path.parent(op.newPath));
        matches.push(...getMatches(e, commonPath));
        let changedPath;
        Path.isBefore(op.path, op.newPath) ? (matches.push(...getMatches(e, Path.parent(op.path))), changedPath = op.newPath) : (matches.push(...getMatches(e, Path.parent(op.newPath))), changedPath = op.path);
        const changedNode = Node$1.get(editor, Path.parent(changedPath)), changedNodeKey = DOMEditor.findKey(e, changedNode), changedPathRef = Editor.pathRef(e, Path.parent(changedPath));
        pathRefMatches.push([changedPathRef, changedNodeKey]);
        break;
      }
    }
    switch (apply2(op), op.type) {
      case "insert_node":
      case "remove_node":
      case "merge_node":
      case "move_node":
      case "split_node":
      case "insert_text":
      case "remove_text":
      case "set_selection":
        IS_NODE_MAP_DIRTY.set(e, !0);
    }
    for (const [path2, key] of matches) {
      const [node2] = Editor.node(e, path2);
      NODE_TO_KEY.set(node2, key);
    }
    for (const [pathRef2, key] of pathRefMatches) {
      if (pathRef2.current) {
        const [node2] = Editor.node(e, pathRef2.current);
        NODE_TO_KEY.set(node2, key);
      }
      pathRef2.unref();
    }
  }, e.setFragmentData = (data) => {
    const {
      selection
    } = e;
    if (!selection)
      return;
    const [start2, end2] = Range.edges(selection), startVoid = Editor.void(e, {
      at: start2.path
    }), endVoid = Editor.void(e, {
      at: end2.path
    });
    if (Range.isCollapsed(selection) && !startVoid)
      return;
    const domRange = DOMEditor.toDOMRange(e, selection);
    let contents = domRange.cloneContents(), attach = contents.childNodes[0];
    if (contents.childNodes.forEach((node2) => {
      node2.textContent && node2.textContent.trim() !== "" && (attach = node2);
    }), endVoid) {
      const [voidNode] = endVoid, r = domRange.cloneRange(), domNode = DOMEditor.toDOMNode(e, voidNode);
      r.setEndAfter(domNode), contents = r.cloneContents();
    }
    if (startVoid && (attach = contents.querySelector("[data-slate-spacer]")), Array.from(contents.querySelectorAll("[data-slate-zero-width]")).forEach((zw) => {
      const isNewline = zw.getAttribute("data-slate-zero-width") === "n";
      zw.textContent = isNewline ? `
` : "";
    }), isDOMText(attach)) {
      const span = attach.ownerDocument.createElement("span");
      span.style.whiteSpace = "pre", span.appendChild(attach), contents.appendChild(span), attach = span;
    }
    const fragment2 = e.getFragment(), string2 = JSON.stringify(fragment2), encoded = window.btoa(encodeURIComponent(string2));
    attach.setAttribute("data-slate-fragment", encoded), data.setData(`application/${clipboardFormatKey}`, encoded);
    const div = contents.ownerDocument.createElement("div");
    return div.appendChild(contents), div.setAttribute("hidden", "true"), contents.ownerDocument.body.appendChild(div), data.setData("text/html", div.innerHTML), data.setData("text/plain", getPlainText(div)), contents.ownerDocument.body.removeChild(div), data;
  }, e.insertData = (data) => {
    e.insertFragmentData(data) || e.insertTextData(data);
  }, e.insertFragmentData = (data) => {
    const fragment2 = data.getData(`application/${clipboardFormatKey}`) || getSlateFragmentAttribute(data);
    if (fragment2) {
      const decoded = decodeURIComponent(window.atob(fragment2)), parsed = JSON.parse(decoded);
      return e.insertFragment(parsed), !0;
    }
    return !1;
  }, e.insertTextData = (data) => {
    const text = data.getData("text/plain");
    if (text) {
      const lines = text.split(/\r\n|\r|\n/);
      let split = !1;
      for (const line of lines)
        split && Transforms.splitNodes(e, {
          always: !0
        }), e.insertText(line), split = !0;
      return !0;
    }
    return !1;
  }, e.onChange = (options) => {
    const onContextChange = EDITOR_TO_ON_CHANGE.get(e);
    onContextChange && onContextChange(options), onChange(options);
  }, e;
}, getMatches = (e, path2) => {
  const matches = [];
  for (const [n2, p] of Editor.levels(e, {
    at: path2
  })) {
    const key = DOMEditor.findKey(e, n2);
    matches.push([p, key]);
  }
  return matches;
}, TRIPLE_CLICK = 3, HOTKEYS = {
  bold: "mod+b",
  compose: ["down", "left", "right", "up", "backspace", "enter"],
  moveBackward: "left",
  moveForward: "right",
  moveWordBackward: "ctrl+left",
  moveWordForward: "ctrl+right",
  deleteBackward: "shift?+backspace",
  deleteForward: "shift?+delete",
  extendBackward: "shift+left",
  extendForward: "shift+right",
  italic: "mod+i",
  insertSoftBreak: "shift+enter",
  splitBlock: "enter",
  undo: "mod+z"
}, APPLE_HOTKEYS = {
  moveLineBackward: "opt+up",
  moveLineForward: "opt+down",
  moveWordBackward: "opt+left",
  moveWordForward: "opt+right",
  deleteBackward: ["ctrl+backspace", "ctrl+h"],
  deleteForward: ["ctrl+delete", "ctrl+d"],
  deleteLineBackward: "cmd+shift?+backspace",
  deleteLineForward: ["cmd+shift?+delete", "ctrl+k"],
  deleteWordBackward: "opt+shift?+backspace",
  deleteWordForward: "opt+shift?+delete",
  extendLineBackward: "opt+shift+up",
  extendLineForward: "opt+shift+down",
  redo: "cmd+shift+z",
  transposeCharacter: "ctrl+t"
}, WINDOWS_HOTKEYS = {
  deleteWordBackward: "ctrl+shift?+backspace",
  deleteWordForward: "ctrl+shift?+delete",
  redo: ["ctrl+y", "ctrl+shift+z"]
}, create = (key) => {
  const generic = HOTKEYS[key], apple = APPLE_HOTKEYS[key], windows = WINDOWS_HOTKEYS[key], isGeneric = generic && isHotkey$1(generic), isApple = apple && isHotkey$1(apple), isWindows = windows && isHotkey$1(windows);
  return (event) => !!(isGeneric && isGeneric(event) || IS_APPLE && isApple && isApple(event) || !IS_APPLE && isWindows && isWindows(event));
};
var Hotkeys = {
  isBold: create("bold"),
  isCompose: create("compose"),
  isMoveBackward: create("moveBackward"),
  isMoveForward: create("moveForward"),
  isDeleteBackward: create("deleteBackward"),
  isDeleteForward: create("deleteForward"),
  isDeleteLineBackward: create("deleteLineBackward"),
  isDeleteLineForward: create("deleteLineForward"),
  isDeleteWordBackward: create("deleteWordBackward"),
  isDeleteWordForward: create("deleteWordForward"),
  isExtendBackward: create("extendBackward"),
  isExtendForward: create("extendForward"),
  isExtendLineBackward: create("extendLineBackward"),
  isExtendLineForward: create("extendLineForward"),
  isItalic: create("italic"),
  isMoveLineBackward: create("moveLineBackward"),
  isMoveLineForward: create("moveLineForward"),
  isMoveWordBackward: create("moveWordBackward"),
  isMoveWordForward: create("moveWordForward"),
  isRedo: create("redo"),
  isSoftBreak: create("insertSoftBreak"),
  isSplitBlock: create("splitBlock"),
  isTransposeCharacter: create("transposeCharacter"),
  isUndo: create("undo")
};
const shallowCompare = (obj1, obj2) => Object.keys(obj1).length === Object.keys(obj2).length && Object.keys(obj1).every((key) => obj2.hasOwnProperty(key) && obj1[key] === obj2[key]), isDecorationFlagsEqual = (range2, other) => {
  const {
    anchor: _rangeAnchor,
    focus: _rangeFocus,
    ...rangeOwnProps
  } = range2, {
    anchor: _otherAnchor,
    focus: _otherFocus,
    ...otherOwnProps
  } = other;
  return range2[PLACEHOLDER_SYMBOL] === other[PLACEHOLDER_SYMBOL] && shallowCompare(rangeOwnProps, otherOwnProps);
}, isElementDecorationsEqual = (list, another) => {
  if (list === another)
    return !0;
  if (!list || !another || list.length !== another.length)
    return !1;
  for (let i = 0; i < list.length; i++) {
    const range2 = list[i], other = another[i];
    if (!Range.equals(range2, other) || !isDecorationFlagsEqual(range2, other))
      return !1;
  }
  return !0;
}, isTextDecorationsEqual = (list, another) => {
  if (list === another)
    return !0;
  if (!list || !another || list.length !== another.length)
    return !1;
  for (let i = 0; i < list.length; i++) {
    const range2 = list[i], other = another[i];
    if (range2.anchor.offset !== other.anchor.offset || range2.focus.offset !== other.focus.offset || !isDecorationFlagsEqual(range2, other))
      return !1;
  }
  return !0;
}, splitDecorationsByChild = (editor, node2, decorations) => {
  const decorationsByChild = Array.from(node2.children, () => []);
  if (decorations.length === 0)
    return decorationsByChild;
  const path2 = DOMEditor.findPath(editor, node2), level = path2.length, ancestorRange = Editor.range(editor, path2), cachedChildRanges = new Array(node2.children.length), getChildRange = (index) => {
    const cachedRange = cachedChildRanges[index];
    if (cachedRange)
      return cachedRange;
    const childRange = Editor.range(editor, [...path2, index]);
    return cachedChildRanges[index] = childRange, childRange;
  };
  for (const decoration of decorations) {
    const decorationRange = Range.intersection(ancestorRange, decoration);
    if (!decorationRange)
      continue;
    const [startPoint, endPoint] = Range.edges(decorationRange), startIndex = startPoint.path[level], endIndex = endPoint.path[level];
    for (let i = startIndex; i <= endIndex; i++) {
      const ds = decorationsByChild[i];
      if (!ds)
        continue;
      const childRange = getChildRange(i), childDecorationRange = Range.intersection(childRange, decoration);
      childDecorationRange && ds.push({
        ...decoration,
        ...childDecorationRange
      });
    }
  }
  return decorationsByChild;
};
function isEqualValues(context, a, b) {
  if (!a || !b)
    return a === b;
  if (a.length !== b.length)
    return !1;
  for (let index = 0; index < a.length; index++) {
    const blockA = a.at(index), blockB = b.at(index);
    if (!blockA || !blockB || !isEqualBlocks(context, blockA, blockB))
      return !1;
  }
  return !0;
}
function isEqualBlocks(context, a, b) {
  return a._type !== b._type ? !1 : a._type === context.schema.block.name && b._type === context.schema.block.name ? isEqualTextBlocks(context, a, b) : isEqualPortableTextObjects(a, b);
}
function isEqualTextBlocks(context, a, b) {
  return !isTextBlock(context, a) || !isTextBlock(context, b) || a._key !== b._key || a.style !== b.style || a.listItem !== b.listItem || a.level !== b.level || "markDefs" in a && "markDefs" in b && (!Array.isArray(a.markDefs) || !Array.isArray(b.markDefs) || !isEqualMarkDefs(a.markDefs, b.markDefs)) || !isEqualChildren(a.children, b.children) ? !1 : isEqualProps(a, b, ["_key", "_type", "style", "listItem", "level", "markDefs", "children"]);
}
function isEqualProps(a, b, excludeKeys) {
  const keysA = Object.keys(a).filter((key) => !excludeKeys.includes(key)), keysB = Object.keys(b).filter((key) => !excludeKeys.includes(key));
  if (keysA.length !== keysB.length)
    return !1;
  for (const key of keysA) {
    if (!(key in a) || !(key in b))
      return !1;
    const valueA = a[key], valueB = b[key];
    if (valueA !== valueB && !isDeepEqual(valueA, valueB))
      return !1;
  }
  return !0;
}
function isEqualInlineObjects(a, b) {
  return a._key !== b._key || a._type !== b._type ? !1 : isEqualProps(a, b, ["_key", "_type"]);
}
function isEqualMarks(a, b) {
  if (!a || !b)
    return a === b;
  if (a.length !== b.length)
    return !1;
  for (let index = 0; index < a.length; index++)
    if (a.at(index) !== b.at(index))
      return !1;
  return !0;
}
function isEqualSpans(a, b) {
  return a._key !== b._key || a._type !== b._type || a.text !== b.text || !isEqualMarks(a.marks, b.marks) ? !1 : isEqualProps(a, b, ["_key", "_type", "text", "marks"]);
}
function isEqualMarkDefs(a, b) {
  if (a.length !== b.length)
    return !1;
  for (let index = 0; index < a.length; index++) {
    const markDefA = a.at(index), markDefB = b.at(index);
    if (!markDefA || !markDefB || !isDeepEqual(markDefA, markDefB))
      return !1;
  }
  return !0;
}
function isEqualChildren(a, b) {
  if (a.length !== b.length)
    return !1;
  for (let index = 0; index < a.length; index++) {
    const childA = a.at(index), childB = b.at(index);
    if (!childA || !childB || !isEqualChild(childA, childB))
      return !1;
  }
  return !0;
}
function isEqualChild(a, b) {
  return a._type === "span" && b._type === "span" ? isEqualSpans(a, b) : isEqualInlineObjects(a, b);
}
function isEqualPortableTextObjects(a, b) {
  return a._key !== b._key || a._type !== b._type ? !1 : isEqualProps(a, b, ["_key", "_type"]);
}
function isDeepEqual(data, other) {
  return isDeepEqualImplementation(data, other);
}
function isDeepEqualImplementation(data, other) {
  if (data === other || Object.is(data, other))
    return !0;
  if (typeof data != "object" || typeof other != "object" || data === null || other === null || Object.getPrototypeOf(data) !== Object.getPrototypeOf(other))
    return !1;
  if (Array.isArray(data))
    return isDeepEqualArrays(data, other);
  if (data instanceof Map)
    return isDeepEqualMaps(data, other);
  if (data instanceof Set)
    return isDeepEqualSets(data, other);
  if (data instanceof Date)
    return data.getTime() === other.getTime();
  if (data instanceof RegExp)
    return data.toString() === other.toString();
  if (Object.keys(data).length !== Object.keys(other).length)
    return !1;
  for (const [key, value] of Object.entries(data))
    if (!(key in other) || !isDeepEqualImplementation(
      value,
      // @ts-expect-error [ts7053] - We already checked that `other` has `key`
      other[key]
    ))
      return !1;
  return !0;
}
function isDeepEqualArrays(data, other) {
  if (data.length !== other.length)
    return !1;
  for (const [index, item] of data.entries())
    if (!isDeepEqualImplementation(item, other[index]))
      return !1;
  return !0;
}
function isDeepEqualMaps(data, other) {
  if (data.size !== other.size)
    return !1;
  for (const [key, value] of data.entries())
    if (!other.has(key) || !isDeepEqualImplementation(value, other.get(key)))
      return !1;
  return !0;
}
function isDeepEqualSets(data, other) {
  if (data.size !== other.size)
    return !1;
  const otherCopy = [...other];
  for (const dataItem of data) {
    let isFound = !1;
    for (const [index, otherItem] of otherCopy.entries())
      if (isDeepEqualImplementation(dataItem, otherItem)) {
        isFound = !0, otherCopy.splice(index, 1);
        break;
      }
    if (!isFound)
      return !1;
  }
  return !0;
}
const VOID_CHILD_KEY = "void-child";
function toSlateBlock(block, {
  schemaTypes
}) {
  const {
    _type,
    _key,
    ...rest
  } = block;
  if (block && block._type === schemaTypes.block.name) {
    const textBlock = block;
    let hasInlines2 = !1;
    const hasMissingMarkDefs = typeof textBlock.markDefs > "u", hasMissingChildren = typeof textBlock.children > "u", children = (textBlock.children || []).map((child) => {
      const {
        _type: childType,
        _key: childKey,
        ...childProps
      } = child, propKeys = Object.keys(childProps);
      return childType === void 0 && propKeys.length === 1 && propKeys.at(0) === "text" ? {
        _key: childKey,
        _type: schemaTypes.span.name,
        text: childProps.text
      } : childType !== schemaTypes.span.name ? (hasInlines2 = !0, {
        _type: childType,
        _key: childKey,
        children: [{
          _key: VOID_CHILD_KEY,
          _type: schemaTypes.span.name,
          text: "",
          marks: []
        }],
        value: childProps,
        __inline: !0
      }) : child;
    });
    return !hasMissingMarkDefs && !hasMissingChildren && !hasInlines2 && Element$2.isElement(block) ? block : {
      _type,
      _key,
      ...rest,
      children
    };
  }
  return {
    _type,
    _key,
    children: [{
      _key: VOID_CHILD_KEY,
      _type: "span",
      text: "",
      marks: []
    }],
    value: rest
  };
}
function fromSlateBlock(block, textBlockType) {
  const {
    _key,
    _type
  } = block;
  if (!_key || !_type)
    throw new Error("Not a valid block");
  if (_type === textBlockType && "children" in block && Array.isArray(block.children) && _key) {
    let hasInlines2 = !1;
    const children = block.children.map((child) => {
      const {
        _type: _cType
      } = child;
      if ("value" in child && _cType !== "span") {
        hasInlines2 = !0;
        const {
          value: v,
          _key: k,
          _type: t,
          __inline: _i,
          children: _c,
          ...rest
        } = child;
        return {
          ...rest,
          ...v,
          _key: k,
          _type: t
        };
      }
      return child;
    });
    return hasInlines2 ? {
      ...block,
      children,
      _key,
      _type
    } : block;
  }
  const blockValue = "value" in block && block.value;
  return {
    _key,
    _type,
    ...typeof blockValue == "object" ? blockValue : {}
  };
}
function isEqualToEmptyEditor(initialValue, blocks, schemaTypes) {
  if (!blocks || blocks.length !== 1)
    return !1;
  const firstBlock = blocks.at(0);
  if (!firstBlock)
    return !0;
  if (!Element$2.isElement(firstBlock) || firstBlock._type !== schemaTypes.block.name || "listItem" in firstBlock || !("style" in firstBlock) || firstBlock.style !== schemaTypes.styles.at(0)?.name || !Array.isArray(firstBlock.children) || firstBlock.children.length !== 1)
    return !1;
  const firstChild = firstBlock.children.at(0);
  return !(!firstChild || !Text$1.isText(firstChild) || !("_type" in firstChild) || firstChild._type !== schemaTypes.span.name || firstChild.text !== "" || firstChild.marks?.join("") || "markDefs" in firstBlock && Array.isArray(firstBlock.markDefs) && firstBlock.markDefs.length > 0 || Object.keys(firstBlock).some((key) => key !== "_type" && key !== "_key" && key !== "children" && key !== "markDefs" && key !== "style") || isEqualValues({
    schema: schemaTypes
  }, initialValue, [firstBlock]));
}
function getFocusBlock({
  editor
}) {
  if (!editor.selection)
    return [void 0, void 0];
  try {
    return Editor.node(editor, editor.selection.focus.path.slice(0, 1)) ?? [void 0, void 0];
  } catch {
    return [void 0, void 0];
  }
}
function getFocusSpan({
  editor
}) {
  if (!editor.selection)
    return [void 0, void 0];
  try {
    const [focusBlock] = getFocusBlock({
      editor
    });
    if (!focusBlock)
      return [void 0, void 0];
    if (!editor.isTextBlock(focusBlock))
      return [void 0, void 0];
    const [node2, path2] = Editor.node(editor, editor.selection.focus.path.slice(0, 2));
    if (editor.isTextSpan(node2))
      return [node2, path2];
  } catch {
    return [void 0, void 0];
  }
  return [void 0, void 0];
}
function getPointBlock({
  editor,
  point: point2
}) {
  try {
    const [block] = Editor.node(editor, point2.path.slice(0, 1)) ?? [void 0, void 0];
    return block ? [block, point2.path.slice(0, 1)] : [void 0, void 0];
  } catch {
    return [void 0, void 0];
  }
}
function getFocusChild({
  editor
}) {
  const [focusBlock, focusBlockPath] = getFocusBlock({
    editor
  }), childIndex = editor.selection?.focus.path.at(1);
  if (!focusBlock || !focusBlockPath || childIndex === void 0)
    return [void 0, void 0];
  try {
    const focusChild = Node$1.child(focusBlock, childIndex);
    return focusChild ? [focusChild, [...focusBlockPath, childIndex]] : [void 0, void 0];
  } catch {
    return [void 0, void 0];
  }
}
function getPointChild({
  editor,
  point: point2
}) {
  const [block, blockPath] = getPointBlock({
    editor,
    point: point2
  }), childIndex = point2.path.at(1);
  if (!block || !blockPath || childIndex === void 0)
    return [void 0, void 0];
  try {
    const pointChild = Node$1.child(block, childIndex);
    return pointChild ? [pointChild, [...blockPath, childIndex]] : [void 0, void 0];
  } catch {
    return [void 0, void 0];
  }
}
function getFirstBlock({
  editor
}) {
  if (editor.children.length === 0)
    return [void 0, void 0];
  const firstBlockPath = Editor.start(editor, []).path.at(0);
  try {
    return firstBlockPath !== void 0 ? Editor.node(editor, [firstBlockPath]) ?? [void 0, void 0] : [void 0, void 0];
  } catch {
    return [void 0, void 0];
  }
}
function getLastBlock({
  editor
}) {
  if (editor.children.length === 0)
    return [void 0, void 0];
  const lastBlockPath = Editor.end(editor, []).path.at(0);
  try {
    return lastBlockPath !== void 0 ? Editor.node(editor, [lastBlockPath]) ?? [void 0, void 0] : [void 0, void 0];
  } catch {
    return [void 0, void 0];
  }
}
function getNodeBlock({
  editor,
  schema,
  node: node2
}) {
  if (Editor.isEditor(node2))
    return;
  if (isBlockElement({
    editor,
    schema
  }, node2))
    return elementToBlock({
      schema,
      element: node2
    });
  const parent2 = Array.from(Editor.nodes(editor, {
    mode: "highest",
    at: [],
    match: (n2) => isBlockElement({
      editor,
      schema
    }, n2) && n2.children.some((child) => child._key === node2._key)
  })).at(0)?.at(0);
  return Element$2.isElement(parent2) ? elementToBlock({
    schema,
    element: parent2
  }) : void 0;
}
function elementToBlock({
  schema,
  element
}) {
  return fromSlateBlock(element, schema.block.name);
}
function isBlockElement({
  editor,
  schema
}, node2) {
  return Element$2.isElement(node2) && !editor.isInline(node2) && (schema.block.name === node2._type || schema.blockObjects.some((blockObject) => blockObject.name === node2._type));
}
function isListItemActive({
  editor,
  listItem
}) {
  if (!editor.selection)
    return !1;
  const selectedBlocks = [...Editor.nodes(editor, {
    at: editor.selection,
    match: (node2) => editor.isTextBlock(node2)
  })];
  return selectedBlocks.length > 0 ? selectedBlocks.every(([node2]) => editor.isListBlock(node2) && node2.listItem === listItem) : !1;
}
function isStyleActive({
  editor,
  style
}) {
  if (!editor.selection)
    return !1;
  const selectedBlocks = [...Editor.nodes(editor, {
    at: editor.selection,
    match: (node2) => editor.isTextBlock(node2)
  })];
  return selectedBlocks.length > 0 ? selectedBlocks.every(([node2]) => node2.style === style) : !1;
}
function slateRangeToSelection({
  schema,
  editor,
  range: range2
}) {
  const [anchorBlock] = getPointBlock({
    editor,
    point: range2.anchor
  }), [focusBlock] = getPointBlock({
    editor,
    point: range2.focus
  });
  if (!anchorBlock || !focusBlock)
    return null;
  const [anchorChild] = anchorBlock._type === schema.block.name ? getPointChild({
    editor,
    point: range2.anchor
  }) : [void 0, void 0], [focusChild] = focusBlock._type === schema.block.name ? getPointChild({
    editor,
    point: range2.focus
  }) : [void 0, void 0], selection = {
    anchor: {
      path: [{
        _key: anchorBlock._key
      }],
      offset: range2.anchor.offset
    },
    focus: {
      path: [{
        _key: focusBlock._key
      }],
      offset: range2.focus.offset
    },
    backward: Range.isBackward(range2)
  };
  return anchorChild && (selection.anchor.path.push("children"), selection.anchor.path.push({
    _key: anchorChild._key
  })), focusChild && (selection.focus.path.push("children"), selection.focus.path.push({
    _key: focusChild._key
  })), selection;
}
function slatePointToSelectionPoint({
  schema,
  editor,
  point: point2
}) {
  const [block] = getPointBlock({
    editor,
    point: point2
  });
  if (!block)
    return;
  const [child] = block._type === schema.block.name ? getPointChild({
    editor,
    point: point2
  }) : [void 0, void 0];
  return child ? {
    path: [{
      _key: block._key
    }, "children", {
      _key: child._key
    }],
    offset: point2.offset
  } : {
    path: [{
      _key: block._key
    }],
    offset: point2.offset
  };
}
function getEventPosition({
  editorActor,
  slateEditor,
  event
}) {
  if (editorActor.getSnapshot().matches({
    setup: "setting up"
  }))
    return;
  const eventNode = getEventNode({
    slateEditor,
    event
  });
  if (!eventNode)
    return;
  const eventBlock = getNodeBlock({
    editor: slateEditor,
    schema: editorActor.getSnapshot().context.schema,
    node: eventNode
  }), eventPositionBlock = getEventPositionBlock({
    node: eventNode,
    slateEditor,
    event
  }), eventSelection = getEventSelection({
    schema: editorActor.getSnapshot().context.schema,
    slateEditor,
    event
  });
  if (eventBlock && eventPositionBlock && !eventSelection && !Editor.isEditor(eventNode))
    return {
      block: eventPositionBlock,
      isEditor: !1,
      selection: {
        anchor: getBlockStartPoint({
          context: editorActor.getSnapshot().context,
          block: {
            node: eventBlock,
            path: [{
              _key: eventBlock._key
            }]
          }
        }),
        focus: getBlockEndPoint({
          context: editorActor.getSnapshot().context,
          block: {
            node: eventBlock,
            path: [{
              _key: eventBlock._key
            }]
          }
        })
      }
    };
  if (!eventPositionBlock || !eventSelection)
    return;
  const eventSelectionFocusBlockKey = getBlockKeyFromSelectionPoint(eventSelection.focus);
  if (eventSelectionFocusBlockKey !== void 0)
    return isSelectionCollapsed(eventSelection) && eventBlock && eventSelectionFocusBlockKey !== eventBlock._key ? {
      block: eventPositionBlock,
      isEditor: !1,
      selection: {
        anchor: getBlockStartPoint({
          context: editorActor.getSnapshot().context,
          block: {
            node: eventBlock,
            path: [{
              _key: eventBlock._key
            }]
          }
        }),
        focus: getBlockEndPoint({
          context: editorActor.getSnapshot().context,
          block: {
            node: eventBlock,
            path: [{
              _key: eventBlock._key
            }]
          }
        })
      }
    } : {
      block: eventPositionBlock,
      isEditor: Editor.isEditor(eventNode),
      selection: eventSelection
    };
}
function getEventNode({
  slateEditor,
  event
}) {
  if (!DOMEditor.hasTarget(slateEditor, event.target))
    return;
  let node2;
  try {
    node2 = DOMEditor.toSlateNode(slateEditor, event.target);
  } catch (error) {
    console.error(error);
  }
  return node2;
}
function getEventPositionBlock({
  node: node2,
  slateEditor,
  event
}) {
  const [firstBlock] = getFirstBlock({
    editor: slateEditor
  });
  if (!firstBlock)
    return;
  let firstBlockElement;
  try {
    firstBlockElement = DOMEditor.toDOMNode(slateEditor, firstBlock);
  } catch (error) {
    console.error(error);
  }
  if (!firstBlockElement)
    return;
  const firstBlockRect = firstBlockElement.getBoundingClientRect();
  if (event.pageY < firstBlockRect.top)
    return "start";
  const [lastBlock] = getLastBlock({
    editor: slateEditor
  });
  if (!lastBlock)
    return;
  let lastBlockElement;
  try {
    lastBlockElement = DOMEditor.toDOMNode(slateEditor, lastBlock);
  } catch (error) {
    console.error(error);
  }
  if (!lastBlockElement)
    return;
  const lastBlockRef = lastBlockElement.getBoundingClientRect();
  if (event.pageY > lastBlockRef.bottom)
    return "end";
  let element;
  try {
    element = DOMEditor.toDOMNode(slateEditor, node2);
  } catch (error) {
    console.error(error);
  }
  if (!element)
    return;
  const elementRect = element.getBoundingClientRect(), top = elementRect.top, height = elementRect.height;
  return Math.abs(top - event.pageY) < height / 2 ? "start" : "end";
}
function getEventSelection({
  schema,
  slateEditor,
  event
}) {
  const range2 = getSlateRangeFromEvent(slateEditor, event);
  return range2 ? slateRangeToSelection({
    schema,
    editor: slateEditor,
    range: range2
  }) : null;
}
function getSlateRangeFromEvent(editor, event) {
  if (!event.target || !isDOMNode(event.target))
    return;
  const window2 = DOMEditor.getWindow(editor);
  let domRange;
  if (window2.document.caretPositionFromPoint !== void 0) {
    const position = window2.document.caretPositionFromPoint(event.clientX, event.clientY);
    if (position)
      try {
        domRange = window2.document.createRange(), domRange.setStart(position.offsetNode, position.offset), domRange.setEnd(position.offsetNode, position.offset);
      } catch {
      }
  } else if (window2.document.caretRangeFromPoint !== void 0)
    domRange = window2.document.caretRangeFromPoint(event.clientX, event.clientY) ?? void 0;
  else {
    console.warn("Neither caretPositionFromPoint nor caretRangeFromPoint is supported");
    return;
  }
  if (!domRange)
    return;
  let range2;
  try {
    range2 = DOMEditor.toSlateRange(editor, domRange, {
      exactMatch: !1,
      // It can still throw even with this option set to true
      suppressThrow: !1
    });
  } catch {
  }
  return range2;
}
function normalizePoint(point2, value) {
  if (!point2 || !value)
    return null;
  const newPath = [];
  let newOffset = point2.offset || 0;
  const blockKey = typeof point2.path[0] == "object" && "_key" in point2.path[0] && point2.path[0]._key, childKey = typeof point2.path[2] == "object" && "_key" in point2.path[2] && point2.path[2]._key, block = value.find((blk) => blk._key === blockKey);
  if (block)
    newPath.push({
      _key: block._key
    });
  else
    return null;
  if (block && point2.path[1] === "children") {
    if (!block.children || Array.isArray(block.children) && block.children.length === 0)
      return null;
    const child = Array.isArray(block.children) && block.children.find((cld) => cld._key === childKey);
    if (child)
      newPath.push("children"), newPath.push({
        _key: child._key
      }), newOffset = child.text && child.text.length >= point2.offset ? point2.offset : child.text && child.text.length || 0;
    else
      return null;
  }
  return {
    path: newPath,
    offset: newOffset
  };
}
function normalizeSelection(selection, value) {
  if (!selection || !value || value.length === 0)
    return null;
  let newAnchor = null, newFocus = null;
  const {
    anchor,
    focus
  } = selection;
  return anchor && value.find((blk) => isKeyedSegment(anchor.path[0]) && blk._key === anchor.path[0]._key) && (newAnchor = normalizePoint(anchor, value)), focus && value.find((blk) => isKeyedSegment(focus.path[0]) && blk._key === focus.path[0]._key) && (newFocus = normalizePoint(focus, value)), newAnchor && newFocus ? {
    anchor: newAnchor,
    focus: newFocus,
    backward: selection.backward
  } : null;
}
function toSlateRange(snapshot) {
  if (!snapshot.context.selection)
    return null;
  if (isEqualSelectionPoints(snapshot.context.selection.anchor, snapshot.context.selection.focus)) {
    const anchorPoint2 = toSlateSelectionPoint(snapshot, snapshot.context.selection.anchor, snapshot.context.selection.backward ? "backward" : "forward");
    return anchorPoint2 ? {
      anchor: anchorPoint2,
      focus: anchorPoint2
    } : null;
  }
  const anchorPoint = toSlateSelectionPoint(snapshot, snapshot.context.selection.anchor, snapshot.context.selection.backward ? "forward" : "backward"), focusPoint = toSlateSelectionPoint(snapshot, snapshot.context.selection.focus, snapshot.context.selection.backward ? "backward" : "forward");
  return !anchorPoint || !focusPoint ? null : {
    anchor: anchorPoint,
    focus: focusPoint
  };
}
function toSlateSelectionPoint(snapshot, selectionPoint, direction) {
  const blockKey = getBlockKeyFromSelectionPoint(selectionPoint);
  if (!blockKey)
    return;
  const blockIndex = snapshot.blockIndexMap.get(blockKey);
  if (blockIndex === void 0)
    return;
  const block = snapshot.context.value.at(blockIndex);
  if (!block)
    return;
  if (!isTextBlock(snapshot.context, block))
    return {
      path: [blockIndex, 0],
      offset: 0
    };
  let childKey = getChildKeyFromSelectionPoint({
    path: selectionPoint.path
  });
  const spanSelectionPoint = childKey ? void 0 : blockOffsetToSpanSelectionPoint({
    context: {
      schema: snapshot.context.schema,
      value: [block]
    },
    blockOffset: {
      path: [{
        _key: blockKey
      }],
      offset: selectionPoint.offset
    },
    direction
  });
  if (childKey = spanSelectionPoint ? getChildKeyFromSelectionPoint(spanSelectionPoint) : childKey, !childKey)
    return {
      path: [blockIndex, 0],
      offset: 0
    };
  let offset = spanSelectionPoint?.offset ?? selectionPoint.offset, childPath = [], childIndex = -1, pathChild;
  for (const child of block.children)
    if (childIndex++, child._key === childKey) {
      pathChild = child, isSpan(snapshot.context, child) ? childPath = [childIndex] : (childPath = [childIndex, 0], offset = 0);
      break;
    }
  return childPath.length === 0 ? {
    path: [blockIndex, 0],
    offset: 0
  } : {
    path: [blockIndex].concat(childPath),
    offset: isSpan(snapshot.context, pathChild) ? Math.min(pathChild.text.length, offset) : offset
  };
}
function useIsMounted() {
  const isMountedRef = useRef(!1);
  return useEffect(() => (isMountedRef.current = !0, () => {
    isMountedRef.current = !1;
  }), []), isMountedRef.current;
}
const useIsomorphicLayoutEffect = CAN_USE_DOM ? useLayoutEffect : useEffect;
function useMutationObserver(node2, callback, options) {
  const [mutationObserver] = useState(() => new MutationObserver(callback));
  useIsomorphicLayoutEffect(() => {
    mutationObserver.takeRecords();
  }), useEffect(() => {
    if (!node2.current)
      throw new Error("Failed to attach MutationObserver, `node` is undefined");
    return mutationObserver.observe(node2.current, options), () => mutationObserver.disconnect();
  }, [mutationObserver, node2, options]);
}
const EditorContext = createContext(null), useSlateStatic = () => {
  const editor = useContext(EditorContext);
  if (!editor)
    throw new Error("The `useSlateStatic` hook must be used inside the <Slate> component's context.");
  return editor;
}, ReactEditor = DOMEditor, RESOLVE_DELAY = 25, FLUSH_DELAY = 200, debug = (..._) => {
}, isDataTransfer = (value) => value?.constructor.name === "DataTransfer";
function createAndroidInputManager({
  editor,
  scheduleOnDOMSelectionChange,
  onDOMSelectionChange
}) {
  let flushing = !1, compositionEndTimeoutId = null, flushTimeoutId = null, actionTimeoutId = null, idCounter = 0, insertPositionHint = !1;
  const applyPendingSelection = () => {
    const pendingSelection = EDITOR_TO_PENDING_SELECTION.get(editor);
    if (EDITOR_TO_PENDING_SELECTION.delete(editor), pendingSelection) {
      const {
        selection
      } = editor, normalized = normalizeRange(editor, pendingSelection);
      normalized && (!selection || !Range.equals(normalized, selection)) && Transforms.select(editor, normalized);
    }
  }, performAction = () => {
    const action = EDITOR_TO_PENDING_ACTION.get(editor);
    if (EDITOR_TO_PENDING_ACTION.delete(editor), !!action) {
      if (action.at) {
        const target = Point.isPoint(action.at) ? normalizePoint$1(editor, action.at) : normalizeRange(editor, action.at);
        if (!target)
          return;
        const targetRange2 = Editor.range(editor, target);
        (!editor.selection || !Range.equals(editor.selection, targetRange2)) && Transforms.select(editor, target);
      }
      action.run();
    }
  }, flush = () => {
    if (flushTimeoutId && (clearTimeout(flushTimeoutId), flushTimeoutId = null), actionTimeoutId && (clearTimeout(actionTimeoutId), actionTimeoutId = null), !hasPendingDiffs() && !hasPendingAction()) {
      applyPendingSelection();
      return;
    }
    flushing || (flushing = !0, setTimeout(() => flushing = !1)), hasPendingAction() && (flushing = "action");
    const selectionRef = editor.selection && Editor.rangeRef(editor, editor.selection, {
      affinity: "forward"
    });
    EDITOR_TO_USER_MARKS.set(editor, editor.marks), debug("flush", EDITOR_TO_PENDING_ACTION.get(editor), EDITOR_TO_PENDING_DIFFS.get(editor));
    let scheduleSelectionChange = hasPendingDiffs(), diff2;
    for (; diff2 = EDITOR_TO_PENDING_DIFFS.get(editor)?.[0]; ) {
      const pendingMarks = EDITOR_TO_PENDING_INSERTION_MARKS.get(editor);
      pendingMarks !== void 0 && (EDITOR_TO_PENDING_INSERTION_MARKS.delete(editor), editor.marks = pendingMarks), pendingMarks && insertPositionHint === !1 && (insertPositionHint = null, debug("insert after mark placeholder"));
      const range2 = targetRange(diff2);
      (!editor.selection || !Range.equals(editor.selection, range2)) && Transforms.select(editor, range2), diff2.diff.text ? Editor.insertText(editor, diff2.diff.text) : Editor.deleteFragment(editor), EDITOR_TO_PENDING_DIFFS.set(
        editor,
        // biome-ignore lint/suspicious/noNonNullAssertedOptionalChain: Slate upstream pattern — diffs guaranteed to exist in loop
        EDITOR_TO_PENDING_DIFFS.get(editor)?.filter(({
          id
        }) => id !== diff2.id)
      ), verifyDiffState(editor, diff2) || (scheduleSelectionChange = !1, EDITOR_TO_PENDING_ACTION.delete(editor), EDITOR_TO_USER_MARKS.delete(editor), flushing = "action", EDITOR_TO_PENDING_SELECTION.delete(editor), scheduleOnDOMSelectionChange.cancel(), onDOMSelectionChange.cancel(), selectionRef?.unref());
    }
    const selection = selectionRef?.unref();
    if (selection && !EDITOR_TO_PENDING_SELECTION.get(editor) && (!editor.selection || !Range.equals(selection, editor.selection)) && Transforms.select(editor, selection), hasPendingAction()) {
      performAction();
      return;
    }
    scheduleSelectionChange && scheduleOnDOMSelectionChange(), scheduleOnDOMSelectionChange.flush(), onDOMSelectionChange.flush(), applyPendingSelection();
    const userMarks = EDITOR_TO_USER_MARKS.get(editor);
    EDITOR_TO_USER_MARKS.delete(editor), userMarks !== void 0 && (editor.marks = userMarks, editor.onChange());
  }, handleCompositionEnd = (_event) => {
    compositionEndTimeoutId && clearTimeout(compositionEndTimeoutId), compositionEndTimeoutId = setTimeout(() => {
      IS_COMPOSING.set(editor, !1), flush();
    }, RESOLVE_DELAY);
  }, handleCompositionStart = (_event) => {
    IS_COMPOSING.set(editor, !0), compositionEndTimeoutId && (clearTimeout(compositionEndTimeoutId), compositionEndTimeoutId = null);
  }, updatePlaceholderVisibility = (forceHide = !1) => {
    const placeholderElement = EDITOR_TO_PLACEHOLDER_ELEMENT.get(editor);
    if (placeholderElement) {
      if (hasPendingDiffs() || forceHide) {
        placeholderElement.style.display = "none";
        return;
      }
      placeholderElement.style.removeProperty("display");
    }
  }, storeDiff = (path2, diff2) => {
    const pendingDiffs = EDITOR_TO_PENDING_DIFFS.get(editor) ?? [];
    EDITOR_TO_PENDING_DIFFS.set(editor, pendingDiffs);
    const target = Node$1.leaf(editor, path2), idx = pendingDiffs.findIndex((change) => Path.equals(change.path, path2));
    if (idx < 0) {
      normalizeStringDiff(target.text, diff2) && pendingDiffs.push({
        path: path2,
        diff: diff2,
        id: idCounter++
      }), updatePlaceholderVisibility();
      return;
    }
    const merged = mergeStringDiffs(target.text, pendingDiffs[idx].diff, diff2);
    if (!merged) {
      pendingDiffs.splice(idx, 1), updatePlaceholderVisibility();
      return;
    }
    pendingDiffs[idx] = {
      ...pendingDiffs[idx],
      diff: merged
    };
  }, scheduleAction = (run, {
    at
  } = {}) => {
    insertPositionHint = !1, EDITOR_TO_PENDING_SELECTION.delete(editor), scheduleOnDOMSelectionChange.cancel(), onDOMSelectionChange.cancel(), hasPendingAction() && flush(), EDITOR_TO_PENDING_ACTION.set(editor, {
      at,
      run
    }), actionTimeoutId = setTimeout(flush);
  }, handleDOMBeforeInput = (event) => {
    if (flushTimeoutId && (clearTimeout(flushTimeoutId), flushTimeoutId = null), IS_NODE_MAP_DIRTY.get(editor))
      return;
    const {
      inputType: type
    } = event;
    let targetRange2 = null;
    const data = event.dataTransfer || event.data || void 0;
    insertPositionHint !== !1 && type !== "insertText" && type !== "insertCompositionText" && (insertPositionHint = !1);
    let [nativeTargetRange] = event.getTargetRanges();
    nativeTargetRange && (targetRange2 = ReactEditor.toSlateRange(editor, nativeTargetRange, {
      exactMatch: !1,
      suppressThrow: !0
    }));
    const domSelection = ReactEditor.getWindow(editor).getSelection();
    if (!targetRange2 && domSelection && (nativeTargetRange = domSelection, targetRange2 = ReactEditor.toSlateRange(editor, domSelection, {
      exactMatch: !1,
      suppressThrow: !0
    })), targetRange2 = targetRange2 ?? editor.selection, !targetRange2)
      return;
    let canStoreDiff = !0;
    if (type.startsWith("delete")) {
      const direction = type.endsWith("Backward") ? "backward" : "forward";
      let [start2, end2] = Range.edges(targetRange2), [leaf2, path2] = Editor.leaf(editor, start2.path);
      if (Range.isExpanded(targetRange2) && leaf2.text.length === start2.offset && end2.offset === 0) {
        const next2 = Editor.next(editor, {
          at: start2.path,
          match: Text$1.isText
        });
        next2 && Path.equals(next2[1], end2.path) && (direction === "backward" ? (targetRange2 = {
          anchor: end2,
          focus: end2
        }, start2 = end2, [leaf2, path2] = next2) : (targetRange2 = {
          anchor: start2,
          focus: start2
        }, end2 = start2));
      }
      const diff2 = {
        text: "",
        start: start2.offset,
        end: end2.offset
      }, relevantPendingDiffs = EDITOR_TO_PENDING_DIFFS.get(editor)?.find((change) => Path.equals(change.path, path2)), diffs = relevantPendingDiffs ? [relevantPendingDiffs.diff, diff2] : [diff2];
      if (applyStringDiff(leaf2.text, ...diffs).length === 0 && (canStoreDiff = !1), Range.isExpanded(targetRange2)) {
        if (canStoreDiff && Path.equals(targetRange2.anchor.path, targetRange2.focus.path)) {
          const point2 = {
            path: targetRange2.anchor.path,
            offset: start2.offset
          }, range2 = Editor.range(editor, point2, point2);
          return handleUserSelect(range2), storeDiff(targetRange2.anchor.path, {
            text: "",
            end: end2.offset,
            start: start2.offset
          });
        }
        return scheduleAction(() => Editor.deleteFragment(editor, {
          direction
        }), {
          at: targetRange2
        });
      }
    }
    switch (type) {
      case "deleteByComposition":
      case "deleteByCut":
      case "deleteByDrag":
        return scheduleAction(() => Editor.deleteFragment(editor), {
          at: targetRange2
        });
      case "deleteContent":
      case "deleteContentForward": {
        const {
          anchor
        } = targetRange2;
        if (canStoreDiff && Range.isCollapsed(targetRange2)) {
          const targetNode = Node$1.leaf(editor, anchor.path);
          if (anchor.offset < targetNode.text.length)
            return storeDiff(anchor.path, {
              text: "",
              start: anchor.offset,
              end: anchor.offset + 1
            });
        }
        return scheduleAction(() => Editor.deleteForward(editor), {
          at: targetRange2
        });
      }
      case "deleteContentBackward": {
        const {
          anchor
        } = targetRange2, nativeCollapsed = isDOMSelection(nativeTargetRange) ? nativeTargetRange.isCollapsed : !!nativeTargetRange?.collapsed;
        return canStoreDiff && nativeCollapsed && Range.isCollapsed(targetRange2) && anchor.offset > 0 ? storeDiff(anchor.path, {
          text: "",
          start: anchor.offset - 1,
          end: anchor.offset
        }) : scheduleAction(() => Editor.deleteBackward(editor), {
          at: targetRange2
        });
      }
      case "deleteEntireSoftLine":
        return scheduleAction(() => {
          Editor.deleteBackward(editor, {
            unit: "line"
          }), Editor.deleteForward(editor, {
            unit: "line"
          });
        }, {
          at: targetRange2
        });
      case "deleteHardLineBackward":
        return scheduleAction(() => Editor.deleteBackward(editor, {
          unit: "block"
        }), {
          at: targetRange2
        });
      case "deleteSoftLineBackward":
        return scheduleAction(() => Editor.deleteBackward(editor, {
          unit: "line"
        }), {
          at: targetRange2
        });
      case "deleteHardLineForward":
        return scheduleAction(() => Editor.deleteForward(editor, {
          unit: "block"
        }), {
          at: targetRange2
        });
      case "deleteSoftLineForward":
        return scheduleAction(() => Editor.deleteForward(editor, {
          unit: "line"
        }), {
          at: targetRange2
        });
      case "deleteWordBackward":
        return scheduleAction(() => Editor.deleteBackward(editor, {
          unit: "word"
        }), {
          at: targetRange2
        });
      case "deleteWordForward":
        return scheduleAction(() => Editor.deleteForward(editor, {
          unit: "word"
        }), {
          at: targetRange2
        });
      case "insertLineBreak":
        return scheduleAction(() => Editor.insertSoftBreak(editor), {
          at: targetRange2
        });
      case "insertParagraph":
        return scheduleAction(() => Editor.insertBreak(editor), {
          at: targetRange2
        });
      case "insertCompositionText":
      case "deleteCompositionText":
      case "insertFromComposition":
      case "insertFromDrop":
      case "insertFromPaste":
      case "insertFromYank":
      case "insertReplacementText":
      case "insertText": {
        if (isDataTransfer(data))
          return scheduleAction(() => ReactEditor.insertData(editor, data), {
            at: targetRange2
          });
        let text = data ?? "";
        if (EDITOR_TO_PENDING_INSERTION_MARKS.get(editor) && (text = text.replace("\uFEFF", "")), type === "insertText" && /.*\n.*\n$/.test(text) && (text = text.slice(0, -1)), text.includes(`
`))
          return scheduleAction(() => {
            const parts = text.split(`
`);
            parts.forEach((line, i) => {
              line && Editor.insertText(editor, line), i !== parts.length - 1 && Editor.insertSoftBreak(editor);
            });
          }, {
            at: targetRange2
          });
        if (Path.equals(targetRange2.anchor.path, targetRange2.focus.path)) {
          const [start2, end2] = Range.edges(targetRange2), diff2 = {
            start: start2.offset,
            end: end2.offset,
            text
          };
          if (text && insertPositionHint && type === "insertCompositionText") {
            const hintPosition = insertPositionHint.start + insertPositionHint.text.search(/\S|$/);
            diff2.start + diff2.text.search(/\S|$/) === hintPosition + 1 && diff2.end === insertPositionHint.start + insertPositionHint.text.length ? (diff2.start -= 1, insertPositionHint = null, scheduleFlush()) : insertPositionHint = !1;
          } else type === "insertText" ? insertPositionHint === null ? insertPositionHint = diff2 : insertPositionHint && Range.isCollapsed(targetRange2) && insertPositionHint.end + insertPositionHint.text.length === start2.offset ? insertPositionHint = {
            ...insertPositionHint,
            text: insertPositionHint.text + text
          } : insertPositionHint = !1 : insertPositionHint = !1;
          if (canStoreDiff) {
            const currentSelection = editor.selection;
            if (storeDiff(start2.path, diff2), currentSelection) {
              const newPoint = {
                path: start2.path,
                offset: start2.offset + text.length
              };
              scheduleAction(() => {
                Transforms.select(editor, {
                  anchor: newPoint,
                  focus: newPoint
                });
              }, {
                at: newPoint
              });
            }
            return;
          }
        }
        return scheduleAction(() => Editor.insertText(editor, text), {
          at: targetRange2
        });
      }
    }
  }, hasPendingAction = () => !!EDITOR_TO_PENDING_ACTION.get(editor), hasPendingDiffs = () => !!EDITOR_TO_PENDING_DIFFS.get(editor)?.length, hasPendingChanges = () => hasPendingAction() || hasPendingDiffs(), isFlushing = () => flushing, handleUserSelect = (range2) => {
    EDITOR_TO_PENDING_SELECTION.set(editor, range2), flushTimeoutId && (clearTimeout(flushTimeoutId), flushTimeoutId = null);
    const {
      selection
    } = editor;
    if (!range2)
      return;
    const pathChanged = !selection || !Path.equals(selection.anchor.path, range2.anchor.path), parentPathChanged = !selection || !Path.equals(selection.anchor.path.slice(0, -1), range2.anchor.path.slice(0, -1));
    (pathChanged && insertPositionHint || parentPathChanged) && (insertPositionHint = !1), (pathChanged || hasPendingDiffs()) && (flushTimeoutId = setTimeout(flush, FLUSH_DELAY));
  }, handleInput = () => {
    (hasPendingAction() || !hasPendingDiffs()) && flush();
  }, handleKeyDown = (_) => {
    hasPendingDiffs() || (updatePlaceholderVisibility(!0), setTimeout(updatePlaceholderVisibility));
  }, scheduleFlush = () => {
    hasPendingAction() || (actionTimeoutId = setTimeout(flush));
  };
  return {
    flush,
    scheduleFlush,
    hasPendingDiffs,
    hasPendingAction,
    hasPendingChanges,
    isFlushing,
    handleUserSelect,
    handleCompositionEnd,
    handleCompositionStart,
    handleDOMBeforeInput,
    handleKeyDown,
    handleDomMutations: (mutations) => {
      hasPendingDiffs() || hasPendingAction() || mutations.some((mutation) => isTrackedMutation(editor, mutation, mutations)) && EDITOR_TO_FORCE_RENDER.get(editor)?.();
    },
    handleInput
  };
}
const MUTATION_OBSERVER_CONFIG$1 = {
  subtree: !0,
  childList: !0,
  characterData: !0
}, useAndroidInputManager = IS_ANDROID ? ({
  node: node2,
  ...options
}) => {
  if (!IS_ANDROID)
    return null;
  const editor = useSlateStatic(), isMounted = useIsMounted(), [inputManager] = useState(() => createAndroidInputManager({
    editor,
    ...options
  }));
  return useMutationObserver(node2, inputManager.handleDomMutations, MUTATION_OBSERVER_CONFIG$1), EDITOR_TO_SCHEDULE_FLUSH.set(editor, inputManager.scheduleFlush), isMounted && inputManager.flush(), inputManager;
} : () => null;
class ChildrenHelper {
  /**
   * Sparse array of Slate node keys, each index corresponding to an index in
   * the children array
   *
   * Fetching the key for a Slate node is expensive, so we cache them here.
   */
  /**
   * The index of the next node to be read in the children array
   */
  constructor(editor, children) {
    this.editor = editor, this.children = children, this.cachedKeys = new Array(children.length), this.pointerIndex = 0;
  }
  /**
   * Read a given number of nodes, advancing the pointer by that amount
   */
  read(n2) {
    if (n2 === 1)
      return [this.children[this.pointerIndex++]];
    const slicedChildren = this.remaining(n2);
    return this.pointerIndex += n2, slicedChildren;
  }
  /**
   * Get the remaining children without advancing the pointer
   *
   * @param [maxChildren] Limit the number of children returned.
   */
  remaining(maxChildren) {
    return maxChildren === void 0 ? this.children.slice(this.pointerIndex) : this.children.slice(this.pointerIndex, this.pointerIndex + maxChildren);
  }
  /**
   * Whether all children have been read
   */
  get reachedEnd() {
    return this.pointerIndex >= this.children.length;
  }
  /**
   * Determine whether a node with a given key appears in the unread part of the
   * children array, and return its index relative to the current pointer if so
   *
   * Searching for the node object itself using indexOf is most efficient, but
   * will fail to locate nodes that have been modified. In this case, nodes
   * should be identified by their keys instead.
   *
   * Searching an array of keys using indexOf is very inefficient since fetching
   * the keys for all children in advance is very slow. Insead, if the node
   * search fails to return a value, fetch the keys of each remaining child one
   * by one and compare it to the known key.
   */
  lookAhead(node2, key) {
    const elementResult = this.children.indexOf(node2, this.pointerIndex);
    if (elementResult > -1)
      return elementResult - this.pointerIndex;
    for (let i = this.pointerIndex; i < this.children.length; i++) {
      const candidateNode = this.children[i];
      if (this.findKey(candidateNode, i) === key)
        return i - this.pointerIndex;
    }
    return -1;
  }
  /**
   * Convert an array of Slate nodes to an array of chunk leaves, each
   * containing the node and its key
   */
  toChunkLeaves(nodes2, startIndex) {
    return nodes2.map((node2, i) => ({
      type: "leaf",
      node: node2,
      key: this.findKey(node2, startIndex + i),
      index: startIndex + i
    }));
  }
  /**
   * Get the key for a Slate node, cached using the node's index
   */
  findKey(node2, index) {
    const cachedKey = this.cachedKeys[index];
    if (cachedKey)
      return cachedKey;
    const key = ReactEditor.findKey(this.editor, node2);
    return this.cachedKeys[index] = key, key;
  }
}
class ChunkTreeHelper {
  /**
   * The root of the chunk tree
   */
  /**
   * The ideal size of a chunk
   */
  /**
   * Whether debug mode is enabled
   *
   * If enabled, the pointer state will be checked for internal consistency
   * after each mutating operation.
   */
  /**
   * Whether the traversal has reached the end of the chunk tree
   *
   * When this is true, the pointerChunk and pointerIndex point to the last
   * top-level node in the chunk tree, although pointerNode returns null.
   */
  /**
   * The chunk containing the current node
   */
  /**
   * The index of the current node within pointerChunk
   *
   * Can be -1 to indicate that the pointer is before the start of the tree.
   */
  /**
   * Similar to a Slate path; tracks the path of pointerChunk relative to the
   * root.
   *
   * Used to move the pointer from the current chunk to the parent chunk more
   * efficiently.
   */
  /**
   * Indexing the current chunk's children has a slight time cost, which adds up
   * when traversing very large trees, so the current node is cached.
   *
   * A value of undefined means that the current node is not cached. This
   * property must be set to undefined whenever the pointer is moved, unless
   * the pointer is guaranteed to point to the same node that it did previously.
   */
  constructor(chunkTree, {
    chunkSize,
    debug: debug2
  }) {
    this.root = chunkTree, this.chunkSize = chunkSize, this.debug = debug2 ?? !1, this.pointerChunk = chunkTree, this.pointerIndex = -1, this.pointerIndexStack = [], this.reachedEnd = !1, this.validateState();
  }
  /**
   * Move the pointer to the next leaf in the chunk tree
   */
  readLeaf() {
    if (this.reachedEnd)
      return null;
    for (; ; )
      if (this.pointerIndex + 1 < this.pointerSiblings.length) {
        this.pointerIndex++, this.cachedPointerNode = void 0;
        break;
      } else {
        if (this.pointerChunk.type === "root")
          return this.reachedEnd = !0, null;
        this.exitChunk();
      }
    return this.validateState(), this.enterChunkUntilLeaf(!1), this.pointerNode;
  }
  /**
   * Move the pointer to the previous leaf in the chunk tree
   */
  returnToPreviousLeaf() {
    if (this.reachedEnd) {
      this.reachedEnd = !1, this.enterChunkUntilLeaf(!0);
      return;
    }
    for (; ; )
      if (this.pointerIndex >= 1) {
        this.pointerIndex--, this.cachedPointerNode = void 0;
        break;
      } else if (this.pointerChunk.type === "root") {
        this.pointerIndex = -1;
        return;
      } else
        this.exitChunk();
    this.validateState(), this.enterChunkUntilLeaf(!0);
  }
  /**
   * Insert leaves before the current leaf, leaving the pointer unchanged
   */
  insertBefore(leaves) {
    this.returnToPreviousLeaf(), this.insertAfter(leaves), this.readLeaf();
  }
  /**
   * Insert leaves after the current leaf, leaving the pointer on the last
   * inserted leaf
   *
   * The insertion algorithm first checks for any chunk we're currently at the
   * end of that can receive additional leaves. Next, it tries to insert leaves
   * at the starts of any subsequent chunks.
   *
   * Any remaining leaves are passed to rawInsertAfter to be chunked and
   * inserted at the highest possible level.
   */
  insertAfter(leaves) {
    if (leaves.length === 0)
      return;
    let beforeDepth = 0, afterDepth = 0;
    for (; this.pointerChunk.type === "chunk" && this.pointerIndex === this.pointerSiblings.length - 1; ) {
      const remainingCapacity = this.chunkSize - this.pointerSiblings.length, toInsertCount = Math.min(remainingCapacity, leaves.length);
      if (toInsertCount > 0) {
        const leavesToInsert = leaves.splice(0, toInsertCount);
        this.rawInsertAfter(leavesToInsert, beforeDepth);
      }
      this.exitChunk(), beforeDepth++;
    }
    if (leaves.length === 0)
      return;
    const rawInsertPointer = this.savePointer();
    let finalPointer = null;
    if (this.readLeaf())
      for (; this.pointerChunk.type === "chunk" && this.pointerIndex === 0; ) {
        const remainingCapacity = this.chunkSize - this.pointerSiblings.length, toInsertCount = Math.min(remainingCapacity, leaves.length);
        if (toInsertCount > 0) {
          const leavesToInsert = leaves.splice(-toInsertCount, toInsertCount);
          this.pointerIndex = -1, this.cachedPointerNode = void 0, this.rawInsertAfter(leavesToInsert, afterDepth), finalPointer || (finalPointer = this.savePointer());
        }
        this.exitChunk(), afterDepth++;
      }
    this.restorePointer(rawInsertPointer);
    const minDepth = Math.max(beforeDepth, afterDepth);
    this.rawInsertAfter(leaves, minDepth), finalPointer && this.restorePointer(finalPointer), this.validateState();
  }
  /**
   * Remove the current node and decrement the pointer, deleting any ancestor
   * chunk that becomes empty as a result
   */
  remove() {
    this.pointerSiblings.splice(this.pointerIndex--, 1), this.cachedPointerNode = void 0, this.pointerSiblings.length === 0 && this.pointerChunk.type === "chunk" ? (this.exitChunk(), this.remove()) : this.invalidateChunk(), this.validateState();
  }
  /**
   * Add the current chunk and all ancestor chunks to the list of modified
   * chunks
   */
  invalidateChunk() {
    for (let c2 = this.pointerChunk; c2.type === "chunk"; c2 = c2.parent)
      this.root.modifiedChunks.add(c2);
  }
  /**
   * Whether the pointer is at the start of the tree
   */
  get atStart() {
    return this.pointerChunk.type === "root" && this.pointerIndex === -1;
  }
  /**
   * The siblings of the current node
   */
  get pointerSiblings() {
    return this.pointerChunk.children;
  }
  /**
   * Get the current node (uncached)
   *
   * If the pointer is at the start or end of the document, returns null.
   *
   * Usually, the current node is a chunk leaf, although it can be a chunk
   * while insertions are in progress.
   */
  getPointerNode() {
    return this.reachedEnd || this.pointerIndex === -1 ? null : this.pointerSiblings[this.pointerIndex] ?? null;
  }
  /**
   * Cached getter for the current node
   */
  get pointerNode() {
    if (this.cachedPointerNode !== void 0)
      return this.cachedPointerNode;
    const pointerNode = this.getPointerNode();
    return this.cachedPointerNode = pointerNode, pointerNode;
  }
  /**
   * Get the path of a chunk relative to the root, returning null if the chunk
   * is not connected to the root
   */
  getChunkPath(chunk) {
    const path2 = [];
    for (let c2 = chunk; c2.type === "chunk"; c2 = c2.parent) {
      const index = c2.parent.children.indexOf(c2);
      if (index === -1)
        return null;
      path2.unshift(index);
    }
    return path2;
  }
  /**
   * Save the current pointer to be restored later
   */
  savePointer() {
    if (this.atStart)
      return "start";
    if (!this.pointerNode)
      throw new Error("Cannot save pointer when pointerNode is null");
    return {
      chunk: this.pointerChunk,
      node: this.pointerNode
    };
  }
  /**
   * Restore the pointer to a previous state
   */
  restorePointer(savedPointer) {
    if (savedPointer === "start") {
      this.pointerChunk = this.root, this.pointerIndex = -1, this.pointerIndexStack = [], this.reachedEnd = !1, this.cachedPointerNode = void 0;
      return;
    }
    const {
      chunk,
      node: node2
    } = savedPointer, index = chunk.children.indexOf(node2);
    if (index === -1)
      throw new Error("Cannot restore point because saved node is no longer in saved chunk");
    const indexStack = this.getChunkPath(chunk);
    if (!indexStack)
      throw new Error("Cannot restore point because saved chunk is no longer connected to root");
    this.pointerChunk = chunk, this.pointerIndex = index, this.pointerIndexStack = indexStack, this.reachedEnd = !1, this.cachedPointerNode = node2, this.validateState();
  }
  /**
   * Assuming the current node is a chunk, move the pointer into that chunk
   *
   * @param end If true, place the pointer on the last node of the chunk.
   * Otherwise, place the pointer on the first node.
   */
  enterChunk(end2) {
    if (this.pointerNode?.type !== "chunk")
      throw new Error("Cannot enter non-chunk");
    if (this.pointerIndexStack.push(this.pointerIndex), this.pointerChunk = this.pointerNode, this.pointerIndex = end2 ? this.pointerSiblings.length - 1 : 0, this.cachedPointerNode = void 0, this.validateState(), this.pointerChunk.children.length === 0)
      throw new Error("Cannot enter empty chunk");
  }
  /**
   * Assuming the current node is a chunk, move the pointer into that chunk
   * repeatedly until the current node is a leaf
   *
   * @param end If true, place the pointer on the last node of the chunk.
   * Otherwise, place the pointer on the first node.
   */
  enterChunkUntilLeaf(end2) {
    for (; this.pointerNode?.type === "chunk"; )
      this.enterChunk(end2);
  }
  /**
   * Move the pointer to the parent chunk
   */
  exitChunk() {
    if (this.pointerChunk.type === "root")
      throw new Error("Cannot exit root");
    const previousPointerChunk = this.pointerChunk;
    this.pointerChunk = previousPointerChunk.parent, this.pointerIndex = this.pointerIndexStack.pop(), this.cachedPointerNode = void 0, this.validateState();
  }
  /**
   * Insert leaves immediately after the current node, leaving the pointer on
   * the last inserted leaf
   *
   * Leaves are chunked according to the number of nodes already in the parent
   * plus the number of nodes being inserted, or the minimum depth if larger
   */
  rawInsertAfter(leaves, minDepth) {
    if (leaves.length === 0)
      return;
    const groupIntoChunks = (leaves2, parent2, perChunk) => {
      if (perChunk === 1)
        return leaves2;
      const chunks2 = [];
      for (let i = 0; i < this.chunkSize; i++) {
        const chunkNodes = leaves2.slice(i * perChunk, (i + 1) * perChunk);
        if (chunkNodes.length === 0)
          break;
        const chunk = {
          type: "chunk",
          key: new Key(),
          parent: parent2,
          children: []
        };
        chunk.children = groupIntoChunks(chunkNodes, chunk, perChunk / this.chunkSize), chunks2.push(chunk);
      }
      return chunks2;
    }, newTotal = this.pointerSiblings.length + leaves.length;
    let depthForTotal = 0;
    for (let i = this.chunkSize; i < newTotal; i *= this.chunkSize)
      depthForTotal++;
    const depth = Math.max(depthForTotal, minDepth), perTopLevelChunk = this.chunkSize ** depth, chunks = groupIntoChunks(leaves, this.pointerChunk, perTopLevelChunk);
    this.pointerSiblings.splice(this.pointerIndex + 1, 0, ...chunks), this.pointerIndex += chunks.length, this.cachedPointerNode = void 0, this.invalidateChunk(), this.validateState();
  }
  /**
   * If debug mode is enabled, ensure that the state is internally consistent
   */
  // istanbul ignore next
  validateState() {
    if (!this.debug)
      return;
    const validateDescendant = (node2) => {
      if (node2.type === "chunk") {
        const {
          parent: parent2,
          children
        } = node2;
        if (!parent2.children.includes(node2))
          throw new Error(`Debug: Chunk ${node2.key.id} has an incorrect parent property`);
        children.forEach(validateDescendant);
      }
    };
    if (this.root.children.forEach(validateDescendant), this.cachedPointerNode !== void 0 && this.cachedPointerNode !== this.getPointerNode())
      throw new Error("Debug: The cached pointer is incorrect and has not been invalidated");
    const actualIndexStack = this.getChunkPath(this.pointerChunk);
    if (!actualIndexStack)
      throw new Error("Debug: The pointer chunk is not connected to the root");
    if (!Path.equals(this.pointerIndexStack, actualIndexStack))
      throw new Error(`Debug: The cached index stack [${this.pointerIndexStack.join(", ")}] does not match the path of the pointer chunk [${actualIndexStack.join(", ")}]`);
  }
}
const reconcileChildren = (editor, {
  chunkTree,
  children,
  chunkSize,
  rerenderChildren = [],
  onInsert,
  onUpdate,
  onIndexChange,
  debug: debug2
}) => {
  chunkTree.modifiedChunks.clear();
  const chunkTreeHelper = new ChunkTreeHelper(chunkTree, {
    chunkSize,
    debug: debug2
  }), childrenHelper = new ChildrenHelper(editor, children);
  let treeLeaf;
  for (; treeLeaf = chunkTreeHelper.readLeaf(); ) {
    const lookAhead = childrenHelper.lookAhead(treeLeaf.node, treeLeaf.key), wasMoved = lookAhead > 0 && chunkTree.movedNodeKeys.has(treeLeaf.key);
    if (lookAhead === -1 || wasMoved) {
      chunkTreeHelper.remove();
      continue;
    }
    const insertedChildrenStartIndex = childrenHelper.pointerIndex, insertedChildren = childrenHelper.read(lookAhead + 1), matchingChild = insertedChildren.pop();
    if (insertedChildren.length) {
      const leavesToInsert = childrenHelper.toChunkLeaves(insertedChildren, insertedChildrenStartIndex);
      chunkTreeHelper.insertBefore(leavesToInsert), insertedChildren.forEach((node2, relativeIndex) => {
        onInsert?.(node2, insertedChildrenStartIndex + relativeIndex);
      });
    }
    const matchingChildIndex = childrenHelper.pointerIndex - 1;
    treeLeaf.node !== matchingChild && (treeLeaf.node = matchingChild, chunkTreeHelper.invalidateChunk(), onUpdate?.(matchingChild, matchingChildIndex)), treeLeaf.index !== matchingChildIndex && (treeLeaf.index = matchingChildIndex, onIndexChange?.(matchingChild, matchingChildIndex)), rerenderChildren.includes(matchingChildIndex) && chunkTreeHelper.invalidateChunk();
  }
  if (!childrenHelper.reachedEnd) {
    const remainingChildren = childrenHelper.remaining(), leavesToInsert = childrenHelper.toChunkLeaves(remainingChildren, childrenHelper.pointerIndex);
    chunkTreeHelper.returnToPreviousLeaf(), chunkTreeHelper.insertAfter(leavesToInsert), remainingChildren.forEach((node2, relativeIndex) => {
      onInsert?.(node2, childrenHelper.pointerIndex + relativeIndex);
    });
  }
  chunkTree.movedNodeKeys.clear();
}, KEY_TO_CHUNK_TREE = /* @__PURE__ */ new WeakMap(), getChunkTreeForNode = (editor, node2, options = {}) => {
  const key = ReactEditor.findKey(editor, node2);
  let chunkTree = KEY_TO_CHUNK_TREE.get(key);
  return chunkTree || (chunkTree = {
    type: "root",
    movedNodeKeys: /* @__PURE__ */ new Set(),
    modifiedChunks: /* @__PURE__ */ new Set(),
    children: []
  }, KEY_TO_CHUNK_TREE.set(key, chunkTree)), options.reconcile && reconcileChildren(editor, {
    chunkTree,
    children: node2.children,
    ...options.reconcile
  }), chunkTree;
}, defaultRenderChunk = ({
  children
}) => children, ChunkAncestor = (props) => {
  const {
    root,
    ancestor,
    renderElement,
    renderChunk = defaultRenderChunk
  } = props;
  return ancestor.children.map((chunkNode) => {
    if (chunkNode.type === "chunk") {
      const key = chunkNode.key.id, renderedChunk = renderChunk({
        highest: ancestor === root,
        lowest: chunkNode.children.some((c2) => c2.type === "leaf"),
        attributes: {
          "data-slate-chunk": !0
        },
        children: /* @__PURE__ */ jsx(MemoizedChunk, { root, ancestor: chunkNode, renderElement, renderChunk })
      });
      return /* @__PURE__ */ jsx(Fragment, { children: renderedChunk }, key);
    }
    const element = chunkNode.node;
    return renderElement(element, chunkNode.index, chunkNode.key);
  });
}, ChunkTree = ChunkAncestor, MemoizedChunk = React.memo(ChunkAncestor, (prev, next2) => prev.root === next2.root && prev.renderElement === next2.renderElement && prev.renderChunk === next2.renderChunk && !next2.root.modifiedChunks.has(next2.ancestor));
function useGenericSelector(selector, equalityFn) {
  const [, forceRender] = useReducer((s) => s + 1, 0), latestSubscriptionCallbackError = useRef(void 0), latestSelector = useRef(() => null), latestSelectedState = useRef(null);
  let selectedState;
  try {
    if (selector !== latestSelector.current || latestSubscriptionCallbackError.current) {
      const selectorResult = selector();
      equalityFn(latestSelectedState.current, selectorResult) ? selectedState = latestSelectedState.current : selectedState = selectorResult;
    } else
      selectedState = latestSelectedState.current;
  } catch (err) {
    throw latestSubscriptionCallbackError.current && isError(err) && (err.message += `
The error may be correlated with this previous error:
${latestSubscriptionCallbackError.current.stack}

`), err;
  }
  latestSelector.current = selector, latestSelectedState.current = selectedState, latestSubscriptionCallbackError.current = void 0;
  const update = useCallback(() => {
    try {
      const newSelectedState = latestSelector.current();
      if (equalityFn(latestSelectedState.current, newSelectedState))
        return;
      latestSelectedState.current = newSelectedState;
    } catch (err) {
      err instanceof Error ? latestSubscriptionCallbackError.current = err : latestSubscriptionCallbackError.current = new Error(String(err));
    }
    forceRender();
  }, []);
  return [selectedState, update];
}
function isError(error) {
  return error instanceof Error;
}
const DecorateContext = createContext({}), useDecorations = (node2, parentDecorations) => {
  const editor = useSlateStatic(), {
    decorate,
    addEventListener
  } = useContext(DecorateContext), selector = () => {
    const path2 = ReactEditor.findPath(editor, node2);
    return decorate([node2, path2]);
  }, equalityFn = Text$1.isText(node2) ? isTextDecorationsEqual : isElementDecorationsEqual, [decorations, update] = useGenericSelector(selector, equalityFn);
  return useIsomorphicLayoutEffect(() => {
    const unsubscribe = addEventListener(update);
    return update(), unsubscribe;
  }, [addEventListener, update]), useMemo(() => [...decorations, ...parentDecorations], [decorations, parentDecorations]);
}, useDecorateContext = (decorateProp) => {
  const eventListeners = useRef(/* @__PURE__ */ new Set()), latestDecorate = useRef(decorateProp);
  useIsomorphicLayoutEffect(() => {
    latestDecorate.current = decorateProp, eventListeners.current.forEach((listener) => {
      listener();
    });
  }, [decorateProp]);
  const decorate = useCallback((entry) => latestDecorate.current(entry), []), addEventListener = useCallback((callback) => (eventListeners.current.add(callback), () => {
    eventListeners.current.delete(callback);
  }), []);
  return useMemo(() => ({
    decorate,
    addEventListener
  }), [decorate, addEventListener]);
}, rtlRange = "\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC", ltrRange = "A-Za-z\xC0-\xD6\xD8-\xF6\xF8-\u02B8\u0300-\u0590\u0800-\u1FFF\u200E\u2C00-\uFB1C\uFE00-\uFE6F\uFEFD-\uFFFF", rtl = new RegExp(`^[^${ltrRange}]*[${rtlRange}]`), ltr = new RegExp(`^[^${rtlRange}]*[${ltrRange}]`);
function getDirection(value) {
  const source = String(value || "");
  return rtl.test(source) ? "rtl" : ltr.test(source) ? "ltr" : "neutral";
}
const SlateString = (props) => {
  const {
    isLast,
    leaf: leaf2,
    parent: parent2,
    text
  } = props, editor = useSlateStatic(), path2 = ReactEditor.findPath(editor, text), parentPath = Path.parent(path2), isMarkPlaceholder = !!leaf2[MARK_PLACEHOLDER_SYMBOL];
  return editor.isVoid(parent2) ? /* @__PURE__ */ jsx(ZeroWidthString, { length: Node$1.string(parent2).length }) : leaf2.text === "" && parent2.children[parent2.children.length - 1] === text && !editor.isInline(parent2) && Editor.string(editor, parentPath) === "" ? /* @__PURE__ */ jsx(ZeroWidthString, { isLineBreak: !0, isMarkPlaceholder }) : leaf2.text === "" ? /* @__PURE__ */ jsx(ZeroWidthString, { isMarkPlaceholder }) : isLast && leaf2.text.slice(-1) === `
` ? /* @__PURE__ */ jsx(TextString, { isTrailing: !0, text: leaf2.text }) : /* @__PURE__ */ jsx(TextString, { text: leaf2.text });
}, TextString = (props) => {
  const {
    text,
    isTrailing = !1
  } = props, ref = useRef(null), getTextContent = () => `${text ?? ""}${isTrailing ? `
` : ""}`, [initialText] = useState(getTextContent);
  return useIsomorphicLayoutEffect(() => {
    const textWithTrailing = getTextContent();
    ref.current && ref.current.textContent !== textWithTrailing && (ref.current.textContent = textWithTrailing);
  }), /* @__PURE__ */ jsx(MemoizedText$1, { ref, children: initialText });
}, MemoizedText$1 = memo(forwardRef((props, ref) => /* @__PURE__ */ jsx("span", { "data-slate-string": !0, ref, children: props.children }))), ZeroWidthString = (props) => {
  const {
    length = 0,
    isLineBreak = !1,
    isMarkPlaceholder = !1
  } = props, attributes = {
    "data-slate-zero-width": isLineBreak ? "n" : "z",
    "data-slate-length": length
  };
  return isMarkPlaceholder && (attributes["data-slate-mark-placeholder"] = !0), /* @__PURE__ */ jsxs("span", { ...attributes, children: [
    !IS_ANDROID || !isLineBreak ? "\uFEFF" : null,
    isLineBreak ? /* @__PURE__ */ jsx("br", {}) : null
  ] });
}, PLACEHOLDER_DELAY = IS_ANDROID ? 300 : 0;
function disconnectPlaceholderResizeObserver(placeholderResizeObserver, releaseObserver) {
  placeholderResizeObserver.current && (placeholderResizeObserver.current.disconnect(), releaseObserver && (placeholderResizeObserver.current = null));
}
function clearTimeoutRef(timeoutRef) {
  timeoutRef.current && (clearTimeout(timeoutRef.current), timeoutRef.current = null);
}
const defaultRenderLeaf = (props) => /* @__PURE__ */ jsx(DefaultLeaf, { ...props }), Leaf = (props) => {
  const {
    leaf: leaf2,
    isLast,
    text,
    parent: parent2,
    renderPlaceholder,
    renderLeaf = defaultRenderLeaf,
    leafPosition
  } = props, editor = useSlateStatic(), placeholderResizeObserver = useRef(null), placeholderRef = useRef(null), [showPlaceholder, setShowPlaceholder] = useState(!1), showPlaceholderTimeoutRef = useRef(null), callbackPlaceholderRef = useCallback((placeholderEl) => {
    if (disconnectPlaceholderResizeObserver(placeholderResizeObserver, placeholderEl == null), placeholderEl == null)
      EDITOR_TO_PLACEHOLDER_ELEMENT.delete(editor), leaf2.onPlaceholderResize?.(null);
    else {
      if (EDITOR_TO_PLACEHOLDER_ELEMENT.set(editor, placeholderEl), !placeholderResizeObserver.current) {
        const ResizeObserver$1 = window.ResizeObserver || ResizeObserver;
        placeholderResizeObserver.current = new ResizeObserver$1(() => {
          leaf2.onPlaceholderResize?.(placeholderEl);
        });
      }
      placeholderResizeObserver.current.observe(placeholderEl), placeholderRef.current = placeholderEl;
    }
  }, [placeholderRef, leaf2, editor]);
  let children = /* @__PURE__ */ jsx(SlateString, { isLast, leaf: leaf2, parent: parent2, text });
  const leafIsPlaceholder = !!leaf2[PLACEHOLDER_SYMBOL];
  if (useEffect(() => (leafIsPlaceholder ? showPlaceholderTimeoutRef.current || (showPlaceholderTimeoutRef.current = setTimeout(() => {
    setShowPlaceholder(!0), showPlaceholderTimeoutRef.current = null;
  }, PLACEHOLDER_DELAY)) : (clearTimeoutRef(showPlaceholderTimeoutRef), setShowPlaceholder(!1)), () => clearTimeoutRef(showPlaceholderTimeoutRef)), [leafIsPlaceholder, setShowPlaceholder]), leafIsPlaceholder && showPlaceholder) {
    const placeholderProps = {
      children: leaf2.placeholder,
      attributes: {
        "data-slate-placeholder": !0,
        style: {
          position: "absolute",
          top: 0,
          pointerEvents: "none",
          width: "100%",
          maxWidth: "100%",
          display: "block",
          opacity: "0.333",
          userSelect: "none",
          textDecoration: "none",
          // Fixes https://github.com/udecode/plate/issues/2315
          WebkitUserModify: IS_WEBKIT ? "inherit" : void 0
        },
        contentEditable: !1,
        ref: callbackPlaceholderRef
      }
    };
    children = /* @__PURE__ */ jsxs(React.Fragment, { children: [
      children,
      renderPlaceholder(placeholderProps)
    ] });
  }
  return renderLeaf({
    attributes: {
      "data-slate-leaf": !0
    },
    children,
    leaf: leaf2,
    text,
    leafPosition
  });
}, MemoizedLeaf = React.memo(Leaf, (prev, next2) => next2.parent === prev.parent && next2.isLast === prev.isLast && next2.renderLeaf === prev.renderLeaf && next2.renderPlaceholder === prev.renderPlaceholder && next2.text === prev.text && Text$1.equals(next2.leaf, prev.leaf) && next2.leaf[PLACEHOLDER_SYMBOL] === prev.leaf[PLACEHOLDER_SYMBOL]), DefaultLeaf = (props) => {
  const {
    attributes,
    children
  } = props;
  return /* @__PURE__ */ jsx("span", { ...attributes, children });
}, defaultRenderText = (props) => /* @__PURE__ */ jsx(DefaultText, { ...props }), Text = (props) => {
  const {
    decorations: parentDecorations,
    isLast,
    parent: parent2,
    renderPlaceholder,
    renderLeaf,
    renderText = defaultRenderText,
    text
  } = props, editor = useSlateStatic(), ref = useRef(null), decorations = useDecorations(text, parentDecorations), decoratedLeaves = Text$1.decorations(text, decorations), key = ReactEditor.findKey(editor, text), children = [];
  for (let i = 0; i < decoratedLeaves.length; i++) {
    const {
      leaf: leaf2,
      position
    } = decoratedLeaves[i];
    children.push(/* @__PURE__ */ jsx(MemoizedLeaf, { isLast: isLast && i === decoratedLeaves.length - 1, renderPlaceholder, leaf: leaf2, leafPosition: position, text, parent: parent2, renderLeaf }, `${key.id}-${i}`));
  }
  const attributes = {
    "data-slate-node": "text",
    ref: useCallback((span) => {
      const KEY_TO_ELEMENT = EDITOR_TO_KEY_TO_ELEMENT.get(editor);
      span ? (KEY_TO_ELEMENT?.set(key, span), NODE_TO_ELEMENT.set(text, span), ELEMENT_TO_NODE.set(span, text)) : (KEY_TO_ELEMENT?.delete(key), NODE_TO_ELEMENT.delete(text), ref.current && ELEMENT_TO_NODE.delete(ref.current)), ref.current = span;
    }, [ref, editor, key, text])
  };
  return renderText({
    text,
    children,
    attributes
  });
}, MemoizedText = React.memo(Text, (prev, next2) => next2.parent === prev.parent && next2.isLast === prev.isLast && next2.renderText === prev.renderText && next2.renderLeaf === prev.renderLeaf && next2.renderPlaceholder === prev.renderPlaceholder && next2.text === prev.text && isTextDecorationsEqual(next2.decorations, prev.decorations)), DefaultText = (props) => {
  const {
    attributes,
    children
  } = props;
  return /* @__PURE__ */ jsx("span", { ...attributes, children });
}, defaultRenderElement = (props) => /* @__PURE__ */ jsx(DefaultElement, { ...props }), Element$1 = (props) => {
  const {
    decorations: parentDecorations,
    element,
    renderElement = defaultRenderElement,
    renderChunk,
    renderPlaceholder,
    renderLeaf,
    renderText
  } = props, editor = useSlateStatic(), readOnly = useReadOnly(), isInline = editor.isInline(element), decorations = useDecorations(element, parentDecorations), key = ReactEditor.findKey(editor, element), ref = useCallback((ref2) => {
    const KEY_TO_ELEMENT = EDITOR_TO_KEY_TO_ELEMENT.get(editor);
    ref2 ? (KEY_TO_ELEMENT?.set(key, ref2), NODE_TO_ELEMENT.set(element, ref2), ELEMENT_TO_NODE.set(ref2, element)) : (KEY_TO_ELEMENT?.delete(key), NODE_TO_ELEMENT.delete(element));
  }, [editor, key, element]);
  let children = useChildren({
    decorations,
    node: element,
    renderElement,
    renderChunk,
    renderPlaceholder,
    renderLeaf,
    renderText
  });
  const attributes = {
    "data-slate-node": "element",
    ref
  };
  if (isInline && (attributes["data-slate-inline"] = !0), !isInline && Editor.hasInlines(editor, element)) {
    const text = Node$1.string(element), dir = getDirection(text);
    dir === "rtl" && (attributes.dir = dir);
  }
  if (Editor.isVoid(editor, element)) {
    attributes["data-slate-void"] = !0, !readOnly && isInline && (attributes.contentEditable = !1);
    const Tag = isInline ? "span" : "div", [textEntry] = Node$1.texts(element), [text] = textEntry;
    children = /* @__PURE__ */ jsx(Tag, { "data-slate-spacer": !0, style: {
      height: "0",
      color: "transparent",
      outline: "none",
      position: "absolute"
    }, children: /* @__PURE__ */ jsx(MemoizedText, { renderPlaceholder, decorations: [], isLast: !1, parent: element, text }) }), NODE_TO_INDEX.set(text, 0), NODE_TO_PARENT.set(text, element);
  }
  return renderElement({
    attributes,
    children,
    element
  });
}, MemoizedElement = React.memo(Element$1, (prev, next2) => prev.element === next2.element && prev.renderElement === next2.renderElement && prev.renderChunk === next2.renderChunk && prev.renderText === next2.renderText && prev.renderLeaf === next2.renderLeaf && prev.renderPlaceholder === next2.renderPlaceholder && isElementDecorationsEqual(prev.decorations, next2.decorations)), DefaultElement = (props) => {
  const {
    attributes,
    children,
    element
  } = props, Tag = useSlateStatic().isInline(element) ? "span" : "div";
  return /* @__PURE__ */ jsx(Tag, { ...attributes, style: {
    position: "relative"
  }, children });
}, ElementContext = createContext(null), useChildren = (props) => {
  const {
    decorations,
    node: node2,
    renderElement,
    renderChunk,
    renderPlaceholder,
    renderText,
    renderLeaf
  } = props, editor = useSlateStatic();
  IS_NODE_MAP_DIRTY.set(editor, !1);
  const chunkSize = !Editor.isEditor(node2) && Element$2.isElement(node2) && !editor.isInline(node2) && Editor.hasInlines(editor, node2) ? null : editor.getChunkSize(node2), chunking = !!chunkSize, {
    decorationsByChild,
    childrenToRedecorate
  } = useDecorationsByChild(editor, node2, decorations);
  chunking || node2.children.forEach((n2, i) => {
    NODE_TO_INDEX.set(n2, i), NODE_TO_PARENT.set(n2, node2);
  });
  const renderElementComponent = useCallback((n2, i, cachedKey) => {
    const key = cachedKey ?? ReactEditor.findKey(editor, n2);
    return /* @__PURE__ */ jsx(ElementContext.Provider, { value: n2, children: /* @__PURE__ */ jsx(MemoizedElement, { decorations: decorationsByChild[i] ?? [], element: n2, renderElement, renderChunk, renderPlaceholder, renderLeaf, renderText }, key.id) }, `provider-${key.id}`);
  }, [editor, decorationsByChild, renderElement, renderChunk, renderPlaceholder, renderLeaf, renderText]), renderTextComponent = (n2, i) => {
    const key = ReactEditor.findKey(editor, n2);
    return /* @__PURE__ */ jsx(MemoizedText, { decorations: decorationsByChild[i] ?? [], isLast: i === node2.children.length - 1, parent: node2, renderPlaceholder, renderLeaf, renderText, text: n2 }, key.id);
  };
  if (!chunking)
    return node2.children.map((n2, i) => Text$1.isText(n2) ? renderTextComponent(n2, i) : renderElementComponent(n2, i));
  const chunkTree = getChunkTreeForNode(editor, node2, {
    reconcile: {
      chunkSize,
      rerenderChildren: childrenToRedecorate,
      onInsert: (n2, i) => {
        NODE_TO_INDEX.set(n2, i), NODE_TO_PARENT.set(n2, node2);
      },
      onUpdate: (n2, i) => {
        NODE_TO_INDEX.set(n2, i), NODE_TO_PARENT.set(n2, node2);
      },
      onIndexChange: (n2, i) => {
        NODE_TO_INDEX.set(n2, i);
      }
    }
  });
  return /* @__PURE__ */ jsx(ChunkTree, { root: chunkTree, ancestor: chunkTree, renderElement: renderElementComponent, renderChunk });
}, useDecorationsByChild = (editor, node2, decorations) => {
  const decorationsByChild = splitDecorationsByChild(editor, node2, decorations), mutableDecorationsByChild = useRef(decorationsByChild).current, childrenToRedecorate = [];
  mutableDecorationsByChild.length = decorationsByChild.length;
  for (let i = 0; i < decorationsByChild.length; i++) {
    const decorations2 = decorationsByChild[i], previousDecorations = mutableDecorationsByChild[i] ?? null;
    isElementDecorationsEqual(previousDecorations, decorations2) || (mutableDecorationsByChild[i] = decorations2, childrenToRedecorate.push(i));
  }
  return {
    decorationsByChild: mutableDecorationsByChild,
    childrenToRedecorate
  };
}, ComposingContext = createContext(!1), ReadOnlyContext = createContext(!1), useReadOnly = () => useContext(ReadOnlyContext), SlateSelectorContext = createContext({}), refEquality = (a, b) => a === b;
function useSlateSelector(selector, equalityFn = refEquality, {
  deferred
} = {}) {
  const context = useContext(SlateSelectorContext);
  if (!context)
    throw new Error("The `useSlateSelector` hook must be used inside the <Slate> component's context.");
  const {
    addEventListener
  } = context, editor = useSlateStatic(), genericSelector = useCallback(() => selector(editor), [editor, selector]), [selectedState, update] = useGenericSelector(genericSelector, equalityFn);
  return useIsomorphicLayoutEffect(() => {
    const unsubscribe = addEventListener(update, {
      deferred
    });
    return update(), unsubscribe;
  }, [addEventListener, update, deferred]), selectedState;
}
function useSelectorContext() {
  const eventListeners = useRef(/* @__PURE__ */ new Set()), deferredEventListeners = useRef(/* @__PURE__ */ new Set()), onChange = useCallback(() => {
    eventListeners.current.forEach((listener) => {
      listener();
    });
  }, []), flushDeferred = useCallback(() => {
    deferredEventListeners.current.forEach((listener) => {
      listener();
    }), deferredEventListeners.current.clear();
  }, []), addEventListener = useCallback((callbackProp, {
    deferred = !1
  } = {}) => {
    const callback = deferred ? () => deferredEventListeners.current.add(callbackProp) : callbackProp;
    return eventListeners.current.add(callback), () => {
      eventListeners.current.delete(callback);
    };
  }, []);
  return {
    selectorContext: useMemo(() => ({
      addEventListener,
      flushDeferred
    }), [addEventListener, flushDeferred]),
    onChange
  };
}
function useFlushDeferredSelectorsOnRender() {
  const {
    flushDeferred
  } = useContext(SlateSelectorContext);
  useIsomorphicLayoutEffect(flushDeferred);
}
const useSlate = () => {
  const {
    addEventListener
  } = useContext(SlateSelectorContext), [, forceRender] = useReducer((s) => s + 1, 0);
  if (!addEventListener)
    throw new Error("The `useSlate` hook must be used inside the <Slate> component's context.");
  return useIsomorphicLayoutEffect(() => addEventListener(forceRender), [addEventListener]), useSlateStatic();
};
function useTrackUserInput() {
  const editor = useSlateStatic(), receivedUserInput = useRef(!1), animationFrameIdRef = useRef(0), onUserInput = useCallback(() => {
    if (receivedUserInput.current)
      return;
    receivedUserInput.current = !0;
    const window2 = ReactEditor.getWindow(editor);
    window2.cancelAnimationFrame(animationFrameIdRef.current), animationFrameIdRef.current = window2.requestAnimationFrame(() => {
      receivedUserInput.current = !1;
    });
  }, [editor]);
  return useEffect(() => () => cancelAnimationFrame(animationFrameIdRef.current), []), {
    receivedUserInput,
    onUserInput
  };
}
function debounce(func, wait) {
  let timeoutId, lastArgs;
  const debounced = (...args) => {
    lastArgs = args, timeoutId !== void 0 && clearTimeout(timeoutId), timeoutId = setTimeout(() => {
      timeoutId = void 0;
      const args2 = lastArgs;
      lastArgs = void 0, args2 && func(...args2);
    }, wait);
  };
  return debounced.cancel = () => {
    timeoutId !== void 0 && (clearTimeout(timeoutId), timeoutId = void 0), lastArgs = void 0;
  }, debounced.flush = () => {
    if (timeoutId !== void 0) {
      clearTimeout(timeoutId), timeoutId = void 0;
      const args = lastArgs;
      lastArgs = void 0, args && func(...args);
    }
  }, debounced;
}
function throttle(func, wait) {
  let timeoutId, lastArgs, lastCallTime;
  const invoke = () => {
    const args = lastArgs;
    lastArgs = void 0, lastCallTime = Date.now(), args && func(...args);
  }, startTimer = (remaining) => {
    timeoutId = setTimeout(() => {
      timeoutId = void 0, lastArgs && invoke();
    }, remaining);
  }, throttled = (...args) => {
    const now = Date.now();
    if (lastArgs = args, lastCallTime === void 0) {
      invoke();
      return;
    }
    const elapsed = now - lastCallTime;
    elapsed >= wait ? (timeoutId !== void 0 && (clearTimeout(timeoutId), timeoutId = void 0), invoke()) : timeoutId === void 0 && startTimer(wait - elapsed);
  };
  return throttled.cancel = () => {
    timeoutId !== void 0 && (clearTimeout(timeoutId), timeoutId = void 0), lastArgs = void 0, lastCallTime = void 0;
  }, throttled.flush = () => {
    timeoutId !== void 0 && (clearTimeout(timeoutId), timeoutId = void 0), lastArgs && invoke();
  }, throttled;
}
const createRestoreDomManager = (editor, receivedUserInput) => {
  let bufferedMutations = [];
  const clear = () => {
    bufferedMutations = [];
  }, registerMutations = (mutations) => {
    if (!receivedUserInput.current)
      return;
    const trackedMutations = mutations.filter((mutation) => isTrackedMutation(editor, mutation, mutations));
    bufferedMutations.push(...trackedMutations);
  };
  function restoreDOM() {
    bufferedMutations.length > 0 && (bufferedMutations.reverse().forEach((mutation) => {
      mutation.type !== "characterData" && (mutation.removedNodes.forEach((node2) => {
        mutation.target.insertBefore(node2, mutation.nextSibling);
      }), mutation.addedNodes.forEach((node2) => {
        mutation.target.removeChild(node2);
      }));
    }), clear());
  }
  return {
    registerMutations,
    restoreDOM,
    clear
  };
}, MUTATION_OBSERVER_CONFIG = {
  subtree: !0,
  childList: !0,
  characterData: !0,
  characterDataOldValue: !0
};
class RestoreDOMComponent extends Component {
  static contextType = EditorContext;
  context = null;
  manager = null;
  mutationObserver = null;
  observe() {
    const {
      node: node2
    } = this.props;
    if (!node2.current)
      throw new Error("Failed to attach MutationObserver, `node` is undefined");
    this.mutationObserver?.observe(node2.current, MUTATION_OBSERVER_CONFIG);
  }
  componentDidMount() {
    const {
      receivedUserInput
    } = this.props, editor = this.context;
    this.manager = createRestoreDomManager(editor, receivedUserInput), this.mutationObserver = new MutationObserver(this.manager.registerMutations), this.observe();
  }
  getSnapshotBeforeUpdate() {
    const pendingMutations = this.mutationObserver?.takeRecords();
    return pendingMutations?.length && this.manager?.registerMutations(pendingMutations), this.mutationObserver?.disconnect(), this.manager?.restoreDOM(), null;
  }
  componentDidUpdate() {
    this.manager?.clear(), this.observe();
  }
  componentWillUnmount() {
    this.mutationObserver?.disconnect();
  }
  render() {
    return this.props.children;
  }
}
const RestoreDOM = IS_ANDROID ? RestoreDOMComponent : ({
  children
}) => /* @__PURE__ */ jsx(Fragment$1, { children }), Children = (props) => /* @__PURE__ */ jsx(React.Fragment, { children: useChildren(props) }), Editable = forwardRef((props, forwardedRef) => {
  const defaultRenderPlaceholder = useCallback((props2) => /* @__PURE__ */ jsx(DefaultPlaceholder, { ...props2 }), []), {
    autoFocus,
    decorate = defaultDecorate,
    onDOMBeforeInput: propsOnDOMBeforeInput,
    placeholder,
    readOnly = !1,
    renderElement,
    renderChunk,
    renderLeaf,
    renderText,
    renderPlaceholder = defaultRenderPlaceholder,
    scrollSelectionIntoView = defaultScrollSelectionIntoView,
    style: userStyle = {},
    as: Component2 = "div",
    disableDefaultStyles = !1,
    ...attributes
  } = props, editor = useSlate(), [isComposing, setIsComposing] = useState(!1), ref = useRef(null), deferredOperations = useRef([]), [placeholderHeight, setPlaceholderHeight] = useState(), processing = useRef(!1), {
    onUserInput,
    receivedUserInput
  } = useTrackUserInput(), [, forceRender] = useReducer((s) => s + 1, 0);
  EDITOR_TO_FORCE_RENDER.set(editor, forceRender), IS_READ_ONLY.set(editor, readOnly);
  const state = useMemo(() => ({
    isDraggingInternally: !1,
    isUpdatingSelection: !1,
    latestElement: null,
    hasMarkPlaceholder: !1
  }), []);
  useEffect(() => {
    ref.current && autoFocus && ref.current.focus();
  }, [autoFocus]);
  const androidInputManagerRef = useRef(void 0), onDOMSelectionChange = useMemo(() => throttle(() => {
    if (IS_NODE_MAP_DIRTY.get(editor)) {
      onDOMSelectionChange();
      return;
    }
    const root = ReactEditor.toDOMNode(editor, editor).getRootNode();
    if (!processing.current && IS_WEBKIT && root instanceof ShadowRoot) {
      processing.current = !0, getActiveElement() ? document.execCommand("indent") : Transforms.deselect(editor), processing.current = !1;
      return;
    }
    const androidInputManager = androidInputManagerRef.current;
    if ((IS_ANDROID || !ReactEditor.isComposing(editor)) && (!state.isUpdatingSelection || androidInputManager?.isFlushing()) && !state.isDraggingInternally) {
      const root2 = ReactEditor.findDocumentOrShadowRoot(editor), {
        activeElement
      } = root2, el2 = ReactEditor.toDOMNode(editor, editor), domSelection = getSelection(root2);
      if (activeElement === el2 ? (state.latestElement = activeElement, IS_FOCUSED.set(editor, !0)) : IS_FOCUSED.delete(editor), !domSelection)
        return Transforms.deselect(editor);
      const {
        anchorNode,
        focusNode
      } = domSelection, anchorNodeSelectable = ReactEditor.hasEditableTarget(editor, anchorNode) || ReactEditor.isTargetInsideNonReadonlyVoid(editor, anchorNode), focusNodeInEditor = ReactEditor.hasTarget(editor, focusNode);
      if (anchorNodeSelectable && focusNodeInEditor) {
        const range2 = ReactEditor.toSlateRange(editor, domSelection, {
          exactMatch: !1,
          suppressThrow: !0
        });
        range2 && (!ReactEditor.isComposing(editor) && !androidInputManager?.hasPendingChanges() && !androidInputManager?.isFlushing() ? Transforms.select(editor, range2) : androidInputManager?.handleUserSelect(range2));
      }
      readOnly && (!anchorNodeSelectable || !focusNodeInEditor) && Transforms.deselect(editor);
    }
  }, 100), [editor, readOnly, state]), scheduleOnDOMSelectionChange = useMemo(() => debounce(onDOMSelectionChange, 0), [onDOMSelectionChange]);
  androidInputManagerRef.current = useAndroidInputManager({
    node: ref,
    onDOMSelectionChange,
    scheduleOnDOMSelectionChange
  }), useIsomorphicLayoutEffect(() => {
    let window2 = null;
    ref.current && (window2 = getDefaultView(ref.current)) ? (EDITOR_TO_WINDOW.set(editor, window2), EDITOR_TO_ELEMENT.set(editor, ref.current), NODE_TO_ELEMENT.set(editor, ref.current), ELEMENT_TO_NODE.set(ref.current, editor)) : NODE_TO_ELEMENT.delete(editor);
    const {
      selection
    } = editor, root = ReactEditor.findDocumentOrShadowRoot(editor), domSelection = getSelection(root);
    if (!domSelection || !ReactEditor.isFocused(editor) || androidInputManagerRef.current?.hasPendingAction())
      return;
    const setDomSelection = (forceChange) => {
      const hasDomSelection = domSelection.type !== "None";
      if (!selection && !hasDomSelection)
        return;
      const focusNode = domSelection.focusNode;
      let anchorNode = null;
      if (IS_FIREFOX && domSelection.rangeCount > 1) {
        const firstRange = domSelection.getRangeAt(0), lastRange = domSelection.getRangeAt(domSelection.rangeCount - 1);
        firstRange.startContainer === focusNode ? anchorNode = lastRange.endContainer : anchorNode = firstRange.startContainer;
      } else
        anchorNode = domSelection.anchorNode;
      const editorElement = EDITOR_TO_ELEMENT.get(editor);
      let hasDomSelectionInEditor = !1;
      if (containsShadowAware(editorElement, anchorNode) && containsShadowAware(editorElement, focusNode) && (hasDomSelectionInEditor = !0), hasDomSelection && hasDomSelectionInEditor && selection && !forceChange) {
        const slateRange = ReactEditor.toSlateRange(editor, domSelection, {
          exactMatch: !0,
          // domSelection is not necessarily a valid Slate range
          // (e.g. when clicking on contentEditable:false element)
          suppressThrow: !0
        });
        if (slateRange && Range.equals(slateRange, selection) && (!state.hasMarkPlaceholder || anchorNode?.parentElement?.hasAttribute("data-slate-mark-placeholder")))
          return;
      }
      if (selection && !ReactEditor.hasRange(editor, selection)) {
        editor.selection = ReactEditor.toSlateRange(editor, domSelection, {
          exactMatch: !1,
          suppressThrow: !0
        });
        return;
      }
      state.isUpdatingSelection = !0;
      let newDomRange = null;
      try {
        newDomRange = selection && ReactEditor.toDOMRange(editor, selection);
      } catch {
      }
      return newDomRange ? (ReactEditor.isComposing(editor) && !IS_ANDROID ? domSelection.collapseToEnd() : Range.isBackward(selection) ? domSelection.setBaseAndExtent(newDomRange.endContainer, newDomRange.endOffset, newDomRange.startContainer, newDomRange.startOffset) : domSelection.setBaseAndExtent(newDomRange.startContainer, newDomRange.startOffset, newDomRange.endContainer, newDomRange.endOffset), scrollSelectionIntoView(editor, newDomRange)) : domSelection.removeAllRanges(), newDomRange;
    };
    domSelection.rangeCount <= 1 && setDomSelection();
    const ensureSelection = androidInputManagerRef.current?.isFlushing() === "action";
    if (!IS_ANDROID || !ensureSelection) {
      setTimeout(() => {
        state.isUpdatingSelection = !1;
      });
      return;
    }
    let timeoutId = null;
    const animationFrameId = requestAnimationFrame(() => {
      if (ensureSelection) {
        const ensureDomSelection = (forceChange) => {
          try {
            ReactEditor.toDOMNode(editor, editor).focus(), setDomSelection(forceChange);
          } catch {
          }
        };
        ensureDomSelection(), timeoutId = setTimeout(() => {
          ensureDomSelection(!0), state.isUpdatingSelection = !1;
        });
      }
    });
    return () => {
      cancelAnimationFrame(animationFrameId), timeoutId && clearTimeout(timeoutId);
    };
  });
  const onDOMBeforeInput = useCallback((event) => {
    handleNativeHistoryEvents(editor, event);
    const root = ReactEditor.toDOMNode(editor, editor).getRootNode();
    if (processing?.current && IS_WEBKIT && root instanceof ShadowRoot) {
      const range2 = event.getTargetRanges()[0], newRange = new window.Range();
      newRange.setStart(range2.startContainer, range2.startOffset), newRange.setEnd(range2.endContainer, range2.endOffset);
      const slateRange = ReactEditor.toSlateRange(editor, newRange, {
        exactMatch: !1,
        suppressThrow: !1
      });
      Transforms.select(editor, slateRange), event.preventDefault(), event.stopImmediatePropagation();
      return;
    }
    if (onUserInput(), !readOnly && ReactEditor.hasEditableTarget(editor, event.target) && !isDOMEventHandled(event, propsOnDOMBeforeInput)) {
      if (androidInputManagerRef.current)
        return androidInputManagerRef.current.handleDOMBeforeInput(event);
      scheduleOnDOMSelectionChange.flush(), onDOMSelectionChange.flush();
      const {
        selection
      } = editor, {
        inputType: type
      } = event, data = event.dataTransfer || event.data || void 0, isCompositionChange = type === "insertCompositionText" || type === "deleteCompositionText";
      if (isCompositionChange && ReactEditor.isComposing(editor))
        return;
      let native = !1;
      if (type === "insertText" && selection && Range.isCollapsed(selection) && // Only use native character insertion for single characters a-z or space for now.
      // Long-press events (hold a + press 4 = ä) to choose a special character otherwise
      // causes duplicate inserts.
      event.data && event.data.length === 1 && /[a-z ]/i.test(event.data) && // Chrome has issues correctly editing the start of nodes: https://bugs.chromium.org/p/chromium/issues/detail?id=1249405
      // When there is an inline element, e.g. a link, and you select
      // right after it (the start of the next node).
      selection.anchor.offset !== 0 && (native = !0, editor.marks && (native = !1), !IS_NODE_MAP_DIRTY.get(editor))) {
        const {
          anchor
        } = selection, [node2, offset] = ReactEditor.toDOMPoint(editor, anchor), anchorNode = node2.parentElement?.closest("a"), window2 = ReactEditor.getWindow(editor);
        if (native && anchorNode && ReactEditor.hasDOMNode(editor, anchorNode)) {
          const lastText = window2?.document.createTreeWalker(anchorNode, NodeFilter.SHOW_TEXT).lastChild();
          lastText === node2 && lastText.textContent?.length === offset && (native = !1);
        }
        if (native && node2.parentElement && window2?.getComputedStyle(node2.parentElement)?.whiteSpace === "pre") {
          const block = Editor.above(editor, {
            at: anchor.path,
            match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2)
          });
          block && Node$1.string(block[0]).includes("	") && (native = !1);
        }
      }
      if ((!type.startsWith("delete") || type.startsWith("deleteBy")) && !IS_NODE_MAP_DIRTY.get(editor)) {
        const [targetRange2] = event.getTargetRanges();
        if (targetRange2) {
          const range2 = ReactEditor.toSlateRange(editor, targetRange2, {
            exactMatch: !1,
            suppressThrow: !1
          });
          if (!selection || !Range.equals(selection, range2)) {
            native = !1;
            const selectionRef = !isCompositionChange && editor.selection && Editor.rangeRef(editor, editor.selection);
            Transforms.select(editor, range2), selectionRef && EDITOR_TO_USER_SELECTION.set(editor, selectionRef);
          }
        }
      }
      if (isCompositionChange)
        return;
      if (native || event.preventDefault(), selection && Range.isExpanded(selection) && type.startsWith("delete")) {
        const direction = type.endsWith("Backward") ? "backward" : "forward";
        Editor.deleteFragment(editor, {
          direction
        });
        return;
      }
      switch (type) {
        case "deleteByComposition":
        case "deleteByCut":
        case "deleteByDrag": {
          Editor.deleteFragment(editor);
          break;
        }
        case "deleteContent":
        case "deleteContentForward": {
          Editor.deleteForward(editor);
          break;
        }
        case "deleteContentBackward": {
          Editor.deleteBackward(editor);
          break;
        }
        case "deleteEntireSoftLine": {
          Editor.deleteBackward(editor, {
            unit: "line"
          }), Editor.deleteForward(editor, {
            unit: "line"
          });
          break;
        }
        case "deleteHardLineBackward": {
          Editor.deleteBackward(editor, {
            unit: "block"
          });
          break;
        }
        case "deleteSoftLineBackward": {
          Editor.deleteBackward(editor, {
            unit: "line"
          });
          break;
        }
        case "deleteHardLineForward": {
          Editor.deleteForward(editor, {
            unit: "block"
          });
          break;
        }
        case "deleteSoftLineForward": {
          Editor.deleteForward(editor, {
            unit: "line"
          });
          break;
        }
        case "deleteWordBackward": {
          Editor.deleteBackward(editor, {
            unit: "word"
          });
          break;
        }
        case "deleteWordForward": {
          Editor.deleteForward(editor, {
            unit: "word"
          });
          break;
        }
        case "insertLineBreak":
          Editor.insertSoftBreak(editor);
          break;
        case "insertParagraph": {
          Editor.insertBreak(editor);
          break;
        }
        case "insertFromComposition":
        case "insertFromDrop":
        case "insertFromPaste":
        case "insertFromYank":
        case "insertReplacementText":
        case "insertText": {
          type === "insertFromComposition" && ReactEditor.isComposing(editor) && (setIsComposing(!1), IS_COMPOSING.set(editor, !1)), data?.constructor.name === "DataTransfer" ? ReactEditor.insertData(editor, data) : typeof data == "string" && (native ? deferredOperations.current.push(() => Editor.insertText(editor, data)) : Editor.insertText(editor, data));
          break;
        }
      }
      const toRestore = EDITOR_TO_USER_SELECTION.get(editor)?.unref();
      EDITOR_TO_USER_SELECTION.delete(editor), toRestore && (!editor.selection || !Range.equals(editor.selection, toRestore)) && Transforms.select(editor, toRestore);
    }
  }, [editor, onDOMSelectionChange, onUserInput, propsOnDOMBeforeInput, readOnly, scheduleOnDOMSelectionChange]), callbackRef = useCallback((node2) => {
    node2 == null ? (onDOMSelectionChange.cancel(), scheduleOnDOMSelectionChange.cancel(), EDITOR_TO_ELEMENT.delete(editor), NODE_TO_ELEMENT.delete(editor), ref.current && HAS_BEFORE_INPUT_SUPPORT && ref.current.removeEventListener("beforeinput", onDOMBeforeInput)) : HAS_BEFORE_INPUT_SUPPORT && node2.addEventListener("beforeinput", onDOMBeforeInput), ref.current = node2, typeof forwardedRef == "function" ? forwardedRef(node2) : forwardedRef && (forwardedRef.current = node2);
  }, [onDOMSelectionChange, scheduleOnDOMSelectionChange, editor, onDOMBeforeInput, forwardedRef]);
  useIsomorphicLayoutEffect(() => {
    const window2 = ReactEditor.getWindow(editor), onSelectionChange = ({
      target
    }) => {
      const targetTagName = (target instanceof HTMLElement ? target : null)?.tagName;
      targetTagName === "INPUT" || targetTagName === "TEXTAREA" || scheduleOnDOMSelectionChange();
    };
    window2.document.addEventListener("selectionchange", onSelectionChange);
    const stoppedDragging = () => {
      state.isDraggingInternally = !1;
    };
    return window2.document.addEventListener("dragend", stoppedDragging), window2.document.addEventListener("drop", stoppedDragging), () => {
      window2.document.removeEventListener("selectionchange", onSelectionChange), window2.document.removeEventListener("dragend", stoppedDragging), window2.document.removeEventListener("drop", stoppedDragging);
    };
  }, [scheduleOnDOMSelectionChange, state]);
  const decorations = decorate([editor, []]), decorateContext = useDecorateContext(decorate), showPlaceholder = placeholder && editor.children.length === 1 && Array.from(Node$1.texts(editor)).length === 1 && Node$1.string(editor) === "" && !isComposing, placeHolderResizeHandler = useCallback((placeholderEl) => {
    setPlaceholderHeight(placeholderEl && showPlaceholder ? placeholderEl.getBoundingClientRect()?.height : void 0);
  }, [showPlaceholder]);
  if (showPlaceholder) {
    const start2 = Editor.start(editor, []);
    decorations.push({
      [PLACEHOLDER_SYMBOL]: !0,
      placeholder,
      onPlaceholderResize: placeHolderResizeHandler,
      anchor: start2,
      focus: start2
    });
  }
  const {
    marks: marks2
  } = editor;
  if (state.hasMarkPlaceholder = !1, editor.selection && Range.isCollapsed(editor.selection) && marks2) {
    const {
      anchor
    } = editor.selection, leaf2 = Node$1.leaf(editor, anchor.path), {
      text: _text,
      ...rest
    } = leaf2;
    if (!Text$1.equals(leaf2, marks2, {
      loose: !0
    })) {
      state.hasMarkPlaceholder = !0;
      const unset2 = Object.fromEntries(Object.keys(rest).map((mark) => [mark, null]));
      decorations.push({
        [MARK_PLACEHOLDER_SYMBOL]: !0,
        ...unset2,
        ...marks2,
        anchor,
        focus: anchor
      });
    }
  }
  return useEffect(() => {
    setTimeout(() => {
      const {
        selection
      } = editor;
      if (selection) {
        const {
          anchor
        } = selection, text = Node$1.leaf(editor, anchor.path);
        if (marks2 && !Text$1.equals(text, marks2, {
          loose: !0
        })) {
          EDITOR_TO_PENDING_INSERTION_MARKS.set(editor, marks2);
          return;
        }
      }
      EDITOR_TO_PENDING_INSERTION_MARKS.delete(editor);
    });
  }), useFlushDeferredSelectorsOnRender(), /* @__PURE__ */ jsx(ReadOnlyContext.Provider, { value: readOnly, children: /* @__PURE__ */ jsx(ComposingContext.Provider, { value: isComposing, children: /* @__PURE__ */ jsx(DecorateContext.Provider, { value: decorateContext, children: /* @__PURE__ */ jsx(RestoreDOM, { node: ref, receivedUserInput, children: /* @__PURE__ */ jsx(
    Component2,
    {
      role: readOnly ? void 0 : "textbox",
      "aria-multiline": readOnly ? void 0 : !0,
      translate: "no",
      ...attributes,
      spellCheck: HAS_BEFORE_INPUT_SUPPORT || !CAN_USE_DOM ? attributes.spellCheck : !1,
      autoCorrect: HAS_BEFORE_INPUT_SUPPORT || !CAN_USE_DOM ? attributes.autoCorrect : "false",
      autoCapitalize: HAS_BEFORE_INPUT_SUPPORT || !CAN_USE_DOM ? attributes.autoCapitalize : "false",
      "data-slate-editor": !0,
      "data-slate-node": "value",
      contentEditable: !readOnly,
      zindex: -1,
      suppressContentEditableWarning: !0,
      ref: callbackRef,
      style: {
        ...disableDefaultStyles ? {} : {
          // Allow positioning relative to the editable element.
          position: "relative",
          // Preserve adjacent whitespace and new lines.
          whiteSpace: "pre-wrap",
          // Allow words to break if they are too long.
          wordWrap: "break-word",
          // Make the minimum height that of the placeholder.
          ...placeholderHeight ? {
            minHeight: placeholderHeight
          } : {}
        },
        // Allow for passed-in styles to override anything.
        ...userStyle
      },
      onBeforeInput: useCallback((event) => {
        if (!HAS_BEFORE_INPUT_SUPPORT && !readOnly && !isEventHandled(event, attributes.onBeforeInput) && ReactEditor.hasSelectableTarget(editor, event.target) && (event.preventDefault(), !ReactEditor.isComposing(editor))) {
          const text = event.data;
          Editor.insertText(editor, text);
        }
      }, [attributes.onBeforeInput, editor, readOnly]),
      onInput: useCallback((event) => {
        if (!isEventHandled(event, attributes.onInput)) {
          if (androidInputManagerRef.current) {
            androidInputManagerRef.current.handleInput();
            return;
          }
          for (const op of deferredOperations.current)
            op();
          deferredOperations.current = [], ReactEditor.isFocused(editor) || handleNativeHistoryEvents(editor, event.nativeEvent);
        }
      }, [attributes.onInput, editor]),
      onBlur: useCallback((event) => {
        if (readOnly || state.isUpdatingSelection || !ReactEditor.hasSelectableTarget(editor, event.target) || isEventHandled(event, attributes.onBlur))
          return;
        const root = ReactEditor.findDocumentOrShadowRoot(editor);
        if (state.latestElement === root.activeElement)
          return;
        const {
          relatedTarget
        } = event, el = ReactEditor.toDOMNode(editor, editor);
        if (relatedTarget !== el && !(isDOMElement(relatedTarget) && relatedTarget.hasAttribute("data-slate-spacer"))) {
          if (relatedTarget != null && isDOMNode(relatedTarget) && ReactEditor.hasDOMNode(editor, relatedTarget)) {
            const node2 = ReactEditor.toSlateNode(editor, relatedTarget);
            if (Element$2.isElement(node2) && !editor.isVoid(node2))
              return;
          }
          IS_WEBKIT && getSelection(root)?.removeAllRanges(), IS_FOCUSED.delete(editor);
        }
      }, [readOnly, state.isUpdatingSelection, state.latestElement, editor, attributes.onBlur]),
      onClick: useCallback((event) => {
        if (ReactEditor.hasTarget(editor, event.target) && !isEventHandled(event, attributes.onClick) && isDOMNode(event.target)) {
          const node2 = ReactEditor.toSlateNode(editor, event.target), path2 = ReactEditor.findPath(editor, node2);
          if (!Editor.hasPath(editor, path2) || Node$1.get(editor, path2) !== node2)
            return;
          if (event.detail === TRIPLE_CLICK && path2.length >= 1) {
            let blockPath = path2;
            Element$2.isElement(node2) && Editor.isBlock(editor, node2) || (blockPath = Editor.above(editor, {
              match: (n2) => Element$2.isElement(n2) && Editor.isBlock(editor, n2),
              at: path2
            })?.[1] ?? path2.slice(0, 1));
            const range2 = Editor.range(editor, blockPath);
            Transforms.select(editor, range2);
            return;
          }
          if (readOnly)
            return;
          const start2 = Editor.start(editor, path2), end2 = Editor.end(editor, path2), startVoid = Editor.void(editor, {
            at: start2
          }), endVoid = Editor.void(editor, {
            at: end2
          });
          if (startVoid && endVoid && Path.equals(startVoid[1], endVoid[1])) {
            const range2 = Editor.range(editor, start2);
            Transforms.select(editor, range2);
          }
        }
      }, [editor, attributes.onClick, readOnly]),
      onCompositionEnd: useCallback((event) => {
        if (!isDOMEventTargetInput(event) && ReactEditor.hasSelectableTarget(editor, event.target)) {
          if (ReactEditor.isComposing(editor) && Promise.resolve().then(() => {
            setIsComposing(!1), IS_COMPOSING.set(editor, !1);
          }), androidInputManagerRef.current?.handleCompositionEnd(event), isEventHandled(event, attributes.onCompositionEnd) || IS_ANDROID)
            return;
          if (!IS_WEBKIT && !IS_FIREFOX_LEGACY && !IS_IOS && !IS_WECHATBROWSER && !IS_UC_MOBILE && event.data) {
            const placeholderMarks = EDITOR_TO_PENDING_INSERTION_MARKS.get(editor);
            EDITOR_TO_PENDING_INSERTION_MARKS.delete(editor), placeholderMarks !== void 0 && (EDITOR_TO_USER_MARKS.set(editor, editor.marks), editor.marks = placeholderMarks), Editor.insertText(editor, event.data);
            const userMarks = EDITOR_TO_USER_MARKS.get(editor);
            EDITOR_TO_USER_MARKS.delete(editor), userMarks !== void 0 && (editor.marks = userMarks);
          }
        }
      }, [attributes.onCompositionEnd, editor]),
      onCompositionUpdate: useCallback((event) => {
        ReactEditor.hasSelectableTarget(editor, event.target) && !isEventHandled(event, attributes.onCompositionUpdate) && !isDOMEventTargetInput(event) && (ReactEditor.isComposing(editor) || (setIsComposing(!0), IS_COMPOSING.set(editor, !0)));
      }, [attributes.onCompositionUpdate, editor]),
      onCompositionStart: useCallback((event) => {
        if (!isDOMEventTargetInput(event) && ReactEditor.hasSelectableTarget(editor, event.target)) {
          if (androidInputManagerRef.current?.handleCompositionStart(event), isEventHandled(event, attributes.onCompositionStart) || IS_ANDROID)
            return;
          setIsComposing(!0);
          const {
            selection
          } = editor;
          if (selection && Range.isExpanded(selection)) {
            Editor.deleteFragment(editor);
            return;
          }
        }
      }, [attributes.onCompositionStart, editor]),
      onCopy: useCallback((event) => {
        ReactEditor.hasSelectableTarget(editor, event.target) && !isEventHandled(event, attributes.onCopy) && !isDOMEventTargetInput(event) && (event.preventDefault(), ReactEditor.setFragmentData(editor, event.clipboardData, "copy"));
      }, [attributes.onCopy, editor]),
      onCut: useCallback((event) => {
        if (!readOnly && ReactEditor.hasSelectableTarget(editor, event.target) && !isEventHandled(event, attributes.onCut) && !isDOMEventTargetInput(event)) {
          event.preventDefault(), ReactEditor.setFragmentData(editor, event.clipboardData, "cut");
          const {
            selection
          } = editor;
          if (selection)
            if (Range.isExpanded(selection))
              Editor.deleteFragment(editor);
            else {
              const node2 = Node$1.parent(editor, selection.anchor.path);
              Editor.isVoid(editor, node2) && Transforms.delete(editor);
            }
        }
      }, [readOnly, editor, attributes.onCut]),
      onDragOver: useCallback((event) => {
        if (ReactEditor.hasTarget(editor, event.target) && !isEventHandled(event, attributes.onDragOver)) {
          const node2 = ReactEditor.toSlateNode(editor, event.target);
          Element$2.isElement(node2) && Editor.isVoid(editor, node2) && event.preventDefault();
        }
      }, [attributes.onDragOver, editor]),
      onDragStart: useCallback((event) => {
        if (!readOnly && ReactEditor.hasTarget(editor, event.target) && !isEventHandled(event, attributes.onDragStart)) {
          const node2 = ReactEditor.toSlateNode(editor, event.target), path2 = ReactEditor.findPath(editor, node2);
          if (Element$2.isElement(node2) && Editor.isVoid(editor, node2) || Editor.void(editor, {
            at: path2,
            voids: !0
          })) {
            const range2 = Editor.range(editor, path2);
            Transforms.select(editor, range2);
          }
          state.isDraggingInternally = !0, ReactEditor.setFragmentData(editor, event.dataTransfer, "drag");
        }
      }, [readOnly, editor, attributes.onDragStart, state]),
      onDrop: useCallback((event) => {
        if (!readOnly && ReactEditor.hasTarget(editor, event.target) && !isEventHandled(event, attributes.onDrop)) {
          event.preventDefault();
          const draggedRange = editor.selection, range2 = ReactEditor.findEventRange(editor, event), data = event.dataTransfer;
          Transforms.select(editor, range2), state.isDraggingInternally && draggedRange && !Range.equals(draggedRange, range2) && !Editor.void(editor, {
            at: range2,
            voids: !0
          }) && Transforms.delete(editor, {
            at: draggedRange
          }), ReactEditor.insertData(editor, data), ReactEditor.isFocused(editor) || ReactEditor.focus(editor);
        }
      }, [readOnly, editor, attributes.onDrop, state]),
      onDragEnd: useCallback((event) => {
        !readOnly && state.isDraggingInternally && attributes.onDragEnd && ReactEditor.hasTarget(editor, event.target) && attributes.onDragEnd(event);
      }, [readOnly, state, attributes, editor]),
      onFocus: useCallback((event) => {
        if (!readOnly && !state.isUpdatingSelection && ReactEditor.hasEditableTarget(editor, event.target) && !isEventHandled(event, attributes.onFocus)) {
          const el = ReactEditor.toDOMNode(editor, editor), root = ReactEditor.findDocumentOrShadowRoot(editor);
          if (state.latestElement = root.activeElement, IS_FIREFOX && event.target !== el) {
            el.focus();
            return;
          }
          IS_FOCUSED.set(editor, !0);
        }
      }, [readOnly, state, editor, attributes.onFocus]),
      onKeyDown: useCallback((event) => {
        if (!readOnly && ReactEditor.hasEditableTarget(editor, event.target)) {
          androidInputManagerRef.current?.handleKeyDown(event);
          const {
            nativeEvent
          } = event;
          if (ReactEditor.isComposing(editor) && nativeEvent.isComposing === !1 && (IS_COMPOSING.set(editor, !1), setIsComposing(!1)), isEventHandled(event, attributes.onKeyDown) || ReactEditor.isComposing(editor))
            return;
          const {
            selection
          } = editor, element = editor.children[selection !== null ? selection.focus.path[0] : 0], isRTL = getDirection(Node$1.string(element)) === "rtl";
          if (Hotkeys.isRedo(nativeEvent)) {
            event.preventDefault();
            const maybeHistoryEditor = editor;
            typeof maybeHistoryEditor.redo == "function" && maybeHistoryEditor.redo();
            return;
          }
          if (Hotkeys.isUndo(nativeEvent)) {
            event.preventDefault();
            const maybeHistoryEditor = editor;
            typeof maybeHistoryEditor.undo == "function" && maybeHistoryEditor.undo();
            return;
          }
          if (Hotkeys.isMoveLineBackward(nativeEvent)) {
            event.preventDefault(), Transforms.move(editor, {
              unit: "line",
              reverse: !0
            });
            return;
          }
          if (Hotkeys.isMoveLineForward(nativeEvent)) {
            event.preventDefault(), Transforms.move(editor, {
              unit: "line"
            });
            return;
          }
          if (Hotkeys.isExtendLineBackward(nativeEvent)) {
            event.preventDefault(), Transforms.move(editor, {
              unit: "line",
              edge: "focus",
              reverse: !0
            });
            return;
          }
          if (Hotkeys.isExtendLineForward(nativeEvent)) {
            event.preventDefault(), Transforms.move(editor, {
              unit: "line",
              edge: "focus"
            });
            return;
          }
          if (Hotkeys.isMoveBackward(nativeEvent)) {
            event.preventDefault(), selection && Range.isCollapsed(selection) ? Transforms.move(editor, {
              reverse: !isRTL
            }) : Transforms.collapse(editor, {
              edge: isRTL ? "end" : "start"
            });
            return;
          }
          if (Hotkeys.isMoveForward(nativeEvent)) {
            event.preventDefault(), selection && Range.isCollapsed(selection) ? Transforms.move(editor, {
              reverse: isRTL
            }) : Transforms.collapse(editor, {
              edge: isRTL ? "start" : "end"
            });
            return;
          }
          if (Hotkeys.isMoveWordBackward(nativeEvent)) {
            event.preventDefault(), selection && Range.isExpanded(selection) && Transforms.collapse(editor, {
              edge: "focus"
            }), Transforms.move(editor, {
              unit: "word",
              reverse: !isRTL
            });
            return;
          }
          if (Hotkeys.isMoveWordForward(nativeEvent)) {
            event.preventDefault(), selection && Range.isExpanded(selection) && Transforms.collapse(editor, {
              edge: "focus"
            }), Transforms.move(editor, {
              unit: "word",
              reverse: isRTL
            });
            return;
          }
          if (HAS_BEFORE_INPUT_SUPPORT) {
            if ((IS_CHROME || IS_WEBKIT) && selection && (Hotkeys.isDeleteBackward(nativeEvent) || Hotkeys.isDeleteForward(nativeEvent)) && Range.isCollapsed(selection)) {
              const currentNode = Node$1.parent(editor, selection.anchor.path);
              if (Element$2.isElement(currentNode) && Editor.isVoid(editor, currentNode) && (Editor.isInline(editor, currentNode) || Editor.isBlock(editor, currentNode))) {
                event.preventDefault(), Editor.deleteBackward(editor, {
                  unit: "block"
                });
                return;
              }
            }
          } else {
            if (Hotkeys.isBold(nativeEvent) || Hotkeys.isItalic(nativeEvent) || Hotkeys.isTransposeCharacter(nativeEvent)) {
              event.preventDefault();
              return;
            }
            if (Hotkeys.isSoftBreak(nativeEvent)) {
              event.preventDefault(), Editor.insertSoftBreak(editor);
              return;
            }
            if (Hotkeys.isSplitBlock(nativeEvent)) {
              event.preventDefault(), Editor.insertBreak(editor);
              return;
            }
            if (Hotkeys.isDeleteBackward(nativeEvent)) {
              event.preventDefault(), selection && Range.isExpanded(selection) ? Editor.deleteFragment(editor, {
                direction: "backward"
              }) : Editor.deleteBackward(editor);
              return;
            }
            if (Hotkeys.isDeleteForward(nativeEvent)) {
              event.preventDefault(), selection && Range.isExpanded(selection) ? Editor.deleteFragment(editor, {
                direction: "forward"
              }) : Editor.deleteForward(editor);
              return;
            }
            if (Hotkeys.isDeleteLineBackward(nativeEvent)) {
              event.preventDefault(), selection && Range.isExpanded(selection) ? Editor.deleteFragment(editor, {
                direction: "backward"
              }) : Editor.deleteBackward(editor, {
                unit: "line"
              });
              return;
            }
            if (Hotkeys.isDeleteLineForward(nativeEvent)) {
              event.preventDefault(), selection && Range.isExpanded(selection) ? Editor.deleteFragment(editor, {
                direction: "forward"
              }) : Editor.deleteForward(editor, {
                unit: "line"
              });
              return;
            }
            if (Hotkeys.isDeleteWordBackward(nativeEvent)) {
              event.preventDefault(), selection && Range.isExpanded(selection) ? Editor.deleteFragment(editor, {
                direction: "backward"
              }) : Editor.deleteBackward(editor, {
                unit: "word"
              });
              return;
            }
            if (Hotkeys.isDeleteWordForward(nativeEvent)) {
              event.preventDefault(), selection && Range.isExpanded(selection) ? Editor.deleteFragment(editor, {
                direction: "forward"
              }) : Editor.deleteForward(editor, {
                unit: "word"
              });
              return;
            }
          }
        }
      }, [readOnly, editor, attributes.onKeyDown]),
      onPaste: useCallback((event) => {
        !readOnly && ReactEditor.hasEditableTarget(editor, event.target) && !isEventHandled(event, attributes.onPaste) && (!HAS_BEFORE_INPUT_SUPPORT || isPlainTextOnlyPaste(event.nativeEvent) || IS_WEBKIT) && (event.preventDefault(), ReactEditor.insertData(editor, event.clipboardData));
      }, [readOnly, editor, attributes.onPaste]),
      children: /* @__PURE__ */ jsx(Children, { decorations, node: editor, renderElement, renderChunk, renderPlaceholder, renderLeaf, renderText })
    }
  ) }) }) }) });
}), DefaultPlaceholder = ({
  attributes,
  children
}) => (
  // COMPAT: Artificially add a line-break to the end on the placeholder element
  // to prevent Android IMEs to pick up its content in autocorrect and to auto-capitalize the first letter
  /* @__PURE__ */ jsxs("span", { ...attributes, children: [
    children,
    IS_ANDROID && /* @__PURE__ */ jsx("br", {})
  ] })
), defaultDecorate = () => [], defaultScrollSelectionIntoView = (editor, domRange) => {
  const isBackward = !!editor.selection && Range.isBackward(editor.selection), domFocusPoint = domRange.cloneRange();
  if (domFocusPoint.collapse(isBackward), domFocusPoint.getBoundingClientRect) {
    const leafEl = domFocusPoint.startContainer.parentElement, domRect = domFocusPoint.getBoundingClientRect();
    if (domRect.width === 0 && domRect.height === 0 && domRect.x === 0 && domRect.y === 0) {
      const leafRect = leafEl.getBoundingClientRect();
      if (leafRect.width > 0 || leafRect.height > 0)
        return;
    }
    leafEl.getBoundingClientRect = domFocusPoint.getBoundingClientRect.bind(domFocusPoint), scrollIntoView(leafEl, {
      scrollMode: "if-needed"
    }), delete leafEl.getBoundingClientRect;
  }
}, isEventHandled = (event, handler) => handler ? handler(event) ?? (event.isDefaultPrevented() || event.isPropagationStopped()) : !1, isDOMEventTargetInput = (event) => isDOMNode(event.target) && (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement), isDOMEventHandled = (event, handler) => handler ? handler(event) ?? event.defaultPrevented : !1, handleNativeHistoryEvents = (editor, event) => {
  const maybeHistoryEditor = editor;
  if (event.inputType === "historyUndo" && typeof maybeHistoryEditor.undo == "function") {
    maybeHistoryEditor.undo();
    return;
  }
  if (event.inputType === "historyRedo" && typeof maybeHistoryEditor.redo == "function") {
    maybeHistoryEditor.redo();
    return;
  }
}, FocusedContext = createContext(!1), REACT_MAJOR_VERSION = parseInt(React.version.split(".")[0], 10), Slate = (props) => {
  const {
    editor,
    children,
    onChange,
    onSelectionChange,
    onValueChange,
    initialValue,
    ...rest
  } = props;
  React.useState(() => {
    if (!Node$1.isNodeList(initialValue))
      throw new Error(`[Slate] initialValue is invalid! Expected a list of elements but got: ${Scrubber.stringify(initialValue)}`);
    if (!Editor.isEditor(editor))
      throw new Error(`[Slate] editor is invalid! You passed: ${Scrubber.stringify(editor)}`);
    editor.children = initialValue, Object.assign(editor, rest);
  });
  const {
    selectorContext,
    onChange: handleSelectorChange
  } = useSelectorContext(), onContextChange = useCallback(() => {
    onChange && onChange(editor.children), onSelectionChange && editor.operations.find((op) => op.type === "set_selection") && onSelectionChange(editor.selection), onValueChange && editor.operations.find((op) => op.type !== "set_selection") && onValueChange(editor.children), handleSelectorChange();
  }, [editor, handleSelectorChange, onChange, onSelectionChange, onValueChange]);
  useEffect(() => (EDITOR_TO_ON_CHANGE.set(editor, onContextChange), () => {
    EDITOR_TO_ON_CHANGE.set(editor, () => {
    });
  }), [editor, onContextChange]);
  const [isFocused, setIsFocused] = useState(ReactEditor.isFocused(editor));
  return useEffect(() => {
    setIsFocused(ReactEditor.isFocused(editor));
  }, [editor]), useIsomorphicLayoutEffect(() => {
    const fn = () => setIsFocused(ReactEditor.isFocused(editor));
    return REACT_MAJOR_VERSION >= 17 ? (document.addEventListener("focusin", fn), document.addEventListener("focusout", fn), () => {
      document.removeEventListener("focusin", fn), document.removeEventListener("focusout", fn);
    }) : (document.addEventListener("focus", fn, !0), document.addEventListener("blur", fn, !0), () => {
      document.removeEventListener("focus", fn, !0), document.removeEventListener("blur", fn, !0);
    });
  }, []), /* @__PURE__ */ jsx(SlateSelectorContext.Provider, { value: selectorContext, children: /* @__PURE__ */ jsx(EditorContext.Provider, { value: editor, children: /* @__PURE__ */ jsx(FocusedContext.Provider, { value: isFocused, children }) }) });
};
function getDefaultExportFromCjs(x) {
  return x && x.__esModule && Object.prototype.hasOwnProperty.call(x, "default") ? x.default : x;
}
var reactDom = { exports: {} }, reactDom_production = {};
/**
 * @license React
 * react-dom.production.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var hasRequiredReactDom_production;
function requireReactDom_production() {
  if (hasRequiredReactDom_production) return reactDom_production;
  hasRequiredReactDom_production = 1;
  var React$1 = React;
  function formatProdErrorMessage(code2) {
    var url = "https://react.dev/errors/" + code2;
    if (1 < arguments.length) {
      url += "?args[]=" + encodeURIComponent(arguments[1]);
      for (var i = 2; i < arguments.length; i++) url += "&args[]=" + encodeURIComponent(arguments[i]);
    }
    return "Minified React error #" + code2 + "; visit " + url + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  function noop2() {
  }
  var Internals = {
    d: {
      f: noop2,
      r: function() {
        throw Error(formatProdErrorMessage(522));
      },
      D: noop2,
      C: noop2,
      L: noop2,
      m: noop2,
      X: noop2,
      S: noop2,
      M: noop2
    },
    p: 0,
    findDOMNode: null
  }, REACT_PORTAL_TYPE = /* @__PURE__ */ Symbol.for("react.portal");
  function createPortal$1(children, containerInfo, implementation) {
    var key = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return {
      $$typeof: REACT_PORTAL_TYPE,
      key: key == null ? null : "" + key,
      children,
      containerInfo,
      implementation
    };
  }
  var ReactSharedInternals = React$1.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;
  function getCrossOriginStringAs(as, input) {
    if (as === "font") return "";
    if (typeof input == "string") return input === "use-credentials" ? input : "";
  }
  return reactDom_production.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = Internals, reactDom_production.createPortal = function(children, container) {
    var key = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
    if (!container || container.nodeType !== 1 && container.nodeType !== 9 && container.nodeType !== 11) throw Error(formatProdErrorMessage(299));
    return createPortal$1(children, container, null, key);
  }, reactDom_production.flushSync = function(fn) {
    var previousTransition = ReactSharedInternals.T, previousUpdatePriority = Internals.p;
    try {
      if (ReactSharedInternals.T = null, Internals.p = 2, fn) return fn();
    } finally {
      ReactSharedInternals.T = previousTransition, Internals.p = previousUpdatePriority, Internals.d.f();
    }
  }, reactDom_production.preconnect = function(href, options) {
    typeof href == "string" && (options ? (options = options.crossOrigin, options = typeof options == "string" ? options === "use-credentials" ? options : "" : void 0) : options = null, Internals.d.C(href, options));
  }, reactDom_production.prefetchDNS = function(href) {
    typeof href == "string" && Internals.d.D(href);
  }, reactDom_production.preinit = function(href, options) {
    if (typeof href == "string" && options && typeof options.as == "string") {
      var as = options.as, crossOrigin = getCrossOriginStringAs(as, options.crossOrigin), integrity = typeof options.integrity == "string" ? options.integrity : void 0, fetchPriority = typeof options.fetchPriority == "string" ? options.fetchPriority : void 0;
      as === "style" ? Internals.d.S(href, typeof options.precedence == "string" ? options.precedence : void 0, {
        crossOrigin,
        integrity,
        fetchPriority
      }) : as === "script" && Internals.d.X(href, {
        crossOrigin,
        integrity,
        fetchPriority,
        nonce: typeof options.nonce == "string" ? options.nonce : void 0
      });
    }
  }, reactDom_production.preinitModule = function(href, options) {
    if (typeof href == "string") if (typeof options == "object" && options !== null) {
      if (options.as == null || options.as === "script") {
        var crossOrigin = getCrossOriginStringAs(options.as, options.crossOrigin);
        Internals.d.M(href, {
          crossOrigin,
          integrity: typeof options.integrity == "string" ? options.integrity : void 0,
          nonce: typeof options.nonce == "string" ? options.nonce : void 0
        });
      }
    } else options == null && Internals.d.M(href);
  }, reactDom_production.preload = function(href, options) {
    if (typeof href == "string" && typeof options == "object" && options !== null && typeof options.as == "string") {
      var as = options.as, crossOrigin = getCrossOriginStringAs(as, options.crossOrigin);
      Internals.d.L(href, as, {
        crossOrigin,
        integrity: typeof options.integrity == "string" ? options.integrity : void 0,
        nonce: typeof options.nonce == "string" ? options.nonce : void 0,
        type: typeof options.type == "string" ? options.type : void 0,
        fetchPriority: typeof options.fetchPriority == "string" ? options.fetchPriority : void 0,
        referrerPolicy: typeof options.referrerPolicy == "string" ? options.referrerPolicy : void 0,
        imageSrcSet: typeof options.imageSrcSet == "string" ? options.imageSrcSet : void 0,
        imageSizes: typeof options.imageSizes == "string" ? options.imageSizes : void 0,
        media: typeof options.media == "string" ? options.media : void 0
      });
    }
  }, reactDom_production.preloadModule = function(href, options) {
    if (typeof href == "string") if (options) {
      var crossOrigin = getCrossOriginStringAs(options.as, options.crossOrigin);
      Internals.d.m(href, {
        as: typeof options.as == "string" && options.as !== "script" ? options.as : void 0,
        crossOrigin,
        integrity: typeof options.integrity == "string" ? options.integrity : void 0
      });
    } else Internals.d.m(href);
  }, reactDom_production.requestFormReset = function(form) {
    Internals.d.r(form);
  }, reactDom_production.unstable_batchedUpdates = function(fn, a) {
    return fn(a);
  }, reactDom_production.useFormState = function(action, initialState, permalink) {
    return ReactSharedInternals.H.useFormState(action, initialState, permalink);
  }, reactDom_production.useFormStatus = function() {
    return ReactSharedInternals.H.useHostTransitionStatus();
  }, reactDom_production.version = "19.2.3", reactDom_production;
}
var reactDom_development = {};
/**
 * @license React
 * react-dom.development.js
 *
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var hasRequiredReactDom_development;
function requireReactDom_development() {
  return hasRequiredReactDom_development || (hasRequiredReactDom_development = 1, process.env.NODE_ENV !== "production" && (function() {
    function noop2() {
    }
    function testStringCoercion(value) {
      return "" + value;
    }
    function createPortal$1(children, containerInfo, implementation) {
      var key = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
      try {
        testStringCoercion(key);
        var JSCompiler_inline_result = !1;
      } catch {
        JSCompiler_inline_result = !0;
      }
      return JSCompiler_inline_result && (console.error("The provided key is an unsupported type %s. This value must be coerced to a string before using it here.", typeof Symbol == "function" && Symbol.toStringTag && key[Symbol.toStringTag] || key.constructor.name || "Object"), testStringCoercion(key)), {
        $$typeof: REACT_PORTAL_TYPE,
        key: key == null ? null : "" + key,
        children,
        containerInfo,
        implementation
      };
    }
    function getCrossOriginStringAs(as, input) {
      if (as === "font") return "";
      if (typeof input == "string") return input === "use-credentials" ? input : "";
    }
    function getValueDescriptorExpectingObjectForWarning(thing) {
      return thing === null ? "`null`" : thing === void 0 ? "`undefined`" : thing === "" ? "an empty string" : 'something with type "' + typeof thing + '"';
    }
    function getValueDescriptorExpectingEnumForWarning(thing) {
      return thing === null ? "`null`" : thing === void 0 ? "`undefined`" : thing === "" ? "an empty string" : typeof thing == "string" ? JSON.stringify(thing) : typeof thing == "number" ? "`" + thing + "`" : 'something with type "' + typeof thing + '"';
    }
    function resolveDispatcher() {
      var dispatcher = ReactSharedInternals.H;
      return dispatcher === null && console.error(`Invalid hook call. Hooks can only be called inside of the body of a function component. This could happen for one of the following reasons:
1. You might have mismatching versions of React and the renderer (such as React DOM)
2. You might be breaking the Rules of Hooks
3. You might have more than one copy of React in the same app
See https://react.dev/link/invalid-hook-call for tips about how to debug and fix this problem.`), dispatcher;
    }
    typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStart(Error());
    var React$1 = React, Internals = {
      d: {
        f: noop2,
        r: function() {
          throw Error("Invalid form element. requestFormReset must be passed a form that was rendered by React.");
        },
        D: noop2,
        C: noop2,
        L: noop2,
        m: noop2,
        X: noop2,
        S: noop2,
        M: noop2
      },
      p: 0,
      findDOMNode: null
    }, REACT_PORTAL_TYPE = /* @__PURE__ */ Symbol.for("react.portal"), ReactSharedInternals = React$1.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;
    typeof Map == "function" && Map.prototype != null && typeof Map.prototype.forEach == "function" && typeof Set == "function" && Set.prototype != null && typeof Set.prototype.clear == "function" && typeof Set.prototype.forEach == "function" || console.error("React depends on Map and Set built-in types. Make sure that you load a polyfill in older browsers. https://reactjs.org/link/react-polyfills"), reactDom_development.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = Internals, reactDom_development.createPortal = function(children, container) {
      var key = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
      if (!container || container.nodeType !== 1 && container.nodeType !== 9 && container.nodeType !== 11) throw Error("Target container is not a DOM element.");
      return createPortal$1(children, container, null, key);
    }, reactDom_development.flushSync = function(fn) {
      var previousTransition = ReactSharedInternals.T, previousUpdatePriority = Internals.p;
      try {
        if (ReactSharedInternals.T = null, Internals.p = 2, fn) return fn();
      } finally {
        ReactSharedInternals.T = previousTransition, Internals.p = previousUpdatePriority, Internals.d.f() && console.error("flushSync was called from inside a lifecycle method. React cannot flush when React is already rendering. Consider moving this call to a scheduler task or micro task.");
      }
    }, reactDom_development.preconnect = function(href, options) {
      typeof href == "string" && href ? options != null && typeof options != "object" ? console.error("ReactDOM.preconnect(): Expected the `options` argument (second) to be an object but encountered %s instead. The only supported option at this time is `crossOrigin` which accepts a string.", getValueDescriptorExpectingEnumForWarning(options)) : options != null && typeof options.crossOrigin != "string" && console.error("ReactDOM.preconnect(): Expected the `crossOrigin` option (second argument) to be a string but encountered %s instead. Try removing this option or passing a string value instead.", getValueDescriptorExpectingObjectForWarning(options.crossOrigin)) : console.error("ReactDOM.preconnect(): Expected the `href` argument (first) to be a non-empty string but encountered %s instead.", getValueDescriptorExpectingObjectForWarning(href)), typeof href == "string" && (options ? (options = options.crossOrigin, options = typeof options == "string" ? options === "use-credentials" ? options : "" : void 0) : options = null, Internals.d.C(href, options));
    }, reactDom_development.prefetchDNS = function(href) {
      if (typeof href != "string" || !href) console.error("ReactDOM.prefetchDNS(): Expected the `href` argument (first) to be a non-empty string but encountered %s instead.", getValueDescriptorExpectingObjectForWarning(href));
      else if (1 < arguments.length) {
        var options = arguments[1];
        typeof options == "object" && options.hasOwnProperty("crossOrigin") ? console.error("ReactDOM.prefetchDNS(): Expected only one argument, `href`, but encountered %s as a second argument instead. This argument is reserved for future options and is currently disallowed. It looks like the you are attempting to set a crossOrigin property for this DNS lookup hint. Browsers do not perform DNS queries using CORS and setting this attribute on the resource hint has no effect. Try calling ReactDOM.prefetchDNS() with just a single string argument, `href`.", getValueDescriptorExpectingEnumForWarning(options)) : console.error("ReactDOM.prefetchDNS(): Expected only one argument, `href`, but encountered %s as a second argument instead. This argument is reserved for future options and is currently disallowed. Try calling ReactDOM.prefetchDNS() with just a single string argument, `href`.", getValueDescriptorExpectingEnumForWarning(options));
      }
      typeof href == "string" && Internals.d.D(href);
    }, reactDom_development.preinit = function(href, options) {
      if (typeof href == "string" && href ? options == null || typeof options != "object" ? console.error("ReactDOM.preinit(): Expected the `options` argument (second) to be an object with an `as` property describing the type of resource to be preinitialized but encountered %s instead.", getValueDescriptorExpectingEnumForWarning(options)) : options.as !== "style" && options.as !== "script" && console.error('ReactDOM.preinit(): Expected the `as` property in the `options` argument (second) to contain a valid value describing the type of resource to be preinitialized but encountered %s instead. Valid values for `as` are "style" and "script".', getValueDescriptorExpectingEnumForWarning(options.as)) : console.error("ReactDOM.preinit(): Expected the `href` argument (first) to be a non-empty string but encountered %s instead.", getValueDescriptorExpectingObjectForWarning(href)), typeof href == "string" && options && typeof options.as == "string") {
        var as = options.as, crossOrigin = getCrossOriginStringAs(as, options.crossOrigin), integrity = typeof options.integrity == "string" ? options.integrity : void 0, fetchPriority = typeof options.fetchPriority == "string" ? options.fetchPriority : void 0;
        as === "style" ? Internals.d.S(href, typeof options.precedence == "string" ? options.precedence : void 0, {
          crossOrigin,
          integrity,
          fetchPriority
        }) : as === "script" && Internals.d.X(href, {
          crossOrigin,
          integrity,
          fetchPriority,
          nonce: typeof options.nonce == "string" ? options.nonce : void 0
        });
      }
    }, reactDom_development.preinitModule = function(href, options) {
      var encountered = "";
      if (typeof href == "string" && href || (encountered += " The `href` argument encountered was " + getValueDescriptorExpectingObjectForWarning(href) + "."), options !== void 0 && typeof options != "object" ? encountered += " The `options` argument encountered was " + getValueDescriptorExpectingObjectForWarning(options) + "." : options && "as" in options && options.as !== "script" && (encountered += " The `as` option encountered was " + getValueDescriptorExpectingEnumForWarning(options.as) + "."), encountered) console.error("ReactDOM.preinitModule(): Expected up to two arguments, a non-empty `href` string and, optionally, an `options` object with a valid `as` property.%s", encountered);
      else switch (encountered = options && typeof options.as == "string" ? options.as : "script", encountered) {
        case "script":
          break;
        default:
          encountered = getValueDescriptorExpectingEnumForWarning(encountered), console.error('ReactDOM.preinitModule(): Currently the only supported "as" type for this function is "script" but received "%s" instead. This warning was generated for `href` "%s". In the future other module types will be supported, aligning with the import-attributes proposal. Learn more here: (https://github.com/tc39/proposal-import-attributes)', encountered, href);
      }
      typeof href == "string" && (typeof options == "object" && options !== null ? (options.as == null || options.as === "script") && (encountered = getCrossOriginStringAs(options.as, options.crossOrigin), Internals.d.M(href, {
        crossOrigin: encountered,
        integrity: typeof options.integrity == "string" ? options.integrity : void 0,
        nonce: typeof options.nonce == "string" ? options.nonce : void 0
      })) : options == null && Internals.d.M(href));
    }, reactDom_development.preload = function(href, options) {
      var encountered = "";
      if (typeof href == "string" && href || (encountered += " The `href` argument encountered was " + getValueDescriptorExpectingObjectForWarning(href) + "."), options == null || typeof options != "object" ? encountered += " The `options` argument encountered was " + getValueDescriptorExpectingObjectForWarning(options) + "." : typeof options.as == "string" && options.as || (encountered += " The `as` option encountered was " + getValueDescriptorExpectingObjectForWarning(options.as) + "."), encountered && console.error('ReactDOM.preload(): Expected two arguments, a non-empty `href` string and an `options` object with an `as` property valid for a `<link rel="preload" as="..." />` tag.%s', encountered), typeof href == "string" && typeof options == "object" && options !== null && typeof options.as == "string") {
        encountered = options.as;
        var crossOrigin = getCrossOriginStringAs(encountered, options.crossOrigin);
        Internals.d.L(href, encountered, {
          crossOrigin,
          integrity: typeof options.integrity == "string" ? options.integrity : void 0,
          nonce: typeof options.nonce == "string" ? options.nonce : void 0,
          type: typeof options.type == "string" ? options.type : void 0,
          fetchPriority: typeof options.fetchPriority == "string" ? options.fetchPriority : void 0,
          referrerPolicy: typeof options.referrerPolicy == "string" ? options.referrerPolicy : void 0,
          imageSrcSet: typeof options.imageSrcSet == "string" ? options.imageSrcSet : void 0,
          imageSizes: typeof options.imageSizes == "string" ? options.imageSizes : void 0,
          media: typeof options.media == "string" ? options.media : void 0
        });
      }
    }, reactDom_development.preloadModule = function(href, options) {
      var encountered = "";
      typeof href == "string" && href || (encountered += " The `href` argument encountered was " + getValueDescriptorExpectingObjectForWarning(href) + "."), options !== void 0 && typeof options != "object" ? encountered += " The `options` argument encountered was " + getValueDescriptorExpectingObjectForWarning(options) + "." : options && "as" in options && typeof options.as != "string" && (encountered += " The `as` option encountered was " + getValueDescriptorExpectingObjectForWarning(options.as) + "."), encountered && console.error('ReactDOM.preloadModule(): Expected two arguments, a non-empty `href` string and, optionally, an `options` object with an `as` property valid for a `<link rel="modulepreload" as="..." />` tag.%s', encountered), typeof href == "string" && (options ? (encountered = getCrossOriginStringAs(options.as, options.crossOrigin), Internals.d.m(href, {
        as: typeof options.as == "string" && options.as !== "script" ? options.as : void 0,
        crossOrigin: encountered,
        integrity: typeof options.integrity == "string" ? options.integrity : void 0
      })) : Internals.d.m(href));
    }, reactDom_development.requestFormReset = function(form) {
      Internals.d.r(form);
    }, reactDom_development.unstable_batchedUpdates = function(fn, a) {
      return fn(a);
    }, reactDom_development.useFormState = function(action, initialState, permalink) {
      return resolveDispatcher().useFormState(action, initialState, permalink);
    }, reactDom_development.useFormStatus = function() {
      return resolveDispatcher().useHostTransitionStatus();
    }, reactDom_development.version = "19.2.3", typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u" && typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop == "function" && __REACT_DEVTOOLS_GLOBAL_HOOK__.registerInternalModuleStop(Error());
  })()), reactDom_development;
}
var hasRequiredReactDom;
function requireReactDom() {
  if (hasRequiredReactDom) return reactDom.exports;
  hasRequiredReactDom = 1;
  function checkDCE() {
    if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function")) {
      if (process.env.NODE_ENV !== "production")
        throw new Error("^_^");
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(checkDCE);
      } catch (err) {
        console.error(err);
      }
    }
  }
  return process.env.NODE_ENV === "production" ? (checkDCE(), reactDom.exports = requireReactDom_production()) : reactDom.exports = requireReactDom_development(), reactDom.exports;
}
var reactDomExports = requireReactDom(), ReactDOM = /* @__PURE__ */ getDefaultExportFromCjs(reactDomExports);
const withReact = (editor, clipboardFormatKey = "x-slate-fragment") => {
  let e = editor;
  e = withDOM(e, clipboardFormatKey);
  const {
    onChange,
    apply: apply2,
    insertText: insertText2
  } = e;
  return e.getChunkSize = () => null, IS_ANDROID && (e.insertText = (text, options) => (EDITOR_TO_PENDING_SELECTION.delete(e), insertText2(text, options))), e.onChange = (options) => {
    (REACT_MAJOR_VERSION < 18 ? ReactDOM.unstable_batchedUpdates : (callback) => callback())(() => {
      onChange(options);
    });
  }, e.apply = (operation) => {
    if (operation.type === "move_node") {
      const parent2 = Node$1.parent(e, operation.path);
      if (e.getChunkSize(parent2)) {
        const node2 = Node$1.get(e, operation.path), chunkTree = getChunkTreeForNode(e, parent2), key = ReactEditor.findKey(e, node2);
        chunkTree.movedNodeKeys.add(key);
      }
    }
    apply2(operation);
  }, e;
}, EditorActorContext = createContext({}), IS_MAC = typeof window < "u" && /Mac|iPod|iPhone|iPad/.test(window.navigator.userAgent), modifiers = {
  alt: "altKey",
  control: "ctrlKey",
  meta: "metaKey",
  shift: "shiftKey"
}, aliases = {
  add: "+",
  break: "pause",
  cmd: "meta",
  command: "meta",
  ctl: "control",
  ctrl: "control",
  del: "delete",
  down: "arrowdown",
  esc: "escape",
  ins: "insert",
  left: "arrowleft",
  mod: IS_MAC ? "meta" : "control",
  opt: "alt",
  option: "alt",
  return: "enter",
  right: "arrowright",
  space: " ",
  spacebar: " ",
  up: "arrowup",
  win: "meta",
  windows: "meta"
}, keyCodes = {
  backspace: 8,
  tab: 9,
  enter: 13,
  shift: 16,
  control: 17,
  alt: 18,
  pause: 19,
  capslock: 20,
  escape: 27,
  " ": 32,
  pageup: 33,
  pagedown: 34,
  end: 35,
  home: 36,
  arrowleft: 37,
  arrowup: 38,
  arrowright: 39,
  arrowdown: 40,
  insert: 45,
  delete: 46,
  meta: 91,
  numlock: 144,
  scrolllock: 145,
  ";": 186,
  "=": 187,
  ",": 188,
  "-": 189,
  ".": 190,
  "/": 191,
  "`": 192,
  "[": 219,
  "\\": 220,
  "]": 221,
  "'": 222,
  f1: 112,
  f2: 113,
  f3: 114,
  f4: 115,
  f5: 116,
  f6: 117,
  f7: 118,
  f8: 119,
  f9: 120,
  f10: 121,
  f11: 122,
  f12: 123,
  f13: 124,
  f14: 125,
  f15: 126,
  f16: 127,
  f17: 128,
  f18: 129,
  f19: 130,
  f20: 131
};
function isHotkey(hotkey, event) {
  return compareHotkey(parseHotkey(hotkey), event);
}
function parseHotkey(hotkey) {
  const parsedHotkey = {
    altKey: !1,
    ctrlKey: !1,
    metaKey: !1,
    shiftKey: !1
  }, hotkeySegments = hotkey.replace("++", "+add").split("+");
  for (const rawHotkeySegment of hotkeySegments) {
    const optional = rawHotkeySegment.endsWith("?") && rawHotkeySegment.length > 1, hotkeySegment = optional ? rawHotkeySegment.slice(0, -1) : rawHotkeySegment, keyName = toKeyName(hotkeySegment), modifier = modifiers[keyName], alias = aliases[hotkeySegment], code2 = keyCodes[keyName];
    if (hotkeySegment.length > 1 && modifier === void 0 && alias === void 0 && code2 === void 0)
      throw new TypeError(`Unknown modifier: "${hotkeySegment}"`);
    (hotkeySegments.length === 1 || modifier === void 0) && (parsedHotkey.key = keyName, parsedHotkey.keyCode = toKeyCode(hotkeySegment)), modifier !== void 0 && (parsedHotkey[modifier] = optional ? null : !0);
  }
  return parsedHotkey;
}
function compareHotkey(parsedHotkey, event) {
  return (parsedHotkey.altKey == null || parsedHotkey.altKey === event.altKey) && (parsedHotkey.ctrlKey == null || parsedHotkey.ctrlKey === event.ctrlKey) && (parsedHotkey.metaKey == null || parsedHotkey.metaKey === event.metaKey) && (parsedHotkey.shiftKey == null || parsedHotkey.shiftKey === event.shiftKey) ? parsedHotkey.keyCode !== void 0 && event.keyCode !== void 0 ? parsedHotkey.keyCode === 91 && event.keyCode === 93 ? !0 : parsedHotkey.keyCode === event.keyCode : parsedHotkey.keyCode === event.keyCode || parsedHotkey.key === event.key.toLowerCase() : !1;
}
function toKeyCode(name) {
  const keyName = toKeyName(name);
  return keyCodes[keyName] ?? keyName.toUpperCase().charCodeAt(0);
}
function toKeyName(name) {
  const keyName = name.toLowerCase();
  return aliases[keyName] ?? keyName;
}
const reservedHotkeys = ["enter", "tab", "shift", "delete", "end"];
function performHotkey({
  editorActor,
  editor,
  portableTextEditor,
  hotkeys,
  event
}) {
  editorActor.getSnapshot().matches({
    "edit mode": "read only"
  }) || Object.keys(hotkeys).forEach((cat) => {
    if (cat === "marks")
      for (const hotkey in hotkeys[cat]) {
        if (reservedHotkeys.includes(hotkey))
          throw new Error(`The hotkey ${hotkey} is reserved!`);
        if (isHotkey(hotkey, event.nativeEvent)) {
          event.preventDefault();
          const possibleMark = hotkeys[cat];
          if (possibleMark) {
            const mark = possibleMark[hotkey];
            mark && editorActor.send({
              type: "behavior event",
              behaviorEvent: {
                type: "decorator.toggle",
                decorator: mark
              },
              editor
            });
          }
        }
      }
    if (cat === "custom")
      for (const hotkey in hotkeys[cat]) {
        if (reservedHotkeys.includes(hotkey))
          throw new Error(`The hotkey ${hotkey} is reserved!`);
        if (isHotkey(hotkey, event.nativeEvent)) {
          const possibleCommand = hotkeys[cat];
          if (possibleCommand) {
            const command = possibleCommand[hotkey];
            command && command(event, portableTextEditor);
          }
        }
      }
  });
}
function moveRangeByOperation(range2, operation) {
  const anchor = Point.transform(range2.anchor, operation), focus = Point.transform(range2.focus, operation);
  return anchor === null || focus === null ? null : Point.equals(anchor, range2.anchor) && Point.equals(focus, range2.focus) ? range2 : {
    anchor,
    focus
  };
}
const slateOperationCallback = ({
  input,
  sendBack
}) => {
  const originalApply = input.slateEditor.apply;
  return input.slateEditor.apply = (op) => {
    op.type !== "set_selection" && sendBack({
      type: "slate operation",
      operation: op
    }), originalApply(op);
  }, () => {
    input.slateEditor.apply = originalApply;
  };
}, rangeDecorationsMachine = setup({
  types: {
    context: {},
    input: {},
    events: {}
  },
  actions: {
    "update pending range decorations": assign({
      pendingRangeDecorations: ({
        context,
        event
      }) => event.type !== "range decorations updated" ? context.pendingRangeDecorations : event.rangeDecorations
    }),
    "set up initial range decorations": ({
      context
    }) => {
      const rangeDecorationState = [];
      for (const rangeDecoration of context.pendingRangeDecorations) {
        const slateRange = toSlateRange({
          context: {
            schema: context.schema,
            value: context.slateEditor.value,
            selection: rangeDecoration.selection
          },
          blockIndexMap: context.slateEditor.blockIndexMap
        });
        if (!Range.isRange(slateRange)) {
          rangeDecoration.onMoved?.({
            newSelection: null,
            rangeDecoration,
            origin: "local"
          });
          continue;
        }
        rangeDecorationState.push({
          rangeDecoration,
          ...slateRange
        });
      }
      context.slateEditor.decoratedRanges = rangeDecorationState;
    },
    "update range decorations": ({
      context,
      event
    }) => {
      if (event.type !== "range decorations updated")
        return;
      const rangeDecorationState = [];
      for (const rangeDecoration of event.rangeDecorations) {
        const slateRange = toSlateRange({
          context: {
            schema: context.schema,
            value: context.slateEditor.value,
            selection: rangeDecoration.selection
          },
          blockIndexMap: context.slateEditor.blockIndexMap
        });
        if (!Range.isRange(slateRange)) {
          rangeDecoration.onMoved?.({
            newSelection: null,
            rangeDecoration,
            origin: "local"
          });
          continue;
        }
        rangeDecorationState.push({
          rangeDecoration,
          ...slateRange
        });
      }
      context.slateEditor.decoratedRanges = rangeDecorationState;
    },
    "move range decorations": ({
      context,
      event
    }) => {
      if (event.type !== "slate operation")
        return;
      const rangeDecorationState = [];
      for (const decoratedRange of context.slateEditor.decoratedRanges) {
        const slateRange = toSlateRange({
          context: {
            schema: context.schema,
            value: context.slateEditor.value,
            selection: decoratedRange.rangeDecoration.selection
          },
          blockIndexMap: context.slateEditor.blockIndexMap
        });
        if (!Range.isRange(slateRange)) {
          decoratedRange.rangeDecoration.onMoved?.({
            newSelection: null,
            rangeDecoration: decoratedRange.rangeDecoration,
            origin: "local"
          });
          continue;
        }
        let newRange;
        if (newRange = moveRangeByOperation(slateRange, event.operation), newRange && newRange !== slateRange || newRange === null && slateRange) {
          const newRangeSelection = newRange ? slateRangeToSelection({
            schema: context.schema,
            editor: context.slateEditor,
            range: newRange
          }) : null;
          decoratedRange.rangeDecoration.onMoved?.({
            newSelection: newRangeSelection,
            rangeDecoration: decoratedRange.rangeDecoration,
            origin: "local"
          });
        }
        newRange !== null && rangeDecorationState.push({
          ...newRange || slateRange,
          rangeDecoration: {
            ...decoratedRange.rangeDecoration,
            selection: slateRangeToSelection({
              schema: context.schema,
              editor: context.slateEditor,
              range: newRange
            })
          }
        });
      }
      context.slateEditor.decoratedRanges = rangeDecorationState;
    },
    "assign readOnly": assign({
      readOnly: ({
        context,
        event
      }) => event.type !== "update read only" ? context.readOnly : event.readOnly
    }),
    "update decorate": assign({
      decorate: ({
        context
      }) => ({
        fn: createDecorate(context.schema, context.slateEditor)
      })
    })
  },
  actors: {
    "slate operation listener": fromCallback(slateOperationCallback)
  },
  guards: {
    "has pending range decorations": ({
      context
    }) => context.pendingRangeDecorations.length > 0,
    "has range decorations": ({
      context
    }) => context.slateEditor.decoratedRanges.length > 0,
    "has different decorations": ({
      context,
      event
    }) => {
      if (event.type !== "range decorations updated")
        return !1;
      const existingRangeDecorations = context.slateEditor.decoratedRanges.map((decoratedRange) => ({
        anchor: decoratedRange.rangeDecoration.selection?.anchor,
        focus: decoratedRange.rangeDecoration.selection?.focus,
        payload: decoratedRange.rangeDecoration.payload
      })), newRangeDecorations = event.rangeDecorations.map((rangeDecoration) => ({
        anchor: rangeDecoration.selection?.anchor,
        focus: rangeDecoration.selection?.focus,
        payload: rangeDecoration.payload
      }));
      return !isDeepEqual(existingRangeDecorations, newRangeDecorations);
    },
    "not read only": ({
      context
    }) => !context.readOnly,
    "should skip setup": ({
      context
    }) => context.skipSetup
  }
}).createMachine({
  id: "range decorations",
  context: ({
    input
  }) => ({
    readOnly: input.readOnly,
    pendingRangeDecorations: input.rangeDecorations,
    decoratedRanges: [],
    skipSetup: input.skipSetup,
    schema: input.schema,
    slateEditor: input.slateEditor,
    decorate: {
      fn: createDecorate(input.schema, input.slateEditor)
    }
  }),
  invoke: {
    src: "slate operation listener",
    input: ({
      context
    }) => ({
      slateEditor: context.slateEditor
    })
  },
  on: {
    "update read only": {
      actions: ["assign readOnly"]
    }
  },
  initial: "setting up",
  states: {
    "setting up": {
      always: [{
        guard: and(["should skip setup", "has pending range decorations"]),
        target: "ready",
        actions: ["set up initial range decorations", "update decorate"]
      }, {
        guard: "should skip setup",
        target: "ready"
      }],
      on: {
        "range decorations updated": {
          actions: ["update pending range decorations"]
        },
        ready: [{
          target: "ready",
          guard: "has pending range decorations",
          actions: ["set up initial range decorations", "update decorate"]
        }, {
          target: "ready"
        }]
      }
    },
    ready: {
      initial: "idle",
      on: {
        "range decorations updated": {
          target: ".idle",
          guard: "has different decorations",
          actions: ["update range decorations", "update decorate"]
        }
      },
      states: {
        idle: {
          on: {
            "slate operation": {
              target: "moving range decorations",
              guard: and(["has range decorations", "not read only"])
            }
          }
        },
        "moving range decorations": {
          entry: ["move range decorations"],
          always: {
            target: "idle"
          }
        }
      }
    }
  }
});
function createDecorate(schema, slateEditor) {
  return function([node2, path2]) {
    const defaultStyle = schema.styles.at(0)?.name, firstBlock = slateEditor.value[0];
    if (slateEditor.value.length === 1 && firstBlock && isEmptyTextBlock({
      schema
    }, firstBlock) && (!firstBlock.style || firstBlock.style === defaultStyle) && !firstBlock.listItem)
      return [{
        anchor: {
          path: [0, 0],
          offset: 0
        },
        focus: {
          path: [0, 0],
          offset: 0
        },
        placeholder: !0
      }];
    if (path2.length === 0)
      return [];
    if (!Element$2.isElement(node2) || node2.children.length === 0)
      return [];
    const blockIndex = path2.at(0);
    return blockIndex === void 0 ? [] : slateEditor.decoratedRanges.filter((decoratedRange) => Range.isCollapsed(decoratedRange) ? node2.children.some((_, childIndex) => Path.equals(decoratedRange.anchor.path, [blockIndex, childIndex]) && Path.equals(decoratedRange.focus.path, [blockIndex, childIndex])) : Range.intersection(decoratedRange, {
      anchor: {
        path: path2,
        offset: 0
      },
      focus: {
        path: path2,
        offset: 0
      }
    }) || Range.includes(decoratedRange, path2));
  };
}
const RelayActorContext = createContext({});
function RenderDefaultBlockObject(props) {
  const $ = c(4);
  let t0;
  $[0] === /* @__PURE__ */ Symbol.for("react.memo_cache_sentinel") ? (t0 = {
    userSelect: "none"
  }, $[0] = t0) : t0 = $[0];
  let t1;
  return $[1] !== props.blockObject._key || $[2] !== props.blockObject._type ? (t1 = /* @__PURE__ */ jsxs("div", { style: t0, children: [
    "[",
    props.blockObject._type,
    ": ",
    props.blockObject._key,
    "]"
  ] }), $[1] = props.blockObject._key, $[2] = props.blockObject._type, $[3] = t1) : t1 = $[3], t1;
}
function RenderDefaultInlineObject(props) {
  const $ = c(4);
  let t0;
  $[0] === /* @__PURE__ */ Symbol.for("react.memo_cache_sentinel") ? (t0 = {
    userSelect: "none"
  }, $[0] = t0) : t0 = $[0];
  let t1;
  return $[1] !== props.inlineObject._key || $[2] !== props.inlineObject._type ? (t1 = /* @__PURE__ */ jsxs("span", { style: t0, children: [
    "[",
    props.inlineObject._type,
    ": ",
    props.inlineObject._key,
    "]"
  ] }), $[1] = props.inlineObject._key, $[2] = props.inlineObject._type, $[3] = t1) : t1 = $[3], t1;
}
function DropIndicator() {
  const $ = c(1);
  let t0;
  return $[0] === /* @__PURE__ */ Symbol.for("react.memo_cache_sentinel") ? (t0 = /* @__PURE__ */ jsx("div", { contentEditable: !1, className: "pt-drop-indicator", style: {
    position: "absolute",
    width: "100%",
    height: 1,
    borderBottom: "1px solid currentColor",
    zIndex: 5
  }, children: /* @__PURE__ */ jsx("span", {}) }), $[0] = t0) : t0 = $[0], t0;
}
function serializePath(path2) {
  return path2.map((segment) => isKeyedSegment(segment) ? segment._key : segment).join(".");
}
function defaultCompare(a, b) {
  return a === b;
}
function useEditorSelector(editor, selector, t0) {
  const $ = c(3), compare = t0 === void 0 ? defaultCompare : t0;
  let t1;
  return $[0] !== editor || $[1] !== selector ? (t1 = (editorActorSnapshot) => {
    const snapshot = getEditorSnapshot({
      editorActorSnapshot,
      slateEditorInstance: editor._internal.slateEditor.instance
    });
    return selector(snapshot);
  }, $[0] = editor, $[1] = selector, $[2] = t1) : t1 = $[2], useSelector(editor._internal.editorActor, t1, compare);
}
function getEditorSnapshot({
  editorActorSnapshot,
  slateEditorInstance
}) {
  const selection = slateEditorInstance.selection ? slateRangeToSelection({
    schema: editorActorSnapshot.context.schema,
    editor: slateEditorInstance,
    range: slateEditorInstance.selection
  }) : null;
  return {
    blockIndexMap: slateEditorInstance.blockIndexMap,
    context: {
      converters: [...editorActorSnapshot.context.converters],
      keyGenerator: editorActorSnapshot.context.keyGenerator,
      readOnly: editorActorSnapshot.matches({
        "edit mode": "read only"
      }),
      schema: editorActorSnapshot.context.schema,
      selection,
      value: slateEditorInstance.value
    },
    decoratorState: slateEditorInstance.decoratorState
  };
}
const emptySet = /* @__PURE__ */ new Set(), defaultSelectionState = {
  focusedChildPath: void 0,
  selectedChildPaths: emptySet,
  focusedBlockKey: void 0,
  selectedBlockKeys: emptySet
}, SelectionStateContext = createContext(defaultSelectionState);
function SelectionStateProvider(t0) {
  const $ = c(5), {
    children
  } = t0, editorActor = useContext(EditorActorContext), slateEditor = useSlateStatic();
  let t1;
  $[0] !== slateEditor ? (t1 = (editorActorSnapshot) => {
    const snapshot = getEditorSnapshot({
      editorActorSnapshot,
      slateEditorInstance: slateEditor
    });
    if (!snapshot.context.selection)
      return defaultSelectionState;
    const isCollapsed = isSelectionCollapsed$1(snapshot);
    let focusedChildPath;
    if (isCollapsed) {
      const focusChild = getFocusChild$1(snapshot);
      focusChild && (focusedChildPath = serializePath(focusChild.path));
    }
    const selectedChildren = getSelectedChildren()(snapshot);
    let selectedChildPaths = selectedChildren.length > 0 ? new Set(selectedChildren.map(_temp$4)) : emptySet;
    isCollapsed && focusedChildPath && !selectedChildPaths.has(focusedChildPath) && (selectedChildPaths = new Set(selectedChildPaths), selectedChildPaths.add(focusedChildPath));
    const startPoint = getSelectionStartPoint(snapshot), endPoint = getSelectionEndPoint(snapshot), startBlockKey = startPoint ? getBlockKeyFromSelectionPoint(startPoint) : void 0, endBlockKey = endPoint ? getBlockKeyFromSelectionPoint(endPoint) : void 0;
    let selectedBlockKeys = emptySet;
    if (startBlockKey && endBlockKey) {
      const startBlockIndex = snapshot.blockIndexMap.get(startBlockKey), endBlockIndex = snapshot.blockIndexMap.get(endBlockKey);
      if (startBlockIndex !== void 0 && endBlockIndex !== void 0) {
        const minIndex = Math.min(startBlockIndex, endBlockIndex), maxIndex = Math.max(startBlockIndex, endBlockIndex);
        selectedBlockKeys = /* @__PURE__ */ new Set();
        for (const [key, index] of snapshot.blockIndexMap)
          index >= minIndex && index <= maxIndex && selectedBlockKeys.add(key);
      }
    }
    const focusedBlockKey = isCollapsed ? startBlockKey : void 0;
    return {
      focusedChildPath,
      selectedChildPaths: selectedChildPaths.size > 0 ? selectedChildPaths : emptySet,
      focusedBlockKey,
      selectedBlockKeys: selectedBlockKeys.size > 0 ? selectedBlockKeys : emptySet
    };
  }, $[0] = slateEditor, $[1] = t1) : t1 = $[1];
  const selectionState = useSelector(editorActor, t1, _temp2$3);
  let t2;
  return $[2] !== children || $[3] !== selectionState ? (t2 = /* @__PURE__ */ jsx(SelectionStateContext.Provider, { value: selectionState, children }), $[2] = children, $[3] = selectionState, $[4] = t2) : t2 = $[4], t2;
}
function _temp2$3(prev, next2) {
  if (prev.focusedChildPath !== next2.focusedChildPath)
    return !1;
  if (prev.selectedChildPaths !== next2.selectedChildPaths) {
    if (prev.selectedChildPaths.size !== next2.selectedChildPaths.size)
      return !1;
    for (const path2 of prev.selectedChildPaths)
      if (!next2.selectedChildPaths.has(path2))
        return !1;
  }
  if (prev.focusedBlockKey !== next2.focusedBlockKey)
    return !1;
  if (prev.selectedBlockKeys !== next2.selectedBlockKeys) {
    if (prev.selectedBlockKeys.size !== next2.selectedBlockKeys.size)
      return !1;
    for (const key_0 of prev.selectedBlockKeys)
      if (!next2.selectedBlockKeys.has(key_0))
        return !1;
  }
  return !0;
}
function _temp$4(child) {
  return serializePath(child.path);
}
function RenderBlockObject(props) {
  const $ = c(34), blockObjectRef = useRef(null), {
    selectedBlockKeys,
    focusedBlockKey
  } = useContext(SelectionStateContext);
  let t0;
  $[0] !== props.element._key || $[1] !== selectedBlockKeys ? (t0 = selectedBlockKeys.has(props.element._key), $[0] = props.element._key, $[1] = selectedBlockKeys, $[2] = t0) : t0 = $[2];
  const selected = t0, focused = focusedBlockKey === props.element._key;
  let t1;
  if ($[3] !== props.element._type || $[4] !== props.legacySchema.blockObjects) {
    let t22;
    $[6] !== props.element._type ? (t22 = (schemaType) => schemaType.name === props.element._type, $[6] = props.element._type, $[7] = t22) : t22 = $[7], t1 = props.legacySchema.blockObjects.find(t22), $[3] = props.element._type, $[4] = props.legacySchema.blockObjects, $[5] = t1;
  } else
    t1 = $[5];
  const legacySchemaType = t1;
  legacySchemaType || console.error(`Unable to find Block Object "${props.element._type}" in Schema`);
  let t2;
  $[8] !== props.blockObject || $[9] !== props.element._key || $[10] !== props.element._type ? (t2 = props.blockObject ?? {
    _key: props.element._key,
    _type: props.element._type
  }, $[8] = props.blockObject, $[9] = props.element._key, $[10] = props.element._type, $[11] = t2) : t2 = $[11];
  const blockObject = t2;
  let t3;
  $[12] !== props.dropPosition ? (t3 = props.dropPosition === "start" ? /* @__PURE__ */ jsx(DropIndicator, {}) : null, $[12] = props.dropPosition, $[13] = t3) : t3 = $[13];
  const t4 = !props.readOnly;
  let t5;
  $[14] !== blockObject || $[15] !== focused || $[16] !== legacySchemaType || $[17] !== props.element._key || $[18] !== props.renderBlock || $[19] !== selected ? (t5 = props.renderBlock && legacySchemaType ? /* @__PURE__ */ jsx(RenderBlock$1, { renderBlock: props.renderBlock, editorElementRef: blockObjectRef, focused, path: [{
    _key: props.element._key
  }], schemaType: legacySchemaType, selected, type: legacySchemaType, value: blockObject, children: /* @__PURE__ */ jsx(RenderDefaultBlockObject, { blockObject }) }) : /* @__PURE__ */ jsx(RenderDefaultBlockObject, { blockObject }), $[14] = blockObject, $[15] = focused, $[16] = legacySchemaType, $[17] = props.element._key, $[18] = props.renderBlock, $[19] = selected, $[20] = t5) : t5 = $[20];
  let t6;
  $[21] !== t4 || $[22] !== t5 ? (t6 = /* @__PURE__ */ jsx("div", { ref: blockObjectRef, contentEditable: !1, draggable: t4, children: t5 }), $[21] = t4, $[22] = t5, $[23] = t6) : t6 = $[23];
  let t7;
  $[24] !== props.dropPosition ? (t7 = props.dropPosition === "end" ? /* @__PURE__ */ jsx(DropIndicator, {}) : null, $[24] = props.dropPosition, $[25] = t7) : t7 = $[25];
  let t8;
  return $[26] !== props.attributes || $[27] !== props.children || $[28] !== props.element._key || $[29] !== props.element._type || $[30] !== t3 || $[31] !== t6 || $[32] !== t7 ? (t8 = /* @__PURE__ */ jsxs("div", { ...props.attributes, className: "pt-block pt-object-block", "data-block-key": props.element._key, "data-block-name": props.element._type, "data-block-type": "object", children: [
    t3,
    props.children,
    t6,
    t7
  ] }), $[26] = props.attributes, $[27] = props.children, $[28] = props.element._key, $[29] = props.element._type, $[30] = t3, $[31] = t6, $[32] = t7, $[33] = t8) : t8 = $[33], t8;
}
function RenderBlock$1({
  renderBlock,
  children,
  editorElementRef,
  focused,
  path: path2,
  schemaType,
  selected,
  type,
  value
}) {
  return renderBlock({
    children,
    editorElementRef,
    focused,
    path: path2,
    schemaType,
    selected,
    type,
    value
  });
}
function RenderInlineObject(props) {
  const $ = c(28), inlineObjectRef = useRef(null), slateEditor = useSlateStatic();
  let t0;
  if ($[0] !== props.element._type || $[1] !== props.legacySchema.inlineObjects) {
    let t12;
    $[3] !== props.element._type ? (t12 = (inlineObject) => inlineObject.name === props.element._type, $[3] = props.element._type, $[4] = t12) : t12 = $[4], t0 = props.legacySchema.inlineObjects.find(t12), $[0] = props.element._type, $[1] = props.legacySchema.inlineObjects, $[2] = t0;
  } else
    t0 = $[2];
  const legacySchemaType = t0;
  legacySchemaType || console.error(`Unable to find Inline Object "${props.element._type}" in Schema`);
  const slatePath = DOMEditor.findPath(slateEditor, props.element), [block] = getPointBlock({
    editor: slateEditor,
    point: {
      path: slatePath,
      offset: 0
    }
  });
  block || console.error(`Unable to find parent block of inline object ${props.element._key}`);
  const path2 = block ? [{
    _key: block._key
  }, "children", {
    _key: props.element._key
  }] : void 0, selectionState = useContext(SelectionStateContext), serializedPath = path2 ? serializePath(path2) : void 0, selected = serializedPath ? selectionState.selectedChildPaths.has(serializedPath) : !1, focused = serializedPath ? selectionState.focusedChildPath === serializedPath : !1;
  let t1;
  $[5] !== props.element ? (t1 = "value" in props.element && typeof props.element.value == "object" ? props.element.value : {}, $[5] = props.element, $[6] = t1) : t1 = $[6];
  let t2;
  $[7] !== props.element._key || $[8] !== props.element._type || $[9] !== t1 ? (t2 = {
    _key: props.element._key,
    _type: props.element._type,
    ...t1
  }, $[7] = props.element._key, $[8] = props.element._type, $[9] = t1, $[10] = t2) : t2 = $[10];
  const inlineObject_0 = t2;
  let t3;
  $[11] === /* @__PURE__ */ Symbol.for("react.memo_cache_sentinel") ? (t3 = {
    display: "inline-block"
  }, $[11] = t3) : t3 = $[11];
  const t4 = !props.readOnly;
  let t5;
  $[12] !== focused || $[13] !== inlineObject_0 || $[14] !== legacySchemaType || $[15] !== path2 || $[16] !== props.renderChild || $[17] !== selected ? (t5 = props.renderChild && path2 && legacySchemaType ? /* @__PURE__ */ jsx(RenderChild$1, { renderChild: props.renderChild, annotations: [], editorElementRef: inlineObjectRef, selected, focused, path: path2, schemaType: legacySchemaType, value: inlineObject_0, type: legacySchemaType, children: /* @__PURE__ */ jsx(RenderDefaultInlineObject, { inlineObject: inlineObject_0 }) }) : /* @__PURE__ */ jsx(RenderDefaultInlineObject, { inlineObject: inlineObject_0 }), $[12] = focused, $[13] = inlineObject_0, $[14] = legacySchemaType, $[15] = path2, $[16] = props.renderChild, $[17] = selected, $[18] = t5) : t5 = $[18];
  let t6;
  $[19] !== t4 || $[20] !== t5 ? (t6 = /* @__PURE__ */ jsx("span", { ref: inlineObjectRef, style: t3, draggable: t4, children: t5 }), $[19] = t4, $[20] = t5, $[21] = t6) : t6 = $[21];
  let t7;
  return $[22] !== inlineObject_0._key || $[23] !== inlineObject_0._type || $[24] !== props.attributes || $[25] !== props.children || $[26] !== t6 ? (t7 = /* @__PURE__ */ jsxs("span", { ...props.attributes, className: "pt-inline-object", "data-child-key": inlineObject_0._key, "data-child-name": inlineObject_0._type, "data-child-type": "object", children: [
    props.children,
    t6
  ] }), $[22] = inlineObject_0._key, $[23] = inlineObject_0._type, $[24] = props.attributes, $[25] = props.children, $[26] = t6, $[27] = t7) : t7 = $[27], t7;
}
function RenderChild$1({
  renderChild,
  annotations,
  children,
  editorElementRef,
  focused,
  path: path2,
  schemaType,
  selected,
  value,
  type
}) {
  return renderChild({
    annotations,
    children,
    editorElementRef,
    focused,
    path: path2,
    schemaType,
    selected,
    value,
    type
  });
}
function RenderTextBlock(props) {
  const $ = c(76), blockRef = useRef(null), {
    selectedBlockKeys,
    focusedBlockKey
  } = useContext(SelectionStateContext);
  let t0;
  $[0] !== props.textBlock._key || $[1] !== selectedBlockKeys ? (t0 = selectedBlockKeys.has(props.textBlock._key), $[0] = props.textBlock._key, $[1] = selectedBlockKeys, $[2] = t0) : t0 = $[2];
  const selected = t0, focused = focusedBlockKey === props.textBlock._key;
  let t1;
  $[3] !== props.textBlock._key ? (t1 = (editor) => editor.listIndexMap.get(props.textBlock._key), $[3] = props.textBlock._key, $[4] = t1) : t1 = $[4];
  const listIndex = useSlateSelector(t1);
  let children = props.children;
  if (props.renderStyle && props.textBlock.style) {
    let t22;
    $[5] !== props.legacySchema || $[6] !== props.textBlock.style ? (t22 = props.textBlock.style !== void 0 ? props.legacySchema.styles.find((style) => style.value === props.textBlock.style) : void 0, $[5] = props.legacySchema, $[6] = props.textBlock.style, $[7] = t22) : t22 = $[7];
    const legacyStyleSchemaType = t22;
    if (legacyStyleSchemaType) {
      let t32;
      $[8] !== props.textBlock._key ? (t32 = [{
        _key: props.textBlock._key
      }], $[8] = props.textBlock._key, $[9] = t32) : t32 = $[9];
      let t42;
      $[10] !== children || $[11] !== focused || $[12] !== legacyStyleSchemaType || $[13] !== props.renderStyle || $[14] !== props.textBlock || $[15] !== selected || $[16] !== t32 ? (t42 = /* @__PURE__ */ jsx(RenderStyle, { renderStyle: props.renderStyle, block: props.textBlock, editorElementRef: blockRef, focused, path: t32, schemaType: legacyStyleSchemaType, selected, value: props.textBlock.style, children }), $[10] = children, $[11] = focused, $[12] = legacyStyleSchemaType, $[13] = props.renderStyle, $[14] = props.textBlock, $[15] = selected, $[16] = t32, $[17] = t42) : t42 = $[17], children = t42;
    } else
      console.error(`Unable to find Schema type for text block style ${props.textBlock.style}`);
  }
  if (props.renderListItem && props.textBlock.listItem) {
    let t22;
    if ($[18] !== props.legacySchema.lists || $[19] !== props.textBlock.listItem) {
      let t32;
      $[21] !== props.textBlock.listItem ? (t32 = (list) => list.value === props.textBlock.listItem, $[21] = props.textBlock.listItem, $[22] = t32) : t32 = $[22], t22 = props.legacySchema.lists.find(t32), $[18] = props.legacySchema.lists, $[19] = props.textBlock.listItem, $[20] = t22;
    } else
      t22 = $[20];
    const legacyListItemSchemaType = t22;
    if (legacyListItemSchemaType) {
      const t32 = props.textBlock.level ?? 1;
      let t42;
      $[23] !== props.textBlock._key ? (t42 = [{
        _key: props.textBlock._key
      }], $[23] = props.textBlock._key, $[24] = t42) : t42 = $[24];
      let t52;
      $[25] !== children || $[26] !== focused || $[27] !== legacyListItemSchemaType || $[28] !== props.renderListItem || $[29] !== props.textBlock || $[30] !== selected || $[31] !== t32 || $[32] !== t42 ? (t52 = /* @__PURE__ */ jsx(RenderListItem, { renderListItem: props.renderListItem, block: props.textBlock, editorElementRef: blockRef, focused, level: t32, path: t42, selected, value: props.textBlock.listItem, schemaType: legacyListItemSchemaType, children }), $[25] = children, $[26] = focused, $[27] = legacyListItemSchemaType, $[28] = props.renderListItem, $[29] = props.textBlock, $[30] = selected, $[31] = t32, $[32] = t42, $[33] = t52) : t52 = $[33], children = t52;
    } else
      console.error(`Unable to find Schema type for text block list item ${props.textBlock.listItem}`);
  }
  const t2 = props.attributes;
  let t3;
  $[34] !== props.textBlock.style ? (t3 = props.textBlock.style ? [`pt-text-block-style-${props.textBlock.style}`] : [], $[34] = props.textBlock.style, $[35] = t3) : t3 = $[35];
  let t4;
  $[36] !== props.textBlock.level || $[37] !== props.textBlock.listItem ? (t4 = props.textBlock.listItem ? ["pt-list-item", `pt-list-item-${props.textBlock.listItem}`, `pt-list-item-level-${props.textBlock.level ?? 1}`] : [], $[36] = props.textBlock.level, $[37] = props.textBlock.listItem, $[38] = t4) : t4 = $[38];
  let t5;
  $[39] !== t3 || $[40] !== t4 ? (t5 = ["pt-block", "pt-text-block", ...t3, ...t4], $[39] = t3, $[40] = t4, $[41] = t5) : t5 = $[41];
  const t6 = t5.join(" ");
  let t7;
  $[42] !== props.textBlock.listItem ? (t7 = props.textBlock.listItem !== void 0 ? {
    "data-list-item": props.textBlock.listItem
  } : {}, $[42] = props.textBlock.listItem, $[43] = t7) : t7 = $[43];
  let t8;
  $[44] !== props.textBlock.level ? (t8 = props.textBlock.level !== void 0 ? {
    "data-level": props.textBlock.level
  } : {}, $[44] = props.textBlock.level, $[45] = t8) : t8 = $[45];
  let t9;
  $[46] !== props.textBlock.style ? (t9 = props.textBlock.style !== void 0 ? {
    "data-style": props.textBlock.style
  } : {}, $[46] = props.textBlock.style, $[47] = t9) : t9 = $[47];
  let t10;
  $[48] !== listIndex ? (t10 = listIndex !== void 0 ? {
    "data-list-index": listIndex
  } : {}, $[48] = listIndex, $[49] = t10) : t10 = $[49];
  let t11;
  $[50] !== props.dropPosition ? (t11 = props.dropPosition === "start" ? /* @__PURE__ */ jsx(DropIndicator, {}) : null, $[50] = props.dropPosition, $[51] = t11) : t11 = $[51];
  let t12;
  $[52] !== children || $[53] !== focused || $[54] !== props.legacySchema || $[55] !== props.renderBlock || $[56] !== props.textBlock || $[57] !== selected ? (t12 = props.renderBlock ? /* @__PURE__ */ jsx(RenderBlock, { renderBlock: props.renderBlock, editorElementRef: blockRef, focused, level: props.textBlock.level, listItem: props.textBlock.listItem, path: [{
    _key: props.textBlock._key
  }], selected, schemaType: props.legacySchema.block, style: props.textBlock.style, type: props.legacySchema.block, value: props.textBlock, children }) : children, $[52] = children, $[53] = focused, $[54] = props.legacySchema, $[55] = props.renderBlock, $[56] = props.textBlock, $[57] = selected, $[58] = t12) : t12 = $[58];
  let t13;
  $[59] !== t12 ? (t13 = /* @__PURE__ */ jsx("div", { ref: blockRef, children: t12 }), $[59] = t12, $[60] = t13) : t13 = $[60];
  let t14;
  $[61] !== props.dropPosition ? (t14 = props.dropPosition === "end" ? /* @__PURE__ */ jsx(DropIndicator, {}) : null, $[61] = props.dropPosition, $[62] = t14) : t14 = $[62];
  let t15;
  return $[63] !== props.attributes || $[64] !== props.spellCheck || $[65] !== props.textBlock._key || $[66] !== props.textBlock._type || $[67] !== t10 || $[68] !== t11 || $[69] !== t13 || $[70] !== t14 || $[71] !== t6 || $[72] !== t7 || $[73] !== t8 || $[74] !== t9 ? (t15 = /* @__PURE__ */ jsxs("div", { ...t2, className: t6, spellCheck: props.spellCheck, "data-block-key": props.textBlock._key, "data-block-name": props.textBlock._type, "data-block-type": "text", ...t7, ...t8, ...t9, ...t10, children: [
    t11,
    t13,
    t14
  ] }), $[63] = props.attributes, $[64] = props.spellCheck, $[65] = props.textBlock._key, $[66] = props.textBlock._type, $[67] = t10, $[68] = t11, $[69] = t13, $[70] = t14, $[71] = t6, $[72] = t7, $[73] = t8, $[74] = t9, $[75] = t15) : t15 = $[75], t15;
}
function RenderBlock({
  renderBlock,
  children,
  editorElementRef,
  focused,
  level,
  listItem,
  path: path2,
  selected,
  style,
  schemaType,
  type,
  value
}) {
  return renderBlock({
    children,
    editorElementRef,
    focused,
    level,
    listItem,
    path: path2,
    selected,
    style,
    schemaType,
    type,
    value
  });
}
function RenderListItem({
  renderListItem,
  block,
  children,
  editorElementRef,
  focused,
  level,
  path: path2,
  schemaType,
  selected,
  value
}) {
  return renderListItem({
    block,
    children,
    editorElementRef,
    focused,
    level,
    path: path2,
    schemaType,
    selected,
    value
  });
}
function RenderStyle({
  renderStyle,
  block,
  children,
  editorElementRef,
  focused,
  path: path2,
  schemaType,
  selected,
  value
}) {
  return renderStyle({
    block,
    children,
    editorElementRef,
    focused,
    path: path2,
    schemaType,
    selected,
    value
  });
}
function RenderElement(props) {
  const $ = c(36), editorActor = useContext(EditorActorContext), schema = useSelector(editorActor, _temp$3), legacySchema = useSelector(editorActor, _temp2$2), slateStatic = useSlateStatic();
  if ("__inline" in props.element && props.element.__inline === !0) {
    let t02;
    return $[0] !== legacySchema || $[1] !== props.attributes || $[2] !== props.children || $[3] !== props.element || $[4] !== props.readOnly || $[5] !== props.renderChild || $[6] !== schema ? (t02 = /* @__PURE__ */ jsx(RenderInlineObject, { attributes: props.attributes, element: props.element, legacySchema, readOnly: props.readOnly, renderChild: props.renderChild, schema, children: props.children }), $[0] = legacySchema, $[1] = props.attributes, $[2] = props.children, $[3] = props.element, $[4] = props.readOnly, $[5] = props.renderChild, $[6] = schema, $[7] = t02) : t02 = $[7], t02;
  }
  let block, t0;
  if ($[8] !== props.element._key || $[9] !== schema || $[10] !== slateStatic.blockIndexMap || $[11] !== slateStatic.value) {
    const blockIndex = slateStatic.blockIndexMap.get(props.element._key);
    block = blockIndex !== void 0 ? slateStatic.value.at(blockIndex) : void 0, t0 = isTextBlock({
      schema
    }, block), $[8] = props.element._key, $[9] = schema, $[10] = slateStatic.blockIndexMap, $[11] = slateStatic.value, $[12] = block, $[13] = t0;
  } else
    block = $[12], t0 = $[13];
  if (t0) {
    const t12 = props.dropPosition?.blockKey === props.element._key ? props.dropPosition.positionBlock : void 0;
    let t22;
    return $[14] !== block || $[15] !== legacySchema || $[16] !== props.attributes || $[17] !== props.children || $[18] !== props.element || $[19] !== props.readOnly || $[20] !== props.renderBlock || $[21] !== props.renderListItem || $[22] !== props.renderStyle || $[23] !== props.spellCheck || $[24] !== t12 ? (t22 = /* @__PURE__ */ jsx(RenderTextBlock, { attributes: props.attributes, dropPosition: t12, element: props.element, legacySchema, readOnly: props.readOnly, renderBlock: props.renderBlock, renderListItem: props.renderListItem, renderStyle: props.renderStyle, spellCheck: props.spellCheck, textBlock: block, children: props.children }), $[14] = block, $[15] = legacySchema, $[16] = props.attributes, $[17] = props.children, $[18] = props.element, $[19] = props.readOnly, $[20] = props.renderBlock, $[21] = props.renderListItem, $[22] = props.renderStyle, $[23] = props.spellCheck, $[24] = t12, $[25] = t22) : t22 = $[25], t22;
  }
  const t1 = props.dropPosition?.blockKey === props.element._key ? props.dropPosition.positionBlock : void 0;
  let t2;
  return $[26] !== block || $[27] !== legacySchema || $[28] !== props.attributes || $[29] !== props.children || $[30] !== props.element || $[31] !== props.readOnly || $[32] !== props.renderBlock || $[33] !== schema || $[34] !== t1 ? (t2 = /* @__PURE__ */ jsx(RenderBlockObject, { attributes: props.attributes, blockObject: block, dropPosition: t1, element: props.element, legacySchema, readOnly: props.readOnly, renderBlock: props.renderBlock, schema, children: props.children }), $[26] = block, $[27] = legacySchema, $[28] = props.attributes, $[29] = props.children, $[30] = props.element, $[31] = props.readOnly, $[32] = props.renderBlock, $[33] = schema, $[34] = t1, $[35] = t2) : t2 = $[35], t2;
}
function _temp2$2(s_0) {
  return s_0.context.getLegacySchema();
}
function _temp$3(s) {
  return s.context.schema;
}
function RenderSpan(props) {
  const $ = c(36), slateEditor = useSlateStatic(), editorActor = useContext(EditorActorContext), legacySchema = useSelector(editorActor, _temp$2), spanRef = useRef(null), parent2 = props.children.props.parent, block = parent2 && slateEditor.isTextBlock(parent2) ? parent2 : void 0;
  let t0;
  $[0] !== block || $[1] !== props.leaf._key ? (t0 = block ? [{
    _key: block._key
  }, "children", {
    _key: props.leaf._key
  }] : void 0, $[0] = block, $[1] = props.leaf._key, $[2] = t0) : t0 = $[2];
  const path2 = t0, selectionState = useContext(SelectionStateContext);
  let focused, t1;
  if ($[3] !== path2 || $[4] !== selectionState) {
    const serializedPath = path2 ? serializePath(path2) : void 0;
    focused = serializedPath ? selectionState.focusedChildPath === serializedPath : !1, t1 = serializedPath ? selectionState.selectedChildPaths.has(serializedPath) : !1, $[3] = path2, $[4] = selectionState, $[5] = focused, $[6] = t1;
  } else
    focused = $[5], t1 = $[6];
  const selected = t1;
  let annotationMarkDefs, children;
  if ($[7] !== block || $[8] !== editorActor || $[9] !== focused || $[10] !== legacySchema || $[11] !== path2 || $[12] !== props.children || $[13] !== props.leaf.marks || $[14] !== props.renderAnnotation || $[15] !== props.renderDecorator || $[16] !== selected) {
    const decoratorSchemaTypes = editorActor.getSnapshot().context.schema.decorators.map(_temp2$1), decorators = [...new Set((props.leaf.marks ?? []).filter((mark) => decoratorSchemaTypes.includes(mark)))];
    annotationMarkDefs = (props.leaf.marks ?? []).flatMap((mark_0) => {
      if (decoratorSchemaTypes.includes(mark_0))
        return [];
      const markDef_0 = block?.markDefs?.find((markDef) => markDef._key === mark_0);
      return markDef_0 ? [markDef_0] : [];
    }), children = props.children;
    for (const mark_1 of decorators) {
      const legacyDecoratorSchemaType = legacySchema.decorators.find((dec) => dec.value === mark_1);
      path2 && legacyDecoratorSchemaType && props.renderDecorator && (children = /* @__PURE__ */ jsx(RenderDecorator, { renderDecorator: props.renderDecorator, editorElementRef: spanRef, focused, path: path2, selected, schemaType: legacyDecoratorSchemaType, value: mark_1, type: legacyDecoratorSchemaType, children }));
    }
    for (const annotationMarkDef of annotationMarkDefs) {
      const legacyAnnotationSchemaType = legacySchema.annotations.find((t) => t.name === annotationMarkDef._type);
      legacyAnnotationSchemaType && (block && path2 && props.renderAnnotation ? children = /* @__PURE__ */ jsx("span", { ref: spanRef, children: /* @__PURE__ */ jsx(RenderAnnotation, { renderAnnotation: props.renderAnnotation, block, editorElementRef: spanRef, focused, path: path2, selected, schemaType: legacyAnnotationSchemaType, value: annotationMarkDef, type: legacyAnnotationSchemaType, children }) }) : children = /* @__PURE__ */ jsx("span", { ref: spanRef, children }));
    }
    $[7] = block, $[8] = editorActor, $[9] = focused, $[10] = legacySchema, $[11] = path2, $[12] = props.children, $[13] = props.leaf.marks, $[14] = props.renderAnnotation, $[15] = props.renderDecorator, $[16] = selected, $[17] = annotationMarkDefs, $[18] = children;
  } else
    annotationMarkDefs = $[17], children = $[18];
  if (block && path2 && props.renderChild) {
    let t22;
    if ($[19] !== block.children || $[20] !== props.leaf) {
      let t3;
      $[22] !== props.leaf ? (t3 = (_child) => _child._key === props.leaf._key, $[22] = props.leaf, $[23] = t3) : t3 = $[23], t22 = block.children.find(t3), $[19] = block.children, $[20] = props.leaf, $[21] = t22;
    } else
      t22 = $[21];
    const child = t22;
    if (child) {
      let t3;
      $[24] !== annotationMarkDefs || $[25] !== child || $[26] !== children || $[27] !== focused || $[28] !== legacySchema.span || $[29] !== path2 || $[30] !== props.renderChild || $[31] !== selected ? (t3 = /* @__PURE__ */ jsx(RenderChild, { renderChild: props.renderChild, annotations: annotationMarkDefs, editorElementRef: spanRef, focused, path: path2, schemaType: legacySchema.span, selected, value: child, type: legacySchema.span, children }), $[24] = annotationMarkDefs, $[25] = child, $[26] = children, $[27] = focused, $[28] = legacySchema.span, $[29] = path2, $[30] = props.renderChild, $[31] = selected, $[32] = t3) : t3 = $[32], children = t3;
    }
  }
  let t2;
  return $[33] !== children || $[34] !== props.attributes ? (t2 = /* @__PURE__ */ jsx("span", { ...props.attributes, ref: spanRef, children }), $[33] = children, $[34] = props.attributes, $[35] = t2) : t2 = $[35], t2;
}
function _temp2$1(decorator) {
  return decorator.name;
}
function _temp$2(s) {
  return s.context.getLegacySchema();
}
function RenderAnnotation({
  renderAnnotation,
  block,
  children,
  editorElementRef,
  focused,
  path: path2,
  schemaType,
  selected,
  value,
  type
}) {
  return renderAnnotation({
    block,
    children,
    editorElementRef,
    focused,
    path: path2,
    schemaType,
    selected,
    value,
    type
  });
}
function RenderDecorator({
  renderDecorator,
  children,
  editorElementRef,
  focused,
  path: path2,
  schemaType,
  selected,
  value,
  type
}) {
  return renderDecorator({
    children,
    editorElementRef,
    focused,
    path: path2,
    schemaType,
    selected,
    value,
    type
  });
}
function RenderChild({
  renderChild,
  annotations,
  children,
  editorElementRef,
  focused,
  path: path2,
  schemaType,
  selected,
  value,
  type
}) {
  return renderChild({
    annotations,
    children,
    editorElementRef,
    focused,
    path: path2,
    schemaType,
    selected,
    value,
    type
  });
}
const PLACEHOLDER_STYLE = {
  position: "absolute",
  userSelect: "none",
  pointerEvents: "none",
  left: 0,
  right: 0
};
function RenderLeaf(props) {
  const $ = c(12), editorActor = useContext(EditorActorContext), schema = useSelector(editorActor, _temp$1);
  if (props.leaf._type !== schema.span.name)
    return props.children;
  let t0;
  $[0] !== props ? (t0 = /* @__PURE__ */ jsx(RenderSpan, { ...props }), $[0] = props, $[1] = t0) : t0 = $[1];
  let renderedSpan = t0;
  if (props.renderPlaceholder && props.leaf.placeholder && props.text.text === "") {
    let t1;
    $[2] !== props.renderPlaceholder ? (t1 = props.renderPlaceholder(), $[2] = props.renderPlaceholder, $[3] = t1) : t1 = $[3];
    let t2;
    $[4] !== t1 ? (t2 = /* @__PURE__ */ jsx("span", { style: PLACEHOLDER_STYLE, contentEditable: !1, children: t1 }), $[4] = t1, $[5] = t2) : t2 = $[5];
    let t3;
    return $[6] !== renderedSpan || $[7] !== t2 ? (t3 = /* @__PURE__ */ jsxs(Fragment$1, { children: [
      t2,
      renderedSpan
    ] }), $[6] = renderedSpan, $[7] = t2, $[8] = t3) : t3 = $[8], t3;
  }
  const rangeDecoration = props.leaf.rangeDecoration;
  if (rangeDecoration) {
    let t1;
    $[9] !== rangeDecoration || $[10] !== renderedSpan ? (t1 = rangeDecoration.component({
      children: renderedSpan
    }), $[9] = rangeDecoration, $[10] = renderedSpan, $[11] = t1) : t1 = $[11], renderedSpan = t1;
  }
  return renderedSpan;
}
function _temp$1(s) {
  return s.context.schema;
}
function RenderText(props) {
  const $ = c(5);
  let t0;
  return $[0] !== props.attributes || $[1] !== props.children || $[2] !== props.text._key || $[3] !== props.text._type ? (t0 = /* @__PURE__ */ jsx("span", { ...props.attributes, "data-child-key": props.text._key, "data-child-name": props.text._type, "data-child-type": "span", children: props.children }), $[0] = props.attributes, $[1] = props.children, $[2] = props.text._key, $[3] = props.text._type, $[4] = t0) : t0 = $[4], t0;
}
function createEditorPriority(config) {
  return {
    id: defaultKeyGenerator(),
    name: config?.name,
    reference: config?.reference
  };
}
const corePriority = createEditorPriority({
  name: "core"
});
function getDragSelection({
  eventSelection,
  snapshot
}) {
  let dragSelection = eventSelection;
  if (getFocusInlineObject({
    ...snapshot,
    context: {
      ...snapshot.context,
      selection: eventSelection
    }
  }))
    return dragSelection;
  const draggingCollapsedSelection = isSelectionCollapsed$1({
    context: {
      ...snapshot.context,
      selection: eventSelection
    }
  }), draggedTextBlock = getFocusTextBlock({
    ...snapshot,
    context: {
      ...snapshot.context,
      selection: eventSelection
    }
  }), draggedSpan = getFocusSpan$1({
    ...snapshot,
    context: {
      ...snapshot.context,
      selection: eventSelection
    }
  });
  draggingCollapsedSelection && draggedTextBlock && draggedSpan && (dragSelection = {
    anchor: getBlockStartPoint({
      context: snapshot.context,
      block: draggedTextBlock
    }),
    focus: getBlockEndPoint({
      context: snapshot.context,
      block: draggedTextBlock
    })
  });
  const selectedBlocks = getSelectedBlocks(snapshot);
  if (snapshot.context.selection && isSelectionExpanded(snapshot) && selectedBlocks.length > 1) {
    const selectionStartBlock = getSelectionStartBlock(snapshot), selectionEndBlock = getSelectionEndBlock(snapshot);
    if (!selectionStartBlock || !selectionEndBlock)
      return dragSelection;
    const selectionStartPoint = getBlockStartPoint({
      context: snapshot.context,
      block: selectionStartBlock
    }), selectionEndPoint = getBlockEndPoint({
      context: snapshot.context,
      block: selectionEndBlock
    });
    isOverlappingSelection(eventSelection)({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: {
          anchor: selectionStartPoint,
          focus: selectionEndPoint
        }
      }
    }) && (dragSelection = {
      anchor: selectionStartPoint,
      focus: selectionEndPoint
    });
  }
  return dragSelection;
}
function createDropPositionBehaviorsConfig({
  setDropPosition
}) {
  return [{
    behavior: defineBehavior({
      on: "drag.dragover",
      guard: ({
        snapshot,
        event
      }) => {
        const dropFocusBlock = getFocusBlock$1({
          ...snapshot,
          context: {
            ...snapshot.context,
            selection: event.position.selection
          }
        });
        if (!dropFocusBlock)
          return !1;
        const dragOrigin = event.dragOrigin;
        if (!dragOrigin)
          return !1;
        const dragSelection = getDragSelection({
          eventSelection: dragOrigin.selection,
          snapshot
        });
        return getSelectedBlocks({
          ...snapshot,
          context: {
            ...snapshot.context,
            selection: dragSelection
          }
        }).some((draggedBlock) => draggedBlock.node._key === dropFocusBlock.node._key) || !isSelectingEntireBlocks({
          ...snapshot,
          context: {
            ...snapshot.context,
            selection: dragSelection
          }
        }) ? !1 : {
          dropFocusBlock
        };
      },
      actions: [({
        event
      }, {
        dropFocusBlock
      }) => [{
        type: "effect",
        effect: () => {
          setDropPosition({
            blockKey: dropFocusBlock.node._key,
            positionBlock: event.position.block
          });
        }
      }]]
    }),
    priority: createEditorPriority({
      reference: {
        priority: corePriority,
        importance: "lower"
      }
    })
  }, {
    behavior: defineBehavior({
      on: "drag.*",
      guard: ({
        event
      }) => event.type !== "drag.dragover",
      actions: [({
        event
      }) => [{
        type: "effect",
        effect: () => {
          setDropPosition(void 0);
        }
      }, forward(event)]]
    }),
    priority: createEditorPriority({
      reference: {
        priority: corePriority,
        importance: "lower"
      }
    })
  }];
}
function useDropPosition() {
  const $ = c(3), editorActor = useContext(EditorActorContext), [dropPosition, setDropPosition] = useState();
  let t0, t1;
  return $[0] !== editorActor ? (t0 = () => {
    const behaviorConfigs = createDropPositionBehaviorsConfig({
      setDropPosition
    });
    for (const behaviorConfig of behaviorConfigs)
      editorActor.send({
        type: "add behavior",
        behaviorConfig
      });
    return () => {
      for (const behaviorConfig_0 of behaviorConfigs)
        editorActor.send({
          type: "remove behavior",
          behaviorConfig: behaviorConfig_0
        });
    };
  }, t1 = [editorActor, setDropPosition], $[0] = editorActor, $[1] = t0, $[2] = t1) : (t0 = $[1], t1 = $[2]), useEffect(t0, t1), dropPosition;
}
const PortableTextEditorContext = createContext(null), usePortableTextEditor = () => {
  const editor = useContext(PortableTextEditorContext);
  if (!editor)
    throw new Error("The `usePortableTextEditor` hook must be used inside the <PortableTextEditor> component's context.");
  return editor;
}, validateSelectionSetup = setup({
  types: {
    context: {},
    input: {},
    events: {}
  },
  guards: {
    "pending operations": ({
      context
    }) => context.slateEditor.operations.length > 0
  }
}), validateSelectionAction = validateSelectionSetup.createAction(({
  context,
  event
}) => {
  validateSelection(context.slateEditor, event.editorElement);
}), validateSelectionMachine = validateSelectionSetup.createMachine({
  id: "validate selection",
  context: ({
    input
  }) => ({
    slateEditor: input.slateEditor
  }),
  initial: "idle",
  states: {
    idle: {
      on: {
        "validate selection": [{
          guard: "pending operations",
          target: "waiting"
        }, {
          actions: [validateSelectionAction],
          target: "idle"
        }]
      }
    },
    waiting: {
      after: {
        0: [{
          guard: "pending operations",
          target: ".",
          reenter: !0
        }, {
          target: "idle",
          actions: [validateSelectionAction]
        }]
      },
      on: {
        "validate selection": {
          target: ".",
          reenter: !0
        }
      }
    }
  }
});
function validateSelection(slateEditor, editorElement) {
  if (!slateEditor.selection)
    return;
  let root;
  try {
    root = ReactEditor.findDocumentOrShadowRoot(slateEditor);
  } catch {
  }
  if (!root || editorElement !== root.activeElement)
    return;
  const domSelection = ReactEditor.getWindow(slateEditor).getSelection();
  if (!domSelection || domSelection.rangeCount === 0)
    return;
  const existingDOMRange = domSelection.getRangeAt(0);
  try {
    const newDOMRange = ReactEditor.toDOMRange(slateEditor, slateEditor.selection);
    (newDOMRange.startOffset !== existingDOMRange.startOffset || newDOMRange.endOffset !== existingDOMRange.endOffset) && (debug$1.selection("DOM range out of sync, validating selection"), domSelection?.removeAllRanges(), domSelection.addRange(newDOMRange));
  } catch {
    debug$1.selection("Could not resolve selection, selecting top document"), Transforms.deselect(slateEditor), slateEditor.children.length > 0 && Transforms.select(slateEditor, Editor.start(slateEditor, [])), slateEditor.onChange();
  }
}
const PortableTextEditable = forwardRef(function(props, forwardedRef) {
  const $ = c(179);
  let hotkeys, onBeforeInput, onBlur, onClick, onCopy, onCut, onDrag, onDragEnd, onDragEnter, onDragLeave, onDragOver, onDragStart, onDrop, onFocus, onPaste, propsSelection, rangeDecorations, renderAnnotation, renderBlock, renderChild, renderDecorator, renderListItem, renderPlaceholder, renderStyle, restProps, scrollSelectionIntoView, spellCheck;
  $[0] !== props ? ({
    hotkeys,
    onBlur,
    onFocus,
    onBeforeInput,
    onPaste,
    onCopy,
    onCut,
    onClick,
    onDragStart,
    onDrag,
    onDragEnd,
    onDragEnter,
    onDragOver,
    onDrop,
    onDragLeave,
    rangeDecorations,
    renderAnnotation,
    renderBlock,
    renderChild,
    renderDecorator,
    renderListItem,
    renderPlaceholder,
    renderStyle,
    selection: propsSelection,
    scrollSelectionIntoView,
    spellCheck,
    ...restProps
  } = props, $[0] = props, $[1] = hotkeys, $[2] = onBeforeInput, $[3] = onBlur, $[4] = onClick, $[5] = onCopy, $[6] = onCut, $[7] = onDrag, $[8] = onDragEnd, $[9] = onDragEnter, $[10] = onDragLeave, $[11] = onDragOver, $[12] = onDragStart, $[13] = onDrop, $[14] = onFocus, $[15] = onPaste, $[16] = propsSelection, $[17] = rangeDecorations, $[18] = renderAnnotation, $[19] = renderBlock, $[20] = renderChild, $[21] = renderDecorator, $[22] = renderListItem, $[23] = renderPlaceholder, $[24] = renderStyle, $[25] = restProps, $[26] = scrollSelectionIntoView, $[27] = spellCheck) : (hotkeys = $[1], onBeforeInput = $[2], onBlur = $[3], onClick = $[4], onCopy = $[5], onCut = $[6], onDrag = $[7], onDragEnd = $[8], onDragEnter = $[9], onDragLeave = $[10], onDragOver = $[11], onDragStart = $[12], onDrop = $[13], onFocus = $[14], onPaste = $[15], propsSelection = $[16], rangeDecorations = $[17], renderAnnotation = $[18], renderBlock = $[19], renderChild = $[20], renderDecorator = $[21], renderListItem = $[22], renderPlaceholder = $[23], renderStyle = $[24], restProps = $[25], scrollSelectionIntoView = $[26], spellCheck = $[27]);
  const portableTextEditor = usePortableTextEditor(), [hasInvalidValue, setHasInvalidValue] = useState(!1), editorActor = useContext(EditorActorContext), relayActor = useContext(RelayActorContext), readOnly = useSelector(editorActor, _temp), slateEditor = useSlate();
  let t0;
  $[28] !== slateEditor ? (t0 = {
    input: {
      slateEditor
    }
  }, $[28] = slateEditor, $[29] = t0) : t0 = $[29];
  const validateSelectionActor = useActorRef(validateSelectionMachine, t0);
  let t1;
  $[30] !== rangeDecorations ? (t1 = rangeDecorations ?? [], $[30] = rangeDecorations, $[31] = t1) : t1 = $[31];
  let t2;
  $[32] !== editorActor ? (t2 = editorActor.getSnapshot(), $[32] = editorActor, $[33] = t2) : t2 = $[33];
  const t3 = t2.context.schema;
  let t4;
  $[34] !== editorActor ? (t4 = editorActor.getSnapshot().matches({
    setup: "setting up"
  }), $[34] = editorActor, $[35] = t4) : t4 = $[35];
  const t5 = !t4;
  let t6;
  $[36] !== readOnly || $[37] !== slateEditor || $[38] !== t1 || $[39] !== t2.context.schema || $[40] !== t5 ? (t6 = {
    input: {
      rangeDecorations: t1,
      readOnly,
      schema: t3,
      slateEditor,
      skipSetup: t5
    }
  }, $[36] = readOnly, $[37] = slateEditor, $[38] = t1, $[39] = t2.context.schema, $[40] = t5, $[41] = t6) : t6 = $[41];
  const rangeDecorationsActor = useActorRef(rangeDecorationsMachine, t6), decorate = useSelector(rangeDecorationsActor, _temp2), dropPosition = useDropPosition();
  let t7, t8;
  $[42] !== rangeDecorationsActor || $[43] !== readOnly ? (t7 = () => {
    rangeDecorationsActor.send({
      type: "update read only",
      readOnly
    });
  }, t8 = [rangeDecorationsActor, readOnly], $[42] = rangeDecorationsActor, $[43] = readOnly, $[44] = t7, $[45] = t8) : (t7 = $[44], t8 = $[45]), useEffect(t7, t8);
  let t10, t9;
  $[46] !== rangeDecorations || $[47] !== rangeDecorationsActor ? (t9 = () => {
    rangeDecorationsActor.send({
      type: "range decorations updated",
      rangeDecorations: rangeDecorations ?? []
    });
  }, t10 = [rangeDecorationsActor, rangeDecorations], $[46] = rangeDecorations, $[47] = rangeDecorationsActor, $[48] = t10, $[49] = t9) : (t10 = $[48], t9 = $[49]), useEffect(t9, t10);
  let t11;
  $[50] !== dropPosition || $[51] !== readOnly || $[52] !== renderBlock || $[53] !== renderChild || $[54] !== renderListItem || $[55] !== renderStyle || $[56] !== spellCheck ? (t11 = (eProps) => /* @__PURE__ */ jsx(RenderElement, { ...eProps, dropPosition, readOnly, renderBlock, renderChild, renderListItem, renderStyle, spellCheck }), $[50] = dropPosition, $[51] = readOnly, $[52] = renderBlock, $[53] = renderChild, $[54] = renderListItem, $[55] = renderStyle, $[56] = spellCheck, $[57] = t11) : t11 = $[57];
  const renderElement = t11;
  let t12;
  $[58] !== readOnly || $[59] !== renderAnnotation || $[60] !== renderChild || $[61] !== renderDecorator || $[62] !== renderPlaceholder ? (t12 = (leafProps) => /* @__PURE__ */ jsx(RenderLeaf, { ...leafProps, readOnly, renderAnnotation, renderChild, renderDecorator, renderPlaceholder }), $[58] = readOnly, $[59] = renderAnnotation, $[60] = renderChild, $[61] = renderDecorator, $[62] = renderPlaceholder, $[63] = t12) : t12 = $[63];
  const renderLeaf = t12, renderText = _temp3;
  let t13;
  $[64] !== editorActor || $[65] !== propsSelection || $[66] !== slateEditor ? (t13 = () => {
    if (propsSelection) {
      debug$1.selection(`Selection from props ${JSON.stringify(propsSelection)}`);
      const normalizedSelection = normalizeSelection(propsSelection, slateEditor.value);
      if (normalizedSelection !== null) {
        debug$1.selection(`Normalized selection from props ${JSON.stringify(normalizedSelection)}`);
        const slateRange = toSlateRange({
          context: {
            schema: editorActor.getSnapshot().context.schema,
            value: slateEditor.value,
            selection: normalizedSelection
          },
          blockIndexMap: slateEditor.blockIndexMap
        });
        slateRange && (Transforms.select(slateEditor, slateRange), slateEditor.operations.some(_temp4) || editorActor.send({
          type: "update selection",
          selection: normalizedSelection
        }), slateEditor.onChange());
      }
    }
  }, $[64] = editorActor, $[65] = propsSelection, $[66] = slateEditor, $[67] = t13) : t13 = $[67];
  const restoreSelectionFromProps = t13;
  let t14, t15;
  $[68] !== editorActor || $[69] !== rangeDecorationsActor || $[70] !== restoreSelectionFromProps ? (t14 = () => {
    const onReady = editorActor.on("ready", () => {
      rangeDecorationsActor.send({
        type: "ready"
      }), restoreSelectionFromProps();
    }), onInvalidValue = editorActor.on("invalid value", () => {
      setHasInvalidValue(!0);
    }), onValueChanged = editorActor.on("value changed", () => {
      setHasInvalidValue(!1);
    });
    return () => {
      onReady.unsubscribe(), onInvalidValue.unsubscribe(), onValueChanged.unsubscribe();
    };
  }, t15 = [rangeDecorationsActor, editorActor, restoreSelectionFromProps], $[68] = editorActor, $[69] = rangeDecorationsActor, $[70] = restoreSelectionFromProps, $[71] = t14, $[72] = t15) : (t14 = $[71], t15 = $[72]), useEffect(t14, t15);
  let t16, t17;
  $[73] !== hasInvalidValue || $[74] !== propsSelection || $[75] !== restoreSelectionFromProps ? (t16 = () => {
    propsSelection && !hasInvalidValue && restoreSelectionFromProps();
  }, t17 = [hasInvalidValue, propsSelection, restoreSelectionFromProps], $[73] = hasInvalidValue, $[74] = propsSelection, $[75] = restoreSelectionFromProps, $[76] = t16, $[77] = t17) : (t16 = $[76], t17 = $[77]), useEffect(t16, t17);
  let t18;
  $[78] !== editorActor || $[79] !== onCopy || $[80] !== slateEditor ? (t18 = (event) => {
    if (onCopy)
      onCopy(event) !== void 0 && event.preventDefault();
    else if (event.nativeEvent.clipboardData) {
      event.stopPropagation(), event.preventDefault();
      const selection = slateEditor.selection ? slateRangeToSelection({
        schema: editorActor.getSnapshot().context.schema,
        editor: slateEditor,
        range: slateEditor.selection
      }) : void 0, position = selection ? {
        selection
      } : void 0;
      if (!position) {
        console.warn("Could not find position for copy event");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "clipboard.copy",
          originEvent: {
            dataTransfer: event.nativeEvent.clipboardData
          },
          position
        },
        editor: slateEditor,
        nativeEvent: event
      });
    }
  }, $[78] = editorActor, $[79] = onCopy, $[80] = slateEditor, $[81] = t18) : t18 = $[81];
  const handleCopy = t18;
  let t19;
  $[82] !== editorActor || $[83] !== onCut || $[84] !== slateEditor ? (t19 = (event_0) => {
    if (onCut)
      onCut(event_0) !== void 0 && event_0.preventDefault();
    else if (event_0.nativeEvent.clipboardData) {
      event_0.stopPropagation(), event_0.preventDefault();
      const selection_0 = editorActor.getSnapshot().context.selection, position_0 = selection_0 ? {
        selection: selection_0
      } : void 0;
      if (!position_0) {
        console.warn("Could not find position for cut event");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "clipboard.cut",
          originEvent: {
            dataTransfer: event_0.nativeEvent.clipboardData
          },
          position: position_0
        },
        editor: slateEditor,
        nativeEvent: event_0
      });
    }
  }, $[82] = editorActor, $[83] = onCut, $[84] = slateEditor, $[85] = t19) : t19 = $[85];
  const handleCut = t19;
  let t20;
  $[86] !== editorActor || $[87] !== onPaste || $[88] !== portableTextEditor || $[89] !== relayActor || $[90] !== slateEditor ? (t20 = (event_1) => {
    const value = slateEditor.value, path2 = (slateEditor.selection ? slateRangeToSelection({
      schema: editorActor.getSnapshot().context.schema,
      editor: slateEditor,
      range: slateEditor.selection
    }) : null)?.focus.path || [], onPasteResult = onPaste?.({
      event: event_1,
      value,
      path: path2,
      schemaTypes: portableTextEditor.schemaTypes
    });
    if (onPasteResult || !slateEditor.selection)
      event_1.preventDefault(), relayActor.send({
        type: "loading"
      }), Promise.resolve(onPasteResult).then((result_1) => {
        if (debug$1.behaviors("Custom paste function from client resolved", result_1), !result_1 || !result_1.insert) {
          debug$1.behaviors("No result from custom paste handler, pasting normally");
          const selection_1 = editorActor.getSnapshot().context.selection, position_1 = selection_1 ? {
            selection: selection_1
          } : void 0;
          if (!position_1) {
            console.warn("Could not find position for paste event");
            return;
          }
          editorActor.send({
            type: "behavior event",
            behaviorEvent: {
              type: "clipboard.paste",
              originEvent: {
                dataTransfer: event_1.clipboardData
              },
              position: position_1
            },
            editor: slateEditor,
            nativeEvent: event_1
          });
        } else
          result_1.insert ? editorActor.send({
            type: "behavior event",
            behaviorEvent: {
              type: "insert.blocks",
              blocks: parseBlocks({
                context: {
                  keyGenerator: editorActor.getSnapshot().context.keyGenerator,
                  schema: editorActor.getSnapshot().context.schema
                },
                blocks: result_1.insert,
                options: {
                  normalize: !1,
                  removeUnusedMarkDefs: !0,
                  validateFields: !1
                }
              }),
              placement: "auto"
            },
            editor: slateEditor
          }) : console.warn("Your onPaste function returned something unexpected:", result_1);
      }).catch(_temp5).finally(() => {
        relayActor.send({
          type: "done loading"
        });
      });
    else if (event_1.nativeEvent.clipboardData) {
      event_1.preventDefault(), event_1.stopPropagation();
      const selection_2 = editorActor.getSnapshot().context.selection, position_2 = selection_2 ? {
        selection: selection_2
      } : void 0;
      if (!position_2) {
        console.warn("Could not find position for paste event");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "clipboard.paste",
          originEvent: {
            dataTransfer: event_1.nativeEvent.clipboardData
          },
          position: position_2
        },
        editor: slateEditor,
        nativeEvent: event_1
      });
    }
    debug$1.behaviors("No result from custom paste handler, pasting normally");
  }, $[86] = editorActor, $[87] = onPaste, $[88] = portableTextEditor, $[89] = relayActor, $[90] = slateEditor, $[91] = t20) : t20 = $[91];
  const handlePaste = t20;
  let t21;
  $[92] !== editorActor || $[93] !== onFocus || $[94] !== relayActor || $[95] !== slateEditor ? (t21 = (event_2) => {
    onFocus && onFocus(event_2), event_2.isDefaultPrevented() || (relayActor.send({
      type: "focused",
      event: event_2
    }), !slateEditor.selection && slateEditor.children.length === 1 && isEmptyTextBlock(editorActor.getSnapshot().context, slateEditor.value.at(0)) && (Transforms.select(slateEditor, Editor.start(slateEditor, [])), slateEditor.onChange()));
  }, $[92] = editorActor, $[93] = onFocus, $[94] = relayActor, $[95] = slateEditor, $[96] = t21) : t21 = $[96];
  const handleOnFocus = t21;
  let t22;
  $[97] !== editorActor || $[98] !== onClick || $[99] !== slateEditor ? (t22 = (event_3) => {
    if (onClick && onClick(event_3), event_3.isDefaultPrevented() || event_3.isPropagationStopped())
      return;
    const position_3 = getEventPosition({
      editorActor,
      slateEditor,
      event: event_3.nativeEvent
    });
    position_3 && editorActor.send({
      type: "behavior event",
      behaviorEvent: {
        type: "mouse.click",
        position: position_3
      },
      editor: slateEditor,
      nativeEvent: event_3
    });
  }, $[97] = editorActor, $[98] = onClick, $[99] = slateEditor, $[100] = t22) : t22 = $[100];
  const handleClick = t22;
  let t23;
  $[101] !== onBlur || $[102] !== relayActor ? (t23 = (event_4) => {
    onBlur && onBlur(event_4), event_4.isPropagationStopped() || relayActor.send({
      type: "blurred",
      event: event_4
    });
  }, $[101] = onBlur, $[102] = relayActor, $[103] = t23) : t23 = $[103];
  const handleOnBlur = t23;
  let t24;
  $[104] !== onBeforeInput ? (t24 = (event_5) => {
    onBeforeInput && onBeforeInput(event_5);
  }, $[104] = onBeforeInput, $[105] = t24) : t24 = $[105];
  const handleOnBeforeInput = t24;
  let t25;
  $[106] !== editorActor || $[107] !== hotkeys || $[108] !== portableTextEditor || $[109] !== props || $[110] !== slateEditor ? (t25 = (event_6) => {
    props.onKeyDown && props.onKeyDown(event_6), event_6.isDefaultPrevented() || performHotkey({
      editorActor,
      editor: slateEditor,
      portableTextEditor,
      hotkeys: hotkeys ?? {},
      event: event_6
    }), event_6.isDefaultPrevented() || editorActor.send({
      type: "behavior event",
      behaviorEvent: {
        type: "keyboard.keydown",
        originEvent: {
          key: event_6.key,
          code: event_6.code,
          altKey: event_6.altKey,
          ctrlKey: event_6.ctrlKey,
          metaKey: event_6.metaKey,
          shiftKey: event_6.shiftKey
        }
      },
      editor: slateEditor,
      nativeEvent: event_6
    });
  }, $[106] = editorActor, $[107] = hotkeys, $[108] = portableTextEditor, $[109] = props, $[110] = slateEditor, $[111] = t25) : t25 = $[111];
  const handleKeyDown = t25;
  let t26;
  $[112] !== editorActor || $[113] !== props || $[114] !== slateEditor ? (t26 = (event_7) => {
    props.onKeyUp && props.onKeyUp(event_7), event_7.isDefaultPrevented() || editorActor.send({
      type: "behavior event",
      behaviorEvent: {
        type: "keyboard.keyup",
        originEvent: {
          key: event_7.key,
          code: event_7.code,
          altKey: event_7.altKey,
          ctrlKey: event_7.ctrlKey,
          metaKey: event_7.metaKey,
          shiftKey: event_7.shiftKey
        }
      },
      editor: slateEditor,
      nativeEvent: event_7
    });
  }, $[112] = editorActor, $[113] = props, $[114] = slateEditor, $[115] = t26) : t26 = $[115];
  const handleKeyUp = t26;
  let t27;
  bb0: {
    if (scrollSelectionIntoView === void 0) {
      t27 = void 0;
      break bb0;
    }
    if (scrollSelectionIntoView === null) {
      t27 = noop;
      break bb0;
    }
    let t282;
    $[116] !== portableTextEditor || $[117] !== scrollSelectionIntoView ? (t282 = (_editor, domRange) => {
      scrollSelectionIntoView(portableTextEditor, domRange);
    }, $[116] = portableTextEditor, $[117] = scrollSelectionIntoView, $[118] = t282) : t282 = $[118], t27 = t282;
  }
  const scrollSelectionIntoViewToSlate = t27;
  let t28, t29;
  $[119] !== editorActor || $[120] !== slateEditor ? (t28 = () => {
    const window2 = ReactEditor.getWindow(slateEditor), onDragEnd_0 = () => {
      editorActor.send({
        type: "dragend"
      });
    }, onDrop_0 = () => {
      editorActor.send({
        type: "drop"
      });
    };
    return window2.document.addEventListener("dragend", onDragEnd_0), window2.document.addEventListener("drop", onDrop_0), () => {
      window2.document.removeEventListener("dragend", onDragEnd_0), window2.document.removeEventListener("drop", onDrop_0);
    };
  }, t29 = [slateEditor, editorActor], $[119] = editorActor, $[120] = slateEditor, $[121] = t28, $[122] = t29) : (t28 = $[121], t29 = $[122]), useEffect(t28, t29);
  let t30;
  $[123] !== editorActor || $[124] !== onDragStart || $[125] !== slateEditor ? (t30 = (event_8) => {
    if (onDragStart?.(event_8), event_8.isDefaultPrevented() || event_8.isPropagationStopped())
      return;
    const position_4 = getEventPosition({
      editorActor,
      slateEditor,
      event: event_8.nativeEvent
    });
    if (!position_4) {
      console.warn("Could not find position for dragstart event");
      return;
    }
    return editorActor.send({
      type: "dragstart",
      origin: position_4
    }), editorActor.send({
      type: "behavior event",
      behaviorEvent: {
        type: "drag.dragstart",
        originEvent: {
          clientX: event_8.clientX,
          clientY: event_8.clientY,
          dataTransfer: event_8.dataTransfer
        },
        position: position_4
      },
      editor: slateEditor
    }), !0;
  }, $[123] = editorActor, $[124] = onDragStart, $[125] = slateEditor, $[126] = t30) : t30 = $[126];
  const handleDragStart = t30;
  let t31;
  $[127] !== editorActor || $[128] !== onDrag || $[129] !== slateEditor ? (t31 = (event_9) => {
    if (onDrag?.(event_9), !(event_9.isDefaultPrevented() || event_9.isPropagationStopped() || !getEventPosition({
      editorActor,
      slateEditor,
      event: event_9.nativeEvent
    })))
      return editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "drag.drag",
          originEvent: {
            dataTransfer: event_9.dataTransfer
          }
        },
        editor: slateEditor
      }), !0;
  }, $[127] = editorActor, $[128] = onDrag, $[129] = slateEditor, $[130] = t31) : t31 = $[130];
  const handleDrag = t31;
  let t32;
  $[131] !== editorActor || $[132] !== onDragEnd || $[133] !== slateEditor ? (t32 = (event_10) => {
    if (onDragEnd?.(event_10), !(event_10.isDefaultPrevented() || event_10.isPropagationStopped()))
      return editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "drag.dragend",
          originEvent: {
            dataTransfer: event_10.dataTransfer
          }
        },
        editor: slateEditor
      }), !0;
  }, $[131] = editorActor, $[132] = onDragEnd, $[133] = slateEditor, $[134] = t32) : t32 = $[134];
  const handleDragEnd = t32;
  let t33;
  $[135] !== editorActor || $[136] !== onDragEnter || $[137] !== slateEditor ? (t33 = (event_11) => {
    if (onDragEnter?.(event_11), event_11.isDefaultPrevented() || event_11.isPropagationStopped())
      return;
    const position_6 = getEventPosition({
      editorActor,
      slateEditor,
      event: event_11.nativeEvent
    });
    if (position_6)
      return editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "drag.dragenter",
          originEvent: {
            dataTransfer: event_11.dataTransfer
          },
          position: position_6
        },
        editor: slateEditor
      }), !0;
  }, $[135] = editorActor, $[136] = onDragEnter, $[137] = slateEditor, $[138] = t33) : t33 = $[138];
  const handleDragEnter = t33;
  let t34;
  $[139] !== editorActor || $[140] !== onDragOver || $[141] !== slateEditor ? (t34 = (event_12) => {
    if (onDragOver?.(event_12), event_12.isDefaultPrevented() || event_12.isPropagationStopped())
      return;
    const position_7 = getEventPosition({
      editorActor,
      slateEditor,
      event: event_12.nativeEvent
    });
    if (position_7)
      return editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "drag.dragover",
          originEvent: {
            dataTransfer: event_12.dataTransfer
          },
          dragOrigin: editorActor.getSnapshot().context.internalDrag?.origin,
          position: position_7
        },
        editor: slateEditor,
        nativeEvent: event_12
      }), !0;
  }, $[139] = editorActor, $[140] = onDragOver, $[141] = slateEditor, $[142] = t34) : t34 = $[142];
  const handleDragOver = t34;
  let t35;
  $[143] !== editorActor || $[144] !== onDrop || $[145] !== slateEditor ? (t35 = (event_13) => {
    if (onDrop?.(event_13), event_13.isDefaultPrevented() || event_13.isPropagationStopped())
      return;
    const position_8 = getEventPosition({
      editorActor,
      slateEditor,
      event: event_13.nativeEvent
    });
    if (!position_8) {
      console.warn("Could not find position for drop event");
      return;
    }
    return editorActor.send({
      type: "behavior event",
      behaviorEvent: {
        type: "drag.drop",
        originEvent: {
          dataTransfer: event_13.dataTransfer
        },
        dragOrigin: editorActor.getSnapshot().context.internalDrag?.origin,
        position: position_8
      },
      editor: slateEditor,
      nativeEvent: event_13
    }), !0;
  }, $[143] = editorActor, $[144] = onDrop, $[145] = slateEditor, $[146] = t35) : t35 = $[146];
  const handleDrop = t35;
  let t36;
  $[147] !== editorActor || $[148] !== onDragLeave || $[149] !== slateEditor ? (t36 = (event_14) => {
    if (onDragLeave?.(event_14), !(event_14.isDefaultPrevented() || event_14.isPropagationStopped() || !getEventPosition({
      editorActor,
      slateEditor,
      event: event_14.nativeEvent
    })))
      return editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "drag.dragleave",
          originEvent: {
            dataTransfer: event_14.dataTransfer
          }
        },
        editor: slateEditor
      }), !0;
  }, $[147] = editorActor, $[148] = onDragLeave, $[149] = slateEditor, $[150] = t36) : t36 = $[150];
  const handleDragLeave = t36;
  let t37;
  $[151] !== forwardedRef || $[152] !== validateSelectionActor ? (t37 = (editorElement) => {
    if (typeof forwardedRef == "function" ? forwardedRef(editorElement) : forwardedRef && (forwardedRef.current = editorElement), editorElement) {
      const mutationObserver = new MutationObserver(() => {
        validateSelectionActor.send({
          type: "validate selection",
          editorElement
        });
      });
      return mutationObserver.observe(editorElement, {
        attributeOldValue: !1,
        attributes: !1,
        characterData: !1,
        childList: !0,
        subtree: !0
      }), () => {
        mutationObserver.disconnect();
      };
    }
  }, $[151] = forwardedRef, $[152] = validateSelectionActor, $[153] = t37) : t37 = $[153];
  const callbackRef = t37;
  if (!portableTextEditor)
    return null;
  let t38;
  return $[154] !== callbackRef || $[155] !== decorate || $[156] !== handleClick || $[157] !== handleCopy || $[158] !== handleCut || $[159] !== handleDrag || $[160] !== handleDragEnd || $[161] !== handleDragEnter || $[162] !== handleDragLeave || $[163] !== handleDragOver || $[164] !== handleDragStart || $[165] !== handleDrop || $[166] !== handleKeyDown || $[167] !== handleKeyUp || $[168] !== handleOnBeforeInput || $[169] !== handleOnBlur || $[170] !== handleOnFocus || $[171] !== handlePaste || $[172] !== hasInvalidValue || $[173] !== readOnly || $[174] !== renderElement || $[175] !== renderLeaf || $[176] !== restProps || $[177] !== scrollSelectionIntoViewToSlate ? (t38 = hasInvalidValue ? null : /* @__PURE__ */ jsx(SelectionStateProvider, { children: /* @__PURE__ */ jsx(Editable, { ...restProps, ref: callbackRef, "data-read-only": readOnly, autoFocus: !1, className: restProps.className || "pt-editable", decorate, onBlur: handleOnBlur, onCopy: handleCopy, onCut: handleCut, onClick: handleClick, onDOMBeforeInput: handleOnBeforeInput, onDragStart: handleDragStart, onDrag: handleDrag, onDragEnd: handleDragEnd, onDragEnter: handleDragEnter, onDragOver: handleDragOver, onDrop: handleDrop, onDragLeave: handleDragLeave, onFocus: handleOnFocus, onKeyDown: handleKeyDown, onKeyUp: handleKeyUp, onPaste: handlePaste, readOnly, renderPlaceholder: void 0, renderElement, renderLeaf, renderText, scrollSelectionIntoView: scrollSelectionIntoViewToSlate }) }), $[154] = callbackRef, $[155] = decorate, $[156] = handleClick, $[157] = handleCopy, $[158] = handleCut, $[159] = handleDrag, $[160] = handleDragEnd, $[161] = handleDragEnter, $[162] = handleDragLeave, $[163] = handleDragOver, $[164] = handleDragStart, $[165] = handleDrop, $[166] = handleKeyDown, $[167] = handleKeyUp, $[168] = handleOnBeforeInput, $[169] = handleOnBlur, $[170] = handleOnFocus, $[171] = handlePaste, $[172] = hasInvalidValue, $[173] = readOnly, $[174] = renderElement, $[175] = renderLeaf, $[176] = restProps, $[177] = scrollSelectionIntoViewToSlate, $[178] = t38) : t38 = $[178], t38;
});
PortableTextEditable.displayName = "ForwardRef(PortableTextEditable)";
function noop() {
}
function _temp(s) {
  return s.matches({
    "edit mode": "read only"
  });
}
function _temp2(s_0) {
  return s_0.context.decorate?.fn;
}
function _temp3(props_0) {
  return /* @__PURE__ */ jsx(RenderText, { ...props_0 });
}
function _temp4(o) {
  return o.type === "set_selection";
}
function _temp5(error) {
  return console.warn(error), error;
}
const forEachActor = (actorRef, callback) => {
  callback(actorRef);
  const children = actorRef.getSnapshot().children;
  children && Object.values(children).forEach((child) => {
    forEachActor(child, callback);
  });
};
function stopActor(actorRef) {
  const persistedSnapshots = [];
  forEachActor(actorRef, (ref) => {
    persistedSnapshots.push([ref, ref.getSnapshot()]), ref.observers = /* @__PURE__ */ new Set();
  });
  const systemSnapshot = actorRef.system.getSnapshot?.();
  actorRef.stop(), actorRef.system._snapshot = systemSnapshot, persistedSnapshots.forEach(([ref, snapshot]) => {
    ref._processingStatus = 0, ref._snapshot = snapshot;
  });
}
const converterJson = {
  mimeType: "application/json",
  serialize: ({
    snapshot,
    event
  }) => {
    const portableTextConverter = snapshot.context.converters.find((converter) => converter.mimeType === "application/x-portable-text");
    return portableTextConverter ? {
      ...portableTextConverter.serialize({
        snapshot,
        event
      }),
      mimeType: "application/json",
      originEvent: event.originEvent
    } : {
      type: "serialization.failure",
      mimeType: "application/json",
      originEvent: event.originEvent,
      reason: "No application/x-portable-text Converter found"
    };
  },
  deserialize: ({
    snapshot,
    event
  }) => {
    const portableTextConverter = snapshot.context.converters.find((converter) => converter.mimeType === "application/x-portable-text");
    return portableTextConverter ? {
      ...portableTextConverter.deserialize({
        snapshot,
        event
      }),
      mimeType: "application/json"
    } : {
      type: "deserialization.failure",
      mimeType: "application/json",
      reason: "No application/x-portable-text Converter found"
    };
  }
}, converterPortableText = {
  mimeType: "application/x-portable-text",
  serialize: ({
    snapshot,
    event
  }) => {
    if (!snapshot.context.selection)
      return {
        type: "serialization.failure",
        mimeType: "application/x-portable-text",
        originEvent: event.originEvent,
        reason: "No selection"
      };
    const blocks = getSelectedValue(snapshot);
    return blocks.length === 0 ? {
      type: "serialization.failure",
      mimeType: "application/x-portable-text",
      reason: "No blocks serialized",
      originEvent: event.originEvent
    } : {
      type: "serialization.success",
      data: JSON.stringify(blocks),
      mimeType: "application/x-portable-text",
      originEvent: event.originEvent
    };
  },
  deserialize: ({
    snapshot,
    event
  }) => {
    const blocks = JSON.parse(event.data);
    if (!Array.isArray(blocks))
      return {
        type: "deserialization.failure",
        mimeType: "application/x-portable-text",
        reason: "Data is not an array"
      };
    const parsedBlocks = blocks.flatMap((block) => {
      const parsedBlock = parseBlock({
        context: snapshot.context,
        block,
        options: {
          normalize: !1,
          removeUnusedMarkDefs: !0,
          validateFields: !1
        }
      });
      return parsedBlock ? [parsedBlock] : [];
    });
    return parsedBlocks.length === 0 && blocks.length > 0 ? {
      type: "deserialization.failure",
      mimeType: "application/x-portable-text",
      reason: "No blocks were parsed"
    } : {
      type: "deserialization.success",
      data: parsedBlocks,
      mimeType: "application/x-portable-text"
    };
  }
};
function createConverterTextHtml(legacySchema) {
  return {
    mimeType: "text/html",
    serialize: ({
      snapshot,
      event
    }) => {
      if (!snapshot.context.selection)
        return {
          type: "serialization.failure",
          mimeType: "text/html",
          originEvent: event.originEvent,
          reason: "No selection"
        };
      const blocks = getSelectedValue(snapshot), html = toHTML(blocks, {
        onMissingComponent: !1,
        components: {
          unknownType: ({
            children
          }) => children !== void 0 ? `${children}` : ""
        }
      });
      return html === "" ? {
        type: "serialization.failure",
        mimeType: "text/html",
        originEvent: event.originEvent,
        reason: "Serialized HTML is empty"
      } : {
        type: "serialization.success",
        data: html,
        mimeType: "text/html",
        originEvent: event.originEvent
      };
    },
    deserialize: ({
      snapshot,
      event
    }) => {
      const parsedBlocks = htmlToBlocks(event.data, legacySchema.portableText, {
        keyGenerator: snapshot.context.keyGenerator,
        unstable_whitespaceOnPasteMode: legacySchema.block.options.unstable_whitespaceOnPasteMode
      }).flatMap((block) => {
        const parsedBlock = parseBlock({
          context: snapshot.context,
          block,
          options: {
            normalize: !1,
            removeUnusedMarkDefs: !0,
            validateFields: !1
          }
        });
        return parsedBlock ? [parsedBlock] : [];
      });
      return parsedBlocks.length === 0 ? {
        type: "deserialization.failure",
        mimeType: "text/html",
        reason: "No blocks deserialized"
      } : {
        type: "deserialization.success",
        data: parsedBlocks,
        mimeType: "text/html"
      };
    }
  };
}
const converterTextMarkdown = {
  mimeType: "text/markdown",
  serialize: ({
    snapshot,
    event
  }) => {
    if (!snapshot.context.selection)
      return {
        type: "serialization.failure",
        mimeType: "text/markdown",
        reason: "No selection",
        originEvent: event.originEvent
      };
    const blocks = getSelectedValue(snapshot);
    return {
      type: "serialization.success",
      data: portableTextToMarkdown(blocks),
      mimeType: "text/markdown",
      originEvent: event.originEvent
    };
  },
  deserialize: ({
    snapshot,
    event
  }) => {
    const parsedBlocks = markdownToPortableText(event.data, {
      keyGenerator: snapshot.context.keyGenerator,
      schema: snapshot.context.schema
    }).flatMap((block) => {
      const parsedBlock = parseBlock({
        context: snapshot.context,
        block,
        options: {
          normalize: !1,
          removeUnusedMarkDefs: !0,
          validateFields: !1
        }
      });
      return parsedBlock ? [parsedBlock] : [];
    });
    return parsedBlocks.length === 0 ? {
      type: "deserialization.failure",
      mimeType: "text/markdown",
      reason: "No blocks deserialized"
    } : {
      type: "deserialization.success",
      data: parsedBlocks,
      mimeType: "text/markdown"
    };
  }
};
function createConverterTextPlain(legacySchema) {
  return {
    mimeType: "text/plain",
    serialize: ({
      snapshot,
      event
    }) => snapshot.context.selection ? {
      type: "serialization.success",
      data: getSelectedValue(snapshot).map((block) => isTextBlock(snapshot.context, block) ? block.children.map((child) => child._type === snapshot.context.schema.span.name ? child.text : event.originEvent === "drag.dragstart" ? `[${snapshot.context.schema.inlineObjects.find((inlineObjectType) => inlineObjectType.name === child._type)?.title ?? "Object"}]` : "").join("") : event.originEvent === "drag.dragstart" ? `[${snapshot.context.schema.blockObjects.find((blockObjectType) => blockObjectType.name === block._type)?.title ?? "Object"}]` : "").filter((block) => block !== "").join(`

`),
      mimeType: "text/plain",
      originEvent: event.originEvent
    } : {
      type: "serialization.failure",
      mimeType: "text/plain",
      originEvent: event.originEvent,
      reason: "No selection"
    },
    deserialize: ({
      snapshot,
      event
    }) => {
      const textToHtml = `<html><body>${escapeHtml(event.data).split(/\n{2,}/).map((line) => line ? `<p>${line.replace(/(?:\r\n|\r|\n)/g, "<br/>")}</p>` : "<p></p>").join("")}</body></html>`, parsedBlocks = htmlToBlocks(textToHtml, legacySchema.portableText, {
        keyGenerator: snapshot.context.keyGenerator
      }).flatMap((block) => {
        const parsedBlock = parseBlock({
          context: snapshot.context,
          block,
          options: {
            normalize: !1,
            removeUnusedMarkDefs: !0,
            validateFields: !1
          }
        });
        return parsedBlock ? [parsedBlock] : [];
      });
      return parsedBlocks.length === 0 ? {
        type: "deserialization.failure",
        mimeType: "text/plain",
        reason: "No blocks deserialized"
      } : {
        type: "deserialization.success",
        data: parsedBlocks,
        mimeType: "text/plain"
      };
    }
  };
}
const entityMap = {
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;",
  "/": "&#x2F;",
  "`": "&#x60;",
  "=": "&#x3D;"
};
function escapeHtml(str) {
  return String(str).replace(/[&<>"'`=/]/g, (s) => entityMap[s] ?? s);
}
function createCoreConverters(legacySchema) {
  return [converterJson, converterPortableText, converterTextMarkdown, createConverterTextHtml(legacySchema), createConverterTextPlain(legacySchema)];
}
function compileType(rawType) {
  return Schema.compile({
    name: "blockTypeSchema",
    types: [rawType]
  }).get(rawType.name);
}
function createEditableAPI(editor, editorActor) {
  const types = editorActor.getSnapshot().context.schema;
  return {
    focus: () => {
      editorActor.send({
        type: "focus",
        editor
      });
    },
    blur: () => {
      editorActor.send({
        type: "blur",
        editor
      });
    },
    toggleMark: (mark) => {
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "decorator.toggle",
          decorator: mark
        },
        editor
      });
    },
    toggleList: (listItem) => {
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "list item.toggle",
          listItem
        },
        editor
      });
    },
    toggleBlockStyle: (style) => {
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "style.toggle",
          style
        },
        editor
      });
    },
    isMarkActive: (mark) => {
      const snapshot = getEditorSnapshot({
        editorActorSnapshot: editorActor.getSnapshot(),
        slateEditorInstance: editor
      });
      return getActiveDecorators(snapshot).includes(mark);
    },
    marks: () => {
      const snapshot = getEditorSnapshot({
        editorActorSnapshot: editorActor.getSnapshot(),
        slateEditorInstance: editor
      }), activeAnnotations = getActiveAnnotationsMarks(snapshot), activeDecorators = getActiveDecorators(snapshot);
      return [...activeAnnotations, ...activeDecorators];
    },
    undo: () => {
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "history.undo"
        },
        editor
      });
    },
    redo: () => {
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "history.redo"
        },
        editor
      });
    },
    select: (selection) => {
      const slateSelection = toSlateRange({
        context: {
          schema: editorActor.getSnapshot().context.schema,
          value: editor.value,
          selection
        },
        blockIndexMap: editor.blockIndexMap
      });
      slateSelection ? Transforms.select(editor, slateSelection) : Transforms.deselect(editor), editor.onChange();
    },
    focusBlock: () => {
      if (!editor.selection)
        return;
      const focusBlockIndex = editor.selection.focus.path.at(0);
      if (focusBlockIndex !== void 0)
        return editor.value.at(focusBlockIndex);
    },
    focusChild: () => {
      if (!editor.selection)
        return;
      const focusBlockIndex = editor.selection.focus.path.at(0), focusChildIndex = editor.selection.focus.path.at(1), block = focusBlockIndex !== void 0 ? editor.value.at(focusBlockIndex) : void 0;
      if (block && isTextBlock(editorActor.getSnapshot().context, block))
        return focusChildIndex === void 0 ? void 0 : block.children.at(focusChildIndex);
    },
    insertChild: (type, value) => (editorActor.send({
      type: "behavior event",
      behaviorEvent: {
        type: "insert.child",
        child: {
          _type: type.name,
          ...value || {}
        }
      },
      editor
    }), editor.selection ? slateRangeToSelection({
      schema: editorActor.getSnapshot().context.schema,
      editor,
      range: editor.selection
    })?.focus.path ?? [] : []),
    insertBlock: (type, value) => (editorActor.send({
      type: "behavior event",
      behaviorEvent: {
        type: "insert.block",
        block: {
          _type: type.name,
          ...value || {}
        },
        placement: "auto"
      },
      editor
    }), editor.selection ? slateRangeToSelection({
      schema: editorActor.getSnapshot().context.schema,
      editor,
      range: editor.selection
    })?.focus.path ?? [] : []),
    hasBlockStyle: (style) => {
      try {
        return isStyleActive({
          editor,
          style
        });
      } catch {
        return !1;
      }
    },
    hasListStyle: (listItem) => {
      try {
        return isListItemActive({
          editor,
          listItem
        });
      } catch {
        return !1;
      }
    },
    isVoid: (element) => ![types.block.name, types.span.name].includes(element._type),
    findByPath: (path2) => {
      const blockKey = getBlockKeyFromSelectionPoint({
        path: path2
      });
      if (!blockKey)
        return [void 0, void 0];
      const blockIndex = editor.blockIndexMap.get(blockKey);
      if (blockIndex === void 0)
        return [void 0, void 0];
      const block = editor.value.at(blockIndex);
      if (!block)
        return [void 0, void 0];
      const childKey = getChildKeyFromSelectionPoint({
        path: path2
      });
      if (path2.length === 1 && !childKey)
        return [block, [{
          _key: block._key
        }]];
      if (isTextBlock(editorActor.getSnapshot().context, block) && childKey) {
        const child = block.children.find((child2) => child2._key === childKey);
        if (child)
          return [child, [{
            _key: block._key
          }, "children", {
            _key: child._key
          }]];
      }
      return [void 0, void 0];
    },
    findDOMNode: (element) => {
      let node2;
      try {
        const [item] = Array.from(Editor.nodes(editor, {
          at: [],
          match: (n2) => n2._key === element._key
        }) || [])[0] || [void 0];
        item && (node2 = ReactEditor.toDOMNode(editor, item));
      } catch {
      }
      return node2;
    },
    activeAnnotations: () => {
      if (!editor.selection || editor.selection.focus.path.length < 2)
        return [];
      try {
        const activeAnnotations = [], spans = Editor.nodes(editor, {
          at: editor.selection,
          match: (node2) => Text$1.isText(node2) && node2.marks !== void 0 && Array.isArray(node2.marks) && node2.marks.length > 0
        });
        for (const [span, path2] of spans) {
          const [block] = Editor.node(editor, path2, {
            depth: 1
          });
          editor.isTextBlock(block) && block.markDefs?.forEach((def) => {
            Text$1.isText(span) && span.marks && Array.isArray(span.marks) && span.marks.includes(def._key) && activeAnnotations.push(def);
          });
        }
        return activeAnnotations;
      } catch {
        return [];
      }
    },
    isAnnotationActive: (annotationType) => {
      const snapshot = getEditorSnapshot({
        editorActorSnapshot: editorActor.getSnapshot(),
        slateEditorInstance: editor
      });
      return isActiveAnnotation(annotationType)(snapshot);
    },
    addAnnotation: (type, value) => {
      const snapshotBefore = getEditorSnapshot({
        editorActorSnapshot: editorActor.getSnapshot(),
        slateEditorInstance: editor
      }), selectedValueBefore = getSelectedValue(snapshotBefore), focusSpanBefore = getFocusSpan$1(snapshotBefore), markDefsBefore = selectedValueBefore.flatMap((block) => isTextBlock(snapshotBefore.context, block) ? block.markDefs ?? [] : []);
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "annotation.add",
          annotation: {
            name: type.name,
            value: value ?? {}
          }
        },
        editor
      });
      const snapshotAfter = getEditorSnapshot({
        editorActorSnapshot: editorActor.getSnapshot(),
        slateEditorInstance: editor
      }), selectedValueAfter = getSelectedValue(snapshotAfter), focusBlockAfter = getFocusBlock$1(snapshotAfter), focusSpanAfter = getFocusSpan$1(snapshotAfter), newMarkDefKeysOnFocusSpan = focusSpanAfter?.node.marks?.filter((mark) => !focusSpanBefore?.node.marks?.includes(mark) && !snapshotAfter.context.schema.decorators.map((decorator) => decorator.name).includes(mark)), markDefs = selectedValueAfter.flatMap((block) => isTextBlock(snapshotAfter.context, block) ? block.markDefs?.map((markDef2) => ({
        markDef: markDef2,
        path: [{
          _key: block._key
        }, "markDefs", {
          _key: markDef2._key
        }]
      })) ?? [] : []).filter((markDef2) => !markDefsBefore.some((markDefBefore) => markDefBefore._key === markDef2.markDef._key)), spanPath = focusSpanAfter?.path, markDef = markDefs.find((markDef2) => newMarkDefKeysOnFocusSpan?.some((mark) => mark === markDef2.markDef._key));
      if (focusBlockAfter && spanPath && markDef)
        return {
          markDefPath: markDef.path,
          markDefPaths: markDefs.map((markDef2) => markDef2.path),
          spanPath
        };
    },
    delete: (selection, options) => {
      selection && editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "delete",
          at: selection,
          unit: options?.mode === "blocks" ? "block" : options?.mode === "children" ? "child" : void 0
        },
        editor
      });
    },
    removeAnnotation: (type) => {
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "annotation.remove",
          annotation: {
            name: type.name
          }
        },
        editor
      });
    },
    getSelection: () => {
      if (!editor.selection)
        return null;
      if (editor.selection === editor.lastSlateSelection)
        return editor.lastSelection;
      const selection = slateRangeToSelection({
        schema: editorActor.getSnapshot().context.schema,
        editor,
        range: editor.selection
      });
      return editor.lastSlateSelection = editor.selection, editor.lastSelection = selection, selection;
    },
    getValue: () => editor.value,
    isCollapsedSelection: () => !!editor.selection && Range.isCollapsed(editor.selection),
    isExpandedSelection: () => !!editor.selection && Range.isExpanded(editor.selection),
    insertBreak: () => {
      editor.insertBreak(), editor.onChange();
    },
    getFragment: () => {
      const snapshot = getEditorSnapshot({
        editorActorSnapshot: editorActor.getSnapshot(),
        slateEditorInstance: editor
      });
      return getSelectedValue(snapshot);
    },
    isSelectionsOverlapping: (selectionA, selectionB) => {
      const rangeA = toSlateRange({
        context: {
          schema: editorActor.getSnapshot().context.schema,
          value: editor.value,
          selection: selectionA
        },
        blockIndexMap: editor.blockIndexMap
      }), rangeB = toSlateRange({
        context: {
          schema: editorActor.getSnapshot().context.schema,
          value: editor.value,
          selection: selectionB
        },
        blockIndexMap: editor.blockIndexMap
      });
      return Range.isRange(rangeA) && Range.isRange(rangeB) && Range.includes(rangeA, rangeB);
    }
  };
}
const levelIndexMaps = /* @__PURE__ */ new Map();
function buildIndexMaps(context, {
  blockIndexMap,
  listIndexMap
}) {
  blockIndexMap.clear(), listIndexMap.clear(), levelIndexMaps.clear();
  let previousListItem;
  for (let blockIndex = 0; blockIndex < context.value.length; blockIndex++) {
    const block = context.value.at(blockIndex);
    if (block === void 0)
      continue;
    if (blockIndexMap.set(block._key, blockIndex), !isTextBlock(context, block)) {
      levelIndexMaps.clear(), previousListItem = void 0;
      continue;
    }
    if (block.listItem === void 0 || block.level === void 0) {
      levelIndexMaps.clear(), previousListItem = void 0;
      continue;
    }
    if (!previousListItem) {
      const levelIndexMap2 = levelIndexMaps.get(block.listItem) ?? /* @__PURE__ */ new Map();
      levelIndexMap2.set(block.level, 1), levelIndexMaps.set(block.listItem, levelIndexMap2), listIndexMap.set(block._key, 1), previousListItem = {
        listItem: block.listItem,
        level: block.level
      };
      continue;
    }
    if (previousListItem.listItem === block.listItem && previousListItem.level < block.level) {
      const levelIndexMap2 = levelIndexMaps.get(block.listItem) ?? /* @__PURE__ */ new Map();
      levelIndexMap2.set(block.level, 1), levelIndexMaps.set(block.listItem, levelIndexMap2), listIndexMap.set(block._key, 1), previousListItem = {
        listItem: block.listItem,
        level: block.level
      };
      continue;
    }
    levelIndexMaps.forEach((levelIndexMap2, listItem) => {
      if (listItem === block.listItem)
        return;
      const levelsToDelete = [];
      levelIndexMap2.forEach((_, level) => {
        level >= block.level && levelsToDelete.push(level);
      }), levelsToDelete.forEach((level) => {
        levelIndexMap2.delete(level);
      });
    });
    const levelIndexMap = levelIndexMaps.get(block.listItem) ?? /* @__PURE__ */ new Map(), levelCounter = levelIndexMap.get(block.level) ?? 0;
    levelIndexMap.set(block.level, levelCounter + 1), levelIndexMaps.set(block.listItem, levelIndexMap), listIndexMap.set(block._key, levelCounter + 1), previousListItem = {
      listItem: block.listItem,
      level: block.level
    };
  }
}
function createPlaceholderBlock(context) {
  return {
    _type: context.schema.block.name,
    _key: context.keyGenerator(),
    style: context.schema.styles[0]?.name ?? "normal",
    markDefs: [],
    children: [{
      _type: context.schema.span.name,
      _key: context.keyGenerator(),
      text: "",
      marks: []
    }]
  };
}
function createBehaviorApiPlugin(editorActor) {
  return function(editor) {
    const {
      delete: editorDelete,
      insertNodes: insertNodes2,
      select: select2,
      setSelection: setSelection2
    } = editor;
    return editor.delete = (options) => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        editorDelete(options);
        return;
      }
      const range2 = options?.at ? Editor.range(editor, options.at) : void 0, selection = range2 ? slateRangeToSelection({
        schema: editorActor.getSnapshot().context.schema,
        editor,
        range: range2
      }) : void 0;
      selection ? editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "delete",
          at: selection,
          direction: options?.reverse ? "backward" : "forward",
          unit: options?.unit
        },
        editor
      }) : editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "delete",
          direction: options?.reverse ? "backward" : "forward",
          unit: options?.unit
        },
        editor
      });
    }, editor.deleteBackward = (unit) => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        console.error("Unexpected call to .deleteBackward(...)");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "delete.backward",
          unit
        },
        editor
      });
    }, editor.deleteForward = (unit) => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        console.error("Unexpected call to .deleteForward(...)");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "delete.forward",
          unit
        },
        editor
      });
    }, editor.insertBreak = () => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        console.error("Unexpected call to .insertBreak(...)");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "insert.break"
        },
        editor
      });
    }, editor.insertData = (dataTransfer) => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        console.error("Unexpected call to .insertData(...)");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "input.*",
          originEvent: {
            dataTransfer
          }
        },
        editor
      });
    }, editor.insertNodes = (nodes2, options) => {
      if (editor.isNormalizingNode) {
        const normalizedNodes = (Node$1.isNode(nodes2) ? [nodes2] : nodes2).map((node2) => Text$1.isText(node2) && typeof node2._type != "string" ? {
          ...node2,
          _type: editorActor.getSnapshot().context.schema.span.name
        } : node2);
        insertNodes2(normalizedNodes, options);
        return;
      }
      insertNodes2(nodes2, options);
    }, editor.insertSoftBreak = () => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        console.error("Unexpected call to .insertSoftBreak(...)");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "insert.soft break"
        },
        editor
      });
    }, editor.insertText = (text) => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        console.error("Unexpected call to .insertText(...)");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "insert.text",
          text
        },
        editor
      });
    }, editor.redo = () => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        console.error("Unexpected call to .redo(...)");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "history.redo"
        },
        editor
      });
    }, editor.select = (location) => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        select2(location);
        return;
      }
      if (editor.selection) {
        select2(location);
        return;
      }
      const range2 = Editor.range(editor, location);
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "select",
          at: slateRangeToSelection({
            schema: editorActor.getSnapshot().context.schema,
            editor,
            range: range2
          })
        },
        editor
      });
    }, editor.setSelection = (partialRange) => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        setSelection2(partialRange);
        return;
      }
      const anchor = partialRange.anchor ? slatePointToSelectionPoint({
        schema: editorActor.getSnapshot().context.schema,
        editor,
        point: partialRange.anchor
      }) : void 0, focus = partialRange.focus ? slatePointToSelectionPoint({
        schema: editorActor.getSnapshot().context.schema,
        editor,
        point: partialRange.focus
      }) : void 0, backward = editor.selection ? Range.isBackward({
        anchor: partialRange.anchor ?? editor.selection.anchor,
        focus: partialRange.focus ?? editor.selection.focus
      }) : partialRange.anchor && partialRange.focus ? Range.isBackward({
        anchor: partialRange.anchor,
        focus: partialRange.focus
      }) : void 0;
      if (editor.selection) {
        const newAnchor = partialRange.anchor ?? editor.selection.anchor, newFocus = partialRange.focus ?? editor.selection.focus;
        if (Point.equals(newAnchor, editor.selection.anchor) && Point.equals(newFocus, editor.selection.focus)) {
          setSelection2(partialRange);
          return;
        }
      }
      if (!anchor || !focus) {
        setSelection2(partialRange);
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "select",
          at: {
            anchor,
            focus,
            backward
          }
        },
        editor
      });
    }, editor.setFragmentData = () => {
      console.error("Unexpected call to .setFragmentData(...)");
    }, editor.undo = () => {
      if (editor.isNormalizingNode || editor.isPerformingBehaviorOperation) {
        console.error("Unexpected call to .undo(...)");
        return;
      }
      editorActor.send({
        type: "behavior event",
        behaviorEvent: {
          type: "history.undo"
        },
        editor
      });
    }, editor;
  };
}
function createUndoSteps({
  steps,
  op,
  editor,
  currentUndoStepId,
  previousUndoStepId
}) {
  const lastStep = steps.at(-1);
  if (!lastStep)
    return createNewStep(steps, op, editor);
  if (editor.operations.length > 0)
    return currentUndoStepId === previousUndoStepId || editor.isNormalizingNode ? mergeIntoLastStep(steps, lastStep, op) : createNewStep(steps, op, editor);
  if (op.type === "set_selection" && currentUndoStepId === void 0 && previousUndoStepId !== void 0 || op.type === "set_selection" && currentUndoStepId !== void 0 && previousUndoStepId !== void 0 && previousUndoStepId !== currentUndoStepId)
    return mergeIntoLastStep(steps, lastStep, op);
  if (currentUndoStepId === void 0 && previousUndoStepId === void 0) {
    if (op.type === "set_selection")
      return mergeIntoLastStep(steps, lastStep, op);
    const lastOp = lastStep.operations.at(-1);
    return lastOp && op.type === "insert_text" && lastOp.type === "insert_text" && op.offset === lastOp.offset + lastOp.text.length && Path.equals(op.path, lastOp.path) && op.text !== " " || lastOp && op.type === "remove_text" && lastOp.type === "remove_text" && op.offset + op.text.length === lastOp.offset && Path.equals(op.path, lastOp.path) ? mergeIntoLastStep(steps, lastStep, op) : createNewStep(steps, op, editor);
  }
  return createNewStep(steps, op, editor);
}
function createNewStep(steps, op, editor) {
  const operations = editor.selection === null ? [op] : [{
    type: "set_selection",
    properties: {
      ...editor.selection
    },
    newProperties: {
      ...editor.selection
    }
  }, op];
  return [...steps, {
    operations,
    timestamp: /* @__PURE__ */ new Date()
  }];
}
function mergeIntoLastStep(steps, lastStep, op) {
  return [...steps.slice(0, -1), {
    timestamp: lastStep.timestamp,
    operations: [...lastStep.operations, op]
  }];
}
const UNDO_STEP_LIMIT = 1e3;
function createHistoryPlugin({
  editorActor,
  subscriptions
}) {
  return function(editor) {
    let previousSnapshot = editor.value, previousUndoStepId = editor.undoStepId;
    subscriptions.push(() => {
      const subscription = editorActor.on("patches", ({
        patches,
        snapshot
      }) => {
        let reset = !1;
        for (const patch of patches)
          if (!reset && patch.origin !== "local") {
            if (patch.type === "unset" && patch.path.length === 0) {
              editor.history = {
                undos: [],
                redos: []
              }, editor.remotePatches.splice(0, editor.remotePatches.length), editor.withHistory = !0, reset = !0;
              return;
            }
            editor.remotePatches.push({
              patch,
              time: /* @__PURE__ */ new Date(),
              snapshot,
              previousSnapshot
            });
          }
        previousSnapshot = snapshot;
      });
      return () => {
        subscription.unsubscribe();
      };
    });
    const {
      apply: apply2
    } = editor;
    return editor.apply = (op) => {
      if (editorActor.getSnapshot().matches({
        "edit mode": "read only"
      })) {
        apply2(op);
        return;
      }
      if (editor.isProcessingRemoteChanges) {
        apply2(op);
        return;
      }
      if (editor.isUndoing || editor.isRedoing) {
        apply2(op);
        return;
      }
      const withHistory = editor.withHistory, currentUndoStepId = editor.undoStepId;
      if (!withHistory) {
        previousUndoStepId = currentUndoStepId, apply2(op);
        return;
      }
      for (op.type !== "set_selection" && (editor.history.redos = []), editor.history.undos = createUndoSteps({
        steps: editor.history.undos,
        op,
        editor,
        currentUndoStepId,
        previousUndoStepId
      }); editor.history.undos.length > UNDO_STEP_LIMIT; )
        editor.history.undos.shift();
      previousUndoStepId = currentUndoStepId, apply2(op);
    }, editor;
  };
}
function withNormalizeNode(editor, fn) {
  const prev = editor.isNormalizingNode;
  editor.isNormalizingNode = !0, fn(), editor.isNormalizingNode = prev;
}
function withoutPatching(editor, fn) {
  const prev = editor.isPatching;
  editor.isPatching = !1, fn(), editor.isPatching = prev;
}
function createNormalizationPlugin(editorActor) {
  return function(editor) {
    const {
      apply: apply2,
      normalizeNode: normalizeNode2
    } = editor, defaultStyle = editorActor.getSnapshot().context.schema.styles.at(0)?.name;
    return editor.normalizeNode = (nodeEntry) => {
      const [node2, path2] = nodeEntry;
      if (Editor.isEditor(node2) && node2.children.length === 0 && withoutPatching(editor, () => {
        withNormalizeNode(editor, () => {
          Transforms.insertNodes(editor, createPlaceholderBlock(editorActor.getSnapshot().context), {
            at: [0],
            select: !0
          });
        });
      }), editor.isTextBlock(node2)) {
        const children = Node$1.children(editor, path2);
        for (const [child, childPath] of children) {
          const nextNode = node2.children[childPath[1] + 1];
          if (editor.isTextSpan(child) && editor.isTextSpan(nextNode) && child.marks?.every((mark) => nextNode.marks?.includes(mark)) && nextNode.marks?.every((mark) => child.marks?.includes(mark))) {
            debug$1.normalization("merging spans with same marks"), withNormalizeNode(editor, () => {
              Transforms.mergeNodes(editor, {
                at: [childPath[0], childPath[1] + 1],
                voids: !0
              });
            });
            return;
          }
        }
      }
      if (editor.isTextBlock(node2) && !Array.isArray(node2.markDefs)) {
        debug$1.normalization("adding .markDefs to block node"), withNormalizeNode(editor, () => {
          Transforms.setNodes(editor, {
            markDefs: []
          }, {
            at: path2
          });
        });
        return;
      }
      if (defaultStyle && editor.isTextBlock(node2) && typeof node2.style > "u") {
        debug$1.normalization("adding .style to block node"), withNormalizeNode(editor, () => {
          Transforms.setNodes(editor, {
            style: defaultStyle
          }, {
            at: path2
          });
        });
        return;
      }
      if (editor.isTextSpan(node2) && !Array.isArray(node2.marks)) {
        debug$1.normalization("Adding .marks to span node"), withNormalizeNode(editor, () => {
          Transforms.setNodes(editor, {
            marks: []
          }, {
            at: path2
          });
        });
        return;
      }
      if (editor.isTextSpan(node2)) {
        const blockPath = Path.parent(path2), [block] = Editor.node(editor, blockPath), decorators = editorActor.getSnapshot().context.schema.decorators.map((decorator) => decorator.name), annotations = node2.marks?.filter((mark) => !decorators.includes(mark));
        if (editor.isTextBlock(block) && node2.text === "" && annotations && annotations.length > 0) {
          debug$1.normalization("removing annotations from empty span node"), withNormalizeNode(editor, () => {
            Transforms.setNodes(editor, {
              marks: node2.marks?.filter((mark) => decorators.includes(mark))
            }, {
              at: path2
            });
          });
          return;
        }
      }
      if (editor.isTextBlock(node2)) {
        const decorators = editorActor.getSnapshot().context.schema.decorators.map((decorator) => decorator.name);
        for (const [child, childPath] of Node$1.children(editor, path2))
          if (editor.isTextSpan(child)) {
            const marks2 = child.marks ?? [], orphanedAnnotations = marks2.filter((mark) => !decorators.includes(mark) && !node2.markDefs?.find((def) => def._key === mark));
            if (orphanedAnnotations.length > 0) {
              debug$1.normalization("removing orphaned annotations from span node"), withNormalizeNode(editor, () => {
                Transforms.setNodes(editor, {
                  marks: marks2.filter((mark) => !orphanedAnnotations.includes(mark))
                }, {
                  at: childPath
                });
              });
              return;
            }
          }
      }
      if (editor.isTextSpan(node2)) {
        const blockPath = Path.parent(path2), [block] = Editor.node(editor, blockPath);
        if (editor.isTextBlock(block)) {
          const decorators = editorActor.getSnapshot().context.schema.decorators.map((decorator) => decorator.name), marks2 = node2.marks ?? [], orphanedAnnotations = marks2.filter((mark) => !decorators.includes(mark) && !block.markDefs?.find((def) => def._key === mark));
          if (orphanedAnnotations.length > 0) {
            debug$1.normalization("removing orphaned annotations from span node"), withNormalizeNode(editor, () => {
              Transforms.setNodes(editor, {
                marks: marks2.filter((mark) => !orphanedAnnotations.includes(mark))
              }, {
                at: path2
              });
            });
            return;
          }
        }
      }
      if (editor.isTextBlock(node2)) {
        const markDefs = node2.markDefs ?? [], markDefKeys = /* @__PURE__ */ new Set(), newMarkDefs = [];
        for (const markDef of markDefs)
          markDefKeys.has(markDef._key) || (markDefKeys.add(markDef._key), newMarkDefs.push(markDef));
        if (markDefs.length !== newMarkDefs.length) {
          debug$1.normalization("removing duplicate markDefs"), withNormalizeNode(editor, () => {
            Transforms.setNodes(editor, {
              markDefs: newMarkDefs
            }, {
              at: path2
            });
          });
          return;
        }
      }
      if (editor.isTextBlock(node2) && !editor.operations.some((op) => op.type === "merge_node" && "markDefs" in op.properties && op.path.length === 1)) {
        const newMarkDefs = (node2.markDefs || []).filter((def) => node2.children.find((child) => Text$1.isText(child) && Array.isArray(child.marks) && child.marks.includes(def._key)));
        if (node2.markDefs && !isEqualMarkDefs(newMarkDefs, node2.markDefs)) {
          debug$1.normalization("removing markDef not in use"), withNormalizeNode(editor, () => {
            Transforms.setNodes(editor, {
              markDefs: newMarkDefs
            }, {
              at: path2
            });
          });
          return;
        }
      }
      withNormalizeNode(editor, () => {
        normalizeNode2(nodeEntry);
      });
    }, editor.apply = (op) => {
      if (editor.isProcessingRemoteChanges) {
        apply2(op);
        return;
      }
      if (editor.isUndoing || editor.isRedoing) {
        apply2(op);
        return;
      }
      if (op.type === "set_selection")
        if (op.properties && op.newProperties && op.properties.anchor && op.properties.focus && op.newProperties.anchor && op.newProperties.focus) {
          const previousSelectionIsCollapsed = Range.isCollapsed({
            anchor: op.properties.anchor,
            focus: op.properties.focus
          }), newSelectionIsCollapsed = Range.isCollapsed({
            anchor: op.newProperties.anchor,
            focus: op.newProperties.focus
          });
          if (previousSelectionIsCollapsed && newSelectionIsCollapsed) {
            const focusSpan = Array.from(Editor.nodes(editor, {
              mode: "lowest",
              at: op.properties.focus,
              match: (n2) => editor.isTextSpan(n2),
              voids: !1
            }))[0]?.[0], newFocusSpan = Array.from(Editor.nodes(editor, {
              mode: "lowest",
              at: op.newProperties.focus,
              match: (n2) => editor.isTextSpan(n2),
              voids: !1
            }))[0]?.[0], movedToNextSpan = focusSpan && newFocusSpan && op.newProperties.focus.path[0] === op.properties.focus.path[0] && op.newProperties.focus.path[1] === op.properties.focus.path[1] + 1 && focusSpan.text.length === op.properties.focus.offset && op.newProperties.focus.offset === 0, movedToPreviousSpan = focusSpan && newFocusSpan && op.newProperties.focus.path[0] === op.properties.focus.path[0] && op.newProperties.focus.path[1] === op.properties.focus.path[1] - 1 && op.properties.focus.offset === 0 && newFocusSpan.text.length === op.newProperties.focus.offset;
            !movedToNextSpan && !movedToPreviousSpan && (editor.decoratorState = {});
          }
        } else
          editor.decoratorState = {};
      if (op.type === "merge_node" && op.path.length === 1 && "markDefs" in op.properties && op.properties._type === editorActor.getSnapshot().context.schema.block.name && Array.isArray(op.properties.markDefs) && op.properties.markDefs.length > 0 && op.path[0] - 1 >= 0) {
        const [targetBlock, targetPath] = Editor.node(editor, [op.path[0] - 1]);
        if (editor.isTextBlock(targetBlock)) {
          const oldDefs = Array.isArray(targetBlock.markDefs) && targetBlock.markDefs || [], newMarkDefs = [...new Map([...oldDefs, ...op.properties.markDefs].map((def) => [def._key, def])).values()];
          debug$1.normalization("copying markDefs over to merged block", op), Transforms.setNodes(editor, {
            markDefs: newMarkDefs
          }, {
            at: targetPath,
            voids: !1
          }), apply2(op);
          return;
        }
      }
      apply2(op);
    }, editor;
  };
}
function cloneDiff(diff2) {
  const [type, patch] = diff2;
  return [type, patch];
}
function getCommonOverlap(textA, textB) {
  let text1 = textA, text2 = textB;
  const text1Length = text1.length, text2Length = text2.length;
  if (text1Length === 0 || text2Length === 0) return 0;
  text1Length > text2Length ? text1 = text1.substring(text1Length - text2Length) : text1Length < text2Length && (text2 = text2.substring(0, text1Length));
  const textLength = Math.min(text1Length, text2Length);
  if (text1 === text2) return textLength;
  let best = 0, length = 1;
  for (let found = 0; found !== -1; ) {
    const pattern = text1.substring(textLength - length);
    if (found = text2.indexOf(pattern), found === -1) return best;
    length += found, (found === 0 || text1.substring(textLength - length) === text2.substring(0, length)) && (best = length, length++);
  }
  return best;
}
function getCommonPrefix(text1, text2) {
  if (!text1 || !text2 || text1[0] !== text2[0]) return 0;
  let pointerMin = 0, pointerMax = Math.min(text1.length, text2.length), pointerMid = pointerMax, pointerStart = 0;
  for (; pointerMin < pointerMid; ) text1.substring(pointerStart, pointerMid) === text2.substring(pointerStart, pointerMid) ? (pointerMin = pointerMid, pointerStart = pointerMin) : pointerMax = pointerMid, pointerMid = Math.floor((pointerMax - pointerMin) / 2 + pointerMin);
  return pointerMid;
}
function getCommonSuffix(text1, text2) {
  if (!text1 || !text2 || text1[text1.length - 1] !== text2[text2.length - 1]) return 0;
  let pointerMin = 0, pointerMax = Math.min(text1.length, text2.length), pointerMid = pointerMax, pointerEnd = 0;
  for (; pointerMin < pointerMid; ) text1.substring(text1.length - pointerMid, text1.length - pointerEnd) === text2.substring(text2.length - pointerMid, text2.length - pointerEnd) ? (pointerMin = pointerMid, pointerEnd = pointerMin) : pointerMax = pointerMid, pointerMid = Math.floor((pointerMax - pointerMin) / 2 + pointerMin);
  return pointerMid;
}
function isHighSurrogate(char) {
  const charCode = char.charCodeAt(0);
  return charCode >= 55296 && charCode <= 56319;
}
function isLowSurrogate(char) {
  const charCode = char.charCodeAt(0);
  return charCode >= 56320 && charCode <= 57343;
}
function bisect(text1, text2, deadline) {
  const text1Length = text1.length, text2Length = text2.length, maxD = Math.ceil((text1Length + text2Length) / 2), vOffset = maxD, vLength = 2 * maxD, v1 = new Array(vLength), v2 = new Array(vLength);
  for (let x = 0; x < vLength; x++) v1[x] = -1, v2[x] = -1;
  v1[vOffset + 1] = 0, v2[vOffset + 1] = 0;
  const delta = text1Length - text2Length, front = delta % 2 !== 0;
  let k1start = 0, k1end = 0, k2start = 0, k2end = 0;
  for (let d = 0; d < maxD && !(Date.now() > deadline); d++) {
    for (let k1 = -d + k1start; k1 <= d - k1end; k1 += 2) {
      const k1Offset = vOffset + k1;
      let x1;
      k1 === -d || k1 !== d && v1[k1Offset - 1] < v1[k1Offset + 1] ? x1 = v1[k1Offset + 1] : x1 = v1[k1Offset - 1] + 1;
      let y1 = x1 - k1;
      for (; x1 < text1Length && y1 < text2Length && text1.charAt(x1) === text2.charAt(y1); ) x1++, y1++;
      if (v1[k1Offset] = x1, x1 > text1Length) k1end += 2;
      else if (y1 > text2Length) k1start += 2;
      else if (front) {
        const k2Offset = vOffset + delta - k1;
        if (k2Offset >= 0 && k2Offset < vLength && v2[k2Offset] !== -1) {
          const x2 = text1Length - v2[k2Offset];
          if (x1 >= x2) return bisectSplit(text1, text2, x1, y1, deadline);
        }
      }
    }
    for (let k2 = -d + k2start; k2 <= d - k2end; k2 += 2) {
      const k2Offset = vOffset + k2;
      let x2;
      k2 === -d || k2 !== d && v2[k2Offset - 1] < v2[k2Offset + 1] ? x2 = v2[k2Offset + 1] : x2 = v2[k2Offset - 1] + 1;
      let y2 = x2 - k2;
      for (; x2 < text1Length && y2 < text2Length && text1.charAt(text1Length - x2 - 1) === text2.charAt(text2Length - y2 - 1); ) x2++, y2++;
      if (v2[k2Offset] = x2, x2 > text1Length) k2end += 2;
      else if (y2 > text2Length) k2start += 2;
      else if (!front) {
        const k1Offset = vOffset + delta - k2;
        if (k1Offset >= 0 && k1Offset < vLength && v1[k1Offset] !== -1) {
          const x1 = v1[k1Offset], y1 = vOffset + x1 - k1Offset;
          if (x2 = text1Length - x2, x1 >= x2) return bisectSplit(text1, text2, x1, y1, deadline);
        }
      }
    }
  }
  return [[DIFF_DELETE, text1], [DIFF_INSERT, text2]];
}
function bisectSplit(text1, text2, x, y, deadline) {
  const text1a = text1.substring(0, x), text2a = text2.substring(0, y), text1b = text1.substring(x), text2b = text2.substring(y), diffs = doDiff(text1a, text2a, {
    checkLines: !1,
    deadline
  }), diffsb = doDiff(text1b, text2b, {
    checkLines: !1,
    deadline
  });
  return diffs.concat(diffsb);
}
function findHalfMatch(text1, text2, timeout = 1) {
  if (timeout <= 0) return null;
  const longText = text1.length > text2.length ? text1 : text2, shortText = text1.length > text2.length ? text2 : text1;
  if (longText.length < 4 || shortText.length * 2 < longText.length) return null;
  const halfMatch1 = halfMatchI(longText, shortText, Math.ceil(longText.length / 4)), halfMatch2 = halfMatchI(longText, shortText, Math.ceil(longText.length / 2));
  let halfMatch;
  if (halfMatch1 && halfMatch2) halfMatch = halfMatch1[4].length > halfMatch2[4].length ? halfMatch1 : halfMatch2;
  else {
    if (!halfMatch1 && !halfMatch2) return null;
    halfMatch2 ? halfMatch1 || (halfMatch = halfMatch2) : halfMatch = halfMatch1;
  }
  if (!halfMatch) throw new Error("Unable to find a half match.");
  let text1A, text1B, text2A, text2B;
  text1.length > text2.length ? (text1A = halfMatch[0], text1B = halfMatch[1], text2A = halfMatch[2], text2B = halfMatch[3]) : (text2A = halfMatch[0], text2B = halfMatch[1], text1A = halfMatch[2], text1B = halfMatch[3]);
  const midCommon = halfMatch[4];
  return [text1A, text1B, text2A, text2B, midCommon];
}
function halfMatchI(longText, shortText, i) {
  const seed = longText.slice(i, i + Math.floor(longText.length / 4));
  let j = -1, bestCommon = "", bestLongTextA, bestLongTextB, bestShortTextA, bestShortTextB;
  for (; (j = shortText.indexOf(seed, j + 1)) !== -1; ) {
    const prefixLength = getCommonPrefix(longText.slice(i), shortText.slice(j)), suffixLength = getCommonSuffix(longText.slice(0, i), shortText.slice(0, j));
    bestCommon.length < suffixLength + prefixLength && (bestCommon = shortText.slice(j - suffixLength, j) + shortText.slice(j, j + prefixLength), bestLongTextA = longText.slice(0, i - suffixLength), bestLongTextB = longText.slice(i + prefixLength), bestShortTextA = shortText.slice(0, j - suffixLength), bestShortTextB = shortText.slice(j + prefixLength));
  }
  return bestCommon.length * 2 >= longText.length ? [bestLongTextA || "", bestLongTextB || "", bestShortTextA || "", bestShortTextB || "", bestCommon || ""] : null;
}
function charsToLines(diffs, lineArray) {
  for (let x = 0; x < diffs.length; x++) {
    const chars = diffs[x][1], text = [];
    for (let y = 0; y < chars.length; y++) text[y] = lineArray[chars.charCodeAt(y)];
    diffs[x][1] = text.join("");
  }
}
function linesToChars(textA, textB) {
  const lineArray = [], lineHash = {};
  lineArray[0] = "";
  function diffLinesToMunge(text) {
    let chars = "", lineStart = 0, lineEnd = -1, lineArrayLength = lineArray.length;
    for (; lineEnd < text.length - 1; ) {
      lineEnd = text.indexOf(`
`, lineStart), lineEnd === -1 && (lineEnd = text.length - 1);
      let line = text.slice(lineStart, lineEnd + 1);
      (lineHash.hasOwnProperty ? lineHash.hasOwnProperty(line) : lineHash[line] !== void 0) ? chars += String.fromCharCode(lineHash[line]) : (lineArrayLength === maxLines && (line = text.slice(lineStart), lineEnd = text.length), chars += String.fromCharCode(lineArrayLength), lineHash[line] = lineArrayLength, lineArray[lineArrayLength++] = line), lineStart = lineEnd + 1;
    }
    return chars;
  }
  let maxLines = 4e4;
  const chars1 = diffLinesToMunge(textA);
  maxLines = 65535;
  const chars2 = diffLinesToMunge(textB);
  return {
    chars1,
    chars2,
    lineArray
  };
}
function doLineModeDiff(textA, textB, opts) {
  let text1 = textA, text2 = textB;
  const a = linesToChars(text1, text2);
  text1 = a.chars1, text2 = a.chars2;
  const linearray = a.lineArray;
  let diffs = doDiff(text1, text2, {
    checkLines: !1,
    deadline: opts.deadline
  });
  charsToLines(diffs, linearray), diffs = cleanupSemantic(diffs), diffs.push([DIFF_EQUAL, ""]);
  let pointer = 0, countDelete = 0, countInsert = 0, textDelete = "", textInsert = "";
  for (; pointer < diffs.length; ) {
    switch (diffs[pointer][0]) {
      case DIFF_INSERT:
        countInsert++, textInsert += diffs[pointer][1];
        break;
      case DIFF_DELETE:
        countDelete++, textDelete += diffs[pointer][1];
        break;
      case DIFF_EQUAL:
        if (countDelete >= 1 && countInsert >= 1) {
          diffs.splice(pointer - countDelete - countInsert, countDelete + countInsert), pointer = pointer - countDelete - countInsert;
          const aa = doDiff(textDelete, textInsert, {
            checkLines: !1,
            deadline: opts.deadline
          });
          for (let j = aa.length - 1; j >= 0; j--) diffs.splice(pointer, 0, aa[j]);
          pointer += aa.length;
        }
        countInsert = 0, countDelete = 0, textDelete = "", textInsert = "";
        break;
      default:
        throw new Error("Unknown diff operation.");
    }
    pointer++;
  }
  return diffs.pop(), diffs;
}
function computeDiff(text1, text2, opts) {
  let diffs;
  if (!text1) return [[DIFF_INSERT, text2]];
  if (!text2) return [[DIFF_DELETE, text1]];
  const longtext = text1.length > text2.length ? text1 : text2, shorttext = text1.length > text2.length ? text2 : text1, i = longtext.indexOf(shorttext);
  if (i !== -1) return diffs = [[DIFF_INSERT, longtext.substring(0, i)], [DIFF_EQUAL, shorttext], [DIFF_INSERT, longtext.substring(i + shorttext.length)]], text1.length > text2.length && (diffs[0][0] = DIFF_DELETE, diffs[2][0] = DIFF_DELETE), diffs;
  if (shorttext.length === 1) return [[DIFF_DELETE, text1], [DIFF_INSERT, text2]];
  const halfMatch = findHalfMatch(text1, text2);
  if (halfMatch) {
    const text1A = halfMatch[0], text1B = halfMatch[1], text2A = halfMatch[2], text2B = halfMatch[3], midCommon = halfMatch[4], diffsA = doDiff(text1A, text2A, opts), diffsB = doDiff(text1B, text2B, opts);
    return diffsA.concat([[DIFF_EQUAL, midCommon]], diffsB);
  }
  return opts.checkLines && text1.length > 100 && text2.length > 100 ? doLineModeDiff(text1, text2, opts) : bisect(text1, text2, opts.deadline);
}
var __defProp$2 = Object.defineProperty, __getOwnPropSymbols$2 = Object.getOwnPropertySymbols, __hasOwnProp$2 = Object.prototype.hasOwnProperty, __propIsEnum$2 = Object.prototype.propertyIsEnumerable, __defNormalProp$2 = (obj, key, value) => key in obj ? __defProp$2(obj, key, {
  enumerable: !0,
  configurable: !0,
  writable: !0,
  value
}) : obj[key] = value, __spreadValues$2 = (a, b) => {
  for (var prop in b || (b = {})) __hasOwnProp$2.call(b, prop) && __defNormalProp$2(a, prop, b[prop]);
  if (__getOwnPropSymbols$2) for (var prop of __getOwnPropSymbols$2(b)) __propIsEnum$2.call(b, prop) && __defNormalProp$2(a, prop, b[prop]);
  return a;
};
const DIFF_DELETE = -1, DIFF_INSERT = 1, DIFF_EQUAL = 0;
function diff(textA, textB, opts) {
  if (textA === null || textB === null) throw new Error("Null input. (diff)");
  const diffs = doDiff(textA, textB, createInternalOpts(opts || {}));
  return adjustDiffForSurrogatePairs(diffs), diffs;
}
function doDiff(textA, textB, options) {
  let text1 = textA, text2 = textB;
  if (text1 === text2) return text1 ? [[DIFF_EQUAL, text1]] : [];
  let commonlength = getCommonPrefix(text1, text2);
  const commonprefix = text1.substring(0, commonlength);
  text1 = text1.substring(commonlength), text2 = text2.substring(commonlength), commonlength = getCommonSuffix(text1, text2);
  const commonsuffix = text1.substring(text1.length - commonlength);
  text1 = text1.substring(0, text1.length - commonlength), text2 = text2.substring(0, text2.length - commonlength);
  let diffs = computeDiff(text1, text2, options);
  return commonprefix && diffs.unshift([DIFF_EQUAL, commonprefix]), commonsuffix && diffs.push([DIFF_EQUAL, commonsuffix]), diffs = cleanupMerge(diffs), diffs;
}
function createDeadLine(timeout) {
  let t = 1;
  return typeof timeout < "u" && (t = timeout <= 0 ? Number.MAX_VALUE : timeout), Date.now() + t * 1e3;
}
function createInternalOpts(opts) {
  return __spreadValues$2({
    checkLines: !0,
    deadline: createDeadLine(opts.timeout || 1)
  }, opts);
}
function combineChar(data, char, dir) {
  return dir === 1 ? data + char : char + data;
}
function splitChar(data, dir) {
  return dir === 1 ? [data.substring(0, data.length - 1), data[data.length - 1]] : [data.substring(1), data[0]];
}
function hasSharedChar(diffs, i, j, dir) {
  return dir === 1 ? diffs[i][1][diffs[i][1].length - 1] === diffs[j][1][diffs[j][1].length - 1] : diffs[i][1][0] === diffs[j][1][0];
}
function deisolateChar(diffs, i, dir) {
  const inv = dir === 1 ? -1 : 1;
  let insertIdx = null, deleteIdx = null, j = i + dir;
  for (; j >= 0 && j < diffs.length && (insertIdx === null || deleteIdx === null); j += dir) {
    const [op, text2] = diffs[j];
    if (text2.length !== 0) {
      if (op === DIFF_INSERT) {
        insertIdx === null && (insertIdx = j);
        continue;
      } else if (op === DIFF_DELETE) {
        deleteIdx === null && (deleteIdx = j);
        continue;
      } else if (op === DIFF_EQUAL) {
        if (insertIdx === null && deleteIdx === null) {
          const [rest, char2] = splitChar(diffs[i][1], dir);
          diffs[i][1] = rest, diffs[j][1] = combineChar(diffs[j][1], char2, inv);
          return;
        }
        break;
      }
    }
  }
  if (insertIdx !== null && deleteIdx !== null && hasSharedChar(diffs, insertIdx, deleteIdx, dir)) {
    const [insertText2, insertChar] = splitChar(diffs[insertIdx][1], inv), [deleteText2] = splitChar(diffs[deleteIdx][1], inv);
    diffs[insertIdx][1] = insertText2, diffs[deleteIdx][1] = deleteText2, diffs[i][1] = combineChar(diffs[i][1], insertChar, dir);
    return;
  }
  const [text, char] = splitChar(diffs[i][1], dir);
  diffs[i][1] = text, insertIdx === null ? (diffs.splice(j, 0, [DIFF_INSERT, char]), deleteIdx !== null && deleteIdx >= j && deleteIdx++) : diffs[insertIdx][1] = combineChar(diffs[insertIdx][1], char, inv), deleteIdx === null ? diffs.splice(j, 0, [DIFF_DELETE, char]) : diffs[deleteIdx][1] = combineChar(diffs[deleteIdx][1], char, inv);
}
function adjustDiffForSurrogatePairs(diffs) {
  for (let i = 0; i < diffs.length; i++) {
    const [diffType, diffText] = diffs[i];
    if (diffText.length === 0) continue;
    const firstChar = diffText[0], lastChar = diffText[diffText.length - 1];
    isHighSurrogate(lastChar) && diffType === DIFF_EQUAL && deisolateChar(diffs, i, 1), isLowSurrogate(firstChar) && diffType === DIFF_EQUAL && deisolateChar(diffs, i, -1);
  }
  for (let i = 0; i < diffs.length; i++) diffs[i][1].length === 0 && diffs.splice(i, 1);
}
function cleanupSemantic(rawDiffs) {
  let diffs = rawDiffs.map((diff2) => cloneDiff(diff2)), hasChanges = !1;
  const equalities = [];
  let equalitiesLength = 0, lastEquality = null, pointer = 0, lengthInsertions1 = 0, lengthDeletions1 = 0, lengthInsertions2 = 0, lengthDeletions2 = 0;
  for (; pointer < diffs.length; ) diffs[pointer][0] === DIFF_EQUAL ? (equalities[equalitiesLength++] = pointer, lengthInsertions1 = lengthInsertions2, lengthDeletions1 = lengthDeletions2, lengthInsertions2 = 0, lengthDeletions2 = 0, lastEquality = diffs[pointer][1]) : (diffs[pointer][0] === DIFF_INSERT ? lengthInsertions2 += diffs[pointer][1].length : lengthDeletions2 += diffs[pointer][1].length, lastEquality && lastEquality.length <= Math.max(lengthInsertions1, lengthDeletions1) && lastEquality.length <= Math.max(lengthInsertions2, lengthDeletions2) && (diffs.splice(equalities[equalitiesLength - 1], 0, [DIFF_DELETE, lastEquality]), diffs[equalities[equalitiesLength - 1] + 1][0] = DIFF_INSERT, equalitiesLength--, equalitiesLength--, pointer = equalitiesLength > 0 ? equalities[equalitiesLength - 1] : -1, lengthInsertions1 = 0, lengthDeletions1 = 0, lengthInsertions2 = 0, lengthDeletions2 = 0, lastEquality = null, hasChanges = !0)), pointer++;
  for (hasChanges && (diffs = cleanupMerge(diffs)), diffs = cleanupSemanticLossless(diffs), pointer = 1; pointer < diffs.length; ) {
    if (diffs[pointer - 1][0] === DIFF_DELETE && diffs[pointer][0] === DIFF_INSERT) {
      const deletion = diffs[pointer - 1][1], insertion = diffs[pointer][1], overlapLength1 = getCommonOverlap(deletion, insertion), overlapLength2 = getCommonOverlap(insertion, deletion);
      overlapLength1 >= overlapLength2 ? (overlapLength1 >= deletion.length / 2 || overlapLength1 >= insertion.length / 2) && (diffs.splice(pointer, 0, [DIFF_EQUAL, insertion.substring(0, overlapLength1)]), diffs[pointer - 1][1] = deletion.substring(0, deletion.length - overlapLength1), diffs[pointer + 1][1] = insertion.substring(overlapLength1), pointer++) : (overlapLength2 >= deletion.length / 2 || overlapLength2 >= insertion.length / 2) && (diffs.splice(pointer, 0, [DIFF_EQUAL, deletion.substring(0, overlapLength2)]), diffs[pointer - 1][0] = DIFF_INSERT, diffs[pointer - 1][1] = insertion.substring(0, insertion.length - overlapLength2), diffs[pointer + 1][0] = DIFF_DELETE, diffs[pointer + 1][1] = deletion.substring(overlapLength2), pointer++), pointer++;
    }
    pointer++;
  }
  return diffs;
}
const nonAlphaNumericRegex = /[^a-zA-Z0-9]/, whitespaceRegex = /\s/, linebreakRegex = /[\r\n]/, blanklineEndRegex = /\n\r?\n$/, blanklineStartRegex = /^\r?\n\r?\n/;
function cleanupSemanticLossless(rawDiffs) {
  const diffs = rawDiffs.map((diff2) => cloneDiff(diff2));
  function diffCleanupSemanticScore(one, two) {
    if (!one || !two) return 6;
    const char1 = one.charAt(one.length - 1), char2 = two.charAt(0), nonAlphaNumeric1 = char1.match(nonAlphaNumericRegex), nonAlphaNumeric2 = char2.match(nonAlphaNumericRegex), whitespace1 = nonAlphaNumeric1 && char1.match(whitespaceRegex), whitespace2 = nonAlphaNumeric2 && char2.match(whitespaceRegex), lineBreak1 = whitespace1 && char1.match(linebreakRegex), lineBreak2 = whitespace2 && char2.match(linebreakRegex), blankLine1 = lineBreak1 && one.match(blanklineEndRegex), blankLine2 = lineBreak2 && two.match(blanklineStartRegex);
    return blankLine1 || blankLine2 ? 5 : lineBreak1 || lineBreak2 ? 4 : nonAlphaNumeric1 && !whitespace1 && whitespace2 ? 3 : whitespace1 || whitespace2 ? 2 : nonAlphaNumeric1 || nonAlphaNumeric2 ? 1 : 0;
  }
  let pointer = 1;
  for (; pointer < diffs.length - 1; ) {
    if (diffs[pointer - 1][0] === DIFF_EQUAL && diffs[pointer + 1][0] === DIFF_EQUAL) {
      let equality1 = diffs[pointer - 1][1], edit = diffs[pointer][1], equality2 = diffs[pointer + 1][1];
      const commonOffset = getCommonSuffix(equality1, edit);
      if (commonOffset) {
        const commonString = edit.substring(edit.length - commonOffset);
        equality1 = equality1.substring(0, equality1.length - commonOffset), edit = commonString + edit.substring(0, edit.length - commonOffset), equality2 = commonString + equality2;
      }
      let bestEquality1 = equality1, bestEdit = edit, bestEquality2 = equality2, bestScore = diffCleanupSemanticScore(equality1, edit) + diffCleanupSemanticScore(edit, equality2);
      for (; edit.charAt(0) === equality2.charAt(0); ) {
        equality1 += edit.charAt(0), edit = edit.substring(1) + equality2.charAt(0), equality2 = equality2.substring(1);
        const score = diffCleanupSemanticScore(equality1, edit) + diffCleanupSemanticScore(edit, equality2);
        score >= bestScore && (bestScore = score, bestEquality1 = equality1, bestEdit = edit, bestEquality2 = equality2);
      }
      diffs[pointer - 1][1] !== bestEquality1 && (bestEquality1 ? diffs[pointer - 1][1] = bestEquality1 : (diffs.splice(pointer - 1, 1), pointer--), diffs[pointer][1] = bestEdit, bestEquality2 ? diffs[pointer + 1][1] = bestEquality2 : (diffs.splice(pointer + 1, 1), pointer--));
    }
    pointer++;
  }
  return diffs;
}
function cleanupMerge(rawDiffs) {
  let diffs = rawDiffs.map((diff2) => cloneDiff(diff2));
  diffs.push([DIFF_EQUAL, ""]);
  let pointer = 0, countDelete = 0, countInsert = 0, textDelete = "", textInsert = "", commonlength;
  for (; pointer < diffs.length; ) switch (diffs[pointer][0]) {
    case DIFF_INSERT:
      countInsert++, textInsert += diffs[pointer][1], pointer++;
      break;
    case DIFF_DELETE:
      countDelete++, textDelete += diffs[pointer][1], pointer++;
      break;
    case DIFF_EQUAL:
      countDelete + countInsert > 1 ? (countDelete !== 0 && countInsert !== 0 && (commonlength = getCommonPrefix(textInsert, textDelete), commonlength !== 0 && (pointer - countDelete - countInsert > 0 && diffs[pointer - countDelete - countInsert - 1][0] === DIFF_EQUAL ? diffs[pointer - countDelete - countInsert - 1][1] += textInsert.substring(0, commonlength) : (diffs.splice(0, 0, [DIFF_EQUAL, textInsert.substring(0, commonlength)]), pointer++), textInsert = textInsert.substring(commonlength), textDelete = textDelete.substring(commonlength)), commonlength = getCommonSuffix(textInsert, textDelete), commonlength !== 0 && (diffs[pointer][1] = textInsert.substring(textInsert.length - commonlength) + diffs[pointer][1], textInsert = textInsert.substring(0, textInsert.length - commonlength), textDelete = textDelete.substring(0, textDelete.length - commonlength))), pointer -= countDelete + countInsert, diffs.splice(pointer, countDelete + countInsert), textDelete.length && (diffs.splice(pointer, 0, [DIFF_DELETE, textDelete]), pointer++), textInsert.length && (diffs.splice(pointer, 0, [DIFF_INSERT, textInsert]), pointer++), pointer++) : pointer !== 0 && diffs[pointer - 1][0] === DIFF_EQUAL ? (diffs[pointer - 1][1] += diffs[pointer][1], diffs.splice(pointer, 1)) : pointer++, countInsert = 0, countDelete = 0, textDelete = "", textInsert = "";
      break;
    default:
      throw new Error("Unknown diff operation");
  }
  diffs[diffs.length - 1][1] === "" && diffs.pop();
  let hasChanges = !1;
  for (pointer = 1; pointer < diffs.length - 1; ) diffs[pointer - 1][0] === DIFF_EQUAL && diffs[pointer + 1][0] === DIFF_EQUAL && (diffs[pointer][1].substring(diffs[pointer][1].length - diffs[pointer - 1][1].length) === diffs[pointer - 1][1] ? (diffs[pointer][1] = diffs[pointer - 1][1] + diffs[pointer][1].substring(0, diffs[pointer][1].length - diffs[pointer - 1][1].length), diffs[pointer + 1][1] = diffs[pointer - 1][1] + diffs[pointer + 1][1], diffs.splice(pointer - 1, 1), hasChanges = !0) : diffs[pointer][1].substring(0, diffs[pointer + 1][1].length) === diffs[pointer + 1][1] && (diffs[pointer - 1][1] += diffs[pointer + 1][1], diffs[pointer][1] = diffs[pointer][1].substring(diffs[pointer + 1][1].length) + diffs[pointer + 1][1], diffs.splice(pointer + 1, 1), hasChanges = !0)), pointer++;
  return hasChanges && (diffs = cleanupMerge(diffs)), diffs;
}
function trueCount(...args) {
  return args.reduce((n2, bool) => n2 + (bool ? 1 : 0), 0);
}
function cleanupEfficiency(rawDiffs, editCost = 4) {
  let diffs = rawDiffs.map((diff2) => cloneDiff(diff2)), hasChanges = !1;
  const equalities = [];
  let equalitiesLength = 0, lastEquality = null, pointer = 0, preIns = !1, preDel = !1, postIns = !1, postDel = !1;
  for (; pointer < diffs.length; ) diffs[pointer][0] === DIFF_EQUAL ? (diffs[pointer][1].length < editCost && (postIns || postDel) ? (equalities[equalitiesLength++] = pointer, preIns = postIns, preDel = postDel, lastEquality = diffs[pointer][1]) : (equalitiesLength = 0, lastEquality = null), postIns = !1, postDel = !1) : (diffs[pointer][0] === DIFF_DELETE ? postDel = !0 : postIns = !0, lastEquality && (preIns && preDel && postIns && postDel || lastEquality.length < editCost / 2 && trueCount(preIns, preDel, postIns, postDel) === 3) && (diffs.splice(equalities[equalitiesLength - 1], 0, [DIFF_DELETE, lastEquality]), diffs[equalities[equalitiesLength - 1] + 1][0] = DIFF_INSERT, equalitiesLength--, lastEquality = null, preIns && preDel ? (postIns = !0, postDel = !0, equalitiesLength = 0) : (equalitiesLength--, pointer = equalitiesLength > 0 ? equalities[equalitiesLength - 1] : -1, postIns = !1, postDel = !1), hasChanges = !0)), pointer++;
  return hasChanges && (diffs = cleanupMerge(diffs)), diffs;
}
var __defProp$1 = Object.defineProperty, __getOwnPropSymbols$1 = Object.getOwnPropertySymbols, __hasOwnProp$1 = Object.prototype.hasOwnProperty, __propIsEnum$1 = Object.prototype.propertyIsEnumerable, __defNormalProp$1 = (obj, key, value) => key in obj ? __defProp$1(obj, key, {
  enumerable: !0,
  configurable: !0,
  writable: !0,
  value
}) : obj[key] = value, __spreadValues$1 = (a, b) => {
  for (var prop in b || (b = {})) __hasOwnProp$1.call(b, prop) && __defNormalProp$1(a, prop, b[prop]);
  if (__getOwnPropSymbols$1) for (var prop of __getOwnPropSymbols$1(b)) __propIsEnum$1.call(b, prop) && __defNormalProp$1(a, prop, b[prop]);
  return a;
};
const DEFAULT_OPTIONS = {
  /**
   * At what point is no match declared (0.0 = perfection, 1.0 = very loose).
   */
  threshold: 0.5,
  /**
   * How far to search for a match (0 = exact location, 1000+ = broad match).
   * A match this many characters away from the expected location will add
   * 1.0 to the score (0.0 is a perfect match).
   */
  distance: 1e3
};
function applyDefaults(options) {
  return __spreadValues$1(__spreadValues$1({}, DEFAULT_OPTIONS), options);
}
const MAX_BITS$1 = 32;
function bitap(text, pattern, loc, opts = {}) {
  if (pattern.length > MAX_BITS$1) throw new Error("Pattern too long for this browser.");
  const options = applyDefaults(opts), s = getAlphabetFromPattern(pattern);
  function getBitapScore(e, x) {
    const accuracy = e / pattern.length, proximity = Math.abs(loc - x);
    return options.distance ? accuracy + proximity / options.distance : proximity ? 1 : accuracy;
  }
  let scoreThreshold = options.threshold, bestLoc = text.indexOf(pattern, loc);
  bestLoc !== -1 && (scoreThreshold = Math.min(getBitapScore(0, bestLoc), scoreThreshold), bestLoc = text.lastIndexOf(pattern, loc + pattern.length), bestLoc !== -1 && (scoreThreshold = Math.min(getBitapScore(0, bestLoc), scoreThreshold)));
  const matchmask = 1 << pattern.length - 1;
  bestLoc = -1;
  let binMin, binMid, binMax = pattern.length + text.length, lastRd = [];
  for (let d = 0; d < pattern.length; d++) {
    for (binMin = 0, binMid = binMax; binMin < binMid; ) getBitapScore(d, loc + binMid) <= scoreThreshold ? binMin = binMid : binMax = binMid, binMid = Math.floor((binMax - binMin) / 2 + binMin);
    binMax = binMid;
    let start2 = Math.max(1, loc - binMid + 1);
    const finish = Math.min(loc + binMid, text.length) + pattern.length, rd = new Array(finish + 2);
    rd[finish + 1] = (1 << d) - 1;
    for (let j = finish; j >= start2; j--) {
      const charMatch = s[text.charAt(j - 1)];
      if (d === 0 ? rd[j] = (rd[j + 1] << 1 | 1) & charMatch : rd[j] = (rd[j + 1] << 1 | 1) & charMatch | ((lastRd[j + 1] | lastRd[j]) << 1 | 1) | lastRd[j + 1], rd[j] & matchmask) {
        const score = getBitapScore(d, j - 1);
        if (score <= scoreThreshold) if (scoreThreshold = score, bestLoc = j - 1, bestLoc > loc) start2 = Math.max(1, 2 * loc - bestLoc);
        else break;
      }
    }
    if (getBitapScore(d + 1, loc) > scoreThreshold) break;
    lastRd = rd;
  }
  return bestLoc;
}
function getAlphabetFromPattern(pattern) {
  const s = {};
  for (let i = 0; i < pattern.length; i++) s[pattern.charAt(i)] = 0;
  for (let i = 0; i < pattern.length; i++) s[pattern.charAt(i)] |= 1 << pattern.length - i - 1;
  return s;
}
function match(text, pattern, searchLocation, options = {}) {
  if (text === null || pattern === null || searchLocation === null) throw new Error("Null input. (match())");
  const loc = Math.max(0, Math.min(searchLocation, text.length));
  if (text === pattern) return 0;
  if (text.length) {
    if (text.substring(loc, loc + pattern.length) === pattern) return loc;
  } else return -1;
  return bitap(text, pattern, loc, options);
}
function diffText1(diffs) {
  const text = [];
  for (let x = 0; x < diffs.length; x++) diffs[x][0] !== DIFF_INSERT && (text[x] = diffs[x][1]);
  return text.join("");
}
function diffText2(diffs) {
  const text = [];
  for (let x = 0; x < diffs.length; x++) diffs[x][0] !== DIFF_DELETE && (text[x] = diffs[x][1]);
  return text.join("");
}
function levenshtein(diffs) {
  let leven = 0, insertions = 0, deletions = 0;
  for (let x = 0; x < diffs.length; x++) {
    const op = diffs[x][0], data = diffs[x][1];
    switch (op) {
      case DIFF_INSERT:
        insertions += data.length;
        break;
      case DIFF_DELETE:
        deletions += data.length;
        break;
      case DIFF_EQUAL:
        leven += Math.max(insertions, deletions), insertions = 0, deletions = 0;
        break;
      default:
        throw new Error("Unknown diff operation.");
    }
  }
  return leven += Math.max(insertions, deletions), leven;
}
function xIndex(diffs, location) {
  let chars1 = 0, chars2 = 0, lastChars1 = 0, lastChars2 = 0, x;
  for (x = 0; x < diffs.length && (diffs[x][0] !== DIFF_INSERT && (chars1 += diffs[x][1].length), diffs[x][0] !== DIFF_DELETE && (chars2 += diffs[x][1].length), !(chars1 > location)); x++) lastChars1 = chars1, lastChars2 = chars2;
  return diffs.length !== x && diffs[x][0] === DIFF_DELETE ? lastChars2 : lastChars2 + (location - lastChars1);
}
function countUtf8Bytes(str) {
  let bytes = 0;
  for (let i = 0; i < str.length; i++) {
    const codePoint = str.codePointAt(i);
    if (typeof codePoint > "u") throw new Error("Failed to get codepoint");
    bytes += utf8len(codePoint);
  }
  return bytes;
}
function adjustIndiciesToUcs2(patches, base, options = {}) {
  let byteOffset = 0, idx = 0;
  function advanceTo(target) {
    for (; byteOffset < target; ) {
      const codePoint = base.codePointAt(idx);
      if (typeof codePoint > "u") return idx;
      byteOffset += utf8len(codePoint), codePoint > 65535 ? idx += 2 : idx += 1;
    }
    if (!options.allowExceedingIndices && byteOffset !== target) throw new Error("Failed to determine byte offset");
    return idx;
  }
  const adjusted = [];
  for (const patch of patches) adjusted.push({
    diffs: patch.diffs.map((diff2) => cloneDiff(diff2)),
    start1: advanceTo(patch.start1),
    start2: advanceTo(patch.start2),
    utf8Start1: patch.utf8Start1,
    utf8Start2: patch.utf8Start2,
    length1: patch.length1,
    length2: patch.length2,
    utf8Length1: patch.utf8Length1,
    utf8Length2: patch.utf8Length2
  });
  return adjusted;
}
function utf8len(codePoint) {
  return codePoint <= 127 ? 1 : codePoint <= 2047 ? 2 : codePoint <= 65535 ? 3 : 4;
}
const MAX_BITS = 32, DEFAULT_MARGIN = 4;
function addPadding(patches, margin = DEFAULT_MARGIN) {
  const paddingLength = margin;
  let nullPadding = "";
  for (let x = 1; x <= paddingLength; x++) nullPadding += String.fromCharCode(x);
  for (const p of patches) p.start1 += paddingLength, p.start2 += paddingLength, p.utf8Start1 += paddingLength, p.utf8Start2 += paddingLength;
  let patch = patches[0], diffs = patch.diffs;
  if (diffs.length === 0 || diffs[0][0] !== DIFF_EQUAL) diffs.unshift([DIFF_EQUAL, nullPadding]), patch.start1 -= paddingLength, patch.start2 -= paddingLength, patch.utf8Start1 -= paddingLength, patch.utf8Start2 -= paddingLength, patch.length1 += paddingLength, patch.length2 += paddingLength, patch.utf8Length1 += paddingLength, patch.utf8Length2 += paddingLength;
  else if (paddingLength > diffs[0][1].length) {
    const firstDiffLength = diffs[0][1].length, extraLength = paddingLength - firstDiffLength;
    diffs[0][1] = nullPadding.substring(firstDiffLength) + diffs[0][1], patch.start1 -= extraLength, patch.start2 -= extraLength, patch.utf8Start1 -= extraLength, patch.utf8Start2 -= extraLength, patch.length1 += extraLength, patch.length2 += extraLength, patch.utf8Length1 += extraLength, patch.utf8Length2 += extraLength;
  }
  if (patch = patches[patches.length - 1], diffs = patch.diffs, diffs.length === 0 || diffs[diffs.length - 1][0] !== DIFF_EQUAL) diffs.push([DIFF_EQUAL, nullPadding]), patch.length1 += paddingLength, patch.length2 += paddingLength, patch.utf8Length1 += paddingLength, patch.utf8Length2 += paddingLength;
  else if (paddingLength > diffs[diffs.length - 1][1].length) {
    const extraLength = paddingLength - diffs[diffs.length - 1][1].length;
    diffs[diffs.length - 1][1] += nullPadding.substring(0, extraLength), patch.length1 += extraLength, patch.length2 += extraLength, patch.utf8Length1 += extraLength, patch.utf8Length2 += extraLength;
  }
  return nullPadding;
}
function createPatchObject(start1, start2) {
  return {
    diffs: [],
    start1,
    start2,
    utf8Start1: start1,
    utf8Start2: start2,
    length1: 0,
    length2: 0,
    utf8Length1: 0,
    utf8Length2: 0
  };
}
function splitMax(patches, margin = DEFAULT_MARGIN) {
  const patchSize = MAX_BITS;
  for (let x = 0; x < patches.length; x++) {
    if (patches[x].length1 <= patchSize) continue;
    const bigpatch = patches[x];
    patches.splice(x--, 1);
    let start1 = bigpatch.start1, start2 = bigpatch.start2, preContext = "";
    for (; bigpatch.diffs.length !== 0; ) {
      const patch = createPatchObject(start1 - preContext.length, start2 - preContext.length);
      let empty = !0;
      if (preContext !== "") {
        const precontextByteCount = countUtf8Bytes(preContext);
        patch.length1 = preContext.length, patch.utf8Length1 = precontextByteCount, patch.length2 = preContext.length, patch.utf8Length2 = precontextByteCount, patch.diffs.push([DIFF_EQUAL, preContext]);
      }
      for (; bigpatch.diffs.length !== 0 && patch.length1 < patchSize - margin; ) {
        const diffType = bigpatch.diffs[0][0];
        let diffText = bigpatch.diffs[0][1], diffTextByteCount = countUtf8Bytes(diffText);
        if (diffType === DIFF_INSERT) {
          patch.length2 += diffText.length, patch.utf8Length2 += diffTextByteCount, start2 += diffText.length;
          const diff2 = bigpatch.diffs.shift();
          diff2 && patch.diffs.push(diff2), empty = !1;
        } else diffType === DIFF_DELETE && patch.diffs.length === 1 && patch.diffs[0][0] === DIFF_EQUAL && diffText.length > 2 * patchSize ? (patch.length1 += diffText.length, patch.utf8Length1 += diffTextByteCount, start1 += diffText.length, empty = !1, patch.diffs.push([diffType, diffText]), bigpatch.diffs.shift()) : (diffText = diffText.substring(0, patchSize - patch.length1 - margin), diffTextByteCount = countUtf8Bytes(diffText), patch.length1 += diffText.length, patch.utf8Length1 += diffTextByteCount, start1 += diffText.length, diffType === DIFF_EQUAL ? (patch.length2 += diffText.length, patch.utf8Length2 += diffTextByteCount, start2 += diffText.length) : empty = !1, patch.diffs.push([diffType, diffText]), diffText === bigpatch.diffs[0][1] ? bigpatch.diffs.shift() : bigpatch.diffs[0][1] = bigpatch.diffs[0][1].substring(diffText.length));
      }
      preContext = diffText2(patch.diffs), preContext = preContext.substring(preContext.length - margin);
      const postContext = diffText1(bigpatch.diffs).substring(0, margin), postContextByteCount = countUtf8Bytes(postContext);
      postContext !== "" && (patch.length1 += postContext.length, patch.length2 += postContext.length, patch.utf8Length1 += postContextByteCount, patch.utf8Length2 += postContextByteCount, patch.diffs.length !== 0 && patch.diffs[patch.diffs.length - 1][0] === DIFF_EQUAL ? patch.diffs[patch.diffs.length - 1][1] += postContext : patch.diffs.push([DIFF_EQUAL, postContext])), empty || patches.splice(++x, 0, patch);
    }
  }
}
function apply(patches, originalText, opts = {}) {
  if (typeof patches == "string") throw new Error("Patches must be an array - pass the patch to `parsePatch()` first");
  let text = originalText;
  if (patches.length === 0) return [text, []];
  const parsed = adjustIndiciesToUcs2(patches, text, {
    allowExceedingIndices: opts.allowExceedingIndices
  }), margin = opts.margin || DEFAULT_MARGIN, deleteThreshold = opts.deleteThreshold || 0.4, nullPadding = addPadding(parsed, margin);
  text = nullPadding + text + nullPadding, splitMax(parsed, margin);
  let delta = 0;
  const results = [];
  for (let x = 0; x < parsed.length; x++) {
    const expectedLoc = parsed[x].start2 + delta, text1 = diffText1(parsed[x].diffs);
    let startLoc, endLoc = -1;
    if (text1.length > MAX_BITS ? (startLoc = match(text, text1.substring(0, MAX_BITS), expectedLoc), startLoc !== -1 && (endLoc = match(text, text1.substring(text1.length - MAX_BITS), expectedLoc + text1.length - MAX_BITS), (endLoc === -1 || startLoc >= endLoc) && (startLoc = -1))) : startLoc = match(text, text1, expectedLoc), startLoc === -1) results[x] = !1, delta -= parsed[x].length2 - parsed[x].length1;
    else {
      results[x] = !0, delta = startLoc - expectedLoc;
      let text2;
      if (endLoc === -1 ? text2 = text.substring(startLoc, startLoc + text1.length) : text2 = text.substring(startLoc, endLoc + MAX_BITS), text1 === text2) text = text.substring(0, startLoc) + diffText2(parsed[x].diffs) + text.substring(startLoc + text1.length);
      else {
        let diffs = diff(text1, text2, {
          checkLines: !1
        });
        if (text1.length > MAX_BITS && levenshtein(diffs) / text1.length > deleteThreshold) results[x] = !1;
        else {
          diffs = cleanupSemanticLossless(diffs);
          let index1 = 0, index2 = 0;
          for (let y = 0; y < parsed[x].diffs.length; y++) {
            const mod = parsed[x].diffs[y];
            mod[0] !== DIFF_EQUAL && (index2 = xIndex(diffs, index1)), mod[0] === DIFF_INSERT ? text = text.substring(0, startLoc + index2) + mod[1] + text.substring(startLoc + index2) : mod[0] === DIFF_DELETE && (text = text.substring(0, startLoc + index2) + text.substring(startLoc + xIndex(diffs, index1 + mod[1].length))), mod[0] !== DIFF_DELETE && (index1 += mod[1].length);
          }
        }
      }
    }
  }
  return text = text.substring(nullPadding.length, text.length - nullPadding.length), [text, results];
}
const patchHeader = /^@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@$/;
function parse(textline) {
  if (!textline) return [];
  const patches = [], lines = textline.split(`
`);
  let textPointer = 0;
  for (; textPointer < lines.length; ) {
    const m = lines[textPointer].match(patchHeader);
    if (!m) throw new Error(`Invalid patch string: ${lines[textPointer]}`);
    const patch = createPatchObject(toInt(m[1]), toInt(m[3]));
    for (patches.push(patch), m[2] === "" ? (patch.start1--, patch.utf8Start1--, patch.length1 = 1, patch.utf8Length1 = 1) : m[2] === "0" ? (patch.length1 = 0, patch.utf8Length1 = 0) : (patch.start1--, patch.utf8Start1--, patch.utf8Length1 = toInt(m[2]), patch.length1 = patch.utf8Length1), m[4] === "" ? (patch.start2--, patch.utf8Start2--, patch.length2 = 1, patch.utf8Length2 = 1) : m[4] === "0" ? (patch.length2 = 0, patch.utf8Length2 = 0) : (patch.start2--, patch.utf8Start2--, patch.utf8Length2 = toInt(m[4]), patch.length2 = patch.utf8Length2), textPointer++; textPointer < lines.length; ) {
      const currentLine = lines[textPointer], sign = currentLine.charAt(0);
      if (sign === "@") break;
      if (sign === "") {
        textPointer++;
        continue;
      }
      let line;
      try {
        line = decodeURI(currentLine.slice(1));
      } catch {
        throw new Error(`Illegal escape in parse: ${currentLine}`);
      }
      const utf8Diff = countUtf8Bytes(line) - line.length;
      if (sign === "-") patch.diffs.push([DIFF_DELETE, line]), patch.length1 -= utf8Diff;
      else if (sign === "+") patch.diffs.push([DIFF_INSERT, line]), patch.length2 -= utf8Diff;
      else if (sign === " ") patch.diffs.push([DIFF_EQUAL, line]), patch.length1 -= utf8Diff, patch.length2 -= utf8Diff;
      else throw new Error(`Invalid patch mode "${sign}" in: ${line}`);
      textPointer++;
    }
  }
  return patches;
}
function toInt(num) {
  return parseInt(num, 10);
}
function createApplyPatch(context) {
  return (editor, patch) => {
    let changed = !1;
    try {
      switch (patch.type) {
        case "insert":
          changed = insertPatch(context, editor, patch);
          break;
        case "unset":
          changed = unsetPatch(editor, patch);
          break;
        case "set":
          changed = setPatch(editor, patch);
          break;
        case "setIfMissing":
          changed = setPatch(editor, patch);
          break;
        case "diffMatchPatch":
          changed = diffMatchPatch(editor, patch);
          break;
      }
    } catch (err) {
      console.error(err);
    }
    return changed;
  };
}
function diffMatchPatch(editor, patch) {
  const block = findBlock(editor.children, patch.path);
  if (!block)
    return !1;
  const child = findBlockChild(block, patch.path);
  if (!child || !(block && editor.isTextBlock(block.node) && patch.path.length === 4 && patch.path[1] === "children" && patch.path[3] === "text") || !Text$1.isText(child.node))
    return !1;
  const patches = parse(patch.value), [newValue] = apply(patches, child.node.text, {
    allowExceedingIndices: !0
  }), diff$1 = cleanupEfficiency(diff(child.node.text, newValue), 5);
  let offset = 0;
  for (const [op, text] of diff$1)
    op === DIFF_INSERT ? (editor.apply({
      type: "insert_text",
      path: [block.index, child.index],
      offset,
      text
    }), offset += text.length) : op === DIFF_DELETE ? editor.apply({
      type: "remove_text",
      path: [block.index, child.index],
      offset,
      text
    }) : op === DIFF_EQUAL && (offset += text.length);
  return !0;
}
function insertPatch(context, editor, patch) {
  const block = findBlock(editor.children, patch.path);
  if (!block) {
    if (patch.path.length === 1 && patch.path[0] === 0) {
      const blocksToInsert = patch.items.map((item) => toSlateBlock(item, {
        schemaTypes: context.schema
      }));
      return Transforms.insertNodes(editor, blocksToInsert, {
        at: [0]
      }), !0;
    }
    return !1;
  }
  if (patch.path.length > 1 && patch.path[1] !== "children")
    return !1;
  if (patch.path.length === 1) {
    const {
      items: items2,
      position: position2
    } = patch, blocksToInsert = items2.map((item) => toSlateBlock(item, {
      schemaTypes: context.schema
    })), targetBlockIndex = block.index, normalizedIdx2 = position2 === "after" ? targetBlockIndex + 1 : targetBlockIndex, editorWasEmptyBefore = isEqualToEmptyEditor(context.initialValue, editor.value, context.schema);
    return Transforms.insertNodes(editor, blocksToInsert, {
      at: [normalizedIdx2]
    }), editorWasEmptyBefore && typeof patch.path[0] == "number" && patch.path[0] === 0 && Transforms.removeNodes(editor, {
      at: [position2 === "before" ? targetBlockIndex + blocksToInsert.length : targetBlockIndex]
    }), !0;
  }
  const {
    items,
    position
  } = patch, targetChild = findBlockChild(block, patch.path);
  if (!targetChild)
    return !1;
  const childrenToInsert = toSlateBlock({
    ...block.node,
    children: items
  }, {
    schemaTypes: context.schema
  }), normalizedIdx = position === "after" ? targetChild.index + 1 : targetChild.index, childInsertPath = [block.index, normalizedIdx];
  return childrenToInsert && Element$2.isElement(childrenToInsert) && Transforms.insertNodes(editor, childrenToInsert.children, {
    at: childInsertPath
  }), !0;
}
function setPatch(editor, patch) {
  let value = patch.value;
  typeof patch.path[3] == "string" && (value = {}, value[patch.path[3]] = patch.value);
  const block = findBlock(editor.children, patch.path);
  if (!block)
    return !1;
  const isTextBlock2 = editor.isTextBlock(block.node);
  if (patch.path.length === 1) {
    const updatedBlock = applyAll(block.node, [{
      ...patch,
      path: patch.path.slice(1)
    }]);
    if (editor.isTextBlock(block.node) && Element$2.isElement(updatedBlock)) {
      Transforms.setNodes(editor, updatedBlock, {
        at: [block.index]
      });
      const previousSelection = editor.selection;
      for (const [_, childPath] of Editor.nodes(editor, {
        at: [block.index],
        reverse: !0,
        mode: "lowest"
      }))
        Transforms.removeNodes(editor, {
          at: childPath
        });
      return Transforms.insertNodes(editor, updatedBlock.children, {
        at: [block.index, 0]
      }), previousSelection && (Transforms.setSelection(editor, previousSelection), Transforms.select(editor, previousSelection)), !0;
    } else
      return Transforms.setNodes(editor, updatedBlock, {
        at: [block.index]
      }), !0;
  }
  if (isTextBlock2 && patch.path[1] !== "children") {
    const updatedBlock = applyAll(block.node, [{
      ...patch,
      path: patch.path.slice(1)
    }]);
    return Transforms.setNodes(editor, updatedBlock, {
      at: [block.index]
    }), !0;
  }
  const child = findBlockChild(block, patch.path);
  if (isTextBlock2 && child) {
    if (Text$1.isText(child.node))
      if (Text$1.isText(value)) {
        if (patch.type === "setIfMissing")
          return !1;
        const oldText = child.node.text, newText = value.text;
        oldText !== newText && (editor.apply({
          type: "remove_text",
          path: [block.index, child.index],
          offset: 0,
          text: oldText
        }), editor.apply({
          type: "insert_text",
          path: [block.index, child.index],
          offset: 0,
          text: newText
        }), editor.onChange());
      } else {
        const propPath = patch.path.slice(3), propEntry = propPath.at(0);
        if (propEntry === void 0 || typeof propEntry == "string" && ["_key", "_type", "text"].includes(propEntry))
          return !1;
        const newNode = applyAll(child.node, [{
          ...patch,
          path: propPath
        }]);
        Transforms.setNodes(editor, newNode, {
          at: [block.index, child.index]
        });
      }
    else {
      const propPath = patch.path.slice(3), reservedProps = ["_key", "_type", "children", "__inline"], propEntry = propPath.at(0);
      if (propEntry === void 0 || typeof propEntry == "string" && reservedProps.includes(propEntry))
        return !1;
      const value2 = "value" in child.node && typeof child.node.value == "object" ? child.node.value : {}, newValue = applyAll(value2, [{
        ...patch,
        path: patch.path.slice(3)
      }]);
      Transforms.setNodes(editor, {
        ...child.node,
        value: newValue
      }, {
        at: [block.index, child.index]
      });
    }
    return !0;
  } else if (block && "value" in block.node)
    if (patch.path.length > 1 && patch.path[1] !== "children") {
      const newVal = applyAll(block.node.value, [{
        ...patch,
        path: patch.path.slice(1)
      }]);
      Transforms.setNodes(editor, {
        ...block.node,
        value: newVal
      }, {
        at: [block.index]
      });
    } else
      return !1;
  return !0;
}
function unsetPatch(editor, patch) {
  if (patch.path.length === 0) {
    Transforms.deselect(editor);
    const children = Node$1.children(editor, [], {
      reverse: !0
    });
    for (const [_, path2] of children)
      Transforms.removeNodes(editor, {
        at: path2
      });
    return !0;
  }
  const block = findBlock(editor.children, patch.path);
  if (!block)
    return !1;
  if (patch.path.length === 1)
    return Transforms.removeNodes(editor, {
      at: [block.index]
    }), !0;
  const child = findBlockChild(block, patch.path);
  if (editor.isTextBlock(block.node) && child && patch.path[1] === "children" && patch.path.length === 3)
    return Transforms.removeNodes(editor, {
      at: [block.index, child.index]
    }), !0;
  if (child && !Text$1.isText(child.node)) {
    const propEntry = patch.path.slice(3).at(0);
    if (propEntry === void 0 || typeof propEntry == "string" && ["_key", "_type", "children", "__inline"].includes(propEntry))
      return !1;
    const value = "value" in child.node && typeof child.node.value == "object" ? child.node.value : {}, newValue = applyAll(value, [{
      ...patch,
      path: patch.path.slice(3)
    }]);
    return Transforms.setNodes(editor, {
      ...child.node,
      value: newValue
    }, {
      at: [block.index, child.index]
    }), !0;
  }
  if (child && Text$1.isText(child.node)) {
    const propPath = patch.path.slice(3), propEntry = propPath.at(0);
    if (propEntry === void 0 || typeof propEntry == "string" && ["_key", "_type"].includes(propEntry))
      return !1;
    if (typeof propEntry == "string" && propEntry === "text")
      return editor.apply({
        type: "remove_text",
        path: [block.index, child.index],
        offset: 0,
        text: child.node.text
      }), !0;
    const newNode = applyAll(child.node, [{
      ...patch,
      path: propPath
    }]), newKeys = Object.keys(newNode), removedProperties = Object.keys(child.node).filter((property) => !newKeys.includes(property));
    return Transforms.unsetNodes(editor, removedProperties, {
      at: [block.index, child.index]
    }), !0;
  }
  if (!child) {
    if ("value" in block.node) {
      const newVal = applyAll(block.node.value, [{
        ...patch,
        path: patch.path.slice(1)
      }]);
      return Transforms.setNodes(editor, {
        ...block.node,
        value: newVal
      }, {
        at: [block.index]
      }), !0;
    }
    if (editor.isTextBlock(block.node)) {
      const propEntry = patch.path.slice(1).at(0);
      return propEntry === void 0 || typeof propEntry != "string" || ["_key", "_type", "children"].includes(propEntry) ? !1 : (Transforms.unsetNodes(editor, [propEntry], {
        at: [block.index]
      }), !0);
    }
    return !1;
  }
  return !1;
}
function findBlock(children, path2) {
  let blockIndex = -1;
  const block = children.find((node2, index) => {
    const isMatch = isKeyedSegment(path2[0]) ? node2._key === path2[0]._key : index === path2[0];
    return isMatch && (blockIndex = index), isMatch;
  });
  if (block)
    return {
      node: block,
      index: blockIndex
    };
}
function findBlockChild(block, path2) {
  const blockNode = block.node;
  if (!Element$2.isElement(blockNode) || path2[1] !== "children")
    return;
  let childIndex = -1;
  const child = blockNode.children.find((node2, index) => {
    const isMatch = isKeyedSegment(path2[2]) ? node2._key === path2[2]._key : index === path2[2];
    return isMatch && (childIndex = index), isMatch;
  });
  if (child)
    return {
      node: child,
      index: childIndex
    };
}
function insertTextPatch(schema, children, operation, beforeValue) {
  const block = isTextBlock({
    schema
  }, children[operation.path[0]]) && children[operation.path[0]];
  if (!block)
    throw new Error("Could not find block");
  const textChild = isTextBlock({
    schema
  }, block) && isSpan({
    schema
  }, block.children[operation.path[1]]) && block.children[operation.path[1]];
  if (!textChild)
    throw new Error("Could not find child");
  const path2 = [{
    _key: block._key
  }, "children", {
    _key: textChild._key
  }, "text"], prevBlock = beforeValue[operation.path[0]], prevChild = isTextBlock({
    schema
  }, prevBlock) && prevBlock.children[operation.path[1]], prevText = isSpan({
    schema
  }, prevChild) ? prevChild.text : "", patch = diffMatchPatch$1(prevText, textChild.text, path2);
  return patch.value.length ? [patch] : [];
}
function removeTextPatch(schema, children, operation, beforeValue) {
  const block = children[operation.path[0]];
  if (!block)
    throw new Error("Could not find block");
  const child = isTextBlock({
    schema
  }, block) && block.children[operation.path[1]] || void 0, textChild = isSpan({
    schema
  }, child) ? child : void 0;
  if (child && !textChild)
    throw new Error("Expected span");
  if (!textChild)
    throw new Error("Could not find child");
  const path2 = [{
    _key: block._key
  }, "children", {
    _key: textChild._key
  }, "text"], beforeBlock = beforeValue[operation.path[0]], prevTextChild = isTextBlock({
    schema
  }, beforeBlock) && beforeBlock.children[operation.path[1]], prevText = isSpan({
    schema
  }, prevTextChild) && prevTextChild.text, patch = diffMatchPatch$1(prevText || "", textChild.text, path2);
  return patch.value ? [patch] : [];
}
function setNodePatch(schema, children, operation) {
  const blockIndex = operation.path.at(0);
  if (blockIndex !== void 0 && operation.path.length === 1) {
    const block = children.at(blockIndex);
    if (!block)
      return console.error("Could not find block at index", blockIndex), [];
    if (isTextBlock({
      schema
    }, block)) {
      const patches = [];
      for (const key of Object.keys(operation.newProperties)) {
        const value = operation.newProperties[key];
        key === "_key" ? patches.push(set(value, [blockIndex, "_key"])) : patches.push(set(value, [{
          _key: block._key
        }, key]));
      }
      for (const key of Object.keys(operation.properties))
        key in operation.newProperties || patches.push(unset([{
          _key: block._key
        }, key]));
      return patches;
    } else {
      const patches = [], _key = operation.newProperties._key;
      _key !== void 0 && patches.push(set(_key, [blockIndex, "_key"]));
      const newValue = "value" in operation.newProperties && typeof operation.newProperties.value == "object" ? operation.newProperties.value : {}, keys = Object.keys(newValue);
      for (const key of keys) {
        const value2 = newValue[key];
        patches.push(set(value2, [{
          _key: block._key
        }, key]));
      }
      const value = "value" in operation.properties && typeof operation.properties.value == "object" ? operation.properties.value : {};
      for (const key of Object.keys(value))
        key in newValue || patches.push(unset([{
          _key: block._key
        }, key]));
      return patches;
    }
  } else if (operation.path.length === 2) {
    const block = children[operation.path[0]];
    if (isTextBlock({
      schema
    }, block)) {
      const child = block.children[operation.path[1]];
      if (child) {
        const blockKey = block._key, childKey = child._key, patches = [];
        if (Element$2.isElement(child)) {
          const _key = operation.newProperties._key;
          _key !== void 0 && patches.push(set(_key, [{
            _key: blockKey
          }, "children", block.children.indexOf(child), "_key"]));
          const properties = "value" in operation.newProperties && typeof operation.newProperties.value == "object" ? operation.newProperties.value : {}, keys = Object.keys(properties);
          for (const key of keys) {
            const value = properties[key];
            patches.push(set(value, [{
              _key: blockKey
            }, "children", {
              _key: childKey
            }, key]));
          }
          return patches;
        }
        const newPropNames = Object.keys(operation.newProperties);
        for (const keyName of newPropNames) {
          const value = operation.newProperties[keyName];
          if (keyName === "_key") {
            patches.push(set(value, [{
              _key: blockKey
            }, "children", block.children.indexOf(child), keyName]));
            continue;
          }
          patches.push(set(value, [{
            _key: blockKey
          }, "children", {
            _key: childKey
          }, keyName]));
        }
        const propNames = Object.keys(operation.properties);
        for (const keyName of propNames)
          keyName in operation.newProperties || patches.push(unset([{
            _key: blockKey
          }, "children", {
            _key: childKey
          }, keyName]));
        return patches;
      }
      throw new Error("Could not find a valid child");
    }
    throw new Error("Could not find a valid block");
  } else
    throw new Error(`Unexpected path encountered: ${JSON.stringify(operation.path)}`);
}
function insertNodePatch(schema, children, operation, beforeValue) {
  const block = beforeValue[operation.path[0]];
  if (operation.path.length === 1) {
    const position = operation.path[0] === 0 ? "before" : "after", beforeBlock = beforeValue[operation.path[0] - 1], targetKey = operation.path[0] === 0 ? block?._key : beforeBlock?._key;
    return targetKey ? [insert([fromSlateBlock(operation.node, schema.block.name)], position, [{
      _key: targetKey
    }])] : [setIfMissing(beforeValue, []), insert([fromSlateBlock(operation.node, schema.block.name)], "before", [operation.path[0]])];
  } else if (isTextBlock({
    schema
  }, block) && operation.path.length === 2 && children[operation.path[0]]) {
    const position = block.children.length === 0 || !block.children[operation.path[1] - 1] ? "before" : "after", path2 = block.children.length <= 1 || !block.children[operation.path[1] - 1] ? [{
      _key: block._key
    }, "children", 0] : [{
      _key: block._key
    }, "children", {
      _key: block.children[operation.path[1] - 1]._key
    }], setIfMissingPatch = setIfMissing([], [{
      _key: block._key
    }, "children"]);
    if (Text$1.isText(operation.node))
      return [setIfMissingPatch, insert([operation.node], position, path2)];
    const _type = operation.node._type, _key = operation.node._key, value = "value" in operation.node && typeof operation.node.value == "object" ? operation.node.value : {};
    return [setIfMissingPatch, insert([{
      _type,
      _key,
      ...value
    }], position, path2)];
  }
  return [];
}
function splitNodePatch(schema, children, operation, beforeValue) {
  const patches = [], splitBlock = children[operation.path[0]];
  if (!isTextBlock({
    schema
  }, splitBlock))
    throw new Error(`Block with path ${JSON.stringify(operation.path[0])} is not a text block and can't be split`);
  if (operation.path.length === 1) {
    const oldBlock = beforeValue[operation.path[0]];
    if (isTextBlock({
      schema
    }, oldBlock)) {
      const nextBlock = children[operation.path[0] + 1];
      if (!nextBlock)
        return patches;
      const targetValue = fromSlateBlock(nextBlock, schema.block.name);
      targetValue && (patches.push(insert([targetValue], "after", [{
        _key: splitBlock._key
      }])), oldBlock.children.slice(operation.position).forEach((span) => {
        const path2 = [{
          _key: oldBlock._key
        }, "children", {
          _key: span._key
        }];
        patches.push(unset(path2));
      }));
    }
    return patches;
  }
  if (operation.path.length === 2) {
    const splitSpan = splitBlock.children[operation.path[1]];
    if (isSpan({
      schema
    }, splitSpan)) {
      const targetSpans = fromSlateBlock({
        ...splitBlock,
        children: splitBlock.children.slice(operation.path[1] + 1, operation.path[1] + 2)
      }, schema.block.name).children;
      patches.push(setIfMissing([], [{
        _key: splitBlock._key
      }, "children"])), patches.push(insert(targetSpans, "after", [{
        _key: splitBlock._key
      }, "children", {
        _key: splitSpan._key
      }])), patches.push(set(splitSpan.text, [{
        _key: splitBlock._key
      }, "children", {
        _key: splitSpan._key
      }, "text"]));
    }
    return patches;
  }
  return patches;
}
function removeNodePatch(schema, beforeValue, operation) {
  const block = beforeValue[operation.path[0]];
  if (operation.path.length === 1) {
    if (block && block._key)
      return [unset([{
        _key: block._key
      }])];
    throw new Error("Block not found");
  } else if (isTextBlock({
    schema
  }, block) && operation.path.length === 2) {
    const spanToRemove = block.children[operation.path[1]];
    return spanToRemove ? block.children.filter((span) => span._key === operation.node._key).length > 1 ? (console.warn(`Multiple spans have \`_key\` ${operation.node._key}. It's ambiguous which one to remove.`, JSON.stringify(block, null, 2)), []) : [unset([{
      _key: block._key
    }, "children", {
      _key: spanToRemove._key
    }])] : [];
  } else
    return [];
}
function mergeNodePatch(schema, children, operation, beforeValue) {
  const patches = [], block = beforeValue[operation.path[0]], updatedBlock = children[operation.path[0]];
  if (operation.path.length === 1)
    if (block?._key) {
      const prevBlock = children[operation.path[0] - 1];
      if (!prevBlock)
        throw new Error("Previous block not found!");
      const newBlock = fromSlateBlock(prevBlock, schema.block.name);
      patches.push(set(newBlock, [{
        _key: newBlock._key
      }])), patches.push(unset([{
        _key: block._key
      }]));
    } else
      throw new Error("Target key not found!");
  else if (isTextBlock({
    schema
  }, block) && isTextBlock({
    schema
  }, updatedBlock) && operation.path.length === 2) {
    const updatedSpan = updatedBlock.children[operation.path[1] - 1] && isSpan({
      schema
    }, updatedBlock.children[operation.path[1] - 1]) ? updatedBlock.children[operation.path[1] - 1] : void 0, removedSpan = block.children[operation.path[1]] && isSpan({
      schema
    }, block.children[operation.path[1]]) ? block.children[operation.path[1]] : void 0;
    if (updatedSpan) {
      const spansMatchingKey = block.children.filter((span) => span._key === updatedSpan._key);
      if (spansMatchingKey.length === 1) {
        const prevSpan = spansMatchingKey[0];
        isSpan({
          schema
        }, prevSpan) && prevSpan.text !== updatedSpan.text && patches.push(set(updatedSpan.text, [{
          _key: block._key
        }, "children", {
          _key: updatedSpan._key
        }, "text"]));
      } else
        console.warn(`Multiple spans have \`_key\` ${updatedSpan._key}. It's ambiguous which one to update.`, JSON.stringify(block, null, 2));
    }
    removedSpan && (block.children.filter((span) => span._key === removedSpan._key).length === 1 ? patches.push(unset([{
      _key: block._key
    }, "children", {
      _key: removedSpan._key
    }])) : console.warn(`Multiple spans have \`_key\` ${removedSpan._key}. It's ambiguous which one to remove.`, JSON.stringify(block, null, 2)));
  }
  return patches;
}
function moveNodePatch(schema, beforeValue, operation) {
  const patches = [], block = beforeValue[operation.path[0]], targetBlock = beforeValue[operation.newPath[0]];
  if (!targetBlock || !block)
    return patches;
  if (operation.path.length === 1) {
    const position = operation.path[0] > operation.newPath[0] ? "before" : "after";
    patches.push(unset([{
      _key: block._key
    }])), patches.push(insert([block], position, [{
      _key: targetBlock._key
    }]));
  } else if (operation.path.length === 2 && isTextBlock({
    schema
  }, block) && isTextBlock({
    schema
  }, targetBlock)) {
    const child = block.children[operation.path[1]], targetChild = targetBlock.children[operation.newPath[1]], position = operation.newPath[1] === targetBlock.children.length ? "after" : "before", childToInsert = block.children[operation.path[1]];
    if (!child || !targetChild || !childToInsert)
      return patches;
    patches.push(unset([{
      _key: block._key
    }, "children", {
      _key: child._key
    }])), patches.push(setIfMissing([], [{
      _key: targetBlock._key
    }, "children"])), patches.push(insert([childToInsert], position, [{
      _key: targetBlock._key
    }, "children", {
      _key: targetChild._key
    }]));
  }
  return patches;
}
function withRemoteChanges(editor, fn) {
  const prev = editor.isProcessingRemoteChanges;
  editor.isProcessingRemoteChanges = !0, fn(), editor.isProcessingRemoteChanges = prev;
}
function pluginWithoutHistory(editor, fn) {
  const prev = editor.withHistory;
  editor.withHistory = !1, fn(), editor.withHistory = prev;
}
function createPatchesPlugin({
  editorActor,
  relayActor,
  subscriptions
}) {
  let previousValue;
  const applyPatch = createApplyPatch(editorActor.getSnapshot().context);
  return function(editor) {
    previousValue = [...editor.value];
    const {
      apply: apply2
    } = editor;
    let bufferedPatches = [];
    const handleBufferedRemotePatches = () => {
      if (bufferedPatches.length === 0)
        return;
      const patches = bufferedPatches;
      bufferedPatches = [];
      let changed = !1;
      withRemoteChanges(editor, () => {
        Editor.withoutNormalizing(editor, () => {
          withoutPatching(editor, () => {
            pluginWithoutHistory(editor, () => {
              for (const patch of patches)
                try {
                  changed = applyPatch(editor, patch), changed ? debug$1.syncPatch(`(applied) ${JSON.stringify(patch, null, 2)}`) : debug$1.syncPatch(`(ignored) ${JSON.stringify(patch, null, 2)}`);
                } catch (error) {
                  console.error(`Applying patch ${JSON.stringify(patch)} failed due to: ${error instanceof Error ? error.message : error}`);
                }
            });
          });
        }), changed && (editor.normalize(), editor.onChange());
      });
    }, handlePatches = ({
      patches
    }) => {
      const remotePatches = patches.filter((p) => p.origin !== "local");
      remotePatches.length !== 0 && (bufferedPatches = bufferedPatches.concat(remotePatches), handleBufferedRemotePatches());
    };
    return subscriptions.push(() => {
      debug$1.syncPatch("subscribing to remote patches");
      const sub = editorActor.on("patches", handlePatches);
      return () => {
        debug$1.syncPatch("unsubscribing to remote patches"), sub.unsubscribe();
      };
    }), editor.apply = (operation) => {
      let patches = [];
      previousValue = editor.value;
      const editorWasEmpty = isEqualToEmptyEditor(editorActor.getSnapshot().context.initialValue, previousValue, editorActor.getSnapshot().context.schema);
      apply2(operation);
      const editorIsEmpty = isEqualToEmptyEditor(editorActor.getSnapshot().context.initialValue, editor.value, editorActor.getSnapshot().context.schema);
      if (!editor.isPatching)
        return editor;
      switch (editorWasEmpty && !editorIsEmpty && operation.type !== "set_selection" && patches.push(insert(previousValue, "before", [0])), operation.type) {
        case "insert_text":
          patches = [...patches, ...insertTextPatch(editorActor.getSnapshot().context.schema, editor.children, operation, previousValue)];
          break;
        case "remove_text":
          patches = [...patches, ...removeTextPatch(editorActor.getSnapshot().context.schema, editor.children, operation, previousValue)];
          break;
        case "remove_node":
          patches = [...patches, ...removeNodePatch(editorActor.getSnapshot().context.schema, previousValue, operation)];
          break;
        case "split_node":
          patches = [...patches, ...splitNodePatch(editorActor.getSnapshot().context.schema, editor.children, operation, previousValue)];
          break;
        case "insert_node":
          patches = [...patches, ...insertNodePatch(editorActor.getSnapshot().context.schema, editor.children, operation, previousValue)];
          break;
        case "set_node":
          patches = [...patches, ...setNodePatch(editorActor.getSnapshot().context.schema, editor.children, operation)];
          break;
        case "merge_node":
          patches = [...patches, ...mergeNodePatch(editorActor.getSnapshot().context.schema, editor.children, operation, previousValue)];
          break;
        case "move_node":
          patches = [...patches, ...moveNodePatch(editorActor.getSnapshot().context.schema, previousValue, operation)];
          break;
      }
      if (!editorWasEmpty && editorIsEmpty && ["merge_node", "set_node", "remove_text", "remove_node"].includes(operation.type) && (patches = [...patches, unset([])], relayActor.send({
        type: "unset",
        previousValue
      })), editorWasEmpty && patches.length > 0 && (patches = [setIfMissing([], []), ...patches]), patches.length > 0)
        for (const patch of patches)
          editorActor.send({
            type: "internal.patch",
            patch: {
              ...patch,
              origin: "local"
            },
            operationId: editor.undoStepId,
            value: editor.value
          });
      return editor;
    }, editor;
  };
}
function createSchemaPlugin({
  editorActor
}) {
  return function(editor) {
    editor.isTextBlock = (value) => Editor.isEditor(value) ? !1 : isTextBlock(editorActor.getSnapshot().context, value), editor.isTextSpan = (value) => Editor.isEditor(value) ? !1 : isSpan(editorActor.getSnapshot().context, value), editor.isListBlock = (value) => Editor.isEditor(value) ? !1 : isListBlock(editorActor.getSnapshot().context, value), editor.isVoid = (element) => Editor.isEditor(element) ? !1 : editorActor.getSnapshot().context.schema.block.name !== element._type && (editorActor.getSnapshot().context.schema.blockObjects.map((obj) => obj.name).includes(element._type) || editorActor.getSnapshot().context.schema.inlineObjects.map((obj) => obj.name).includes(element._type)), editor.isInline = (element) => Editor.isEditor(element) ? !1 : editorActor.getSnapshot().context.schema.inlineObjects.map((obj) => obj.name).includes(element._type) && "__inline" in element && element.__inline === !0;
    const {
      normalizeNode: normalizeNode2
    } = editor;
    return editor.normalizeNode = (entry) => {
      const [node2, path2] = entry;
      if (node2._type === void 0 && path2.length === 2) {
        debug$1.normalization("Setting span type on text node without a type");
        const span = node2, key = span._key || editorActor.getSnapshot().context.keyGenerator();
        withNormalizeNode(editor, () => {
          Transforms.setNodes(editor, {
            ...span,
            _type: editorActor.getSnapshot().context.schema.span.name,
            _key: key
          }, {
            at: path2
          });
        });
        return;
      }
      if (node2._key === void 0 && (path2.length === 1 || path2.length === 2)) {
        debug$1.normalization("Setting missing key on child node without a key");
        const key = editorActor.getSnapshot().context.keyGenerator();
        withNormalizeNode(editor, () => {
          Transforms.setNodes(editor, {
            _key: key
          }, {
            at: path2
          });
        });
        return;
      }
      withNormalizeNode(editor, () => {
        normalizeNode2(entry);
      });
    }, editor;
  };
}
function createUniqueKeysPlugin(editorActor) {
  const context = editorActor.getSnapshot().context;
  return function(editor) {
    const {
      apply: apply2,
      normalizeNode: normalizeNode2
    } = editor;
    return editor.apply = (operation) => {
      if (editor.isProcessingRemoteChanges) {
        apply2(operation);
        return;
      }
      if (editor.isUndoing || editor.isRedoing) {
        apply2(operation);
        return;
      }
      if (operation.type === "split_node") {
        const _key = operation.properties._key && keyExistsAtPath({
          blockIndexMap: editor.blockIndexMap,
          context: {
            schema: context.schema,
            value: editor.value
          }
        }, operation.path, operation.properties._key) ? void 0 : operation.properties._key;
        apply2({
          ...operation,
          properties: {
            ...operation.properties,
            _key: _key === void 0 ? editorActor.getSnapshot().context.keyGenerator() : _key
          }
        });
        return;
      }
      if (operation.type === "insert_node" && !Editor.isEditor(operation.node)) {
        const _key = operation.node._key && keyExistsAtPath({
          blockIndexMap: editor.blockIndexMap,
          context: {
            schema: context.schema,
            value: editor.value
          }
        }, operation.path, operation.node._key) ? void 0 : operation.node._key;
        apply2({
          ...operation,
          node: {
            ...operation.node,
            _key: _key === void 0 ? editorActor.getSnapshot().context.keyGenerator() : _key
          }
        });
        return;
      }
      if (operation.type === "merge_node") {
        const index = operation.path[operation.path.length - 1], prevPath = Path.previous(operation.path), prevIndex = prevPath[prevPath.length - 1];
        if (operation.path.length !== 1 || prevPath.length !== 1) {
          apply2(operation);
          return;
        }
        const block = editor.value.at(index), previousBlock = editor.value.at(prevIndex);
        if (!block || !previousBlock) {
          apply2(operation);
          return;
        }
        if (!isTextBlock(editorActor.getSnapshot().context, block) || !isTextBlock(editorActor.getSnapshot().context, previousBlock)) {
          apply2(operation);
          return;
        }
        const previousBlockChildKeys = previousBlock.children.map((child) => child._key), previousBlockMarkDefKeys = previousBlock.markDefs?.map((markDef) => markDef._key) ?? [], markDefKeyMap = /* @__PURE__ */ new Map(), adjustedMarkDefs = block.markDefs?.map((markDef) => {
          if (previousBlockMarkDefKeys.includes(markDef._key)) {
            const newKey = editorActor.getSnapshot().context.keyGenerator();
            return markDefKeyMap.set(markDef._key, newKey), {
              ...markDef,
              _key: newKey
            };
          }
          return markDef;
        });
        let childIndex = 0;
        for (const child of block.children) {
          if (isSpan(editorActor.getSnapshot().context, child)) {
            const marks2 = child.marks?.map((mark) => markDefKeyMap.get(mark) || mark) ?? [];
            isEqualMarks(child.marks, marks2) || Transforms.setNodes(editor, {
              marks: marks2
            }, {
              at: [index, childIndex]
            });
          }
          previousBlockChildKeys.includes(child._key) && Transforms.setNodes(editor, {
            _key: editorActor.getSnapshot().context.keyGenerator()
          }, {
            at: [index, childIndex]
          }), childIndex++;
        }
        apply2({
          ...operation,
          properties: {
            ...operation.properties,
            // Make sure the adjusted markDefs are carried along for the merge
            // operation
            markDefs: adjustedMarkDefs
          }
        });
        return;
      }
      apply2(operation);
    }, editor.normalizeNode = (entry) => {
      const [node2, path2] = entry;
      if (Element$2.isElement(node2)) {
        const [parent2] = Editor.parent(editor, path2);
        if (parent2 && Editor.isEditor(parent2)) {
          const blockKeys = /* @__PURE__ */ new Set();
          for (const sibling of parent2.children) {
            if (sibling._key && blockKeys.has(sibling._key)) {
              const _key = editorActor.getSnapshot().context.keyGenerator();
              blockKeys.add(_key), withNormalizeNode(editor, () => {
                Transforms.setNodes(editor, {
                  _key
                }, {
                  at: path2
                });
              });
              return;
            }
            if (!sibling._key) {
              const _key = editorActor.getSnapshot().context.keyGenerator();
              blockKeys.add(_key), withNormalizeNode(editor, () => {
                Transforms.setNodes(editor, {
                  _key
                }, {
                  at: path2
                });
              });
              return;
            }
            blockKeys.add(sibling._key);
          }
        }
      }
      if (Element$2.isElement(node2) && node2._type === editorActor.getSnapshot().context.schema.block.name) {
        if (!node2._key) {
          withNormalizeNode(editor, () => {
            Transforms.setNodes(editor, {
              _key: editorActor.getSnapshot().context.keyGenerator()
            }, {
              at: path2
            });
          });
          return;
        }
        const childKeys = /* @__PURE__ */ new Set();
        for (const [child, childPath] of Node$1.children(editor, path2)) {
          if (child._key && childKeys.has(child._key)) {
            const _key = editorActor.getSnapshot().context.keyGenerator();
            childKeys.add(_key), withNormalizeNode(editor, () => {
              Transforms.setNodes(editor, {
                _key
              }, {
                at: childPath
              });
            });
            return;
          }
          if (!child._key) {
            const _key = editorActor.getSnapshot().context.keyGenerator();
            childKeys.add(_key), withNormalizeNode(editor, () => {
              Transforms.setNodes(editor, {
                _key
              }, {
                at: childPath
              });
            });
            return;
          }
          childKeys.add(child._key);
        }
      }
      withNormalizeNode(editor, () => {
        normalizeNode2(entry);
      });
    }, editor;
  };
}
function keyExistsAtPath(snapshot, path2, key) {
  if (path2.length === 1)
    return snapshot.blockIndexMap.has(key);
  if (path2.length > 2)
    return !1;
  const parentBlockIndex = path2.at(0), parentBlock = parentBlockIndex !== void 0 ? snapshot.context.value.at(parentBlockIndex) : void 0;
  return !parentBlock || !isTextBlock(snapshot.context, parentBlock) ? !1 : parentBlock.children.some((child) => child._key === key);
}
function updateSelectionPlugin({
  editor,
  editorActor
}) {
  const updateSelection = () => {
    if (editor.selection)
      if (editor.selection === editor.lastSlateSelection)
        editorActor.send({
          type: "update selection",
          selection: editor.lastSelection
        });
      else {
        const selection = slateRangeToSelection({
          schema: editorActor.getSnapshot().context.schema,
          editor,
          range: editor.selection
        });
        editor.lastSlateSelection = editor.selection, editor.lastSelection = selection, editorActor.send({
          type: "update selection",
          selection
        });
      }
    else
      editorActor.send({
        type: "update selection",
        selection: null
      });
  }, {
    onChange
  } = editor;
  return editor.onChange = () => {
    onChange(), editorActor.getSnapshot().matches({
      setup: "setting up"
    }) || updateSelection();
  }, editor;
}
function isEditorNode(node2) {
  return typeof node2 == "object" && node2 !== null ? !("_type" in node2) && "children" in node2 && Array.isArray(node2.children) : !1;
}
function isTextBlockNode(context, node2) {
  return isTypedObject(node2) && node2._type === context.schema.block.name;
}
function isSpanNode(context, node2) {
  return typeof node2 != "object" || node2 === null || "children" in node2 ? !1 : "_type" in node2 ? node2._type === context.schema.span.name : "text" in node2;
}
function isPartialSpanNode(context, node2) {
  return !(typeof node2 != "object" || node2 === null || !("text" in node2) || typeof node2.text != "string" || "_type" in node2 && node2._type !== context.schema.span.name);
}
function isObjectNode(context, node2) {
  return !isEditorNode(node2) && !isTextBlockNode(context, node2) && !isSpanNode(context, node2) && !isPartialSpanNode(context, node2);
}
function getBlock(root, path2) {
  const index = path2.at(0);
  if (!(index === void 0 || path2.length !== 1))
    return root.children.at(index);
}
function getNode(context, root, path2) {
  if (path2.length === 0)
    return root;
  if (path2.length === 1)
    return getBlock(root, path2);
  if (path2.length === 2) {
    const block = getBlock(root, path2.slice(0, 1));
    return !block || !isTextBlockNode(context, block) ? void 0 : block.children.at(path2[1]) || void 0;
  }
}
function getSpan(context, root, path2) {
  const node2 = getNode(context, root, path2);
  if (node2 && isSpanNode(context, node2))
    return node2;
}
function getParent(context, root, path2) {
  if (path2.length === 0)
    return;
  const parentPath = path2.slice(0, -1);
  if (parentPath.length === 0)
    return root;
  const blockIndex = parentPath.at(0);
  if (blockIndex === void 0 || parentPath.length !== 1)
    return;
  const block = root.children.at(blockIndex);
  if (block && isTextBlockNode(context, block))
    return block;
}
function applyOperationToPortableText(context, value, operation) {
  const root = {
    children: value
  };
  try {
    return applyOperationToPortableTextImmutable(context, root, operation).children;
  } catch (e) {
    return console.error(e), value;
  }
}
function applyOperationToPortableTextImmutable(context, root, operation) {
  switch (operation.type) {
    case "insert_node": {
      const {
        path: path2,
        node: insertedNode
      } = operation, parent2 = getParent(context, root, path2), index = path2[path2.length - 1];
      if (!parent2 || index > parent2.children.length)
        return root;
      if (path2.length === 1) {
        if (isTextBlockNode(context, insertedNode)) {
          const newBlock = {
            ...insertedNode,
            children: insertedNode.children.map((child) => "__inline" in child ? {
              _key: child._key,
              _type: child._type,
              ..."value" in child && typeof child.value == "object" ? child.value : {}
            } : child)
          };
          return {
            ...root,
            children: insertChildren(root.children, index, newBlock)
          };
        }
        if (Element$2.isElement(insertedNode) && !("__inline" in insertedNode)) {
          const newBlock = {
            _key: insertedNode._key,
            _type: insertedNode._type,
            ..."value" in insertedNode && typeof insertedNode.value == "object" ? insertedNode.value : {}
          };
          return {
            ...root,
            children: insertChildren(root.children, index, newBlock)
          };
        }
      }
      if (path2.length === 2) {
        const blockIndex = path2[0];
        if (!isTextBlockNode(context, parent2))
          return root;
        let newChild;
        if (isPartialSpanNode(context, insertedNode))
          newChild = insertedNode;
        else if ("__inline" in insertedNode)
          newChild = {
            _key: insertedNode._key,
            _type: insertedNode._type,
            ..."value" in insertedNode && typeof insertedNode.value == "object" ? insertedNode.value : {}
          };
        else
          return root;
        return updateTextBlockAtIndex(context, root, blockIndex, (block) => ({
          ...block,
          children: insertChildren(block.children, index, newChild)
        }));
      }
      return root;
    }
    case "insert_text": {
      const {
        path: path2,
        offset,
        text
      } = operation;
      if (text.length === 0)
        return root;
      const span = getSpan(context, root, path2);
      if (!span)
        return root;
      const blockIndex = path2[0], childIndex = path2[1], before2 = span.text.slice(0, offset), after2 = span.text.slice(offset), newSpan = {
        ...span,
        text: before2 + text + after2
      };
      return updateTextBlockAtIndex(context, root, blockIndex, (block) => ({
        ...block,
        children: replaceChild(block.children, childIndex, newSpan)
      }));
    }
    case "merge_node": {
      const {
        path: path2
      } = operation;
      if (path2.at(-1) === 0)
        return root;
      const node2 = getNode(context, root, path2), prevPath = Path.previous(path2), prev = getNode(context, root, prevPath), parent2 = getParent(context, root, path2);
      if (!node2 || !prev || !parent2)
        return root;
      const index = path2[path2.length - 1];
      if (isPartialSpanNode(context, node2) && isPartialSpanNode(context, prev)) {
        const blockIndex = path2[0], newPrev = {
          ...prev,
          text: prev.text + node2.text
        };
        return updateTextBlockAtIndex(context, root, blockIndex, (block) => {
          const newChildren = replaceChild(block.children, index - 1, newPrev);
          return {
            ...block,
            children: removeChildren(newChildren, index)
          };
        });
      }
      if (isTextBlockNode(context, node2) && isTextBlockNode(context, prev)) {
        const newPrev = {
          ...prev,
          children: [...prev.children, ...node2.children]
        }, newChildren = replaceChild(root.children, index - 1, newPrev);
        return {
          ...root,
          children: removeChildren(newChildren, index)
        };
      }
      return root;
    }
    case "move_node": {
      const {
        path: path2,
        newPath
      } = operation;
      if (Path.isAncestor(path2, newPath))
        return root;
      const node2 = getNode(context, root, path2), parent2 = getParent(context, root, path2), index = path2[path2.length - 1];
      if (!node2 || !parent2)
        return root;
      let newRoot;
      if (path2.length === 1)
        newRoot = {
          ...root,
          children: removeChildren(root.children, index)
        };
      else if (path2.length === 2) {
        const blockIndex = path2[0];
        newRoot = updateTextBlockAtIndex(context, root, blockIndex, (block) => ({
          ...block,
          children: removeChildren(block.children, index)
        }));
      } else
        return root;
      const truePath = Path.transform(path2, operation), newIndex = truePath[truePath.length - 1];
      if (truePath.length === 1)
        return {
          ...newRoot,
          children: insertChildren(newRoot.children, newIndex, node2)
        };
      if (truePath.length === 2) {
        const newBlockIndex = truePath[0], newParent = newRoot.children[newBlockIndex];
        return !newParent || !isTextBlockNode(context, newParent) ? root : updateTextBlockAtIndex(context, newRoot, newBlockIndex, (block) => ({
          ...block,
          children: insertChildren(block.children, newIndex, node2)
        }));
      }
      return root;
    }
    case "remove_node": {
      const {
        path: path2
      } = operation, index = path2[path2.length - 1];
      if (!getParent(context, root, path2))
        return root;
      if (path2.length === 1)
        return {
          ...root,
          children: removeChildren(root.children, index)
        };
      if (path2.length === 2) {
        const blockIndex = path2[0];
        return updateTextBlockAtIndex(context, root, blockIndex, (block) => ({
          ...block,
          children: removeChildren(block.children, index)
        }));
      }
      return root;
    }
    case "remove_text": {
      const {
        path: path2,
        offset,
        text
      } = operation;
      if (text.length === 0)
        return root;
      const span = getSpan(context, root, path2);
      if (!span)
        return root;
      const blockIndex = path2[0], childIndex = path2[1], before2 = span.text.slice(0, offset), after2 = span.text.slice(offset + text.length), newSpan = {
        ...span,
        text: before2 + after2
      };
      return updateTextBlockAtIndex(context, root, blockIndex, (block) => ({
        ...block,
        children: replaceChild(block.children, childIndex, newSpan)
      }));
    }
    case "set_node": {
      const {
        path: path2,
        properties,
        newProperties
      } = operation, node2 = getNode(context, root, path2);
      if (!node2 || isEditorNode(node2))
        return root;
      if (isObjectNode(context, node2)) {
        const valueBefore = "value" in properties && typeof properties.value == "object" ? properties.value : {}, valueAfter = "value" in newProperties && typeof newProperties.value == "object" ? newProperties.value : {}, newNode = {
          ...node2
        };
        for (const key in newProperties) {
          if (key === "value")
            continue;
          const value = newProperties[key];
          value == null ? delete newNode[key] : newNode[key] = value;
        }
        for (const key in properties)
          key !== "value" && (newProperties.hasOwnProperty(key) || delete newNode[key]);
        for (const key in valueAfter) {
          const value = valueAfter[key];
          value == null ? delete newNode[key] : newNode[key] = value;
        }
        for (const key in valueBefore)
          valueAfter.hasOwnProperty(key) || delete newNode[key];
        return path2.length === 1 ? {
          ...root,
          children: replaceChild(root.children, path2[0], newNode)
        } : path2.length === 2 ? updateTextBlockAtIndex(context, root, path2[0], (block) => ({
          ...block,
          children: replaceChild(block.children, path2[1], newNode)
        })) : root;
      }
      if (isTextBlockNode(context, node2)) {
        const newNode = {
          ...node2
        };
        for (const key in newProperties) {
          if (key === "children" || key === "text")
            continue;
          const value = newProperties[key];
          value == null ? delete newNode[key] : newNode[key] = value;
        }
        for (const key in properties)
          newProperties.hasOwnProperty(key) || delete newNode[key];
        return {
          ...root,
          children: replaceChild(root.children, path2[0], newNode)
        };
      }
      if (isPartialSpanNode(context, node2)) {
        const newNode = {
          ...node2
        };
        for (const key in newProperties) {
          if (key === "text")
            continue;
          const value = newProperties[key];
          value == null ? delete newNode[key] : newNode[key] = value;
        }
        for (const key in properties)
          newProperties.hasOwnProperty(key) || delete newNode[key];
        return updateTextBlockAtIndex(context, root, path2[0], (block) => ({
          ...block,
          children: replaceChild(block.children, path2[1], newNode)
        }));
      }
      return root;
    }
    case "split_node": {
      const {
        path: path2,
        position,
        properties
      } = operation;
      if (path2.length === 0)
        return root;
      const parent2 = getParent(context, root, path2), index = path2[path2.length - 1];
      if (!parent2)
        return root;
      if (isEditorNode(parent2)) {
        const block = getBlock(root, path2);
        if (!block || !isTextBlockNode(context, block))
          return root;
        const before2 = block.children.slice(0, position), after2 = block.children.slice(position), updatedTextBlockNode = {
          ...block,
          children: before2
        }, newTextBlockNode = {
          ...properties,
          children: after2,
          _type: context.schema.block.name
        };
        return {
          ...root,
          children: insertChildren(replaceChild(root.children, index, updatedTextBlockNode), index + 1, newTextBlockNode)
        };
      }
      if (isTextBlockNode(context, parent2)) {
        const node2 = getNode(context, root, path2);
        if (!node2 || !isSpanNode(context, node2))
          return root;
        const blockIndex = path2[0], before2 = node2.text.slice(0, position), after2 = node2.text.slice(position), updatedSpanNode = {
          ...node2,
          text: before2
        }, newSpanNode = {
          ...properties,
          text: after2
        };
        return updateTextBlockAtIndex(context, root, blockIndex, (block) => ({
          ...block,
          children: insertChildren(replaceChild(block.children, index, updatedSpanNode), index + 1, newSpanNode)
        }));
      }
      return root;
    }
  }
}
function insertChildren(children, index, ...nodes2) {
  return [...children.slice(0, index), ...nodes2, ...children.slice(index)];
}
function removeChildren(children, index, count = 1) {
  return [...children.slice(0, index), ...children.slice(index + count)];
}
function replaceChild(children, index, newChild) {
  return [...children.slice(0, index), newChild, ...children.slice(index + 1)];
}
function updateTextBlockAtIndex(context, root, blockIndex, updater) {
  const block = root.children.at(blockIndex);
  if (!block || !isTextBlockNode(context, block))
    return root;
  const newBlock = updater(block);
  return {
    ...root,
    children: replaceChild(root.children, blockIndex, newBlock)
  };
}
function updateValuePlugin(context, editor) {
  const {
    apply: apply2
  } = editor;
  return editor.apply = (operation) => {
    if (editor.isNormalizingNode && debug$1.normalization(`(slate operation)
${JSON.stringify(operation, null, 2)}`), operation.type === "set_selection") {
      apply2(operation);
      return;
    }
    if (editor.value = applyOperationToPortableText(context, editor.value, operation), operation.type === "insert_text" || operation.type === "remove_text") {
      apply2(operation);
      return;
    }
    buildIndexMaps({
      schema: context.schema,
      value: editor.value
    }, {
      blockIndexMap: editor.blockIndexMap,
      listIndexMap: editor.listIndexMap
    }), apply2(operation);
  }, editor;
}
const plugins = (editor, options) => {
  const e = editor, {
    editorActor,
    relayActor
  } = options, uniqueKeysPlugin = createUniqueKeysPlugin(editorActor), schemaPlugin = createSchemaPlugin({
    editorActor
  }), patchesPlugin = createPatchesPlugin({
    editorActor,
    relayActor,
    subscriptions: options.subscriptions
  }), historyPlugin = createHistoryPlugin({
    editorActor,
    subscriptions: options.subscriptions
  }), normalizationPlugin = createNormalizationPlugin(editorActor);
  return createBehaviorApiPlugin(editorActor)(schemaPlugin(uniqueKeysPlugin(normalizationPlugin(historyPlugin(patchesPlugin(updateValuePlugin(editorActor.getSnapshot().context, updateSelectionPlugin({
    editorActor,
    editor: e
  }))))))));
};
function createSlateEditor(config) {
  debug$1.setup("creating new slate editor instance");
  const context = config.editorActor.getSnapshot().context, placeholderBlock = createPlaceholderBlock(context), editor = createEditor({
    schema: context.schema,
    keyGenerator: context.keyGenerator
  });
  editor.decoratedRanges = [], editor.decoratorState = {}, editor.blockIndexMap = /* @__PURE__ */ new Map(), editor.history = {
    undos: [],
    redos: []
  }, editor.lastSelection = null, editor.lastSlateSelection = null, editor.listIndexMap = /* @__PURE__ */ new Map(), editor.remotePatches = [], editor.undoStepId = void 0, editor.value = [placeholderBlock], editor.isDeferringMutations = !1, editor.isNormalizingNode = !1, editor.isPatching = !0, editor.isPerformingBehaviorOperation = !1, editor.isProcessingRemoteChanges = !1, editor.isRedoing = !1, editor.isUndoing = !1, editor.withHistory = !0;
  const instance = plugins(withReact(editor), {
    editorActor: config.editorActor,
    relayActor: config.relayActor,
    subscriptions: config.subscriptions
  });
  return buildIndexMaps({
    schema: context.schema,
    value: instance.value
  }, {
    blockIndexMap: instance.blockIndexMap,
    listIndexMap: instance.listIndexMap
  }), {
    instance,
    initialValue: [placeholderBlock]
  };
}
function createEditorDom(sendBack, slateEditor) {
  return {
    getBlockNodes: (snapshot) => getBlockNodes(slateEditor, snapshot),
    getChildNodes: (snapshot) => getChildNodes(slateEditor, snapshot),
    getEditorElement: () => getEditorElement(slateEditor),
    getSelectionRect: (snapshot) => getSelectionRect(snapshot),
    getStartBlockElement: (snapshot) => getStartBlockElement(slateEditor, snapshot),
    getEndBlockElement: (snapshot) => getEndBlockElement(slateEditor, snapshot),
    setDragGhost: ({
      event,
      ghost
    }) => setDragGhost({
      sendBack,
      event,
      ghost
    })
  };
}
function getBlockNodes(slateEditor, snapshot) {
  if (!snapshot.context.selection)
    return [];
  const range2 = toSlateRange(snapshot);
  if (!range2)
    return [];
  try {
    return Array.from(Editor.nodes(slateEditor, {
      at: range2,
      mode: "highest",
      match: (n2) => !Editor.isEditor(n2)
    })).map(([blockNode]) => DOMEditor.toDOMNode(slateEditor, blockNode));
  } catch {
    return [];
  }
}
function getChildNodes(slateEditor, snapshot) {
  if (!snapshot.context.selection)
    return [];
  const range2 = toSlateRange(snapshot);
  if (!range2)
    return [];
  try {
    return Array.from(Editor.nodes(slateEditor, {
      at: range2,
      mode: "lowest",
      match: (n2) => !Editor.isEditor(n2)
    })).map(([childNode]) => DOMEditor.toDOMNode(slateEditor, childNode));
  } catch {
    return [];
  }
}
function getEditorElement(slateEditor) {
  try {
    return DOMEditor.toDOMNode(slateEditor, slateEditor);
  } catch {
    return;
  }
}
function getSelectionRect(snapshot) {
  if (!snapshot.context.selection)
    return null;
  try {
    const selection = window.getSelection();
    return selection ? selection.getRangeAt(0).getBoundingClientRect() : null;
  } catch {
    return null;
  }
}
function getStartBlockElement(slateEditor, snapshot) {
  const startBlock = getSelectionStartBlock(snapshot);
  if (!startBlock)
    return null;
  const startBlockNode = getBlockNodes(slateEditor, {
    ...snapshot,
    context: {
      ...snapshot.context,
      selection: {
        anchor: {
          path: startBlock.path,
          offset: 0
        },
        focus: {
          path: startBlock.path,
          offset: 0
        }
      }
    }
  })?.at(0);
  return startBlockNode && startBlockNode instanceof Element ? startBlockNode : null;
}
function getEndBlockElement(slateEditor, snapshot) {
  const endBlock = getSelectionEndBlock(snapshot);
  if (!endBlock)
    return null;
  const endBlockNode = getBlockNodes(slateEditor, {
    ...snapshot,
    context: {
      ...snapshot.context,
      selection: {
        anchor: {
          path: endBlock.path,
          offset: 0
        },
        focus: {
          path: endBlock.path,
          offset: 0
        }
      }
    }
  })?.at(0);
  return endBlockNode && endBlockNode instanceof Element ? endBlockNode : null;
}
function setDragGhost({
  sendBack,
  event,
  ghost
}) {
  event.originEvent.dataTransfer.setDragImage(ghost.element, ghost.x, ghost.y), sendBack({
    type: "set drag ghost",
    ghost: ghost.element
  });
}
const addAnnotationOnCollapsedSelection = defineBehavior({
  on: "annotation.add",
  guard: ({
    snapshot,
    event
  }) => {
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    };
    if (!isSelectionCollapsed$1(adjustedSnapshot))
      return !1;
    const caretWordSelection = getCaretWordSelection(adjustedSnapshot);
    return !caretWordSelection || !isSelectionExpanded({
      context: {
        ...adjustedSnapshot.context,
        selection: caretWordSelection
      }
    }) ? !1 : {
      caretWordSelection
    };
  },
  actions: [({
    event
  }, {
    caretWordSelection
  }) => [raise({
    type: "select",
    at: caretWordSelection
  }), raise({
    type: "annotation.add",
    annotation: event.annotation
  })]]
}), preventOverlappingAnnotations = defineBehavior({
  // Given an `annotation.add` event
  on: "annotation.add",
  // When the annotation is active in the selection
  guard: ({
    snapshot,
    event
  }) => {
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    };
    return isActiveAnnotation(event.annotation.name, {
      mode: "partial"
    })(adjustedSnapshot);
  },
  // Then the existing annotation is removed
  actions: [({
    event
  }) => [raise({
    type: "annotation.remove",
    annotation: event.annotation,
    at: event.at
  }), raise(event)]]
}), stripAnnotationsOnFullSpanDeletion = defineBehavior({
  on: "delete",
  guard: ({
    snapshot,
    event
  }) => {
    const effectiveSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: event.at ?? snapshot.context.selection
      }
    };
    if (!isSelectionExpanded(effectiveSnapshot))
      return !1;
    const startChild = getSelectionStartChild(effectiveSnapshot), startPoint = getSelectionStartPoint(effectiveSnapshot), endChild = getSelectionEndChild(effectiveSnapshot), endPoint = getSelectionEndPoint(effectiveSnapshot);
    if (!startChild || !endChild || !startPoint || !endPoint || startChild.path[2]._key !== endChild.path[2]._key || !isSpan(snapshot.context, startChild.node) || !(startPoint.offset === 0 && endPoint.offset === startChild.node.text.length))
      return !1;
    const decorators = snapshot.context.schema.decorators.map((decorator) => decorator.name), marks2 = startChild.node.marks ?? [];
    if (!marks2.some((mark) => !decorators.includes(mark)))
      return !1;
    const previousSpan = getPreviousSpan(effectiveSnapshot), nextSpan = getNextSpan(effectiveSnapshot), previousSpanHasSameAnnotation = previousSpan ? previousSpan.node.marks?.some((mark) => !decorators.includes(mark) && marks2.includes(mark)) : !1, nextSpanHasSameAnnotation = nextSpan ? nextSpan.node.marks?.some((mark) => !decorators.includes(mark) && marks2.includes(mark)) : !1;
    if (previousSpanHasSameAnnotation || nextSpanHasSameAnnotation)
      return !1;
    const activeDecorators = getActiveDecorators(effectiveSnapshot);
    return {
      spanPath: startChild.path,
      activeDecorators
    };
  },
  actions: [({
    event
  }, {
    spanPath,
    activeDecorators
  }) => [raise({
    type: "child.set",
    at: spanPath,
    props: {
      marks: activeDecorators
    }
  }), forward(event)]]
}), coreAnnotationBehaviors = [addAnnotationOnCollapsedSelection, preventOverlappingAnnotations, stripAnnotationsOnFullSpanDeletion], defaultKeyboardShortcuts = {
  arrowDown: createKeyboardShortcut({
    default: [{
      key: "ArrowDown",
      alt: !1,
      ctrl: !1,
      meta: !1,
      shift: !1
    }]
  }),
  arrowUp: createKeyboardShortcut({
    default: [{
      key: "ArrowUp",
      alt: !1,
      ctrl: !1,
      meta: !1,
      shift: !1
    }]
  }),
  backspace: createKeyboardShortcut({
    default: [{
      key: "Backspace",
      alt: !1,
      ctrl: !1,
      meta: !1,
      shift: !1
    }]
  }),
  break: createKeyboardShortcut({
    default: [{
      key: "Enter",
      shift: !1
    }]
  }),
  lineBreak: createKeyboardShortcut({
    default: [{
      key: "Enter",
      shift: !0
    }]
  }),
  decorators: {
    strong: bold,
    em: italic,
    underline,
    code
  },
  delete: createKeyboardShortcut({
    default: [{
      key: "Delete",
      alt: !1,
      ctrl: !1,
      meta: !1,
      shift: !1
    }]
  }),
  deleteWord: {
    backward: createKeyboardShortcut({
      default: [{
        key: "Backspace",
        alt: !1,
        ctrl: !0,
        meta: !1
        // shift is optional
      }],
      apple: [{
        key: "Backspace",
        alt: !0,
        ctrl: !1,
        meta: !1
        // shift is optional
      }]
    }),
    forward: createKeyboardShortcut({
      default: [{
        key: "Delete",
        alt: !1,
        ctrl: !0,
        meta: !1
        // shift is optional
      }],
      apple: [{
        key: "Delete",
        alt: !0,
        ctrl: !1,
        meta: !1
        // shift is optional
      }]
    })
  },
  history: {
    undo,
    redo
  },
  tab: createKeyboardShortcut({
    default: [{
      key: "Tab",
      alt: !1,
      ctrl: !1,
      meta: !1,
      shift: !1
    }]
  }),
  shiftTab: createKeyboardShortcut({
    default: [{
      key: "Tab",
      alt: !1,
      ctrl: !1,
      meta: !1,
      shift: !0
    }]
  })
}, arrowDownOnLonelyBlockObject = defineBehavior({
  on: "keyboard.keydown",
  guard: ({
    snapshot,
    event
  }) => {
    if (!defaultKeyboardShortcuts.arrowDown.guard(event.originEvent) || !isSelectionCollapsed$1(snapshot))
      return !1;
    const focusBlockObject = getFocusBlockObject(snapshot), nextBlock = getNextBlock(snapshot);
    return focusBlockObject && !nextBlock;
  },
  actions: [({
    snapshot
  }) => [raise({
    type: "insert.block",
    block: {
      _type: snapshot.context.schema.block.name
    },
    placement: "after"
  })]]
}), arrowUpOnLonelyBlockObject = defineBehavior({
  on: "keyboard.keydown",
  guard: ({
    snapshot,
    event
  }) => {
    if (!defaultKeyboardShortcuts.arrowUp.guard(event.originEvent) || !isSelectionCollapsed$1(snapshot))
      return !1;
    const focusBlockObject = getFocusBlockObject(snapshot), previousBlock = getPreviousBlock(snapshot);
    return focusBlockObject && !previousBlock;
  },
  actions: [({
    snapshot
  }) => [raise({
    type: "insert.block",
    block: {
      _type: snapshot.context.schema.block.name
    },
    placement: "before"
  })]]
}), breakingBlockObject = defineBehavior({
  on: "insert.break",
  guard: ({
    snapshot
  }) => {
    const focusBlockObject = getFocusBlockObject(snapshot);
    return isSelectionCollapsed$1(snapshot) && focusBlockObject !== void 0;
  },
  actions: [({
    snapshot
  }) => [raise({
    type: "insert.block",
    block: {
      _type: snapshot.context.schema.block.name
    },
    placement: "after"
  })]]
}), clickingAboveLonelyBlockObject = defineBehavior({
  on: "mouse.click",
  guard: ({
    snapshot,
    event
  }) => {
    if (snapshot.context.readOnly || snapshot.context.selection && !isSelectionCollapsed$1(snapshot))
      return !1;
    const focusBlockObject = getFocusBlockObject({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: event.position.selection
      }
    }), previousBlock = getPreviousBlock({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: event.position.selection
      }
    });
    return event.position.isEditor && event.position.block === "start" && focusBlockObject && !previousBlock;
  },
  actions: [({
    snapshot,
    event
  }) => [raise({
    type: "select",
    at: event.position.selection
  }), raise({
    type: "insert.block",
    block: {
      _type: snapshot.context.schema.block.name
    },
    placement: "before",
    select: "start"
  })]]
}), clickingBelowLonelyBlockObject = defineBehavior({
  on: "mouse.click",
  guard: ({
    snapshot,
    event
  }) => {
    if (snapshot.context.readOnly || snapshot.context.selection && !isSelectionCollapsed$1(snapshot))
      return !1;
    const focusBlockObject = getFocusBlockObject({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: event.position.selection
      }
    }), nextBlock = getNextBlock({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: event.position.selection
      }
    });
    return event.position.isEditor && event.position.block === "end" && focusBlockObject && !nextBlock;
  },
  actions: [({
    snapshot,
    event
  }) => [raise({
    type: "select",
    at: event.position.selection
  }), raise({
    type: "insert.block",
    block: {
      _type: snapshot.context.schema.block.name
    },
    placement: "after",
    select: "start"
  })]]
}), deletingEmptyTextBlockAfterBlockObject = defineBehavior({
  on: "delete.backward",
  guard: ({
    snapshot
  }) => {
    const focusTextBlock = getFocusTextBlock(snapshot), selectionCollapsed = isSelectionCollapsed$1(snapshot), previousBlock = getPreviousBlock(snapshot);
    return !focusTextBlock || !selectionCollapsed || !previousBlock || isListBlock(snapshot.context, focusTextBlock.node) ? !1 : isEmptyTextBlock(snapshot.context, focusTextBlock.node) && !isTextBlock(snapshot.context, previousBlock.node) ? {
      focusTextBlock,
      previousBlock
    } : !1;
  },
  actions: [(_, {
    focusTextBlock,
    previousBlock
  }) => [raise({
    type: "delete.block",
    at: focusTextBlock.path
  }), raise({
    type: "select",
    at: {
      anchor: {
        path: previousBlock.path,
        offset: 0
      },
      focus: {
        path: previousBlock.path,
        offset: 0
      }
    }
  })]]
}), deletingEmptyTextBlockBeforeBlockObject = defineBehavior({
  on: "delete.forward",
  guard: ({
    snapshot
  }) => {
    const focusTextBlock = getFocusTextBlock(snapshot), selectionCollapsed = isSelectionCollapsed$1(snapshot), nextBlock = getNextBlock(snapshot);
    return !focusTextBlock || !selectionCollapsed || !nextBlock ? !1 : isEmptyTextBlock(snapshot.context, focusTextBlock.node) && !isTextBlock(snapshot.context, nextBlock.node) ? {
      focusTextBlock,
      nextBlock
    } : !1;
  },
  actions: [(_, {
    focusTextBlock,
    nextBlock
  }) => [raise({
    type: "delete.block",
    at: focusTextBlock.path
  }), raise({
    type: "select",
    at: {
      anchor: {
        path: nextBlock.path,
        offset: 0
      },
      focus: {
        path: nextBlock.path,
        offset: 0
      }
    }
  })]]
}), coreBlockObjectBehaviors = {
  arrowDownOnLonelyBlockObject,
  arrowUpOnLonelyBlockObject,
  breakingBlockObject,
  clickingAboveLonelyBlockObject,
  clickingBelowLonelyBlockObject,
  deletingEmptyTextBlockAfterBlockObject,
  deletingEmptyTextBlockBeforeBlockObject
}, coreDecoratorBehaviors = {
  strongShortcut: defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => defaultKeyboardShortcuts.decorators.strong.guard(event.originEvent) && snapshot.context.schema.decorators.some((decorator) => decorator.name === "strong"),
    actions: [() => [raise({
      type: "decorator.toggle",
      decorator: "strong"
    })]]
  }),
  emShortcut: defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => defaultKeyboardShortcuts.decorators.em.guard(event.originEvent) && snapshot.context.schema.decorators.some((decorator) => decorator.name === "em"),
    actions: [() => [raise({
      type: "decorator.toggle",
      decorator: "em"
    })]]
  }),
  underlineShortcut: defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => defaultKeyboardShortcuts.decorators.underline.guard(event.originEvent) && snapshot.context.schema.decorators.some((decorator) => decorator.name === "underline"),
    actions: [() => [raise({
      type: "decorator.toggle",
      decorator: "underline"
    })]]
  }),
  codeShortcut: defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => defaultKeyboardShortcuts.decorators.code.guard(event.originEvent) && snapshot.context.schema.decorators.some((decorator) => decorator.name === "code"),
    actions: [() => [raise({
      type: "decorator.toggle",
      decorator: "code"
    })]]
  })
};
function getCompoundClientRect(nodes2) {
  if (nodes2.length === 0)
    return new DOMRect(0, 0, 0, 0);
  const elements = nodes2.filter((node2) => node2 instanceof Element), firstRect = elements.at(0)?.getBoundingClientRect();
  if (!firstRect)
    return new DOMRect(0, 0, 0, 0);
  let left = firstRect.left, top = firstRect.top, right = firstRect.right, bottom = firstRect.bottom;
  for (let i = 1; i < elements.length; i++) {
    const rect = elements[i].getBoundingClientRect();
    left = Math.min(left, rect.left), top = Math.min(top, rect.top), right = Math.max(right, rect.right), bottom = Math.max(bottom, rect.bottom);
  }
  return new DOMRect(left, top, right - left, bottom - top);
}
const coreDndBehaviors = [
  /**
   * Core Behavior that:
   * 1. Calculates and selects a "drag selection"
   * 2. Constructs and sets a drag ghost element
   * 3. Forwards the dragstart event
   */
  defineBehavior({
    on: "drag.dragstart",
    guard: ({
      snapshot,
      dom,
      event
    }) => {
      const dragSelection = getDragSelection({
        snapshot,
        eventSelection: event.position.selection
      }), selectingEntireBlocks = isSelectingEntireBlocks({
        ...snapshot,
        context: {
          ...snapshot.context,
          selection: dragSelection
        }
      }), draggedDomNodes = {
        blockNodes: dom.getBlockNodes({
          ...snapshot,
          context: {
            ...snapshot.context,
            selection: dragSelection
          }
        }),
        childNodes: dom.getChildNodes({
          ...snapshot,
          context: {
            ...snapshot.context,
            selection: dragSelection
          }
        })
      };
      return {
        dragSelection,
        draggedDomNodes,
        selectingEntireBlocks
      };
    },
    actions: [({
      dom,
      event
    }, {
      dragSelection,
      draggedDomNodes,
      selectingEntireBlocks
    }) => {
      const dragGhost = document.createElement("div");
      if (selectingEntireBlocks) {
        const clonedBlockNodes = draggedDomNodes.blockNodes.map((node2) => node2.cloneNode(!0));
        for (const block of clonedBlockNodes)
          block instanceof HTMLElement && (block.style.position = "relative"), dragGhost.appendChild(block);
        const customGhost = dragGhost.querySelector("[data-pt-drag-ghost-element]");
        if (customGhost && dragGhost.replaceChildren(customGhost), dragGhost.setAttribute("data-dragged", ""), dragGhost.style.position = "absolute", dragGhost.style.left = "-99999px", dragGhost.style.boxSizing = "border-box", document.body.appendChild(dragGhost), customGhost) {
          const customGhostRect = customGhost.getBoundingClientRect(), x = event.originEvent.clientX - customGhostRect.left, y = event.originEvent.clientY - customGhostRect.top;
          return dragGhost.style.width = `${customGhostRect.width}px`, dragGhost.style.height = `${customGhostRect.height}px`, [raise({
            type: "select",
            at: dragSelection
          }), effect(() => {
            dom.setDragGhost({
              event,
              ghost: {
                element: dragGhost,
                x,
                y
              }
            });
          }), forward(event)];
        } else {
          const blocksDomRect = getCompoundClientRect(draggedDomNodes.blockNodes), x = event.originEvent.clientX - blocksDomRect.left, y = event.originEvent.clientY - blocksDomRect.top;
          return dragGhost.style.width = `${blocksDomRect.width}px`, dragGhost.style.height = `${blocksDomRect.height}px`, [raise({
            type: "select",
            at: dragSelection
          }), effect(() => {
            dom.setDragGhost({
              event,
              ghost: {
                element: dragGhost,
                x,
                y
              }
            });
          }), forward(event)];
        }
      } else {
        const clonedChildNodes = draggedDomNodes.childNodes.map((node2) => node2.cloneNode(!0));
        for (const child of clonedChildNodes)
          dragGhost.appendChild(child);
        dragGhost.style.position = "absolute", dragGhost.style.left = "-99999px", dragGhost.style.boxSizing = "border-box", document.body.appendChild(dragGhost);
        const childrenDomRect = getCompoundClientRect(draggedDomNodes.childNodes), x = event.originEvent.clientX - childrenDomRect.left, y = event.originEvent.clientY - childrenDomRect.top;
        return dragGhost.style.width = `${childrenDomRect.width}px`, dragGhost.style.height = `${childrenDomRect.height}px`, [raise({
          type: "select",
          at: dragSelection
        }), effect(() => {
          dom.setDragGhost({
            event,
            ghost: {
              element: dragGhost,
              x,
              y
            }
          });
        }), forward(event)];
      }
    }]
  }),
  /**
   * When dragging over the drag origin, we don't want to show the caret in the
   * text.
   */
  defineBehavior({
    on: "drag.dragover",
    guard: ({
      snapshot,
      event
    }) => {
      const dragOrigin = event.dragOrigin;
      return dragOrigin ? isOverlappingSelection(event.position.selection)({
        ...snapshot,
        context: {
          ...snapshot.context,
          selection: dragOrigin.selection
        }
      }) : !1;
    },
    actions: []
  }),
  /**
   * If the drop position overlaps the drag origin, then the event should be
   * cancelled.
   */
  defineBehavior({
    on: "drag.drop",
    guard: ({
      snapshot,
      event
    }) => {
      const dragOrigin = event.dragOrigin, dropPosition = event.position.selection;
      return dragOrigin ? isOverlappingSelection(dropPosition)({
        ...snapshot,
        context: {
          ...snapshot.context,
          selection: dragOrigin.selection
        }
      }) : !1;
    },
    actions: []
  }),
  /**
   * If we drop and have access to a drag origin, then we can deserialize
   * without creating a new selection.
   */
  defineBehavior({
    on: "drag.drop",
    guard: ({
      event
    }) => event.dragOrigin !== void 0,
    actions: [({
      event
    }) => [raise({
      type: "deserialize",
      originEvent: event
    })]]
  }),
  /**
   * Otherwise, we should to create a new selection.
   */
  defineBehavior({
    on: "drag.drop",
    actions: [({
      event
    }) => [raise({
      type: "select",
      at: event.position.selection
    }), raise({
      type: "deserialize",
      originEvent: event
    })]]
  }),
  /**
   * Core Behavior that uses the drag origin to mimic a move operation during
   * internal dragging.
   */
  defineBehavior({
    on: "deserialization.success",
    guard: ({
      snapshot,
      event
    }) => {
      if (event.originEvent.type !== "drag.drop" || event.originEvent.dragOrigin === void 0)
        return !1;
      const dragOrigin = event.originEvent.dragOrigin, dragSelection = getDragSelection({
        eventSelection: dragOrigin.selection,
        snapshot
      }), dropPosition = event.originEvent.position.selection, droppingOnDragOrigin = dragOrigin ? isOverlappingSelection(dropPosition)({
        ...snapshot,
        context: {
          ...snapshot.context,
          selection: dragSelection
        }
      }) : !1, draggingEntireBlocks = isSelectingEntireBlocks({
        ...snapshot,
        context: {
          ...snapshot.context,
          selection: dragSelection
        }
      }), draggedBlocks = getSelectedBlocks({
        ...snapshot,
        context: {
          ...snapshot.context,
          selection: dragSelection
        }
      });
      return droppingOnDragOrigin ? !1 : {
        dropPosition,
        draggingEntireBlocks,
        draggedBlocks,
        dragOrigin,
        originEvent: event.originEvent
      };
    },
    actions: [({
      event
    }, {
      draggingEntireBlocks,
      draggedBlocks,
      dragOrigin,
      dropPosition,
      originEvent
    }) => [raise({
      type: "select",
      at: dropPosition
    }), ...draggingEntireBlocks ? draggedBlocks.map((block) => raise({
      type: "delete.block",
      at: block.path
    })) : [raise({
      type: "delete",
      at: dragOrigin.selection
    })], raise({
      type: "insert.blocks",
      blocks: event.data,
      placement: draggingEntireBlocks ? originEvent.position.block === "start" ? "before" : originEvent.position.block === "end" ? "after" : "auto" : "auto"
    })]]
  })
], coreInsertBehaviors = [defineBehavior({
  on: "insert.text",
  guard: ({
    snapshot
  }) => {
    if (!getFocusSpan$1(snapshot))
      return !1;
    const markState = getMarkState(snapshot), activeDecorators = getActiveDecorators(snapshot), activeAnnotations = getActiveAnnotationsMarks(snapshot);
    if (markState && markState.state === "unchanged") {
      const markStateDecorators = (markState.marks ?? []).filter((mark) => snapshot.context.schema.decorators.map((decorator) => decorator.name).includes(mark));
      if (markStateDecorators.length === activeDecorators.length && markStateDecorators.every((mark) => activeDecorators.includes(mark)))
        return !1;
    }
    return {
      activeDecorators,
      activeAnnotations
    };
  },
  actions: [({
    snapshot,
    event
  }, {
    activeDecorators,
    activeAnnotations
  }) => [raise({
    type: "insert.child",
    child: {
      _type: snapshot.context.schema.span.name,
      text: event.text,
      marks: [...activeDecorators, ...activeAnnotations]
    }
  })]]
})], breakingAtTheEndOfTextBlock = defineBehavior({
  on: "insert.break",
  guard: ({
    snapshot
  }) => {
    const focusTextBlock = getFocusTextBlock(snapshot), selectionCollapsed = isSelectionCollapsed$1(snapshot);
    if (!snapshot.context.selection || !focusTextBlock || !selectionCollapsed)
      return !1;
    const atTheEndOfBlock = isAtTheEndOfBlock(focusTextBlock)(snapshot), focusListItem = focusTextBlock.node.listItem, focusLevel = focusTextBlock.node.level;
    return atTheEndOfBlock ? {
      focusListItem,
      focusLevel
    } : !1;
  },
  actions: [({
    snapshot
  }, {
    focusListItem,
    focusLevel
  }) => [raise({
    type: "insert.block",
    block: {
      _type: snapshot.context.schema.block.name,
      children: [{
        _type: snapshot.context.schema.span.name,
        text: "",
        marks: []
      }],
      markDefs: [],
      listItem: focusListItem,
      level: focusLevel,
      style: snapshot.context.schema.styles[0]?.name
    },
    placement: "after"
  })]]
}), breakingAtTheStartOfTextBlock = defineBehavior({
  on: "insert.break",
  guard: ({
    snapshot
  }) => {
    const focusTextBlock = getFocusTextBlock(snapshot), selectionCollapsed = isSelectionCollapsed$1(snapshot);
    if (!snapshot.context.selection || !focusTextBlock || !selectionCollapsed)
      return !1;
    const focusSpan = getFocusSpan$1(snapshot), focusDecorators = focusSpan?.node.marks?.filter((mark) => snapshot.context.schema.decorators.some((decorator) => decorator.name === mark) ?? []), focusAnnotations = focusSpan?.node.marks?.filter((mark) => !snapshot.context.schema.decorators.some((decorator) => decorator.name === mark)) ?? [], focusListItem = focusTextBlock.node.listItem, focusLevel = focusTextBlock.node.level;
    return isAtTheStartOfBlock(focusTextBlock)(snapshot) ? {
      focusAnnotations,
      focusDecorators,
      focusListItem,
      focusLevel
    } : !1;
  },
  actions: [({
    snapshot
  }, {
    focusAnnotations,
    focusDecorators,
    focusListItem,
    focusLevel
  }) => [raise({
    type: "insert.block",
    block: {
      _type: snapshot.context.schema.block.name,
      children: [{
        _type: snapshot.context.schema.span.name,
        marks: focusAnnotations.length === 0 ? focusDecorators : [],
        text: ""
      }],
      listItem: focusListItem,
      level: focusLevel,
      style: snapshot.context.schema.styles[0]?.name
    },
    placement: "before",
    select: "none"
  })]]
}), breakingEntireBlocks = defineBehavior({
  on: "insert.break",
  guard: ({
    snapshot
  }) => {
    if (!snapshot.context.selection || !isSelectionExpanded(snapshot))
      return !1;
    const selectedBlocks = getSelectedBlocks(snapshot), selectionStartBlock = getSelectionStartBlock(snapshot), selectionEndBlock = getSelectionEndBlock(snapshot);
    if (!selectionStartBlock || !selectionEndBlock)
      return !1;
    const startBlockStartPoint = getBlockStartPoint({
      context: snapshot.context,
      block: selectionStartBlock
    }), selectionStartPoint = getSelectionStartPoint$1(snapshot.context.selection), endBlockEndPoint = getBlockEndPoint({
      context: snapshot.context,
      block: selectionEndBlock
    }), selectionEndPoint = getSelectionEndPoint$1(snapshot.context.selection);
    return isEqualSelectionPoints(selectionStartPoint, startBlockStartPoint) && isEqualSelectionPoints(selectionEndPoint, endBlockEndPoint) ? {
      selectedBlocks
    } : !1;
  },
  actions: [({
    snapshot
  }, {
    selectedBlocks
  }) => [raise({
    type: "insert.block",
    block: {
      _type: snapshot.context.schema.block.name,
      children: [{
        _type: snapshot.context.schema.span.name,
        text: "",
        marks: []
      }]
    },
    placement: "before",
    select: "start"
  }), ...selectedBlocks.map((block) => raise({
    type: "delete.block",
    at: block.path
  }))]]
}), breakingInlineObject = defineBehavior({
  on: "insert.break",
  guard: ({
    snapshot
  }) => {
    const selectionCollapsed = isSelectionCollapsed$1(snapshot), focusInlineObject = getFocusInlineObject(snapshot);
    return selectionCollapsed && focusInlineObject;
  },
  actions: [() => [raise({
    type: "move.forward",
    distance: 1
  }), raise({
    type: "split"
  })]]
}), coreInsertBreakBehaviors = {
  breakingAtTheEndOfTextBlock,
  breakingAtTheStartOfTextBlock,
  breakingEntireBlocks,
  breakingInlineObject
};
function isAtTheBeginningOfBlock({
  context,
  block
}) {
  return !isTextBlock(context, block) || !context.selection || !isSelectionCollapsed(context.selection) ? !1 : getChildKeyFromSelectionPoint(context.selection.focus) === block.children[0]?._key && context.selection.focus.offset === 0;
}
const MAX_LIST_LEVEL = 10, clearListOnBackspace = defineBehavior({
  on: "delete.backward",
  guard: ({
    snapshot
  }) => {
    const focusTextBlock = getFocusTextBlock(snapshot);
    return !focusTextBlock || focusTextBlock.node.level !== 1 || !isAtTheBeginningOfBlock({
      context: snapshot.context,
      block: focusTextBlock.node
    }) ? !1 : {
      focusTextBlock
    };
  },
  actions: [(_, {
    focusTextBlock
  }) => [raise({
    type: "block.unset",
    props: ["listItem", "level"],
    at: focusTextBlock.path
  })]]
}), unindentListOnBackspace = defineBehavior({
  on: "delete.backward",
  guard: ({
    snapshot
  }) => {
    const selectionCollapsed = isSelectionCollapsed$1(snapshot), focusTextBlock = getFocusTextBlock(snapshot), focusSpan = getFocusSpan$1(snapshot);
    return !selectionCollapsed || !focusTextBlock || !focusSpan ? !1 : focusTextBlock.node.children[0]?._key === focusSpan.node._key && snapshot.context.selection?.focus.offset === 0 && focusTextBlock.node.level !== void 0 && focusTextBlock.node.level > 1 ? {
      focusTextBlock,
      level: focusTextBlock.node.level - 1
    } : !1;
  },
  actions: [(_, {
    focusTextBlock,
    level
  }) => [raise({
    type: "block.set",
    props: {
      level
    },
    at: focusTextBlock.path
  })]]
}), mergeTextIntoListOnDelete = defineBehavior({
  on: "delete.forward",
  guard: ({
    snapshot
  }) => {
    const focusListBlock = getFocusListBlock(snapshot), nextBlock = getNextBlock(snapshot);
    return !focusListBlock || !nextBlock || !isTextBlock(snapshot.context, nextBlock.node) || !isEmptyTextBlock(snapshot.context, focusListBlock.node) ? !1 : {
      focusListBlock,
      nextBlock
    };
  },
  actions: [(_, {
    nextBlock
  }) => [raise({
    type: "insert.block",
    block: nextBlock.node,
    placement: "auto",
    select: "start"
  }), raise({
    type: "delete.block",
    at: nextBlock.path
  })]]
}), mergeTextIntoListOnBackspace = defineBehavior({
  on: "delete.backward",
  guard: ({
    snapshot
  }) => {
    const focusTextBlock = getFocusTextBlock(snapshot), previousBlock = getPreviousBlock(snapshot);
    if (!focusTextBlock || !previousBlock || !isAtTheBeginningOfBlock({
      context: snapshot.context,
      block: focusTextBlock.node
    }) || !isListBlock(snapshot.context, previousBlock.node) || !isEmptyTextBlock(snapshot.context, previousBlock.node))
      return !1;
    const previousBlockEndPoint = getBlockEndPoint({
      context: snapshot.context,
      block: previousBlock
    });
    return {
      focusTextBlock,
      previousBlockEndPoint
    };
  },
  actions: [(_, {
    focusTextBlock,
    previousBlockEndPoint
  }) => [raise({
    type: "select",
    at: {
      anchor: previousBlockEndPoint,
      focus: previousBlockEndPoint
    }
  }), raise({
    type: "insert.block",
    block: focusTextBlock.node,
    placement: "auto",
    select: "start"
  }), raise({
    type: "delete.block",
    at: focusTextBlock.path
  })]]
}), deletingListFromStart = defineBehavior({
  on: "delete",
  guard: ({
    snapshot,
    event
  }) => {
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const blocksToDelete = getSelectedBlocks({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    });
    if (blocksToDelete.length < 2)
      return !1;
    const startBlock = blocksToDelete.at(0)?.node, middleBlocks = blocksToDelete.slice(1, -1), endBlock = blocksToDelete.at(-1)?.node;
    if (!isListBlock(snapshot.context, startBlock) || !isListBlock(snapshot.context, endBlock))
      return !1;
    const deleteStartPoint = getSelectionStartPoint({
      context: {
        ...snapshot.context,
        selection: at
      }
    }), deleteEndPoint = getSelectionEndPoint({
      context: {
        ...snapshot.context,
        selection: at
      }
    });
    if (!deleteStartPoint || !deleteEndPoint)
      return !1;
    const startBlockStartPoint = getBlockStartPoint({
      context: snapshot.context,
      block: {
        node: startBlock,
        path: [{
          _key: startBlock._key
        }]
      }
    });
    if (!isEqualSelectionPoints(deleteStartPoint, startBlockStartPoint))
      return !1;
    const startBlockEndPoint = getBlockEndPoint({
      context: snapshot.context,
      block: {
        node: startBlock,
        path: [{
          _key: startBlock._key
        }]
      }
    }), endBlockEndPoint = getBlockEndPoint({
      context: snapshot.context,
      block: {
        node: endBlock,
        path: [{
          _key: endBlock._key
        }]
      }
    }), slicedEndBlock = sliceTextBlock({
      context: {
        schema: snapshot.context.schema,
        selection: {
          anchor: deleteEndPoint,
          focus: endBlockEndPoint
        }
      },
      block: endBlock
    });
    return {
      startBlockStartPoint,
      startBlockEndPoint,
      middleBlocks,
      endBlock,
      slicedEndBlock
    };
  },
  actions: [(_, {
    startBlockStartPoint,
    startBlockEndPoint,
    middleBlocks,
    endBlock,
    slicedEndBlock
  }) => [
    // All block in between can safely be deleted.
    ...middleBlocks.map((block) => raise({
      type: "delete.block",
      at: block.path
    })),
    // The last block is deleted as well.
    raise({
      type: "delete.block",
      at: [{
        _key: endBlock._key
      }]
    }),
    // But in case the delete operation didn't reach all the way to the end
    // of it, we first place the caret at the end of the start block...
    raise({
      type: "select",
      at: {
        anchor: startBlockEndPoint,
        focus: startBlockEndPoint
      }
    }),
    // ...and insert the rest of the end block at the end of it.
    raise({
      type: "insert.block",
      block: slicedEndBlock,
      placement: "auto",
      select: "none"
    }),
    // And finally, we delete the original text of the start block.
    raise({
      type: "delete",
      at: {
        anchor: startBlockStartPoint,
        focus: startBlockEndPoint
      }
    })
  ]]
}), clearListOnEnter = defineBehavior({
  on: "insert.break",
  guard: ({
    snapshot
  }) => {
    const selectionCollapsed = isSelectionCollapsed$1(snapshot), focusListBlock = getFocusListBlock(snapshot);
    return !selectionCollapsed || !focusListBlock || !isEmptyTextBlock(snapshot.context, focusListBlock.node) ? !1 : {
      focusListBlock
    };
  },
  actions: [(_, {
    focusListBlock
  }) => [raise({
    type: "block.unset",
    props: ["listItem", "level"],
    at: focusListBlock.path
  })]]
}), indentListOnTab = defineBehavior({
  on: "keyboard.keydown",
  guard: ({
    snapshot,
    event
  }) => {
    if (!defaultKeyboardShortcuts.tab.guard(event.originEvent))
      return !1;
    const selectedBlocks = getSelectedBlocks(snapshot), selectedListBlocks = selectedBlocks.flatMap((block) => isListBlock(snapshot.context, block.node) ? [{
      node: block.node,
      path: block.path
    }] : []);
    return selectedListBlocks.length === selectedBlocks.length ? {
      selectedListBlocks
    } : !1;
  },
  actions: [(_, {
    selectedListBlocks
  }) => selectedListBlocks.map((selectedListBlock) => raise({
    type: "block.set",
    props: {
      level: Math.min(MAX_LIST_LEVEL, Math.max(1, selectedListBlock.node.level + 1))
    },
    at: selectedListBlock.path
  }))]
}), unindentListOnShiftTab = defineBehavior({
  on: "keyboard.keydown",
  guard: ({
    snapshot,
    event
  }) => {
    if (!defaultKeyboardShortcuts.shiftTab.guard(event.originEvent))
      return !1;
    const selectedBlocks = getSelectedBlocks(snapshot), selectedListBlocks = selectedBlocks.flatMap((block) => isListBlock(snapshot.context, block.node) ? [{
      node: block.node,
      path: block.path
    }] : []);
    return selectedListBlocks.length === selectedBlocks.length ? {
      selectedListBlocks
    } : !1;
  },
  actions: [(_, {
    selectedListBlocks
  }) => selectedListBlocks.map((selectedListBlock) => raise({
    type: "block.set",
    props: {
      level: Math.min(MAX_LIST_LEVEL, Math.max(1, selectedListBlock.node.level - 1))
    },
    at: selectedListBlock.path
  }))]
}), inheritListLevel = defineBehavior({
  on: "insert.blocks",
  guard: ({
    snapshot,
    event
  }) => {
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: event.at ?? snapshot.context.selection
      }
    }, focusListBlock = getFocusListBlock(adjustedSnapshot);
    if (!focusListBlock)
      return !1;
    const firstInsertedBlock = event.blocks.at(0), secondInsertedBlock = event.blocks.at(1), insertedListBlock = isListBlock(snapshot.context, firstInsertedBlock) ? firstInsertedBlock : isListBlock(snapshot.context, secondInsertedBlock) ? secondInsertedBlock : void 0;
    if (!insertedListBlock)
      return !1;
    const levelDifference = focusListBlock.node.level - insertedListBlock.level;
    return levelDifference === 0 ? !1 : {
      levelDifference,
      insertedListBlock
    };
  },
  actions: [({
    snapshot,
    event
  }, {
    levelDifference,
    insertedListBlock
  }) => {
    let adjustLevel = !0, listStartBlockFound = !1;
    return [raise({
      ...event,
      blocks: event.blocks.map((block) => (block._key === insertedListBlock._key && (listStartBlockFound = !0), adjustLevel ? listStartBlockFound && adjustLevel && isListBlock(snapshot.context, block) ? {
        ...block,
        level: Math.min(MAX_LIST_LEVEL, Math.max(1, block.level + levelDifference))
      } : (listStartBlockFound && (adjustLevel = !1), block) : block))
    })];
  }]
}), inheritListItem = defineBehavior({
  on: "insert.blocks",
  guard: ({
    snapshot,
    event
  }) => {
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: event.at ?? snapshot.context.selection
      }
    }, focusListBlock = getFocusListBlock(adjustedSnapshot);
    if (!focusListBlock || isEmptyTextBlock(snapshot.context, focusListBlock.node))
      return !1;
    const firstInsertedBlock = event.blocks.at(0), secondInsertedBlock = event.blocks.at(1), insertedListBlock = isListBlock(snapshot.context, firstInsertedBlock) ? firstInsertedBlock : isListBlock(snapshot.context, secondInsertedBlock) ? secondInsertedBlock : void 0;
    return !insertedListBlock || focusListBlock.node.level !== insertedListBlock.level || focusListBlock.node.listItem === insertedListBlock.listItem ? !1 : {
      listItem: focusListBlock.node.listItem,
      insertedListBlock
    };
  },
  actions: [({
    snapshot,
    event
  }, {
    listItem,
    insertedListBlock
  }) => {
    let adjustListItem = !0, listStartBlockFound = !1;
    return [raise({
      ...event,
      blocks: event.blocks.map((block) => (block._key === insertedListBlock._key && (listStartBlockFound = !0), adjustListItem ? listStartBlockFound && adjustListItem && isListBlock(snapshot.context, block) ? {
        ...block,
        listItem: block.level === insertedListBlock.level ? listItem : block.listItem
      } : (listStartBlockFound && (adjustListItem = !1), block) : block))
    })];
  }]
}), inheritListProperties = defineBehavior({
  on: "insert.block",
  guard: ({
    snapshot,
    event
  }) => {
    if (event.placement !== "auto" || event.block._type !== snapshot.context.schema.block.name || event.block.listItem !== void 0)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: event.at ?? snapshot.context.selection
      }
    }, focusListBlock = getFocusListBlock(adjustedSnapshot);
    return !focusListBlock || !isEmptyTextBlock(snapshot.context, focusListBlock.node) ? !1 : {
      level: focusListBlock.node.level,
      listItem: focusListBlock.node.listItem
    };
  },
  actions: [({
    event
  }, {
    level,
    listItem
  }) => [raise({
    ...event,
    block: {
      ...event.block,
      level,
      listItem
    }
  })]]
}), coreListBehaviors = {
  clearListOnBackspace,
  unindentListOnBackspace,
  mergeTextIntoListOnDelete,
  mergeTextIntoListOnBackspace,
  deletingListFromStart,
  clearListOnEnter,
  indentListOnTab,
  unindentListOnShiftTab,
  inheritListLevel,
  inheritListItem,
  inheritListProperties
}, coreBehaviors = [...coreAnnotationBehaviors, coreDecoratorBehaviors.strongShortcut, coreDecoratorBehaviors.emShortcut, coreDecoratorBehaviors.underlineShortcut, coreDecoratorBehaviors.codeShortcut, ...coreDndBehaviors, coreBlockObjectBehaviors.clickingAboveLonelyBlockObject, coreBlockObjectBehaviors.clickingBelowLonelyBlockObject, coreBlockObjectBehaviors.arrowDownOnLonelyBlockObject, coreBlockObjectBehaviors.arrowUpOnLonelyBlockObject, coreBlockObjectBehaviors.breakingBlockObject, coreBlockObjectBehaviors.deletingEmptyTextBlockAfterBlockObject, coreBlockObjectBehaviors.deletingEmptyTextBlockBeforeBlockObject, ...coreInsertBehaviors, coreListBehaviors.clearListOnBackspace, coreListBehaviors.unindentListOnBackspace, coreListBehaviors.mergeTextIntoListOnDelete, coreListBehaviors.mergeTextIntoListOnBackspace, coreListBehaviors.deletingListFromStart, coreListBehaviors.clearListOnEnter, coreListBehaviors.indentListOnTab, coreListBehaviors.unindentListOnShiftTab, coreListBehaviors.inheritListLevel, coreListBehaviors.inheritListItem, coreListBehaviors.inheritListProperties, coreInsertBreakBehaviors.breakingAtTheEndOfTextBlock, coreInsertBreakBehaviors.breakingAtTheStartOfTextBlock, coreInsertBreakBehaviors.breakingEntireBlocks, coreInsertBreakBehaviors.breakingInlineObject];
let previousPriority = corePriority;
const coreBehaviorsConfigArray = [];
for (const behavior of coreBehaviors) {
  const priority = createEditorPriority({
    name: "core",
    reference: {
      priority: previousPriority,
      importance: "lower"
    }
  });
  coreBehaviorsConfigArray.push({
    behavior,
    priority
  }), previousPriority = priority;
}
const coreBehaviorsConfig = coreBehaviorsConfigArray;
function createEditorSnapshot({
  converters,
  editor,
  keyGenerator,
  readOnly,
  schema
}) {
  const selection = editor.selection ? slateRangeToSelection({
    schema,
    editor,
    range: editor.selection
  }) : null, context = {
    converters,
    keyGenerator,
    readOnly,
    schema,
    selection,
    value: editor.value
  };
  return {
    blockIndexMap: editor.blockIndexMap,
    context,
    decoratorState: editor.decoratorState
  };
}
const addAnnotationOperationImplementation = ({
  context,
  operation
}) => {
  const parsedAnnotation = parseAnnotation({
    annotation: {
      _type: operation.annotation.name,
      _key: operation.annotation._key,
      ...operation.annotation.value
    },
    context,
    options: {
      validateFields: !0
    }
  });
  if (!parsedAnnotation)
    throw new Error(`Failed to parse annotation ${JSON.stringify(operation.annotation)}`);
  const editor = operation.editor, at = operation.at ? toSlateRange({
    context: {
      schema: context.schema,
      value: operation.editor.value,
      selection: operation.at
    },
    blockIndexMap: operation.editor.blockIndexMap
  }) : null, effectiveSelection = at ?? editor.selection;
  if (!effectiveSelection || Range.isCollapsed(effectiveSelection))
    return;
  const rangeRef2 = at ? Editor.rangeRef(editor, at, {
    affinity: "inward"
  }) : null, selectedBlocks = Editor.nodes(editor, {
    at: effectiveSelection,
    match: (node2) => editor.isTextBlock(node2),
    reverse: Range.isBackward(effectiveSelection)
  });
  let blockIndex = 0;
  for (const [block, blockPath] of selectedBlocks) {
    if (block.children.length === 0 || block.children.length === 1 && block.children[0]?.text === "")
      continue;
    const annotationKey = blockIndex === 0 ? parsedAnnotation._key : context.keyGenerator(), markDefs = block.markDefs ?? [];
    markDefs.find((markDef) => markDef._type === parsedAnnotation._type && markDef._key === annotationKey) === void 0 && Transforms.setNodes(editor, {
      markDefs: [...markDefs, {
        ...parsedAnnotation,
        _key: annotationKey
      }]
    }, {
      at: blockPath
    }), at ? Transforms.setNodes(editor, {}, {
      match: Text$1.isText,
      split: !0,
      at
    }) : Transforms.setNodes(editor, {}, {
      match: Text$1.isText,
      split: !0
    });
    const children = Node$1.children(editor, blockPath), selectionRange = rangeRef2?.current ?? editor.selection;
    for (const [span, path2] of children) {
      if (!editor.isTextSpan(span) || !selectionRange || !Range.includes(selectionRange, path2))
        continue;
      const marks2 = span.marks ?? [];
      Transforms.setNodes(editor, {
        marks: [...marks2, annotationKey]
      }, {
        at: path2
      });
    }
    blockIndex++;
  }
  rangeRef2?.unref();
}, removeAnnotationOperationImplementation = ({
  context,
  operation
}) => {
  const editor = operation.editor, at = operation.at ? toSlateRange({
    context: {
      schema: context.schema,
      value: operation.editor.value,
      selection: operation.at
    },
    blockIndexMap: operation.editor.blockIndexMap
  }) : null, effectiveSelection = at ?? editor.selection;
  if (effectiveSelection)
    if (Range.isCollapsed(effectiveSelection)) {
      const [block, blockPath] = Editor.node(editor, effectiveSelection, {
        depth: 1
      });
      if (!editor.isTextBlock(block))
        return;
      const potentialAnnotations = (block.markDefs ?? []).filter((markDef) => markDef._type === operation.annotation.name), [selectedChild, selectedChildPath] = Editor.node(editor, effectiveSelection, {
        depth: 2
      });
      if (!editor.isTextSpan(selectedChild))
        return;
      const annotationToRemove = selectedChild.marks?.find((mark) => potentialAnnotations.some((markDef) => markDef._key === mark));
      if (!annotationToRemove)
        return;
      const previousSpansWithSameAnnotation = [];
      for (const [child, childPath] of Node$1.children(editor, blockPath, {
        reverse: !0
      }))
        if (editor.isTextSpan(child) && Path.isBefore(childPath, selectedChildPath))
          if (child.marks?.includes(annotationToRemove))
            previousSpansWithSameAnnotation.push([child, childPath]);
          else
            break;
      const nextSpansWithSameAnnotation = [];
      for (const [child, childPath] of Node$1.children(editor, blockPath))
        if (editor.isTextSpan(child) && Path.isAfter(childPath, selectedChildPath))
          if (child.marks?.includes(annotationToRemove))
            nextSpansWithSameAnnotation.push([child, childPath]);
          else
            break;
      for (const [child, childPath] of [...previousSpansWithSameAnnotation, [selectedChild, selectedChildPath], ...nextSpansWithSameAnnotation])
        Transforms.setNodes(editor, {
          marks: child.marks?.filter((mark) => mark !== annotationToRemove)
        }, {
          at: childPath
        });
    } else {
      const rangeRef2 = at ? Editor.rangeRef(editor, at, {
        affinity: "inward"
      }) : null;
      at ? Transforms.setNodes(editor, {}, {
        match: (node2) => editor.isTextSpan(node2),
        split: !0,
        hanging: !0,
        at
      }) : Transforms.setNodes(editor, {}, {
        match: (node2) => editor.isTextSpan(node2),
        split: !0,
        hanging: !0
      });
      const blocks = Editor.nodes(editor, {
        at: effectiveSelection,
        match: (node2) => editor.isTextBlock(node2)
      }), selectionRange = rangeRef2?.current ?? editor.selection;
      for (const [block, blockPath] of blocks) {
        const children = Node$1.children(editor, blockPath);
        for (const [child, childPath] of children) {
          if (!editor.isTextSpan(child) || !selectionRange || !Range.includes(selectionRange, childPath))
            continue;
          const markDefs = block.markDefs ?? [], marks2 = child.marks ?? [], marksWithoutAnnotation = marks2.filter((mark) => markDefs.find((markDef2) => markDef2._key === mark)?._type !== operation.annotation.name);
          marksWithoutAnnotation.length !== marks2.length && Transforms.setNodes(editor, {
            marks: marksWithoutAnnotation
          }, {
            at: childPath
          });
        }
      }
      rangeRef2?.unref();
    }
}, blockSetOperationImplementation = ({
  context,
  operation
}) => {
  const blockIndex = operation.editor.blockIndexMap.get(operation.at[0]._key);
  if (blockIndex === void 0)
    throw new Error(`Unable to find block index for block at ${JSON.stringify(operation.at)}`);
  const slateBlock = operation.editor.children.at(blockIndex);
  if (!slateBlock)
    throw new Error(`Unable to find block at ${JSON.stringify(operation.at)}`);
  if (isTextBlock(context, slateBlock)) {
    const filteredProps = {};
    for (const key of Object.keys(operation.props))
      if (!(key === "_type" || key === "children")) {
        if (key === "style") {
          context.schema.styles.some((style) => style.name === operation.props[key]) && (filteredProps[key] = operation.props[key]);
          continue;
        }
        if (key === "listItem") {
          context.schema.lists.some((list) => list.name === operation.props[key]) && (filteredProps[key] = operation.props[key]);
          continue;
        }
        if (key === "level") {
          filteredProps[key] = operation.props[key];
          continue;
        }
        if (key === "markDefs") {
          const {
            markDefs
          } = parseMarkDefs({
            context,
            markDefs: operation.props[key],
            options: {
              validateFields: !0
            }
          });
          filteredProps[key] = markDefs;
          continue;
        }
        context.schema.block.fields?.some((field) => field.name === key) && (filteredProps[key] = operation.props[key]);
      }
    Transforms.setNodes(operation.editor, filteredProps, {
      at: [blockIndex]
    });
  } else {
    const schemaDefinition = context.schema.blockObjects.find((definition) => definition.name === slateBlock._type), filteredProps = {};
    for (const key of Object.keys(operation.props))
      if (key !== "_type") {
        if (key === "_key") {
          filteredProps[key] = operation.props[key];
          continue;
        }
        schemaDefinition?.fields.some((field) => field.name === key) && (filteredProps[key] = operation.props[key]);
      }
    const patches = Object.entries(filteredProps).map(([key, value]) => key === "_key" ? set(value, ["_key"]) : set(value, ["value", key])), updatedSlateBlock = applyAll(slateBlock, patches);
    Transforms.setNodes(operation.editor, updatedSlateBlock, {
      at: [blockIndex]
    });
  }
}, blockUnsetOperationImplementation = ({
  context,
  operation
}) => {
  const blockKey = operation.at[0]._key, blockIndex = operation.editor.blockIndexMap.get(blockKey);
  if (blockIndex === void 0)
    throw new Error(`Unable to find block index for block key ${blockKey}`);
  const slateBlock = blockIndex !== void 0 ? operation.editor.children.at(blockIndex) : void 0;
  if (!slateBlock)
    throw new Error(`Unable to find block at ${JSON.stringify(operation.at)}`);
  if (isTextBlock(context, slateBlock)) {
    const propsToRemove = operation.props.filter((prop) => prop !== "_type" && prop !== "_key" && prop !== "children");
    Transforms.unsetNodes(operation.editor, propsToRemove, {
      at: [blockIndex]
    }), operation.props.includes("_key") && Transforms.setNodes(operation.editor, {
      _key: context.keyGenerator()
    }, {
      at: [blockIndex]
    });
    return;
  }
  const patches = operation.props.flatMap((key) => key === "_type" ? [] : key === "_key" ? set(context.keyGenerator(), ["_key"]) : unset(["value", key])), updatedSlateBlock = applyAll(slateBlock, patches);
  Transforms.setNodes(operation.editor, updatedSlateBlock, {
    at: [blockIndex]
  });
}, childSetOperationImplementation = ({
  context,
  operation
}) => {
  const location = toSlateRange({
    context: {
      schema: context.schema,
      value: operation.editor.value,
      selection: {
        anchor: {
          path: operation.at,
          offset: 0
        },
        focus: {
          path: operation.at,
          offset: 0
        }
      }
    },
    blockIndexMap: operation.editor.blockIndexMap
  });
  if (!location)
    throw new Error(`Unable to convert ${JSON.stringify(operation.at)} into a Slate Range`);
  const childEntry = Editor.node(operation.editor, location, {
    depth: 2
  }), child = childEntry?.[0], childPath = childEntry?.[1];
  if (!child || !childPath)
    throw new Error(`Unable to find child at ${JSON.stringify(operation.at)}`);
  if (operation.editor.isTextSpan(child)) {
    const {
      _type,
      text,
      ...rest
    } = operation.props;
    Transforms.setNodes(operation.editor, {
      ...child,
      ...rest
    }, {
      at: childPath
    }), typeof text == "string" && child.text !== text && (operation.editor.apply({
      type: "remove_text",
      path: childPath,
      offset: 0,
      text: child.text
    }), operation.editor.apply({
      type: "insert_text",
      path: childPath,
      offset: 0,
      text
    }));
    return;
  }
  if (Element$2.isElement(child)) {
    const definition = context.schema.inlineObjects.find((definition2) => definition2.name === child._type);
    if (!definition)
      throw new Error(`Unable to find schema definition for Inline Object type ${child._type}`);
    const value = "value" in child && typeof child.value == "object" ? child.value : {}, {
      _type,
      _key,
      ...rest
    } = operation.props;
    for (const prop in rest)
      definition.fields.some((field) => field.name === prop) || delete rest[prop];
    Transforms.setNodes(operation.editor, {
      ...child,
      _key: typeof _key == "string" ? _key : child._key,
      value: {
        ...value,
        ...rest
      }
    }, {
      at: childPath
    });
    return;
  }
  throw new Error(`Unable to determine the type of child at ${JSON.stringify(operation.at)}`);
}, childUnsetOperationImplementation = ({
  context,
  operation
}) => {
  const blockKey = operation.at[0]._key, blockIndex = operation.editor.blockIndexMap.get(blockKey);
  if (blockIndex === void 0)
    throw new Error(`Unable to find block index for block key ${blockKey}`);
  const block = blockIndex !== void 0 ? operation.editor.value.at(blockIndex) : void 0;
  if (!block)
    throw new Error(`Unable to find block at ${JSON.stringify(operation.at)}`);
  if (!isTextBlock(context, block))
    throw new Error(`Block ${JSON.stringify(blockKey)} is not a text block`);
  const childKey = operation.at[2]._key;
  if (!childKey)
    throw new Error(`Unable to find child key at ${JSON.stringify(operation.at)}`);
  const childIndex = block.children.findIndex((child2) => child2._key === childKey);
  if (childIndex === -1)
    throw new Error(`Unable to find child at ${JSON.stringify(operation.at)}`);
  const childEntry = Editor.node(operation.editor, [blockIndex, childIndex], {
    depth: 2
  }), child = childEntry?.[0], childPath = childEntry?.[1];
  if (!child || !childPath)
    throw new Error(`Unable to find child at ${JSON.stringify(operation.at)}`);
  if (operation.editor.isTextSpan(child)) {
    const newNode = {};
    for (const prop of operation.props)
      if (prop !== "text" && prop !== "_type") {
        if (prop === "_key") {
          newNode._key = context.keyGenerator();
          continue;
        }
        newNode[prop] = null;
      }
    Transforms.setNodes(operation.editor, newNode, {
      at: childPath
    }), operation.props.includes("text") && operation.editor.apply({
      type: "remove_text",
      path: childPath,
      offset: 0,
      text: child.text
    });
    return;
  }
  if (Element$2.isElement(child)) {
    const value = "value" in child && typeof child.value == "object" ? child.value : {}, patches = operation.props.map((prop) => ({
      type: "unset",
      path: [prop]
    })), newValue = applyAll(value, patches);
    Transforms.setNodes(operation.editor, {
      ...child,
      _key: operation.props.includes("_key") ? context.keyGenerator() : child._key,
      value: newValue
    }, {
      at: childPath
    });
    return;
  }
  throw new Error(`Unable to determine the type of child at ${JSON.stringify(operation.at)}`);
}, decoratorAddOperationImplementation = ({
  context,
  operation
}) => {
  const editor = operation.editor, mark = operation.decorator;
  let at = operation.at ? toSlateRange({
    context: {
      schema: context.schema,
      value: operation.editor.value,
      selection: operation.at
    },
    blockIndexMap: operation.editor.blockIndexMap
  }) : operation.editor.selection;
  if (at) {
    if (Range.isExpanded(at)) {
      const rangeRef2 = Editor.rangeRef(editor, at, {
        affinity: "inward"
      }), [start2, end2] = Range.edges(at), endAtEndOfNode = Editor.isEnd(editor, end2, end2.path);
      Transforms.splitNodes(editor, {
        at: end2,
        match: Text$1.isText,
        mode: "lowest",
        voids: !1,
        always: !endAtEndOfNode
      });
      const startAtStartOfNode = Editor.isStart(editor, start2, start2.path);
      if (Transforms.splitNodes(editor, {
        at: start2,
        match: Text$1.isText,
        mode: "lowest",
        voids: !1,
        always: !startAtStartOfNode
      }), at = rangeRef2.unref(), !at)
        throw new Error("Unable to add decorator without a selection");
      operation.at || Transforms.select(editor, at);
      const splitTextNodes = Editor.nodes(editor, {
        at,
        match: Text$1.isText
      });
      for (const [node2, path2] of splitTextNodes) {
        const marks2 = [...(Array.isArray(node2.marks) ? node2.marks : []).filter((eMark) => eMark !== mark), mark];
        Transforms.setNodes(editor, {
          marks: marks2
        }, {
          at: path2,
          match: Text$1.isText,
          split: !0,
          hanging: !0
        });
      }
    } else {
      if (!Array.from(Editor.nodes(editor, {
        at,
        match: (node2) => editor.isTextSpan(node2)
      }))?.at(0))
        return;
      const [block, blockPath] = Editor.node(editor, at, {
        depth: 1
      }), lonelyEmptySpan = editor.isTextBlock(block) && block.children.length === 1 && editor.isTextSpan(block.children[0]) && block.children[0].text === "" ? block.children[0] : void 0;
      if (lonelyEmptySpan) {
        const existingMarks = lonelyEmptySpan.marks ?? [], existingMarksWithoutDecorator = existingMarks.filter((existingMark) => existingMark !== mark);
        Transforms.setNodes(editor, {
          marks: existingMarks.length === existingMarksWithoutDecorator.length ? [...existingMarks, mark] : existingMarksWithoutDecorator
        }, {
          at: blockPath,
          match: (node2) => editor.isTextSpan(node2)
        });
      } else
        editor.decoratorState[mark] = !0;
    }
    if (editor.selection) {
      const selection = editor.selection;
      editor.selection = {
        ...selection
      };
    }
  }
}, decoratorRemoveOperationImplementation = ({
  context,
  operation
}) => {
  const editor = operation.editor, mark = operation.decorator, at = operation.at ? toSlateRange({
    context: {
      schema: context.schema,
      value: operation.editor.value,
      selection: operation.at
    },
    blockIndexMap: operation.editor.blockIndexMap
  }) : editor.selection;
  if (at) {
    if (Range.isExpanded(at)) {
      const rangeRef2 = Editor.rangeRef(editor, at, {
        affinity: "inward"
      });
      Transforms.setNodes(editor, {}, {
        at,
        match: Text$1.isText,
        split: !0,
        hanging: !0
      });
      const updatedAt = rangeRef2.unref();
      updatedAt && [...Editor.nodes(editor, {
        at: updatedAt,
        match: Text$1.isText
      })].forEach(([node2, path2]) => {
        const block = editor.children[path2[0]];
        Element$2.isElement(block) && block.children.includes(node2) && Transforms.setNodes(editor, {
          marks: (Array.isArray(node2.marks) ? node2.marks : []).filter((eMark) => eMark !== mark),
          _type: "span"
        }, {
          at: path2
        });
      });
    } else {
      const [block, blockPath] = Editor.node(editor, at, {
        depth: 1
      }), lonelyEmptySpan = editor.isTextBlock(block) && block.children.length === 1 && editor.isTextSpan(block.children[0]) && block.children[0].text === "" ? block.children[0] : void 0;
      if (lonelyEmptySpan) {
        const existingMarksWithoutDecorator = (lonelyEmptySpan.marks ?? []).filter((existingMark) => existingMark !== mark);
        Transforms.setNodes(editor, {
          marks: existingMarksWithoutDecorator
        }, {
          at: blockPath,
          match: (node2) => editor.isTextSpan(node2)
        });
      } else
        editor.decoratorState[mark] = !1;
    }
    if (editor.selection) {
      const selection = editor.selection;
      editor.selection = {
        ...selection
      };
    }
  }
}, deleteOperationImplementation = ({
  context,
  operation
}) => {
  const at = operation.at ? toSlateRange({
    context: {
      schema: context.schema,
      value: operation.editor.value,
      selection: operation.at
    },
    blockIndexMap: operation.editor.blockIndexMap
  }) : operation.editor.selection;
  if (!at)
    throw new Error("Unable to delete without a selection");
  const [start2, end2] = Range.edges(at);
  if (operation.unit === "block") {
    const startBlockIndex = start2.path.at(0), endBlockIndex = end2.path.at(0);
    if (startBlockIndex === void 0 || endBlockIndex === void 0)
      throw new Error("Failed to get start or end block index");
    Transforms.removeNodes(operation.editor, {
      at: {
        anchor: {
          path: [startBlockIndex],
          offset: 0
        },
        focus: {
          path: [endBlockIndex],
          offset: 0
        }
      },
      mode: "highest"
    });
    return;
  }
  if (operation.unit === "child") {
    Transforms.removeNodes(operation.editor, {
      at,
      match: (node2) => isSpan(context, node2) && node2._key !== VOID_CHILD_KEY || "__inline" in node2 && node2.__inline === !0
    });
    return;
  }
  if (operation.direction === "backward" && operation.unit === "line") {
    const parentBlockEntry = Editor.above(operation.editor, {
      match: (n2) => Element$2.isElement(n2) && Editor.isBlock(operation.editor, n2),
      at
    });
    if (parentBlockEntry) {
      const [, parentBlockPath] = parentBlockEntry, parentElementRange = Editor.range(operation.editor, parentBlockPath, at.anchor), currentLineRange = findCurrentLineRange(operation.editor, parentElementRange);
      if (!Range.isCollapsed(currentLineRange)) {
        Transforms.delete(operation.editor, {
          at: currentLineRange
        });
        return;
      }
    }
  }
  if (operation.unit === "word" && Range.isCollapsed(at)) {
    deleteText(operation.editor, {
      at,
      unit: "word",
      reverse: operation.direction === "backward"
    });
    return;
  }
  const startBlock = Editor.above(operation.editor, {
    match: (n2) => Element$2.isElement(n2) && Editor.isBlock(operation.editor, n2),
    at: start2,
    voids: !1
  }), endBlock = Editor.above(operation.editor, {
    match: (n2) => Element$2.isElement(n2) && Editor.isBlock(operation.editor, n2),
    at: end2,
    voids: !1
  }), isAcrossBlocks = startBlock && endBlock && !Path.equals(startBlock[1], endBlock[1]), startNonEditable = Editor.void(operation.editor, {
    at: start2,
    mode: "highest"
  }) ?? Editor.elementReadOnly(operation.editor, {
    at: start2,
    mode: "highest"
  }), endNonEditable = Editor.void(operation.editor, {
    at: end2,
    mode: "highest"
  }) ?? Editor.elementReadOnly(operation.editor, {
    at: end2,
    mode: "highest"
  }), matches = [];
  let lastPath;
  for (const entry of Editor.nodes(operation.editor, {
    at,
    voids: !1
  })) {
    const [node2, path2] = entry;
    lastPath && Path.compare(path2, lastPath) === 0 || (Element$2.isElement(node2) && (Editor.isVoid(operation.editor, node2) || Editor.isElementReadOnly(operation.editor, node2)) || !Path.isCommon(path2, start2.path) && !Path.isCommon(path2, end2.path)) && (matches.push(entry), lastPath = path2);
  }
  const pathRefs2 = Array.from(matches, ([, path2]) => Editor.pathRef(operation.editor, path2)), startRef = Editor.pointRef(operation.editor, start2), endRef = Editor.pointRef(operation.editor, end2);
  if (startBlock && endBlock && Point.equals(start2, Editor.start(operation.editor, startBlock[1])) && Point.equals(end2, Editor.end(operation.editor, endBlock[1])) && isAcrossBlocks && !startNonEditable && !endNonEditable) {
    if (!startNonEditable) {
      const point2 = startRef.current, [node2] = Editor.leaf(operation.editor, point2);
      node2.text.length > 0 && operation.editor.apply({
        type: "remove_text",
        path: point2.path,
        offset: 0,
        text: node2.text
      });
    }
    for (const pathRef2 of pathRefs2.reverse()) {
      const path2 = pathRef2.unref();
      path2 && Transforms.removeNodes(operation.editor, {
        at: path2,
        voids: !1
      });
    }
    if (!endNonEditable) {
      const point2 = endRef.current, [node2] = Editor.leaf(operation.editor, point2), {
        path: path2
      } = point2, offset = 0, text = node2.text.slice(offset, end2.offset);
      text.length > 0 && operation.editor.apply({
        type: "remove_text",
        path: path2,
        offset,
        text
      });
    }
    endRef.current && startRef.current && Transforms.removeNodes(operation.editor, {
      at: endRef.current,
      voids: !1
    }), startRef.current && operation.editor.apply({
      type: "set_selection",
      properties: operation.editor.selection,
      newProperties: {
        anchor: startRef.current,
        focus: startRef.current
      }
    });
    return;
  }
  const reverse = operation.direction === "backward", hanging = reverse ? end2 ? isTextBlock(context, endBlock) ? end2.offset === 0 : !0 : !1 : start2 ? isTextBlock(context, startBlock) ? start2.offset === 0 : !0 : !1;
  operation.at ? deleteText(operation.editor, {
    at,
    hanging,
    reverse
  }) : deleteText(operation.editor, {
    hanging,
    reverse
  });
};
function findCurrentLineRange(editor, parentRange) {
  const parentRangeBoundary = Editor.range(editor, Range.end(parentRange)), positions2 = Array.from(Editor.positions(editor, {
    at: parentRange
  }));
  let left = 0, right = positions2.length, middle = Math.floor(right / 2);
  if (rangesAreOnSameLine(editor, Editor.range(editor, positions2[left]), parentRangeBoundary))
    return Editor.range(editor, positions2[left], parentRangeBoundary);
  if (positions2.length < 2)
    return Editor.range(editor, positions2[positions2.length - 1], parentRangeBoundary);
  for (; middle !== positions2.length && middle !== left; )
    rangesAreOnSameLine(editor, Editor.range(editor, positions2[middle]), parentRangeBoundary) ? right = middle : left = middle, middle = Math.floor((left + right) / 2);
  return Editor.range(editor, positions2[left], parentRangeBoundary);
}
function rangesAreOnSameLine(editor, range1, range2) {
  const rect1 = DOMEditor.toDOMRange(editor, range1).getBoundingClientRect(), rect2 = DOMEditor.toDOMRange(editor, range2).getBoundingClientRect();
  return domRectsIntersect(rect1, rect2) && domRectsIntersect(rect2, rect1);
}
function domRectsIntersect(rect, compareRect) {
  const middle = (compareRect.top + compareRect.bottom) / 2;
  return rect.top <= middle && rect.bottom >= middle;
}
function transformOperation(editor, patch, operation, snapshot, previousSnapshot) {
  const transformedOperation = {
    ...operation
  };
  if (patch.type === "insert" && patch.path.length === 1) {
    const pathSegment = patch.path[0], insertBlockIndex = (snapshot || []).findIndex((blk) => isKeyedSegment(pathSegment) && blk._key === pathSegment._key);
    return debug$1.history(`Adjusting block path (+${patch.items.length}) for '${transformedOperation.type}' operation and patch '${patch.type}'`), [adjustBlockPath(transformedOperation, patch.items.length, insertBlockIndex)];
  }
  if (patch.type === "unset" && patch.path.length === 1) {
    const pathSegment = patch.path[0], unsetBlockIndex = (previousSnapshot || []).findIndex((blk) => isKeyedSegment(pathSegment) && blk._key === pathSegment._key);
    return "path" in transformedOperation && Array.isArray(transformedOperation.path) && transformedOperation.path[0] === unsetBlockIndex ? (debug$1.history("Skipping transformation that targeted removed block"), []) : [adjustBlockPath(transformedOperation, -1, unsetBlockIndex)];
  }
  if (patch.type === "unset" && patch.path.length === 0)
    return debug$1.history(`Adjusting selection for unset everything patch and ${operation.type} operation`), [];
  if (patch.type === "diffMatchPatch") {
    const operationTargetBlock = findOperationTargetBlock(editor, transformedOperation), pathSegment = patch.path[0];
    return !operationTargetBlock || !isKeyedSegment(pathSegment) || operationTargetBlock._key !== pathSegment._key ? [transformedOperation] : (parse(patch.value).forEach((diffPatch) => {
      let adjustOffsetBy = 0, changedOffset = diffPatch.utf8Start1;
      const {
        diffs
      } = diffPatch;
      if (diffs.forEach((diff2, index) => {
        const [diffType, text] = diff2;
        diffType === DIFF_INSERT ? (adjustOffsetBy += text.length, changedOffset += text.length) : diffType === DIFF_DELETE ? (adjustOffsetBy -= text.length, changedOffset -= text.length) : diffType === DIFF_EQUAL && (diffs.slice(index).every(([dType]) => dType === DIFF_EQUAL) || (changedOffset += text.length));
      }), transformedOperation.type === "insert_text" && changedOffset < transformedOperation.offset && (transformedOperation.offset += adjustOffsetBy), transformedOperation.type === "remove_text" && changedOffset <= transformedOperation.offset - transformedOperation.text.length && (transformedOperation.offset += adjustOffsetBy), transformedOperation.type === "set_selection") {
        const currentFocus = transformedOperation.properties?.focus ? {
          ...transformedOperation.properties.focus
        } : void 0, currentAnchor = transformedOperation?.properties?.anchor ? {
          ...transformedOperation.properties.anchor
        } : void 0, newFocus = transformedOperation?.newProperties?.focus ? {
          ...transformedOperation.newProperties.focus
        } : void 0, newAnchor = transformedOperation?.newProperties?.anchor ? {
          ...transformedOperation.newProperties.anchor
        } : void 0;
        (currentFocus && currentAnchor || newFocus && newAnchor) && ([currentFocus, currentAnchor, newFocus, newAnchor].forEach((point2) => {
          point2 && changedOffset < point2.offset && (point2.offset += adjustOffsetBy);
        }), currentFocus && currentAnchor && (transformedOperation.properties = {
          focus: currentFocus,
          anchor: currentAnchor
        }), newFocus && newAnchor && (transformedOperation.newProperties = {
          focus: newFocus,
          anchor: newAnchor
        }));
      }
    }), [transformedOperation]);
  }
  return [transformedOperation];
}
function adjustBlockPath(operation, level, blockIndex) {
  const transformedOperation = {
    ...operation
  };
  if (blockIndex >= 0 && transformedOperation.type !== "set_selection" && Array.isArray(transformedOperation.path) && transformedOperation.path[0] >= blockIndex + level && transformedOperation.path[0] + level > -1) {
    const newPath = [transformedOperation.path[0] + level, ...transformedOperation.path.slice(1)];
    transformedOperation.path = newPath;
  }
  if (transformedOperation.type === "set_selection") {
    const currentFocus = transformedOperation.properties?.focus ? {
      ...transformedOperation.properties.focus
    } : void 0, currentAnchor = transformedOperation?.properties?.anchor ? {
      ...transformedOperation.properties.anchor
    } : void 0, newFocus = transformedOperation?.newProperties?.focus ? {
      ...transformedOperation.newProperties.focus
    } : void 0, newAnchor = transformedOperation?.newProperties?.anchor ? {
      ...transformedOperation.newProperties.anchor
    } : void 0;
    (currentFocus && currentAnchor || newFocus && newAnchor) && ([currentFocus, currentAnchor, newFocus, newAnchor].forEach((point2) => {
      point2 && point2.path[0] >= blockIndex + level && point2.path[0] + level > -1 && (point2.path = [point2.path[0] + level, ...point2.path.slice(1)]);
    }), currentFocus && currentAnchor && (transformedOperation.properties = {
      focus: currentFocus,
      anchor: currentAnchor
    }), newFocus && newAnchor && (transformedOperation.newProperties = {
      focus: newFocus,
      anchor: newAnchor
    }));
  }
  return transformedOperation;
}
function findOperationTargetBlock(editor, operation) {
  let block;
  return operation.type === "set_selection" && editor.selection ? block = editor.children[editor.selection.focus.path[0]] : "path" in operation && (block = editor.children[operation.path[0]]), block;
}
function pluginRedoing(editor, fn) {
  const prev = editor.isRedoing;
  editor.isRedoing = !0, fn(), editor.isRedoing = prev;
}
const historyRedoOperationImplementation = ({
  operation
}) => {
  const editor = operation.editor, {
    redos
  } = editor.history;
  if (redos.length > 0) {
    const step = redos[redos.length - 1];
    if (step.operations.length > 0) {
      const otherPatches = editor.remotePatches.filter((item) => item.time >= step.timestamp);
      let transformedOperations = step.operations;
      otherPatches.forEach((item) => {
        transformedOperations = transformedOperations.flatMap((op) => transformOperation(editor, item.patch, op, item.snapshot, item.previousSnapshot));
      });
      try {
        Editor.withoutNormalizing(editor, () => {
          pluginRedoing(editor, () => {
            pluginWithoutHistory(editor, () => {
              transformedOperations.forEach((op) => {
                editor.apply(op);
              });
            });
          });
        });
      } catch (err) {
        console.error(`Could not perform 'history.redo' operation: ${err instanceof Error ? err.message : err}`), editor.remotePatches.splice(0, editor.remotePatches.length), Transforms.deselect(editor), editor.history = {
          undos: [],
          redos: []
        }, editor.withHistory = !0, editor.isRedoing = !1, editor.onChange();
        return;
      }
      editor.history.undos.push(step), editor.history.redos.pop();
    }
  }
};
function pluginUndoing(editor, fn) {
  const prev = editor.isUndoing;
  editor.isUndoing = !0, fn(), editor.isUndoing = prev;
}
const historyUndoOperationImplementation = ({
  operation
}) => {
  const editor = operation.editor, {
    undos
  } = editor.history;
  if (undos.length > 0) {
    const step = undos[undos.length - 1];
    if (step.operations.length > 0) {
      const otherPatches = editor.remotePatches.filter((item) => item.time >= step.timestamp);
      let transformedOperations = step.operations;
      otherPatches.forEach((item) => {
        transformedOperations = transformedOperations.flatMap((op) => transformOperation(editor, item.patch, op, item.snapshot, item.previousSnapshot));
      });
      const reversedOperations = transformedOperations.map(Operation.inverse).reverse();
      try {
        Editor.withoutNormalizing(editor, () => {
          pluginUndoing(editor, () => {
            pluginWithoutHistory(editor, () => {
              reversedOperations.forEach((op) => {
                editor.apply(op);
              });
            });
          });
        });
      } catch (err) {
        console.error(`Could not perform 'history.undo' operation: ${err instanceof Error ? err.message : err}`), editor.remotePatches.splice(0, editor.remotePatches.length), Transforms.deselect(editor), editor.history = {
          undos: [],
          redos: []
        }, editor.withHistory = !0, editor.isUndoing = !1, editor.onChange();
        return;
      }
      editor.history.redos.push(step), editor.history.undos.pop();
    }
  }
}, insertBlockOperationImplementation = ({
  context,
  operation
}) => {
  const parsedBlock = parseBlock({
    block: operation.block,
    context,
    options: {
      normalize: !0,
      removeUnusedMarkDefs: !0,
      validateFields: !0
    }
  });
  if (!parsedBlock)
    throw new Error(`Failed to parse block ${JSON.stringify(operation.block)}`);
  const block = toSlateBlock(parsedBlock, {
    schemaTypes: context.schema
  });
  insertBlock({
    context,
    block,
    placement: operation.placement,
    select: operation.select ?? "start",
    at: operation.at,
    editor: operation.editor
  });
};
function insertBlock(options) {
  const {
    context,
    block,
    placement,
    select: select2,
    editor
  } = options, at = options.at ? toSlateRange({
    context: {
      schema: context.schema,
      value: editor.value,
      selection: options.at
    },
    blockIndexMap: editor.blockIndexMap
  }) : editor.selection;
  if (editor.children.length === 0) {
    insertNodeAt(editor, [0], block, select2);
    return;
  }
  const start2 = at ? Range.start(at) : Editor.start(editor, []), end2 = at ? Range.end(at) : Editor.end(editor, []), [startBlock, startBlockPath] = Array.from(Editor.nodes(editor, {
    at: start2,
    mode: "lowest",
    match: (node2, path2) => Element$2.isElement(node2) && path2.length <= start2.path.length
  })).at(0) ?? [void 0, void 0];
  let [endBlock, endBlockPath] = Array.from(Editor.nodes(editor, {
    at: end2,
    mode: "lowest",
    match: (node2, path2) => Element$2.isElement(node2) && path2.length <= end2.path.length
  })).at(0) ?? [void 0, void 0];
  if (!startBlock || !startBlockPath || !endBlock || !endBlockPath)
    throw new Error("Unable to insert block without a start and end block");
  if (placement === "before") {
    insertNodeAt(editor, startBlockPath, block, select2);
    return;
  }
  if (placement === "after") {
    insertNodeAt(editor, Path.next(endBlockPath), block, select2);
    return;
  }
  if (!at) {
    if (isEmptyTextBlock(context, endBlock)) {
      replaceEmptyTextBlock(editor, endBlockPath, block, select2);
      return;
    }
    if (editor.isTextBlock(block) && editor.isTextBlock(endBlock)) {
      const selectionBefore = Editor.end(editor, endBlockPath);
      insertTextBlockFragment(editor, block, selectionBefore), select2 === "start" ? setSelectionToPoint(editor, selectionBefore) : select2 === "none" && clearSelection(editor);
      return;
    }
    insertNodeAt(editor, Path.next(endBlockPath), block, select2);
    return;
  }
  if (Range.isExpanded(at) && !editor.isTextBlock(block)) {
    const atBeforeDelete = Editor.rangeRef(editor, at, {
      affinity: "inward"
    }), start22 = Range.start(at), startBlock2 = Node$1.get(editor, [start22.path[0]]), startOfBlock = Editor.start(editor, [start22.path[0]]), isAtStartOfBlock = Element$2.isElement(startBlock2) && Point.equals(start22, startOfBlock);
    deleteExpandedRange(editor, at);
    const atAfterDelete = atBeforeDelete.unref() ?? editor.selection, atBeforeInsert = atAfterDelete ? Editor.rangeRef(editor, atAfterDelete, {
      affinity: "inward"
    }) : void 0;
    if (atAfterDelete) {
      const insertPath = isAtStartOfBlock ? [atAfterDelete.anchor.path[0]] : [atAfterDelete.anchor.path[0] + 1];
      if (editor.apply({
        type: "insert_node",
        path: insertPath,
        node: block
      }), select2 !== "none") {
        const point2 = Editor.start(editor, insertPath);
        editor.apply({
          type: "set_selection",
          properties: editor.selection,
          newProperties: {
            anchor: point2,
            focus: point2
          }
        });
      }
    }
    const atAfterInsert = atBeforeInsert?.unref() ?? editor.selection;
    if (select2 === "none" && atAfterInsert && editor.apply({
      type: "set_selection",
      properties: editor.selection,
      newProperties: atAfterInsert
    }), !editor.isTextBlock(block) && atAfterDelete) {
      const emptyBlockPath = isAtStartOfBlock ? [atAfterDelete.anchor.path[0] + 1] : [atAfterDelete.anchor.path[0]];
      try {
        const potentiallyEmptyBlock = Node$1.get(editor, emptyBlockPath);
        Element$2.isElement(potentiallyEmptyBlock) && isEmptyTextBlock(context, potentiallyEmptyBlock) && editor.apply({
          type: "remove_node",
          path: emptyBlockPath,
          node: potentiallyEmptyBlock
        });
      } catch {
      }
    }
    return;
  }
  if (!editor.isTextBlock(block) && editor.isTextBlock(endBlock) && !Range.isExpanded(at)) {
    const selectionPoint = Range.start(at), blockPath = [selectionPoint.path[0]], blockStartPoint = Editor.start(editor, blockPath), blockEndPoint = Editor.end(editor, blockPath), isAtBlockStart = Point.equals(selectionPoint, blockStartPoint), isAtBlockEnd = Point.equals(selectionPoint, blockEndPoint);
    if (!isAtBlockStart && !isAtBlockEnd) {
      const currentBlock = Node$1.get(editor, blockPath), childIndex = selectionPoint.path[1], childOffset = selectionPoint.offset;
      if (childOffset > 0) {
        const textNode = Node$1.get(editor, selectionPoint.path);
        if (childOffset < textNode.text.length) {
          const {
            text: _2,
            ...properties
          } = textNode;
          editor.apply({
            type: "split_node",
            path: selectionPoint.path,
            position: childOffset,
            properties
          });
        }
      }
      const splitAtIndex = childOffset > 0 ? childIndex + 1 : childIndex, {
        children: _,
        ...blockProperties
      } = currentBlock;
      editor.apply({
        type: "split_node",
        path: blockPath,
        position: splitAtIndex,
        properties: blockProperties
      });
      const insertPath = [blockPath[0] + 1];
      if (editor.apply({
        type: "insert_node",
        path: insertPath,
        node: block
      }), select2 === "none") {
        const firstBlockEndPoint = Editor.end(editor, blockPath);
        editor.apply({
          type: "set_selection",
          properties: editor.selection,
          newProperties: {
            anchor: firstBlockEndPoint,
            focus: firstBlockEndPoint
          }
        });
      } else if (select2 === "start") {
        const point2 = Editor.start(editor, insertPath);
        editor.apply({
          type: "set_selection",
          properties: editor.selection,
          newProperties: {
            anchor: point2,
            focus: point2
          }
        });
      } else if (select2 === "end") {
        const point2 = Editor.end(editor, insertPath);
        editor.apply({
          type: "set_selection",
          properties: editor.selection,
          newProperties: {
            anchor: point2,
            focus: point2
          }
        });
      }
      return;
    }
  }
  if (editor.isTextBlock(endBlock) && editor.isTextBlock(block)) {
    let selectionStartPoint = Range.start(at), wasCrossBlockDeletion = !1;
    if (Range.isExpanded(at)) {
      const [start22, end22] = Range.edges(at), isCrossBlock = start22.path[0] !== end22.path[0];
      if (deleteExpandedRange(editor, at), isCrossBlock) {
        wasCrossBlockDeletion = !0;
        const startBlockPath2 = [start22.path[0]], mergedBlock = Node$1.get(editor, startBlockPath2);
        if (editor.isTextBlock(mergedBlock)) {
          const mergePoint = {
            path: [...startBlockPath2, start22.path[1]],
            offset: start22.offset
          };
          setSelectionToPoint(editor, mergePoint), selectionStartPoint = mergePoint;
        }
      }
      const [newEndBlock, newEndBlockPath] = Array.from(Editor.nodes(editor, {
        at: Editor.end(editor, []),
        mode: "lowest",
        match: (node2, path2) => Element$2.isElement(node2) && path2.length === 1
      })).at(-1) ?? [void 0, void 0];
      newEndBlock && newEndBlockPath && Element$2.isElement(newEndBlock) && (endBlock = newEndBlock, endBlockPath = newEndBlockPath);
    }
    if (!editor.isTextBlock(endBlock))
      return;
    if (isEmptyTextBlock(context, endBlock)) {
      replaceEmptyTextBlock(editor, endBlockPath, block, select2);
      return;
    }
    const endBlockChildKeys = endBlock.children.map((child) => child._key), endBlockMarkDefsKeys = endBlock.markDefs?.map((markDef) => markDef._key) ?? [], markDefKeyMap = /* @__PURE__ */ new Map(), adjustedMarkDefs = block.markDefs?.map((markDef) => {
      if (endBlockMarkDefsKeys.includes(markDef._key)) {
        const newKey = context.keyGenerator();
        return markDefKeyMap.set(markDef._key, newKey), {
          ...markDef,
          _key: newKey
        };
      }
      return markDef;
    }), adjustedChildren = block.children.map((child) => {
      if (isSpan(context, child)) {
        const marks2 = child.marks?.map((mark) => markDefKeyMap.get(mark) || mark) ?? [];
        if (!isEqualMarks(child.marks, marks2))
          return {
            ...child,
            _key: endBlockChildKeys.includes(child._key) ? context.keyGenerator() : child._key,
            marks: marks2
          };
      }
      return endBlockChildKeys.includes(child._key) ? {
        ...child,
        _key: context.keyGenerator()
      } : child;
    }), endBlockNode = Node$1.get(editor, endBlockPath);
    if (Element$2.isElement(endBlockNode) && editor.isTextBlock(endBlockNode)) {
      const properties = {
        markDefs: endBlockNode.markDefs
      }, newProperties = {
        markDefs: [...endBlock.markDefs ?? [], ...adjustedMarkDefs ?? []]
      };
      editor.apply({
        type: "set_node",
        path: endBlockPath,
        properties,
        newProperties
      });
    }
    const adjustedBlock = isEqualChildren(block.children, adjustedChildren) ? block : {
      ...block,
      children: adjustedChildren
    };
    if (select2 === "end") {
      const insertAt = editor.selection ? Range.end(editor.selection) : Editor.end(editor, endBlockPath);
      insertTextBlockFragment(editor, adjustedBlock, insertAt);
      return;
    }
    if (insertTextBlockFragment(editor, adjustedBlock, selectionStartPoint), select2 === "start")
      setSelectionToPoint(editor, selectionStartPoint);
    else if (select2 === "none")
      if (wasCrossBlockDeletion)
        setSelectionToPoint(editor, selectionStartPoint);
      else {
        const endBlockStartPoint = Editor.start(editor, endBlockPath);
        Point.equals(selectionStartPoint, endBlockStartPoint) || setSelectionToPoint(editor, selectionStartPoint);
      }
  } else {
    if (!editor.isTextBlock(endBlock)) {
      insertNodeAt(editor, [endBlockPath[0] + 1], block, select2);
      return;
    }
    const endBlockStartPoint = Editor.start(editor, endBlockPath), endBlockEndPoint = Editor.end(editor, endBlockPath), selectionStartPoint = Range.start(at), selectionEndPoint = Range.end(at);
    if (Range.isCollapsed(at) && Point.equals(selectionStartPoint, endBlockStartPoint)) {
      editor.apply({
        type: "insert_node",
        path: endBlockPath,
        node: block
      }), select2 !== "none" && setSelection(editor, endBlockPath, "start"), isEmptyTextBlock(context, endBlock) && removeNodeAt(editor, Path.next(endBlockPath));
      return;
    }
    if (Range.isCollapsed(at) && Point.equals(selectionEndPoint, endBlockEndPoint)) {
      const nextPath = [endBlockPath[0] + 1];
      editor.apply({
        type: "insert_node",
        path: nextPath,
        node: block
      }), select2 !== "none" && setSelection(editor, nextPath, "start");
      return;
    }
    if (Range.isExpanded(at) && Point.equals(selectionStartPoint, endBlockStartPoint) && Point.equals(selectionEndPoint, endBlockEndPoint)) {
      editor.apply({
        type: "insert_node",
        path: endBlockPath,
        node: block
      }), removeNodeAt(editor, Path.next(endBlockPath)), select2 !== "none" && setSelection(editor, endBlockPath, select2);
      return;
    }
    if (Range.isExpanded(at) && Point.equals(selectionStartPoint, endBlockStartPoint)) {
      const [, end22] = Range.edges(at), endNode = Node$1.get(editor, end22.path);
      end22.offset > 0 && editor.apply({
        type: "remove_text",
        path: end22.path,
        offset: 0,
        text: endNode.text.slice(0, end22.offset)
      });
      for (let i = end22.path[1] - 1; i >= 0; i--)
        removeNodeAt(editor, [...endBlockPath, i]);
      insertTextBlockFragment(editor, block, Editor.start(editor, endBlockPath)), select2 !== "none" && setSelection(editor, endBlockPath, select2);
      return;
    }
    if (Range.isExpanded(at) && Point.equals(selectionEndPoint, endBlockEndPoint)) {
      const [start22] = Range.edges(at), blockNode = Node$1.get(editor, endBlockPath);
      for (let i = blockNode.children.length - 1; i > start22.path[1]; i--)
        removeNodeAt(editor, [...endBlockPath, i]);
      const startNode = Node$1.get(editor, start22.path);
      start22.offset < startNode.text.length && editor.apply({
        type: "remove_text",
        path: start22.path,
        offset: start22.offset,
        text: startNode.text.slice(start22.offset)
      }), insertTextBlockFragment(editor, block, start22), select2 !== "none" && setSelection(editor, Path.next(endBlockPath), select2);
      return;
    }
    const [focusChild] = getFocusChild({
      editor
    });
    if (focusChild && editor.isTextSpan(focusChild)) {
      const startPoint = Range.start(at);
      if (editor.isTextBlock(block)) {
        const nodeToSplit = Node$1.get(editor, startPoint.path);
        if (Text$1.isText(nodeToSplit)) {
          const {
            text: _,
            ...properties
          } = nodeToSplit;
          editor.apply({
            type: "split_node",
            path: startPoint.path,
            position: startPoint.offset,
            properties
          });
        }
        insertTextBlockFragment(editor, block, startPoint), select2 === "none" ? setSelectionToRange(editor, at) : setSelection(editor, [endBlockPath[0] + 1], "start");
      } else {
        let currentPath = startPoint.path, currentOffset = startPoint.offset;
        const cursorPositionRef = Editor.pointRef(editor, startPoint, {
          affinity: "backward"
        }), blockPath = [currentPath[0]], firstBlockPathRef = Editor.pathRef(editor, blockPath), textNode = Node$1.get(editor, currentPath);
        if (Text$1.isText(textNode) && currentOffset > 0 && currentOffset < textNode.text.length) {
          const {
            text: _,
            ...properties
          } = textNode;
          editor.apply({
            type: "split_node",
            path: currentPath,
            position: currentOffset,
            properties
          }), currentPath = Path.next(currentPath), currentOffset = 0;
        }
        const splitAtIndex = currentOffset > 0 ? currentPath[1] + 1 : currentPath[1], blockToSplit = Node$1.get(editor, blockPath);
        if (splitAtIndex < blockToSplit.children.length && Element$2.isElement(blockToSplit)) {
          const {
            children: _,
            ...blockProperties
          } = blockToSplit;
          editor.apply({
            type: "split_node",
            path: blockPath,
            position: splitAtIndex,
            properties: blockProperties
          });
        }
        const currentFirstBlockPath = firstBlockPathRef.unref(), insertPath = currentFirstBlockPath ? [currentFirstBlockPath[0] + 1] : [blockPath[0] + 1];
        if (editor.apply({
          type: "insert_node",
          path: insertPath,
          node: block
        }), select2 === "start" || select2 === "end") {
          const point2 = Editor.start(editor, insertPath);
          editor.apply({
            type: "set_selection",
            properties: editor.selection,
            newProperties: {
              anchor: point2,
              focus: point2
            }
          });
        } else {
          const point2 = cursorPositionRef.unref();
          point2 && editor.apply({
            type: "set_selection",
            properties: editor.selection,
            newProperties: {
              anchor: point2,
              focus: point2
            }
          });
        }
      }
    } else {
      const nextPath = [endBlockPath[0] + 1];
      editor.apply({
        type: "insert_node",
        path: nextPath,
        node: block
      }), select2 === "none" ? setSelectionToRange(editor, at) : setSelection(editor, nextPath, select2);
    }
  }
}
function setSelection(editor, path2, position) {
  const point2 = position === "start" ? Editor.start(editor, path2) : Editor.end(editor, path2);
  editor.apply({
    type: "set_selection",
    properties: editor.selection,
    newProperties: {
      anchor: point2,
      focus: point2
    }
  });
}
function clearSelection(editor) {
  editor.selection && editor.apply({
    type: "set_selection",
    properties: editor.selection,
    newProperties: null
  });
}
function setSelectionToPoint(editor, point2) {
  editor.apply({
    type: "set_selection",
    properties: editor.selection,
    newProperties: {
      anchor: point2,
      focus: point2
    }
  });
}
function setSelectionToRange(editor, range2) {
  editor.apply({
    type: "set_selection",
    properties: editor.selection,
    newProperties: range2
  });
}
function insertNodeAt(editor, path2, node2, select2) {
  editor.apply({
    type: "insert_node",
    path: path2,
    node: node2
  }), select2 !== "none" && setSelection(editor, path2, select2);
}
function removeNodeAt(editor, path2) {
  const node2 = Node$1.get(editor, path2);
  editor.apply({
    type: "remove_node",
    path: path2,
    node: node2
  });
}
function replaceEmptyTextBlock(editor, blockPath, newBlock, select2) {
  const hadSelection = editor.selection !== null;
  if (editor.apply({
    type: "insert_node",
    path: blockPath,
    node: newBlock
  }), removeNodeAt(editor, Path.next(blockPath)), select2 === "none" && !hadSelection)
    return;
  const point2 = select2 === "end" ? Editor.end(editor, blockPath) : Editor.start(editor, blockPath);
  clearSelection(editor), editor.apply({
    type: "set_selection",
    properties: null,
    newProperties: {
      anchor: point2,
      focus: point2
    }
  });
}
function deleteSameBlockRange(editor, start2, end2) {
  const blockPath = [start2.path[0]];
  if (Path.equals(start2.path, end2.path)) {
    const textToRemove = Node$1.get(editor, start2.path).text.slice(start2.offset, end2.offset);
    editor.apply({
      type: "remove_text",
      path: start2.path,
      offset: start2.offset,
      text: textToRemove
    });
    return;
  }
  const startNode = Node$1.get(editor, start2.path);
  if (start2.offset < startNode.text.length) {
    const textToRemove = startNode.text.slice(start2.offset);
    editor.apply({
      type: "remove_text",
      path: start2.path,
      offset: start2.offset,
      text: textToRemove
    });
  }
  for (let i = end2.path[1] - 1; i > start2.path[1]; i--)
    removeNodeAt(editor, [...blockPath, i]);
  const newEndPath = [...blockPath, start2.path[1] + 1], endNode = Node$1.get(editor, newEndPath);
  if (end2.offset > 0) {
    const textToRemove = endNode.text.slice(0, end2.offset);
    editor.apply({
      type: "remove_text",
      path: newEndPath,
      offset: 0,
      text: textToRemove
    });
  }
  const startNodeAfter = Node$1.get(editor, start2.path), endNodeAfter = Node$1.get(editor, newEndPath);
  if (Text$1.isText(startNodeAfter) && Text$1.isText(endNodeAfter)) {
    const {
      text: _,
      ...properties
    } = endNodeAfter;
    editor.apply({
      type: "merge_node",
      path: newEndPath,
      position: startNodeAfter.text.length,
      properties
    });
  }
}
function deleteCrossBlockRange(editor, start2, end2) {
  const startBlockPath = [start2.path[0]];
  if (start2.path.length > 1) {
    const startNode = Node$1.get(editor, start2.path);
    if (start2.offset < startNode.text.length) {
      const textToRemove = startNode.text.slice(start2.offset);
      editor.apply({
        type: "remove_text",
        path: start2.path,
        offset: start2.offset,
        text: textToRemove
      });
    }
    const startBlock2 = Node$1.get(editor, startBlockPath);
    for (let i = startBlock2.children.length - 1; i > start2.path[1]; i--)
      removeNodeAt(editor, [...startBlockPath, i]);
  }
  for (let i = end2.path[0] - 1; i > start2.path[0]; i--)
    removeNodeAt(editor, [i]);
  const adjustedEndBlockPath = [start2.path[0] + 1];
  if (end2.path.length > 1) {
    for (let i = 0; i < end2.path[1]; i++)
      removeNodeAt(editor, [...adjustedEndBlockPath, 0]);
    const endNodePath = [...adjustedEndBlockPath, 0], endNode = Node$1.get(editor, endNodePath);
    if (end2.offset > 0) {
      const textToRemove = endNode.text.slice(0, end2.offset);
      editor.apply({
        type: "remove_text",
        path: endNodePath,
        offset: 0,
        text: textToRemove
      });
    }
  }
  const startBlock = Node$1.get(editor, startBlockPath), endBlock = Node$1.get(editor, adjustedEndBlockPath);
  if (editor.isTextBlock(startBlock) && editor.isTextBlock(endBlock)) {
    const {
      children: _,
      ...properties
    } = endBlock;
    editor.apply({
      type: "merge_node",
      path: adjustedEndBlockPath,
      position: startBlock.children.length,
      properties
    });
  }
}
function deleteExpandedRange(editor, range2) {
  const [start2, end2] = Range.edges(range2);
  start2.path[0] === end2.path[0] ? deleteSameBlockRange(editor, start2, end2) : deleteCrossBlockRange(editor, start2, end2);
}
function insertTextBlockFragment(editor, block, at) {
  if (!Element$2.isElement(block) || !editor.isTextBlock(block))
    return;
  if (at.offset > 0) {
    const textNode = Node$1.get(editor, at.path);
    if (Text$1.isText(textNode)) {
      const {
        text: _,
        ...properties
      } = textNode;
      editor.apply({
        type: "split_node",
        path: at.path,
        position: at.offset,
        properties
      });
    }
  }
  const parentPath = Path.parent(at.path);
  let insertIndex = at.path[at.path.length - 1] + (at.offset > 0 ? 1 : 0);
  for (const child of block.children) {
    const childPath = [...parentPath, insertIndex];
    editor.apply({
      type: "insert_node",
      path: childPath,
      node: child
    }), insertIndex++;
  }
}
const insertChildOperationImplementation = ({
  context,
  operation
}) => {
  const focus = operation.editor.selection?.focus, focusBlockIndex = focus?.path.at(0), focusChildIndex = focus?.path.at(1);
  if (focusBlockIndex === void 0 || focusChildIndex === void 0)
    throw new Error("Unable to insert child without a focus");
  const [focusBlock, focusBlockPath] = getFocusBlock({
    editor: operation.editor
  });
  if (!focus || !focusBlock || !focusBlockPath)
    throw new Error("Unable to insert child without a focus block");
  if (!isTextBlock(context, focusBlock))
    throw new Error("Unable to insert child into a non-text block");
  const markDefs = focusBlock.markDefs ?? [], markDefKeyMap = /* @__PURE__ */ new Map();
  for (const markDef of markDefs)
    markDefKeyMap.set(markDef._key, markDef._key);
  const span = parseSpan({
    span: operation.child,
    context,
    markDefKeyMap,
    options: {
      validateFields: !0
    }
  });
  if (span) {
    const [focusSpan] = getFocusSpan({
      editor: operation.editor
    });
    focusSpan ? Transforms.insertNodes(operation.editor, span, {
      at: focus,
      select: !0
    }) : Transforms.insertNodes(operation.editor, span, {
      at: [focusBlockIndex, focusChildIndex + 1],
      select: !0
    }), EDITOR_TO_PENDING_SELECTION.set(operation.editor, operation.editor.selection);
    return;
  }
  const inlineObject = parseInlineObject({
    inlineObject: operation.child,
    context,
    options: {
      validateFields: !0
    }
  });
  if (inlineObject) {
    const {
      _key,
      _type,
      ...rest
    } = inlineObject, [focusSpan] = getFocusSpan({
      editor: operation.editor
    });
    focusSpan ? Transforms.insertNodes(operation.editor, {
      _key,
      _type,
      children: [{
        _key: VOID_CHILD_KEY,
        _type: "span",
        text: "",
        marks: []
      }],
      value: rest,
      __inline: !0
    }, {
      at: focus,
      select: !0
    }) : Transforms.insertNodes(operation.editor, {
      _key,
      _type,
      children: [{
        _key: VOID_CHILD_KEY,
        _type: "span",
        text: "",
        marks: []
      }],
      value: rest,
      __inline: !0
    }, {
      at: [focusBlockIndex, focusChildIndex + 1],
      select: !0
    });
    return;
  }
  throw new Error("Unable to parse child");
}, insertTextOperationImplementation = ({
  operation
}) => {
  Transforms.insertText(operation.editor, operation.text);
}, moveBackwardOperationImplementation = ({
  operation
}) => {
  Transforms.move(operation.editor, {
    unit: "character",
    distance: operation.distance,
    reverse: !0
  });
}, moveBlockOperationImplementation = ({
  operation
}) => {
  const originKey = getBlockKeyFromSelectionPoint({
    path: operation.at
  });
  if (!originKey)
    throw new Error("Failed to get block key from selection point");
  const originBlockIndex = operation.editor.blockIndexMap.get(originKey);
  if (originBlockIndex === void 0)
    throw new Error("Failed to get block index from block key");
  const destinationKey = getBlockKeyFromSelectionPoint({
    path: operation.to
  });
  if (!destinationKey)
    throw new Error("Failed to get block key from selection point");
  const destinationBlockIndex = operation.editor.blockIndexMap.get(destinationKey);
  if (destinationBlockIndex === void 0)
    throw new Error("Failed to get block index from block key");
  Transforms.moveNodes(operation.editor, {
    at: [originBlockIndex],
    to: [destinationBlockIndex],
    mode: "highest"
  });
}, moveForwardOperationImplementation = ({
  operation
}) => {
  Transforms.move(operation.editor, {
    unit: "character",
    distance: operation.distance
  });
}, selectOperationImplementation = ({
  context,
  operation
}) => {
  const newSelection = toSlateRange({
    context: {
      schema: context.schema,
      value: operation.editor.value,
      selection: operation.at
    },
    blockIndexMap: operation.editor.blockIndexMap
  });
  newSelection ? Transforms.select(operation.editor, newSelection) : Transforms.deselect(operation.editor), IS_FOCUSED.get(operation.editor) && IS_READ_ONLY.get(operation.editor) && IS_FOCUSED.set(operation.editor, !1);
}, operationImplementations = {
  "annotation.add": addAnnotationOperationImplementation,
  "annotation.remove": removeAnnotationOperationImplementation,
  "block.set": blockSetOperationImplementation,
  "block.unset": blockUnsetOperationImplementation,
  "child.set": childSetOperationImplementation,
  "child.unset": childUnsetOperationImplementation,
  "decorator.add": decoratorAddOperationImplementation,
  "decorator.remove": decoratorRemoveOperationImplementation,
  delete: deleteOperationImplementation,
  "history.redo": historyRedoOperationImplementation,
  "history.undo": historyUndoOperationImplementation,
  "insert.block": insertBlockOperationImplementation,
  "insert.child": insertChildOperationImplementation,
  "insert.text": insertTextOperationImplementation,
  "move.backward": moveBackwardOperationImplementation,
  "move.block": moveBlockOperationImplementation,
  "move.forward": moveForwardOperationImplementation,
  select: selectOperationImplementation
};
function performOperation({
  context,
  operation
}) {
  const perform = () => {
    try {
      switch (operation.type) {
        case "annotation.add": {
          operationImplementations["annotation.add"]({
            context,
            operation
          });
          break;
        }
        case "annotation.remove": {
          operationImplementations["annotation.remove"]({
            context,
            operation
          });
          break;
        }
        case "block.set": {
          operationImplementations["block.set"]({
            context,
            operation
          });
          break;
        }
        case "block.unset": {
          operationImplementations["block.unset"]({
            context,
            operation
          });
          break;
        }
        case "child.set": {
          operationImplementations["child.set"]({
            context,
            operation
          });
          break;
        }
        case "child.unset": {
          operationImplementations["child.unset"]({
            context,
            operation
          });
          break;
        }
        case "decorator.add": {
          operationImplementations["decorator.add"]({
            context,
            operation
          });
          break;
        }
        case "decorator.remove": {
          operationImplementations["decorator.remove"]({
            context,
            operation
          });
          break;
        }
        case "delete": {
          operationImplementations.delete({
            context,
            operation
          });
          break;
        }
        case "history.redo": {
          operationImplementations["history.redo"]({
            context,
            operation
          });
          break;
        }
        case "history.undo": {
          operationImplementations["history.undo"]({
            context,
            operation
          });
          break;
        }
        case "insert.block": {
          operationImplementations["insert.block"]({
            context,
            operation
          });
          break;
        }
        case "insert.child": {
          operationImplementations["insert.child"]({
            context,
            operation
          });
          break;
        }
        case "insert.text": {
          operationImplementations["insert.text"]({
            context,
            operation
          });
          break;
        }
        case "move.backward": {
          operationImplementations["move.backward"]({
            context,
            operation
          });
          break;
        }
        case "move.block": {
          operationImplementations["move.block"]({
            context,
            operation
          });
          break;
        }
        case "move.forward": {
          operationImplementations["move.forward"]({
            context,
            operation
          });
          break;
        }
        default: {
          operationImplementations.select({
            context,
            operation
          });
          break;
        }
      }
    } catch (error) {
      console.error(new Error(`Performing "${operation.type}" failed due to: ${error instanceof Error ? error.message : error}`));
    }
  };
  Editor.isNormalizing(operation.editor) ? Editor.withoutNormalizing(operation.editor, perform) : perform();
}
function withPerformingBehaviorOperation(editor, fn) {
  const prev = editor.isPerformingBehaviorOperation;
  editor.isPerformingBehaviorOperation = !0, fn(), editor.isPerformingBehaviorOperation = prev;
}
function withoutNormalizingConditional(editor, predicate, fn) {
  predicate() ? Editor.withoutNormalizing(editor, fn) : fn();
}
const abstractAnnotationBehaviors = [defineBehavior({
  on: "annotation.set",
  guard: ({
    snapshot,
    event
  }) => {
    const blockKey = event.at[0]._key, markDefKey = event.at[2]._key, block = getFocusTextBlock({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: {
          anchor: {
            path: [{
              _key: blockKey
            }],
            offset: 0
          },
          focus: {
            path: [{
              _key: blockKey
            }],
            offset: 0
          }
        }
      }
    });
    if (!block)
      return !1;
    const updatedMarkDefs = block.node.markDefs?.map((markDef) => markDef._key === markDefKey ? {
      ...markDef,
      ...event.props
    } : markDef);
    return {
      blockKey,
      updatedMarkDefs
    };
  },
  actions: [(_, {
    blockKey,
    updatedMarkDefs
  }) => [raise({
    type: "block.set",
    at: [{
      _key: blockKey
    }],
    props: {
      markDefs: updatedMarkDefs
    }
  })]]
}), defineBehavior({
  on: "annotation.toggle",
  guard: ({
    snapshot,
    event
  }) => {
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    };
    return isActiveAnnotation(event.annotation.name)(adjustedSnapshot);
  },
  actions: [({
    event
  }) => [raise({
    type: "annotation.remove",
    annotation: event.annotation,
    at: event.at
  })]]
}), defineBehavior({
  on: "annotation.toggle",
  guard: ({
    snapshot,
    event
  }) => {
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    };
    return !isActiveAnnotation(event.annotation.name)(adjustedSnapshot);
  },
  actions: [({
    event
  }) => [raise({
    type: "annotation.add",
    annotation: event.annotation,
    at: event.at
  })]]
})], abstractDecoratorBehaviors = [defineBehavior({
  on: "decorator.toggle",
  guard: ({
    snapshot,
    event
  }) => {
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    };
    return isActiveDecorator(event.decorator)(adjustedSnapshot);
  },
  actions: [({
    event
  }) => [raise({
    type: "decorator.remove",
    decorator: event.decorator,
    at: event.at
  })]]
}), defineBehavior({
  on: "decorator.toggle",
  guard: ({
    snapshot,
    event
  }) => {
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    };
    return !isActiveDecorator(event.decorator)(adjustedSnapshot);
  },
  actions: [({
    event
  }) => [raise({
    ...event,
    type: "decorator.add"
  })]]
})], abstractDeleteBehaviors = [defineBehavior({
  on: "delete.backward",
  guard: ({
    snapshot
  }) => snapshot.context.selection,
  actions: [({
    event
  }) => [raise({
    type: "delete",
    direction: "backward",
    unit: event.unit
  })]]
}), defineBehavior({
  on: "delete",
  guard: ({
    snapshot,
    event
  }) => {
    if (event.direction !== "backward")
      return !1;
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    }, previousBlock = getPreviousBlock(adjustedSnapshot), focusTextBlock = getFocusTextBlock(adjustedSnapshot);
    if (!previousBlock || !focusTextBlock || !isAtTheStartOfBlock(focusTextBlock)(adjustedSnapshot))
      return !1;
    const previousBlockEndPoint = getBlockEndPoint({
      context: snapshot.context,
      block: previousBlock
    });
    return isTextBlock(snapshot.context, previousBlock.node) ? {
      previousBlockEndPoint,
      focusTextBlock
    } : !1;
  },
  actions: [(_, {
    previousBlockEndPoint,
    focusTextBlock
  }) => [raise({
    type: "delete.block",
    at: focusTextBlock.path
  }), raise({
    type: "select",
    at: {
      anchor: previousBlockEndPoint,
      focus: previousBlockEndPoint
    }
  }), raise({
    type: "insert.block",
    block: focusTextBlock.node,
    placement: "auto",
    select: "start"
  })]]
}), defineBehavior({
  on: "delete.forward",
  guard: ({
    snapshot
  }) => snapshot.context.selection,
  actions: [({
    event
  }) => [raise({
    type: "delete",
    direction: "forward",
    unit: event.unit
  })]]
}), defineBehavior({
  on: "delete",
  guard: ({
    snapshot,
    event
  }) => {
    if (event.direction !== "forward")
      return !1;
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const nextBlock = getNextBlock({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    }), focusTextBlock = getFocusTextBlock({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    });
    if (!nextBlock || !focusTextBlock || !isEmptyTextBlock(snapshot.context, focusTextBlock.node))
      return !1;
    const nextBlockStartPoint = getBlockStartPoint({
      context: snapshot.context,
      block: nextBlock
    });
    return {
      focusTextBlock,
      nextBlockStartPoint
    };
  },
  actions: [(_, {
    focusTextBlock,
    nextBlockStartPoint
  }) => [raise({
    type: "delete.block",
    at: focusTextBlock.path
  }), raise({
    type: "select",
    at: {
      anchor: nextBlockStartPoint,
      focus: nextBlockStartPoint
    }
  })]]
}), defineBehavior({
  on: "delete",
  guard: ({
    snapshot,
    event
  }) => {
    if (event.direction !== "forward")
      return !1;
    const at = event.at ?? snapshot.context.selection;
    if (!at)
      return !1;
    const adjustedSnapshot = {
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: at
      }
    }, nextBlock = getNextBlock(adjustedSnapshot), focusTextBlock = getFocusTextBlock(adjustedSnapshot);
    return !nextBlock || !focusTextBlock || !isAtTheEndOfBlock(focusTextBlock)(adjustedSnapshot) || !isTextBlock(snapshot.context, nextBlock.node) ? !1 : {
      nextBlock
    };
  },
  actions: [(_, {
    nextBlock
  }) => [raise({
    type: "delete.block",
    at: nextBlock.path
  }), raise({
    type: "insert.block",
    block: nextBlock.node,
    placement: "auto",
    select: "none"
  })]]
}), defineBehavior({
  on: "delete.block",
  actions: [({
    event
  }) => [raise({
    type: "delete",
    at: {
      anchor: {
        path: event.at,
        offset: 0
      },
      focus: {
        path: event.at,
        offset: 0
      }
    },
    unit: "block"
  })]]
}), defineBehavior({
  on: "delete.child",
  guard: ({
    snapshot,
    event
  }) => {
    const focusChild = getFocusChild$1({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: {
          anchor: {
            path: event.at,
            offset: 0
          },
          focus: {
            path: event.at,
            offset: 0
          }
        }
      }
    });
    return focusChild ? isSpan(snapshot.context, focusChild.node) ? {
      selection: {
        anchor: {
          path: event.at,
          offset: 0
        },
        focus: {
          path: event.at,
          offset: focusChild.node.text.length
        }
      }
    } : {
      selection: {
        anchor: {
          path: event.at,
          offset: 0
        },
        focus: {
          path: event.at,
          offset: 0
        }
      }
    } : !1;
  },
  actions: [(_, {
    selection
  }) => [raise({
    type: "delete",
    at: selection
  })]]
}), defineBehavior({
  on: "delete.text",
  actions: [({
    event
  }) => [raise({
    ...event,
    type: "delete"
  })]]
})], mimeTypePriority = ["application/x-portable-text", "application/json", "text/markdown", "text/html", "text/plain"];
function getFirstAvailableData({
  dataTransfer,
  startAfter
}) {
  const startIndex = startAfter ? mimeTypePriority.indexOf(startAfter) + 1 : 0;
  for (let index = startIndex; index < mimeTypePriority.length; index++) {
    const mimeType = mimeTypePriority.at(index);
    if (!mimeType)
      continue;
    const data = dataTransfer.getData(mimeType);
    if (data)
      return {
        mimeType,
        data
      };
  }
}
const abstractDeserializeBehaviors = [
  defineBehavior({
    on: "deserialize",
    guard: ({
      event
    }) => {
      const availableData = getFirstAvailableData({
        dataTransfer: event.originEvent.originEvent.dataTransfer
      });
      return availableData ? {
        type: "deserialize.data",
        mimeType: availableData.mimeType,
        data: availableData.data,
        originEvent: event.originEvent
      } : !1;
    },
    actions: [(_, deserializeEvent) => [raise(deserializeEvent)]]
  }),
  defineBehavior({
    on: "deserialize",
    actions: [({
      event
    }) => [raise({
      type: "deserialization.failure",
      mimeType: "*/*",
      reason: "No Behavior was able to handle the incoming data",
      originEvent: event.originEvent
    })]]
  }),
  defineBehavior({
    on: "deserialize.data",
    guard: ({
      event
    }) => {
      if (event.mimeType !== "text/html")
        return !1;
      const plainText = event.originEvent.originEvent.dataTransfer.getData("text/plain");
      return event.data !== plainText ? !1 : {
        type: "deserialize.data",
        mimeType: "text/plain",
        data: plainText,
        originEvent: event.originEvent
      };
    },
    actions: [(_, deserializeDataEvent) => [raise(deserializeDataEvent)]]
  }),
  defineBehavior({
    on: "deserialize.data",
    guard: ({
      snapshot,
      event
    }) => {
      const converter = snapshot.context.converters.find((converter2) => converter2.mimeType === event.mimeType);
      return converter ? converter.deserialize({
        snapshot,
        event: {
          type: "deserialize",
          data: event.data
        }
      }) : !1;
    },
    actions: [({
      event
    }, deserializeEvent) => [raise({
      ...deserializeEvent,
      originEvent: event.originEvent
    })]]
  }),
  /**
   * If we are pasting text/plain into a text block then we can probably
   * assume that the intended behavior is that the pasted text inherits
   * formatting from the text it's pasted into.
   */
  defineBehavior({
    on: "deserialization.success",
    guard: ({
      snapshot,
      event
    }) => {
      if (getFocusTextBlock(snapshot) && event.mimeType === "text/plain" && event.originEvent.type !== "drag.drop") {
        const activeDecorators = getActiveDecorators(snapshot);
        return {
          activeAnnotations: getActiveAnnotations(snapshot),
          activeDecorators,
          textRuns: event.data.flatMap((block) => isTextBlock(snapshot.context, block) ? [getTextBlockText(block)] : [])
        };
      }
      return !1;
    },
    actions: [(_, {
      activeAnnotations,
      activeDecorators,
      textRuns
    }) => textRuns.flatMap((textRun, index) => index !== textRuns.length - 1 ? [raise({
      type: "insert.span",
      text: textRun,
      decorators: activeDecorators,
      annotations: activeAnnotations.map(({
        _key,
        _type,
        ...value
      }) => ({
        name: _type,
        value
      }))
    }), raise({
      type: "insert.break"
    })] : [raise({
      type: "insert.span",
      text: textRun,
      decorators: activeDecorators,
      annotations: activeAnnotations.map(({
        _key,
        _type,
        ...value
      }) => ({
        name: _type,
        value
      }))
    })])]
  }),
  defineBehavior({
    on: "deserialization.success",
    actions: [({
      event
    }) => [raise({
      type: "insert.blocks",
      blocks: event.data,
      placement: "auto"
    })]]
  }),
  defineBehavior({
    on: "deserialization.failure",
    guard: ({
      event
    }) => {
      if (event.mimeType === "*/*")
        return !1;
      const availableData = getFirstAvailableData({
        dataTransfer: event.originEvent.originEvent.dataTransfer,
        startAfter: event.mimeType
      });
      return availableData ? {
        type: "deserialize.data",
        mimeType: availableData.mimeType,
        data: availableData.data,
        originEvent: event.originEvent
      } : !1;
    },
    actions: [(_, deserializeDataEvent) => [raise(deserializeDataEvent)]]
  }),
  defineBehavior({
    on: "deserialization.failure",
    actions: [({
      event
    }) => [{
      type: "effect",
      effect: () => {
        console.warn(`Deserialization of ${event.mimeType} failed with reason "${event.reason}"`);
      }
    }]]
  })
], abstractInputBehaviors = [
  defineBehavior({
    on: "input.*",
    guard: ({
      snapshot
    }) => isSelectionExpanded(snapshot),
    actions: [({
      event
    }) => [raise({
      type: "delete"
    }), forward(event)]]
  }),
  /**
   * Handle input events where HTML equals plain text (e.g., Safari autocorrect).
   * In this case, we use insert.text to preserve existing marks.
   */
  defineBehavior({
    on: "input.*",
    guard: ({
      event
    }) => {
      const text = event.originEvent.dataTransfer.getData("text/plain"), html = event.originEvent.dataTransfer.getData("text/html"), types = event.originEvent.dataTransfer.types;
      return !text || text.includes(`
`) ? !1 : types.length === 1 ? {
        text
      } : types.length > 2 ? !1 : html && text === html ? {
        text
      } : !1;
    },
    actions: [(_, {
      text
    }) => [raise({
      type: "insert.text",
      text
    })]]
  }),
  defineBehavior({
    on: "input.*",
    actions: [({
      event
    }) => [raise({
      type: "deserialize",
      originEvent: event
    })]]
  })
];
function getUniqueBlockKey(blockKey) {
  return (snapshot) => !blockKey || snapshot.blockIndexMap.has(blockKey) ? snapshot.context.keyGenerator() : blockKey;
}
const abstractInsertBehaviors = [
  defineBehavior({
    on: "insert.blocks",
    guard: ({
      event
    }) => {
      const onlyBlock = event.blocks.length === 1 ? event.blocks.at(0) : void 0;
      return onlyBlock ? {
        onlyBlock
      } : !1;
    },
    actions: [({
      event
    }, {
      onlyBlock
    }) => [raise({
      type: "insert.block",
      block: onlyBlock,
      placement: event.placement,
      select: event.select ?? "end",
      ...event.at ? {
        at: event.at
      } : {}
    })]]
  }),
  defineBehavior({
    on: "insert.blocks",
    guard: ({
      event
    }) => event.placement === "before" || event.placement === "after",
    actions: [({
      snapshot,
      event
    }) => {
      let firstBlockKey, lastBlockKey, previousBlockKey;
      const actions = [];
      let index = -1;
      for (const block of event.blocks) {
        index++;
        const key = getUniqueBlockKey(block._key)(snapshot);
        index === 0 && (firstBlockKey = key), index === event.blocks.length - 1 && (lastBlockKey = key), actions.push(raise({
          type: "insert.block",
          block: key !== block._key ? {
            ...block,
            _key: key
          } : block,
          placement: event.placement === "after" ? "after" : index === 0 ? "before" : "after",
          select: "none",
          ...previousBlockKey ? {
            at: {
              anchor: {
                path: [{
                  _key: previousBlockKey
                }],
                offset: 0
              },
              focus: {
                path: [{
                  _key: previousBlockKey
                }],
                offset: 0
              }
            }
          } : event.at ? {
            at: event.at
          } : {}
        })), previousBlockKey = key;
      }
      const select2 = event.select ?? "end";
      return select2 === "start" && firstBlockKey && actions.push(raise({
        type: "select.block",
        at: [{
          _key: firstBlockKey
        }],
        select: "start"
      })), select2 === "end" && lastBlockKey && actions.push(raise({
        type: "select.block",
        at: [{
          _key: lastBlockKey
        }],
        select: "end"
      })), actions;
    }]
  }),
  defineBehavior({
    on: "insert.blocks",
    guard: ({
      snapshot,
      event
    }) => {
      if (event.placement !== "auto")
        return !1;
      const at = event.at ?? snapshot.context.selection;
      if (!at)
        return !1;
      const adjustedSnapshot = {
        ...snapshot,
        context: {
          ...snapshot.context,
          selection: at
        }
      }, focusTextBlock = getFocusTextBlock(adjustedSnapshot);
      if (!focusTextBlock || isEmptyTextBlock(snapshot.context, focusTextBlock.node))
        return !1;
      const focusBlockStartPoint = getBlockStartPoint({
        context: snapshot.context,
        block: focusTextBlock
      }), focusBlockEndPoint = getBlockEndPoint({
        context: snapshot.context,
        block: focusTextBlock
      }), focusTextBlockAfter = sliceTextBlock({
        context: {
          schema: snapshot.context.schema,
          selection: {
            anchor: at.focus,
            focus: focusBlockEndPoint
          }
        },
        block: focusTextBlock.node
      }), isFirstBlockTextBlock = isTextBlock(snapshot.context, event.blocks.at(0));
      return {
        focusTextBlock,
        focusBlockStartPoint,
        focusBlockEndPoint,
        focusTextBlockAfter,
        at,
        originalSelection: snapshot.context.selection,
        isFirstBlockTextBlock
      };
    },
    actions: [({
      snapshot,
      event
    }, {
      focusTextBlock,
      focusBlockEndPoint,
      focusTextBlockAfter,
      at,
      focusBlockStartPoint,
      isFirstBlockTextBlock,
      originalSelection
    }) => {
      let previousBlockKey, firstBlockKey;
      const actions = [];
      let index = -1;
      for (const block of event.blocks) {
        if (index++, index === 0) {
          isEqualSelectionPoints(at.focus, focusBlockEndPoint) || actions.push(raise({
            type: "delete",
            at: {
              anchor: at.focus,
              focus: focusBlockEndPoint
            }
          }));
          const key2 = getUniqueBlockKey(block._key)(snapshot), deletingEndToEnd = isEqualSelectionPoints(at.focus, focusBlockStartPoint);
          isTextBlock(snapshot.context, block) && !deletingEndToEnd ? (firstBlockKey = focusTextBlock.node._key, previousBlockKey = focusTextBlock.node._key) : (firstBlockKey = key2, previousBlockKey = key2), actions.push(raise({
            type: "insert.block",
            block: key2 !== block._key ? {
              ...block,
              _key: key2
            } : block,
            placement: "auto",
            select: "end",
            ...event.at ? {
              at: event.at
            } : {}
          }));
          continue;
        }
        if (index === event.blocks.length - 1) {
          actions.push(raise({
            type: "insert.block",
            block,
            placement: "after",
            select: "end",
            at: previousBlockKey ? {
              anchor: {
                path: [{
                  _key: previousBlockKey
                }],
                offset: 0
              },
              focus: {
                path: [{
                  _key: previousBlockKey
                }],
                offset: 0
              }
            } : void 0
          }));
          continue;
        }
        const key = getUniqueBlockKey(block._key)(snapshot);
        actions.push(raise({
          type: "insert.block",
          block: key !== block._key ? {
            ...block,
            _key: key
          } : block,
          placement: "after",
          select: previousBlockKey ? "none" : "end",
          at: previousBlockKey ? {
            anchor: {
              path: [{
                _key: previousBlockKey
              }],
              offset: 0
            },
            focus: {
              path: [{
                _key: previousBlockKey
              }],
              offset: 0
            }
          } : void 0
        })), previousBlockKey = key;
      }
      return isEmptyTextBlock(snapshot.context, focusTextBlockAfter) || actions.push(raise({
        type: "insert.block",
        block: focusTextBlockAfter,
        placement: "auto",
        select: event.select === "end" ? "none" : "end"
      })), event.select === "none" && actions.push(raise({
        type: "select",
        at: originalSelection
      })), event.select === "start" && ((isEqualSelectionPoints(at.focus, focusBlockStartPoint) || !isFirstBlockTextBlock) && firstBlockKey ? actions.push(raise({
        type: "select.block",
        at: [{
          _key: firstBlockKey
        }],
        select: "start"
      })) : actions.push(raise({
        type: "select",
        at: {
          anchor: at.focus,
          focus: at.focus
        }
      }))), actions;
    }]
  }),
  defineBehavior({
    on: "insert.blocks",
    guard: ({
      snapshot,
      event
    }) => event.placement !== "auto" ? !1 : {
      originalSelection: snapshot.context.selection
    },
    actions: [({
      snapshot,
      event
    }, {
      originalSelection
    }) => {
      let firstBlockKey, lastBlockKey, previousBlockKey;
      const actions = [];
      let index = -1;
      for (const block of event.blocks) {
        index++;
        const key = getUniqueBlockKey(block._key)(snapshot);
        index === 0 && (firstBlockKey = key), index === event.blocks.length - 1 && (lastBlockKey = key), actions.push(raise({
          type: "insert.block",
          block: key !== block._key ? {
            ...block,
            _key: key
          } : block,
          placement: index === 0 ? "auto" : "after",
          select: "none",
          ...previousBlockKey ? {
            at: {
              anchor: {
                path: [{
                  _key: previousBlockKey
                }],
                offset: 0
              },
              focus: {
                path: [{
                  _key: previousBlockKey
                }],
                offset: 0
              }
            }
          } : event.at ? {
            at: event.at
          } : {}
        })), previousBlockKey = key;
      }
      const select2 = event.select ?? "end";
      return select2 === "none" ? actions.push(raise({
        type: "select",
        at: originalSelection
      })) : select2 === "start" && firstBlockKey ? actions.push(raise({
        type: "select.block",
        at: [{
          _key: firstBlockKey
        }],
        select: "start"
      })) : lastBlockKey && actions.push(raise({
        type: "select.block",
        at: [{
          _key: lastBlockKey
        }],
        select: "end"
      })), actions;
    }]
  }),
  defineBehavior({
    on: "insert.break",
    actions: [() => [raise({
      type: "split"
    })]]
  }),
  defineBehavior({
    on: "insert.child",
    guard: ({
      snapshot
    }) => {
      const lastBlock = getLastBlock$1(snapshot);
      return !lastBlock || snapshot.context.selection ? !1 : {
        lastBlockEndPoint: getBlockEndPoint({
          context: snapshot.context,
          block: lastBlock
        })
      };
    },
    actions: [({
      event
    }, {
      lastBlockEndPoint
    }) => [raise({
      type: "select",
      at: {
        anchor: lastBlockEndPoint,
        focus: lastBlockEndPoint
      }
    }), raise(event)]]
  }),
  defineBehavior({
    on: "insert.child",
    guard: ({
      snapshot
    }) => {
      const focusTextBlock = getFocusTextBlock(snapshot);
      return snapshot.context.selection && !focusTextBlock;
    },
    actions: [({
      snapshot,
      event
    }) => [raise({
      type: "insert.block",
      block: {
        _type: snapshot.context.schema.block.name,
        children: [{
          _type: snapshot.context.schema.span.name,
          text: "",
          marks: []
        }]
      },
      placement: "auto",
      select: "end"
    }), raise(event)]]
  }),
  defineBehavior({
    on: "insert.inline object",
    actions: [({
      event
    }) => [raise({
      type: "insert.child",
      child: {
        _type: event.inlineObject.name,
        ...event.inlineObject.value
      }
    })]]
  }),
  defineBehavior({
    on: "insert.soft break",
    actions: [() => [raise({
      type: "insert.text",
      text: `
`
    })]]
  }),
  defineBehavior({
    on: "insert.span",
    guard: ({
      snapshot
    }) => !getFocusTextBlock(snapshot),
    actions: [({
      snapshot,
      event
    }) => [raise({
      type: "insert.block",
      block: {
        _type: snapshot.context.schema.block.name,
        children: [{
          _type: snapshot.context.schema.span.name,
          text: "",
          marks: []
        }]
      },
      placement: "auto",
      select: "end"
    }), raise(event)]]
  }),
  defineBehavior({
    on: "insert.span",
    guard: ({
      snapshot,
      event
    }) => {
      const focusTextBlock = getFocusTextBlock(snapshot);
      return {
        markDefs: event.annotations?.map((annotation) => ({
          _type: annotation.name,
          _key: snapshot.context.keyGenerator(),
          ...annotation.value
        })) ?? [],
        focusTextBlock
      };
    },
    actions: [({
      snapshot,
      event
    }, {
      markDefs,
      focusTextBlock
    }) => [...focusTextBlock ? [raise({
      type: "block.set",
      at: focusTextBlock.path,
      props: {
        markDefs: [...focusTextBlock.node.markDefs ?? [], ...markDefs]
      }
    })] : [], raise({
      type: "insert.child",
      child: {
        _type: snapshot.context.schema.span.name,
        text: event.text,
        marks: [...event.decorators ?? [], ...markDefs.map((markDef) => markDef._key)]
      }
    })]]
  }),
  /**
   * If there's an expanded selection, then we delete the selection before we
   * insert the text.
   */
  defineBehavior({
    on: "insert.text",
    guard: ({
      snapshot
    }) => isSelectionExpanded(snapshot),
    actions: [({
      event
    }) => [raise({
      type: "delete"
    }), raise(event)]]
  }),
  /**
   * If there's no selection, then we select the end of the editor before we
   * we insert the text.
   */
  defineBehavior({
    on: "insert.text",
    guard: ({
      snapshot
    }) => {
      if (snapshot.context.selection)
        return !1;
      const lastBlok = getLastBlock$1(snapshot);
      return lastBlok ? {
        endPoint: getBlockEndPoint({
          context: snapshot.context,
          block: lastBlok
        })
      } : !1;
    },
    actions: [({
      event
    }, {
      endPoint
    }) => [raise({
      type: "select",
      at: {
        anchor: endPoint,
        focus: endPoint
      }
    }), raise(event)]]
  })
], shiftLeft = createKeyboardShortcut({
  default: [{
    key: "ArrowLeft",
    shift: !0,
    meta: !1,
    ctrl: !1,
    alt: !1
  }]
}), abstractKeyboardBehaviors = [
  /**
   * When Backspace is pressed on an inline object, Slate will raise a
   * `delete.backward` event with `unit: 'block'`. This is wrong and this
   * Behavior adjusts that.
   */
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => defaultKeyboardShortcuts.backspace.guard(event.originEvent) && isSelectionCollapsed$1(snapshot) && getFocusInlineObject(snapshot),
    actions: [() => [raise({
      type: "delete.backward",
      unit: "character"
    })]]
  }),
  /**
   * When Delete is pressed on an inline object, Slate will raise a
   * `delete.forward` event with `unit: 'block'`. This is wrong and this
   * Behavior adjusts that.
   */
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => defaultKeyboardShortcuts.delete.guard(event.originEvent) && isSelectionCollapsed$1(snapshot) && getFocusInlineObject(snapshot),
    actions: [() => [raise({
      type: "delete.forward",
      unit: "character"
    })]]
  }),
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      event
    }) => defaultKeyboardShortcuts.deleteWord.backward.guard(event.originEvent),
    actions: [() => [raise({
      type: "delete.backward",
      unit: "word"
    })]]
  }),
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      event
    }) => defaultKeyboardShortcuts.deleteWord.forward.guard(event.originEvent),
    actions: [() => [raise({
      type: "delete.forward",
      unit: "word"
    })]]
  }),
  /**
   * Allow raising an `insert.break` event when pressing Enter on an inline
   * object.
   */
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => defaultKeyboardShortcuts.break.guard(event.originEvent) && isSelectionCollapsed$1(snapshot) && getFocusInlineObject(snapshot),
    actions: [() => [raise({
      type: "insert.break"
    })]]
  }),
  /**
   * On Firefox, Enter might collapse the selection. To mitigate this, we
   * `raise` an `insert.break` event manually.
   */
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => defaultKeyboardShortcuts.break.guard(event.originEvent) && isSelectionExpanded(snapshot),
    actions: [() => [raise({
      type: "insert.break"
    })]]
  }),
  /**
   * On WebKit, Shift+Enter results in an `insertParagraph` input event rather
   * than an `insertLineBreak` input event. This Behavior makes sure we catch
   * that `keyboard.keydown` event beforehand and raise an `insert.soft break` manually.
   */
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      event
    }) => defaultKeyboardShortcuts.lineBreak.guard(event.originEvent),
    actions: [() => [raise({
      type: "insert.soft break"
    })]]
  }),
  /**
   * Manual handling of undo shortcuts.
   */
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      event
    }) => defaultKeyboardShortcuts.history.undo.guard(event.originEvent),
    actions: [() => [raise({
      type: "history.undo"
    })]]
  }),
  /**
   * Manual handling of redo shortcuts.
   */
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      event
    }) => defaultKeyboardShortcuts.history.redo.guard(event.originEvent),
    actions: [() => [raise({
      type: "history.redo"
    })]]
  }),
  /**
   * Fix edge case where Shift+ArrowLeft didn't reduce a selection hanging
   * onto an empty text block.
   */
  defineBehavior({
    on: "keyboard.keydown",
    guard: ({
      snapshot,
      event
    }) => {
      if (!snapshot.context.selection || !shiftLeft.guard(event.originEvent))
        return !1;
      const focusBlock = getFocusBlock$1(snapshot);
      if (!focusBlock)
        return !1;
      const previousBlock = getPreviousBlock({
        ...snapshot,
        context: {
          ...snapshot.context,
          selection: {
            anchor: {
              path: focusBlock.path,
              offset: 0
            },
            focus: {
              path: focusBlock.path,
              offset: 0
            }
          }
        }
      });
      return previousBlock && isTextBlock(snapshot.context, focusBlock.node) && snapshot.context.selection.focus.offset === 0 && isEmptyTextBlock(snapshot.context, focusBlock.node) ? {
        previousBlock,
        selection: snapshot.context.selection
      } : !1;
    },
    actions: [({
      snapshot
    }, {
      previousBlock,
      selection
    }) => [raise({
      type: "select",
      at: {
        anchor: selection.anchor,
        focus: getBlockEndPoint({
          context: snapshot.context,
          block: previousBlock
        })
      }
    })]]
  })
], abstractListItemBehaviors = [defineBehavior({
  on: "list item.add",
  guard: ({
    snapshot,
    event
  }) => snapshot.context.schema.lists.some((list) => list.name === event.listItem) ? {
    selectedTextBlocks: getSelectedTextBlocks(snapshot)
  } : !1,
  actions: [({
    event
  }, {
    selectedTextBlocks
  }) => selectedTextBlocks.map((block) => raise({
    type: "block.set",
    at: block.path,
    props: {
      level: block.node.level ?? 1,
      listItem: event.listItem
    }
  }))]
}), defineBehavior({
  on: "list item.remove",
  guard: ({
    snapshot
  }) => ({
    selectedTextBlocks: getSelectedTextBlocks(snapshot)
  }),
  actions: [(_, {
    selectedTextBlocks
  }) => selectedTextBlocks.map((block) => raise({
    type: "block.unset",
    at: block.path,
    props: ["level", "listItem"]
  }))]
}), defineBehavior({
  on: "list item.toggle",
  guard: ({
    snapshot,
    event
  }) => isActiveListItem(event.listItem)(snapshot),
  actions: [({
    event
  }) => [raise({
    type: "list item.remove",
    listItem: event.listItem
  })]]
}), defineBehavior({
  on: "list item.toggle",
  guard: ({
    snapshot,
    event
  }) => !isActiveListItem(event.listItem)(snapshot),
  actions: [({
    event
  }) => [raise({
    type: "list item.add",
    listItem: event.listItem
  })]]
})], abstractMoveBehaviors = [defineBehavior({
  on: "move.block up",
  guard: ({
    snapshot,
    event
  }) => {
    const previousBlock = getPreviousBlock({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: {
          anchor: {
            path: event.at,
            offset: 0
          },
          focus: {
            path: event.at,
            offset: 0
          }
        }
      }
    });
    return previousBlock ? {
      previousBlock
    } : !1;
  },
  actions: [({
    event
  }, {
    previousBlock
  }) => [raise({
    type: "move.block",
    at: event.at,
    to: previousBlock.path
  })]]
}), defineBehavior({
  on: "move.block down",
  guard: ({
    snapshot,
    event
  }) => {
    const nextBlock = getNextBlock({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: {
          anchor: {
            path: event.at,
            offset: 0
          },
          focus: {
            path: event.at,
            offset: 0
          }
        }
      }
    });
    return nextBlock ? {
      nextBlock
    } : !1;
  },
  actions: [({
    event
  }, {
    nextBlock
  }) => [raise({
    type: "move.block",
    at: event.at,
    to: nextBlock.path
  })]]
})], abstractSelectBehaviors = [defineBehavior({
  on: "select.block",
  guard: ({
    snapshot,
    event
  }) => {
    if (event.select !== "end")
      return !1;
    const block = getFocusBlock$1({
      ...snapshot,
      context: {
        ...snapshot.context,
        selection: {
          anchor: {
            path: event.at,
            offset: 0
          },
          focus: {
            path: event.at,
            offset: 0
          }
        }
      }
    });
    return block ? {
      blockEndPoint: getBlockEndPoint({
        context: snapshot.context,
        block
      })
    } : !1;
  },
  actions: [(_, {
    blockEndPoint
  }) => [raise({
    type: "select",
    at: {
      anchor: blockEndPoint,
      focus: blockEndPoint
    }
  })]]
}), defineBehavior({
  on: "select.block",
  actions: [({
    event
  }) => [raise({
    type: "select",
    at: {
      anchor: {
        path: event.at,
        offset: 0
      },
      focus: {
        path: event.at,
        offset: 0
      }
    }
  })]]
}), defineBehavior({
  on: "select.previous block",
  guard: ({
    snapshot
  }) => {
    const previousBlock = getPreviousBlock(snapshot);
    return previousBlock ? {
      previousBlock
    } : !1;
  },
  actions: [({
    event
  }, {
    previousBlock
  }) => [raise({
    type: "select.block",
    at: previousBlock.path,
    select: event.select
  })]]
}), defineBehavior({
  on: "select.next block",
  guard: ({
    snapshot
  }) => {
    const nextBlock = getNextBlock(snapshot);
    return nextBlock ? {
      nextBlock
    } : !1;
  },
  actions: [({
    event
  }, {
    nextBlock
  }) => [raise({
    type: "select.block",
    at: nextBlock.path,
    select: event.select
  })]]
})], abstractSerializeBehaviors = [defineBehavior({
  on: "serialize",
  actions: [({
    event
  }) => [raise({
    type: "serialize.data",
    mimeType: "application/x-portable-text",
    originEvent: event.originEvent
  }), raise({
    type: "serialize.data",
    mimeType: "application/json",
    originEvent: event.originEvent
  }), raise({
    type: "serialize.data",
    mimeType: "text/markdown",
    originEvent: event.originEvent
  }), raise({
    type: "serialize.data",
    mimeType: "text/html",
    originEvent: event.originEvent
  }), raise({
    type: "serialize.data",
    mimeType: "text/plain",
    originEvent: event.originEvent
  })]]
}), defineBehavior({
  on: "serialize.data",
  guard: ({
    snapshot,
    event
  }) => {
    const converter = snapshot.context.converters.find((converter2) => converter2.mimeType === event.mimeType);
    return converter ? converter.serialize({
      snapshot,
      event: {
        type: "serialize",
        originEvent: event.originEvent.type
      }
    }) : !1;
  },
  actions: [({
    event
  }, serializeEvent) => [raise({
    ...serializeEvent,
    originEvent: event.originEvent
  })]]
}), defineBehavior({
  on: "serialization.success",
  actions: [({
    event
  }) => [{
    type: "effect",
    effect: () => {
      event.originEvent.originEvent.dataTransfer.setData(event.mimeType, event.data);
    }
  }]]
}), defineBehavior({
  on: "serialization.failure",
  actions: [({
    event
  }) => [{
    type: "effect",
    effect: () => {
      console.warn(`Serialization of ${event.mimeType} failed with reason "${event.reason}"`);
    }
  }]]
})], abstractSplitBehaviors = [
  /**
   * You can't split an inline object.
   */
  defineBehavior({
    on: "split",
    guard: ({
      snapshot
    }) => isSelectionCollapsed(snapshot.context.selection) && getFocusInlineObject(snapshot),
    actions: []
  }),
  /**
   * You can't split a block object.
   */
  defineBehavior({
    on: "split",
    guard: ({
      snapshot
    }) => isSelectionCollapsed(snapshot.context.selection) && getFocusBlockObject(snapshot),
    actions: []
  }),
  defineBehavior({
    on: "split",
    guard: ({
      snapshot
    }) => {
      const selection = snapshot.context.selection;
      if (!selection || isSelectionCollapsed(selection))
        return !1;
      const startPoint = getSelectionStartPoint$1(selection), endPoint = getSelectionEndPoint$1(selection);
      if (!startPoint || !endPoint)
        return !1;
      const startBlock = getSelectionStartBlock(snapshot), endBlock = getSelectionEndBlock(snapshot);
      if (!startBlock || !endBlock)
        return !1;
      const startBlockStartPoint = getBlockStartPoint({
        context: snapshot.context,
        block: startBlock
      }), endBlockEndPoint = getBlockEndPoint({
        context: snapshot.context,
        block: endBlock
      });
      return !!(isTextBlock(snapshot.context, startBlock.node) && isTextBlock(snapshot.context, endBlock.node) && !isEqualSelectionPoints(startPoint, startBlockStartPoint) && !isEqualSelectionPoints(endPoint, endBlockEndPoint));
    },
    actions: [() => [raise({
      type: "delete"
    }), raise({
      type: "split"
    })]]
  }),
  defineBehavior({
    on: "split",
    guard: ({
      snapshot
    }) => isSelectionExpanded(snapshot),
    actions: [() => [raise({
      type: "delete"
    })]]
  }),
  defineBehavior({
    on: "split",
    guard: ({
      snapshot
    }) => {
      const selection = snapshot.context.selection;
      if (!selection || !isSelectionCollapsed(selection))
        return !1;
      const selectionStartPoint = getSelectionStartPoint$1(selection), focusTextBlock = getFocusTextBlock(snapshot);
      if (!focusTextBlock)
        return !1;
      const blockEndPoint = getBlockEndPoint({
        context: snapshot.context,
        block: focusTextBlock
      }), newTextBlockSelection = {
        anchor: selectionStartPoint,
        focus: blockEndPoint
      }, newTextBlock = parseBlock({
        block: sliceTextBlock({
          context: {
            ...snapshot.context,
            selection: newTextBlockSelection
          },
          block: focusTextBlock.node
        }),
        context: snapshot.context,
        options: {
          normalize: !1,
          removeUnusedMarkDefs: !0,
          validateFields: !1
        }
      });
      return newTextBlock ? {
        newTextBlock,
        newTextBlockSelection
      } : !1;
    },
    actions: [(_, {
      newTextBlock,
      newTextBlockSelection
    }) => isSelectionCollapsed(newTextBlockSelection) ? [raise({
      type: "insert.block",
      block: newTextBlock,
      placement: "after",
      select: "start"
    })] : [raise({
      type: "delete",
      at: newTextBlockSelection
    }), raise({
      type: "insert.block",
      block: newTextBlock,
      placement: "after",
      select: "start"
    })]]
  })
], abstractStyleBehaviors = [defineBehavior({
  on: "style.add",
  guard: ({
    snapshot
  }) => ({
    selectedTextBlocks: getSelectedTextBlocks(snapshot)
  }),
  actions: [({
    event
  }, {
    selectedTextBlocks
  }) => selectedTextBlocks.map((block) => raise({
    type: "block.set",
    at: block.path,
    props: {
      style: event.style
    }
  }))]
}), defineBehavior({
  on: "style.remove",
  guard: ({
    snapshot
  }) => ({
    selectedTextBlocks: getSelectedTextBlocks(snapshot)
  }),
  actions: [(_, {
    selectedTextBlocks
  }) => selectedTextBlocks.map((block) => raise({
    type: "block.unset",
    at: block.path,
    props: ["style"]
  }))]
}), defineBehavior({
  on: "style.toggle",
  guard: ({
    snapshot,
    event
  }) => isActiveStyle(event.style)(snapshot),
  actions: [({
    event
  }) => [raise({
    type: "style.remove",
    style: event.style
  })]]
}), defineBehavior({
  on: "style.toggle",
  guard: ({
    snapshot,
    event
  }) => !isActiveStyle(event.style)(snapshot),
  actions: [({
    event
  }) => [raise({
    type: "style.add",
    style: event.style
  })]]
})], abstractBehaviors = [defineBehavior({
  on: "clipboard.copy",
  guard: ({
    snapshot
  }) => {
    const focusSpan = getFocusSpan$1(snapshot), selectionCollapsed = isSelectionCollapsed$1(snapshot);
    return focusSpan && selectionCollapsed;
  },
  actions: []
}), defineBehavior({
  on: "clipboard.copy",
  actions: [({
    event
  }) => [raise({
    type: "serialize",
    originEvent: event
  })]]
}), defineBehavior({
  on: "clipboard.cut",
  guard: ({
    snapshot
  }) => {
    const focusSpan = getFocusSpan$1(snapshot), selectionCollapsed = isSelectionCollapsed$1(snapshot);
    return focusSpan && selectionCollapsed;
  },
  actions: []
}), defineBehavior({
  on: "clipboard.cut",
  guard: ({
    snapshot
  }) => snapshot.context.selection,
  actions: [({
    event
  }) => [raise({
    type: "serialize",
    originEvent: event
  }), raise({
    type: "delete"
  })]]
}), defineBehavior({
  on: "drag.dragstart",
  actions: [({
    event
  }) => [raise({
    type: "serialize",
    originEvent: event
  })]]
}), defineBehavior({
  on: "clipboard.paste",
  guard: ({
    snapshot
  }) => isSelectionExpanded(snapshot),
  actions: [({
    event
  }) => [raise({
    type: "delete"
  }), forward(event)]]
}), defineBehavior({
  on: "clipboard.paste",
  actions: [({
    event
  }) => [raise({
    type: "deserialize",
    originEvent: event
  })]]
}), ...abstractAnnotationBehaviors, ...abstractDecoratorBehaviors, ...abstractDeleteBehaviors, ...abstractDeserializeBehaviors, ...abstractInputBehaviors, ...abstractInsertBehaviors, ...abstractKeyboardBehaviors, ...abstractListItemBehaviors, ...abstractMoveBehaviors, ...abstractStyleBehaviors, ...abstractSelectBehaviors, ...abstractSerializeBehaviors, ...abstractSplitBehaviors];
function isSyntheticBehaviorEvent(event) {
  return !isCustomBehaviorEvent(event) && !isNativeBehaviorEvent(event) && !isAbstractBehaviorEvent(event);
}
const abstractBehaviorEventTypes = ["annotation.set", "annotation.toggle", "decorator.toggle", "delete.backward", "delete.block", "delete.child", "delete.forward", "delete.text", "deserialize", "deserialize.data", "deserialization.success", "deserialization.failure", "insert.blocks", "insert.break", "insert.inline object", "insert.soft break", "insert.span", "list item.add", "list item.remove", "list item.toggle", "move.block down", "move.block up", "select.block", "select.previous block", "select.next block", "serialize", "serialize.data", "serialization.success", "serialization.failure", "split", "style.add", "style.remove", "style.toggle"];
function isAbstractBehaviorEvent(event) {
  return abstractBehaviorEventTypes.includes(event.type);
}
const nativeBehaviorEventTypes = ["clipboard.copy", "clipboard.cut", "clipboard.paste", "drag.dragstart", "drag.drag", "drag.dragend", "drag.dragenter", "drag.dragover", "drag.dragleave", "drag.drop", "input.*", "keyboard.keydown", "keyboard.keyup", "mouse.click"];
function isNativeBehaviorEvent(event) {
  return nativeBehaviorEventTypes.includes(event.type);
}
function isCustomBehaviorEvent(event) {
  return event.type.startsWith("custom.");
}
function eventCategory(event) {
  return isNativeBehaviorEvent(event) ? "native" : isAbstractBehaviorEvent(event) ? "synthetic" : isCustomBehaviorEvent(event) ? "custom" : "synthetic";
}
function performEvent({
  mode,
  behaviors,
  remainingEventBehaviors,
  event,
  editor,
  converters,
  keyGenerator,
  readOnly,
  schema,
  nativeEvent,
  sendBack
}) {
  mode === "send" && !isNativeBehaviorEvent(event) && (editor.undoStepId = defaultKeyGenerator()), debug$1.behaviors(`(${mode}:${eventCategory(event)})`, JSON.stringify(event, null, 2));
  const eventBehaviors = [...remainingEventBehaviors, ...abstractBehaviors].filter((behavior) => {
    if (behavior.on === "*")
      return !0;
    const [listenedNamespace] = behavior.on.includes("*") && behavior.on.includes(".") ? behavior.on.split(".") : [void 0], [eventNamespace] = event.type.includes(".") ? event.type.split(".") : [void 0];
    return listenedNamespace !== void 0 && eventNamespace !== void 0 && listenedNamespace === eventNamespace || listenedNamespace !== void 0 && eventNamespace === void 0 && listenedNamespace === event.type ? !0 : behavior.on === event.type;
  });
  if (eventBehaviors.length === 0 && isSyntheticBehaviorEvent(event)) {
    nativeEvent?.preventDefault(), mode === "send" && (editor.undoStepId = void 0), withPerformingBehaviorOperation(editor, () => {
      debug$1.operation(JSON.stringify(event, null, 2)), performOperation({
        context: {
          keyGenerator,
          schema
        },
        operation: {
          ...event,
          editor
        }
      });
    }), mode === "send" && editor.onChange();
    return;
  }
  const guardSnapshot = createEditorSnapshot({
    converters,
    editor,
    keyGenerator,
    readOnly,
    schema
  });
  let nativeEventPrevented = !1, defaultBehaviorOverwritten = !1, eventBehaviorIndex = -1;
  for (const eventBehavior of eventBehaviors) {
    eventBehaviorIndex++;
    let shouldRun = !1;
    try {
      shouldRun = eventBehavior.guard === void 0 || eventBehavior.guard({
        snapshot: guardSnapshot,
        event,
        dom: createEditorDom(sendBack, editor)
      });
    } catch (error) {
      console.error(new Error(`Evaluating guard for "${event.type}" failed due to: ${error instanceof Error ? error.message : error}`));
    }
    if (!shouldRun)
      continue;
    defaultBehaviorOverwritten = !0, eventBehavior.actions.length === 0 && (nativeEventPrevented = !0);
    let actionSetIndex = -1;
    for (const actionSet of eventBehavior.actions) {
      actionSetIndex++;
      const actionsSnapshot = createEditorSnapshot({
        converters,
        editor,
        keyGenerator,
        readOnly,
        schema
      });
      let actions = [];
      try {
        actions = actionSet({
          snapshot: actionsSnapshot,
          event,
          dom: createEditorDom(sendBack, editor)
        }, shouldRun);
      } catch (error) {
        console.error(new Error(`Evaluating actions for "${event.type}" failed due to: ${error instanceof Error ? error.message : error}`));
      }
      if (actions.length === 0)
        continue;
      nativeEventPrevented = actions.some((action) => action.type === "raise" || action.type === "execute") || !actions.some((action) => action.type === "forward");
      let undoStepCreated = !1;
      actionSetIndex > 0 && (editor.undoStepId = defaultKeyGenerator(), undoStepCreated = !0), !undoStepCreated && actions.some((action) => action.type === "execute") && (editor.undoStepId = defaultKeyGenerator(), undoStepCreated = !0);
      const actionTypes = actions.map((action) => action.type), uniqueActionTypes = new Set(actionTypes), raiseGroup = actionTypes.length > 1 && uniqueActionTypes.size === 1 && uniqueActionTypes.has("raise"), executeGroup = actionTypes.length > 1 && uniqueActionTypes.size === 1 && uniqueActionTypes.has("execute");
      withoutNormalizingConditional(editor, () => raiseGroup || executeGroup, () => {
        for (const action of actions) {
          if (action.type === "effect") {
            try {
              action.effect({
                send: sendBack
              });
            } catch (error) {
              console.error(new Error(`Executing effect as a result of "${event.type}" failed due to: ${error instanceof Error ? error.message : error}`));
            }
            continue;
          }
          if (action.type === "forward") {
            const remainingEventBehaviors2 = eventBehaviors.slice(eventBehaviorIndex + 1);
            performEvent({
              mode: mode === "execute" ? "execute" : "forward",
              behaviors,
              remainingEventBehaviors: remainingEventBehaviors2,
              event: action.event,
              editor,
              converters,
              keyGenerator,
              readOnly,
              schema,
              nativeEvent,
              sendBack
            });
            continue;
          }
          if (action.type === "raise") {
            performEvent({
              mode: mode === "execute" ? "execute" : "raise",
              behaviors,
              remainingEventBehaviors: mode === "execute" ? remainingEventBehaviors : behaviors,
              event: action.event,
              editor,
              converters,
              keyGenerator,
              readOnly,
              schema,
              nativeEvent,
              sendBack
            });
            continue;
          }
          performEvent({
            mode: "execute",
            behaviors,
            remainingEventBehaviors: [],
            event: action.event,
            editor,
            converters,
            keyGenerator,
            readOnly,
            schema,
            nativeEvent: void 0,
            sendBack
          });
        }
      }), undoStepCreated && (editor.undoStepId = void 0);
    }
    break;
  }
  !defaultBehaviorOverwritten && isSyntheticBehaviorEvent(event) ? (nativeEvent?.preventDefault(), mode === "send" && (editor.undoStepId = void 0), withPerformingBehaviorOperation(editor, () => {
    debug$1.operation(JSON.stringify(event, null, 2)), performOperation({
      context: {
        keyGenerator,
        schema
      },
      operation: {
        ...event,
        editor
      }
    });
  }), mode === "send" && editor.onChange()) : nativeEventPrevented && (nativeEvent?.preventDefault(), mode === "send" && editor.onChange());
}
function sortByPriority(items) {
  if (items.length === 0)
    return [];
  const itemsWithPriority = items.filter((item) => item.priority !== void 0), itemsWithoutPriority = items.filter((item) => item.priority === void 0);
  if (itemsWithPriority.length === 0)
    return items;
  const itemsByPriorityId = new Map(itemsWithPriority.map((item) => [item.priority.id, item])), graph = /* @__PURE__ */ new Map(), inDegree = /* @__PURE__ */ new Map();
  function ensureNode(id) {
    graph.has(id) || (graph.set(id, /* @__PURE__ */ new Set()), inDegree.set(id, 0));
  }
  for (const item of itemsWithPriority) {
    const id = item.priority.id;
    ensureNode(id);
  }
  function addEdge(fromId, toId) {
    !graph.has(fromId) || !graph.has(toId) || (graph.get(fromId)?.add(toId), inDegree.set(toId, (inDegree.get(toId) ?? 0) + 1));
  }
  for (const item of itemsWithPriority) {
    const id = item.priority.id, visited = /* @__PURE__ */ new Set();
    let ref = item.priority.reference;
    for (; ref; ) {
      const refId = ref.priority.id;
      if (ensureNode(refId), visited.has(refId))
        throw new Error("Circular dependency detected in priorities");
      visited.add(refId), ref.importance === "higher" ? addEdge(id, refId) : addEdge(refId, id), ref = ref.priority.reference;
    }
  }
  const queue = [];
  for (const [id, degree] of inDegree)
    degree === 0 && queue.push(id);
  const result = [];
  for (; queue.length > 0; ) {
    const currentId = queue.shift(), currentItem = itemsByPriorityId.get(currentId);
    currentItem && result.push(currentItem);
    for (const neighborId of graph.get(currentId) ?? []) {
      const newDegree = (inDegree.get(neighborId) ?? 0) - 1;
      inDegree.set(neighborId, newDegree), newDegree === 0 && queue.push(neighborId);
    }
  }
  for (const item of itemsWithPriority)
    result.includes(item) || result.push(item);
  return [...result, ...itemsWithoutPriority];
}
function pathsOverlap(pathA, pathB) {
  const minLength = Math.min(pathA.length, pathB.length);
  for (let i = 0; i < minLength; i++)
    if (!isEqualPathSegments(pathA[i], pathB[i]))
      return !1;
  return !0;
}
function rerouteExternalBehaviorEvent({
  event,
  slateEditor
}) {
  switch (event.type) {
    case "blur":
      return {
        type: "blur",
        editor: slateEditor
      };
    case "focus":
      return {
        type: "focus",
        editor: slateEditor
      };
    case "insert.block object":
      return {
        type: "behavior event",
        behaviorEvent: {
          type: "insert.block",
          block: {
            _type: event.blockObject.name,
            ...event.blockObject.value ?? {}
          },
          placement: event.placement
        },
        editor: slateEditor
      };
    default:
      return {
        type: "behavior event",
        behaviorEvent: event,
        editor: slateEditor
      };
  }
}
const editorMachine = setup({
  types: {
    context: {},
    events: {},
    emitted: {},
    input: {},
    tags: {}
  },
  actions: {
    "add behavior to context": assign({
      behaviors: ({
        context,
        event
      }) => (assertEvent(event, "add behavior"), /* @__PURE__ */ new Set([...context.behaviors, event.behaviorConfig])),
      behaviorsSorted: !1
    }),
    "remove behavior from context": assign({
      behaviors: ({
        context,
        event
      }) => (assertEvent(event, "remove behavior"), context.behaviors.delete(event.behaviorConfig), /* @__PURE__ */ new Set([...context.behaviors]))
    }),
    "add slate editor to context": assign({
      slateEditor: ({
        context,
        event
      }) => event.type === "add slate editor" ? event.editor : context.slateEditor
    }),
    "emit patch event": emit(({
      event
    }) => (assertEvent(event, "internal.patch"), event)),
    "emit mutation event": emit(({
      event
    }) => (assertEvent(event, "mutation"), event)),
    "emit read only": emit({
      type: "read only"
    }),
    "emit editable": emit({
      type: "editable"
    }),
    "defer event": assign({
      pendingEvents: ({
        context,
        event
      }) => (assertEvent(event, ["internal.patch", "mutation"]), [...context.pendingEvents, event])
    }),
    "emit pending events": enqueueActions(({
      context,
      enqueue
    }) => {
      for (const event of context.pendingEvents)
        enqueue.emit(event);
    }),
    "emit ready": emit({
      type: "ready"
    }),
    "clear pending events": assign({
      pendingEvents: []
    }),
    "discard conflicting pending patches": assign({
      pendingEvents: ({
        context,
        event
      }) => {
        if (event.type !== "patches")
          return context.pendingEvents;
        const incomingPaths = event.patches.map((patch) => patch.path);
        return context.pendingEvents.filter((pendingEvent) => pendingEvent.type !== "internal.patch" ? !0 : !incomingPaths.some((incomingPath) => pathsOverlap(pendingEvent.patch.path, incomingPath)));
      }
    }),
    "discard all pending events": assign({
      pendingEvents: []
    }),
    "defer incoming patches": assign({
      pendingIncomingPatchesEvents: ({
        context,
        event
      }) => event.type === "patches" ? [...context.pendingIncomingPatchesEvents, event] : context.pendingIncomingPatchesEvents
    }),
    "emit pending incoming patches": enqueueActions(({
      context,
      enqueue
    }) => {
      for (const event of context.pendingIncomingPatchesEvents)
        enqueue.emit(event);
    }),
    "clear pending incoming patches": assign({
      pendingIncomingPatchesEvents: []
    }),
    "handle blur": ({
      event
    }) => {
      assertEvent(event, "blur");
      try {
        ReactEditor.blur(event.editor);
      } catch (error) {
        console.error(new Error(`Failed to blur editor: ${error instanceof Error ? error.message : error}`));
      }
    },
    "handle focus": ({
      context
    }) => {
      const slateEditor = context.slateEditor;
      if (!slateEditor) {
        console.error("No Slate editor found to focus");
        return;
      }
      try {
        const currentSelection = slateEditor.selection;
        ReactEditor.focus(slateEditor), currentSelection && (Transforms.select(slateEditor, currentSelection), EDITOR_TO_PENDING_SELECTION.set(slateEditor, slateEditor.selection), slateEditor.onChange());
      } catch (error) {
        console.error(new Error(`Failed to focus editor: ${error instanceof Error ? error.message : error}`));
      }
    },
    "handle behavior event": ({
      context,
      event,
      self
    }) => {
      assertEvent(event, ["behavior event"]);
      try {
        const behaviors = [...context.behaviors.values()].map((config) => config.behavior);
        performEvent({
          mode: "send",
          behaviors,
          remainingEventBehaviors: behaviors,
          event: event.behaviorEvent,
          editor: event.editor,
          converters: [...context.converters],
          keyGenerator: context.keyGenerator,
          schema: context.schema,
          readOnly: self.getSnapshot().matches({
            "edit mode": "read only"
          }),
          nativeEvent: event.nativeEvent,
          sendBack: (eventSentBack) => {
            if (eventSentBack.type === "set drag ghost") {
              self.send(eventSentBack);
              return;
            }
            self.send(rerouteExternalBehaviorEvent({
              event: eventSentBack,
              slateEditor: event.editor
            }));
          }
        });
      } catch (error) {
        console.error(new Error(`Raising "${event.behaviorEvent.type}" failed due to: ${error instanceof Error ? error.message : error}`));
      }
    },
    "sort behaviors": assign({
      behaviors: ({
        context
      }) => context.behaviorsSorted ? context.behaviors : new Set(sortByPriority([...context.behaviors.values()])),
      behaviorsSorted: !0
    })
  },
  guards: {
    "slate is busy": ({
      context
    }) => context.slateEditor ? context.slateEditor.operations.length > 0 : !1,
    "slate is normalizing node": ({
      context
    }) => context.slateEditor ? context.slateEditor.isNormalizingNode : !1
  }
}).createMachine({
  id: "editor",
  context: ({
    input
  }) => ({
    behaviors: new Set(coreBehaviorsConfig),
    behaviorsSorted: !1,
    converters: new Set(input.converters ?? []),
    getLegacySchema: input.getLegacySchema,
    keyGenerator: input.keyGenerator,
    pendingEvents: [],
    pendingIncomingPatchesEvents: [],
    schema: input.schema,
    selection: null,
    initialReadOnly: input.readOnly ?? !1,
    initialValue: input.initialValue
  }),
  on: {
    "add behavior": {
      actions: "add behavior to context"
    },
    "remove behavior": {
      actions: "remove behavior from context"
    },
    "add slate editor": {
      actions: "add slate editor to context"
    },
    "update selection": {
      actions: [assign({
        selection: ({
          event
        }) => event.selection
      }), emit(({
        event
      }) => ({
        ...event,
        type: "selection"
      }))]
    },
    "set drag ghost": {
      actions: assign({
        dragGhost: ({
          event
        }) => event.ghost
      })
    }
  },
  type: "parallel",
  states: {
    "edit mode": {
      initial: "read only",
      states: {
        "read only": {
          initial: "determine initial edit mode",
          on: {
            "behavior event": {
              actions: ["sort behaviors", "handle behavior event"],
              guard: ({
                event
              }) => event.behaviorEvent.type === "clipboard.copy" || event.behaviorEvent.type === "mouse.click" || event.behaviorEvent.type === "serialize" || event.behaviorEvent.type === "serialization.failure" || event.behaviorEvent.type === "serialization.success" || event.behaviorEvent.type === "select"
            }
          },
          states: {
            "determine initial edit mode": {
              entry: [() => {
                debug$1.state("entry: edit mode->read only->determine initial edit mode");
              }],
              exit: [() => {
                debug$1.state("exit: edit mode->read only->determine initial edit mode");
              }],
              on: {
                "done syncing value": [{
                  target: "#editor.edit mode.read only.read only",
                  guard: ({
                    context
                  }) => context.initialReadOnly
                }, {
                  target: "#editor.edit mode.editable"
                }]
              }
            },
            "read only": {
              entry: [() => {
                debug$1.state("entry: edit mode->read only->read only");
              }],
              exit: [() => {
                debug$1.state("exit: edit mode->read only->read only");
              }],
              on: {
                "update readOnly": {
                  guard: ({
                    event
                  }) => !event.readOnly,
                  target: "#editor.edit mode.editable",
                  actions: ["emit editable"]
                }
              }
            }
          }
        },
        editable: {
          on: {
            "update readOnly": {
              guard: ({
                event
              }) => event.readOnly,
              target: "#editor.edit mode.read only.read only",
              actions: ["emit read only"]
            },
            "behavior event": {
              actions: ["sort behaviors", "handle behavior event"]
            },
            blur: {
              actions: "handle blur"
            },
            focus: {
              target: ".focusing",
              actions: [assign({
                slateEditor: ({
                  event
                }) => event.editor
              })]
            }
          },
          initial: "idle",
          states: {
            idle: {
              entry: [() => {
                debug$1.state("entry: edit mode->editable->idle");
              }],
              exit: [() => {
                debug$1.state("exit: edit mode->editable-idle");
              }],
              on: {
                dragstart: {
                  actions: [assign({
                    internalDrag: ({
                      event
                    }) => ({
                      origin: event.origin
                    })
                  })],
                  target: "dragging internally"
                }
              }
            },
            focusing: {
              initial: "checking if busy",
              states: {
                "checking if busy": {
                  entry: [() => {
                    debug$1.state("entry: edit mode->editable->focusing->checking if busy");
                  }],
                  exit: [() => {
                    debug$1.state("exit: edit mode->editable->focusing->checking if busy");
                  }],
                  always: [{
                    guard: "slate is busy",
                    target: "busy"
                  }, {
                    target: "#editor.edit mode.editable.idle",
                    actions: ["handle focus"]
                  }]
                },
                busy: {
                  entry: [() => {
                    debug$1.state("entry: edit mode->editable->focusing-busy");
                  }],
                  exit: [() => {
                    debug$1.state("exit: edit mode->editable->focusing->busy");
                  }],
                  after: {
                    10: {
                      target: "checking if busy"
                    }
                  }
                }
              }
            },
            "dragging internally": {
              entry: [() => {
                debug$1.state("entry: edit mode->editable->dragging internally");
              }],
              exit: [() => {
                debug$1.state("exit: edit mode->editable->dragging internally");
              }, ({
                context
              }) => {
                if (context.dragGhost)
                  try {
                    context.dragGhost.parentNode?.removeChild(context.dragGhost);
                  } catch (error) {
                    console.error(new Error(`Removing the drag ghost failed due to: ${error instanceof Error ? error.message : error}`));
                  }
              }, assign({
                dragGhost: void 0
              }), assign({
                internalDrag: void 0
              })],
              tags: ["dragging internally"],
              on: {
                dragend: {
                  target: "idle"
                },
                drop: {
                  target: "idle"
                }
              }
            }
          }
        }
      }
    },
    setup: {
      initial: "setting up",
      states: {
        "setting up": {
          entry: [() => {
            debug$1.state("entry: setup->setting up");
          }],
          exit: [() => {
            debug$1.state("exit: setup->setting up");
          }, "emit ready", "emit pending incoming patches", "clear pending incoming patches"],
          on: {
            "internal.patch": {
              actions: "defer event"
            },
            mutation: {
              actions: "defer event"
            },
            "done syncing value": {
              target: "set up"
            },
            patches: {
              actions: ["defer incoming patches"]
            }
          }
        },
        "set up": {
          type: "parallel",
          states: {
            "value sync": {
              initial: "idle",
              states: {
                idle: {
                  entry: [() => {
                    debug$1.state("entry: setup->set up->value sync->idle");
                  }],
                  exit: [() => {
                    debug$1.state("exit: setup->set up->value sync->idle");
                  }],
                  on: {
                    patches: {
                      actions: [emit(({
                        event
                      }) => event)]
                    },
                    "syncing value": {
                      target: "syncing value"
                    }
                  }
                },
                "syncing value": {
                  entry: [() => {
                    debug$1.state("entry: setup->set up->value sync->syncing value");
                  }],
                  exit: [() => {
                    debug$1.state("exit: setup->set up->value sync->syncing value");
                  }, "emit pending incoming patches", "clear pending incoming patches"],
                  on: {
                    patches: {
                      actions: ["defer incoming patches"]
                    },
                    "done syncing value": {
                      target: "idle"
                    }
                  }
                }
              }
            },
            writing: {
              initial: "pristine",
              states: {
                pristine: {
                  initial: "idle",
                  states: {
                    idle: {
                      entry: [() => {
                        debug$1.state("entry: setup->set up->writing->pristine->idle");
                      }],
                      exit: [() => {
                        debug$1.state("exit: setup->set up->writing->pristine->idle");
                      }],
                      on: {
                        "internal.patch": [{
                          guard: "slate is normalizing node",
                          actions: "defer event"
                        }, {
                          actions: "defer event",
                          target: "#editor.setup.set up.writing.dirty"
                        }],
                        mutation: [{
                          guard: "slate is normalizing node",
                          actions: "defer event"
                        }, {
                          actions: "defer event",
                          target: "#editor.setup.set up.writing.dirty"
                        }],
                        patches: {
                          actions: "discard conflicting pending patches"
                        },
                        "syncing value": {
                          actions: "discard all pending events"
                        }
                      }
                    }
                  }
                },
                dirty: {
                  entry: [() => {
                    debug$1.state("entry: setup->set up->writing->dirty");
                  }, "emit pending events", "clear pending events"],
                  exit: [() => {
                    debug$1.state("exit: setup->set up->writing->dirty");
                  }],
                  on: {
                    "internal.patch": {
                      actions: "emit patch event"
                    },
                    mutation: {
                      actions: "emit mutation event"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}), mutationMachine = setup({
  types: {
    context: {},
    events: {},
    input: {},
    emitted: {}
  },
  actions: {
    "assign readOnly": assign({
      readOnly: ({
        context,
        event
      }) => event.type === "update readOnly" ? event.readOnly : context.readOnly
    }),
    "emit patch": emit(({
      event
    }) => (assertEvent(event, "patch"), {
      type: "patch",
      patch: event.patch
    })),
    "set is deferring mutations": ({
      context
    }) => {
      context.slateEditor.isDeferringMutations = !0;
    },
    "emit mutations": enqueueActions(({
      context,
      enqueue
    }) => {
      for (const bulk of context.pendingMutations)
        enqueue.emit({
          type: "mutation",
          patches: bulk.patches,
          snapshot: bulk.value
        });
      context.slateEditor.isDeferringMutations = !1;
    }),
    "clear pending mutations": assign({
      pendingMutations: []
    }),
    "defer mutation": assign({
      pendingMutations: ({
        context,
        event
      }) => {
        if (assertEvent(event, "patch"), context.pendingMutations.length === 0)
          return [{
            operationId: event.operationId,
            value: event.value,
            patches: [event.patch]
          }];
        const lastBulk = context.pendingMutations.at(-1);
        return lastBulk && lastBulk.operationId === event.operationId ? context.pendingMutations.slice(0, -1).concat({
          value: event.value,
          operationId: lastBulk.operationId,
          patches: [...lastBulk.patches, event.patch]
        }) : context.pendingMutations.concat({
          value: event.value,
          operationId: event.operationId,
          patches: [event.patch]
        });
      }
    }),
    "clear pending patch events": assign({
      pendingPatchEvents: []
    }),
    "defer patch": assign({
      pendingPatchEvents: ({
        context,
        event
      }) => event.type === "patch" ? [...context.pendingPatchEvents, event] : context.pendingPatchEvents
    }),
    "emit pending patch events": enqueueActions(({
      context,
      enqueue
    }) => {
      for (const event of context.pendingPatchEvents)
        enqueue.emit(event);
    })
  },
  actors: {
    "type listener": fromCallback(({
      input,
      sendBack
    }) => {
      const originalApply = input.slateEditor.apply;
      return input.slateEditor.apply = (op) => {
        op.type === "insert_text" || op.type === "remove_text" ? sendBack({
          type: "typing"
        }) : sendBack({
          type: "not typing"
        }), originalApply(op);
      }, () => {
        input.slateEditor.apply = originalApply;
      };
    }),
    "mutation interval": fromCallback(({
      sendBack
    }) => {
      const interval = setInterval(
        () => {
          sendBack({
            type: "emit changes"
          });
        },
        // @ts-expect-error - dot notation required for Vite to replace at build time
        process.env.NODE_ENV === "test" ? 250 : 1e3
      );
      return () => {
        clearInterval(interval);
      };
    })
  },
  guards: {
    "is read-only": ({
      context
    }) => context.readOnly,
    "slate is normalizing": ({
      context
    }) => Editor.isNormalizing(context.slateEditor)
  },
  delays: {
    "type debounce": 250
  }
}).createMachine({
  id: "mutation",
  context: ({
    input
  }) => ({
    pendingMutations: [],
    pendingPatchEvents: [],
    readOnly: input.readOnly,
    schema: input.schema,
    slateEditor: input.slateEditor
  }),
  on: {
    "update readOnly": {
      actions: ["assign readOnly"]
    }
  },
  type: "parallel",
  states: {
    typing: {
      initial: "idle",
      invoke: {
        src: "type listener",
        input: ({
          context
        }) => ({
          slateEditor: context.slateEditor
        })
      },
      states: {
        idle: {
          entry: [() => {
            debug$1.mutation("entry: typing->idle");
          }],
          exit: [() => {
            debug$1.mutation("exit: typing->idle"), debug$1.mutation("entry: typing->typing");
          }],
          on: {
            typing: {
              target: "typing"
            }
          }
        },
        typing: {
          after: {
            "type debounce": {
              target: "idle",
              actions: [raise$1({
                type: "emit changes"
              }), () => {
                debug$1.mutation("exit: typing->typing");
              }]
            }
          },
          on: {
            "not typing": {
              target: "idle",
              actions: [raise$1({
                type: "emit changes"
              })]
            },
            typing: {
              target: "typing",
              reenter: !0
            }
          }
        }
      }
    },
    mutations: {
      initial: "idle",
      states: {
        idle: {
          entry: [() => {
            debug$1.mutation("entry: mutations->idle");
          }],
          exit: [() => {
            debug$1.mutation("exit: mutations->idle");
          }],
          on: {
            patch: [{
              guard: "is read-only",
              actions: ["set is deferring mutations", "defer patch", "defer mutation"],
              target: "has pending mutations"
            }, {
              actions: ["set is deferring mutations", "emit patch", "defer mutation"],
              target: "has pending mutations"
            }]
          }
        },
        "has pending mutations": {
          entry: [() => {
            debug$1.mutation("entry: mutations->has pending mutations");
          }],
          exit: [() => {
            debug$1.mutation("exit: mutations->has pending mutations");
          }],
          invoke: {
            src: "mutation interval"
          },
          on: {
            "emit changes": {
              guard: and([not("is read-only"), "slate is normalizing"]),
              target: "idle",
              actions: ["emit pending patch events", "clear pending patch events", "emit mutations", "clear pending mutations"]
            },
            patch: [{
              guard: "is read-only",
              actions: ["defer patch", "defer mutation"]
            }, {
              actions: ["emit patch", "defer mutation"]
            }]
          }
        }
      }
    }
  }
}), relayMachine = setup({
  types: {
    context: {},
    events: {},
    emitted: {}
  }
}).createMachine({
  id: "relay",
  context: {
    prevSelection: null,
    lastEventWasFocused: !1
  },
  on: {
    focused: {
      actions: [assign({
        lastEventWasFocused: !0
      }), emit(({
        event
      }) => event)]
    },
    selection: [{
      guard: ({
        context
      }) => context.lastEventWasFocused,
      actions: [assign({
        prevSelection: ({
          event
        }) => event.selection
      }), emit(({
        event
      }) => event), assign({
        lastEventWasFocused: !1
      })]
    }, {
      guard: ({
        context,
        event
      }) => context.prevSelection !== event.selection,
      actions: [assign({
        prevSelection: ({
          event
        }) => event.selection
      }), emit(({
        event
      }) => event), assign({
        lastEventWasFocused: !1
      })]
    }],
    "*": {
      actions: [emit(({
        event
      }) => event), assign({
        lastEventWasFocused: !1
      })]
    }
  }
});
function validateValue(value, types, keyGenerator) {
  let resolution = null, valid = !0;
  const validChildTypes = [types.span.name, ...types.inlineObjects.map((t) => t.name)], validBlockTypes = [types.block.name, ...types.blockObjects.map((t) => t.name)];
  return value === void 0 ? {
    valid: !0,
    resolution: null,
    value
  } : !Array.isArray(value) || value.length === 0 ? {
    valid: !1,
    resolution: {
      patches: [unset([])],
      description: "Editor value must be an array of Portable Text blocks, or undefined.",
      action: "Unset the value",
      item: value,
      i18n: {
        description: "inputs.portable-text.invalid-value.not-an-array.description",
        action: "inputs.portable-text.invalid-value.not-an-array.action"
      }
    },
    value
  } : (value.some((blk, index) => {
    if (typeof blk != "object" || blk === null)
      return resolution = {
        patches: [unset([index])],
        description: `Block must be an object, got ${String(blk)}`,
        action: "Unset invalid item",
        item: blk,
        i18n: {
          description: "inputs.portable-text.invalid-value.not-an-object.description",
          action: "inputs.portable-text.invalid-value.not-an-object.action",
          values: {
            index
          }
        }
      }, !0;
    if (!blk._key || typeof blk._key != "string")
      return resolution = {
        patches: [set({
          ...blk,
          _key: keyGenerator()
        }, [index])],
        description: `Block at index ${index} is missing required _key.`,
        action: "Set the block with a random _key value",
        item: blk,
        i18n: {
          description: "inputs.portable-text.invalid-value.missing-key.description",
          action: "inputs.portable-text.invalid-value.missing-key.action",
          values: {
            index
          }
        }
      }, !0;
    if (!blk._type || !validBlockTypes.includes(blk._type)) {
      if (blk._type === "block") {
        const currentBlockTypeName = types.block.name;
        return resolution = {
          patches: [set({
            ...blk,
            _type: currentBlockTypeName
          }, [{
            _key: blk._key
          }])],
          description: `Block with _key '${blk._key}' has invalid type name '${blk._type}'. According to the schema, the block type name is '${currentBlockTypeName}'`,
          action: `Use type '${currentBlockTypeName}'`,
          item: blk,
          i18n: {
            description: "inputs.portable-text.invalid-value.incorrect-block-type.description",
            action: "inputs.portable-text.invalid-value.incorrect-block-type.action",
            values: {
              key: blk._key,
              expectedTypeName: currentBlockTypeName
            }
          }
        }, !0;
      }
      return !blk._type && isTextBlock({
        schema: types
      }, {
        ...blk,
        _type: types.block.name
      }) ? (resolution = {
        patches: [set({
          ...blk,
          _type: types.block.name
        }, [{
          _key: blk._key
        }])],
        description: `Block with _key '${blk._key}' is missing a type name. According to the schema, the block type name is '${types.block.name}'`,
        action: `Use type '${types.block.name}'`,
        item: blk,
        i18n: {
          description: "inputs.portable-text.invalid-value.missing-block-type.description",
          action: "inputs.portable-text.invalid-value.missing-block-type.action",
          values: {
            key: blk._key,
            expectedTypeName: types.block.name
          }
        }
      }, !0) : blk._type ? (resolution = {
        patches: [unset([{
          _key: blk._key
        }])],
        description: `Block with _key '${blk._key}' has invalid _type '${blk._type}'`,
        action: "Remove the block",
        item: blk,
        i18n: {
          description: "inputs.portable-text.invalid-value.disallowed-type.description",
          action: "inputs.portable-text.invalid-value.disallowed-type.action",
          values: {
            key: blk._key,
            typeName: blk._type
          }
        }
      }, !0) : (resolution = {
        patches: [unset([{
          _key: blk._key
        }])],
        description: `Block with _key '${blk._key}' is missing an _type property`,
        action: "Remove the block",
        item: blk,
        i18n: {
          description: "inputs.portable-text.invalid-value.missing-type.description",
          action: "inputs.portable-text.invalid-value.missing-type.action",
          values: {
            key: blk._key
          }
        }
      }, !0);
    }
    if (blk._type === types.block.name) {
      const textBlock = blk;
      if (textBlock.children && !Array.isArray(textBlock.children))
        return resolution = {
          patches: [set({
            children: []
          }, [{
            _key: textBlock._key
          }])],
          description: `Text block with _key '${textBlock._key}' has a invalid required property 'children'.`,
          action: "Reset the children property",
          item: textBlock,
          i18n: {
            description: "inputs.portable-text.invalid-value.missing-or-invalid-children.description",
            action: "inputs.portable-text.invalid-value.missing-or-invalid-children.action",
            values: {
              key: textBlock._key
            }
          }
        }, !0;
      if (textBlock.children === void 0 || Array.isArray(textBlock.children) && textBlock.children.length === 0) {
        const newSpan = {
          _type: types.span.name,
          _key: keyGenerator(),
          text: "",
          marks: []
        };
        return resolution = {
          autoResolve: !0,
          patches: [setIfMissing([], [{
            _key: blk._key
          }, "children"]), insert([newSpan], "after", [{
            _key: blk._key
          }, "children", 0])],
          description: `Children for text block with _key '${blk._key}' is empty.`,
          action: "Insert an empty text",
          item: blk,
          i18n: {
            description: "inputs.portable-text.invalid-value.empty-children.description",
            action: "inputs.portable-text.invalid-value.empty-children.action",
            values: {
              key: blk._key
            }
          }
        }, !0;
      }
      const allUsedMarks = [...new Set(textBlock.children.filter((child) => isSpan({
        schema: types
      }, child)).flatMap((cld) => cld.marks || []))];
      if (Array.isArray(blk.markDefs) && blk.markDefs.length > 0) {
        const unusedMarkDefs = [...new Set(blk.markDefs.map((def) => def._key).filter((key) => !allUsedMarks.includes(key)))];
        if (unusedMarkDefs.length > 0)
          return resolution = {
            autoResolve: !0,
            patches: unusedMarkDefs.map((markDefKey) => unset([{
              _key: blk._key
            }, "markDefs", {
              _key: markDefKey
            }])),
            description: `Block contains orphaned data (unused mark definitions): ${unusedMarkDefs.join(", ")}.`,
            action: "Remove unused mark definition item",
            item: blk,
            i18n: {
              description: "inputs.portable-text.invalid-value.orphaned-mark-defs.description",
              action: "inputs.portable-text.invalid-value.orphaned-mark-defs.action",
              values: {
                key: blk._key,
                unusedMarkDefs: unusedMarkDefs.map((m) => m.toString())
              }
            }
          }, !0;
      }
      const orphanedMarks = allUsedMarks.filter((mark) => !types.decorators.map((dec) => dec.name).includes(mark)).filter((mark) => textBlock.markDefs === void 0 || !textBlock.markDefs.find((def) => def._key === mark));
      if (orphanedMarks.length > 0) {
        const spanChildren = textBlock.children.filter((cld) => cld._type === types.span.name && Array.isArray(cld.marks) && cld.marks.some((mark) => orphanedMarks.includes(mark)));
        if (spanChildren) {
          const orphaned = orphanedMarks.join(", ");
          return resolution = {
            autoResolve: !0,
            patches: spanChildren.map((child) => set((child.marks || []).filter((cMrk) => !orphanedMarks.includes(cMrk)), [{
              _key: blk._key
            }, "children", {
              _key: child._key
            }, "marks"])),
            description: `Block with _key '${blk._key}' contains marks (${orphaned}) not supported by the current content model.`,
            action: "Remove invalid marks",
            item: blk,
            i18n: {
              description: "inputs.portable-text.invalid-value.orphaned-marks.description",
              action: "inputs.portable-text.invalid-value.orphaned-marks.action",
              values: {
                key: blk._key,
                orphanedMarks: orphanedMarks.map((m) => m.toString())
              }
            }
          }, !0;
        }
      }
      textBlock.children.some((child, cIndex) => {
        if (typeof child != "object" || child === null)
          return resolution = {
            patches: [unset([{
              _key: blk._key
            }, "children", cIndex])],
            description: `Child at index '${cIndex}' in block with key '${blk._key}' is not an object.`,
            action: "Remove the item",
            item: blk,
            i18n: {
              description: "inputs.portable-text.invalid-value.non-object-child.description",
              action: "inputs.portable-text.invalid-value.non-object-child.action",
              values: {
                key: blk._key,
                index: cIndex
              }
            }
          }, !0;
        if (!child._key || typeof child._key != "string") {
          const newChild = {
            ...child,
            _key: keyGenerator()
          };
          return resolution = {
            autoResolve: !0,
            patches: [set(newChild, [{
              _key: blk._key
            }, "children", cIndex])],
            description: `Child at index ${cIndex} is missing required _key in block with _key ${blk._key}.`,
            action: "Set a new random _key on the object",
            item: blk,
            i18n: {
              description: "inputs.portable-text.invalid-value.missing-child-key.description",
              action: "inputs.portable-text.invalid-value.missing-child-key.action",
              values: {
                key: blk._key,
                index: cIndex
              }
            }
          }, !0;
        }
        return child._type ? validChildTypes.includes(child._type) ? child._type === types.span.name && typeof child.text != "string" ? (resolution = {
          patches: [set({
            ...child,
            text: ""
          }, [{
            _key: blk._key
          }, "children", {
            _key: child._key
          }])],
          description: `Child with _key '${child._key}' in block with key '${blk._key}' has missing or invalid text property!`,
          action: "Write an empty text property to the object",
          item: blk,
          i18n: {
            description: "inputs.portable-text.invalid-value.invalid-span-text.description",
            action: "inputs.portable-text.invalid-value.invalid-span-text.action",
            values: {
              key: blk._key,
              childKey: child._key
            }
          }
        }, !0) : !1 : (resolution = {
          patches: [unset([{
            _key: blk._key
          }, "children", {
            _key: child._key
          }])],
          description: `Child with _key '${child._key}' in block with key '${blk._key}' has invalid '_type' property (${child._type}).`,
          action: "Remove the object",
          item: blk,
          i18n: {
            description: "inputs.portable-text.invalid-value.disallowed-child-type.description",
            action: "inputs.portable-text.invalid-value.disallowed-child-type.action",
            values: {
              key: blk._key,
              childKey: child._key,
              childType: child._type
            }
          }
        }, !0) : (resolution = {
          patches: [unset([{
            _key: blk._key
          }, "children", {
            _key: child._key
          }])],
          description: `Child with _key '${child._key}' in block with key '${blk._key}' is missing '_type' property.`,
          action: "Remove the object",
          item: blk,
          i18n: {
            description: "inputs.portable-text.invalid-value.missing-child-type.description",
            action: "inputs.portable-text.invalid-value.missing-child-type.action",
            values: {
              key: blk._key,
              childKey: child._key
            }
          }
        }, !0);
      }) && (valid = !1);
    }
    return !1;
  }) && (valid = !1), {
    valid,
    resolution,
    value
  });
}
const syncValueCallback = ({
  sendBack,
  input
}) => {
  updateValue({
    context: input.context,
    sendBack,
    slateEditor: input.slateEditor,
    value: input.value,
    streamBlocks: input.streamBlocks
  });
}, syncValueLogic = fromCallback(syncValueCallback), syncMachine = setup({
  types: {
    context: {},
    input: {},
    events: {},
    emitted: {}
  },
  actions: {
    "assign initial value synced": assign({
      initialValueSynced: !0
    }),
    "assign readOnly": assign({
      readOnly: ({
        event
      }) => (assertEvent(event, "update readOnly"), event.readOnly)
    }),
    "assign pending value": assign({
      pendingValue: ({
        event
      }) => (assertEvent(event, "update value"), event.value)
    }),
    "clear pending value": assign({
      pendingValue: void 0
    }),
    "assign previous value": assign({
      previousValue: ({
        event
      }) => (assertEvent(event, "done syncing"), event.value)
    }),
    "emit done syncing value": emit({
      type: "done syncing value"
    }),
    "emit syncing value": emit({
      type: "syncing value"
    })
  },
  guards: {
    "initial value synced": ({
      context
    }) => context.initialValueSynced,
    "is busy": ({
      context
    }) => {
      const isBusy = context.slateEditor.isDeferringMutations || context.slateEditor.isProcessingRemoteChanges;
      return debug$1.syncValue(JSON.stringify({
        isBusy,
        isDeferringMutations: context.slateEditor.isDeferringMutations,
        isProcessingRemoteChanges: context.slateEditor.isProcessingRemoteChanges
      })), isBusy;
    },
    "is empty value": ({
      event
    }) => event.type === "update value" && event.value === void 0,
    "is empty array": ({
      event
    }) => event.type === "update value" && Array.isArray(event.value) && event.value.length === 0,
    "is new value": ({
      context,
      event
    }) => event.type !== "update value" || context.previousValue === event.value ? !1 : !isEqualValues({
      schema: context.schema
    }, context.previousValue, event.value),
    "value changed while syncing": ({
      context,
      event
    }) => event.type !== "done syncing" || context.pendingValue === event.value ? !1 : !isEqualValues({
      schema: context.schema
    }, context.pendingValue, event.value),
    "pending value equals previous value": ({
      context
    }) => isEqualValues({
      schema: context.schema
    }, context.pendingValue, context.previousValue)
  },
  actors: {
    "sync value": syncValueLogic
  }
}).createMachine({
  id: "sync",
  context: ({
    input
  }) => ({
    initialValue: input.initialValue,
    initialValueSynced: !1,
    keyGenerator: input.keyGenerator,
    schema: input.schema,
    readOnly: input.readOnly,
    slateEditor: input.slateEditor,
    pendingValue: void 0,
    previousValue: void 0
  }),
  entry: [raise$1(({
    context
  }) => ({
    type: "update value",
    value: context.initialValue
  }))],
  on: {
    "update readOnly": {
      actions: ["assign readOnly"]
    }
  },
  initial: "idle",
  states: {
    idle: {
      entry: [() => {
        debug$1.syncValue("entry: syncing->idle");
      }],
      exit: [() => {
        debug$1.syncValue("exit: syncing->idle");
      }],
      on: {
        "update value": [{
          guard: and(["is empty value", not("initial value synced")]),
          actions: ["assign initial value synced", "emit done syncing value"]
        }, {
          guard: and(["is empty array", not("initial value synced")]),
          actions: ["assign initial value synced", emit({
            type: "value changed",
            value: []
          }), "emit done syncing value"]
        }, {
          guard: and(["is busy", "is new value"]),
          target: "busy",
          actions: ["assign pending value"]
        }, {
          guard: "is new value",
          target: "syncing",
          actions: ["assign pending value"]
        }, {
          guard: not("initial value synced"),
          actions: [() => {
            debug$1.syncValue("no new value \u2013 setting initial value as synced");
          }, "assign initial value synced", "emit done syncing value"]
        }, {
          actions: [() => {
            debug$1.syncValue("no new value and initial value already synced");
          }]
        }]
      }
    },
    busy: {
      entry: [() => {
        debug$1.syncValue("entry: syncing->busy");
      }],
      exit: [() => {
        debug$1.syncValue("exit: syncing->busy");
      }],
      after: {
        1e3: [{
          guard: "is busy",
          target: ".",
          reenter: !0,
          actions: [() => {
            debug$1.syncValue("reenter: syncing->busy");
          }]
        }, {
          target: "syncing"
        }]
      },
      on: {
        "update value": [{
          guard: "is new value",
          actions: ["assign pending value"]
        }]
      }
    },
    syncing: {
      entry: [() => {
        debug$1.syncValue("entry: syncing->syncing");
      }, "emit syncing value"],
      exit: [() => {
        debug$1.syncValue("exit: syncing->syncing");
      }, "emit done syncing value"],
      invoke: {
        src: "sync value",
        id: "sync value",
        input: ({
          context
        }) => ({
          context: {
            keyGenerator: context.keyGenerator,
            previousValue: context.previousValue,
            readOnly: context.readOnly,
            schema: context.schema
          },
          slateEditor: context.slateEditor,
          streamBlocks: !context.initialValueSynced,
          value: context.pendingValue
        })
      },
      on: {
        "update value": {
          guard: "is new value",
          actions: ["assign pending value"]
        },
        patch: {
          actions: [emit(({
            event
          }) => event)]
        },
        "invalid value": {
          actions: [emit(({
            event
          }) => event)]
        },
        "value changed": {
          actions: [emit(({
            event
          }) => event)]
        },
        "done syncing": [{
          guard: "value changed while syncing",
          actions: ["assign previous value", "assign initial value synced"],
          target: "syncing",
          reenter: !0
        }, {
          target: "idle",
          actions: ["clear pending value", "assign previous value", "assign initial value synced"]
        }]
      }
    }
  }
});
async function updateValue({
  context,
  sendBack,
  slateEditor,
  streamBlocks,
  value
}) {
  let doneSyncing = !1, isChanged = !1, isValid = !0;
  const hadSelection = !!slateEditor.selection;
  if ((!value || value.length === 0) && (clearEditor({
    slateEditor,
    doneSyncing
  }), isChanged = !0), value && value.length > 0)
    if (streamBlocks)
      await new Promise((resolve) => {
        if (doneSyncing) {
          resolve();
          return;
        }
        isChanged = removeExtraBlocks({
          slateEditor,
          value
        }), (async () => {
          for await (const [currentBlock, currentBlockIndex] of getStreamedBlocks({
            value
          })) {
            const {
              blockChanged,
              blockValid
            } = syncBlock({
              context,
              sendBack,
              block: currentBlock,
              index: currentBlockIndex,
              slateEditor,
              value
            });
            if (isChanged = blockChanged || isChanged, isValid = isValid && blockValid, !isValid)
              break;
          }
          resolve();
        })();
      });
    else {
      if (doneSyncing)
        return;
      isChanged = removeExtraBlocks({
        slateEditor,
        value
      });
      let index = 0;
      for (const block of value) {
        const {
          blockChanged,
          blockValid
        } = syncBlock({
          context,
          sendBack,
          block,
          index,
          slateEditor,
          value
        });
        if (isChanged = blockChanged || isChanged, isValid = isValid && blockValid, !blockValid)
          break;
        index++;
      }
    }
  if (!isValid) {
    debug$1.syncValue("Invalid value, returning"), doneSyncing = !0, sendBack({
      type: "done syncing",
      value
    });
    return;
  }
  if (isChanged) {
    debug$1.syncValue("remote value changed, syncing local value");
    try {
      slateEditor.onChange();
    } catch (err) {
      console.error(err), sendBack({
        type: "invalid value",
        resolution: null,
        value
      }), doneSyncing = !0, sendBack({
        type: "done syncing",
        value
      });
      return;
    }
    hadSelection && !slateEditor.selection && slateEditor.children.length > 0 && (Transforms.select(slateEditor, Editor.start(slateEditor, [])), slateEditor.onChange()), sendBack({
      type: "value changed",
      value
    });
  } else
    debug$1.syncValue("remote value and local value are equal, no need to sync");
  doneSyncing = !0, sendBack({
    type: "done syncing",
    value
  });
}
async function* getStreamedBlocks({
  value
}) {
  let index = 0;
  for await (const block of value)
    index % 10 === 0 && await new Promise((resolve) => setTimeout(resolve, 0)), yield [block, index], index++;
}
function clearEditor({
  slateEditor,
  doneSyncing
}) {
  Editor.withoutNormalizing(slateEditor, () => {
    pluginWithoutHistory(slateEditor, () => {
      withRemoteChanges(slateEditor, () => {
        withoutPatching(slateEditor, () => {
          if (doneSyncing)
            return;
          const childrenLength = slateEditor.children.length;
          slateEditor.children.forEach((_, index) => {
            Transforms.removeNodes(slateEditor, {
              at: [childrenLength - 1 - index]
            });
          });
        });
      });
    });
  });
}
function removeExtraBlocks({
  slateEditor,
  value
}) {
  let isChanged = !1;
  return Editor.withoutNormalizing(slateEditor, () => {
    withRemoteChanges(slateEditor, () => {
      withoutPatching(slateEditor, () => {
        const childrenLength = slateEditor.children.length;
        if (value.length < childrenLength) {
          for (let i = childrenLength - 1; i > value.length - 1; i--)
            Transforms.removeNodes(slateEditor, {
              at: [i]
            });
          isChanged = !0;
        }
      });
    });
  }), isChanged;
}
function syncBlock({
  context,
  sendBack,
  block,
  index,
  slateEditor,
  value
}) {
  const oldSlateBlock = slateEditor.children.at(index), oldBlock = slateEditor.value.at(index);
  if (!oldSlateBlock || !oldBlock) {
    const validation2 = validateValue([block], context.schema, context.keyGenerator);
    if (debug$1.syncValue("Validating and inserting new block in the end of the value", block), validation2.valid || validation2.resolution?.autoResolve) {
      const slateBlock = toSlateBlock(block, {
        schemaTypes: context.schema
      });
      return Editor.withoutNormalizing(slateEditor, () => {
        withRemoteChanges(slateEditor, () => {
          withoutPatching(slateEditor, () => {
            Transforms.insertNodes(slateEditor, slateBlock, {
              at: [index]
            });
          });
        });
      }), {
        blockChanged: !0,
        blockValid: !0
      };
    }
    return debug$1.syncValue("Invalid", validation2), sendBack({
      type: "invalid value",
      resolution: validation2.resolution,
      value
    }), {
      blockChanged: !1,
      blockValid: !1
    };
  }
  if (isEqualBlocks(context, block, oldBlock))
    return {
      blockChanged: !1,
      blockValid: !0
    };
  const blockToValidate = value[index];
  if (!blockToValidate)
    return {
      blockChanged: !1,
      blockValid: !0
    };
  const validation = validateValue([blockToValidate], context.schema, context.keyGenerator);
  return !validation.valid && validation.resolution?.autoResolve && validation.resolution?.patches.length > 0 && !context.readOnly && context.previousValue && context.previousValue !== value && (console.warn(`${validation.resolution.action} for block with _key '${blockToValidate._key}'. ${validation.resolution?.description}`), validation.resolution.patches.forEach((patch) => {
    sendBack({
      type: "patch",
      patch
    });
  })), validation.valid || validation.resolution?.autoResolve ? (oldBlock._key === block._key && oldBlock._type === block._type ? (debug$1.syncValue("Updating block", oldBlock, block), Editor.withoutNormalizing(slateEditor, () => {
    withRemoteChanges(slateEditor, () => {
      withoutPatching(slateEditor, () => {
        updateBlock({
          context,
          slateEditor,
          oldSlateBlock,
          block,
          index
        });
      });
    });
  })) : (debug$1.syncValue("Replacing block", oldBlock, block), Editor.withoutNormalizing(slateEditor, () => {
    withRemoteChanges(slateEditor, () => {
      withoutPatching(slateEditor, () => {
        replaceBlock({
          context,
          slateEditor,
          block,
          index
        });
      });
    });
  })), {
    blockChanged: !0,
    blockValid: !0
  }) : (sendBack({
    type: "invalid value",
    resolution: validation.resolution,
    value
  }), {
    blockChanged: !1,
    blockValid: !1
  });
}
function replaceBlock({
  context,
  slateEditor,
  block,
  index
}) {
  const slateBlock = toSlateBlock(block, {
    schemaTypes: context.schema
  }), currentSelection = slateEditor.selection, selectionFocusOnBlock = currentSelection && currentSelection.focus.path[0] === index;
  selectionFocusOnBlock && Transforms.deselect(slateEditor), Transforms.removeNodes(slateEditor, {
    at: [index]
  }), Transforms.insertNodes(slateEditor, slateBlock, {
    at: [index]
  }), slateEditor.onChange(), selectionFocusOnBlock && Transforms.select(slateEditor, currentSelection);
}
function updateBlock({
  context,
  slateEditor,
  oldSlateBlock,
  block,
  index
}) {
  const slateBlock = toSlateBlock(block, {
    schemaTypes: context.schema
  });
  if (Transforms.setNodes(slateEditor, slateBlock, {
    at: [index]
  }), slateEditor.isTextBlock(slateBlock) && slateEditor.isTextBlock(oldSlateBlock)) {
    const oldBlockChildrenLength = oldSlateBlock.children.length;
    slateBlock.children.length < oldBlockChildrenLength && Array.from(Array(oldBlockChildrenLength - slateBlock.children.length)).forEach((_, i) => {
      const childIndex = oldBlockChildrenLength - 1 - i;
      childIndex > 0 && (debug$1.syncValue("Removing child"), Transforms.removeNodes(slateEditor, {
        at: [index, childIndex]
      }));
    }), slateBlock.children.forEach((currentBlockChild, currentBlockChildIndex) => {
      const oldBlockChild = oldSlateBlock.children.at(currentBlockChildIndex), isChildChanged = !oldBlockChild || !isEqualChild(currentBlockChild, oldBlockChild), isTextChanged = oldBlockChild && Text$1.isText(oldBlockChild) && currentBlockChild.text !== oldBlockChild.text, path2 = [index, currentBlockChildIndex];
      if (isChildChanged)
        if (currentBlockChild._key === oldBlockChild?._key && currentBlockChild._type === oldBlockChild?._type) {
          debug$1.syncValue("Updating changed child", currentBlockChild, oldBlockChild), Transforms.setNodes(slateEditor, currentBlockChild, {
            at: path2
          });
          const isSpanNode2 = isSpan({
            schema: context.schema
          }, currentBlockChild) && isSpan({
            schema: context.schema
          }, oldBlockChild);
          isSpanNode2 && isTextChanged ? (oldBlockChild.text.length > 0 && deleteText(slateEditor, {
            at: {
              focus: {
                path: path2,
                offset: 0
              },
              anchor: {
                path: path2,
                offset: oldBlockChild.text.length
              }
            }
          }), Transforms.insertText(slateEditor, currentBlockChild.text, {
            at: path2
          }), slateEditor.onChange()) : isSpanNode2 || (debug$1.syncValue("Updating changed inline object child", currentBlockChild), Transforms.setNodes(slateEditor, {
            _key: VOID_CHILD_KEY
          }, {
            at: [...path2, 0],
            voids: !0
          }));
        } else oldBlockChild ? (debug$1.syncValue("Replacing child", currentBlockChild), Transforms.removeNodes(slateEditor, {
          at: [index, currentBlockChildIndex]
        }), Transforms.insertNodes(slateEditor, currentBlockChild, {
          at: [index, currentBlockChildIndex]
        }), slateEditor.onChange()) : oldBlockChild || (debug$1.syncValue("Inserting new child", currentBlockChild), Transforms.insertNodes(slateEditor, currentBlockChild, {
          at: [index, currentBlockChildIndex]
        }), slateEditor.onChange());
    });
  }
}
function createInternalEditor(config) {
  debug$1.setup("creating new editor instance");
  const subscriptions = [], editorActor = createActor(editorMachine, {
    input: editorConfigToMachineInput(config)
  }), relayActor = createActor(relayMachine), slateEditor = createSlateEditor({
    editorActor,
    relayActor,
    subscriptions
  }), editable = createEditableAPI(slateEditor.instance, editorActor), {
    mutationActor,
    syncActor
  } = createActors({
    editorActor,
    relayActor,
    slateEditor: slateEditor.instance,
    subscriptions
  }), editor = {
    dom: createEditorDom((event) => editorActor.send(event), slateEditor.instance),
    getSnapshot: () => getEditorSnapshot({
      editorActorSnapshot: editorActor.getSnapshot(),
      slateEditorInstance: slateEditor.instance
    }),
    registerBehavior: (behaviorConfig) => {
      const priority = createEditorPriority({
        name: "custom",
        reference: {
          priority: corePriority,
          importance: "higher"
        }
      }), behaviorConfigWithPriority = {
        ...behaviorConfig,
        priority
      };
      return editorActor.send({
        type: "add behavior",
        behaviorConfig: behaviorConfigWithPriority
      }), () => {
        editorActor.send({
          type: "remove behavior",
          behaviorConfig: behaviorConfigWithPriority
        });
      };
    },
    send: (event) => {
      switch (event.type) {
        case "update value":
          syncActor.send(event);
          break;
        case "update readOnly":
        case "patches":
          editorActor.send(event);
          break;
        default:
          editorActor.send(rerouteExternalBehaviorEvent({
            event,
            slateEditor: slateEditor.instance
          }));
      }
    },
    on: (event, listener) => relayActor.on(event, (event2) => {
      switch (event2.type) {
        case "blurred":
        case "done loading":
        case "editable":
        case "focused":
        case "invalid value":
        case "loading":
        case "mutation":
        case "patch":
        case "read only":
        case "ready":
        case "selection":
        case "value changed":
          listener(event2);
          break;
      }
    }),
    _internal: {
      editable,
      editorActor,
      slateEditor
    }
  };
  return {
    actors: {
      editorActor,
      mutationActor,
      relayActor,
      syncActor
    },
    editor,
    subscriptions
  };
}
function editorConfigToMachineInput(config) {
  const {
    legacySchema,
    schema
  } = compileSchemasFromEditorConfig(config);
  return {
    converters: createCoreConverters(legacySchema),
    getLegacySchema: () => legacySchema,
    keyGenerator: config.keyGenerator ?? defaultKeyGenerator,
    readOnly: config.readOnly,
    schema,
    initialValue: config.initialValue
  };
}
function compileSchemasFromEditorConfig(config) {
  const legacySchema = config.schemaDefinition ? compileSchemaDefinitionToPortableTextMemberSchemaTypes(config.schemaDefinition) : createPortableTextMemberSchemaTypes(config.schema.hasOwnProperty("jsonType") ? config.schema : compileType(config.schema)), schema = config.schemaDefinition ? compileSchema(config.schemaDefinition) : portableTextMemberSchemaTypesToSchema(legacySchema);
  return {
    legacySchema,
    schema
  };
}
function createActors(config) {
  debug$1.setup("creating new actors");
  const mutationActor = createActor(mutationMachine, {
    input: {
      readOnly: config.editorActor.getSnapshot().matches({
        "edit mode": "read only"
      }),
      schema: config.editorActor.getSnapshot().context.schema,
      slateEditor: config.slateEditor
    }
  }), syncActor = createActor(syncMachine, {
    input: {
      initialValue: config.editorActor.getSnapshot().context.initialValue,
      keyGenerator: config.editorActor.getSnapshot().context.keyGenerator,
      readOnly: config.editorActor.getSnapshot().matches({
        "edit mode": "read only"
      }),
      schema: config.editorActor.getSnapshot().context.schema,
      slateEditor: config.slateEditor
    }
  });
  return config.subscriptions.push(() => {
    const subscription = mutationActor.on("*", (event) => {
      event.type === "mutation" && config.editorActor.send({
        type: "mutation",
        patches: event.patches,
        value: event.snapshot
      }), event.type === "patch" && config.relayActor.send(event);
    });
    return () => {
      mutationActor.send({
        type: "emit changes"
      }), subscription.unsubscribe();
    };
  }), config.subscriptions.push(() => {
    const subscription = syncActor.on("*", (event) => {
      switch (event.type) {
        case "invalid value":
          config.relayActor.send(event);
          break;
        case "value changed":
          config.relayActor.send(event);
          break;
        case "patch":
          config.editorActor.send({
            ...event,
            type: "internal.patch",
            value: config.slateEditor.value
          });
          break;
        default:
          config.editorActor.send(event);
      }
    });
    return () => {
      subscription.unsubscribe();
    };
  }), config.subscriptions.push(() => {
    const subscription = config.editorActor.subscribe((snapshot) => {
      snapshot.matches({
        "edit mode": "read only"
      }) ? (mutationActor.send({
        type: "update readOnly",
        readOnly: !0
      }), syncActor.send({
        type: "update readOnly",
        readOnly: !0
      })) : (mutationActor.send({
        type: "update readOnly",
        readOnly: !1
      }), syncActor.send({
        type: "update readOnly",
        readOnly: !1
      }));
    });
    return () => {
      subscription.unsubscribe();
    };
  }), config.subscriptions.push(() => {
    const subscription = config.editorActor.on("*", (event) => {
      switch (event.type) {
        case "editable":
        case "mutation":
        case "ready":
        case "read only":
        case "selection":
          config.relayActor.send(event);
          break;
        case "internal.patch":
          mutationActor.send({
            ...event,
            type: "patch"
          });
          break;
      }
    });
    return () => {
      subscription.unsubscribe();
    };
  }), {
    mutationActor,
    syncActor
  };
}
function eventToChange(event) {
  switch (event.type) {
    case "blurred":
      return {
        type: "blur",
        event: event.event
      };
    case "patch":
      return event;
    case "loading":
      return {
        type: "loading",
        isLoading: !0
      };
    case "done loading":
      return {
        type: "loading",
        isLoading: !1
      };
    case "focused":
      return {
        type: "focus",
        event: event.event
      };
    case "value changed":
      return {
        type: "value",
        value: event.value
      };
    case "invalid value":
      return {
        type: "invalidValue",
        resolution: event.resolution,
        value: event.value
      };
    case "mutation":
      return {
        type: "mutation",
        patches: event.patches,
        snapshot: event.value
      };
    case "ready":
      return event;
    case "selection":
      return event;
    case "unset":
      return event;
  }
}
class PortableTextEditor {
  /**
   * An observable of all the editor changes.
   */
  change$ = new Subject();
  /**
   * A lookup table for all the relevant schema types for this portable text type.
   */
  /**
   * The editor instance
   */
  /*
   * The editor API (currently implemented with Slate).
   */
  constructor(config) {
    this.editor = config.editor, this.schemaTypes = config.editor._internal.editorActor.getSnapshot().context.getLegacySchema(), this.editable = config.editor._internal.editable;
  }
  setEditable = (editable) => {
    this.editor._internal.editable = {
      ...this.editor._internal.editable,
      ...editable
    };
  };
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const isActive = useEditorSelector(editor, selectors.getActiveAnnotations)
   * ```
   */
  static activeAnnotations = (editor) => editor && editor.editable ? editor.editable.activeAnnotations() : [];
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const isActive = useEditorSelector(editor, selectors.isActiveAnnotation(...))
   * ```
   */
  static isAnnotationActive = (editor, annotationType) => editor && editor.editable ? editor.editable.isAnnotationActive(annotationType) : !1;
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'annotation.add',
   *  annotation: {
   *    name: '...',
   *    value: {...},
   *  }
   * })
   * ```
   */
  static addAnnotation = (editor, type, value) => editor.editable?.addAnnotation(type, value);
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'blur',
   * })
   * ```
   */
  static blur = (editor) => {
    editor.editable?.blur();
  };
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'delete',
   *  at: {...},
   *  direction: '...',
   *  unit: '...',
   * })
   * ```
   */
  static delete = (editor, selection, options) => editor.editable?.delete(selection, options);
  static findDOMNode = (editor, element) => editor.editable?.findDOMNode(element);
  static findByPath = (editor, path2) => editor.editable?.findByPath(path2) || [];
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'focus',
   * })
   * ```
   */
  static focus = (editor) => {
    editor.editable?.focus();
  };
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const focusBlock = useEditorSelector(editor, selectors.getFocusBlock)
   * ```
   */
  static focusBlock = (editor) => editor.editable?.focusBlock();
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const focusChild = useEditorSelector(editor, selectors.getFocusChild)
   * ```
   */
  static focusChild = (editor) => editor.editable?.focusChild();
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const selection = useEditorSelector(editor, selectors.getSelection)
   * ```
   */
  static getSelection = (editor) => editor.editable ? editor.editable.getSelection() : null;
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const value = useEditorSelector(editor, selectors.getValue)
   * ```
   */
  static getValue = (editor) => editor.editable?.getValue();
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const isActive = useEditorSelector(editor, selectors.isActiveStyle(...))
   * ```
   */
  static hasBlockStyle = (editor, blockStyle) => editor.editable?.hasBlockStyle(blockStyle);
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const isActive = useEditorSelector(editor, selectors.isActiveListItem(...))
   * ```
   */
  static hasListStyle = (editor, listStyle) => editor.editable?.hasListStyle(listStyle);
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const isSelectionCollapsed = useEditorSelector(editor, selectors.isSelectionCollapsed)
   * ```
   */
  static isCollapsedSelection = (editor) => editor.editable?.isCollapsedSelection();
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const isSelectionExpanded = useEditorSelector(editor, selectors.isSelectionExpanded)
   * ```
   */
  static isExpandedSelection = (editor) => editor.editable?.isExpandedSelection();
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const isActive = useEditorSelector(editor, selectors.isActiveDecorator(...))
   * ```
   */
  static isMarkActive = (editor, mark) => editor.editable?.isMarkActive(mark);
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'insert.span',
   *  text: '...',
   *  annotations: [{name: '...', value: {...}}],
   *  decorators: ['...'],
   * })
   * editor.send({
   *  type: 'insert.inline object',
   *  inlineObject: {
   *    name: '...',
   *    value: {...},
   *  },
   * })
   * ```
   */
  static insertChild = (editor, type, value) => editor.editable?.insertChild(type, value);
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'insert.block object',
   *  blockObject: {
   *    name: '...',
   *    value: {...},
   *  },
   *  placement: 'auto' | 'after' | 'before',
   * })
   * ```
   */
  static insertBlock = (editor, type, value) => editor.editable?.insertBlock(type, value);
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'insert.break',
   * })
   * ```
   */
  static insertBreak = (editor) => editor.editable?.insertBreak();
  static isVoid = (editor, element) => editor.editable?.isVoid(element);
  static isObjectPath = (_editor, path2) => {
    if (!path2 || !Array.isArray(path2))
      return !1;
    const isChildObjectEditPath = path2.length > 3 && path2[1] === "children";
    return path2.length > 1 && path2[1] !== "children" || isChildObjectEditPath;
  };
  static marks = (editor) => editor.editable?.marks();
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'select',
   *  selection: {...},
   * })
   * ```
   */
  static select = (editor, selection) => {
    editor.editable?.select(selection);
  };
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'annotation.remove',
   *  annotation: {
   *    name: '...',
   *  },
   * })
   * ```
   */
  static removeAnnotation = (editor, type) => editor.editable?.removeAnnotation(type);
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'style.toggle',
   *  style: '...',
   * })
   * ```
   */
  static toggleBlockStyle = (editor, blockStyle) => editor.editable?.toggleBlockStyle(blockStyle);
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'list item.toggle',
   *  listItem: '...',
   * })
   * ```
   */
  static toggleList = (editor, listStyle) => editor.editable?.toggleList(listStyle);
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *  type: 'decorator.toggle',
   *  decorator: '...',
   * })
   * ```
   */
  static toggleMark = (editor, mark) => {
    editor.editable?.toggleMark(mark);
  };
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const selectedValue = useEditorSelector(editor, selectors.getSelectedValue)
   * ```
   */
  static getFragment = (editor) => editor.editable?.getFragment();
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *   type: 'history.undo',
   * })
   * ```
   */
  static undo = (editor) => {
    editor.editable?.undo();
  };
  /**
   * @deprecated
   * Use `editor.send(...)` instead
   *
   * ```
   * const editor = useEditor()
   * editor.send({
   *   type: 'history.redo',
   * })
   * ```
   */
  static redo = (editor) => {
    editor.editable?.redo();
  };
  /**
   * @deprecated
   * Use built-in selectors or write your own: https://www.portabletext.org/reference/selectors/
   *
   * ```
   * import * as selectors from '@portabletext/editor/selectors'
   * const editor = useEditor()
   * const isOverlapping = useEditorSelector(editor, selectors.isOverlappingSelection(selectionB))
   * ```
   */
  static isSelectionsOverlapping = (editor, selectionA, selectionB) => editor.editable?.isSelectionsOverlapping(selectionA, selectionB);
}
function EditorProvider(props) {
  const $ = c(29);
  let t0;
  $[0] !== props.initialConfig ? (t0 = () => {
    const internalEditor = createInternalEditor(props.initialConfig), portableTextEditor = new PortableTextEditor({
      editor: internalEditor.editor
    });
    return {
      internalEditor,
      portableTextEditor
    };
  }, $[0] = props.initialConfig, $[1] = t0) : t0 = $[1];
  const [t1] = useState(t0), {
    internalEditor: internalEditor_0,
    portableTextEditor: portableTextEditor_0
  } = t1;
  let t2;
  $[2] !== internalEditor_0.actors.editorActor || $[3] !== internalEditor_0.actors.mutationActor || $[4] !== internalEditor_0.actors.relayActor || $[5] !== internalEditor_0.actors.syncActor || $[6] !== internalEditor_0.editor._internal.slateEditor.instance || $[7] !== internalEditor_0.subscriptions || $[8] !== portableTextEditor_0 ? (t2 = () => {
    const unsubscribers = [];
    for (const subscription of internalEditor_0.subscriptions)
      unsubscribers.push(subscription());
    const relayActorSubscription = internalEditor_0.actors.relayActor.on("*", (event) => {
      const change = eventToChange(event);
      change && portableTextEditor_0.change$.next(change);
    });
    return unsubscribers.push(relayActorSubscription.unsubscribe), internalEditor_0.actors.editorActor.start(), internalEditor_0.actors.editorActor.send({
      type: "add slate editor",
      editor: internalEditor_0.editor._internal.slateEditor.instance
    }), internalEditor_0.actors.mutationActor.start(), internalEditor_0.actors.relayActor.start(), internalEditor_0.actors.syncActor.start(), () => {
      for (const unsubscribe of unsubscribers)
        unsubscribe();
      stopActor(internalEditor_0.actors.editorActor), stopActor(internalEditor_0.actors.mutationActor), stopActor(internalEditor_0.actors.relayActor), stopActor(internalEditor_0.actors.syncActor);
    };
  }, $[2] = internalEditor_0.actors.editorActor, $[3] = internalEditor_0.actors.mutationActor, $[4] = internalEditor_0.actors.relayActor, $[5] = internalEditor_0.actors.syncActor, $[6] = internalEditor_0.editor._internal.slateEditor.instance, $[7] = internalEditor_0.subscriptions, $[8] = portableTextEditor_0, $[9] = t2) : t2 = $[9];
  let t3;
  $[10] !== internalEditor_0 || $[11] !== portableTextEditor_0 ? (t3 = [internalEditor_0, portableTextEditor_0], $[10] = internalEditor_0, $[11] = portableTextEditor_0, $[12] = t3) : t3 = $[12], useEffect(t2, t3);
  let t4;
  $[13] !== portableTextEditor_0 || $[14] !== props.children ? (t4 = /* @__PURE__ */ jsx(PortableTextEditorContext.Provider, { value: portableTextEditor_0, children: props.children }), $[13] = portableTextEditor_0, $[14] = props.children, $[15] = t4) : t4 = $[15];
  let t5;
  $[16] !== internalEditor_0.editor._internal.slateEditor.initialValue || $[17] !== internalEditor_0.editor._internal.slateEditor.instance || $[18] !== t4 ? (t5 = /* @__PURE__ */ jsx(Slate, { editor: internalEditor_0.editor._internal.slateEditor.instance, initialValue: internalEditor_0.editor._internal.slateEditor.initialValue, children: t4 }), $[16] = internalEditor_0.editor._internal.slateEditor.initialValue, $[17] = internalEditor_0.editor._internal.slateEditor.instance, $[18] = t4, $[19] = t5) : t5 = $[19];
  let t6;
  $[20] !== internalEditor_0.actors.relayActor || $[21] !== t5 ? (t6 = /* @__PURE__ */ jsx(RelayActorContext.Provider, { value: internalEditor_0.actors.relayActor, children: t5 }), $[20] = internalEditor_0.actors.relayActor, $[21] = t5, $[22] = t6) : t6 = $[22];
  let t7;
  $[23] !== internalEditor_0.actors.editorActor || $[24] !== t6 ? (t7 = /* @__PURE__ */ jsx(EditorActorContext.Provider, { value: internalEditor_0.actors.editorActor, children: t6 }), $[23] = internalEditor_0.actors.editorActor, $[24] = t6, $[25] = t7) : t7 = $[25];
  let t8;
  return $[26] !== internalEditor_0.editor || $[27] !== t7 ? (t8 = /* @__PURE__ */ jsx(EditorContext$1.Provider, { value: internalEditor_0.editor, children: t7 }), $[26] = internalEditor_0.editor, $[27] = t7, $[28] = t8) : t8 = $[28], t8;
}
const usePortableTextEditorSelection = () => {
  const $ = c(5), editorActor = useContext(EditorActorContext);
  let t0;
  $[0] !== editorActor ? (t0 = editorActor.getSnapshot(), $[0] = editorActor, $[1] = t0) : t0 = $[1];
  const [selection, setSelection2] = useState(t0.context.selection);
  let t1, t2;
  return $[2] !== editorActor ? (t1 = () => {
    const subscription = editorActor.on("selection", (event) => {
      startTransition(() => {
        setSelection2(event.selection);
      });
    });
    return () => {
      subscription.unsubscribe();
    };
  }, t2 = [editorActor], $[2] = editorActor, $[3] = t1, $[4] = t2) : (t1 = $[3], t2 = $[4]), useEffect(t1, t2), selection;
};
export {
  EditorProvider,
  PortableTextEditable,
  PortableTextEditor,
  defineSchema,
  defaultKeyGenerator as keyGenerator,
  useEditor,
  useEditorSelector,
  usePortableTextEditor,
  usePortableTextEditorSelection
};
//# sourceMappingURL=index.js.map
