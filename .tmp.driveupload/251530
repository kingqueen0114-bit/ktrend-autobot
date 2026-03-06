import {ClientConfig} from '@sanity/client'
import {Command} from '@oclif/core'
import {ConfigEnv} from 'vite'
import ConfigStore from 'configstore'
import {ConsentStatus} from '@sanity/telemetry'
import {Debugger} from 'debug'
import debugIt from 'debug'
import {InlineConfig} from 'vite'
import {Interfaces} from '@oclif/core'
import {PluginOptions} from 'babel-plugin-react-compiler'
import {SanityClient} from '@sanity/client'
import {TelemetryEvent} from '@sanity/telemetry'
import {TelemetryLogger} from '@sanity/telemetry'
import {URL as URL_2} from 'node:url'
import {Worker as Worker_2} from 'node:worker_threads'
import {WorkerOptions as WorkerOptions_2} from 'node:worker_threads'
import {Workspace} from 'sanity'
import * as z from 'zod'
import {z as z_2} from 'zod'

declare type Args<T extends typeof Command> = Interfaces.InferredArgs<T['args']>

/**
 * Clears the global CLI telemetry store.
 * @internal
 */
export declare function clearCliTelemetry(): void

/**
 * @public
 * Symbol used to store the CLI telemetry store on globalThis.
 * Use `getCliTelemetry()` to access the store instead of accessing this directly.
 */
export declare const CLI_TELEMETRY_SYMBOL: unique symbol

/**
 * @public
 */
export declare interface CliConfig {
  /** The project ID and dataset the Sanity CLI should use to run its commands */
  api?: {
    dataset?: string
    projectId?: string
  }
  /** Configuration for custom Sanity apps built with the App SDK */
  app?: {
    /** The entrypoint for your custom app. By default, `src/App.tsx` */
    entry?: string
    /** String encoding of an icon (typically an SVG) */
    icon?: string
    /** @deprecated Use deployment.appId */
    id?: string
    /** The ID for the Sanity organization that manages this application */
    organizationId?: string
    /** The title of the custom app. Used in Dashboard and in the browser tab */
    title?: string
  }
  /** @deprecated Use deployment.autoUpdates */
  autoUpdates?: boolean
  /** Options for custom app and Studio deployments */
  deployment?: {
    /**
     * The ID for your custom app or Studio. Generated when deploying your app or Studio for the first time.
     * Get your app ID by either:
     * 1. Checking the output of `sanity deploy`, or
     * 2. Checking your project’s Studio tab at https://sanity.io/manage
     *
     * @remarks This is required for all custom app deployments, and for Studios opting in to fine grained version control.
     * {@link https://www.sanity.io/docs/studio/latest-version-of-sanity#k0896ed4574b7}
     */
    appId?: string
    /**
     * Enable automatic updates for your Studio or custom app’s Sanity dependencies.
     * {@link https://www.sanity.io/docs/studio/latest-version-of-sanity}
     */
    autoUpdates?: boolean
  }
  /** Define the GraphQL APIs that the CLI can deploy and interact with */
  graphql?: Array<{
    filterSuffix?: string
    generation?: 'gen1' | 'gen2' | 'gen3'
    id?: string
    nonNullDocumentFields?: boolean
    playground?: boolean
    source?: string
    tag?: string
    workspace?: string
  }>
  /** Configuration for the Media Library */
  mediaLibrary?: {
    /** The path to the Media Library aspects directory. When using the CLI to manage aspects, this is the directory they will be read from and written to. */
    aspectsPath?: string
  }
  /** Contains the property `basePath` which lets you change the top-level slug for the Studio. You typically need to set this if you embed the Studio in another application where it is one of many routes. Defaults to an empty string. */
  project?: {
    basePath?: string
  }
  /** Configuration options for React Compiler */
  reactCompiler?: PluginOptions
  /** Wraps the Studio in \<React.StrictMode\> root to aid in flagging potential problems related to concurrent features (startTransition, useTransition, useDeferredValue, Suspense). Can also be enabled by setting SANITY_STUDIO_REACT_STRICT_MODE="true"|"false". It only applies to sanity dev in development mode and is ignored in sanity build and in production. Defaults to false. */
  reactStrictMode?: boolean
  /**
   * Configuration for schema extraction (`sanity schema extract`)
   */
  schemaExtraction?: {
    /**
     * When true, schema fields marked as required will be non-optional in the output.
     * Defaults to `false`
     */
    enforceRequiredFields?: boolean
    /**
     * Output path for the extracted schema file.
     * Defaults to `schema.json` in the working directory.
     */
    path?: string
    /**
     * Additional glob patterns to watch for schema changes in watch mode.
     * These extend the default patterns:
     * - `sanity.config.{js,jsx,ts,tsx,mjs}`
     * - `schema*\/**\/*.{js,jsx,ts,tsx,mjs}`
     */
    watchPatterns?: string[]
    /**
     * The name of the workspace to generate a schema for. Required if your Sanity project has more than one
     * workspace.
     */
    workspace?: string
  }
  /** Defines the hostname and port that the development server should run on. hostname defaults to localhost, and port to 3333. */
  server?: {
    hostname?: string
    port?: number
  }
  /** @deprecated Use deployment.appId */
  studioHost?: string
  /**
   * Configuration for Sanity typegen
   */
  typegen?: Partial<TypeGenConfig>
  /** Exposes the default Vite configuration for custom apps and the Studio so it can be changed and extended. */
  vite?: UserViteConfig
}

/**
 * @public
 */
export declare type CLITelemetryStore = TelemetryLogger<TelemetryUserProperties>

/**
 * The CLI user configuration schema.
 *
 * @internal
 */
declare type CliUserConfig = z_2.infer<z_2.ZodObject<typeof cliUserConfigSchema>>

declare const cliUserConfigSchema: {
  authToken: z_2.ZodOptional<z_2.ZodString>
  telemetryConsent: z_2.ZodOptional<
    z_2.ZodObject<
      {
        updatedAt: z_2.ZodOptional<z_2.ZodNumber>
        value: z_2.ZodObject<
          {
            status: z_2.ZodEnum<{
              undetermined: 'undetermined'
              unset: 'unset'
              granted: 'granted'
              denied: 'denied'
            }>
            type: z_2.ZodString
          },
          z_2.core.$loose
        >
      },
      z_2.core.$strip
    >
  >
}

export declare function colorizeJson(input: unknown): string

/**
 * @internal
 */
declare const configDefinition: z.ZodObject<
  {
    formatGeneratedCode: z.ZodDefault<z.ZodBoolean>
    generates: z.ZodDefault<z.ZodString>
    overloadClientMethods: z.ZodDefault<z.ZodBoolean>
    path: z.ZodDefault<z.ZodUnion<[z.ZodString, z.ZodArray<z.ZodString>]>>
    schema: z.ZodDefault<z.ZodString>
  },
  z.core.$strip
>

export declare type ConsentInformation =
  | {
      reason: 'fetchError' | 'unauthenticated'
      status: Extract<ConsentStatus, 'undetermined'>
    }
  | {
      reason?: 'localOverride'
      status: Extract<ConsentStatus, 'denied'>
    }
  | {
      reason?: never
      status: Extract<ConsentStatus, 'granted'>
    }
  | {
      reason?: never
      status: Extract<ConsentStatus, 'unset'>
    }

/**
 * Create a config in the provided config store that expires after the provided TTL.
 */
export declare function createExpiringConfig<Type>({
  fetchValue,
  key,
  onCacheHit,
  onFetch,
  onRevalidate,
  store,
  ttl,
  validateValue,
}: ExpiringConfigOptions<Type>): ExpiringConfigApi<Type>

/**
 * Creates a new worker for a studio worker task.
 *
 * This uses a combination of vite for "bundling" + jsdom for emulating a browser
 * environment under the hood, which means that the same thing that will work in vite
 * _should_ work in the worker - to a degree. If the user has defined any typescript
 * path aliases, these will have to be added as aliases to the vite config - the same
 * behavior as you would see with regular vite. Other things that are accounted for:
 *
 * - TypeScript support (+JSX, enums and other "compilation needed" features)
 * - CSS, font and other file imports will resolve to a file path
 * - CSS module imports will resolve to a javascript object of class names
 * - Environment variables are available both as `import.meta.env` and `process.env`,
 *   and `.env` files are loaded in the same way that they would in a Sanity studio.
 * - Browser globals not available in a Node.js environment but _are_ provided by JSDOM
 *   are defined directly to the Node environment as globals. While this polutes the
 *   global namespace, it is done only in the worker thread.
 * - Certain browser globals that are _not_ available in JSDOM are also provided to the
 *   global namespace - things like `requestIdleCallback`, `IntersectionObserver` etc.
 *   These are provided with a minimal stub implementation to make them not crash.
 *
 * @param filePath - Path to the worker file (`.ts` works and is encouraged)
 * @param options - Options to pass to the worker
 * @returns A promise that resolves with the message from the worker
 * @throws If the file does not exist
 * @throws If the worker exits with a non-zero code
 * @internal
 */
export declare function createStudioWorker(
  filePath: URL,
  options: StudioWorkerTaskOptions,
): Worker_2

/**
 * Creates a file-based telemetry store with cached consent and reliable synchronous I/O.
 *
 * Key optimizations:
 * - Consent resolved once at creation and cached (vs checking on every emit)
 * - File path generated and directory created once during initialization
 * - Synchronous file writes to ensure events are captured even during process exit
 *
 * @param sessionId - Unique session identifier for file isolation
 * @param options - Configuration options
 * @returns TelemetryStore instance compatible with the telemetry interface
 *
 * @internal
 */
export declare function createTelemetryStore(
  sessionId: string,
  options: CreateTelemetryStoreOptions,
): CLITelemetryStore

/**
 * FILE MANAGEMENT STRATEGY:
 *
 * The telemetry system uses a multi-file approach to handle concurrent CLI processes:
 *
 * 1. WRITING (per session):
 *    - Each CLI session gets a unique file: telemetry-\{hash\}-\{env\}-\{sessionId\}.ndjson
 *    - Prevents write conflicts when multiple CLI commands run simultaneously
 *    - Events are written using an RxJS queue for ordered processing with retry logic
 *
 * 2. FLUSHING (aggregate all sessions):
 *    - findTelemetryFiles() discovers ALL telemetry files for user/environment
 *    - Events are collected from all session files and sent as a batch
 *    - Files are deleted after successful transmission
 *
 * 3. CLEANUP (background maintenance):
 *    - cleanupOldTelemetryFiles() removes stale files older than 7 days
 *    - Prevents disk space accumulation from abandoned sessions
 */
declare interface CreateTelemetryStoreOptions {
  resolveConsent: () => Promise<ConsentInformation>
}

/**
 * `debug` instance for the CLI
 *
 * @internal
 */
declare const debug_2: debugIt.Debugger
export {debug_2 as debug}

/**
 * This function is a replacement for built in dynamic import
 * This handles the case for windows file paths especially for absolute paths.
 *
 * @param source - File path
 */
export declare function doImport(source: string): Promise<any>

export declare interface ExpiringConfigApi<Type> {
  /**
   * Delete the cached value.
   */
  delete: () => void
  /**
   * Attempt to get the cached value. If there is no cached value, or the cached value has expired,
   * fetch, cache, and return the value.
   */
  get: () => Promise<Type>
}

export declare interface ExpiringConfigOptions<Type> {
  /** Fetch value */
  fetchValue: () => Promise<Type> | Type
  /** Config key */
  key: string
  /** Config store */
  store: ConfigStore
  /** TTL (milliseconds) */
  ttl: number
  /** Subscribe to cache hit event */
  onCacheHit?: () => void
  /** Subscribe to fetch event */
  onFetch?: () => void
  /** Subscribe to revalidate event */
  onRevalidate?: () => void
  /**
   * Assert the fetched value is valid, or throw if invalid.
   * If none is provided, it will always accept the fetched value.
   */
  validateValue?: (value: unknown) => value is Type
}

/**
 * Checks if a file exists and can be "accessed".
 * Prone to race conditions, but good enough for our use cases.
 *
 * @param filePath - The path to the file to check
 * @returns A promise that resolves to true if the file exists, false otherwise
 * @internal
 */
export declare function fileExists(filePath: string): Promise<boolean>

/**
 * Finds the path for a given set of files.
 *
 * @param basePath - The base path to search for files.
 * @param files - The files to search for.
 * @internal
 */
export declare function findPathForFiles(basePath: string, files: string[]): Promise<PathResult[]>

/**
 * Resolve project root directory and type.
 *
 * Project root is:
 * - `studio` - A pre-blueprints Sanity studio root (containing `sanity.config.(ts|js)`)
 * - `app` - A Sanity app root (containing `sanity.cli.(ts|js)`)
 *
 * If a Sanity Studio v2/v1 root is found (containing `sanity.json` with `root: true`),
 * an error is thrown, as v2/v1 is no longer supported.
 *
 * @internal
 */
export declare function findProjectRoot(cwd: string): Promise<ProjectRootResult>

/**
 * Resolve project root directory and type synchronously.
 *
 * Project root is:
 * - `studio` - A pre-blueprints Sanity studio root (containing `sanity.config.(ts|js)`)
 * - `app` - A Sanity app root (containing `sanity.cli.(ts|js)`)
 *
 * If a Sanity Studio v2/v1 root is found (containing `sanity.json` with `root: true`),
 * an error is thrown, as v2/v1 is no longer supported.
 *
 * @param cwd - Current working directory to start searching from
 * @returns Project root result
 * @internal
 */
export declare function findProjectRootSync(cwd: string): ProjectRootResult

/**
 * Resolves to a string containing the found config path, otherwise throws an error.
 * Also throws if Sanity v2 studio root is found.
 *
 * @param basePath - The base path to start searching from
 * @returns A promise that resolves to a string containing the found config path
 * @throws On multiple config files found, if v2 studio root found, or no config found
 * @internal
 */
export declare function findStudioConfigPath(basePath: string): Promise<string>

declare type Flags<T extends typeof Command> = Interfaces.InferredFlags<
  (typeof SanityCommand)['baseFlags'] & T['flags']
>

/**
 * Standalone, stateless function to flush telemetry files.
 *
 * This function can be used independently of the telemetry store, making it
 * suitable for use in child processes or other contexts where store state
 * is not available.
 *
 * @param options - Configuration for consent resolution and event sending
 * @returns Promise that resolves when flush operation is complete
 *
 * @internal
 */
export declare function flushTelemetryFiles(options: FlushTelemetryFilesOptions): Promise<void>

declare interface FlushTelemetryFilesOptions {
  resolveConsent: () => Promise<ConsentInformation>
  sendEvents: (events: TelemetryEvent[]) => Promise<void>
}

export declare function formatObject(obj: unknown): string

/**
 * Get the CLI config for a project, given the root path.
 *
 * We really want to avoid loading the CLI config in the main thread, as we'll need
 * TypeScript loading logic, potentially with ts path aliases, syntax extensions and all
 * sorts of nonsense. Thus, we _attempt_ to use a worker thread - but have to fall back
 * to using the main thread if not possible. This can be the case if the configuration
 * contains non-serializable properties, such as functions. This is unfortunately used
 * by the vite config, for example.
 *
 * @param rootPath - Root path for the project, eg where `sanity.cli.(ts|js)` is located.
 * @returns The CLI config
 * @internal
 */
export declare function getCliConfig(rootPath: string): Promise<CliConfig>

/**
 * Get the CLI config for a project synchronously, given the root path.
 *
 * This loads the CLI config in the main thread using tsx/register for TypeScript support.
 * Note: This is a synchronous operation and does not use worker threads like the async version.
 *
 * @param rootPath - Root path for the project, eg where `sanity.cli.(ts|js)` is located.
 * @returns The CLI config
 * @internal
 */
export declare function getCliConfigSync(rootPath: string): CliConfig

/**
 * @public
 */
export declare function getCliTelemetry(): CLITelemetryStore

/**
 * Get the CLI authentication token from the environment or the config file
 *
 * @returns A promise that resolves to a CLI token, or undefined if no token is found
 * @internal
 */
export declare function getCliToken(): Promise<string | undefined>

/**
 * Get the config value for the given property
 *
 * @param prop - The property to get the value for
 * @returns The value of the given property
 * @internal
 */
export declare function getConfig<P extends keyof CliUserConfig>(prop: P): Promise<CliUserConfig[P]>

export declare function getEmptyAuth(): {
  authenticated: boolean
  client: SanityClient
  currentUser: null
}

/**
 * Create a "global" (unscoped) Sanity API client.
 *
 * @public
 *
 * @param options - The options to use for the client.
 * @returns Promise that resolves to a configured Sanity API client.
 */
export declare function getGlobalCliClient({
  requireUser,
  token: providedToken,
  ...config
}: GlobalCliClientOptions): Promise<SanityClient>

/**
 * Create a "project" (scoped) Sanity API client.
 *
 * @public
 *
 * @param options - The options to use for the client.
 * @returns Promise that resolves to a configured Sanity API client.
 */
export declare function getProjectCliClient({
  requireUser,
  token: providedToken,
  ...config
}: ProjectCliClientOptions): Promise<SanityClient>

/**
 * Gets an environment variable with the appropriate Sanity prefix based on whether it's an app or studio.
 *
 * @param suffix - The suffix for the environment variable (e.g., 'SERVER_HOSTNAME')
 * @param isApp - Whether to use the app prefix (SANITY_APP_) or studio prefix (SANITY_STUDIO_)
 * @returns The value of the environment variable, or undefined if not set
 *
 * @example
 * ```ts
 * // For studio: SANITY_STUDIO_SERVER_HOSTNAME
 * const studioHostname = getSanityEnvVar('SERVER_HOSTNAME', false)
 *
 * // For app: SANITY_APP_SERVER_HOSTNAME
 * const appHostname = getSanityEnvVar('SERVER_HOSTNAME', true)
 * ```
 *
 * @internal
 */
export declare function getSanityEnvVar(suffix: string, isApp: boolean): string | undefined

/**
 * @internal
 * @returns The domain for sanity depending on the environment
 */
export declare function getSanityUrl(): 'https://www.sanity.work' | 'https://www.sanity.io'

/**
 * Get the studio config for a project, given the root path.
 *
 * @param rootPath - The root path for the project
 * @returns The studio config (some properties may be missing)
 * @public
 */
export declare function getStudioConfig(
  rootPath: string,
  options: {
    resolvePlugins: true
  },
): Promise<ResolvedStudioConfig>

export declare function getStudioConfig(
  rootPath: string,
  options: {
    resolvePlugins: false
  },
): Promise<RawStudioConfig>

/**
 * Resolves the workspaces from the studio config.
 *
 * NOTE: This function should only be called from a worker thread.
 *
 * @param configPath - The path to the studio config
 * @returns The workspaces
 * @internal
 */
export declare function getStudioWorkspaces(configPath: string): Promise<Workspace[]>

/**
 * Gets the base telemetry information needed for file operations.
 *
 * This shared utility extracts common logic used by:
 * - `generateTelemetryFilePath` - for generating session-specific file paths
 * - `findTelemetryFiles` - for discovering all telemetry files via glob patterns
 *
 * @returns Promise resolving to base telemetry information
 * @throws Error if no auth token is found
 * @internal
 */
export declare function getTelemetryBaseInfo(): Promise<TelemetryBaseInfo>

/**
 * Starts a terminal timer
 *
 * @internal
 */
export declare function getTimer(): TimeMeasurer

export declare const getUserConfig: () => ConfigStore

/**
 * @public
 */
export declare interface GlobalCliClientOptions extends ClientConfig {
  /**
   * The API version to use for this client.
   */
  apiVersion: string
  /**
   * Whether to require a user to be authenticated to use this client.
   * Default: `false`.
   * Throws an error if `true` and user is not authenticated.
   */
  requireUser?: boolean
}

/**
 * Imports a module using jiti and returns its exports.
 * This is a thin wrapper around tsx to allow swapping out the underlying implementation in the future if needed.
 *
 * @param filePath - Path to the module to import.
 * @param options - Options for the importModule function.
 * @returns The exported module.
 *
 * @internal
 */
export declare function importModule<T = unknown>(
  filePath: string | URL,
  options?: ImportModuleOptions,
): Promise<T>

declare interface ImportModuleOptions {
  /**
   * Whether to return the default export of the module.
   */
  default?: true
  /**
   * Path to the tsconfig file to use for the import. If not provided, the tsconfig
   * will be inferred from the nearest `tsconfig.json` file.
   */
  tsconfigPath?: string
}

export declare const isCi: () => boolean

export declare function isInteractive(): boolean

/**
 * Checks if the given value is a record (javascript objectish)
 *
 * @param value - Value to check
 * @returns True if the value is a record, false otherwise
 * @internal
 */
export declare function isRecord(value: unknown): value is Record<string, unknown>

/**
 * Checks if the environment is staging.
 *
 * @returns True if the environment is staging, false otherwise
 * @internal
 */
export declare function isStaging(): boolean

export declare function isTrueish(value: string | undefined): boolean

/**
 * Mocks a browser-like environment for processes in the main thread by:
 * - Injecting browser globals (window, document, ResizeObserver, etc.)
 * - Loading studio environment variables from the project's sanity installation into process.env
 *
 * This is useful for commands like `sanity exec` that have to run user scripts
 * in the main thread of the process (but in a child process).
 *
 * Be cautious when using this, since it will pollute the global namespace with browser globals.
 *
 * If your code can run in a worker thread, you should use the `studioWorkerTask` function instead.
 *
 * @param basePath - The root path of the Sanity Studio project
 * @returns A cleanup function that removes the injected globals and environment variables
 * @internal
 */
export declare function mockBrowserEnvironment(basePath: string): Promise<() => void>

/**
 * Normalizes a path for cross-platform comparison by converting backslashes to forward slashes.
 * Useful for converting windows paths to unix paths.
 *
 * @param path - Path to normalize
 * @returns Normalized path with forward slashes
 * @public
 */
export declare function normalizePath(path: string): string

export declare interface Output {
  error: Command['error']
  log: Command['log']
  warn: Command['warn']
}

/**
 * Comprehensive representation of a package.json file.
 * Consolidates all properties from previous type definitions.
 *
 * @public
 */
export declare type PackageJson = z_2.infer<typeof packageJsonSchema>

/**
 * Comprehensive package.json schema including all common properties.
 * Feel free to add properties to this,
 * 🟠ℹ️   BUT ENSURE OPTIONAL STUFF IS ACTUALLY OPTIONAL  ℹ️🟠
 * 🟠ℹ️ SINCE THIS IS USED IN A NUMBER OF LOCATIONS WHERE ℹ️🟠
 * 🟠ℹ️ WE CANNOT ENFORCE/GUARANTEE ANY PARTICULAR PROPS  ℹ️🟠
 */
declare const packageJsonSchema: z_2.ZodObject<
  {
    name: z_2.ZodString
    version: z_2.ZodString
    dependencies: z_2.ZodOptional<z_2.ZodRecord<z_2.ZodString, z_2.ZodString>>
    devDependencies: z_2.ZodOptional<z_2.ZodRecord<z_2.ZodString, z_2.ZodString>>
    peerDependencies: z_2.ZodOptional<z_2.ZodRecord<z_2.ZodString, z_2.ZodString>>
    exports: z_2.ZodOptional<z_2.ZodRecord<z_2.ZodString, z_2.ZodAny>>
    main: z_2.ZodOptional<z_2.ZodString>
    types: z_2.ZodOptional<z_2.ZodString>
    author: z_2.ZodOptional<z_2.ZodString>
    description: z_2.ZodOptional<z_2.ZodString>
    engines: z_2.ZodOptional<z_2.ZodRecord<z_2.ZodString, z_2.ZodString>>
    license: z_2.ZodOptional<z_2.ZodString>
    private: z_2.ZodOptional<z_2.ZodBoolean>
    repository: z_2.ZodOptional<
      z_2.ZodObject<
        {
          type: z_2.ZodString
          url: z_2.ZodString
        },
        z_2.core.$strip
      >
    >
    scripts: z_2.ZodOptional<z_2.ZodRecord<z_2.ZodString, z_2.ZodString>>
  },
  z_2.core.$loose
>

/**
 * Parses an optional string flag from oclif.
 * If the input is undefined, return undefined
 * but if the input is empty, throw an error.
 *
 *
 * @param input - The input to parse
 * Throws an error if the input is empty
 */
export declare function parseStringFlag(
  flagName: string,
  input?: string,
): Promise<string | undefined>

/**
 * @internal
 */
declare interface PathResult {
  exists: boolean
  path: string
}

export declare function printKeyValue(obj: Record<string, unknown>): void

/**
 * @public
 */
export declare interface ProjectCliClientOptions extends ClientConfig {
  /**
   * The API version to use for this client.
   */
  apiVersion: string
  /**
   * The project ID to use for this client.
   */
  projectId: string
  /**
   * The dataset to use for this client.
   */
  dataset?: string
  /**
   * Whether to require a user to be authenticated to use this client.
   * Default: `false`.
   * Throws an error if `true` and user is not authenticated.
   */
  requireUser?: boolean
}

/**
 * Result of finding a project configuration
 *
 * @public
 */
export declare interface ProjectRootResult {
  directory: string
  /**
   * Path to the project configuration file, if found.
   */
  path: string
  /**
   * Type of project root.
   */
  type: 'app' | 'studio'
}

/**
 * Wraps a Node.js Worker in a Promise that resolves with the first message
 * the worker sends, and rejects on error, message deserialization failure,
 * or non-zero exit code. The worker is terminated after a message or error
 * is received.
 *
 * @param worker - The Worker instance to promisify
 * @returns A promise that resolves with the first message from the worker
 * @throws If the worker emits an error, a message deserialization error, or exits with a non-zero code
 * @internal
 */
export declare function promisifyWorker<T = unknown>(worker: Worker_2): Promise<T>

declare const rawConfigSchema: z_2.ZodUnion<
  readonly [
    z_2.ZodArray<
      z_2.ZodObject<
        {
          basePath: z_2.ZodString
          name: z_2.ZodString
          plugins: z_2.ZodOptional<z_2.ZodArray<z_2.ZodUnknown>>
          title: z_2.ZodString
          unstable_sources: z_2.ZodArray<
            z_2.ZodObject<
              {
                dataset: z_2.ZodString
                projectId: z_2.ZodString
                schema: z_2.ZodObject<
                  {
                    _original: z_2.ZodObject<
                      {
                        name: z_2.ZodOptional<z_2.ZodString>
                        types: z_2.ZodArray<z_2.ZodObject<{}, z_2.core.$loose>>
                      },
                      z_2.core.$strip
                    >
                  },
                  z_2.core.$strip
                >
              },
              z_2.core.$strip
            >
          >
          dataset: z_2.ZodString
          projectId: z_2.ZodString
          schema: z_2.ZodObject<
            {
              _original: z_2.ZodObject<
                {
                  name: z_2.ZodOptional<z_2.ZodString>
                  types: z_2.ZodArray<z_2.ZodObject<{}, z_2.core.$loose>>
                },
                z_2.core.$strip
              >
            },
            z_2.core.$strip
          >
        },
        z_2.core.$strip
      >
    >,
    z_2.ZodObject<
      {
        basePath: z_2.ZodOptional<z_2.ZodString>
        name: z_2.ZodOptional<z_2.ZodString>
        plugins: z_2.ZodOptional<z_2.ZodArray<z_2.ZodUnknown>>
        schema: z_2.ZodOptional<
          z_2.ZodObject<
            {
              name: z_2.ZodOptional<z_2.ZodString>
              types: z_2.ZodArray<z_2.ZodObject<{}, z_2.core.$loose>>
            },
            z_2.core.$strip
          >
        >
        title: z_2.ZodOptional<z_2.ZodString>
        unstable_sources: z_2.ZodArray<
          z_2.ZodObject<
            {
              dataset: z_2.ZodString
              projectId: z_2.ZodString
              schema: z_2.ZodObject<
                {
                  _original: z_2.ZodObject<
                    {
                      name: z_2.ZodOptional<z_2.ZodString>
                      types: z_2.ZodArray<z_2.ZodObject<{}, z_2.core.$loose>>
                    },
                    z_2.core.$strip
                  >
                },
                z_2.core.$strip
              >
            },
            z_2.core.$strip
          >
        >
        dataset: z_2.ZodString
        projectId: z_2.ZodString
      },
      z_2.core.$loose
    >,
  ]
>

declare type RawStudioConfig = z_2.infer<typeof rawConfigSchema>

/**
 * Reads and parses an NDJSON (newline-delimited JSON) file containing telemetry events.
 *
 * @param filePath - Path to the NDJSON file
 * @returns Promise resolving to array of parsed telemetry events
 * @throws Error if file cannot be read or contains invalid JSON
 *
 * @internal
 */
export declare function readNDJSON<T>(filePath: string): Promise<T[]>

/**
 * Read the `package.json` file at the given path
 *
 * @param filePath - Path to package.json to read
 * @param options - Options object for controlling read behavior
 * @returns The parsed package.json
 * @public
 */
export declare function readPackageJson(
  filePath: string | URL,
  options?: ReadPackageJsonOptions,
): Promise<PackageJson>

/**
 * Options for reading package.json files
 *
 * @public
 */
export declare interface ReadPackageJsonOptions {
  /**
   * Default values to merge with the parsed package.json.
   * Parsed values take precedence over defaults.
   */
  defaults?: Partial<PackageJson>
  /**
   * Skip Zod schema validation. When true, the file is parsed but not validated.
   * Defaults to false.
   */
  skipSchemaValidation?: boolean
}

/**
 * Generic recursive search function for project configuration files (synchronous version).
 *
 * @param basePath - The base path to start searching from
 * @param findConfigFn - Function that looks for config files in a given directory
 * @param projectType - The type of project ('app' | 'studio')
 * @param iterations - Current iteration count, passed internally to prevent infinite recursion
 * @returns An object if config is found, false otherwise
 * @internal
 */
export declare function recursivelyResolveProjectRootSync(
  basePath: string,
  findConfigFn: (path: string) => string | undefined,
  projectType: 'app' | 'studio',
  iterations?: number,
): false | ProjectRootResult

declare type RequireProps<T, K extends keyof T> = Omit<T, K> & Required<Pick<T, K>>

declare const resolvedConfigSchema: z_2.ZodArray<
  z_2.ZodObject<
    {
      basePath: z_2.ZodString
      name: z_2.ZodString
      plugins: z_2.ZodOptional<z_2.ZodArray<z_2.ZodUnknown>>
      title: z_2.ZodString
      unstable_sources: z_2.ZodArray<
        z_2.ZodObject<
          {
            dataset: z_2.ZodString
            projectId: z_2.ZodString
            schema: z_2.ZodObject<
              {
                _original: z_2.ZodObject<
                  {
                    name: z_2.ZodOptional<z_2.ZodString>
                    types: z_2.ZodArray<z_2.ZodObject<{}, z_2.core.$loose>>
                  },
                  z_2.core.$strip
                >
              },
              z_2.core.$strip
            >
          },
          z_2.core.$strip
        >
      >
      dataset: z_2.ZodString
      projectId: z_2.ZodString
      schema: z_2.ZodObject<
        {
          _original: z_2.ZodObject<
            {
              name: z_2.ZodOptional<z_2.ZodString>
              types: z_2.ZodArray<z_2.ZodObject<{}, z_2.core.$loose>>
            },
            z_2.core.$strip
          >
        },
        z_2.core.$strip
      >
    },
    z_2.core.$strip
  >
>

declare type ResolvedStudioConfig = z_2.infer<typeof resolvedConfigSchema>

/**
 * Resolves and imports a package from the local project's node_modules,
 * relative to the given working directory. This avoids circular dependencies
 * and ensures the correct version of the package is used.
 *
 * @param packageName - The name of the package to resolve (e.g., 'sanity')
 * @param workDir - The working directory to resolve the package from
 * @returns The imported module
 * @throws If the package cannot be resolved or imported
 *
 * @example
 * ```ts
 * const {createSchema} = await resolveLocalPackage('sanity', workDir)
 * ```
 *
 * @internal
 */
export declare function resolveLocalPackage<T = unknown>(
  packageName: string,
  workDir: string,
): Promise<T>

/**
 * `structuredClone()`, but doesn't throw on non-clonable values - instead it drops them.
 *
 * @param obj - The object to clone.
 * @returns The cloned object.
 * @internal
 */
export declare function safeStructuredClone<T>(obj: T): T

export declare abstract class SanityCommand<T extends typeof Command> extends Command {
  protected args: Args<T>
  protected flags: Flags<T>
  /**
   * Get the global API client.
   *
   * @param args - The global API client options.
   * @returns The global API client.
   *
   * @deprecated use `getGlobalCliClient` function directly instead.
   */
  protected getGlobalApiClient: (args: GlobalCliClientOptions) => Promise<SanityClient>
  /**
   * Get the project API client.
   *
   * @param args - The project API client options.
   * @returns The project API client.
   *
   * @deprecated use `getProjectCliClient` function directly instead.
   */
  protected getProjectApiClient: (args: ProjectCliClientOptions) => Promise<SanityClient>
  /**
   * Helper for outputting to the console.
   *
   * @example
   * ```ts
   * this.output.log('Hello')
   * this.output.warn('Warning')
   * this.output.error('Error')
   * ```
   */
  protected output: Output
  /**
   * The telemetry store.
   *
   * @returns The telemetry store.
   */
  protected telemetry: CLITelemetryStore
  /**
   * Get the CLI config.
   *
   * @returns The CLI config.
   */
  protected getCliConfig(): Promise<CliConfig>
  /**
   * Get the project ID from the CLI config.
   *
   * @returns The project ID or `undefined` if it's not set.
   */
  protected getProjectId(): Promise<string | undefined>
  /**
   * Get the project's root directory by resolving the config
   *
   * @returns The project root result.
   */
  protected getProjectRoot(): Promise<ProjectRootResult>
  init(): Promise<void>
  /**
   * Check if the command is running in unattended mode.
   *
   * This means the command should not ask for user input, instead using defaults where
   * possible, and if that does not make sense (eg there's missing information), then we
   * should error out (remember to exit with a non-zero code).
   *
   * Most commands should take an explicit `--yes` flag to enable unattended mode, but
   * some commands may also be run in unattended mode if `process.stdin` is not a TTY
   * (eg when running in a CI environment).
   */
  protected isUnattended(): boolean
  /**
   * Resolver for checking if the terminal is interactive. Override in tests to provide mock values.
   *
   * @returns Whether the terminal is interactive.
   */
  protected resolveIsInteractive(): boolean
}

export declare type SanityOrgUser = {
  email: string
  id: string
  name: string
  profileImage?: string
  provider: 'github' | 'google' | 'sanity' | `saml-${string}`
  tosAcceptedAt?: string
}

/**
 * Sets the global CLI telemetry store.
 * @internal
 */
export declare function setCliTelemetry(telemetry: CLITelemetryStore): void

/**
 * Set the config value for the given property.
 * Validates that the passed value adheres to the defined CLI config schema.
 *
 * @param prop - The property to set the value for
 * @param value - The value to set
 * @internal
 */
export declare function setConfig<P extends keyof CliUserConfig>(
  prop: P,
  value: CliUserConfig[P],
): Promise<void>

/**
 * Executes a worker file in a Sanity Studio browser context.
 *
 * This uses a combination of vite for "bundling" + jsdom for emulating a browser
 * environment under the hood, which means that the same thing that will work in vite
 * _should_ work in the worker - to a degree. If the user has defined any typescript
 * path aliases, these will have to be added as aliases to the vite config - the same
 * behavior as you would see with regular vite. Other things that are accounted for:
 *
 * - TypeScript support (+JSX, enums and other "compilation needed" features)
 * - CSS, font and other file imports will resolve to a file path
 * - CSS module imports will resolve to a javascript object of class names
 * - Environment variables are available both as `import.meta.env` and `process.env`,
 *   and `.env` files are loaded in the same way that they would in a Sanity studio.
 * - Browser globals not available in a Node.js environment but _are_ provided by JSDOM
 *   are defined directly to the Node environment as globals. While this polutes the
 *   global namespace, it is done only in the worker thread.
 * - Certain browser globals that are _not_ available in JSDOM are also provided to the
 *   global namespace - things like `requestIdleCallback`, `IntersectionObserver` etc.
 *   These are provided with a minimal stub implementation to make them not crash.
 *
 * @param filePath - Path to the worker file (`.ts` works and is encouraged)
 * @param options - Options to pass to the worker
 * @returns A promise that resolves with the message from the worker
 * @throws If the file does not exist
 * @throws If the worker exits with a non-zero code
 * @internal
 */
export declare function studioWorkerTask<T = unknown>(
  filePath: URL,
  options: StudioWorkerTaskOptions,
): Promise<T>

/**
 * Options for the studio worker task
 *
 * @internal
 */
declare interface StudioWorkerTaskOptions extends RequireProps<WorkerOptions_2, 'name'> {
  studioRootPath: string
}

/**
 * Get a `debug` instance which extends the CLI debug instance with the given namespace,
 * eg namespace would be `sanity:cli:<providedNamespace>`
 *
 * @param namespace - The namespace to extend the CLI debug instance with
 * @returns The extended `debug` instance
 */
export declare const subdebug: (namespace: string) => debugIt.Debugger

/**
 * Base information needed for telemetry file operations.
 * Contains common data used by both file path generation and pattern matching.
 */
declare interface TelemetryBaseInfo {
  /** Base filename pattern without sessionId suffix */
  basePattern: string
  /** Base directory where telemetry files are stored */
  directory: string
  /** Environment: 'staging' or 'production' */
  environment: string
  /** Hashed token (first 8 chars of SHA256) for privacy */
  hashedToken: string
}

/**
 * Debug logger for telemetry store operations
 * @internal
 */
export declare const telemetryStoreDebug: Debugger

/**
 * @public
 */
export declare interface TelemetryUserProperties {
  cliVersion: string
  cpuArchitecture: string
  machinePlatform: string
  runtime: string
  runtimeVersion: string
  dataset?: string
  projectId?: string
}

declare interface TimeMeasurer {
  end: (name: string) => number
  getTimings: () => Record<string, number>
  start: (name: string) => void
}

/**
 * Tries to find the studio config path, returning `undefined` if not found.
 *
 * @param basePath - The base path to start searching from
 * @returns A promise that resolves to a string containing the found config path, or `undefined` if not found
 * @throws On errors other than config not found
 * @internal
 */
export declare function tryFindStudioConfigPath(basePath: string): Promise<string | undefined>

/**
 * Try to get the default export of a module of the cli config.
 * This can be either ESM or CJS.
 */
export declare function tryGetDefaultExport(mod: unknown): unknown

/**
 * Executes a worker file with tsx registered. This means you can import other
 * typescript with fairly rich syntax, and still have that only apply to the worker
 * thread instead of the full parent process. The worker should emit a message when
 * complete using `parentPort`. Once it has received a single message will resolve the
 * returned promise with that message. If you are expecting multiple messages, you will
 * have to implement another method ;)
 *
 * @param filePath - Path to the worker file
 * @param options - Options to pass to the worker
 * @returns A promise that resolves with the message from the worker
 * @throws If the file does not exist
 * @throws If the worker exits with a non-zero code
 * @internal
 */
export declare function tsxWorkerTask<T = unknown>(
  filePath: URL_2,
  options: TsxWorkerTaskOptions,
): Promise<T>

/**
 * Options for the tsx worker task
 *
 * @internal
 */
declare interface TsxWorkerTaskOptions extends RequireProps<WorkerOptions_2, 'name'> {
  rootPath: string
}

declare type TypeGenConfig = z.infer<typeof configDefinition>

/**
 * @public
 */
export declare type UserViteConfig =
  | ((config: InlineConfig, env: ConfigEnv) => InlineConfig | Promise<InlineConfig>)
  | InlineConfig

export {}
