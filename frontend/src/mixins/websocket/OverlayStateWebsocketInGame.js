/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about the overlay state(s) of the current user
 */

export const OverlayStateWebsocketInGame = {
    data() {
        return {
            overlayState: null,
            overlayStateWebsocket: null,
            overlayStateWebsocketStatus: "",
            overlayStateWebsocketInterval: null,
        }
    },

    methods: {
        connectOverlayStateWebsocket() {
            // Create websocket connection
            this.overlayStateWebsocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/overlay_state/${this.user}/`)

            this.overlayStateWebsocket.onopen = () => {
                console.info("OverlayState websocket connected.")

                // Get data after connecting successfully
                this.overlayStateWebsocket.send(JSON.stringify({"command": "get_overlay_state"}))

                clearInterval(this.overlayStateWebsocketInterval)
                this.overlayStateWebsocketStatus = "connected"
            }

            this.overlayStateWebsocket.onmessage = (e) => {
                this.overlayState = JSON.parse(e.data)
                console.debug("OverlayStateData => ", this.overlayState)
            }

            this.overlayStateWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("OverlayState websocket disconnected cleanly.")
                } else {
                    // Reconnect if not closed cleanly
                    console.warn("OverlayState websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                    this.overlayStateWebsocketStatus = "reconnecting"
                    this.overlayStateWebsocketInterval = setInterval(this.connectOverlayStateWebsocket, 5000)
                }
            }
        }
    },

    created() {
        this.connectOverlayStateWebsocket()
    },

    beforeDestroy() {
        if (this.overlayStateWebsocket) {
            this.overlayStateWebsocket.close()

            if (this.overlayStateWebsocketInterval) {
                clearInterval(this.overlayStateWebsocketInterval)
            }
        }
    }
}
