import { $f as DocumentActionDescription, $h as SanityCreateConfigContextValue, $v as AddonDatasetContextValue, Af as MentionUserContextValue, Bt as DocumentFieldActionNode$1, Cb as Locale, Cg as CommentsOnboardingContextValue, DS as TrackerContextGetSnapshot, Df as TasksUpsellContextValue, Dg as CommentsContextValue, E_ as CopyPasteContextType, Ft as DocumentFieldAction$1, IS as ConnectorContextValue, Lg as CommentsUpsellContextValue, Mf as TasksEnabledContextValue, Mg as CommentInputContextValue, OS as TrackerContextStore, Of as TasksContextValue, Pc as FormCallbacksValue, Qg as UpsellDialogViewedInfo, Qr as FormNodePresence, Qs as EnhancedObjectDialogContextValue, Rg as UpsellData, Rn as PortableTextMemberItem, Sd as MetadataWrapper, Sr as FormValueContextValue, Tg as CommentsEnabledContextValue, Wh as UserColorManager, Yo as PortableTextMarker, Yv as StudioColorScheme, Zr as FieldPresenceData, Zy as CommentsAuthoringPathContextValue, _h as EventsStore, ag as AppIdCache, bC as PerspectiveContextValue, by as CommentsSelectedPathContextValue, cp as SchedulesContextValue, dr as FormBuilderContextValue, eu as ZIndexContextValue, gd as ReleasesUpsellContextValue, ip as DocumentActionProps, jy as CommentIntentGetter, kc as ReferenceInputOptions, kf as TasksNavigationContextValue, lv as SearchContextValue, or as VirtualizerScrollInstance, pt as Source$1, rs as FieldCommentsProps, s_ as StudioAnnouncementsContextValue, sy as WorkspacesContextValue, t as ActiveWorkspaceMatcherContextValue, t_ as NavbarContextValue, ui as ResourceCache, vt as Workspace, vy as RouterHistory, wS as ChangeIndicatorTrackerContextValue, zp as DocumentChangeContextInstance, zu as PreviewCardContextValue } from "./_chunks-dts/ActiveWorkspaceMatcherContext.js";
import { C as RouterPanes, N as PaneContextValue, O as StructureToolContextValue, P as PaneLayoutContextValue, i as PaneRouterContextValue, s as DocumentPaneContextValue, v as PaneNode } from "./_chunks-dts/types.js";
import { g as PresentationParamsContextValue, h as PresentationNavigateContextValue, m as PresentationContextValue, v as PresentationPluginOptions } from "./_chunks-dts/types2.js";
import { _ as RouterContextValue } from "./_chunks-dts/types3.js";
import * as react466 from "react";
import { CSSProperties, ComponentType, MutableRefObject, PropsWithChildren, ReactNode, RefObject } from "react";
import { ObjectSchemaType, Path, PortableTextBlock, SanityDocument, ValidationMarker } from "@sanity/types";
import { SanityClient } from "@sanity/client";
import { i18n } from "i18next";
import { BehaviorSubject, Observable } from "rxjs";
import { PubSub } from "nano-pubsub";
import { PortableTextMemberSchemaTypes } from "@portabletext/sanity-bridge";
import { SanityDocument as SanityDocument$2 } from "sanity";
import { SemVer } from "semver";
import { Serializable } from "@sanity/presentation-comlink";
/** @internal */
declare const ActiveWorkspaceMatcherContext: react466.Context<ActiveWorkspaceMatcherContextValue | null>;
/**
 * @beta
 * @hidden
 */
declare const AddonDatasetContext: react466.Context<AddonDatasetContextValue | null>;
/**
 * @internal
 */
declare const AppIdCacheContext: react466.Context<AppIdCache | null>;
/**
 * @internal
 */
interface AssetLimitUpsellContextValue {
  upsellDialogOpen: boolean;
  handleOpenDialog: (source: UpsellDialogViewedInfo['source']) => void;
  upsellData: UpsellData | null;
  telemetryLogs: {
    dialogSecondaryClicked: () => void;
    dialogPrimaryClicked: () => void;
  };
}
/**
 * @internal
 */
declare const AssetLimitUpsellContext: react466.Context<AssetLimitUpsellContextValue | null>;
interface CalendarContextValue {
  date?: Date;
  endDate?: Date;
  focusedDate: Date;
  selectRange?: boolean;
  selectTime?: boolean;
  /**
   * An integer indicating the first day of the week.
   * Can be either 1 (Monday), 6 (Saturday) or 7 (Sunday).
   */
  firstWeekDay: 1 | 6 | 7;
}
/**
 * @internal
 */
declare const CalendarContext: react466.Context<CalendarContextValue | undefined>;
/**
 * @internal
 * @hidden
 */
type ChangeIndicatorTrackerContextStoreType = TrackerContextStore<ChangeIndicatorTrackerContextValue> | null;
/**
 * @internal
 * @hidden
 */
type ChangeIndicatorTrackerGetSnapshotType = TrackerContextGetSnapshot<ChangeIndicatorTrackerContextValue> | null;
/** @internal */
declare const ChangeIndicatorTrackerContextStore: react466.Context<ChangeIndicatorTrackerContextStoreType>;
/** @internal */
declare const ChangeIndicatorTrackerContextGetSnapshot: react466.Context<ChangeIndicatorTrackerGetSnapshotType>;
/**
 * The setter for ColorSchemeValueContext, in a separate context to avoid unnecessary re-renders
 * If set to false then the UI should adjust to reflect that the Studio can't change the color scheme
 * @internal
 */
declare const ColorSchemeSetValueContext: react466.Context<false | ((nextScheme: StudioColorScheme) => void) | null>;
/**
 * Used to keep track of the internal value, which can be "system" in addition to "light" and "dark"
 * @internal
 */
declare const ColorSchemeValueContext: react466.Context<StudioColorScheme | null>;
/**
 * @internal
 */
declare const CommentInputContext: react466.Context<CommentInputContextValue | null>;
/**
 * @beta
 * @hidden
 */
declare const CommentsAuthoringPathContext: react466.Context<CommentsAuthoringPathContextValue | null>;
/**
 * @internal
 */
declare const CommentsContext: react466.Context<CommentsContextValue | null>;
/**
 * @internal
 */
declare const CommentsEnabledContext: react466.Context<CommentsEnabledContextValue>;
/**
 * @internal
 */
declare const CommentsIntentContext: react466.Context<CommentIntentGetter | undefined>;
/**
 * @internal
 */
declare const CommentsOnboardingContext: react466.Context<CommentsOnboardingContextValue | null>;
/**
 * @internal
 */
declare const CommentsSelectedPathContext: react466.Context<CommentsSelectedPathContextValue | null>;
/**
 * @internal
 */
declare const CommentsUpsellContext: react466.Context<CommentsUpsellContextValue | null>;
/**
 * @beta
 * @hidden
 */
declare const CopyPasteContext: react466.Context<CopyPasteContextType | null>;
/**
 * Entry in the dialog stack.
 *
 * @beta
 */
interface DialogStackEntry {
  id: string;
  path?: Path;
}
/**
 * Context value for tracking the dialog stack.
 *
 * @beta
 */
interface DialogStackContextValue {
  /** Stack of dialog entries, last one is the top */
  stack: DialogStackEntry[];
  /** Push a dialog onto the stack */
  push: (id: string, path?: Path) => void;
  /** Remove a dialog from the stack */
  remove: (id: string) => void;
  /** Update the path of an existing dialog entry */
  update: (id: string, path?: Path) => void;
  /** Close dialogs. Pass `{ toParent: true }` to close only the top dialog and navigate to the parent. */
  close: (options?: {
    /**
     * When true, closes only the top dialog and navigates to its parent path.
     * When false or omitted, closes all dialogs and resets to the root path.
     */
    toParent?: boolean;
  }) => void;
  /** Navigate to a specific path, updating the form path and cleaning up stack entries that are at or deeper than the target. */
  navigateTo: (path: Path) => void;
}
/**
 * Context for tracking the stack of open dialogs.
 *
 * @beta
 */
declare const DialogStackContext: react466.Context<DialogStackContextValue | null>;
/** @internal */
declare const DiffContext: react466.Context<{
  path: Path;
}>;
/**
 * @internal
 */
declare const DocumentActionPropsContext: react466.Context<DocumentActionProps | undefined>;
/**
 * @internal
 */
declare const DocumentActionsStateContext: react466.Context<DocumentActionDescription[] | null>;
/** @internal */
declare const DocumentChangeContext: react466.Context<DocumentChangeContextInstance | null>;
/**
 * @internal
 */
interface DocumentFieldActionsContextValue {
  actions: DocumentFieldAction$1[];
}
/**
 * @internal
 */
declare const DocumentFieldActionsContext: react466.Context<DocumentFieldActionsContextValue | null>;
/**
 * @internal
 */
interface DocumentIdContextValue {
  id: string;
}
/**
 * @internal
 */
declare const DocumentIdContext: react466.Context<DocumentIdContextValue | null>;
/**
 * @internal
 */
interface DocumentLimitUpsellContextValue {
  upsellDialogOpen: boolean;
  handleOpenDialog: (source: UpsellDialogViewedInfo['source']) => void;
  handleClose: () => void;
  upsellData: UpsellData | null;
  telemetryLogs: {
    dialogSecondaryClicked: () => void;
    dialogPrimaryClicked: () => void;
    panelPrimaryClicked: () => void;
    panelSecondaryClicked: () => void;
  };
}
/**
 * @internal
 */
declare const DocumentLimitUpsellContext: react466.Context<DocumentLimitUpsellContextValue | null>;
/** @internal */
declare const DocumentPaneContext: react466.Context<DocumentPaneContextValue | null>;
/** @internal */
interface DocumentSheetListContextValue {
  focusAnchorCell: () => void;
  resetFocusSelection: () => void;
  setSelectedAnchorCell: (colId: string, rowIndex: number) => void;
  getStateByCellId: (colId: string, rowIndex: number) => 'focused' | 'selectedAnchor' | 'selectedRange' | null;
  submitFocusedCell: () => void;
}
/** @internal */
declare const DocumentSheetListContext: react466.Context<DocumentSheetListContextValue | undefined>;
/**
 * @internal
 * @deprecated This context is no longer used and will be removed in a future release as we make the enhanced object dialog the default.
 */
declare const EnhancedObjectDialogContext: react466.Context<EnhancedObjectDialogContextValue>;
/**
 * @internal
 */
declare const EventsContext: react466.Context<EventsStore | null>;
/** @internal */
interface FieldActionsContextValue {
  actions: DocumentFieldActionNode$1[];
  __internal_comments?: FieldCommentsProps;
  __internal_slot?: ReactNode;
  focused?: boolean;
  hovered: boolean;
  onMouseEnter: () => void;
  onMouseLeave: () => void;
}
/** @internal */
declare const FieldActionsContext: react466.Context<FieldActionsContextValue>;
/**
 * @internal
 */
declare const FormBuilderContext: react466.Context<FormBuilderContextValue | null>;
/**
 * @internal
 */
declare const FormCallbacksContext: react466.Context<FormCallbacksValue | null>;
/** @internal */
declare const FormFieldPresenceContext: react466.Context<FormNodePresence[]>;
/**
 * @internal
 */
declare const FormValueContext: react466.Context<FormValueContextValue | null>;
interface FreeTrialResponse {
  id: string;
  icon: string;
  style: string;
  showOnLoad: FreeTrialDialog | null;
  showOnClick: FreeTrialDialog | null;
  daysLeft: number;
  totalDays: number;
}
interface FreeTrialDialog {
  _id: string;
  _type: 'dialog';
  _createdAt: string;
  ctaButton?: {
    text: string;
    action: 'openNext' | 'closeDialog' | 'openUrl';
    url?: string;
  };
  secondaryButton?: {
    text: string;
  };
  descriptionText: PortableTextBlock[];
  dialogType: 'modal' | 'popover';
  headingText: string;
  id: string;
  image: Image$1 | null;
  tags?: Tag[];
  _rev: string;
  _updatedAt: string;
}
interface Tag {
  _type: 'tag';
  _key: string;
  tag: string;
}
interface Image$1 {
  asset: {
    url: string;
    altText: string | null;
  };
}
/**
 * @internal
 */
interface FreeTrialContextProps {
  data: FreeTrialResponse | null;
  showDialog: boolean;
  showOnLoad: boolean;
  /**
   * If the user is seeing the `showOnLoad` popover or modal, and clicks on the pricing button the `showOnClick` modal should be triggered.
   */
  toggleShowContent: (closeAndReOpen?: boolean) => void;
}
/**
 * @internal
 */
declare const FreeTrialContext: react466.Context<FreeTrialContextProps | undefined>;
/**
 * Context for tracking fullscreen state of portable text editors by their path
 * @internal
 */
interface FullscreenPTEContextValue {
  /**
   * Get the fullscreen state for a specific path
   */
  getFullscreenPath: (path: Path) => string | undefined;
  /**
   * Set the fullscreen state for a specific path
   */
  setFullscreenPath: (path: Path, isFullscreen: boolean) => void;
  /**
   * Check if any portable text editor is currently in fullscreen mode
   */
  hasAnyFullscreen: () => boolean;
  /**
   * Get all fullscreen paths
   */
  allFullscreenPaths: string[];
}
/**
 * @internal
 */
declare const FullscreenPTEContext: react466.Context<FullscreenPTEContextValue>;
/**
 * @internal
 * @hidden
 */
type GetFormValueContextValue = (path: Path) => unknown;
/**
 * @internal
 */
declare const GetFormValueContext: react466.Context<GetFormValueContextValue | null>;
/** @internal */
interface HoveredFieldContextValue {
  store: {
    subscribe: (onStoreCallback: () => void) => () => void;
    getSnapshot: () => string[];
  };
  onMouseEnter: (path: Path) => void;
  onMouseLeave: (path: Path) => void;
}
/** @internal */
declare const HoveredFieldContext: react466.Context<HoveredFieldContextValue>;
/**
 * TODO: remove this context when alternate document-specific context are
 * introduced.
 *
 * The following context is used in the structure tool to set the active
 * document if it's the last pane open in the structure tool. This is a
 * temporary context provider that was introduced when the comments and tasks
 * plugins were refactor and decoupled from the structure tool. ideally this
 * should be removed and replaced with a document-specific context that gives
 * plugin authors access to what the `usePane`, `usePaneRouter`, and
 * `useDocumentPane` provides without exposing specifics from the structure tool
 */
/**
 * @internal
 */
declare const IsLastPaneContext: react466.Context<boolean>;
/**
 * User application from the API
 * @internal
 */
interface UserApplication {
  id: string;
  type: string;
  projectId?: string;
  organizationId?: string;
  title?: string;
  urlType: 'internal' | 'external';
  appHost: string;
}
/**
 * Cache for user applications fetched from the API.
 * Caches by projectId to avoid duplicate fetches.
 * @internal
 */
interface UserApplicationCache {
  /**
   * Get user applications for a project.
   * Returns cached results if available, otherwise fetches from API.
   */
  get: (client: SanityClient) => Promise<UserApplication[]>;
}
/**
 * @hidden
 * @internal
 */
type LiveUserApplicationContextValue = {
  userApplication: UserApplication | undefined;
  isLoading: boolean;
};
/**
 *
 * @hidden
 * @internal
 */
declare const LiveUserApplicationContext: react466.Context<LiveUserApplicationContextValue>;
/**
 * @internal
 * @hidden
 */
interface LocaleContextValue {
  locales: Locale[];
  currentLocale: Locale;
  __internal: {
    i18next: i18n;
  };
  changeLocale: (newLocale: string) => Promise<void>;
}
/**
 * @internal
 * @hidden
 */
declare const LocaleContext: react466.Context<LocaleContextValue | undefined>;
/** @internal */
type MediaLibraryIds = {
  libraryId: string;
  organizationId: string;
};
/** @internal */
declare const MediaLibraryIdsContext: react466.Context<MediaLibraryIds | null>;
/**
 * @internal
 */
declare const MentionUserContext: react466.Context<MentionUserContextValue | null>;
/** @internal */
declare const NavbarContext: react466.Context<NavbarContextValue>;
/**
 * @hidden
 * @internal
 */
type PackageVersionInfoContextValue = {
  /**
   * Request a new update check
   */
  checkForUpdates: () => void;
  /**
   * Status of version check (i.e. are we currently checking for updates)
   */
  versionCheckStatus: {
    lastCheckedAt: Date | null;
    checking: boolean;
  };
  /**
   * Whether this Studio is configured to be auto-updating
   */
  isAutoUpdating: boolean;
  /**
   * If an importmap for the sanity module exists in the DOM, includes details
   * will be undefined if no importmap is found
   */
  importMapInfo?: {
    valid: false;
    error: Error;
  } | {
    valid: true;
    minVersion: SemVer;
    appId?: string;
  };
  /**
   * What is the version tagged as latest (periodically checked)
   */
  latestTaggedVersion?: SemVer;
  /**
   * What version is the Studio currently running
   */
  currentVersion: SemVer;
  /**
   * What is the current auto-updating version (as periodically resolved via module server and configured via manage)
   */
  autoUpdatingVersion?: SemVer;
};
/**
 *
 * @hidden
 * @internal
 */
declare const PackageVersionInfoContext: react466.Context<PackageVersionInfoContextValue>;
/**
 * @internal
 */
declare const PaneContext: react466.Context<PaneContextValue | null>;
/**
 * @internal
 */
declare const PaneLayoutContext: react466.Context<PaneLayoutContextValue | null>;
/**
 *
 * @hidden
 * @beta
 */
declare const PaneRouterContext: react466.Context<PaneRouterContextValue>;
/**
 *
 * @hidden
 * @beta
 */
declare const PerspectiveContext: react466.Context<PerspectiveContextValue | null>;
/**
 * @internal
 */
declare const PortableTextMarkersContext: react466.Context<PortableTextMarker[]>;
/** @internal */
type PortableTextEditorElement = HTMLDivElement | HTMLSpanElement;
/**
 * @internal
 */
declare const PortableTextMemberItemElementRefsContext: react466.Context<BehaviorSubject<Record<string, PortableTextEditorElement | null | undefined>>>;
/**
 * @internal
 */
declare const PortableTextMemberItemsContext: react466.Context<PortableTextMemberItem[]>;
/**
 * Context for Sanity-specific schema types for Portable Text.
 * This provides access to the full Sanity schema types instead of relying on
 * `editor.schemaTypes` from PTE, which will contain minimal PT schema types
 * when PTE removes its Sanity dependencies.
 *
 * @internal
 */
declare const PortableTextMemberSchemaTypesContext: react466.Context<PortableTextMemberSchemaTypes | null>;
/**
 * @internal
 */
declare const PresenceContext: react466.Context<FormNodePresence[]>;
/**
 * @internal
 * @hidden
 */
type PresenceTrackerContextStoreType = TrackerContextStore<FieldPresenceData> | null;
/**
 * @internal
 * @hidden
 */
type PresenceTrackerGetSnapshotType = TrackerContextGetSnapshot<FieldPresenceData> | null;
/** @internal */
declare const PresenceTrackerContextStore: react466.Context<PresenceTrackerContextStoreType>;
/** @internal */
declare const PresenceTrackerContextGetSnapshot: react466.Context<PresenceTrackerGetSnapshotType>;
/**
 * @internal
 */
declare const PresentationContext: react466.Context<PresentationContextValue | null>;
/** @internal */
type PresentationDisplayedDocumentContextValue = (displayed: Partial<SanityDocument$2> | null | undefined) => void;
/**
 * @internal
 */
declare const PresentationDisplayedDocumentContext: react466.Context<PresentationDisplayedDocumentContextValue | null>;
interface PresentationDocumentContextValue {
  options: PresentationPluginOptions[];
  register: (options: PresentationPluginOptions) => () => void;
}
/**
 * @internal
 */
declare const PresentationDocumentContext: react466.Context<PresentationDocumentContextValue | null>;
/**
 * @internal
 */
declare const PresentationNavigateContext: react466.Context<PresentationNavigateContextValue | null>;
interface PanelElement {
  id: string;
  type: 'panel';
  defaultSize: number | null;
  order: number;
  maxWidth: number | null;
  minWidth: number;
}
interface ResizerElement {
  id: string;
  order: number;
  type: 'resizer';
  el: RefObject<HTMLDivElement | null>;
}
interface PresentationPanelsContextValue {
  activeResizer: string | null;
  drag: (id: string, event: MouseEvent) => void;
  getPanelStyle: (id: string) => React.CSSProperties;
  registerElement: (id: string, panel: PanelElement | ResizerElement) => void;
  startDragging: (id: string, event: MouseEvent) => void;
  stopDragging: () => void;
  unregisterElement: (id: string) => void;
}
/**
 * @internal
 */
declare const PresentationPanelsContext: react466.Context<PresentationPanelsContextValue | null>;
/**
 * @internal
 */
declare const PresentationParamsContext: react466.Context<PresentationParamsContextValue | null>;
interface PresentationSharedStateContextValue {
  removeValue: (key: string) => void;
  setValue: (key: string, value: Serializable) => void;
}
/**
 * @internal
 */
declare const PresentationSharedStateContext: react466.Context<PresentationSharedStateContextValue | null>;
/**
 * @internal
 */
declare const PreviewCardContext: react466.Context<PreviewCardContextValue>;
/**
 * @internal
 */
declare const ReferenceInputOptionsContext: react466.Context<ReferenceInputOptions>;
/**
 * @internal
 */
interface ReferenceItemRef {
  menuRef: MutableRefObject<HTMLDivElement | null>;
  menuButtonRef: MutableRefObject<HTMLButtonElement | null>;
  containerRef: MutableRefObject<HTMLDivElement | null>;
}
/**
 * This is a way to store ref of the menu as well as the container of the ReferenceItem
 * so it can be used down the tree for clickOutside handling
 * @internal
 */
declare const ReferenceItemRefContext: react466.Context<ReferenceItemRef | null>;
/**
 * @internal
 */
interface ReleasesMetadataContextValue {
  state: MetadataWrapper;
  addReleaseIdsToListener: (slugs: string[]) => void;
  removeReleaseIdsFromListener: (slugs: string[]) => void;
}
/**
 * @internal
 * @hidden
 */
declare const ReleasesMetadataContext: react466.Context<ReleasesMetadataContextValue | null>;
type SortDirection = 'asc' | 'desc';
interface TableSort {
  column: string;
  direction: SortDirection;
}
/**
 * @internal
 */
interface TableContextValue {
  searchTerm: string | null;
  setSearchTerm: (searchTerm: string) => void;
  sort: TableSort | null;
  setSortColumn: (column: string) => void;
}
/**
 * @internal
 */
declare const TableContext: react466.Context<TableContextValue | null>;
/**
 * @beta
 * @hidden
 */
declare const ReleasesUpsellContext: react466.Context<ReleasesUpsellContextValue | null>;
declare const LOADING_PANE: unique symbol;
interface PaneData {
  active: boolean;
  childItemId: string | null;
  groupIndex: number;
  index: number;
  itemId: string;
  key: string;
  pane: PaneNode | typeof LOADING_PANE;
  params: Record<string, string | undefined> & {
    perspective?: string;
  };
  path: string;
  payload: unknown;
  selected: boolean;
  siblingIndex: number;
  maximized: boolean;
}
interface Panes {
  paneDataItems: PaneData[];
  routerPanes: RouterPanes;
  resolvedPanes: (PaneNode | typeof LOADING_PANE)[];
  maximizedPane: PaneData | null;
  setMaximizedPane: (pane: PaneData | null) => void;
}
/**
 * @internal
 */
declare const ResolvedPanesContext: react466.Context<Panes | null>;
/**
 * @internal
 */
declare function ResolvedPanesProvider({
  children,
  value
}: {
  children: ReactNode;
  value: Panes;
}): react466.JSX.Element;
/**
 * @internal
 */
declare const ResourceCacheContext: react466.Context<ResourceCache | null>;
/** @internal */
declare const ReviewChangesContext: react466.Context<ConnectorContextValue>;
/**
 * @internal
 */
declare const RouterContext: react466.Context<RouterContextValue | null>;
/**
 * Internal use only. Userland should leverage the public `useRouter` APIs.
 * @internal
 */
declare const RouterHistoryContext: react466.Context<RouterHistory | null>;
/**
 * @internal
 */
declare const SanityCreateConfigContext: react466.Context<SanityCreateConfigContextValue>;
interface HasUsedScheduledPublishing {
  used: boolean;
  loading: boolean;
}
/**
 * @internal
 */
type ScheduledPublishingEnabledContextValue = {
  enabled: false;
  mode: null;
  hasUsedScheduledPublishing: HasUsedScheduledPublishing;
} | {
  enabled: true;
  mode: 'default' | 'upsell';
  hasUsedScheduledPublishing: HasUsedScheduledPublishing;
};
/**
 * @internal
 */
declare const ScheduledPublishingEnabledContext: react466.Context<ScheduledPublishingEnabledContextValue>;
/**
 * @internal
 */
interface SchedulePublishUpsellContextValue {
  upsellDialogOpen: boolean;
  handleOpenDialog: (source: UpsellDialogViewedInfo['source']) => void;
  handleClose: () => void;
  upsellData: UpsellData | null;
  telemetryLogs: {
    dialogSecondaryClicked: () => void;
    dialogPrimaryClicked: () => void;
    panelViewed: (source: UpsellDialogViewedInfo['source']) => void;
    panelDismissed: () => void;
    panelPrimaryClicked: () => void;
    panelSecondaryClicked: () => void;
  };
}
/**
 * @internal
 */
declare const SchedulePublishUpsellContext: react466.Context<SchedulePublishUpsellContextValue>;
/**
 * @deprecated we will be dropping support for scheduled publishing on a future major version
 * @internal
 */
declare const SchedulesContext: react466.Context<SchedulesContextValue | undefined>;
/**
 * @internal
 */
declare const ScrollContext: react466.Context<PubSub<Event> | null>;
/**
 * @internal
 */
declare const SearchContext: react466.Context<SearchContextValue | undefined>;
/**
 * Entry representing a selected annotation for the combined popover
 * @internal
 */
interface AnnotationEntry {
  key: string;
  title: string;
  schemaType: ObjectSchemaType;
  onOpen: () => void;
  onRemove: () => void;
  referenceElement: HTMLElement | null;
}
/**
 * Context value for tracking selected annotations
 * @internal
 */
interface SelectedAnnotationsContextValue {
  register: (entry: AnnotationEntry) => void;
  unregister: (key: string) => void;
  annotations: AnnotationEntry[];
}
/**
 * Context for managing selected annotations in the Portable Text editor.
 * Used by CombinedAnnotationPopover to show all active annotations in a single popover.
 * @internal
 */
declare const SelectedAnnotationsContext: react466.Context<SelectedAnnotationsContextValue | null>;
/**
 * @internal
 */
interface SingleDocReleaseContextValue {
  /**
   * Sets the scheduled draft perspective into the local router params.
   */
  onSetScheduledDraftPerspective: (releaseId: string) => void;
}
/**
 * @internal
 */
declare const SingleDocReleaseContext: react466.Context<SingleDocReleaseContextValue | null>;
/**
 * @internal
 */
type SingleDocReleaseEnabledContextValue = {
  enabled: false;
  mode: null;
} | {
  enabled: true;
  mode: 'default' | 'upsell';
};
/**
 * @internal
 */
declare const SingleDocReleaseEnabledContext: react466.Context<SingleDocReleaseEnabledContextValue>;
/**
 * @internal
 */
interface SingleDocReleaseUpsellContextValue {
  upsellDialogOpen: boolean;
  handleOpenDialog: (source: UpsellDialogViewedInfo['source']) => void;
  handleClose: () => void;
  upsellData: UpsellData | null;
  telemetryLogs: {
    dialogSecondaryClicked: () => void;
    dialogPrimaryClicked: () => void;
    panelViewed: (source: UpsellDialogViewedInfo['source']) => void;
    panelDismissed: () => void;
    panelPrimaryClicked: () => void;
    panelSecondaryClicked: () => void;
  };
}
/**
 * @internal
 */
declare const SingleDocReleaseUpsellContext: react466.Context<SingleDocReleaseUpsellContextValue>;
/**
 * @internal
 */
declare const SortableItemIdContext: react466.Context<string | null>;
/**
 * @internal
 */
declare const SourceContext: react466.Context<Source$1 | null>;
/**
 * @internal
 */
declare const StructureToolContext: react466.Context<StructureToolContextValue | null>;
/**
 * @internal
 */
declare const StudioAnnouncementContext: react466.Context<StudioAnnouncementsContextValue | undefined>;
/**
 * @internal
 */
declare const TasksContext: react466.Context<TasksContextValue | null>;
/**
 * @internal
 */
declare const TasksEnabledContext: react466.Context<TasksEnabledContextValue>;
/**
 * @internal
 */
declare const TasksNavigationContext: react466.Context<TasksNavigationContextValue | null>;
/**
 * @beta
 * @hidden
 */
declare const TasksUpsellContext: react466.Context<TasksUpsellContextValue | null>;
/**
 * @internal
 */
declare const UserApplicationCacheContext: react466.Context<UserApplicationCache | null>;
/**
 * @internal
 */
declare const UserColorManagerContext: react466.Context<UserColorManager | null>;
/**
 * @internal
 */
declare const ValidationContext: react466.Context<ValidationMarker[]>;
/**
 * This is used to store the reference to the scroll element for virtualizer
 * @internal
 */
declare const VirtualizerScrollInstanceContext: react466.Context<VirtualizerScrollInstance | null>;
/**
 * @internal
 */
declare const WorkspaceContext: react466.Context<Workspace | null>;
/** @internal */
declare const WorkspacesContext: react466.Context<WorkspacesContextValue | null>;
/**
 * @internal
 */
declare const zIndexContextDefaults: ZIndexContextValue;
/**
 * TODO: Rename to `ZOffsetsContext`
 *
 * @internal
 */
declare const ZIndexContext: react466.Context<ZIndexContextValue>;
export { ActiveWorkspaceMatcherContext, AddonDatasetContext, AnnotationEntry, AppIdCacheContext, AssetLimitUpsellContext, AssetLimitUpsellContextValue, CalendarContext, ChangeIndicatorTrackerContextGetSnapshot, ChangeIndicatorTrackerContextStore, ColorSchemeSetValueContext, ColorSchemeValueContext, CommentInputContext, CommentsAuthoringPathContext, CommentsContext, CommentsEnabledContext, CommentsIntentContext, CommentsOnboardingContext, CommentsSelectedPathContext, CommentsUpsellContext, CopyPasteContext, DialogStackContext, DialogStackContextValue, DialogStackEntry, DiffContext, DocumentActionPropsContext, DocumentActionsStateContext, DocumentChangeContext, DocumentFieldActionsContext, DocumentFieldActionsContextValue, DocumentIdContext, DocumentIdContextValue, DocumentLimitUpsellContext, DocumentLimitUpsellContextValue, DocumentPaneContext, DocumentSheetListContext, EnhancedObjectDialogContext, EventsContext, FieldActionsContext, FieldActionsContextValue, FormBuilderContext, FormCallbacksContext, FormFieldPresenceContext, FormValueContext, FreeTrialContext, FullscreenPTEContext, GetFormValueContext, GetFormValueContextValue, HoveredFieldContext, HoveredFieldContextValue, IsLastPaneContext, LiveUserApplicationContext, LiveUserApplicationContextValue, LocaleContext, LocaleContextValue, MediaLibraryIdsContext, MentionUserContext, NavbarContext, PackageVersionInfoContext, PackageVersionInfoContextValue, PaneContext, PaneLayoutContext, PaneRouterContext, PerspectiveContext, PortableTextEditorElement, PortableTextMarkersContext, PortableTextMemberItemElementRefsContext, PortableTextMemberItemsContext, PortableTextMemberSchemaTypesContext, PresenceContext, PresenceTrackerContextGetSnapshot, PresenceTrackerContextStore, PresentationContext, PresentationDisplayedDocumentContext, PresentationDocumentContext, PresentationNavigateContext, PresentationPanelsContext, PresentationParamsContext, PresentationSharedStateContext, PreviewCardContext, ReferenceInputOptionsContext, ReferenceItemRef, ReferenceItemRefContext, ReleasesMetadataContext, ReleasesUpsellContext, ResolvedPanesContext, ResolvedPanesProvider, ResourceCacheContext, ReviewChangesContext, RouterContext, RouterHistoryContext, SanityCreateConfigContext, SchedulePublishUpsellContext, SchedulePublishUpsellContextValue, ScheduledPublishingEnabledContext, ScheduledPublishingEnabledContextValue, SchedulesContext, ScrollContext, SearchContext, SelectedAnnotationsContext, SelectedAnnotationsContextValue, SingleDocReleaseContext, SingleDocReleaseContextValue, SingleDocReleaseEnabledContext, SingleDocReleaseEnabledContextValue, SingleDocReleaseUpsellContext, SingleDocReleaseUpsellContextValue, SortableItemIdContext, SourceContext, StructureToolContext, StudioAnnouncementContext, TableContext, TasksContext, TasksEnabledContext, TasksNavigationContext, TasksUpsellContext, UserApplicationCacheContext, UserColorManagerContext, ValidationContext, VirtualizerScrollInstanceContext, WorkspaceContext, WorkspacesContext, ZIndexContext, zIndexContextDefaults };