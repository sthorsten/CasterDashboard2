/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about a match
 * Note: The parameter matchID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "~/helpers/WebsocketStatus";
import {WebsocketURL} from "~/helpers/WebsocketURL";

export const OverlayDataWebsocket = {
    data() {
        return {
            overlayData: {},
            tickerOverlayData: {},
            overlayDataWebsocket: null,
            overlayDataWebsocketStatus: WebsocketStatus.CLOSED,
            overlayDataWebsocketTimeout: null,
            overlayDataWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectOverlayDataWebsocket() {
            return new Promise((resolve, reject) => {
                this.overlayDataWebsocketConnectCounter++

                // Create websocket connection
                let websocketURL = `${WebsocketURL.getURL(this.$config)}/ws/overlays/data/${this.userID}/`
                this.overlayDataWebsocket = new WebSocket(websocketURL)

                this.overlayDataWebsocket.onopen = () => {
                    clearInterval(this.overlayDataWebsocketTimeout)
                    this.overlayDataWebsocketConnectCounter = 0
                    this.overlayDataWebsocketStatus = WebsocketStatus.CONNECTED

                    console.info("OverlayData websocket connected.")
                    console.debug("URL => ", websocketURL)
                }

                this.overlayDataWebsocket.onmessage = (e) => {
                    let data = JSON.parse(e.data)
                    this.overlayData = data['match_overlay_data']
                    this.tickerOverlayData = data['ticker_overlay_data']
                    console.debug("OverlayData => ", this.overlayData)
                    console.debug("TickerOverlayData => ", this.tickerOverlayData)
                    resolve()
                }

                this.overlayDataWebsocket.onclose = (e) => {
                    if (e.wasClean) {
                        console.info("OverlayData websocket disconnected cleanly.")
                        resolve()
                    }

                    // Print status error
                    if (e.code === 4000) {
                        this.overlayDataWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Server rejected websocket connection");
                        reject()
                    }

                    // Terminate connection
                    if (this.overlayDataWebsocketConnectCounter >= 5) {
                        this.overlayDataWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Failed to (re)connect OverlayData websocket!")
                        reject()
                    }

                    // Reconnect
                    console.warn("OverlayData websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                    this.overlayDataWebsocketStatus = WebsocketStatus.RECONNECTING
                    this.overlayDataWebsocketTimeout = setTimeout(this.connectMatchMapAllWebsocket, 5000)
                }
            })
        },
    },

    beforeDestroy() {
        // Always close the websocket connection when leaving the site
        if (this.overlayDataWebsocket) {
            this.overlayDataWebsocket.close()
            this.overlayDataWebsocketStatus = WebsocketStatus.CLOSED

            // Cancel reconnection attempt when leaving the site
            if (this.overlayDataWebsocketTimeout) {
                clearTimeout(this.overlayDataWebsocketTimeout)
            }
        }
    }
}
