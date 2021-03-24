/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about a match
 * Note: The parameter matchID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "~/helpers/WebsocketStatus";
import {WebsocketURL} from "~/helpers/WebsocketURL";

export const OverlayStateWebsocket = {
    data() {
        return {
            overlayState: {},
            overlayStateWebsocket: null,
            overlayStateWebsocketStatus: WebsocketStatus.CLOSED,
            overlayStateWebsocketTimeout: null,
            overlayStateWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectOverlayStateWebsocket() {
            return new Promise((resolve, reject) => {
                this.overlayStateWebsocketConnectCounter++

                // Create websocket connection
                let websocketURL = `${WebsocketURL.getURL(this.$config)}/ws/overlays/state/${this.userID}/`
                this.overlayStateWebsocket = new WebSocket(websocketURL)

                this.overlayStateWebsocket.onopen = () => {
                    clearInterval(this.overlayStateWebsocketTimeout)
                    this.overlayStateWebsocketConnectCounter = 0
                    this.overlayStateWebsocketStatus = WebsocketStatus.CONNECTED

                    console.info("OverlayState websocket connected.")
                    console.debug("URL => ", websocketURL)
                }

                this.overlayStateWebsocket.onmessage = (e) => {
                    this.overlayState = JSON.parse(e.data)
                    console.debug("OverlayState => ", this.overlayState)
                    resolve()
                }

                this.overlayStateWebsocket.onclose = (e) => {
                    if (e.wasClean) {
                        console.info("OverlayState websocket disconnected cleanly.")
                        resolve()
                        return
                    }

                    // Print status error
                    if (e.code === 4000) {
                        this.overlayStateWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Server rejected websocket connection");
                        reject()
                        return
                    }

                    // Terminate connection
                    if (this.overlayStateWebsocketConnectCounter >= 10) {
                        this.overlayStateWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Failed to (re)connect OverlayState websocket!")
                        reject()
                        return
                    }

                    // Reconnect
                    let timeout = this.overlayStateWebsocketConnectCounter * 2
                    console.warn(`OverlayState websocket connection closed unexpectedly. Trying to reconnect (${timeout}s.)`)
                    this.overlayStateWebsocketStatus = WebsocketStatus.RECONNECTING
                    this.overlayStateWebsocketTimeout = setTimeout(this.connectOverlayStateWebsocket, timeout * 1000)
                }
            })
        },
    },

    beforeDestroy() {
        // Always close the websocket connection when leaving the site
        if (this.overlayStateWebsocket) {
            this.overlayStateWebsocket.close()
            this.overlayStateWebsocketStatus = WebsocketStatus.CLOSED

            // Cancel reconnection attempt when leaving the site
            if (this.overlayStateWebsocketTimeout) {
                clearTimeout(this.overlayStateWebsocketTimeout)
            }
        }
    }
}
