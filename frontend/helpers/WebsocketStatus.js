/**
 * Simple enum that represents the current state of a websocket connection internally.
 *
 * CLOSED: Websocket connection has not been opened yet.
 * CONNECTING: Websocket connection is being established.
 * CONNECTED: Websocket connection is active.
 * RECONNECTING: Websocket connection has been disconnected unexpectedly by the server and needs to be re-established.
 * ERROR: Websocket connection could not be (re)established.
 */

export const WebsocketStatus = {
    CLOSED: 0,
    CONNECTING: 1,
    CONNECTED: 2,
    RECONNECTING: 3,
    ERROR: -1
}