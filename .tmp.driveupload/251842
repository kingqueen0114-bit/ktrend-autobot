import {Path} from '@sanity/types'

declare interface BaseNode {
  path: Path
}

/**
 * Converts a set of markers with paths into a tree of markers where the paths
 * are embedded in the tree
 */
export declare function convertToTree<const Node extends BaseNode>(nodes: Node[]): Tree<Node>

/**
 * Recursively formats a given tree into a printed user-friendly tree structure
 */
export declare const formatTree: <Node extends BaseNode>({
  getMessage,
  getNodes: getLeaves,
  indent,
  node,
  paddingLength,
}: Options<Node>) => string

/**
 * Recursively calculates the max length of all the keys in the given validation
 * tree respecting extra length due to indentation depth. Used to calculate the
 * padding for the rest of the tree.
 */
export declare const maxKeyLength: (
  children?: Record<string, Tree<BaseNode>>,
  depth?: number,
) => number

declare interface Options<Node extends BaseNode> {
  getMessage: (node: Node) => string
  paddingLength: number
  getNodes?: (node: Tree<Node>) => Node[] | undefined
  indent?: string
  node?: Record<string, Tree<Node>>
}

export declare interface Tree<Node extends BaseNode> {
  children?: Record<string, Tree<Node>>
  nodes?: Node[]
}

export {}
