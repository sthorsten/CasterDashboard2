/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about all matchMaps maps for the current matchMaps id
 * Note: The parameter matchID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "~/helpers/WebsocketStatus"
import {WebsocketURL} from "~/helpers/WebsocketURL"

export const OperatorBansWebsocket = {
  data() {
    return {
      bannedOperators: [],
      operatorBansWebsocket: null,
      operatorBansWebsocketStatus: WebsocketStatus.CLOSED,
      operatorBansWebsocketTimeout: null,
      operatorBansWebsocketConnectCounter: 0,
    }
  },

  methods: {
    async connectOperatorBansWebsocket() {
      return new Promise((resolve, reject) => {
        this.operatorBansWebsocketConnectCounter++

        // Create websocket connection
        let websocketURL = `${WebsocketURL.getURL(this.$config)}/ws/matches/${
          this.matchID
        }/map/${this.mapID}/opbans/`
        this.operatorBansWebsocket = new WebSocket(websocketURL)

        this.operatorBansWebsocket.onopen = () => {
          clearInterval(this.operatorBansWebsocketTimeout)
          this.operatorBansWebsocketConnectCounter = 0
          this.operatorBansWebsocketStatus = WebsocketStatus.CONNECTED

          console.info("OperatorBans websocket connected.")
          console.debug("URL => ", websocketURL)
        }

        this.operatorBansWebsocket.onmessage = (e) => {
          this.bannedOperators = JSON.parse(e.data)
          console.debug("BannedOperators => ", this.bannedOperators)
          resolve()
        }

        this.operatorBansWebsocket.onclose = (e) => {
          if (e.wasClean) {
            console.info("OperatorBans websocket disconnected cleanly.")
            resolve()
            return
          }

          // Print status error
          if (e.code === 4000) {
            this.operatorBansWebsocketStatus = WebsocketStatus.ERROR
            console.error("Server rejected websocket connection")
            reject()
            return
          }

          // Terminate connection
          if (this.operatorBansWebsocketConnectCounter >= 10) {
            this.operatorBansWebsocketStatus = WebsocketStatus.ERROR
            console.error("Failed to (re)connect OperatorBans websocket!")
            reject()
            return
          }

          // Reconnect
          let timeout = this.operatorBansWebsocketConnectCounter * 2
          console.warn(
            `OperatorBans websocket connection closed unexpectedly. Trying to reconnect (${timeout}s.)`
          )
          this.operatorBansWebsocketStatus = WebsocketStatus.RECONNECTING
          this.operatorBansWebsocketTimeout = setTimeout(
            this.connectOperatorBansWebsocket,
            timeout * 1000
          )
        }
      })
    },

    async disconnectOperatorBansWebsocket() {
      // Close the websocket connection
      if (this.operatorBansWebsocket) {
        await this.operatorBansWebsocket.close()
        this.operatorBansWebsocketStatus = WebsocketStatus.CLOSED

        // Cancel reconnection attempt
        if (this.operatorBansWebsocketTimeout) {
          clearTimeout(this.operatorBansWebsocketTimeout)
        }
      }
    },
  },

  beforeDestroy() {
    this.disconnectOperatorBansWebsocket()
  },
}
