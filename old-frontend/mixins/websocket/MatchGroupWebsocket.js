/**
 * Creates and handles a websocket connection to the backend to retrieve realtime information about a match group
 * Note: The parameter userID must be provided by the component this mixin is loaded in!
 */

import {WebsocketStatus} from "~/helpers/WebsocketStatus"
import {WebsocketURL} from "~/helpers/WebsocketURL"

export const MatchGroupWebsocket = {
  data() {
    return {
      matchGroup: {},
      matchGroupWebsocket: null,
      matchGroupWebsocketStatus: WebsocketStatus.CLOSED,
      matchGroupWebsocketTimeout: null,
      matchGroupWebsocketConnectCounter: 0,
    }
  },

  methods: {
    connectMatchGroupWebsocket() {
      return new Promise((resolve, reject) => {
        this.matchGroupWebsocketConnectCounter++

        // Create websocket connection
        let websocketURL = `${WebsocketURL.getURL(
          this.$config
        )}/ws/match_group/${this.userID}/`
        this.matchGroupWebsocket = new WebSocket(websocketURL)

        this.matchGroupWebsocket.onopen = () => {
          clearInterval(this.matchGroupWebsocketTimeout)
          this.matchGroupWebsocketConnectCounter = 0
          this.matchGroupWebsocketStatus = WebsocketStatus.CONNECTED

          console.info("MatchGroup websocket connected.")
          console.debug("URL => ", websocketURL)
        }

        this.matchGroupWebsocket.onmessage = (e) => {
          this.matchGroup = JSON.parse(e.data)
          console.debug("MatchGroup => ", this.matchGroup)
          resolve()
        }

        this.matchGroupWebsocket.onclose = (e) => {
          if (e.wasClean) {
            console.info("MatchGroup websocket disconnected cleanly.")
            resolve()
            return
          }

          // Print status error
          if (e.code === 4000) {
            this.matchGroupWebsocketStatus = WebsocketStatus.ERROR
            console.error("Server rejected websocket connection")
            reject()
            return
          }

          // Terminate connection
          if (this.matchGroupWebsocketConnectCounter >= 10) {
            this.matchGroupWebsocketStatus = WebsocketStatus.ERROR
            console.error("Failed to (re)connect MatchGroup websocket!")
            reject()
            return
          }

          // Reconnect
          let timeout = this.matchGroupWebsocketConnectCounter * 2
          console.warn(
            `MatchGroup websocket connection closed unexpectedly. Trying to reconnect (${timeout}s.)`
          )
          this.matchGroupWebsocketStatus = WebsocketStatus.RECONNECTING
          this.matchGroupWebsocketTimeout = setTimeout(
            this.connectMatchGroupWebsocket,
            timeout * 1000
          )
        }
      })
    },
  },

  beforeDestroy() {
    // Always close the websocket connection when leaving the site
    if (this.matchGroupWebsocket) {
      this.matchGroupWebsocket.close()
      this.matchGroupWebsocketStatus = WebsocketStatus.CLOSED

      // Cancel reconnection attempt when leaving the site
      if (this.matchGroupWebsocketTimeout) {
        clearTimeout(this.matchGroupWebsocketTimeout)
      }
    }
  },
}
