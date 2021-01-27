/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about all matchMaps maps for the current matchMaps id
 * Note: The parameter matchID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "~/helpers/WebsocketStatus";

export const MatchMapAllWebsocket = {
    data() {
        return {
            matchMaps: null,
            matchMapAllWebsocket: null,
            matchMapAllWebsocketStatus: WebsocketStatus.CLOSED,
            matchMapAllWebsocketTimeout: null,
            matchMapAllWebsocketConnectCounter: 0
        }
    },

    methods: {
        connectMatchMapAllWebsocket() {
            this.matchMapAllWebsocketConnectCounter++

            // Create websocket connection
            let websocketURL = `${process.env.websocketBaseURL}/ws/matches/${this.matchID}/maps/`
            this.matchMapAllWebsocket = new WebSocket(websocketURL)

            this.matchMapAllWebsocket.onopen = () => {
                clearInterval(this.matchMapAllWebsocketTimeout)
                this.matchMapAllWebsocketConnectCounter = 0
                this.matchMapAllWebsocketStatus = WebsocketStatus.CONNECTED

                console.info("MatchMapAll websocket connected.")
                console.debug("URL => ", websocketURL)
            }

            this.matchMapAllWebsocket.onmessage = (e) => {
                this.matchMaps = JSON.parse(e.data)
                console.debug("MatchMaps => ", this.matchMaps)
            }

            this.matchMapAllWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("MatchMapAll websocket disconnected cleanly.")
                    return
                }

                // Print status error
                if (e.code === 4000) {
                    this.matchMapAllWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Server rejected websocket connection");
                    return
                }

                // Terminate connection
                if (this.matchMapAllWebsocketConnectCounter >= 5){
                    this.matchMapAllWebsocketStatus = WebsocketStatus.ERROR
                    console.error("Failed to (re)connect MatchMapAll websocket!")
                    return
                }

                // Reconnect
                console.warn("MatchMapAll websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                this.matchMapAllWebsocketStatus = WebsocketStatus.RECONNECTING
                this.matchMapAllWebsocketTimeout = setTimeout(this.connectMatchMapAllWebsocket, 5000)
            }
        },
    },

    beforeDestroy() {
        // Always close the websocket connection when leaving the site
        if (this.matchMapAllWebsocket) {
            this.matchMapAllWebsocket.close()
            this.matchMapAllWebsocketStatus = WebsocketStatus.CLOSED

            // Cancel reconnection attempt when leaving the site
            if (this.matchMapAllWebsocketTimeout) {
                clearTimeout(this.matchMapAllWebsocketTimeout)
            }
        }
    }
}
