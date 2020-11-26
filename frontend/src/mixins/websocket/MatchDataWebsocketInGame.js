/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about the current matchMaps
 */

export const MatchDataWebsocketInGame = {
    data() {
        return {
            matchData: null,
            matchDataWebsocket: null,
            matchDataWebsocketStatus: "",
            matchDataWebsocketInterval: null,
        }
    },

    methods: {
        connectMatchDataWebsocket() {
            // Create websocket connection
            this.matchDataWebsocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/match_data/${this.user}/`)

            this.matchDataWebsocket.onopen = () => {
                console.info("MatchData websocket connected.")

                // Get data after connecting successfully
                this.matchDataWebsocket.send(JSON.stringify({"command": "get_match_data"}))

                clearInterval(this.matchDataWebsocketInterval)
                this.matchDataWebsocketStatus = "connected"
            }

            this.matchDataWebsocket.onmessage = (e) => {
                this.matchData = JSON.parse(e.data)
                console.debug("MatchData => ", this.matchData)
            }

            this.matchDataWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("MatchData websocket disconnected cleanly.")
                } else {
                    // Reconnect if not closed cleanly
                    console.warn("MatchData websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                    this.matchDataWebsocketStatus = "reconnecting"
                    this.matchDataWebsocketInterval = setInterval(this.connectMatchDataWebsocket, 5000)
                }
            }
        },
    },

    created(){
        this.connectMatchDataWebsocket()
    },

    beforeDestroy() {
        if (this.matchDataWebsocket) {
            this.matchDataWebsocket.close()

            if (this.matchDataWebsocketInterval) {
                clearInterval(this.matchDataWebsocketInterval)
            }
        }
    }
}
