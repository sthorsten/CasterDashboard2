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
                        return
                    }

                    // Print status error
                    if (e.code === 4000) {
                        this.roundWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Server rejected websocket connection");
                        reject()
                        return
                    }

                    // Terminate connection
                    if (this.roundWebsocketConnectCounter >= 10) {
                        this.roundWebsocketStatus = WebsocketStatus.ERROR
                        console.error("Failed to (re)connect rounds websocket!")
                        reject()
                        return
                    }

                    // Reconnect
                    let timeout = this.roundWebsocketConnectCounter * 2
                    console.warn(`Rounds websocket connection closed unexpectedly. Trying to reconnect (${timeout}s.)`)
                    this.roundWebsocketStatus = WebsocketStatus.RECONNECTING
                    this.roundWebsocketTimeout = setTimeout(this.connectRoundWebsocket, timeout * 1000)
                }
            })
        },

        async disconnectRoundWebsocket() {
            // Close the websocket connection
            if (this.roundWebsocket) {
                await this.roundWebsocket.close()
                this.roundWebsocketStatus = WebsocketStatus.CLOSED

                // Cancel reconnection attempt
                if (this.roundWebsocketTimeout) {
                    clearTimeout(this.roundWebsocketTimeout)
                }
            }
        }
    },

    beforeDestroy() {
        this.disconnectRoundWebsocket()
    }
}
