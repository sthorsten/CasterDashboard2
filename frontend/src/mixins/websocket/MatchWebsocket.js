/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about the current matchMaps
 * Note: The parameter matchID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "@/helpers/const/WebsocketStatus";

export const MatchWebsocket = {
    data() {
        return {
            match: null,
            matchWebsocket: null,
            matchWebsocketStatus: WebsocketStatus.CLOSED,
            matchWebsocketTimeout: null,
            matchWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectMatchWebsocket() {
            this.matchWebsocketConnectCounter++

            // Create websocket connection
            let websocketURL = `${this.$store.getters.websocketURL}/ws/match/${this.matchID}/`
            this.matchWebsocket = new WebSocket(websocketURL)

            this.matchWebsocket.onopen = () => {
                clearInterval(this.matchWebsocketTimeout)
                this.matchWebsocketConnectCounter = 0
                this.matchWebsocketStatus = WebsocketStatus.CONNECTED

                console.info("Match websocket connected.")
                console.debug("URL => ", websocketURL)
            }

            this.matchWebsocket.onmessage = (e) => {
                this.match = JSON.parse(e.data)
                console.debug("Match => ", this.match)
            }

            this.matchWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("Match websocket disconnected cleanly.")
                    return
                }

                // Print status error
                if (e.code === 4000) {
                    this.matchWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Server rejected websocket connection");
                    return
                }

                // Terminate connection
                if (this.matchWebsocketConnectCounter >= 5){
                    this.matchWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Failed to (re)connect Match websocket!")
                    return
                }

                // Reconnect
                console.warn("Match websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                this.matchWebsocketStatus = WebsocketStatus.RECONNECTING
                this.matchWebsocketTimeout = setTimeout(this.connectMatchWebsocket, 5000)
            }
        },
    },

    beforeDestroy() {
        // Always close the websocket connection when leaving the site
        if (this.matchWebsocket) {
            this.matchWebsocket.close()
            this.matchWebsocketStatus = WebsocketStatus.CLOSED

            // Cancel reconnection attempt when leaving the site
            if (this.matchWebsocketTimeout) {
                clearTimeout(this.matchWebsocketTimeout)
            }
        }
    }
}
