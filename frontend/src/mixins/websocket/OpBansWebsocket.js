/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about all operator bans for a given match and map
 * Note: The parameters matchID and mapID must be provided by the component this mixin is loaded in
 */

import {WebsocketStatus} from "@/helpers/const/WebsocketStatus";

export const OpBansWebsocket = {
    data() {
        return {
            opBans: null,
            opBansWebsocket: null,
            opBansWebsocketStatus: WebsocketStatus.CLOSED,
            opBansWebsocketTimeout: null,
            opBansWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectOpBansWebsocket() {
            this.opBansWebsocketConnectCounter++

            // Create websocket connection
            let websocketURL = `${this.$store.getters.websocketURL}/ws/matches/${this.matchID}/map/${this.mapID}/opbans/`
            this.opBansWebsocket = new WebSocket(websocketURL)

            this.opBansWebsocket.onopen = () => {
                clearInterval(this.opBansWebsocketTimeout)
                this.opBansWebsocketConnectCounter = 0
                this.opBansWebsocketStatus = WebsocketStatus.CONNECTED

                console.info("OpBans websocket connected.")
                console.debug("URL => ", websocketURL)
            }

            this.opBansWebsocket.onmessage = (e) => {
                this.opBans = JSON.parse(e.data)
                console.debug("OpBans => ", this.opBans)
            }

            this.opBansWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("OpBans websocket disconnected cleanly.")
                    return
                }

                // Print status error
                if (e.code === 4000) {
                    this.opBansWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Server rejected websocket connection");
                    return
                }

                // Terminate connection
                if (this.opBansWebsocketConnectCounter >= 5) {
                    this.opBansWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Failed to (re)connect OpBans websocket!")
                    return
                }

                // Reconnect
                console.warn("OpBans websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                this.opBansWebsocketStatus = WebsocketStatus.RECONNECTING
                this.opBansWebsocketTimeout = setTimeout(this.connectMatchWebsocket, 5000)
            }
        },
    },

    beforeDestroy() {
        // Always close the websocket connection when leaving the site
        if (this.opBansWebsocket) {
            this.opBansWebsocket.close()
            this.opBansWebsocketStatus = WebsocketStatus.CLOSED

            // Cancel reconnection attempt when leaving the site
            if (this.opBansWebsocketTimeout) {
                clearTimeout(this.opBansWebsocketTimeout)
            }
        }
    }
}
