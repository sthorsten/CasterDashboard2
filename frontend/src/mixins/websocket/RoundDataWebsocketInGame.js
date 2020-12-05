/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about all rounds in the current matchMaps and map
 */

export const RoundDataWebsocketInGame = {
    data() {
        return {
            roundData: null,
            roundDataWebsocket: null,
            roundDataWebsocketStatus: "",
            roundDataWebsocketInterval: null,
        }
    },

    methods: {
        connectRoundDataWebsocket() {
            // Create websocket connection
            this.roundDataWebsocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/round_data/${this.match.id}/${this.matchMap.map}/`)

            this.roundDataWebsocket.onopen = () => {
                console.info("RoundData websocket connected.")

                // Get data after connecting successfully
                this.roundDataWebsocket.send(JSON.stringify({"command": "get_round_data"}))

                clearInterval(this.roundDataWebsocketInterval)
                this.roundDataWebsocketStatus = "connected"
            }

            this.roundDataWebsocket.onmessage = (e) => {
                this.roundData = JSON.parse(e.data)
                console.debug("RoundData => ", this.roundData)
            }

            this.roundDataWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("RoundData websocket disconnected cleanly.")
                } else {
                    // Reconnect if not closed cleanly
                    console.warn("RoundData websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                    this.roundDataWebsocketStatus = "reconnecting"
                    this.roundDataWebsocketInterval = setInterval(this.connectRoundDataWebsocket, 5000)
                }
            }
        },
    },

    beforeDestroy() {
        if (this.roundDataWebsocket) {
            this.roundDataWebsocket.close()

            if (this.roundDataWebsocketInterval) {
                clearInterval(this.roundDataWebsocketInterval)
            }
        }
    }
}
