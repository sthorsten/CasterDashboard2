/**
 * Gets the map, that is being played in a given matchMaps
 */

import axios from "axios"

export const CurrentMap = {
    data() {
        return {
            currentMap: null
        }
    },

    methods: {
        getCurrentMap() {
            axios.get(`${this.$store.state.backendURL}/api/matches/maps/?match=${this.matchID}&status=2`, this.$store.getters.authHeader
            ).then((response) => {
                if (response.data.length > 0) {
                    this.currentMap = response.data[0]
                    console.debug("Current map => ", this.currentMap)
                } else {
                    console.warn("No current map!")
                }
            }).catch((error) => {
                console.error("Axios error => ", error.response)
            })
        }
    },

    created() {
        this.getCurrentMap()
    }
}