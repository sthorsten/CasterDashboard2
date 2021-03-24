/**
 * Sets the URL scheme from http:// to ws:// and https:// to wss://
 */

export const WebsocketURL = {
    getURL(config) {
        let websocketBaseURL = ""
        let baseURL = ""

        if (config.baseURL){
            baseURL = config.baseURL.split("://")[1]

            if (location.protocol === "http:") {
                websocketBaseURL = "ws://" + baseURL
            } else if (location.protocol === "https:") {
                websocketBaseURL =  "wss://" + baseURL
            }

        } else {
            if (location.protocol === "http:") {
                websocketBaseURL = "ws://" + location.host
            } else if (location.protocol === "https:") {
                websocketBaseURL =  "wss://" + location.host
            }
        }

        return websocketBaseURL
    }
}
