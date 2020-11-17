/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about the current map picks & bans
 */

export const MapDataWebsocketInGame = {
    data() {
        return {
            mapData: null,
            mapDataWebsocket: null,
            mapDataWebsocketStatus: "",
            mapDataWebsocketInterval: null,
        }
    },

    methods: {
        connectMapDataWebsocket() {
            // Create websocket connection
            this.mapDataWebsocket = new WebSocket(`${this.$store.getters.websocketURL}/ws/map_data/${this.user}/`)

            this.mapDataWebsocket.onopen = () => {
                console.info("MapData websocket connected.")

                // Get data after connecting successfully
                this.mapDataWebsocket.send(JSON.stringify({"command": "get_map_data"}))

                clearInterval(this.mapDataWebsocketInterval)
                this.mapDataWebsocketStatus = "connected"
            }

            this.mapDataWebsocket.onmessage = (e) => {
                this.mapData = JSON.parse(e.data)
                console.debug("MapData => ", this.mapData)
            }

            this.mapDataWebsocket.onclose = (e) => {
                if (e.wasClean) {
                    console.info("MapData websocket disconnected cleanly.")
                } else {
                    // Reconnect if not closed cleanly
                    console.warn("MapData websocket connection closed unexpectedly. Trying to reconnect (5s.)")
                    this.mapDataWebsocketStatus = "reconnecting"
                    this.mapDataWebsocketInterval = setInterval(this.connectMapDataWebsocket, 5000)
                }
            }
        },
    },

    created(){
        this.connectMapDataWebsocket()
    },

    beforeDestroy() {
        if (this.mapDataWebsocket) {
            this.mapDataWebsocket.close()

            if (this.mapDataWebsocketInterval) {
                clearInterval(this.mapDataWebsocketInterval)
            }
        }
    }
}
