import * as _portabletext_schema6 from "@portabletext/schema";
import { AnnotationDefinition, AnnotationSchemaType, BaseDefinition, BlockObjectDefinition, BlockObjectSchemaType, DecoratorDefinition, DecoratorSchemaType, FieldDefinition, InlineObjectDefinition, InlineObjectSchemaType, ListDefinition, ListSchemaType, PortableTextBlock, PortableTextBlock as PortableTextBlock$1, PortableTextChild, PortableTextChild as PortableTextChild$1, PortableTextListBlock, PortableTextObject, PortableTextObject as PortableTextObject$1, PortableTextSpan, PortableTextSpan as PortableTextSpan$1, PortableTextTextBlock, PortableTextTextBlock as PortableTextTextBlock$1, Schema, SchemaDefinition, SchemaDefinition as SchemaDefinition$1, StyleDefinition, StyleSchemaType, TypedObject, defineSchema } from "@portabletext/schema";
import * as xstate73 from "xstate";
import { ActorRef, ActorRefFrom, EventObject, Snapshot } from "xstate";
import * as react10 from "react";
import React$1, { BaseSyntheticEvent, ClipboardEvent as ClipboardEvent$1, FocusEvent, JSX, PropsWithChildren, ReactElement, RefObject, TextareaHTMLAttributes } from "react";
import { Patch, Patch as Patch$1 } from "@portabletext/patches";
import { Observable, Subject } from "rxjs";
import { ArrayDefinition, ArraySchemaType, BlockDecoratorDefinition, BlockListDefinition, BlockStyleDefinition, ObjectSchemaType } from "@sanity/types";
type MIMEType = `${string}/${string}`;
/**
 * @internal
 */
type PickFromUnion<TUnion, TTagKey extends keyof TUnion, TPickedTags extends TUnion[TTagKey]> = TUnion extends Record<TTagKey, TPickedTags> ? TUnion : never;
type NamespaceEvent<TEvent, TNamespace$1 extends string> = TEvent extends {
  type: infer TEventType;
} ? { [K in keyof TEvent]: K extends 'type' ? `${TNamespace$1}.${TEventType & string}` : TEvent[K] } : never;
type StrictExtract<T, U extends T> = U;
type Converter<TMIMEType extends MIMEType = MIMEType> = {
  mimeType: TMIMEType;
  serialize: Serializer<TMIMEType>;
  deserialize: Deserializer<TMIMEType>;
};
type ConverterEvent<TMIMEType extends MIMEType = MIMEType> = {
  type: 'serialize';
  originEvent: 'clipboard.copy' | 'clipboard.cut' | 'drag.dragstart';
} | {
  type: 'serialization.failure';
  mimeType: TMIMEType;
  originEvent: 'clipboard.copy' | 'clipboard.cut' | 'drag.dragstart';
  reason: string;
} | {
  type: 'serialization.success';
  data: string;
  mimeType: TMIMEType;
  originEvent: 'clipboard.copy' | 'clipboard.cut' | 'drag.dragstart';
} | {
  type: 'deserialize';
  data: string;
} | {
  type: 'deserialization.failure';
  mimeType: TMIMEType;
  reason: string;
} | {
  type: 'deserialization.success';
  data: Array<PortableTextBlock>;
  mimeType: TMIMEType;
};
type Serializer<TMIMEType extends MIMEType> = ({
  snapshot,
  event
}: {
  snapshot: EditorSnapshot;
  event: PickFromUnion<ConverterEvent<TMIMEType>, 'type', 'serialize'>;
}) => PickFromUnion<ConverterEvent<TMIMEType>, 'type', 'serialization.success' | 'serialization.failure'>;
type Deserializer<TMIMEType extends MIMEType> = ({
  snapshot,
  event
}: {
  snapshot: EditorSnapshot;
  event: PickFromUnion<ConverterEvent<TMIMEType>, 'type', 'deserialize'>;
}) => PickFromUnion<ConverterEvent<TMIMEType>, 'type', 'deserialization.success' | 'deserialization.failure'>;
/**
 * A segment in a path that identifies an element by its `_key` property.
 * @public
 */
interface KeyedSegment {
  _key: string;
}
/**
 * A tuple representing a range selection, e.g., `[0, 5]` or `['', 3]`.
 * @public
 */
type IndexTuple = [number | '', number | ''];
/**
 * A single segment in a path. Can be:
 * - A string (property name)
 * - A number (array index)
 * - A KeyedSegment (object with `_key`)
 * - An IndexTuple (range selection)
 * @public
 */
type PathSegment = string | number | KeyedSegment | IndexTuple;
/**
 * A path is an array of path segments that describes a location in a document.
 * @public
 */
type Path = PathSegment[];
/**
 * @public
 */
type BlockPath = [{
  _key: string;
}];
/**
 * @public
 */
type AnnotationPath = [{
  _key: string;
}, 'markDefs', {
  _key: string;
}];
/**
 * @public
 */
type ChildPath = [{
  _key: string;
}, 'children', {
  _key: string;
}];
type LeafEdge = 'start' | 'end';
type MaximizeMode = RangeMode | 'all';
type MoveUnit = 'offset' | 'character' | 'word' | 'line';
type RangeDirection = TextDirection | 'outward' | 'inward';
type RangeMode = 'highest' | 'lowest';
type SelectionEdge = 'anchor' | 'focus' | 'start' | 'end';
type SelectionMode = 'all' | 'highest' | 'lowest';
type TextDirection = 'forward' | 'backward';
type TextUnit = 'character' | 'word' | 'line' | 'block';
type TextUnitAdjustment = TextUnit | 'offset';
type OmitFirstArg<F> = F extends ((x: any, ...args: infer P) => infer R) ? (...args: P) => R : never;
interface NodeInsertNodesOptions<T extends Node$1> {
  at?: Location;
  match?: NodeMatch<T>;
  mode?: RangeMode;
  hanging?: boolean;
  select?: boolean;
  voids?: boolean;
  batchDirty?: boolean;
}
interface NodeTransforms {
  /**
   * Insert nodes in the editor
   * at the specified location or (if not defined) the current selection or (if not defined) the end of the document.
   */
  insertNodes: <T extends Node$1>(editor: Editor$1, nodes: Node$1 | Node$1[], options?: NodeInsertNodesOptions<T>) => void;
  /**
   * Lift nodes at a specific location upwards in the document tree, splitting
   * their parent in two if necessary.
   */
  liftNodes: <T extends Node$1>(editor: Editor$1, options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: MaximizeMode;
    voids?: boolean;
  }) => void;
  /**
   * Merge a node at a location with the previous node of the same depth,
   * removing any empty containing nodes after the merge if necessary.
   */
  mergeNodes: <T extends Node$1>(editor: Editor$1, options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: RangeMode;
    hanging?: boolean;
    voids?: boolean;
  }) => void;
  /**
   * Move the nodes at a location to a new location.
   */
  moveNodes: <T extends Node$1>(editor: Editor$1, options: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: MaximizeMode;
    to: Path$1;
    voids?: boolean;
  }) => void;
  /**
   * Remove the nodes at a specific location in the document.
   */
  removeNodes: <T extends Node$1>(editor: Editor$1, options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: RangeMode;
    hanging?: boolean;
    voids?: boolean;
  }) => void;
  /**
   * Set new properties on the nodes at a location.
   */
  setNodes: <T extends Node$1>(editor: Editor$1, props: Partial<T>, options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: MaximizeMode;
    hanging?: boolean;
    split?: boolean;
    voids?: boolean;
    compare?: PropsCompare;
    merge?: PropsMerge;
  }) => void;
  /**
   * Split the nodes at a specific location.
   */
  splitNodes: <T extends Node$1>(editor: Editor$1, options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: RangeMode;
    always?: boolean;
    height?: number;
    voids?: boolean;
  }) => void;
  /**
   * Unset properties on the nodes at a location.
   */
  unsetNodes: <T extends Node$1>(editor: Editor$1, props: string | string[], options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: MaximizeMode;
    hanging?: boolean;
    split?: boolean;
    voids?: boolean;
  }) => void;
  /**
   * Unwrap the nodes at a location from a parent node, splitting the parent if
   * necessary to ensure that only the content in the range is unwrapped.
   */
  unwrapNodes: <T extends Node$1>(editor: Editor$1, options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: MaximizeMode;
    split?: boolean;
    voids?: boolean;
  }) => void;
  /**
   * Wrap the nodes at a location in a new container node, splitting the edges
   * of the range first to ensure that only the content in the range is wrapped.
   */
  wrapNodes: <T extends Node$1>(editor: Editor$1, element: Element$1, options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: MaximizeMode;
    split?: boolean;
    voids?: boolean;
  }) => void;
}
declare const NodeTransforms: NodeTransforms;
interface TextDeleteOptions {
  at?: Location;
  distance?: number;
  unit?: TextUnit;
  reverse?: boolean;
  hanging?: boolean;
  voids?: boolean;
}
interface TextInsertFragmentOptions {
  at?: Location;
  hanging?: boolean;
  voids?: boolean;
  batchDirty?: boolean;
}
interface TextInsertTextOptions {
  at?: Location;
  voids?: boolean;
}
interface TextTransforms {
  /**
   * Delete content in the editor.
   */
  delete: (editor: Editor$1, options?: TextDeleteOptions) => void;
  /**
   * Insert a fragment in the editor
   * at the specified location or (if not defined) the current selection or (if not defined) the end of the document.
   */
  insertFragment: (editor: Editor$1, fragment: Node$1[], options?: TextInsertFragmentOptions) => void;
  /**
   * Insert a string of text in the editor
   * at the specified location or (if not defined) the current selection or (if not defined) the end of the document.
   */
  insertText: (editor: Editor$1, text: string, options?: TextInsertTextOptions) => void;
}
declare const TextTransforms: TextTransforms;
/**
 * The `Editor` interface stores all the state of a Slate editor. It is extended
 * by plugins that wish to add their own helpers and implement new behaviors.
 */
interface BaseEditor {
  children: Descendant[];
  selection: Selection$1;
  operations: Operation[];
  marks: EditorMarks | null;
  apply: (operation: Operation) => void;
  createSpan: () => Text$1;
  getDirtyPaths: (operation: Operation) => Path$1[];
  getFragment: () => Descendant[];
  isElementReadOnly: (element: Element$1) => boolean;
  isSelectable: (element: Element$1) => boolean;
  markableVoid: (element: Element$1) => boolean;
  normalizeNode: (entry: NodeEntry, options?: {
    operation?: Operation;
    fallbackElement?: () => Element$1;
  }) => void;
  onChange: (options?: {
    operation?: Operation;
  }) => void;
  shouldNormalize: ({
    iteration,
    dirtyPaths,
    operation
  }: {
    iteration: number;
    initialDirtyPathsLength: number;
    dirtyPaths: Path$1[];
    operation?: Operation;
  }) => boolean;
  addMark: OmitFirstArg<typeof Editor$1.addMark>;
  collapse: OmitFirstArg<typeof Transforms.collapse>;
  delete: OmitFirstArg<typeof Transforms.delete>;
  deleteBackward: (unit: TextUnit) => void;
  deleteForward: (unit: TextUnit) => void;
  deleteFragment: OmitFirstArg<typeof Editor$1.deleteFragment>;
  deselect: OmitFirstArg<typeof Transforms.deselect>;
  insertBreak: OmitFirstArg<typeof Editor$1.insertBreak>;
  insertFragment: OmitFirstArg<typeof Transforms.insertFragment>;
  insertNode: OmitFirstArg<typeof Editor$1.insertNode>;
  insertNodes: OmitFirstArg<typeof Transforms.insertNodes>;
  insertSoftBreak: OmitFirstArg<typeof Editor$1.insertSoftBreak>;
  insertText: OmitFirstArg<typeof Transforms.insertText>;
  liftNodes: OmitFirstArg<typeof Transforms.liftNodes>;
  mergeNodes: OmitFirstArg<typeof Transforms.mergeNodes>;
  move: OmitFirstArg<typeof Transforms.move>;
  moveNodes: OmitFirstArg<typeof Transforms.moveNodes>;
  normalize: OmitFirstArg<typeof Editor$1.normalize>;
  removeMark: OmitFirstArg<typeof Editor$1.removeMark>;
  removeNodes: OmitFirstArg<typeof Transforms.removeNodes>;
  select: OmitFirstArg<typeof Transforms.select>;
  setNodes: <T extends Node$1>(props: Partial<T>, options?: {
    at?: Location;
    match?: NodeMatch<T>;
    mode?: MaximizeMode;
    hanging?: boolean;
    split?: boolean;
    voids?: boolean;
    compare?: PropsCompare;
    merge?: PropsMerge;
  }) => void;
  setNormalizing: OmitFirstArg<typeof Editor$1.setNormalizing>;
  setPoint: OmitFirstArg<typeof Transforms.setPoint>;
  setSelection: OmitFirstArg<typeof Transforms.setSelection>;
  splitNodes: OmitFirstArg<typeof Transforms.splitNodes>;
  unsetNodes: OmitFirstArg<typeof Transforms.unsetNodes>;
  unwrapNodes: OmitFirstArg<typeof Transforms.unwrapNodes>;
  withoutNormalizing: OmitFirstArg<typeof Editor$1.withoutNormalizing>;
  wrapNodes: OmitFirstArg<typeof Transforms.wrapNodes>;
  above: <T extends Ancestor>(options?: EditorAboveOptions<T>) => NodeEntry<T> | undefined;
  after: OmitFirstArg<typeof Editor$1.after>;
  before: OmitFirstArg<typeof Editor$1.before>;
  edges: OmitFirstArg<typeof Editor$1.edges>;
  elementReadOnly: OmitFirstArg<typeof Editor$1.elementReadOnly>;
  end: OmitFirstArg<typeof Editor$1.end>;
  first: OmitFirstArg<typeof Editor$1.first>;
  fragment: OmitFirstArg<typeof Editor$1.fragment>;
  getMarks: OmitFirstArg<typeof Editor$1.marks>;
  hasBlocks: OmitFirstArg<typeof Editor$1.hasBlocks>;
  hasInlines: OmitFirstArg<typeof Editor$1.hasInlines>;
  hasPath: OmitFirstArg<typeof Editor$1.hasPath>;
  hasTexts: OmitFirstArg<typeof Editor$1.hasTexts>;
  isBlock: OmitFirstArg<typeof Editor$1.isBlock>;
  isEdge: OmitFirstArg<typeof Editor$1.isEdge>;
  isEmpty: OmitFirstArg<typeof Editor$1.isEmpty>;
  isEnd: OmitFirstArg<typeof Editor$1.isEnd>;
  isInline: OmitFirstArg<typeof Editor$1.isInline>;
  isNormalizing: OmitFirstArg<typeof Editor$1.isNormalizing>;
  isStart: OmitFirstArg<typeof Editor$1.isStart>;
  isVoid: OmitFirstArg<typeof Editor$1.isVoid>;
  last: OmitFirstArg<typeof Editor$1.last>;
  leaf: OmitFirstArg<typeof Editor$1.leaf>;
  levels: <T extends Node$1>(options?: EditorLevelsOptions<T>) => Generator<NodeEntry<T>, void, undefined>;
  next: <T extends Descendant>(options?: EditorNextOptions<T>) => NodeEntry<T> | undefined;
  node: OmitFirstArg<typeof Editor$1.node>;
  nodes: <T extends Node$1>(options?: EditorNodesOptions<T>) => Generator<NodeEntry<T>, void, undefined>;
  parent: OmitFirstArg<typeof Editor$1.parent>;
  path: OmitFirstArg<typeof Editor$1.path>;
  pathRef: OmitFirstArg<typeof Editor$1.pathRef>;
  pathRefs: OmitFirstArg<typeof Editor$1.pathRefs>;
  point: OmitFirstArg<typeof Editor$1.point>;
  pointRef: OmitFirstArg<typeof Editor$1.pointRef>;
  pointRefs: OmitFirstArg<typeof Editor$1.pointRefs>;
  positions: OmitFirstArg<typeof Editor$1.positions>;
  previous: <T extends Node$1>(options?: EditorPreviousOptions<T>) => NodeEntry<T> | undefined;
  range: OmitFirstArg<typeof Editor$1.range>;
  rangeRef: OmitFirstArg<typeof Editor$1.rangeRef>;
  rangeRefs: OmitFirstArg<typeof Editor$1.rangeRefs>;
  start: OmitFirstArg<typeof Editor$1.start>;
  string: OmitFirstArg<typeof Editor$1.string>;
  unhangRange: OmitFirstArg<typeof Editor$1.unhangRange>;
  void: OmitFirstArg<typeof Editor$1.void>;
  shouldMergeNodesRemovePrevNode: OmitFirstArg<typeof Editor$1.shouldMergeNodesRemovePrevNode>;
}
type Editor$1 = ExtendedType<'Editor', BaseEditor>;
type BaseSelection = Range | null;
type Selection$1 = ExtendedType<'Selection', BaseSelection>;
type EditorMarks = Omit<Text$1, 'text'>;
interface EditorAboveOptions<T extends Ancestor> {
  at?: Location;
  match?: NodeMatch<T>;
  mode?: MaximizeMode;
  voids?: boolean;
}
interface EditorAfterOptions {
  distance?: number;
  unit?: TextUnitAdjustment;
  voids?: boolean;
}
interface EditorBeforeOptions {
  distance?: number;
  unit?: TextUnitAdjustment;
  voids?: boolean;
}
interface EditorDirectedDeletionOptions {
  unit?: TextUnit;
}
interface EditorElementReadOnlyOptions {
  at?: Location;
  mode?: MaximizeMode;
  voids?: boolean;
}
interface EditorFragmentDeletionOptions {
  direction?: TextDirection;
}
interface EditorIsEditorOptions {
  deep?: boolean;
}
interface EditorLeafOptions {
  depth?: number;
  edge?: LeafEdge;
}
interface EditorLevelsOptions<T extends Node$1> {
  at?: Location;
  match?: NodeMatch<T>;
  reverse?: boolean;
  voids?: boolean;
}
interface EditorNextOptions<T extends Descendant> {
  at?: Location;
  match?: NodeMatch<T>;
  mode?: SelectionMode;
  voids?: boolean;
}
interface EditorNodeOptions {
  depth?: number;
  edge?: LeafEdge;
}
interface EditorNodesOptions<T extends Node$1> {
  at?: Location | Span;
  match?: NodeMatch<T>;
  mode?: SelectionMode;
  universal?: boolean;
  reverse?: boolean;
  voids?: boolean;
  pass?: (entry: NodeEntry) => boolean;
}
interface EditorNormalizeOptions {
  force?: boolean;
  operation?: Operation;
}
interface EditorParentOptions {
  depth?: number;
  edge?: LeafEdge;
}
interface EditorPathOptions {
  depth?: number;
  edge?: LeafEdge;
}
interface EditorPathRefOptions {
  affinity?: TextDirection | null;
}
interface EditorPointOptions {
  edge?: LeafEdge;
}
interface EditorPointRefOptions {
  affinity?: TextDirection | null;
}
interface EditorPositionsOptions {
  at?: Location;
  unit?: TextUnitAdjustment;
  reverse?: boolean;
  voids?: boolean;
}
interface EditorPreviousOptions<T extends Node$1> {
  at?: Location;
  match?: NodeMatch<T>;
  mode?: SelectionMode;
  voids?: boolean;
}
interface EditorRangeRefOptions {
  affinity?: RangeDirection | null;
}
interface EditorStringOptions {
  voids?: boolean;
}
interface EditorUnhangRangeOptions {
  voids?: boolean;
}
interface EditorVoidOptions {
  at?: Location;
  mode?: MaximizeMode;
  voids?: boolean;
}
interface EditorInterface {
  /**
   * Get the ancestor above a location in the document.
   */
  above: <T extends Ancestor>(editor: Editor$1, options?: EditorAboveOptions<T>) => NodeEntry<T> | undefined;
  /**
   * Add a custom property to the leaf text nodes in the current selection.
   *
   * If the selection is currently collapsed, the marks will be added to the
   * `editor.marks` property instead, and applied when text is inserted next.
   */
  addMark: (editor: Editor$1, key: string, value: any) => void;
  /**
   * Get the point after a location.
   */
  after: (editor: Editor$1, at: Location, options?: EditorAfterOptions) => Point | undefined;
  /**
   * Get the point before a location.
   */
  before: (editor: Editor$1, at: Location, options?: EditorBeforeOptions) => Point | undefined;
  /**
   * Delete content in the editor backward from the current selection.
   */
  deleteBackward: (editor: Editor$1, options?: EditorDirectedDeletionOptions) => void;
  /**
   * Delete content in the editor forward from the current selection.
   */
  deleteForward: (editor: Editor$1, options?: EditorDirectedDeletionOptions) => void;
  /**
   * Delete the content in the current selection.
   */
  deleteFragment: (editor: Editor$1, options?: EditorFragmentDeletionOptions) => void;
  /**
   * Get the start and end points of a location.
   */
  edges: (editor: Editor$1, at: Location) => [Point, Point];
  /**
   * Match a read-only element in the current branch of the editor.
   */
  elementReadOnly: (editor: Editor$1, options?: EditorElementReadOnlyOptions) => NodeEntry<Element$1> | undefined;
  /**
   * Get the end point of a location.
   */
  end: (editor: Editor$1, at: Location) => Point;
  /**
   * Get the first node at a location.
   */
  first: (editor: Editor$1, at: Location) => NodeEntry;
  /**
   * Get the fragment at a location.
   */
  fragment: (editor: Editor$1, at: Location) => Descendant[];
  /**
   * Check if a node has block children.
   */
  hasBlocks: (editor: Editor$1, element: Element$1) => boolean;
  /**
   * Check if a node has inline and text children.
   */
  hasInlines: (editor: Editor$1, element: Element$1) => boolean;
  hasPath: (editor: Editor$1, path: Path$1) => boolean;
  /**
   * Check if a node has text children.
   */
  hasTexts: (editor: Editor$1, element: Element$1) => boolean;
  /**
   * Insert a block break at the current selection.
   *
   * If the selection is currently expanded, it will be deleted first.
   */
  insertBreak: (editor: Editor$1) => void;
  /**
   * Inserts a fragment
   * at the specified location or (if not defined) the current selection or (if not defined) the end of the document.
   */
  insertFragment: (editor: Editor$1, fragment: Node$1[], options?: TextInsertFragmentOptions) => void;
  /**
   * Atomically inserts `nodes`
   * at the specified location or (if not defined) the current selection or (if not defined) the end of the document.
   */
  insertNode: <T extends Node$1>(editor: Editor$1, node: Node$1, options?: NodeInsertNodesOptions<T>) => void;
  /**
   * Insert a soft break at the current selection.
   *
   * If the selection is currently expanded, it will be deleted first.
   */
  insertSoftBreak: (editor: Editor$1) => void;
  /**
   * Insert a string of text
   * at the specified location or (if not defined) the current selection or (if not defined) the end of the document.
   */
  insertText: (editor: Editor$1, text: string, options?: TextInsertTextOptions) => void;
  /**
   * Check if a value is a block `Element` object.
   */
  isBlock: (editor: Editor$1, value: Element$1) => boolean;
  /**
   * Check if a point is an edge of a location.
   */
  isEdge: (editor: Editor$1, point: Point, at: Location) => boolean;
  /**
   * Check if a value is an `Editor` object.
   */
  isEditor: (value: any, options?: EditorIsEditorOptions) => value is Editor$1;
  /**
   * Check if a value is a read-only `Element` object.
   */
  isElementReadOnly: (editor: Editor$1, element: Element$1) => boolean;
  /**
   * Check if an element is empty, accounting for void nodes.
   */
  isEmpty: (editor: Editor$1, element: Element$1) => boolean;
  /**
   * Check if a point is the end point of a location.
   */
  isEnd: (editor: Editor$1, point: Point, at: Location) => boolean;
  /**
   * Check if a value is an inline `Element` object.
   */
  isInline: (editor: Editor$1, value: Element$1) => boolean;
  /**
   * Check if the editor is currently normalizing after each operation.
   */
  isNormalizing: (editor: Editor$1) => boolean;
  /**
   * Check if a value is a selectable `Element` object.
   */
  isSelectable: (editor: Editor$1, element: Element$1) => boolean;
  /**
   * Check if a point is the start point of a location.
   */
  isStart: (editor: Editor$1, point: Point, at: Location) => boolean;
  /**
   * Check if a value is a void `Element` object.
   */
  isVoid: (editor: Editor$1, value: Element$1) => boolean;
  /**
   * Get the last node at a location.
   */
  last: (editor: Editor$1, at: Location) => NodeEntry;
  /**
   * Get the leaf text node at a location.
   */
  leaf: (editor: Editor$1, at: Location, options?: EditorLeafOptions) => NodeEntry<Text$1>;
  /**
   * Iterate through all of the levels at a location.
   */
  levels: <T extends Node$1>(editor: Editor$1, options?: EditorLevelsOptions<T>) => Generator<NodeEntry<T>, void, undefined>;
  /**
   * Get the marks that would be added to text at the current selection.
   */
  marks: (editor: Editor$1) => Omit<Text$1, 'text'> | null;
  /**
   * Get the matching node in the branch of the document after a location.
   */
  next: <T extends Descendant>(editor: Editor$1, options?: EditorNextOptions<T>) => NodeEntry<T> | undefined;
  /**
   * Get the node at a location.
   */
  node: (editor: Editor$1, at: Location, options?: EditorNodeOptions) => NodeEntry;
  /**
   * Iterate through all of the nodes in the Editor.
   */
  nodes: <T extends Node$1>(editor: Editor$1, options?: EditorNodesOptions<T>) => Generator<NodeEntry<T>, void, undefined>;
  /**
   * Normalize any dirty objects in the editor.
   */
  normalize: (editor: Editor$1, options?: EditorNormalizeOptions) => void;
  /**
   * Get the parent node of a location.
   */
  parent: (editor: Editor$1, at: Location, options?: EditorParentOptions) => NodeEntry<Ancestor>;
  /**
   * Get the path of a location.
   */
  path: (editor: Editor$1, at: Location, options?: EditorPathOptions) => Path$1;
  /**
   * Create a mutable ref for a `Path` object, which will stay in sync as new
   * operations are applied to the editor.
   */
  pathRef: (editor: Editor$1, path: Path$1, options?: EditorPathRefOptions) => PathRef;
  /**
   * Get the set of currently tracked path refs of the editor.
   */
  pathRefs: (editor: Editor$1) => Set<PathRef>;
  /**
   * Get the start or end point of a location.
   */
  point: (editor: Editor$1, at: Location, options?: EditorPointOptions) => Point;
  /**
   * Create a mutable ref for a `Point` object, which will stay in sync as new
   * operations are applied to the editor.
   */
  pointRef: (editor: Editor$1, point: Point, options?: EditorPointRefOptions) => PointRef;
  /**
   * Get the set of currently tracked point refs of the editor.
   */
  pointRefs: (editor: Editor$1) => Set<PointRef>;
  /**
   * Return all the positions in `at` range where a `Point` can be placed.
   *
   * By default, moves forward by individual offsets at a time, but
   * the `unit` option can be used to to move by character, word, line, or block.
   *
   * The `reverse` option can be used to change iteration direction.
   *
   * Note: By default void nodes are treated as a single point and iteration
   * will not happen inside their content unless you pass in true for the
   * `voids` option, then iteration will occur.
   */
  positions: (editor: Editor$1, options?: EditorPositionsOptions) => Generator<Point, void, undefined>;
  /**
   * Get the matching node in the branch of the document before a location.
   */
  previous: <T extends Node$1>(editor: Editor$1, options?: EditorPreviousOptions<T>) => NodeEntry<T> | undefined;
  /**
   * Get a range of a location.
   */
  range: (editor: Editor$1, at: Location, to?: Location) => Range;
  /**
   * Create a mutable ref for a `Range` object, which will stay in sync as new
   * operations are applied to the editor.
   */
  rangeRef: (editor: Editor$1, range: Range, options?: EditorRangeRefOptions) => RangeRef;
  /**
   * Get the set of currently tracked range refs of the editor.
   */
  rangeRefs: (editor: Editor$1) => Set<RangeRef>;
  /**
   * Remove a custom property from all of the leaf text nodes in the current
   * selection.
   *
   * If the selection is currently collapsed, the removal will be stored on
   * `editor.marks` and applied to the text inserted next.
   */
  removeMark: (editor: Editor$1, key: string) => void;
  /**
   * Manually set if the editor should currently be normalizing.
   *
   * Note: Using this incorrectly can leave the editor in an invalid state.
   *
   */
  setNormalizing: (editor: Editor$1, isNormalizing: boolean) => void;
  /**
   * Get the start point of a location.
   */
  start: (editor: Editor$1, at: Location) => Point;
  /**
   * Get the text string content of a location.
   *
   * Note: by default the text of void nodes is considered to be an empty
   * string, regardless of content, unless you pass in true for the voids option
   */
  string: (editor: Editor$1, at: Location, options?: EditorStringOptions) => string;
  /**
   * Convert a range into a non-hanging one.
   */
  unhangRange: (editor: Editor$1, range: Range, options?: EditorUnhangRangeOptions) => Range;
  /**
   * Match a void node in the current branch of the editor.
   */
  void: (editor: Editor$1, options?: EditorVoidOptions) => NodeEntry<Element$1> | undefined;
  /**
   * Call a function, deferring normalization until after it completes.
   */
  withoutNormalizing: (editor: Editor$1, fn: () => void) => void;
  /**
   *  Call a function, Determine whether or not remove the previous node when merge.
   */
  shouldMergeNodesRemovePrevNode: (editor: Editor$1, prevNodeEntry: NodeEntry, curNodeEntry: NodeEntry) => boolean;
}
declare const Editor$1: EditorInterface;
/**
 * A helper type for narrowing matched nodes with a predicate.
 */
type NodeMatch<T extends Node$1> = ((node: Node$1, path: Path$1) => node is T) | ((node: Node$1, path: Path$1) => boolean);
type PropsCompare = (prop: Partial<Node$1>, node: Partial<Node$1>) => boolean;
type PropsMerge = (prop: Partial<Node$1>, node: Partial<Node$1>) => object;
/**
 * `Element` objects are a type of node in a Slate document that contain other
 * element nodes or text nodes. They can be either "blocks" or "inlines"
 * depending on the Slate editor's configuration.
 */
interface BaseElement {
  children: Descendant[];
}
type Element$1 = ExtendedType<'Element', BaseElement>;
interface ElementIsElementOptions {
  deep?: boolean;
}
interface ElementInterface {
  /**
   * Check if a value implements the 'Ancestor' interface.
   */
  isAncestor: (value: any, options?: ElementIsElementOptions) => value is Ancestor;
  /**
   * Check if a value implements the `Element` interface.
   */
  isElement: (value: any, options?: ElementIsElementOptions) => value is Element$1;
  /**
   * Check if a value is an array of `Element` objects.
   */
  isElementList: (value: any, options?: ElementIsElementOptions) => value is Element$1[];
  /**
   * Check if a set of props is a partial of Element.
   */
  isElementProps: (props: any) => props is Partial<Element$1>;
  /**
   * Check if a value implements the `Element` interface and has elementKey with selected value.
   * Default it check to `type` key value
   */
  isElementType: <T extends Element$1>(value: any, elementVal: string, elementKey?: string) => value is T;
  /**
   * Check if an element matches set of properties.
   *
   * Note: this checks custom properties, and it does not ensure that any
   * children are equivalent.
   */
  matches: (element: Element$1, props: Partial<Element$1>) => boolean;
}
declare const Element$1: ElementInterface;
/**
 * `ElementEntry` objects refer to an `Element` and the `Path` where it can be
 * found inside a root node.
 */
type ElementEntry = [Element$1, Path$1];
/**
 * The `Location` interface is a union of the ways to refer to a specific
 * location in a Slate document: paths, points or ranges.
 *
 * Methods will often accept a `Location` instead of requiring only a `Path`,
 * `Point` or `Range`. This eliminates the need for developers to manage
 * converting between the different interfaces in their own code base.
 */
type Location = Path$1 | Point | Range;
interface LocationInterface {
  /**
   * Check if a value implements the `Location` interface.
   */
  isLocation: (value: any) => value is Location;
}
declare const Location: LocationInterface;
/**
 * The `Span` interface is a low-level way to refer to locations in nodes
 * without using `Point` which requires leaf text nodes to be present.
 */
type Span = [Path$1, Path$1];
interface SpanInterface {
  /**
   * Check if a value implements the `Span` interface.
   */
  isSpan: (value: any) => value is Span;
}
declare const Span: SpanInterface;
type Node$1 = Editor$1 | Element$1 | Text$1;
interface NodeAncestorsOptions {
  reverse?: boolean;
}
interface NodeChildrenOptions {
  reverse?: boolean;
}
interface NodeDescendantsOptions {
  from?: Path$1;
  to?: Path$1;
  reverse?: boolean;
  pass?: (node: NodeEntry) => boolean;
}
interface NodeElementsOptions {
  from?: Path$1;
  to?: Path$1;
  reverse?: boolean;
  pass?: (node: NodeEntry) => boolean;
}
interface NodeIsNodeOptions {
  deep?: boolean;
}
interface NodeLevelsOptions {
  reverse?: boolean;
}
interface NodeNodesOptions {
  from?: Path$1;
  to?: Path$1;
  reverse?: boolean;
  pass?: (entry: NodeEntry) => boolean;
}
interface NodeTextsOptions {
  from?: Path$1;
  to?: Path$1;
  reverse?: boolean;
  pass?: (node: NodeEntry) => boolean;
}
interface NodeInterface {
  /**
   * Get the node at a specific path, asserting that it's an ancestor node.
   */
  ancestor: (root: Node$1, path: Path$1) => Ancestor;
  /**
   * Return a generator of all the ancestor nodes above a specific path.
   *
   * By default the order is top-down, from highest to lowest ancestor in
   * the tree, but you can pass the `reverse: true` option to go bottom-up.
   */
  ancestors: (root: Node$1, path: Path$1, options?: NodeAncestorsOptions) => Generator<NodeEntry<Ancestor>, void, undefined>;
  /**
   * Get the child of a node at a specific index.
   */
  child: (root: Node$1, index: number) => Descendant;
  /**
   * Iterate over the children of a node at a specific path.
   */
  children: (root: Node$1, path: Path$1, options?: NodeChildrenOptions) => Generator<NodeEntry<Descendant>, void, undefined>;
  /**
   * Get an entry for the common ancesetor node of two paths.
   */
  common: (root: Node$1, path: Path$1, another: Path$1) => NodeEntry;
  /**
   * Get the node at a specific path, asserting that it's a descendant node.
   */
  descendant: (root: Node$1, path: Path$1) => Descendant;
  /**
   * Return a generator of all the descendant node entries inside a root node.
   */
  descendants: (root: Node$1, options?: NodeDescendantsOptions) => Generator<NodeEntry<Descendant>, void, undefined>;
  /**
   * Return a generator of all the element nodes inside a root node. Each iteration
   * will return an `ElementEntry` tuple consisting of `[Element, Path]`. If the
   * root node is an element it will be included in the iteration as well.
   */
  elements: (root: Node$1, options?: NodeElementsOptions) => Generator<ElementEntry, void, undefined>;
  /**
   * Extract props from a Node.
   */
  extractProps: (node: Node$1) => NodeProps;
  /**
   * Get the first leaf node entry in a root node from a path.
   */
  first: (root: Node$1, path: Path$1) => NodeEntry;
  /**
   * Get the sliced fragment represented by a range inside a root node.
   */
  fragment: <T extends Ancestor = Editor$1>(root: T, range: Range) => T['children'];
  /**
   * Get the descendant node referred to by a specific path. If the path is an
   * empty array, it refers to the root node itself.
   */
  get: (root: Node$1, path: Path$1) => Node$1;
  /**
   * Similar to get, but returns undefined if the node does not exist.
   */
  getIf: (root: Node$1, path: Path$1) => Node$1 | undefined;
  /**
   * Check if a descendant node exists at a specific path.
   */
  has: (root: Node$1, path: Path$1) => boolean;
  /**
   * Check if a value implements the `Node` interface.
   */
  isNode: (value: any, options?: NodeIsNodeOptions) => value is Node$1;
  /**
   * Check if a value is a list of `Node` objects.
   */
  isNodeList: (value: any, options?: NodeIsNodeOptions) => value is Node$1[];
  /**
   * Get the last leaf node entry in a root node from a path.
   */
  last: (root: Node$1, path: Path$1) => NodeEntry;
  /**
   * Get the node at a specific path, ensuring it's a leaf text node.
   */
  leaf: (root: Node$1, path: Path$1) => Text$1;
  /**
   * Return a generator of the in a branch of the tree, from a specific path.
   *
   * By default the order is top-down, from highest to lowest node in the tree,
   * but you can pass the `reverse: true` option to go bottom-up.
   */
  levels: (root: Node$1, path: Path$1, options?: NodeLevelsOptions) => Generator<NodeEntry, void, undefined>;
  /**
   * Check if a node matches a set of props.
   */
  matches: (node: Node$1, props: Partial<Node$1>) => boolean;
  /**
   * Return a generator of all the node entries of a root node. Each entry is
   * returned as a `[Node, Path]` tuple, with the path referring to the node's
   * position inside the root node.
   */
  nodes: (root: Node$1, options?: NodeNodesOptions) => Generator<NodeEntry, void, undefined>;
  /**
   * Get the parent of a node at a specific path.
   */
  parent: (root: Node$1, path: Path$1) => Ancestor;
  /**
   * Get the concatenated text string of a node's content.
   *
   * Note that this will not include spaces or line breaks between block nodes.
   * It is not a user-facing string, but a string for performing offset-related
   * computations for a node.
   */
  string: (node: Node$1) => string;
  /**
   * Return a generator of all leaf text nodes in a root node.
   */
  texts: (root: Node$1, options?: NodeTextsOptions) => Generator<NodeEntry<Text$1>, void, undefined>;
}
declare const Node$1: NodeInterface;
/**
 * The `Descendant` union type represents nodes that are descendants in the
 * tree. It is returned as a convenience in certain cases to narrow a value
 * further than the more generic `Node` union.
 */
type Descendant = Element$1 | Text$1;
/**
 * The `Ancestor` union type represents nodes that are ancestors in the tree.
 * It is returned as a convenience in certain cases to narrow a value further
 * than the more generic `Node` union.
 */
type Ancestor = Editor$1 | Element$1;
/**
 * `NodeEntry` objects are returned when iterating over the nodes in a Slate
 * document tree. They consist of the node and its `Path` relative to the root
 * node in the document.
 */
type NodeEntry<T extends Node$1 = Node$1> = [T, Path$1];
/**
 * Convenience type for returning the props of a node.
 */
type NodeProps = Omit<Editor$1, 'children'> | Omit<Element$1, 'children'> | Omit<Text$1, 'text'>;
type BaseInsertNodeOperation = {
  type: 'insert_node';
  path: Path$1;
  node: Node$1;
};
type InsertNodeOperation = ExtendedType<'InsertNodeOperation', BaseInsertNodeOperation>;
type BaseInsertTextOperation = {
  type: 'insert_text';
  path: Path$1;
  offset: number;
  text: string;
};
type InsertTextOperation = ExtendedType<'InsertTextOperation', BaseInsertTextOperation>;
type BaseMergeNodeOperation = {
  type: 'merge_node';
  path: Path$1;
  position: number;
  properties: Partial<Node$1>;
};
type MergeNodeOperation = ExtendedType<'MergeNodeOperation', BaseMergeNodeOperation>;
type BaseMoveNodeOperation = {
  type: 'move_node';
  path: Path$1;
  newPath: Path$1;
};
type MoveNodeOperation = ExtendedType<'MoveNodeOperation', BaseMoveNodeOperation>;
type BaseRemoveNodeOperation = {
  type: 'remove_node';
  path: Path$1;
  node: Node$1;
};
type RemoveNodeOperation = ExtendedType<'RemoveNodeOperation', BaseRemoveNodeOperation>;
type BaseRemoveTextOperation = {
  type: 'remove_text';
  path: Path$1;
  offset: number;
  text: string;
};
type RemoveTextOperation = ExtendedType<'RemoveTextOperation', BaseRemoveTextOperation>;
type BaseSetNodeOperation = {
  type: 'set_node';
  path: Path$1;
  properties: Partial<Node$1>;
  newProperties: Partial<Node$1>;
};
type SetNodeOperation = ExtendedType<'SetNodeOperation', BaseSetNodeOperation>;
type BaseSetSelectionOperation = {
  type: 'set_selection';
  properties: null;
  newProperties: Range;
} | {
  type: 'set_selection';
  properties: Partial<Range>;
  newProperties: Partial<Range>;
} | {
  type: 'set_selection';
  properties: Range;
  newProperties: null;
};
type SetSelectionOperation = ExtendedType<'SetSelectionOperation', BaseSetSelectionOperation>;
type BaseSplitNodeOperation = {
  type: 'split_node';
  path: Path$1;
  position: number;
  properties: Partial<Node$1>;
};
type SplitNodeOperation = ExtendedType<'SplitNodeOperation', BaseSplitNodeOperation>;
type NodeOperation = InsertNodeOperation | MergeNodeOperation | MoveNodeOperation | RemoveNodeOperation | SetNodeOperation | SplitNodeOperation;
type SelectionOperation = SetSelectionOperation;
type TextOperation = InsertTextOperation | RemoveTextOperation;
/**
 * `Operation` objects define the low-level instructions that Slate editors use
 * to apply changes to their internal state. Representing all changes as
 * operations is what allows Slate editors to easily implement history,
 * collaboration, and other features.
 */
type BaseOperation = NodeOperation | SelectionOperation | TextOperation;
type Operation = ExtendedType<'Operation', BaseOperation>;
interface OperationInterface {
  /**
   * Check if a value is a `NodeOperation` object.
   */
  isNodeOperation: (value: any) => value is NodeOperation;
  /**
   * Check if a value is an `Operation` object.
   */
  isOperation: (value: any) => value is Operation;
  /**
   * Check if a value is a list of `Operation` objects.
   */
  isOperationList: (value: any) => value is Operation[];
  /**
   * Check if a value is a `SelectionOperation` object.
   */
  isSelectionOperation: (value: any) => value is SelectionOperation;
  /**
   * Check if a value is a `TextOperation` object.
   */
  isTextOperation: (value: any) => value is TextOperation;
  /**
   * Invert an operation, returning a new operation that will exactly undo the
   * original when applied.
   */
  inverse: (op: Operation) => Operation;
}
declare const Operation: OperationInterface;
/**
 * `PathRef` objects keep a specific path in a document synced over time as new
 * operations are applied to the editor. You can access their `current` property
 * at any time for the up-to-date path value.
 */
interface PathRef {
  current: Path$1 | null;
  affinity: 'forward' | 'backward' | null;
  unref(): Path$1 | null;
}
interface PathRefInterface {
  /**
   * Transform the path ref's current value by an operation.
   */
  transform: (ref: PathRef, op: Operation) => void;
}
declare const PathRef: PathRefInterface;
/**
 * `Path` arrays are a list of indexes that describe a node's exact position in
 * a Slate node tree. Although they are usually relative to the root `Editor`
 * object, they can be relative to any `Node` object.
 */
type Path$1 = number[];
interface PathAncestorsOptions {
  reverse?: boolean;
}
interface PathLevelsOptions {
  reverse?: boolean;
}
interface PathTransformOptions {
  affinity?: TextDirection | null;
}
interface PathInterface {
  /**
   * Get a list of ancestor paths for a given path.
   *
   * The paths are sorted from shallowest to deepest ancestor. However, if the
   * `reverse: true` option is passed, they are reversed.
   */
  ancestors: (path: Path$1, options?: PathAncestorsOptions) => Path$1[];
  /**
   * Get the common ancestor path of two paths.
   */
  common: (path: Path$1, another: Path$1) => Path$1;
  /**
   * Compare a path to another, returning an integer indicating whether the path
   * was before, at, or after the other.
   *
   * Note: Two paths of unequal length can still receive a `0` result if one is
   * directly above or below the other. If you want exact matching, use
   * [[Path.equals]] instead.
   */
  compare: (path: Path$1, another: Path$1) => -1 | 0 | 1;
  /**
   * Check if a path ends after one of the indexes in another.
   */
  endsAfter: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path ends at one of the indexes in another.
   */
  endsAt: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path ends before one of the indexes in another.
   */
  endsBefore: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path is exactly equal to another.
   */
  equals: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if the path of previous sibling node exists
   */
  hasPrevious: (path: Path$1) => boolean;
  /**
   * Check if a path is after another.
   */
  isAfter: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path is an ancestor of another.
   */
  isAncestor: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path is before another.
   */
  isBefore: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path is a child of another.
   */
  isChild: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path is equal to or an ancestor of another.
   */
  isCommon: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path is a descendant of another.
   */
  isDescendant: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check if a path is the parent of another.
   */
  isParent: (path: Path$1, another: Path$1) => boolean;
  /**
   * Check is a value implements the `Path` interface.
   */
  isPath: (value: any) => value is Path$1;
  /**
   * Check if a path is a sibling of another.
   */
  isSibling: (path: Path$1, another: Path$1) => boolean;
  /**
   * Get a list of paths at every level down to a path. Note: this is the same
   * as `Path.ancestors`, but including the path itself.
   *
   * The paths are sorted from shallowest to deepest. However, if the `reverse:
   * true` option is passed, they are reversed.
   */
  levels: (path: Path$1, options?: PathLevelsOptions) => Path$1[];
  /**
   * Given a path, get the path to the next sibling node.
   */
  next: (path: Path$1) => Path$1;
  /**
   * Returns whether this operation can affect paths or not. Used as an
   * optimization when updating dirty paths during normalization
   *
   * NOTE: This *must* be kept in sync with the implementation of 'transform'
   * below
   */
  operationCanTransformPath: (operation: Operation) => operation is InsertNodeOperation | RemoveNodeOperation | MergeNodeOperation | SplitNodeOperation | MoveNodeOperation;
  /**
   * Given a path, return a new path referring to the parent node above it.
   */
  parent: (path: Path$1) => Path$1;
  /**
   * Given a path, get the path to the previous sibling node.
   */
  previous: (path: Path$1) => Path$1;
  /**
   * Get a path relative to an ancestor.
   */
  relative: (path: Path$1, ancestor: Path$1) => Path$1;
  /**
   * Transform a path by an operation.
   */
  transform: (path: Path$1, operation: Operation, options?: PathTransformOptions) => Path$1 | null;
}
declare const Path$1: PathInterface;
/**
 * `PointRef` objects keep a specific point in a document synced over time as new
 * operations are applied to the editor. You can access their `current` property
 * at any time for the up-to-date point value.
 */
interface PointRef {
  current: Point | null;
  affinity: TextDirection | null;
  unref(): Point | null;
}
interface PointRefInterface {
  /**
   * Transform the point ref's current value by an operation.
   */
  transform: (ref: PointRef, op: Operation) => void;
}
declare const PointRef: PointRefInterface;
/**
 * `Point` objects refer to a specific location in a text node in a Slate
 * document. Its path refers to the location of the node in the tree, and its
 * offset refers to the distance into the node's string of text. Points can
 * only refer to `Text` nodes.
 */
interface BasePoint {
  path: Path$1;
  offset: number;
}
type Point = ExtendedType<'Point', BasePoint>;
interface PointTransformOptions {
  affinity?: TextDirection | null;
}
interface PointInterface {
  /**
   * Compare a point to another, returning an integer indicating whether the
   * point was before, at, or after the other.
   */
  compare: (point: Point, another: Point) => -1 | 0 | 1;
  /**
   * Check if a point is after another.
   */
  isAfter: (point: Point, another: Point) => boolean;
  /**
   * Check if a point is before another.
   */
  isBefore: (point: Point, another: Point) => boolean;
  /**
   * Check if a point is exactly equal to another.
   */
  equals: (point: Point, another: Point) => boolean;
  /**
   * Check if a value implements the `Point` interface.
   */
  isPoint: (value: any) => value is Point;
  /**
   * Transform a point by an operation.
   */
  transform: (point: Point, op: Operation, options?: PointTransformOptions) => Point | null;
}
declare const Point: PointInterface;
/**
 * `PointEntry` objects are returned when iterating over `Point` objects that
 * belong to a range.
 */
type PointEntry = [Point, 'anchor' | 'focus'];
/**
 * `RangeRef` objects keep a specific range in a document synced over time as new
 * operations are applied to the editor. You can access their `current` property
 * at any time for the up-to-date range value.
 */
interface RangeRef {
  current: Range | null;
  affinity: 'forward' | 'backward' | 'outward' | 'inward' | null;
  unref(): Range | null;
}
interface RangeRefInterface {
  /**
   * Transform the range ref's current value by an operation.
   */
  transform: (ref: RangeRef, op: Operation) => void;
}
declare const RangeRef: RangeRefInterface;
/**
 * `Range` objects are a set of points that refer to a specific span of a Slate
 * document. They can define a span inside a single node or a can span across
 * multiple nodes.
 */
interface BaseRange {
  anchor: Point;
  focus: Point;
}
type Range = ExtendedType<'Range', BaseRange>;
interface RangeEdgesOptions {
  reverse?: boolean;
}
interface RangeTransformOptions {
  affinity?: RangeDirection | null;
}
interface RangeInterface {
  /**
   * Get the start and end points of a range, in the order in which they appear
   * in the document.
   */
  edges: (range: Range, options?: RangeEdgesOptions) => [Point, Point];
  /**
   * Get the end point of a range.
   */
  end: (range: Range) => Point;
  /**
   * Check if a range is exactly equal to another.
   */
  equals: (range: Range, another: Range) => boolean;
  /**
   * Check if a range includes a path, a point or part of another range.
   */
  includes: (range: Range, target: Path$1 | Point | Range) => boolean;
  /**
   * Check if a range includes another range.
   */
  surrounds: (range: Range, target: Range) => boolean;
  /**
   * Get the intersection of a range with another.
   */
  intersection: (range: Range, another: Range) => Range | null;
  /**
   * Check if a range is backward, meaning that its anchor point appears in the
   * document _after_ its focus point.
   */
  isBackward: (range: Range) => boolean;
  /**
   * Check if a range is collapsed, meaning that both its anchor and focus
   * points refer to the exact same position in the document.
   */
  isCollapsed: (range: Range) => boolean;
  /**
   * Check if a range is expanded.
   *
   * This is the opposite of [[Range.isCollapsed]] and is provided for legibility.
   */
  isExpanded: (range: Range) => boolean;
  /**
   * Check if a range is forward.
   *
   * This is the opposite of [[Range.isBackward]] and is provided for legibility.
   */
  isForward: (range: Range) => boolean;
  /**
   * Check if a value implements the [[Range]] interface.
   */
  isRange: (value: any) => value is Range;
  /**
   * Iterate through all of the point entries in a range.
   */
  points: (range: Range) => Generator<PointEntry, void, undefined>;
  /**
   * Get the start point of a range.
   */
  start: (range: Range) => Point;
  /**
   * Transform a range by an operation.
   */
  transform: (range: Range, op: Operation, options?: RangeTransformOptions) => Range | null;
}
declare const Range: RangeInterface;
/**
 * Extendable Custom Types Interface
 */
type ExtendableTypes = 'Editor' | 'Element' | 'Text' | 'Selection' | 'Range' | 'Point' | 'Operation' | 'InsertNodeOperation' | 'InsertTextOperation' | 'MergeNodeOperation' | 'MoveNodeOperation' | 'RemoveNodeOperation' | 'RemoveTextOperation' | 'SetNodeOperation' | 'SetSelectionOperation' | 'SplitNodeOperation';
interface CustomTypes {
  [key: string]: unknown;
}
type ExtendedType<K$1 extends ExtendableTypes, B> = unknown extends CustomTypes[K$1] ? B : CustomTypes[K$1];
/**
 * `Text` objects represent the nodes that contain the actual text content of a
 * Slate document along with any formatting properties. They are always leaf
 * nodes in the document tree as they cannot contain any children.
 */
interface BaseText {
  text: string;
}
type Text$1 = ExtendedType<'Text', BaseText>;
interface LeafPosition {
  start: number;
  end: number;
  isFirst?: true;
  isLast?: true;
}
interface TextEqualsOptions {
  loose?: boolean;
}
type DecoratedRange$1 = Range & {
  /**
   * Customize how another decoration is merged into a text node. If not specified, `Object.assign` would be used.
   * It is useful for overlapping decorations with the same key but different values.
   */
  merge?: (leaf: Text$1, decoration: object) => void;
};
interface TextInterface {
  /**
   * Check if two text nodes are equal.
   *
   * When loose is set, the text is not compared. This is
   * used to check whether sibling text nodes can be merged.
   */
  equals: (text: Text$1, another: Text$1, options?: TextEqualsOptions) => boolean;
  /**
   * Check if a value implements the `Text` interface.
   */
  isText: (value: any) => value is Text$1;
  /**
   * Check if a value is a list of `Text` objects.
   */
  isTextList: (value: any) => value is Text$1[];
  /**
   * Check if some props are a partial of Text.
   */
  isTextProps: (props: any) => props is Partial<Text$1>;
  /**
   * Check if an text matches set of properties.
   *
   * Note: this is for matching custom properties, and it does not ensure that
   * the `text` property are two nodes equal.
   */
  matches: (text: Text$1, props: Partial<Text$1>) => boolean;
  /**
   * Get the leaves for a text node given decorations.
   */
  decorations: (node: Text$1, decorations: DecoratedRange$1[]) => {
    leaf: Text$1;
    position?: LeafPosition;
  }[];
}
declare const Text$1: TextInterface;
interface GeneralTransforms {
  /**
   * Transform the editor by an operation.
   */
  transform: (editor: Editor$1, op: Operation) => void;
}
declare const GeneralTransforms: GeneralTransforms;
interface SelectionCollapseOptions {
  edge?: SelectionEdge;
}
interface SelectionMoveOptions {
  distance?: number;
  unit?: MoveUnit;
  reverse?: boolean;
  edge?: SelectionEdge;
}
interface SelectionSetPointOptions {
  edge?: SelectionEdge;
}
interface SelectionTransforms {
  /**
   * Collapse the selection.
   */
  collapse: (editor: Editor$1, options?: SelectionCollapseOptions) => void;
  /**
   * Unset the selection.
   */
  deselect: (editor: Editor$1) => void;
  /**
   * Move the selection's point forward or backward.
   */
  move: (editor: Editor$1, options?: SelectionMoveOptions) => void;
  /**
   * Set the selection to a new value.
   */
  select: (editor: Editor$1, target: Location) => void;
  /**
   * Set new properties on one of the selection's points.
   */
  setPoint: (editor: Editor$1, props: Partial<Point>, options?: SelectionSetPointOptions) => void;
  /**
   * Set new properties on the selection.
   */
  setSelection: (editor: Editor$1, props: Partial<Range>) => void;
}
declare const SelectionTransforms: SelectionTransforms;
declare const Transforms: GeneralTransforms & NodeTransforms & SelectionTransforms & TextTransforms;
/**
 * @public
 */
type EditorSchema = Schema;
type DecoratedRange = BaseRange & {
  rangeDecoration: RangeDecoration;
};
type StringDiff = {
  start: number;
  end: number;
  text: string;
};
type TextDiff = {
  id: number;
  path: Path$1;
  diff: StringDiff;
};
/**
 * Types.
 */
type DOMNode = globalThis.Node;
type DOMRange = globalThis.Range;
type DOMSelection = globalThis.Selection;
type DOMStaticRange = globalThis.StaticRange;
declare global {
  interface Window {
    Selection: (typeof Selection)['constructor'];
    DataTransfer: (typeof DataTransfer)['constructor'];
    Node: (typeof Node)['constructor'];
  }
}
type DOMPoint = [Node, number];
/**
 * An auto-incrementing identifier for keys.
 */
/**
 * A class that keeps track of a key string. We use a full class here because we
 * want to be able to use them as keys in `WeakMap` objects.
 */
declare class Key {
  id: string;
  constructor();
}
/**
 * A DOM-specific version of the `Editor` interface.
 */
interface DOMEditor extends BaseEditor {
  hasEditableTarget: (editor: Editor$1, target: EventTarget | null) => target is DOMNode;
  hasRange: (editor: Editor$1, range: Range) => boolean;
  hasSelectableTarget: (editor: Editor$1, target: EventTarget | null) => boolean;
  hasTarget: (editor: Editor$1, target: EventTarget | null) => target is DOMNode;
  insertData: (data: DataTransfer) => void;
  insertFragmentData: (data: DataTransfer) => boolean;
  insertTextData: (data: DataTransfer) => boolean;
  isTargetInsideNonReadonlyVoid: (editor: Editor$1, target: EventTarget | null) => boolean;
  setFragmentData: (data: DataTransfer, originEvent?: 'drag' | 'copy' | 'cut') => void;
}
interface DOMEditorInterface {
  /**
   * Experimental and android specific: Get pending diffs
   */
  androidPendingDiffs: (editor: Editor$1) => TextDiff[] | undefined;
  /**
   * Experimental and android specific: Flush all pending diffs and cancel composition at the next possible time.
   */
  androidScheduleFlush: (editor: Editor$1) => void;
  /**
   * Blur the editor.
   */
  blur: (editor: Editor$1) => void;
  /**
   * Deselect the editor.
   */
  deselect: (editor: Editor$1) => void;
  /**
   * Find the DOM node that implements DocumentOrShadowRoot for the editor.
   */
  findDocumentOrShadowRoot: (editor: Editor$1) => Document | ShadowRoot;
  /**
   * Get the target range from a DOM `event`.
   */
  findEventRange: (editor: Editor$1, event: any) => Range;
  /**
   * Find a key for a Slate node.
   */
  findKey: (editor: Editor$1, node: Node$1) => Key;
  /**
   * Find the path of Slate node.
   */
  findPath: (editor: Editor$1, node: Node$1) => Path$1;
  /**
   * Focus the editor.
   */
  focus: (editor: Editor$1, options?: {
    retries: number;
  }) => void;
  /**
   * Return the host window of the current editor.
   */
  getWindow: (editor: Editor$1) => Window;
  /**
   * Check if a DOM node is within the editor.
   */
  hasDOMNode: (editor: Editor$1, target: DOMNode, options?: {
    editable?: boolean;
  }) => boolean;
  /**
   * Check if the target is editable and in the editor.
   */
  hasEditableTarget: (editor: Editor$1, target: EventTarget | null) => target is DOMNode;
  /**
   *
   */
  hasRange: (editor: Editor$1, range: Range) => boolean;
  /**
   * Check if the target can be selectable
   */
  hasSelectableTarget: (editor: Editor$1, target: EventTarget | null) => boolean;
  /**
   * Check if the target is in the editor.
   */
  hasTarget: (editor: Editor$1, target: EventTarget | null) => target is DOMNode;
  /**
   * Insert data from a `DataTransfer` into the editor.
   */
  insertData: (editor: Editor$1, data: DataTransfer) => void;
  /**
   * Insert fragment data from a `DataTransfer` into the editor.
   */
  insertFragmentData: (editor: Editor$1, data: DataTransfer) => boolean;
  /**
   * Insert text data from a `DataTransfer` into the editor.
   */
  insertTextData: (editor: Editor$1, data: DataTransfer) => boolean;
  /**
   * Check if the user is currently composing inside the editor.
   */
  isComposing: (editor: Editor$1) => boolean;
  /**
   * Check if the editor is focused.
   */
  isFocused: (editor: Editor$1) => boolean;
  /**
   * Check if the editor is in read-only mode.
   */
  isReadOnly: (editor: Editor$1) => boolean;
  /**
   * Check if the target is inside void and in an non-readonly editor.
   */
  isTargetInsideNonReadonlyVoid: (editor: Editor$1, target: EventTarget | null) => boolean;
  /**
   * Sets data from the currently selected fragment on a `DataTransfer`.
   */
  setFragmentData: (editor: Editor$1, data: DataTransfer, originEvent?: 'drag' | 'copy' | 'cut') => void;
  /**
   * Find the native DOM element from a Slate node.
   */
  toDOMNode: (editor: Editor$1, node: Node$1) => HTMLElement;
  /**
   * Find a native DOM selection point from a Slate point.
   */
  toDOMPoint: (editor: Editor$1, point: Point) => DOMPoint;
  /**
   * Find a native DOM range from a Slate `range`.
   *
   * Notice: the returned range will always be ordinal regardless of the direction of Slate `range` due to DOM API limit.
   *
   * there is no way to create a reverse DOM Range using Range.setStart/setEnd
   * according to https://dom.spec.whatwg.org/#concept-range-bp-set.
   */
  toDOMRange: (editor: Editor$1, range: Range) => DOMRange;
  /**
   * Find a Slate node from a native DOM `element`.
   */
  toSlateNode: (editor: Editor$1, domNode: DOMNode) => Node$1;
  /**
   * Find a Slate point from a DOM selection's `domNode` and `domOffset`.
   */
  toSlatePoint: <T extends boolean>(editor: Editor$1, domPoint: DOMPoint, options: {
    exactMatch: boolean;
    suppressThrow: T;
    /**
     * The direction to search for Slate leaf nodes if `domPoint` is
     * non-editable and non-void.
     */
    searchDirection?: 'forward' | 'backward';
  }) => T extends true ? Point | null : Point;
  /**
   * Find a Slate range from a DOM range or selection.
   */
  toSlateRange: <T extends boolean>(editor: Editor$1, domRange: DOMRange | DOMStaticRange | DOMSelection, options: {
    exactMatch: boolean;
    suppressThrow: T;
  }) => T extends true ? Range | null : Range;
}
declare const DOMEditor: DOMEditorInterface;
/**
 * A React and DOM-specific version of the `Editor` interface.
 */
interface ReactEditor extends DOMEditor {
  /**
   * Determines the chunk size used by the children chunking optimization. If
   * null is returned (which is the default), the chunking optimization is
   * disabled.
   */
  getChunkSize: (node: Ancestor) => number | null;
}
interface ReactEditorInterface extends DOMEditorInterface {}
declare const ReactEditor: ReactEditorInterface;
interface VoidElement {
  _type: string;
  _key: string;
  children: Descendant[];
  __inline: boolean;
  value: Record<string, unknown>;
}
interface SlateTextBlock extends Omit<PortableTextTextBlock, 'children'> {
  children: Descendant[];
}
declare module '../slate/index' {
  interface CustomTypes {
    Editor: BaseEditor & ReactEditor & PortableTextSlateEditor;
    Element: SlateTextBlock | VoidElement;
    Text: PortableTextSpan;
  }
}
//# sourceMappingURL=slate.d.ts.map
type HistoryItem = {
  operations: Operation[];
  timestamp: Date;
};
interface History {
  redos: HistoryItem[];
  undos: HistoryItem[];
}
type RemotePatch = {
  patch: Patch;
  time: Date;
  snapshot: PortableTextBlock[] | undefined;
  previousSnapshot: PortableTextBlock[] | undefined;
};
interface PortableTextSlateEditor extends ReactEditor {
  _key: 'editor';
  _type: 'editor';
  isTextBlock: (value: unknown) => value is PortableTextTextBlock;
  isTextSpan: (value: unknown) => value is PortableTextSpan;
  isListBlock: (value: unknown) => value is PortableTextListBlock;
  decoratedRanges: Array<DecoratedRange>;
  decoratorState: Record<string, boolean | undefined>;
  blockIndexMap: Map<string, number>;
  history: History;
  lastSelection: EditorSelection;
  lastSlateSelection: Range | null;
  listIndexMap: Map<string, number>;
  remotePatches: Array<RemotePatch>;
  undoStepId: string | undefined;
  value: Array<PortableTextBlock>;
  isDeferringMutations: boolean;
  isNormalizingNode: boolean;
  isPatching: boolean;
  isPerformingBehaviorOperation: boolean;
  isProcessingRemoteChanges: boolean;
  isRedoing: boolean;
  isUndoing: boolean;
  withHistory: boolean;
  /**
   * Undo
   */
  undo: () => void;
  /**
   * Redo
   */
  redo: () => void;
}
/**
 * @public
 */
type EditorEmittedEvent = {
  type: 'blurred';
  event: FocusEvent<HTMLDivElement, Element>;
} | {
  /**
   * @deprecated Will be removed in the next major version
   */
  type: 'done loading';
} | {
  type: 'editable';
} | ErrorEvent | {
  type: 'focused';
  event: FocusEvent<HTMLDivElement, Element>;
} | {
  type: 'invalid value';
  resolution: InvalidValueResolution | null;
  value: Array<PortableTextBlock> | undefined;
} | {
  /**
   * @deprecated Will be removed in the next major version
   */
  type: 'loading';
} | MutationEvent | PatchEvent | {
  type: 'read only';
} | {
  type: 'ready';
} | {
  type: 'selection';
  selection: EditorSelection;
} | {
  type: 'value changed';
  value: Array<PortableTextBlock> | undefined;
};
/**
 * @deprecated The event is no longer emitted
 */
type ErrorEvent = {
  type: 'error';
  name: string;
  description: string;
  data: unknown;
};
/**
 * @public
 */
type MutationEvent = {
  type: 'mutation';
  patches: Array<Patch>;
  value: Array<PortableTextBlock> | undefined;
};
type PatchEvent = {
  type: 'patch';
  patch: Patch;
};
type SlateEditor = {
  instance: PortableTextSlateEditor;
  initialValue: Array<Descendant>;
};
type InternalEditor = Editor & {
  _internal: {
    editable: EditableAPI;
    editorActor: EditorActor;
    slateEditor: SlateEditor;
  };
};
/**
 * @public
 * @deprecated Use `useEditor()` instead
 *
 * ```
 * import {useEditor} from '@portabletext/editor'
 *
 * // Get the editor instance
 * const editor = useEditor()
 *
 * // Send events to the editor
 * editor.send(...)
 *
 * // Derive state from the editor
 * const state = useEditorSelector(editor, snapshot => ...)
 * ```
 */
declare class PortableTextEditor {
  /**
   * An observable of all the editor changes.
   */
  change$: EditorChanges;
  /**
   * A lookup table for all the relevant schema types for this portable text type.
   */
  schemaTypes: PortableTextMemberSchemaTypes;
  /**
   * The editor instance
   */
  private editor;
  private editable;
  constructor(config: {
    editor: InternalEditor;
  });
  setEditable: (editable: EditableAPI) => void;
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
  static activeAnnotations: (editor: PortableTextEditor) => PortableTextObject[];
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
  static isAnnotationActive: (editor: PortableTextEditor, annotationType: PortableTextObject["_type"]) => boolean;
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
  static addAnnotation: <TSchemaType extends {
    name: string;
  }>(editor: PortableTextEditor, type: TSchemaType, value?: {
    [prop: string]: unknown;
  }) => AddedAnnotationPaths | undefined;
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
  static blur: (editor: PortableTextEditor) => void;
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
  static delete: (editor: PortableTextEditor, selection: EditorSelection, options?: EditableAPIDeleteOptions) => void;
  static findDOMNode: (editor: PortableTextEditor, element: PortableTextBlock | PortableTextChild) => Node | undefined;
  static findByPath: (editor: PortableTextEditor, path: Path) => [_portabletext_schema6.PortableTextTextBlock<PortableTextObject | _portabletext_schema6.PortableTextSpan> | PortableTextObject | _portabletext_schema6.PortableTextSpan | undefined, Path | undefined];
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
  static focus: (editor: PortableTextEditor) => void;
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
  static focusBlock: (editor: PortableTextEditor) => PortableTextBlock | undefined;
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
  static focusChild: (editor: PortableTextEditor) => PortableTextChild | undefined;
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
  static getSelection: (editor: PortableTextEditor) => EditorSelection;
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
  static getValue: (editor: PortableTextEditor) => PortableTextBlock[] | undefined;
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
  static hasBlockStyle: (editor: PortableTextEditor, blockStyle: string) => boolean;
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
  static hasListStyle: (editor: PortableTextEditor, listStyle: string) => boolean;
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
  static isCollapsedSelection: (editor: PortableTextEditor) => boolean;
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
  static isExpandedSelection: (editor: PortableTextEditor) => boolean;
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
  static isMarkActive: (editor: PortableTextEditor, mark: string) => boolean;
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
  static insertChild: <TSchemaType extends {
    name: string;
  }>(editor: PortableTextEditor, type: TSchemaType, value?: {
    [prop: string]: unknown;
  }) => Path | undefined;
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
  static insertBlock: <TSchemaType extends {
    name: string;
  }>(editor: PortableTextEditor, type: TSchemaType, value?: {
    [prop: string]: unknown;
  }) => Path | undefined;
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
  static insertBreak: (editor: PortableTextEditor) => void;
  static isVoid: (editor: PortableTextEditor, element: PortableTextBlock | PortableTextChild) => boolean;
  static isObjectPath: (_editor: PortableTextEditor, path: Path) => boolean;
  static marks: (editor: PortableTextEditor) => string[];
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
  static select: (editor: PortableTextEditor, selection: EditorSelection | null) => void;
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
  static removeAnnotation: <TSchemaType extends {
    name: string;
  }>(editor: PortableTextEditor, type: TSchemaType) => void;
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
  static toggleBlockStyle: (editor: PortableTextEditor, blockStyle: string) => void;
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
  static toggleList: (editor: PortableTextEditor, listStyle: string) => void;
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
  static toggleMark: (editor: PortableTextEditor, mark: string) => void;
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
  static getFragment: (editor: PortableTextEditor) => PortableTextBlock[] | undefined;
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
  static undo: (editor: PortableTextEditor) => void;
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
  static redo: (editor: PortableTextEditor) => void;
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
  static isSelectionsOverlapping: (editor: PortableTextEditor, selectionA: EditorSelection, selectionB: EditorSelection) => boolean;
}
/**
 * @beta
 */
type HotkeyOptions = {
  marks?: Record<string, string>;
  custom?: Record<string, (event: BaseSyntheticEvent, editor: PortableTextEditor) => void>;
};
/**
 * @public
 */
type PortableTextEditableProps = Omit<TextareaHTMLAttributes<HTMLDivElement>, 'onPaste' | 'onCopy' | 'onBeforeInput'> & {
  ref?: React.Ref<HTMLDivElement>;
  hotkeys?: HotkeyOptions;
  onBeforeInput?: (event: InputEvent) => void;
  onPaste?: OnPasteFn;
  onCopy?: OnCopyFn;
  rangeDecorations?: RangeDecoration[];
  renderAnnotation?: RenderAnnotationFunction;
  renderBlock?: RenderBlockFunction;
  renderChild?: RenderChildFunction;
  renderDecorator?: RenderDecoratorFunction;
  renderListItem?: RenderListItemFunction;
  renderPlaceholder?: RenderPlaceholderFunction;
  renderStyle?: RenderStyleFunction;
  scrollSelectionIntoView?: ScrollSelectionIntoViewFunction;
  selection?: EditorSelection;
  spellCheck?: boolean;
};
/**
 * @public
 *
 *
 * The core component that renders the editor. Must be placed within the {@link EditorProvider} component.
 *
 * @example
 * ```tsx
 * import { PortableTextEditable, EditorProvider } from '@portabletext/editor'
 *
 * function MyComponent() {
 *  return (
 *   <EditorProvider>
 *    <PortableTextEditable />
 *  </EditorProvider>
 *  )
 * }
 * ```
 * @group Components
 */
declare const PortableTextEditable: react10.ForwardRefExoticComponent<Omit<PortableTextEditableProps, "ref"> & react10.RefAttributes<Omit<HTMLDivElement, "as" | "onPaste" | "onBeforeInput">>>;
/** @beta */
interface EditableAPIDeleteOptions {
  mode?: 'blocks' | 'children' | 'selected';
}
/**
 * @public
 */
type AddedAnnotationPaths = {
  /**
   * @deprecated An annotation may be applied to multiple blocks, resulting
   * in multiple `markDef`'s being created. Use `markDefPaths` instead.
   */
  markDefPath: Path;
  markDefPaths: Array<Path>;
  /**
   * @deprecated Does not return anything meaningful since an annotation
   * can span multiple blocks and spans. If references the span closest
   * to the focus point of the selection.
   */
  spanPath: Path;
};
/** @beta */
interface EditableAPI {
  activeAnnotations: () => PortableTextObject[];
  isAnnotationActive: (annotationType: PortableTextObject['_type']) => boolean;
  addAnnotation: <TSchemaType extends {
    name: string;
  }>(type: TSchemaType, value?: {
    [prop: string]: unknown;
  }) => AddedAnnotationPaths | undefined;
  blur: () => void;
  delete: (selection: EditorSelection, options?: EditableAPIDeleteOptions) => void;
  findByPath: (path: Path) => [PortableTextBlock | PortableTextChild | undefined, Path | undefined];
  findDOMNode: (element: PortableTextBlock | PortableTextChild) => Node | undefined;
  focus: () => void;
  focusBlock: () => PortableTextBlock | undefined;
  focusChild: () => PortableTextChild | undefined;
  getSelection: () => EditorSelection;
  getFragment: () => PortableTextBlock[] | undefined;
  getValue: () => PortableTextBlock[] | undefined;
  hasBlockStyle: (style: string) => boolean;
  hasListStyle: (listStyle: string) => boolean;
  insertBlock: <TSchemaType extends {
    name: string;
  }>(type: TSchemaType, value?: {
    [prop: string]: unknown;
  }) => Path;
  insertChild: <TSchemaType extends {
    name: string;
  }>(type: TSchemaType, value?: {
    [prop: string]: unknown;
  }) => Path;
  insertBreak: () => void;
  isCollapsedSelection: () => boolean;
  isExpandedSelection: () => boolean;
  isMarkActive: (mark: string) => boolean;
  isSelectionsOverlapping: (selectionA: EditorSelection, selectionB: EditorSelection) => boolean;
  isVoid: (element: PortableTextBlock | PortableTextChild) => boolean;
  marks: () => string[];
  redo: () => void;
  removeAnnotation: <TSchemaType extends {
    name: string;
  }>(type: TSchemaType) => void;
  select: (selection: EditorSelection) => void;
  toggleBlockStyle: (blockStyle: string) => void;
  toggleList: (listStyle: string) => void;
  toggleMark: (mark: string) => void;
  undo: () => void;
}
/** @public */
type EditorSelectionPoint = {
  path: Path;
  offset: number;
};
/** @public */
type EditorSelection = {
  anchor: EditorSelectionPoint;
  focus: EditorSelectionPoint;
  backward?: boolean;
} | null;
/**
 * The editor has mutated it's content.
 * @beta */
type MutationChange = {
  type: 'mutation';
  patches: Patch[];
  snapshot: PortableTextBlock[] | undefined;
};
/**
 * The editor has produced a patch
 * @beta */
type PatchChange = {
  type: 'patch';
  patch: Patch;
};
/**
 * The editor has received a new (props) value
 * @beta */
type ValueChange = {
  type: 'value';
  value: PortableTextBlock[] | undefined;
};
/**
 * The editor has a new selection
 * @beta */
type SelectionChange = {
  type: 'selection';
  selection: EditorSelection;
};
/**
 * The editor received focus
 * @beta */
type FocusChange = {
  type: 'focus';
  event: FocusEvent<HTMLDivElement, Element>;
};
/**
 * @beta
 * @deprecated Use `'patch'` changes instead
 */
type UnsetChange = {
  type: 'unset';
  previousValue: PortableTextBlock[];
};
/**
 * The editor blurred
 * @beta */
type BlurChange = {
  type: 'blur';
  event: FocusEvent<HTMLDivElement, Element>;
};
/**
 * The editor is currently loading something
 * Could be used to show a spinner etc.
 * @beta
 * @deprecated Will be removed in the next major version
 */
type LoadingChange = {
  type: 'loading';
  isLoading: boolean;
};
/**
 * The editor content is ready to be edited by the user
 * @beta */
type ReadyChange = {
  type: 'ready';
};
/**
 * The editor produced an error
 * @beta
 * @deprecated The change is no longer emitted
 * */
type ErrorChange = {
  type: 'error';
  name: string;
  level: 'warning' | 'error';
  description: string;
  data?: unknown;
};
/**
 * The editor has invalid data in the value that can be resolved by the user
 * @beta */
type InvalidValueResolution = {
  autoResolve?: boolean;
  patches: Patch[];
  description: string;
  action: string;
  item: PortableTextBlock[] | PortableTextBlock | PortableTextChild | undefined;
  /**
   * i18n keys for the description and action
   *
   * These are in addition to the description and action properties, to decouple the editor from
   * the i18n system, and allow usage without it. The i18n keys take precedence over the
   * description and action properties, if i18n framework is available.
   */
  i18n: {
    description: `inputs.portable-text.invalid-value.${Lowercase<string>}.description`;
    action: `inputs.portable-text.invalid-value.${Lowercase<string>}.action`;
    values?: Record<string, string | number | string[]>;
  };
};
/**
 * The editor has an invalid value
 * @beta */
type InvalidValue = {
  type: 'invalidValue';
  resolution: InvalidValueResolution | null;
  value: PortableTextBlock[] | undefined;
};
/**
 * The editor performed a undo history step
 * @beta
 * @deprecated The change is no longer emitted
 *  */
type UndoChange = {
  type: 'undo';
  patches: Patch[];
  timestamp: Date;
};
/**
 * The editor performed redo history step
 * @beta
 * @deprecated The change is no longer emitted
 *  */
type RedoChange = {
  type: 'redo';
  patches: Patch[];
  timestamp: Date;
};
/**
 * The editor was either connected or disconnected to the network
 * To show out of sync warnings etc when in collaborative mode.
 * @beta
 * @deprecated The change is no longer emitted
 *  */
type ConnectionChange = {
  type: 'connection';
  value: 'online' | 'offline';
};
/**
 * When the editor changes, it will emit a change item describing the change
 * @beta */
type EditorChange = BlurChange | ConnectionChange | ErrorChange | FocusChange | InvalidValue | LoadingChange | MutationChange | PatchChange | ReadyChange | RedoChange | SelectionChange | UndoChange | UnsetChange | ValueChange;
/**
 * @beta
 */
type EditorChanges = Subject<EditorChange>;
/** @beta */
type OnPasteResult = {
  insert?: TypedObject[];
  path?: Path;
} | undefined;
/**
 * @beta
 */
type OnPasteResultOrPromise = OnPasteResult | Promise<OnPasteResult>;
/** @beta */
interface PasteData {
  event: ClipboardEvent$1;
  path: Path;
  schemaTypes: PortableTextMemberSchemaTypes;
  value: PortableTextBlock[] | undefined;
}
/**
 * @beta
 * It is encouraged not to return `Promise<undefined>` from the `OnPasteFn` as
 * a mechanism to fall back to the native paste behaviour. This doesn't work in
 * all cases. Always return plain `undefined` if possible.
 **/
type OnPasteFn = (data: PasteData) => OnPasteResultOrPromise;
/** @beta */
type OnBeforeInputFn = (event: InputEvent) => void;
/** @beta */
type OnCopyFn = (event: ClipboardEvent$1<HTMLDivElement | HTMLSpanElement>) => undefined | unknown;
/** @beta */
type PatchObservable = Observable<{
  patches: Patch[];
  snapshot: PortableTextBlock[] | undefined;
}>;
/** @beta */
interface BlockRenderProps {
  children: ReactElement<any>;
  editorElementRef: RefObject<HTMLElement | null>;
  focused: boolean;
  level?: number;
  listItem?: string;
  path: BlockPath;
  selected: boolean;
  style?: string;
  schemaType: ObjectSchemaType;
  /** @deprecated Use `schemaType` instead */
  type: ObjectSchemaType;
  value: PortableTextBlock;
}
/** @beta */
interface BlockChildRenderProps {
  annotations: PortableTextObject[];
  children: ReactElement<any>;
  editorElementRef: RefObject<HTMLElement | null>;
  focused: boolean;
  path: Path;
  selected: boolean;
  schemaType: ObjectSchemaType;
  /** @deprecated Use `schemaType` instead */
  type: ObjectSchemaType;
  value: PortableTextChild;
}
/** @beta */
interface BlockAnnotationRenderProps {
  block: PortableTextBlock;
  children: ReactElement<any>;
  editorElementRef: RefObject<HTMLElement | null>;
  focused: boolean;
  path: Path;
  schemaType: ObjectSchemaType;
  selected: boolean;
  /** @deprecated Use `schemaType` instead */
  type: ObjectSchemaType;
  value: PortableTextObject;
}
/** @beta */
interface BlockDecoratorRenderProps {
  children: ReactElement<any>;
  editorElementRef: RefObject<HTMLElement | null>;
  focused: boolean;
  path: Path;
  schemaType: BlockDecoratorDefinition;
  selected: boolean;
  /** @deprecated Use `schemaType` instead */
  type: BlockDecoratorDefinition;
  value: string;
}
/** @beta */
interface BlockListItemRenderProps {
  block: PortableTextTextBlock;
  children: ReactElement<any>;
  editorElementRef: RefObject<HTMLElement | null>;
  focused: boolean;
  level: number;
  path: Path;
  schemaType: BlockListDefinition;
  selected: boolean;
  value: string;
}
/** @beta */
type RenderBlockFunction = (props: BlockRenderProps) => JSX.Element;
/** @beta */
type RenderChildFunction = (props: BlockChildRenderProps) => JSX.Element;
/** @beta */
type RenderEditableFunction = (props: PortableTextEditableProps) => JSX.Element;
/** @beta */
type RenderAnnotationFunction = (props: BlockAnnotationRenderProps) => JSX.Element;
/** @beta */
type RenderPlaceholderFunction = () => React.ReactNode;
/** @beta */
type RenderStyleFunction = (props: BlockStyleRenderProps) => JSX.Element;
/** @beta */
interface BlockStyleRenderProps {
  block: PortableTextTextBlock;
  children: ReactElement<any>;
  editorElementRef: RefObject<HTMLElement | null>;
  focused: boolean;
  path: Path;
  selected: boolean;
  schemaType: BlockStyleDefinition;
  value: string;
}
/** @beta */
type RenderListItemFunction = (props: BlockListItemRenderProps) => JSX.Element;
/** @beta */
type RenderDecoratorFunction = (props: BlockDecoratorRenderProps) => JSX.Element;
/** @beta */
type ScrollSelectionIntoViewFunction = (editor: PortableTextEditor, domRange: globalThis.Range) => void;
/**
 * Parameters for the callback that will be called for a RangeDecoration's onMoved.
 * @alpha */
interface RangeDecorationOnMovedDetails {
  rangeDecoration: RangeDecoration;
  newSelection: EditorSelection;
  origin: 'remote' | 'local';
}
/**
 * A range decoration is a UI affordance that wraps a given selection range in the editor
 * with a custom component. This can be used to highlight search results,
 * mark validation errors on specific words, draw user presence and similar.
 * @alpha */
interface RangeDecoration {
  /**
   * A component for rendering the range decoration.
   * The component will receive the children (text) of the range decoration as its children.
   *
   * @example
   * ```ts
   * (rangeComponentProps: PropsWithChildren) => (
   *    <SearchResultHighlight>
   *      {rangeComponentProps.children}
   *    </SearchResultHighlight>
   *  )
   * ```
   */
  component: (props: PropsWithChildren) => ReactElement<any>;
  /**
   * The editor content selection range
   */
  selection: EditorSelection;
  /**
   * A optional callback that will be called when the range decoration potentially moves according to user edits.
   */
  onMoved?: (details: RangeDecorationOnMovedDetails) => void;
  /**
   * A custom payload that can be set on the range decoration
   */
  payload?: Record<string, unknown>;
}
/** @beta */
type PortableTextMemberSchemaTypes = {
  annotations: (ObjectSchemaType & {
    i18nTitleKey?: string;
  })[];
  block: ObjectSchemaType;
  blockObjects: ObjectSchemaType[];
  decorators: BlockDecoratorDefinition[];
  inlineObjects: ObjectSchemaType[];
  portableText: ArraySchemaType<PortableTextBlock>;
  span: ObjectSchemaType;
  styles: BlockStyleDefinition[];
  lists: BlockListDefinition[];
};
/**
 * @public
 */
type EditorContext = {
  converters: Array<Converter>;
  keyGenerator: () => string;
  readOnly: boolean;
  schema: EditorSchema;
  selection: EditorSelection;
  value: Array<PortableTextBlock>;
};
/**
 * @public
 */
type EditorSnapshot = {
  context: EditorContext;
  blockIndexMap: Map<string, number>;
  /**
   * @beta
   * Subject to change
   */
  decoratorState: Record<string, boolean | undefined>;
};
/**
 * @beta
 */
type BehaviorGuard<TBehaviorEvent, TGuardResponse> = (payload: {
  snapshot: EditorSnapshot;
  event: TBehaviorEvent;
  dom: EditorDom;
}) => TGuardResponse | false;
/**
 * @beta
 */
type Behavior<TBehaviorEventType extends '*' | `${BehaviorEventTypeNamespace}.*` | BehaviorEvent['type'] = '*' | `${BehaviorEventTypeNamespace}.*` | BehaviorEvent['type'], TGuardResponse = true, TBehaviorEvent extends ResolveBehaviorEvent<TBehaviorEventType> = ResolveBehaviorEvent<TBehaviorEventType>> = {
  /**
   * Editor Event that triggers this Behavior.
   */
  on: TBehaviorEventType;
  /**
   * Predicate function that determines if the Behavior should be executed.
   * Returning a non-nullable value from the guard will pass the value to the
   * actions and execute them.
   */
  guard?: BehaviorGuard<TBehaviorEvent, TGuardResponse>;
  /**
   * Array of Behavior Action sets.
   * Each set represents a step in the history stack.
   */
  actions: Array<BehaviorActionSet<TBehaviorEvent, TGuardResponse>>;
};
/**
 * @beta
 *
 * @example
 *
 * ```tsx
 * const noLowerCaseA = defineBehavior({
 *   on: 'insert.text',
 *   guard: ({event, snapshot}) => event.text === 'a',
 *   actions: [({event, snapshot}) => [{type: 'insert.text', text: 'A'}]],
 * })
 * ```
 *
 */
declare function defineBehavior<TPayload extends Record<string, unknown>, TBehaviorEventType extends '*' | `${BehaviorEventTypeNamespace}.*` | BehaviorEvent['type'] = CustomBehaviorEvent['type'], TGuardResponse = true>(behavior: Behavior<TBehaviorEventType, TGuardResponse, ResolveBehaviorEvent<TBehaviorEventType, TPayload>>): Behavior;
/**
 * @public
 */
type EditorConfig = {
  /**
   * @beta
   */
  keyGenerator?: () => string;
  readOnly?: boolean;
  initialValue?: Array<PortableTextBlock>;
} & ({
  schemaDefinition: SchemaDefinition;
  schema?: undefined;
} | {
  schemaDefinition?: undefined;
  schema: ArraySchemaType<PortableTextBlock> | ArrayDefinition;
});
/**
 * @public
 */
type EditorEvent = ExternalEditorEvent | ExternalBehaviorEvent | {
  type: 'update value';
  value: Array<PortableTextBlock> | undefined;
};
/**
 * @public
 */
type Editor = {
  dom: EditorDom;
  getSnapshot: () => EditorSnapshot;
  /**
   * @beta
   */
  registerBehavior: (config: {
    behavior: Behavior;
  }) => () => void;
  send: (event: EditorEvent) => void;
  on: ActorRef<Snapshot<unknown>, EventObject, EditorEmittedEvent>['on'];
};
/**
 * @public
 */
type EditorProviderProps = {
  initialConfig: EditorConfig;
  children?: React$1.ReactNode;
};
/**
 * @public
 * The EditorProvider component is used to set up the editor context and configure the Portable Text Editor.
 * @example
 * ```tsx
 * import {EditorProvider} from '@portabletext/editor'
 *
 * function App() {
 *  return (
 *    <EditorProvider initialConfig={{ ... }} >
 *      ...
 *    </EditorProvider>
 *  )
 * }
 *
 * ```
 * @group Components
 */
declare function EditorProvider(props: EditorProviderProps): React$1.JSX.Element;
/**
 * @public
 */
type EditorSelector<TSelected> = (snapshot: EditorSnapshot) => TSelected;
/**
 * @public
 * Hook to select a value from the editor state.
 * @example
 * Pass a selector as the second argument
 * ```tsx
 * import { useEditorSelector } from '@portabletext/editor'
 *
 * function MyComponent(editor) {
 *  const value = useEditorSelector(editor, selector)
 * }
 * ```
 * @example
 * Pass an inline selector as the second argument.
 * In this case, use the editor context to obtain the schema.
 * ```tsx
 * import { useEditorSelector } from '@portabletext/editor'
 *
 * function MyComponent(editor) {
 *  const schema = useEditorSelector(editor, (snapshot) => snapshot.context.schema)
 * }
 * ```
 * @group Hooks
 */
declare function useEditorSelector<TSelected>(editor: Editor, selector: EditorSelector<TSelected>, compare?: (a: TSelected, b: TSelected) => boolean): TSelected;
/**
 * @deprecated Use `useEditor` to get the current editor instance.
 * @public
 * Get the current editor object from the React context.
 */
declare const usePortableTextEditor: () => PortableTextEditor;
/**
 * @deprecated Use `useEditorSelector` to get the current editor selection.
 * @public
 * Get the current editor selection from the React context.
 */
declare const usePortableTextEditorSelection: () => EditorSelection;
/**
 * @public
 */
declare const defaultKeyGenerator: () => string;
/**
 * @public
 * Get the current editor context from the `EditorProvider`.
 * Must be used inside the `EditorProvider` component.
 * @returns The current editor object.
 * @example
 * ```tsx
 * import { useEditor } from '@portabletext/editor'
 *
 * function MyComponent() {
 *  const editor = useEditor()
 * }
 * ```
 * @group Hooks
 */
declare function useEditor(): Editor;
/**
 * @beta
 */
type BlockOffset = {
  path: BlockPath;
  offset: number;
};
type EditorPriority = {
  id: string;
  name?: string;
  reference?: {
    priority: EditorPriority;
    importance: 'higher' | 'lower';
  };
};
type BehaviorConfig = {
  behavior: Behavior;
  priority: EditorPriority;
};
/**
 * @public
 */
type PatchesEvent = {
  type: 'patches';
  patches: Array<Patch>;
  snapshot: Array<PortableTextBlock> | undefined;
};
/**
 * @public
 */
type ExternalEditorEvent = {
  type: 'update readOnly';
  readOnly: boolean;
} | PatchesEvent;
type InternalPatchEvent = NamespaceEvent<PatchEvent, 'internal'> & {
  operationId?: string;
  value: Array<PortableTextBlock>;
};
/**
 * @internal
 */
type EditorActor = ActorRefFrom<typeof editorMachine>;
/**
 * @internal
 */
declare const editorMachine: xstate73.StateMachine<{
  behaviors: Set<BehaviorConfig>;
  behaviorsSorted: boolean;
  converters: Set<Converter>;
  getLegacySchema: () => PortableTextMemberSchemaTypes;
  keyGenerator: () => string;
  pendingEvents: Array<InternalPatchEvent | MutationEvent>;
  pendingIncomingPatchesEvents: Array<PatchesEvent>;
  schema: EditorSchema;
  initialReadOnly: boolean;
  selection: EditorSelection;
  initialValue: Array<PortableTextBlock> | undefined;
  internalDrag?: {
    origin: Pick<EventPosition, "selection">;
  };
  dragGhost?: HTMLElement;
  slateEditor?: PortableTextSlateEditor;
}, InternalPatchEvent | MutationEvent | PatchesEvent | {
  type: "update readOnly";
  readOnly: boolean;
} | {
  type: "add behavior";
  behaviorConfig: BehaviorConfig;
} | {
  type: "remove behavior";
  behaviorConfig: BehaviorConfig;
} | {
  type: "blur";
  editor: PortableTextSlateEditor;
} | {
  type: "focus";
  editor: PortableTextSlateEditor;
} | {
  type: "update selection";
  selection: EditorSelection;
} | {
  type: "done syncing value";
} | {
  type: "syncing value";
} | {
  type: "behavior event";
  behaviorEvent: BehaviorEvent;
  editor: PortableTextSlateEditor;
  nativeEvent?: {
    preventDefault: () => void;
  };
} | {
  type: "set drag ghost";
  ghost: HTMLElement;
} | {
  type: "dragstart";
  ghost?: HTMLElement;
  origin: Pick<EventPosition, "selection">;
} | {
  type: "dragend";
} | {
  type: "drop";
} | {
  type: "add slate editor";
  editor: PortableTextSlateEditor;
}, {}, never, {
  type: "add behavior to context";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "remove behavior from context";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "add slate editor to context";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "emit patch event";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "emit mutation event";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "emit read only";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "emit editable";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "defer event";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "emit pending events";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "emit ready";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "clear pending events";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "discard conflicting pending patches";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "discard all pending events";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "defer incoming patches";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "emit pending incoming patches";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "clear pending incoming patches";
  params: xstate73.NonReducibleUnknown;
} | {
  type: "handle blur";
  params: unknown;
} | {
  type: "handle focus";
  params: unknown;
} | {
  type: "handle behavior event";
  params: unknown;
} | {
  type: "sort behaviors";
  params: xstate73.NonReducibleUnknown;
}, {
  type: "slate is busy";
  params: unknown;
} | {
  type: "slate is normalizing node";
  params: unknown;
}, never, {
  "edit mode": {
    editable: "dragging internally" | "idle" | {
      focusing: "checking if busy" | "busy";
    };
  } | {
    "read only": "read only" | "determine initial edit mode";
  };
  setup: "setting up" | {
    "set up": {
      "value sync": "syncing value" | "idle";
      writing: "dirty" | {
        pristine: "idle";
      };
    };
  };
}, "dragging internally", {
  converters?: Array<Converter>;
  getLegacySchema: () => PortableTextMemberSchemaTypes;
  keyGenerator: () => string;
  readOnly?: boolean;
  schema: EditorSchema;
  initialValue?: Array<PortableTextBlock>;
}, xstate73.NonReducibleUnknown, InternalPatchEvent | MutationEvent | PatchesEvent | {
  type: "blurred";
  event: react10.FocusEvent<HTMLDivElement, Element>;
} | {
  type: "done loading";
} | {
  type: "editable";
} | {
  type: "error";
  name: string;
  description: string;
  data: unknown;
} | {
  type: "focused";
  event: react10.FocusEvent<HTMLDivElement, Element>;
} | {
  type: "invalid value";
  resolution: InvalidValueResolution | null;
  value: Array<PortableTextBlock> | undefined;
} | {
  type: "loading";
} | {
  type: "read only";
} | {
  type: "ready";
} | {
  type: "selection";
  selection: EditorSelection;
} | {
  type: "value changed";
  value: Array<PortableTextBlock> | undefined;
}, xstate73.MetaObject, {
  id: "editor";
  states: {
    readonly 'edit mode': {
      states: {
        readonly 'read only': {
          states: {
            readonly 'determine initial edit mode': {};
            readonly 'read only': {};
          };
        };
        readonly editable: {
          states: {
            readonly idle: {};
            readonly focusing: {
              states: {
                readonly 'checking if busy': {};
                readonly busy: {};
              };
            };
            readonly 'dragging internally': {};
          };
        };
      };
    };
    readonly setup: {
      states: {
        readonly 'setting up': {};
        readonly 'set up': {
          states: {
            readonly 'value sync': {
              states: {
                readonly idle: {};
                readonly 'syncing value': {};
              };
            };
            readonly writing: {
              states: {
                readonly pristine: {
                  states: {
                    readonly idle: {};
                  };
                };
                readonly dirty: {};
              };
            };
          };
        };
      };
    };
  };
}>;
type EventPosition = {
  block: 'start' | 'end';
  /**
   * Did the event origin from the editor DOM node itself or from a child node?
   */
  isEditor: boolean;
  selection: NonNullable<EditorSelection>;
};
type TextBlockWithOptionalKey = Omit<PortableTextTextBlock, '_key'> & {
  _key?: PortableTextTextBlock['_key'];
};
type ObjectBlockWithOptionalKey = Omit<PortableTextObject, '_key'> & {
  _key?: PortableTextObject['_key'];
};
type BlockWithOptionalKey = TextBlockWithOptionalKey | ObjectBlockWithOptionalKey;
type SpanWithOptionalKey = Omit<PortableTextSpan, '_key'> & {
  _key?: PortableTextSpan['_key'];
};
type ChildWithOptionalKey = SpanWithOptionalKey | ObjectBlockWithOptionalKey;
/**
 * @beta
 */
type BehaviorEvent = SyntheticBehaviorEvent | NativeBehaviorEvent | CustomBehaviorEvent;
type BehaviorEventTypeNamespace = SyntheticBehaviorEventNamespace | NativeBehaviorEventNamespace | CustomBehaviorEventNamespace;
type NamespacedBehaviorEventType<TNamespace$1 extends BehaviorEventTypeNamespace | ''> = TNamespace$1 extends '' ? BehaviorEvent['type'] : Extract<BehaviorEvent['type'], TNamespace$1 | `${TNamespace$1}.${string}`>;
/**************************************
 * External events
 **************************************/
type ExternalBehaviorEventNamespace = 'blur' | 'focus' | 'insert';
type ExternalBehaviorEventType<TNamespace$1 extends ExternalBehaviorEventNamespace, TType$1 extends string = ''> = TType$1 extends '' ? `${TNamespace$1}` : `${TNamespace$1}.${TType$1}`;
type ExternalBehaviorEvent = {
  type: ExternalBehaviorEventType<'blur'>;
} | {
  type: ExternalBehaviorEventType<'focus'>;
} | {
  type: ExternalBehaviorEventType<'insert', 'block object'>;
  placement: InsertPlacement;
  blockObject: {
    name: string;
    value?: {
      [prop: string]: unknown;
    };
  };
} | BehaviorEvent;
/**************************************
 * Synthetic events
 **************************************/
declare const syntheticBehaviorEventTypes: readonly ["annotation.add", "annotation.remove", "block.set", "block.unset", "child.set", "child.unset", "decorator.add", "decorator.remove", "delete", "history.redo", "history.undo", "insert.block", "insert.child", "insert.text", "move.backward", "move.block", "move.forward", "select"];
type SyntheticBehaviorEventType = (typeof syntheticBehaviorEventTypes)[number] | (typeof abstractBehaviorEventTypes)[number];
type SyntheticBehaviorEventNamespace = ExtractNamespace<SyntheticBehaviorEventType>;
/**
 * @beta
 */
type SyntheticBehaviorEvent = {
  type: StrictExtract<SyntheticBehaviorEventType, 'annotation.add'>;
  annotation: {
    name: string;
    _key?: string;
    value: {
      [prop: string]: unknown;
    };
  };
  at?: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'annotation.remove'>;
  annotation: {
    name: string;
  };
  at?: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'block.set'>;
  at: BlockPath;
  props: Record<string, unknown>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'block.unset'>;
  at: BlockPath;
  props: Array<string>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'child.set'>;
  at: ChildPath;
  props: {
    [prop: string]: unknown;
  };
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'child.unset'>;
  at: ChildPath;
  props: Array<string>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'decorator.add'>;
  decorator: string;
  at?: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'decorator.remove'>;
  decorator: string;
  at?: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'delete'>;
  at?: NonNullable<EditorSelection>;
  /**
   * Defaults to forward deletion.
   */
  direction?: 'backward' | 'forward';
  /**
   * Defaults to character deletion.
   */
  unit?: 'character' | 'word' | 'line' | 'block' | 'child';
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'history.redo'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'history.undo'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'insert.block'>;
  block: BlockWithOptionalKey;
  placement: InsertPlacement;
  select?: 'start' | 'end' | 'none';
  at?: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'insert.child'>;
  child: ChildWithOptionalKey;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'insert.text'>;
  text: string;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'move.backward'>;
  distance: number;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'move.block'>;
  at: BlockPath;
  to: BlockPath;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'move.forward'>;
  distance: number;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'select'>;
  at: EditorSelection;
} | AbstractBehaviorEvent;
/**
 * @beta
 */
type InsertPlacement = 'auto' | 'after' | 'before';
/**************************************
 * Abstract events
 **************************************/
declare const abstractBehaviorEventTypes: readonly ["annotation.set", "annotation.toggle", "decorator.toggle", "delete.backward", "delete.block", "delete.child", "delete.forward", "delete.text", "deserialize", "deserialize.data", "deserialization.success", "deserialization.failure", "insert.blocks", "insert.break", "insert.inline object", "insert.soft break", "insert.span", "list item.add", "list item.remove", "list item.toggle", "move.block down", "move.block up", "select.block", "select.previous block", "select.next block", "serialize", "serialize.data", "serialization.success", "serialization.failure", "split", "style.add", "style.remove", "style.toggle"];
type AbstractBehaviorEvent = {
  type: StrictExtract<SyntheticBehaviorEventType, 'annotation.set'>;
  at: AnnotationPath;
  props: Record<string, unknown>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'annotation.toggle'>;
  annotation: {
    name: string;
    value: {
      [prop: string]: unknown;
    };
  };
  at?: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'decorator.toggle'>;
  decorator: string;
  at?: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'delete.backward'>;
  unit: 'character' | 'word' | 'line' | 'block';
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'delete.block'>;
  at: BlockPath;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'delete.child'>;
  at: ChildPath;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'delete.forward'>;
  unit: 'character' | 'word' | 'line' | 'block';
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'delete.text'>;
  at: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'deserialize'>;
  originEvent: PickFromUnion<NativeBehaviorEvent, 'type', 'drag.drop' | 'clipboard.paste'> | InputBehaviorEvent;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'deserialize.data'>;
  mimeType: MIMEType;
  data: string;
  originEvent: PickFromUnion<NativeBehaviorEvent, 'type', 'drag.drop' | 'clipboard.paste'> | InputBehaviorEvent;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'serialize'>;
  originEvent: PickFromUnion<NativeBehaviorEvent, 'type', 'clipboard.copy' | 'clipboard.cut' | 'drag.dragstart'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'serialize.data'>;
  mimeType: MIMEType;
  originEvent: PickFromUnion<NativeBehaviorEvent, 'type', 'clipboard.copy' | 'clipboard.cut' | 'drag.dragstart'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'deserialization.success'>;
  mimeType: MIMEType;
  data: Array<PortableTextBlock>;
  originEvent: PickFromUnion<NativeBehaviorEvent, 'type', 'drag.drop' | 'clipboard.paste'> | InputBehaviorEvent;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'deserialization.failure'>;
  mimeType: MIMEType;
  reason: string;
  originEvent: PickFromUnion<NativeBehaviorEvent, 'type', 'drag.drop' | 'clipboard.paste'> | InputBehaviorEvent;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'serialization.success'>;
  mimeType: MIMEType;
  data: string;
  originEvent: PickFromUnion<NativeBehaviorEvent, 'type', 'clipboard.copy' | 'clipboard.cut' | 'drag.dragstart'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'serialization.failure'>;
  mimeType: MIMEType;
  reason: string;
  originEvent: PickFromUnion<NativeBehaviorEvent, 'type', 'clipboard.copy' | 'clipboard.cut' | 'drag.dragstart'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'insert.blocks'>;
  blocks: Array<BlockWithOptionalKey>;
  placement: InsertPlacement;
  select?: 'start' | 'end' | 'none';
  at?: NonNullable<EditorSelection>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'insert.break'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'insert.inline object'>;
  inlineObject: {
    name: string;
    value?: {
      [prop: string]: unknown;
    };
  };
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'insert.soft break'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'insert.span'>;
  text: string;
  annotations?: Array<{
    name: string;
    value: {
      [prop: string]: unknown;
    };
  }>;
  decorators?: Array<string>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'list item.add'>;
  listItem: string;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'list item.remove'>;
  listItem: string;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'list item.toggle'>;
  listItem: string;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'move.block down'>;
  at: BlockPath;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'move.block up'>;
  at: BlockPath;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'select.block'>;
  at: BlockPath;
  select?: 'start' | 'end';
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'select.previous block'>;
  select?: 'start' | 'end';
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'select.next block'>;
  select?: 'start' | 'end';
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'split'>;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'style.add'>;
  style: string;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'style.remove'>;
  style: string;
} | {
  type: StrictExtract<SyntheticBehaviorEventType, 'style.toggle'>;
  style: string;
};
/**************************************
 * Native events
 **************************************/
declare const nativeBehaviorEventTypes: readonly ["clipboard.copy", "clipboard.cut", "clipboard.paste", "drag.dragstart", "drag.drag", "drag.dragend", "drag.dragenter", "drag.dragover", "drag.dragleave", "drag.drop", "input.*", "keyboard.keydown", "keyboard.keyup", "mouse.click"];
type NativeBehaviorEventType = (typeof nativeBehaviorEventTypes)[number];
type NativeBehaviorEventNamespace = ExtractNamespace<NativeBehaviorEventType>;
/**
 * @beta
 */
type NativeBehaviorEvent = ClipboardBehaviorEvent | DragBehaviorEvent | InputBehaviorEvent | KeyboardBehaviorEvent | MouseBehaviorEvent;
type ClipboardBehaviorEvent = {
  type: StrictExtract<NativeBehaviorEventType, 'clipboard.copy'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
  position: Pick<EventPosition, 'selection'>;
} | {
  type: StrictExtract<NativeBehaviorEventType, 'clipboard.cut'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
  position: Pick<EventPosition, 'selection'>;
} | {
  type: StrictExtract<NativeBehaviorEventType, 'clipboard.paste'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
  position: Pick<EventPosition, 'selection'>;
};
type DragBehaviorEvent = {
  type: StrictExtract<NativeBehaviorEventType, 'drag.dragstart'>;
  originEvent: {
    clientX: number;
    clientY: number;
    dataTransfer: DataTransfer;
  };
  position: Pick<EventPosition, 'selection'>;
} | {
  type: StrictExtract<NativeBehaviorEventType, 'drag.drag'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
} | {
  type: StrictExtract<NativeBehaviorEventType, 'drag.dragend'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
} | {
  type: StrictExtract<NativeBehaviorEventType, 'drag.dragenter'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
  position: EventPosition;
} | {
  type: StrictExtract<NativeBehaviorEventType, 'drag.dragover'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
  dragOrigin?: Pick<EventPosition, 'selection'>;
  position: EventPosition;
} | {
  type: StrictExtract<NativeBehaviorEventType, 'drag.drop'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
  dragOrigin?: Pick<EventPosition, 'selection'>;
  position: EventPosition;
} | {
  type: StrictExtract<NativeBehaviorEventType, 'drag.dragleave'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
};
/**
 * Used to represent native InputEvents that hold a DataTransfer object.
 *
 * These can either be one of:
 *
 * - insertFromPaste
 * - insertFromPasteAsQuotation
 * - insertFromDrop
 * - insertReplacementText
 * - insertFromYank
 */
type InputBehaviorEvent = {
  type: StrictExtract<NativeBehaviorEventType, 'input.*'>;
  originEvent: {
    dataTransfer: DataTransfer;
  };
};
type KeyboardBehaviorEvent = {
  type: StrictExtract<NativeBehaviorEventType, 'keyboard.keydown'>;
  originEvent: Pick<KeyboardEvent, 'key' | 'code' | 'altKey' | 'ctrlKey' | 'metaKey' | 'shiftKey'>;
} | {
  type: StrictExtract<NativeBehaviorEventType, 'keyboard.keyup'>;
  originEvent: Pick<KeyboardEvent, 'key' | 'code' | 'altKey' | 'ctrlKey' | 'metaKey' | 'shiftKey'>;
};
type MouseBehaviorEvent = {
  type: StrictExtract<NativeBehaviorEventType, 'mouse.click'>;
  position: EventPosition;
};
/**************************************
 * Custom events
 **************************************/
type CustomBehaviorEventNamespace = 'custom';
type CustomBehaviorEventType<TNamespace$1 extends CustomBehaviorEventNamespace, TType$1 extends string = ''> = TType$1 extends '' ? `${TNamespace$1}` : `${TNamespace$1}.${TType$1}`;
/**
 * @beta
 */
type CustomBehaviorEvent<TPayload extends Record<string, unknown> = Record<string, unknown>, TType$1 extends string = string, TInternalType extends CustomBehaviorEventType<'custom', TType$1> = CustomBehaviorEventType<'custom', TType$1>> = {
  type: TInternalType;
} & TPayload;
/**************************************
 * Resolve behavior event
 **************************************/
type ResolveBehaviorEvent<TBehaviorEventType extends '*' | `${BehaviorEventTypeNamespace}.*` | BehaviorEvent['type'], TPayload extends Record<string, unknown> = Record<string, unknown>> = TBehaviorEventType extends '*' ? BehaviorEvent : TBehaviorEventType extends `${infer TNamespace}.*` ? TNamespace extends BehaviorEventTypeNamespace ? PickFromUnion<BehaviorEvent, 'type', NamespacedBehaviorEventType<TNamespace>> : never : TBehaviorEventType extends `custom.${infer TType}` ? CustomBehaviorEvent<TPayload, TType> : TBehaviorEventType extends BehaviorEvent['type'] ? PickFromUnion<BehaviorEvent, 'type', TBehaviorEventType> : never;
type ExtractNamespace<TType$1 extends string> = TType$1 extends `${infer Namespace}.${string}` ? Namespace : TType$1;
type EditorDom = {
  getBlockNodes: (snapshot: EditorSnapshot) => Array<Node>;
  getChildNodes: (snapshot: EditorSnapshot) => Array<Node>;
  getEditorElement: () => Element | undefined;
  getSelectionRect: (snapshot: EditorSnapshot) => DOMRect | null;
  getStartBlockElement: (snapshot: EditorSnapshot) => Element | null;
  getEndBlockElement: (snapshot: EditorSnapshot) => Element | null;
  /**
   * Let the Editor set the drag ghost. This is to be sure that it will get
   * properly removed again when the drag ends.
   */
  setDragGhost: ({
    event,
    ghost
  }: {
    event: PickFromUnion<BehaviorEvent, 'type', 'drag.dragstart'>;
    ghost: {
      element: HTMLElement;
      x: number;
      y: number;
    };
  }) => void;
};
/**
 * @beta
 */
type BehaviorAction = {
  type: 'execute';
  event: SyntheticBehaviorEvent;
} | {
  type: 'forward';
  event: NativeBehaviorEvent | SyntheticBehaviorEvent | CustomBehaviorEvent;
} | {
  type: 'raise';
  event: SyntheticBehaviorEvent | CustomBehaviorEvent;
} | {
  type: 'effect';
  effect: (payload: {
    /**
     * Send a Behavior Event back into the Editor.
     *
     * @example
     * ```ts
     * defineBehavior({
     *   on: '...',
     *   actions: [
     *     () => [
     *       effect(({send}) => {
     *         doSomethingAsync()
     *           .then(() => {
     *             send({
     *               type: '...',
     *             })
     *           })
     *       })
     *     ],
     *   ],
     * })
     * ```
     */
    send: (event: ExternalBehaviorEvent) => void;
  }) => void;
};
/**
 * Directly executes an event, bypassing all Behavior matching.
 *
 * Use `execute` when you want to perform an action without triggering any
 * Behaviors. The event is executed immediately as a direct operation.
 *
 * @example
 * ```ts
 * defineBehavior({
 *   on: 'insert.text',
 *   guard: ({event}) => event.text === 'a',
 *   actions: [() => [execute({type: 'insert.text', text: 'b'})]],
 * })
 * ```
 *
 * @beta
 */
declare function execute(event: SyntheticBehaviorEvent): PickFromUnion<BehaviorAction, 'type', 'execute'>;
/**
 * Forwards an event to the next Behavior(s) in the current chain.
 *
 * Use `forward` to pass an event to succeeding Behaviors without starting a
 * fresh lookup. This is useful for intercepting events, performing side
 * effects, and then letting the default handling continue.
 *
 * **Key rule:** When forwarding to a different event type, only Behaviors that
 * were already in the remaining chain AND match the new type will run. This
 * means cross-type `forward` is mostly useful for falling through to default
 * Behaviors, not for triggering user-defined Behaviors of a different type.
 *
 * To trigger all Behaviors for a different event type, use {@link raise}
 * instead.
 *
 * @example
 * ```ts
 * // Intercept and forward same event type
 * defineBehavior({
 *   on: 'insert.text',
 *   actions: [({event}) => [effect(logEvent), forward(event)]],
 * })
 *
 * // Forward to default handling of different event type
 * defineBehavior({
 *   on: 'clipboard.paste',
 *   actions: [
 *     ({event}) => {
 *       const text = event.originEvent.dataTransfer?.getData('text/plain')
 *       return text ? [forward({type: 'insert.text', text})] : []
 *     },
 *   ],
 * })
 * ```
 *
 * @beta
 */
declare function forward(event: NativeBehaviorEvent | SyntheticBehaviorEvent | CustomBehaviorEvent): PickFromUnion<BehaviorAction, 'type', 'forward'>;
/**
 * Raises an event, triggering a fresh lookup of all Behaviors.
 *
 * Use `raise` when you want to trigger an event "from scratch", including all
 * Behaviors that match the event type. This is the appropriate action when you
 * want to trigger Behaviors for a different event type.
 *
 * If no Behavior matches the raised event, synthetic events will fall through
 * to their default operation.
 *
 * @example
 * ```ts
 * // Raise a custom event that triggers other Behaviors
 * defineBehavior({
 *   on: 'insert.text',
 *   guard: ({event}) => event.text === 'a',
 *   actions: [() => [raise({type: 'custom.specialInsert'})]],
 * })
 *
 * // Raise a different event type (fresh lookup includes all Behaviors)
 * defineBehavior({
 *   on: 'clipboard.paste',
 *   actions: [
 *     ({event}) => {
 *       const text = event.originEvent.dataTransfer?.getData('text/plain')
 *       return text ? [raise({type: 'insert.text', text})] : []
 *     },
 *   ],
 * })
 * ```
 *
 * @beta
 */
declare function raise(event: SyntheticBehaviorEvent | CustomBehaviorEvent): PickFromUnion<BehaviorAction, 'type', 'raise'>;
/**
 * Performs a side effect.
 *
 * Use `effect` for logging, analytics, async operations, or other side effects.
 *
 * **Note:** Using `effect` alone (without `forward`) will stop event
 * propagation. To perform a side effect while allowing the default Behavior
 * to continue, combine `effect` with `forward`.
 *
 * The effect callback receives a `send` function that can be used to send
 * events back to the editor asynchronously.
 *
 * @example
 * ```ts
 * // Log events while preserving default Behavior
 * defineBehavior({
 *   on: 'insert.text',
 *   actions: [({event}) => [effect(() => console.log(event)), forward(event)]],
 * })
 *
 * // Effect alone stops propagation (native event is cancelled)
 * defineBehavior({
 *   on: 'keyboard.keydown',
 *   actions: [() => [effect(() => console.log('key pressed'))]],
 * })
 *
 * // Async effect that sends an event later
 * defineBehavior({
 *   on: 'custom.save',
 *   actions: [
 *     () => [
 *       effect(async ({send}) => {
 *         await saveDocument()
 *         send({type: 'custom.saved'})
 *       }),
 *     ],
 *   ],
 * })
 * ```
 *
 * @beta
 */
declare function effect(effect: PickFromUnion<BehaviorAction, 'type', 'effect'>['effect']): PickFromUnion<BehaviorAction, 'type', 'effect'>;
/**
 * @beta
 */
type BehaviorActionSet<TBehaviorEvent, TGuardResponse> = (payload: {
  snapshot: EditorSnapshot;
  event: TBehaviorEvent;
  dom: EditorDom;
}, guardResponse: TGuardResponse) => Array<BehaviorAction>;
export { BlockAnnotationRenderProps as $, BlockPath as $t, PortableTextTextBlock$1 as A, ReadyChange as At, EditorSelector as B, ScrollSelectionIntoViewFunction as Bt, ListDefinition as C, OnPasteResultOrPromise as Ct, PortableTextChild$1 as D, PortableTextMemberSchemaTypes as Dt, PortableTextBlock$1 as E, PatchObservable as Et, BlockOffset as F, RenderDecoratorFunction as Ft, EditorConfig as G, PortableTextEditable as Gt, EditorProvider as H, UndoChange as Ht, useEditor as I, RenderEditableFunction as It, defineBehavior as J, PortableTextEditor as Jt, EditorEvent as K, PortableTextEditableProps as Kt, defaultKeyGenerator as L, RenderListItemFunction as Lt, StyleDefinition as M, RenderAnnotationFunction as Mt, StyleSchemaType as N, RenderBlockFunction as Nt, PortableTextObject$1 as O, RangeDecoration as Ot, defineSchema as P, RenderChildFunction as Pt, AddedAnnotationPaths as Q, AnnotationPath as Qt, usePortableTextEditorSelection as R, RenderPlaceholderFunction as Rt, InlineObjectSchemaType as S, OnPasteResult as St, Patch$1 as T, PatchChange as Tt, EditorProviderProps as U, UnsetChange as Ut, useEditorSelector as V, SelectionChange as Vt, Editor as W, ValueChange as Wt, EditorContext as X, MutationEvent as Xt, BehaviorGuard as Y, EditorEmittedEvent as Yt, EditorSnapshot as Z, EditorSchema as Zt, BlockObjectSchemaType as _, LoadingChange as _t, forward as a, BlurChange as at, FieldDefinition as b, OnCopyFn as bt, CustomBehaviorEvent as c, EditableAPIDeleteOptions as ct, SyntheticBehaviorEvent as d, EditorSelection as dt, ChildPath as en, BlockChildRenderProps as et, PatchesEvent as f, EditorSelectionPoint as ft, BlockObjectDefinition as g, InvalidValueResolution as gt, BaseDefinition as h, InvalidValue as ht, execute as i, BlockStyleRenderProps as it, SchemaDefinition$1 as j, RedoChange as jt, PortableTextSpan$1 as k, RangeDecorationOnMovedDetails as kt, InsertPlacement as l, EditorChange as lt, AnnotationSchemaType as m, FocusChange as mt, BehaviorActionSet as n, Path as nn, BlockListItemRenderProps as nt, raise as o, ConnectionChange as ot, AnnotationDefinition as p, ErrorChange as pt, Behavior as q, HotkeyOptions as qt, effect as r, BlockRenderProps as rt, BehaviorEvent as s, EditableAPI as st, BehaviorAction as t, KeyedSegment as tn, BlockDecoratorRenderProps as tt, NativeBehaviorEvent as u, EditorChanges as ut, DecoratorDefinition as v, MutationChange as vt, ListSchemaType as w, PasteData as wt, InlineObjectDefinition as x, OnPasteFn as xt, DecoratorSchemaType as y, OnBeforeInputFn as yt, usePortableTextEditor as z, RenderStyleFunction as zt };
//# sourceMappingURL=behavior.types.action.d.ts.map