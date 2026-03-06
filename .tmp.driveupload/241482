import type {Message} from '@sanity/comlink'

/**
 * @public
 */
declare interface ActiveDeployment {
  id: string
  version: string
  isActiveDeployment: boolean
  userApplicationId: string
  isAutoUpdating: boolean
  manifest: ServerManifest | null
  size: number
  deployedAt: string
  deployedBy: string
  createdAt: string
  updatedAt: string
}

/**
 * Context resource data that apps can emit to update the Agent's understanding
 * of what the user is currently interacting with.
 * @public
 */
declare interface AgentResourceContext extends Record<string, unknown> {
  /**
   * The project ID of the current context
   */
  projectId: string
  /**
   * The dataset of the current context
   */
  dataset: string
  /**
   * Optional document ID if the user is viewing/editing a specific document
   */
  documentId?: string
}

/**
 * Message sent from embedded apps to update the Agent's resource context.
 * This allows the Agent to understand what resource the user is currently
 * interacting with (e.g., which document they're editing).
 * @public
 */
declare interface AgentResourceUpdateMessage extends Message {
  type: 'dashboard/v1/events/agent/resource/update'
  data: AgentResourceContext
}

/**
 * @public
 */
export declare type ApplicationResource = Omit<CoreApplication, 'type'> & {
  type: 'application'
  url: string
}

export declare namespace Auth {
  export {Tokens}
}

declare namespace Auth_2 {
  export {Tokens}
}

declare type AutoUpdatingVersion = 'stable' | 'next' | 'lastest' | string

export declare namespace Bridge {
  export {Context, Listeners, Navigation}
}

declare namespace Bridge_2 {
  export {Context, Listeners, Navigation}
}

/**
 * @public
 */
export declare const BRIDGE_CHANNEL_NAME: BridgeChannelName

/**
 * @public
 */
export declare const BRIDGE_NODE_NAME: BridgeNodeName

/**
 * @public
 */
export declare type BridgeChannelName = 'dashboard/channels/bridge'

/**
 * @public
 * @deprecated Use `Context_v1` instead.
 */
declare type BridgeContext = Context_v1

/**
 * @public
 */
export declare type BridgeNodeName = 'dashboard/nodes/bridge'

/**
 * @public
 */
export declare interface CanvasResource {
  id: string
  type: 'canvas'
}

export declare namespace Context {
  export {BridgeContext, ContextMessage}
}

/**
 * @public
 */
export declare interface Context_v1 {
  organizationId: string
  /**
   * Information about the current application
   */
  resource: Resource
  /**
   * All the resources available to the current user
   */
  availableResources: Resource[]
}

/**
 * Message sent from the bridge to fetch
 * the context of the current application
 * @public
 * @deprecated Use `FrameMessages.ContextMessage` instead.
 */
declare interface ContextMessage extends Message {
  type: 'dashboard/v1/bridge/context'
  response: {
    context: BridgeContext
  }
}

/**
 * Message sent to fetch the context of the
 * current application within the dashboard.
 * @public
 */
export declare interface ContextMessage_v1 extends Message {
  type: 'dashboard/v1/context'
  response: {
    context: Context_v1
  }
}

/**
 * Representation of a core applications, both internal & external.
 * @public
 */
export declare type CoreApplication = InternalCoreApplication | ExternalCoreApplication

/**
 * A core application is not tied to a project therefore
 * has no projectId.
 * @public
 */
export declare interface CoreApplicationProperties extends UserApplicationBaseProperties {
  title: string
  organizationId: string
  projectId?: null
  type: 'coreApp'
}

/**
 * Used to fetch a new token for the current application.
 * @public
 */
declare interface CreateTokenMessage extends Message {
  type: 'dashboard/v1/auth/tokens/create'
  response: {
    token: string
  }
}

/**
 * @public
 * A document must have at least an ID and a type.
 * It can also contain additional information about
 * the resource it is associated with.
 */
declare interface DashboardDocumentReference {
  id: string
  type: string
  /**
   * If provided, this will be used to fetch the resource from the API.
   */
  resource?: {
    id: string
    type: Exclude<Resource['type'], 'application'>
    /**
     * If provided, this will be used to fetch the schema from the schema store of the resource.
     * Typically, this is for studios & this name will be the workspace name.
     */
    schemaName?: string
  } | null
}

export declare namespace Document_2 {
  export {DocumentChangeMessage}
}

/**
 * Used to notify the platform that the document metadata has changed.
 * @public
 */
declare interface DocumentChangeMessage extends Message {
  type: 'dashboard/v1/bridge/listeners/document-change'
  data: {
    title: string
  }
  response: {
    success: boolean
  }
}

export declare namespace Events {
  export {
    AgentResourceContext,
    AgentResourceUpdateMessage,
    FavoriteEventType,
    FavoriteMutateMessage,
    FavoriteQueryMessage,
    FavoriteMessage,
    HistoryEventType,
    HistoryMessage,
    DashboardDocumentReference,
  }
}

declare namespace Events_2 {
  export {
    AgentResourceContext,
    AgentResourceUpdateMessage,
    FavoriteEventType,
    FavoriteMutateMessage,
    FavoriteQueryMessage,
    FavoriteMessage,
    HistoryEventType,
    HistoryMessage,
    DashboardDocumentReference,
  }
}

/**
 * Additional properties that make an application considered to be
 * external which is not deployed on sanity infrastructure, it's
 * therefore hosted elsewhere so we have no deployment info.
 * @public
 */
export declare interface ExternalApplicationProperties {
  urlType: 'external'
  activeDeployment: null
}

/**
 * Representation of an external core application.
 * @public
 */
export declare interface ExternalCoreApplication
  extends CoreApplicationProperties, ExternalApplicationProperties {}

/**
 * Representation of an external studio application.
 * @public
 */
export declare interface ExternalStudioApplication
  extends StudioApplicationProperties, ExternalApplicationProperties {}

/**
 * @public
 */
declare type FavoriteEventType = 'added' | 'removed'

/**
 * @public
 */
declare type FavoriteMessage = FavoriteMutateMessage | FavoriteQueryMessage

/**
 * Message to mutate a favorite item (add or remove)
 * @public
 */
declare interface FavoriteMutateMessage extends Message {
  type: 'dashboard/v1/events/favorite/mutate'
  data:
    | {
        eventType: FavoriteEventType
        document: DashboardDocumentReference
        resource?: {
          id?: string
          type?: StudioResource['type']
        }
      }
    | {
        eventType: FavoriteEventType
        document: DashboardDocumentReference
        resource: {
          id: string
          type?: MediaResource['type']
        }
      }
    | {
        eventType: FavoriteEventType
        document: DashboardDocumentReference
        resource: {
          id: string
          type?: CanvasResource['type']
        }
      }
    | {
        eventType: FavoriteEventType
        document: Required<DashboardDocumentReference>
        resource?: {
          id?: string
          type?: ApplicationResource['type']
        }
      }
  response: {
    success: boolean
  }
}

/**
 * Message to get the favorite status of a document
 * @public
 */
declare interface FavoriteQueryMessage extends Message {
  type: 'dashboard/v1/events/favorite/query'
  data:
    | {
        document: DashboardDocumentReference
        resource?: {
          id?: string
          type?: StudioResource['type']
        }
      }
    | {
        document: DashboardDocumentReference
        resource: {
          id: string
          type?: MediaResource['type']
        }
      }
    | {
        document: DashboardDocumentReference
        resource: {
          id: string
          type?: CanvasResource['type']
        }
      }
    | {
        document: Required<DashboardDocumentReference>
        resource?: {
          id?: string
          type?: ApplicationResource['type']
        }
      }
  response: {
    isFavorited: boolean
  }
}

/**
 * @public
 */
export declare type FrameMessages =
  | Bridge_2.Listeners.History.UpdateURLMessage
  | Bridge_2.Listeners.Document.DocumentChangeMessage
  | Bridge_2.Navigation.NavigateToResourceMessage
  | Bridge_2.Context.ContextMessage
  | Events_2.AgentResourceUpdateMessage
  | Events_2.FavoriteMessage
  | Events_2.HistoryMessage
  | ContextMessage_v1
  | Auth_2.Tokens.CreateTokenMessage

export declare namespace History_2 {
  export {UpdateURLMessage}
}

/**
 * @public
 */
declare type HistoryEventType = 'viewed' | 'edited' | 'created' | 'deleted'

/**
 * @public
 */
declare interface HistoryMessage extends Message {
  type: 'dashboard/v1/events/history'
  data:
    | {
        eventType: HistoryEventType
        document: DashboardDocumentReference
        resource?: {
          id?: string
          type?: StudioResource['type']
        }
      }
    | {
        eventType: HistoryEventType
        document: DashboardDocumentReference
        resource: {
          id: string
          type?: MediaResource['type']
        }
      }
    | {
        eventType: HistoryEventType
        document: DashboardDocumentReference
        resource: {
          id: string
          type?: CanvasResource['type']
        }
      }
    | {
        eventType: HistoryEventType
        document: Required<DashboardDocumentReference>
        resource?: {
          id?: string
          type?: ApplicationResource['type']
        }
      }
}

/**
 * Additional properties that make an application considered
 * to be internal which is deployed on sanity infrastructure.
 * @public
 */
export declare interface InternalApplicationProperties {
  urlType: 'internal'
  activeDeployment: ActiveDeployment | null
}

/**
 * Representation of an internal core application.
 * @public
 */
export declare interface InternalCoreApplication
  extends CoreApplicationProperties, InternalApplicationProperties {}

/**
 * Representation of an internal studio application.
 * @public
 */
export declare interface InternalStudioApplication
  extends StudioApplicationProperties, InternalApplicationProperties {}

export declare namespace Listeners {
  export {Document_2 as Document, History_2 as History}
}

/**
 * @public
 */
export declare interface MediaResource {
  id: string
  type: 'media-library'
}

/**
 * Used to navigate the platform to a new URL.
 * @public
 */
declare interface NavigateToResourceMessage extends Message {
  type: 'dashboard/v1/bridge/navigate-to-resource'
  data: {
    /**
     * Resource ID
     */
    resourceId: string
    /**
     * Resource type
     * @example 'application' | 'studio'
     */
    resourceType: string
    /**
     * Path within the resource to navigate to.
     */
    path?: string
  }
}

export declare namespace Navigation {
  export {NavigateToResourceMessage}
}

/**
 * @public
 */
export declare interface PathChangeMessage extends Message {
  type: 'dashboard/v1/history/change-path'
  data: {
    path: string
    type: 'push' | 'pop' | 'replace'
  }
}

/**
 * @public
 */
export declare type Resource = StudioResource | ApplicationResource | MediaResource | CanvasResource

/**
 * @public
 */
export declare const SDK_CHANNEL_NAME: SDKChannelName

/**
 * @public
 */
export declare const SDK_NODE_NAME: SDKNodeName

/**
 * @public
 */
export declare type SDKChannelName = 'dashboard/channels/sdk'

/**
 * @public
 */
export declare type SDKNodeName = 'dashboard/nodes/sdk'

/**
 * @public
 */
export declare interface ServerManifest {
  buildId?: string
  bundleVersion?: string
  version?: string
  workspaces?: Array<WorkspaceServerManifest>
}

/**
 * Representation of a studio applications, both internal & external.
 * @public
 */
export declare type StudioApplication = InternalStudioApplication | ExternalStudioApplication

/**
 * A studio application always has a projectId
 * and is of type 'studio'.
 * @public
 */
export declare interface StudioApplicationProperties extends UserApplicationBaseProperties {
  title: null
  organizationId?: null
  projectId: string
  type: 'studio'
  manifest: null | StudioManifest
  autoUpdatingVersion: AutoUpdatingVersion | null
  config: {
    'live-manifest'?: {
      createdAt: string
      updatedAt: string
      updatedBy: string
      value: ServerManifest
    }
  }
}

/**
 * @public
 */
export declare type StudioManifest = StudioManifestV2 | StudioManifestV3

/**
 * @public
 */
declare interface StudioManifestCommon {
  version: number
  createdAt: string
  workspaces: WorkspaceManifest[]
}

/**
 * @public
 */
declare interface StudioManifestV2 extends StudioManifestCommon {
  version: 2
}

/**
 * @public
 */
declare interface StudioManifestV3 extends StudioManifestCommon {
  studioVersion: string
  version: 3
}

/**
 * @public
 */
export declare type StudioResource = Pick<
  StudioApplication,
  | 'projectId'
  | 'updatedAt'
  | 'urlType'
  | 'activeDeployment'
  | 'dashboardStatus'
  | 'autoUpdatingVersion'
  | 'manifest'
  | 'config'
> & {
  title: string
  id: string
  basePath: string
  dataset?: string
  href: string
  icon?: string | null
  name: string
  subtitle?: string | null
  url: string
  userApplicationId: string
  type: 'studio'
  hasManifest: boolean
  hasSchema: boolean
  version?: string
}

export declare namespace Tokens {
  export {CreateTokenMessage}
}

/**
 * Used to notify the platform that the URL has changed.
 * @public
 */
declare interface UpdateURLMessage extends Message {
  type: 'dashboard/v1/bridge/listeners/history/update-url'
  data: {
    url: string
  }
  response: {
    success: boolean
  }
}

/**
 * Representation of a user application, both studio & core.
 * @public
 */
export declare type UserApplication = StudioApplication | CoreApplication

/**
 * any user-application share a set of
 * properties which this interface describes.
 *  @public
 */
export declare interface UserApplicationBaseProperties {
  id: string
  appHost: string
  createdAt: string
  updatedAt: string
  dashboardStatus: 'default' | 'disabled'
}

/**
 * @public
 */
export declare type WindowMessages = PathChangeMessage

/**
 * @public
 */
export declare interface WorkspaceManifest {
  name: string
  title: string
  subtitle?: string | null
  basePath: string
  projectId: string
  dataset: string
  icon?: string | null
  schema: string
  tools?: string
}

/**
 * @public
 */
export declare interface WorkspaceServerManifest extends Pick<
  WorkspaceManifest,
  'icon' | 'name' | 'title' | 'dataset' | 'basePath' | 'projectId'
> {
  schemaDescriptorId: string
}

export {}
