/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about all matchMaps maps for the current matchMaps id
 * Note: The parameter matchID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "~/helpers/WebsocketStatus"
import {WebsocketURL} from "~/helpers/WebsocketURL"

export const MatchMapSingleWebsocket = {
  data() {
    return {
      matchMap: {},
      matchMapSingleWebsocket: null,
      matchMapSingleWebsocketStatus: WebsocketStatus.CLOSED,
      matchMapSingleWebsocketTimeout: null,
      matchMapSingleWebsocketConnectCounter: 0,
    }
  },

  methods: {
    connectMatchMapSingleWebsocket() {
      return new Promise((resolve, reject) => {
        this.matchMapSingleWebsocketConnectCounter++

        // Create websocket connection
        let websocketURL = `${WebsocketURL.getURL(this.$config)}/ws/matches/${
          this.matchID
        }/map/${this.mapID}/`
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
          resolve()
        }

        this.matchMapSingleWebsocket.onclose = (e) => {
          if (e.wasClean) {
            console.info("MatchMapSingle websocket disconnected cleanly.")
            resolve()
            return
          }

          // Print status error
          if (e.code === 4000) {
            this.matchMapSingleWebsocketStatus = WebsocketStatus.ERROR
            console.error("Server rejected websocket connection")
            reject()
            return
          }

          // Terminate connection
          if (this.matchMapSingleWebsocketConnectCounter >= 10) {
            this.matchMapSingleWebsocketStatus = WebsocketStatus.ERROR
            console.error("Failed to (re)connect MatchMapSingle websocket!")
            reject()
            return
          }

          // Reconnect
          let timeout = this.matchMapSingleWebsocketConnectCounter * 2
          console.warn(
            `MatchMapSingle websocket connection closed unexpectedly. Trying to reconnect (${timeout}s.)`
          )
          this.matchMapSingleWebsocketStatus = WebsocketStatus.RECONNECTING
          this.matchMapSingleWebsocketTimeout = setTimeout(
            this.connectMatchMapSingleWebsocket,
            timeout * 1000
          )
        }
      })
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
  },
}
