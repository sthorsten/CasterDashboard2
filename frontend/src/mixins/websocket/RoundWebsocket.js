/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about all rounds for a given match and map
 * Note: The parameters matchID and mapID must be provided by the component this mixin is loaded in
 */

import {WebsocketStatus} from "@/helpers/const/WebsocketStatus";

export const RoundWebsocket = {
    data() {
        return {
            rounds: null,
            roundWebsocket: null,
            roundWebsocketStatus: WebsocketStatus.CLOSED,
            roundWebsocketTimeout: null,
            roundWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectRoundWebsocket() {
            this.roundWebsocketConnectCounter++

            // Create websocket connection
            let websocketURL = `${this.$store.getters.websocketURL}/ws/matches/${this.matchID}/map/${this.mapID}/rounds/`
            this.roundWebsocket = new WebSocket(websocketURL)

            this.roundWebsocket.onopen = () => {
                clearInterval(this.roundWebsocketTimeout)
                this.roundWebsocketConnectCounter = 0
                this.roundWebsocketStatus = WebsocketStatus.CONNECTED

                console.info("Round websocket connected.")
                console.debug("URL => ", websocketURL)
            }

            this.roundWebsocket.onmessage = (e) => {
                this.rounds = JSON.parse(e.data)
                console.debug("Rounds => ", this.rounds)
            }

            this.roundWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("Round websocket disconnected cleanly.")
                    return
                }

                // Print status error
                if (e.code === 4000) {
                    this.roundWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Server rejected websocket connection");
                    return
                }

                // Terminate connection
                if (this.roundWebsocketConnectCounter >= 5) {
                    this.roundWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Failed to (re)connect Round websocket!")
                    return
                }

                // Reconnect
                console.warn("Round websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                this.roundWebsocketStatus = WebsocketStatus.RECONNECTING
                this.roundWebsocketTimeout = setTimeout(this.connectMatchWebsocket, 5000)
            }
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
