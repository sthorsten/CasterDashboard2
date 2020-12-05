/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about a single matchMap for the current matchMap id
 * Note: The parameters matchID and mapID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "@/helpers/const/WebsocketStatus";

export const MatchMapSingleWebsocket = {
    data() {
        return {
            matchMap: null,
            matchMapSingleWebsocket: null,
            matchMapSingleWebsocketStatus: WebsocketStatus.CLOSED,
            matchMapSingleWebsocketTimeout: null,
            matchMapSingleWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectMatchMapSingleWebsocket() {
            this.matchMapSingleWebsocketConnectCounter++

            // Create websocket connection
            let websocketURL = `${this.$store.getters.websocketURL}/ws/matches/${this.matchID}/map/${this.mapID}/`
            this.matchMapSingleWebsocket = new WebSocket(websocketURL)

            this.matchMapSingleWebsocket.onopen = () => {
                clearInterval(this.matchMapSingleWebsocketTimeout)
                this.matchMapSingleWebsocketConnectCounter = 0
                this.matchMapSingleWebsocketStatus = WebsocketStatus.CONNECTED

                console.info("MatchMapSingle websocket connected.")
                console.debug("URL => ", websocketURL)
            }

            this.matchMapSingleWebsocket.onmessage = (e) => {
                this.matchMap = JSON.parse(e.data)
                console.debug("MatchMap => ", this.matchMap)
            }

            this.matchMapSingleWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("MatchMapSingle websocket disconnected cleanly.")
                    return
                }

                // Print status error
                if (e.code === 4000) {
                    this.matchMapSingleWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Server rejected websocket connection");
                    return
                }

                // Terminate connection
                if (this.matchMapSingleWebsocketConnectCounter >= 5){
                    this.matchMapSingleWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Failed to (re)connect MatchMapSingle websocket!")
                    return
                }

                // Reconnect
                console.warn("MatchMapSingle websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                this.matchMapSingleWebsocketStatus = WebsocketStatus.RECONNECTING
                this.matchMapSingleWebsocketTimeout = setTimeout(this.connectMatchWebsocket, 5000)
            }
        },
    },

    beforeDestroy() {
        // Always close the websocket connection when leaving the site
        if (this.matchMapSingleWebsocket) {
            this.matchMapSingleWebsocket.close()
            this.matchMapSingleWebsocketStatus = WebsocketStatus.CLOSED

            // Cancel reconnection attempt when leaving the site
            if (this.matchMapSingleWebsocketTimeout) {
                clearTimeout(this.matchMapSingleWebsocketTimeout)
            }
        }
    }
}
