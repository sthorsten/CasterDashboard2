/**
 * Sets the URL scheme from http:// to ws:// and https:// to wss://
 */

export const WebsocketURL = {
    getURL(config) {
        let baseURL = config.baseURL.split("://")[1]

        if (location.protocol === "http:") {
            return "ws://" + baseURL
        } else if (location.protocol === "https:") {
            return "wss://" + baseURL
        }
    }
}
