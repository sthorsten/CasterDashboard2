/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about the current matchmap
 */

export const MatchMapWebsocketInGame = {
    data() {
        return {
            matchMap: null,
            matchMapWebsocket: null,
            matchMapWebsocketStatus: "",
            matchMapWebsocketInterval: null,
        }
    },

    methods: {
        connectMatchMapWebsocket() {
            // Create websocket connection
            this.matchMapWebsocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/match_map/${this.user}/`)

            this.matchMapWebsocket.onopen = () => {
                console.info("MatchMap websocket connected.")

                // Get data after connecting successfully
                this.matchMapWebsocket.send(JSON.stringify({"command": "get_match_map"}))

                clearInterval(this.matchMapWebsocketInterval)
                this.matchMapWebsocketStatus = "connected"
            }

            this.matchMapWebsocket.onmessage = (e) => {
                this.matchMap = JSON.parse(e.data)
                console.debug("MatchMap => ", this.matchMap)
            }

            this.matchMapWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("MatchMap websocket disconnected cleanly.")
                } else {
                    // Reconnect if not closed cleanly
                    console.warn("MatchMap websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                    this.matchMapWebsocketStatus = "reconnecting"
                    this.matchMapWebsocketInterval = setInterval(this.connectMatchMapWebsocket, 5000)
                }
            }
        },
    },

    created() {
        this.connectMatchMapWebsocket()
    },

    beforeDestroy() {
        if (this.matchMapWebsocket) {
            this.matchMapWebsocket.close()

            if (this.matchMapWebsocketInterval) {
                clearInterval(this.matchMapWebsocketInterval)
            }
        }
    }
}
