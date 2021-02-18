/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about a match
 * Note: The parameter matchID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "~/helpers/WebsocketStatus";
import {WebsocketURL} from "~/helpers/WebsocketURL";

export const MatchSingleWebsocket = {
    data() {
        return {
            match: {},
            matchSingleWebsocket: null,
            matchSingleWebsocketStatus: WebsocketStatus.CLOSED,
            matchSingleWebsocketTimeout: null,
            matchSingleWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectMatchSingleWebsocket() {
            return new Promise((resolve, reject) => {
                this.matchSingleWebsocketConnectCounter++

                // Create websocket connection
                let websocketURL = `${WebsocketURL.getURL(this.$config)}/ws/match/${this.matchID}/`
                this.matchSingleWebsocket = new WebSocket(websocketURL)

                this.matchSingleWebsocket.onopen = () => {
                    clearInterval(this.matchSingleWebsocketTimeout)
                    this.matchSingleWebsocketConnectCounter = 0
                    this.matchSingleWebsocketStatus = WebsocketStatus.CONNECTED

                    console.info("MatchSingle websocket connected.")
                    console.debug("URL => ", websocketURL)
                }

                this.matchSingleWebsocket.onmessage = (e) => {
                    this.match = JSON.parse(e.data)
                    console.debug("Match => ", this.match)
                    resolve()
                }

                this.matchSingleWebsocket.onclose = (e) => {
                    if (e.wasClean) {
                        console.info("MatchSingle websocket disconnected cleanly.")
                        resolve()
                    }

                    // Print status error
                    if (e.code === 4000) {
                        this.matchSingleWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Server rejected websocket connection");
                        reject()
                    }

                    // Terminate connection
                    if (this.matchSingleWebsocketConnectCounter >= 5) {
                        this.matchSingleWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Failed to (re)connect MatchSingle websocket!")
                        reject()
                    }

                    // Reconnect
                    console.warn("MatchSingle websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                    this.matchSingleWebsocketStatus = WebsocketStatus.RECONNECTING
                    this.matchSingleWebsocketTimeout = setTimeout(this.connectMatchMapAllWebsocket, 5000)
                }
            })
        },
    },

    beforeDestroy() {
        // Always close the websocket connection when leaving the site
        if (this.matchSingleWebsocket) {
            this.matchSingleWebsocket.close()
            this.matchSingleWebsocketStatus = WebsocketStatus.CLOSED

            // Cancel reconnection attempt when leaving the site
            if (this.matchSingleWebsocketTimeout) {
                clearTimeout(this.matchSingleWebsocketTimeout)
            }
        }
    }
}
