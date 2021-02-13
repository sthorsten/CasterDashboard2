/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about all rounds for the current match and map
 * Note: The parameters matchID and mapID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "~/helpers/WebsocketStatus";
import {WebsocketURL} from "~/helpers/WebsocketURL";

export const RoundWebsocket = {
    data() {
        return {
            rounds: {},
            roundWebsocket: null,
            roundWebsocketStatus: WebsocketStatus.CLOSED,
            roundWebsocketTimeout: null,
            roundWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectRoundWebsocket() {
            return new Promise((resolve, reject) => {
                this.roundWebsocketConnectCounter++

                // Create websocket connection
                let websocketURL = `${WebsocketURL.getURL(this.$config)}/ws/matches/${this.matchID}/map/${this.mapID}/rounds/`
                this.roundWebsocket = new WebSocket(websocketURL)

                this.roundWebsocket.onopen = () => {
                    clearInterval(this.roundWebsocketTimeout)
                    this.roundWebsocketConnectCounter = 0
                    this.roundWebsocketStatus = WebsocketStatus.CONNECTED

                    console.info("rounds websocket connected.")
                    console.debug("URL => ", websocketURL)
                }

                this.roundWebsocket.onmessage = (e) => {
                    this.rounds = JSON.parse(e.data)
                    console.debug("rounds => ", this.rounds)
                    resolve()
                }

                this.roundWebsocket.onclose = (e) => {
                    if (e.wasClean) {
                        console.info("rounds websocket disconnected cleanly.")
                        resolve()
                    }

                    // Print status error
                    if (e.code === 4000) {
                        this.roundWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Server rejected websocket connection");
                        reject()
                    }

                    // Terminate connection
                    if (this.roundWebsocketConnectCounter >= 5) {
                        this.roundWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Failed to (re)connect rounds websocket!")
                        reject()
                    }

                    // Reconnect
                    console.warn("rounds websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                    this.roundWebsocketStatus = WebsocketStatus.RECONNECTING
                    this.roundWebsocketTimeout = setTimeout(this.connectRoundsAllWebsocket, 5000)
                }
            })
        },
    },

    beforeDestroy() {
        // Always close the websocket connection when leaving the site
        if (this.roundWebsocket) {
            this.roundWebsocket.close()
            this.roundWebsocketStatus = WebsocketStatus.CLOSED

            // Cancel reconnection attempt when leaving the site
            if (this.roundWebsocketTimeout) {
                clearTimeout(this.roundWebsocketTimeout)
            }
        }
    }
}