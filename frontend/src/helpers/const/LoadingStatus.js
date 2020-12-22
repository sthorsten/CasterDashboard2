/**
 * Simple enum that represents the loading state of a dashboard page.
 *
 * NONE: Loading process has not started yet.
 * LOADING: Data is being loaded from the backend or external sources.
 * LOADED: Data loaded successfully.
 * TIMOUT: Data could not be loaded in an expected time frame.
 * ERROR: One or more resources failed to load.
 */

export const LoadingStatus = {
    NONE: 0,
    LOADING: 1,
    LOADED: 2,
    TIMEOUT: 3,
    ERROR: -1
}